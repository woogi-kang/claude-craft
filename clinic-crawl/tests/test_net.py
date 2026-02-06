"""Tests for network security utilities."""

from __future__ import annotations

import ipaddress
import time
from unittest.mock import AsyncMock

import httpx
import pytest

from clinic_crawl.net import (
    DomainRateLimiter,
    _get_with_safe_redirects,
    _is_blocked_addr,
    check_response_size,
    is_private_ip,
    validate_url,
)


class TestIsPrivateIp:
    async def test_localhost_ipv4(self):
        assert await is_private_ip("127.0.0.1") is True

    async def test_localhost_ipv6(self):
        assert await is_private_ip("::1") is True

    async def test_rfc1918_10(self):
        assert await is_private_ip("10.0.0.1") is True

    async def test_rfc1918_172(self):
        assert await is_private_ip("172.16.0.1") is True

    async def test_rfc1918_192(self):
        assert await is_private_ip("192.168.1.1") is True

    async def test_link_local(self):
        assert await is_private_ip("169.254.169.254") is True

    async def test_public_ip(self):
        assert await is_private_ip("8.8.8.8") is False

    async def test_public_ip_2(self):
        assert await is_private_ip("1.1.1.1") is False


class TestIsBlockedAddr:
    """Tests for _is_blocked_addr including IPv4-mapped IPv6 bypass."""

    def test_ipv4_localhost(self):
        assert _is_blocked_addr(ipaddress.ip_address("127.0.0.1")) is True

    def test_ipv4_public(self):
        assert _is_blocked_addr(ipaddress.ip_address("8.8.8.8")) is False

    def test_ipv6_localhost(self):
        assert _is_blocked_addr(ipaddress.ip_address("::1")) is True

    def test_ipv4_mapped_ipv6_localhost(self):
        """IPv4-mapped IPv6 like ::ffff:127.0.0.1 must be blocked."""
        addr = ipaddress.ip_address("::ffff:127.0.0.1")
        assert _is_blocked_addr(addr) is True

    def test_ipv4_mapped_ipv6_private(self):
        """IPv4-mapped IPv6 like ::ffff:10.0.0.1 must be blocked."""
        addr = ipaddress.ip_address("::ffff:10.0.0.1")
        assert _is_blocked_addr(addr) is True

    def test_ipv4_mapped_ipv6_metadata(self):
        """IPv4-mapped IPv6 like ::ffff:169.254.169.254 must be blocked."""
        addr = ipaddress.ip_address("::ffff:169.254.169.254")
        assert _is_blocked_addr(addr) is True

    def test_ipv4_mapped_ipv6_public(self):
        """IPv4-mapped IPv6 for public IPs should be allowed."""
        addr = ipaddress.ip_address("::ffff:8.8.8.8")
        assert _is_blocked_addr(addr) is False

    def test_ipv6_unique_local(self):
        assert _is_blocked_addr(ipaddress.ip_address("fc00::1")) is True

    def test_ipv6_link_local(self):
        assert _is_blocked_addr(ipaddress.ip_address("fe80::1")) is True


class TestValidateUrl:
    async def test_valid_https(self):
        assert await validate_url("https://example.com") is None

    async def test_valid_http(self):
        assert await validate_url("http://example.com") is None

    async def test_blocked_scheme_ftp(self):
        result = await validate_url("ftp://example.com/file")
        assert result is not None
        assert "blocked_scheme" in result

    async def test_blocked_scheme_file(self):
        result = await validate_url("file:///etc/passwd")
        assert result is not None
        assert "blocked_scheme" in result

    async def test_private_ip_localhost(self):
        result = await validate_url("http://127.0.0.1/admin")
        assert result is not None
        assert "blocked_private_ip" in result

    async def test_private_ip_metadata(self):
        result = await validate_url("http://169.254.169.254/latest/meta-data/")
        assert result is not None
        assert "blocked_private_ip" in result

    async def test_private_ip_rfc1918(self):
        result = await validate_url("http://192.168.1.1/")
        assert result is not None
        assert "blocked_private_ip" in result

    async def test_missing_host(self):
        result = await validate_url("http://")
        assert result is not None

    async def test_invalid_url(self):
        result = await validate_url("")
        assert result is not None


class TestCheckResponseSize:
    def test_within_limit(self):
        response = httpx.Response(200, content=b"small", headers={})
        assert check_response_size(response, 1000) is True

    def test_exceeds_content_length_header(self):
        response = httpx.Response(200, content=b"x", headers={"content-length": "999999"})
        assert check_response_size(response, 100) is False

    def test_exceeds_body_size(self):
        response = httpx.Response(200, content=b"x" * 200, headers={})
        assert check_response_size(response, 100) is False

    def test_content_length_within_but_body_exceeds(self):
        """Body size check catches chunked responses without accurate Content-Length."""
        response = httpx.Response(200, content=b"x" * 200, headers={"content-length": "50"})
        assert check_response_size(response, 100) is False


class TestGetWithSafeRedirects:
    """Tests for manual redirect following with SSRF validation."""

    async def test_no_redirect(self):
        """Non-redirect response returned directly."""
        mock_response = httpx.Response(200, request=httpx.Request("GET", "https://example.com"))
        client = AsyncMock(spec=httpx.AsyncClient)
        client.get = AsyncMock(return_value=mock_response)

        result = await _get_with_safe_redirects(client, "https://example.com")
        assert result.status_code == 200

    async def test_redirect_to_public_url(self):
        """Safe redirect is followed."""
        redirect_response = httpx.Response(
            302,
            headers={"location": "https://safe.example.com/page"},
            request=httpx.Request("GET", "https://example.com"),
        )
        final_response = httpx.Response(
            200, request=httpx.Request("GET", "https://safe.example.com/page")
        )
        client = AsyncMock(spec=httpx.AsyncClient)
        client.get = AsyncMock(side_effect=[redirect_response, final_response])

        result = await _get_with_safe_redirects(client, "https://example.com")
        assert result.status_code == 200

    async def test_redirect_to_private_ip_blocked(self):
        """Redirect to private IP is blocked."""
        redirect_response = httpx.Response(
            302,
            headers={"location": "http://127.0.0.1/admin"},
            request=httpx.Request("GET", "https://example.com"),
        )
        client = AsyncMock(spec=httpx.AsyncClient)
        client.get = AsyncMock(return_value=redirect_response)

        with pytest.raises(ValueError, match="blocked"):
            await _get_with_safe_redirects(client, "https://example.com")

    async def test_redirect_to_metadata_blocked(self):
        """Redirect to cloud metadata endpoint is blocked."""
        redirect_response = httpx.Response(
            302,
            headers={"location": "http://169.254.169.254/latest/meta-data/"},
            request=httpx.Request("GET", "https://example.com"),
        )
        client = AsyncMock(spec=httpx.AsyncClient)
        client.get = AsyncMock(return_value=redirect_response)

        with pytest.raises(ValueError, match="blocked"):
            await _get_with_safe_redirects(client, "https://example.com")

    async def test_redirect_empty_location(self):
        """Empty location header stops redirect chain."""
        response = httpx.Response(
            302,
            headers={"location": ""},
            request=httpx.Request("GET", "https://example.com"),
        )
        client = AsyncMock(spec=httpx.AsyncClient)
        client.get = AsyncMock(return_value=response)

        result = await _get_with_safe_redirects(client, "https://example.com")
        assert result.status_code == 302


class TestDomainRateLimiter:
    async def test_first_request_no_delay(self):
        limiter = DomainRateLimiter(requests_per_second=10.0)
        start = time.monotonic()
        await limiter.acquire("https://example.com/page1")
        elapsed = time.monotonic() - start
        assert elapsed < 0.1

    async def test_rate_limits_same_domain(self):
        limiter = DomainRateLimiter(requests_per_second=10.0)
        await limiter.acquire("https://example.com/page1")
        start = time.monotonic()
        await limiter.acquire("https://example.com/page2")
        elapsed = time.monotonic() - start
        assert elapsed >= 0.05  # At least ~0.1s interval at 10 rps

    async def test_different_domains_independent(self):
        limiter = DomainRateLimiter(requests_per_second=2.0)
        await limiter.acquire("https://a.com/page")
        start = time.monotonic()
        await limiter.acquire("https://b.com/page")
        elapsed = time.monotonic() - start
        assert elapsed < 0.1  # Different domain, no waiting

    async def test_invalid_url_no_error(self):
        limiter = DomainRateLimiter()
        await limiter.acquire("")  # Should not raise
