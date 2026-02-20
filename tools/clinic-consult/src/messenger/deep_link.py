"""Platform-specific deep link URL construction.

Each messenger has a different URL format for opening a chat directly.
"""

from __future__ import annotations

from urllib.parse import urlparse

from src.messenger import normalize_platform


def _has_domain(url: str, *expected_hosts: str) -> bool:
    """Check if a URL's hostname matches one of *expected_hosts* exactly."""
    try:
        host = (urlparse(url).hostname or "").lower()
        return host in expected_hosts
    except Exception:
        return False


def build_chat_url(platform: str, channel_url: str) -> str | None:
    """Build a direct chat URL from a channel/profile URL.

    Parameters
    ----------
    platform:
        ``"kakao"`` or ``"line"``.
    channel_url:
        The raw channel URL stored in the database.

    Returns
    -------
    str | None
        The direct chat URL, or ``None`` if the URL is invalid.
    """
    if not channel_url:
        return None

    key = normalize_platform(platform)
    if key == "kakao":
        return _kakao_chat_url(channel_url)
    if key == "line":
        return _line_chat_url(channel_url)
    return None


def _kakao_chat_url(url: str) -> str | None:
    """Build KakaoTalk Plus Friend chat URL.

    Format: ``https://pf.kakao.com/{id}/chat``
    """
    url = url.strip().rstrip("/")
    # Strip fragment using urlparse for robustness
    parsed = urlparse(url)
    url = parsed._replace(fragment="").geturl().rstrip("/")
    if not _has_domain(url, "pf.kakao.com"):
        return None
    if not url.endswith("/chat"):
        url = f"{url}/chat"
    return url


def _line_chat_url(url: str) -> str | None:
    """Build LINE Official Account chat URL.

    Supports formats:
    - ``https://line.me/R/ti/p/@{id}`` -> ``https://line.me/R/ti/p/@{id}``
    - ``https://lin.ee/{shortcode}`` -> ``https://lin.ee/{shortcode}``
    - ``https://page.line.me/{id}`` -> ``https://line.me/R/ti/p/@{id}``
    - ``@{id}`` -> ``https://line.me/R/ti/p/@{id}``
    """
    url = url.strip()

    # Already a valid LINE deep link
    if url.startswith("https://line.me/R/ti/p/"):
        return url
    if url.startswith("https://lin.ee/"):
        return url

    # page.line.me format -> extract ID
    if _has_domain(url, "page.line.me"):
        parts = url.rstrip("/").rsplit("/", 1)
        line_id = parts[-1] if len(parts) > 1 else ""
        if line_id:
            if not line_id.startswith("@"):
                line_id = f"@{line_id}"
            return f"https://line.me/R/ti/p/{line_id}"
        return None

    # Bare @id format
    if url.startswith("@"):
        return f"https://line.me/R/ti/p/{url}"

    # line.me but not the deep link format
    if _has_domain(url, "line.me"):
        return url

    return None


def validate_channel_url(platform: str, url: str) -> bool:
    """Check if a channel URL is valid for the given platform."""
    if not url:
        return False

    key = normalize_platform(platform)
    if key == "kakao":
        return _has_domain(url, "pf.kakao.com")
    if key == "line":
        return _has_domain(url, "line.me", "lin.ee", "page.line.me") or url.startswith("@")
    return False
