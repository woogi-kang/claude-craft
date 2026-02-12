"""URL classification, tracking parameter removal, and normalization."""

from __future__ import annotations

import re
from urllib.parse import parse_qs, urlencode, urlparse, urlunparse

from clinic_crawler.constants import PLATFORM_PATTERNS, TRACKING_PARAMS


def classify_url(url: str) -> str | None:
    """Classify a URL into a social platform name."""
    if not url:
        return None
    # Exclude YouTube individual video URLs (not channel-level social links)
    if re.search(r"youtube\.com/(embed|watch|shorts)[\?/]", url, re.IGNORECASE):
        return None
    if re.search(r"youtu\.be/", url, re.IGNORECASE):
        return None
    for platform, patterns in PLATFORM_PATTERNS.items():
        for pat in patterns:
            if re.search(pat, url, re.IGNORECASE):
                return platform
    if url.startswith("tel:"):
        return "Phone"
    if url.startswith("sms:"):
        return "SMS"
    return None


def strip_tracking(url: str) -> str:
    """Remove tracking parameters from URL."""
    try:
        parsed = urlparse(url)
        params = parse_qs(parsed.query)
        clean = {k: v for k, v in params.items() if k not in TRACKING_PARAMS}
        return urlunparse(parsed._replace(query=urlencode(clean, doseq=True)))
    except Exception:
        return url


def normalize_url(url: str) -> str:
    """Normalize URL for dedup: strip tracking, lowercase host, strip trailing slash, normalize phone."""
    if url.startswith("tel:") or url.startswith("sms:"):
        prefix = url[:4]
        return prefix + re.sub(r"[-.\s()+]", "", url[4:])
    url = strip_tracking(url)
    try:
        parsed = urlparse(url)
        host = parsed.netloc.lower()
        path = parsed.path.rstrip("/") or "/"
        # Strip YouTube channel suffixes for dedup (/videos, /featured, /about)
        if "youtube.com" in host:
            path = re.sub(r"/(videos|featured|about|playlists|community|channels)$", "", path)
        return urlunparse(parsed._replace(netloc=host, path=path))
    except Exception:
        return url
