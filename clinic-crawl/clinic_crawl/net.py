"""Network security utilities for safe HTTP requests."""

from __future__ import annotations

import asyncio
import ipaddress
import logging
import socket
import time
from urllib.parse import urljoin, urlparse

import httpx

logger = logging.getLogger(__name__)

_MAX_REDIRECTS = 10


class DomainRateLimiter:
    """Per-domain rate limiter using token bucket algorithm.

    Ensures polite crawling by limiting requests per domain.
    """

    def __init__(self, requests_per_second: float = 2.0) -> None:
        self._rps = requests_per_second
        self._interval = 1.0 / requests_per_second
        self._last_request: dict[str, float] = {}
        self._locks: dict[str, asyncio.Lock] = {}

    def _get_lock(self, domain: str) -> asyncio.Lock:
        return self._locks.setdefault(domain, asyncio.Lock())

    async def acquire(self, url: str) -> None:
        """Wait until a request to this domain is allowed."""
        try:
            domain = urlparse(url).hostname or ""
        except ValueError:
            return

        lock = self._get_lock(domain)
        async with lock:
            now = time.monotonic()
            last = self._last_request.get(domain, 0.0)
            wait = self._interval - (now - last)
            if wait > 0:
                await asyncio.sleep(wait)
            self._last_request[domain] = time.monotonic()


# Max response sizes
MAX_HTML_SIZE = 10 * 1024 * 1024  # 10 MB
MAX_IMAGE_SIZE = 5 * 1024 * 1024  # 5 MB

# Private/internal IP ranges that must be blocked (SSRF protection)
_BLOCKED_NETWORKS = [
    ipaddress.ip_network("10.0.0.0/8"),
    ipaddress.ip_network("172.16.0.0/12"),
    ipaddress.ip_network("192.168.0.0/16"),
    ipaddress.ip_network("169.254.0.0/16"),  # link-local / cloud metadata
    ipaddress.ip_network("127.0.0.0/8"),
    ipaddress.ip_network("0.0.0.0/8"),
    ipaddress.ip_network("::1/128"),
    ipaddress.ip_network("fc00::/7"),  # IPv6 unique local
    ipaddress.ip_network("fe80::/10"),  # IPv6 link-local
]


def _is_blocked_addr(addr: ipaddress.IPv4Address | ipaddress.IPv6Address) -> bool:
    """Check if an IP address falls within any blocked network."""
    # Normalize IPv4-mapped IPv6 (::ffff:x.x.x.x) to IPv4
    if isinstance(addr, ipaddress.IPv6Address) and addr.ipv4_mapped:
        addr = addr.ipv4_mapped
    return any(addr in net for net in _BLOCKED_NETWORKS)


async def is_private_ip(host: str) -> bool:
    """Check if a hostname resolves to a private/internal IP address."""
    try:
        addr = ipaddress.ip_address(host)
        return _is_blocked_addr(addr)
    except ValueError:
        # Not a literal IP - resolve hostname
        try:
            loop = asyncio.get_running_loop()
            results = await loop.getaddrinfo(
                host, None, family=socket.AF_UNSPEC, type=socket.SOCK_STREAM
            )
            for _family, _type, _proto, _canonname, sockaddr in results:
                ip_str = sockaddr[0]
                addr = ipaddress.ip_address(ip_str)
                if _is_blocked_addr(addr):
                    return True
        except (socket.gaierror, OSError):
            pass
    return False


async def validate_url(url: str) -> str | None:
    """Validate a URL for safe external requests.

    Returns an error message if the URL is unsafe, or None if it's safe.
    """
    try:
        parsed = urlparse(url)
    except ValueError:
        return "invalid_url"

    if parsed.scheme not in ("http", "https"):
        return f"blocked_scheme:{parsed.scheme}"

    host = parsed.hostname
    if not host:
        return "missing_host"

    if await is_private_ip(host):
        return f"blocked_private_ip:{host}"

    return None


def check_response_size(response: httpx.Response, max_size: int) -> bool:
    """Check if a response exceeds the maximum allowed size.

    Returns True if the response is within limits.
    Checks both Content-Length header and actual body size.
    """
    content_length = response.headers.get("content-length")
    if content_length is not None:
        try:
            if int(content_length) > max_size:
                return False
        except ValueError:
            pass
    # Post-download check for chunked responses without Content-Length
    if len(response.content) > max_size:
        return False
    return True


async def _get_with_safe_redirects(
    client: httpx.AsyncClient,
    url: str,
    *,
    timeout: float = 10.0,
) -> httpx.Response:
    """Follow redirects manually, validating each destination against SSRF."""
    current_url = url
    for _ in range(_MAX_REDIRECTS):
        response = await client.get(
            current_url,
            follow_redirects=False,
            timeout=timeout,
        )
        if not response.is_redirect:
            return response
        location = response.headers.get("location", "")
        if not location:
            return response
        # Resolve relative redirects
        next_url = urljoin(str(response.url), location)
        error = await validate_url(next_url)
        if error:
            raise ValueError(f"Redirect to {next_url} blocked: {error}")
        current_url = next_url
    raise httpx.TooManyRedirects(
        f"Exceeded {_MAX_REDIRECTS} redirects",
        request=response.request,
    )


async def safe_get(
    client: httpx.AsyncClient,
    url: str,
    *,
    timeout: float = 10.0,
    max_size: int = MAX_HTML_SIZE,
    follow_redirects: bool = True,
) -> httpx.Response:
    """Perform a GET request with SSRF protection and SSL fallback.

    Validates both the initial URL and any redirect destinations against
    private IP ranges. Falls back to verify=False on SSL errors.

    Raises:
        httpx.RequestError: On network errors.
        ValueError: If the URL targets a private IP or response is too large.
    """
    # SSRF check on initial URL
    error = await validate_url(url)
    if error:
        raise ValueError(f"URL blocked: {error}")

    try:
        if follow_redirects:
            response = await _get_with_safe_redirects(client, url, timeout=timeout)
        else:
            response = await client.get(url, follow_redirects=False, timeout=timeout)
    except httpx.ConnectError as exc:
        exc_str = str(exc).lower()
        if "ssl" in exc_str or "certificate" in exc_str or "verify" in exc_str:
            logger.warning("SSL error for %s, retrying without verification", url)
            async with httpx.AsyncClient(
                verify=False,
                headers=dict(client.headers),
            ) as insecure:
                if follow_redirects:
                    response = await _get_with_safe_redirects(
                        insecure,
                        url,
                        timeout=timeout,
                    )
                else:
                    response = await insecure.get(
                        url,
                        follow_redirects=False,
                        timeout=timeout,
                    )
        else:
            raise

    if not check_response_size(response, max_size):
        raise ValueError(f"Response too large (max {max_size} bytes)")

    return response
