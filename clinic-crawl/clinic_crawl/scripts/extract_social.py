"""Social link extraction helpers for agent-based deep crawl."""

from __future__ import annotations

import re
from urllib.parse import urljoin

from clinic_crawl.models.enums import ExtractionMethod
from clinic_crawl.models.social import SocialChannels, SocialLink
from clinic_crawl.patterns import WIDGET_SIGNATURES, identify_platform


def clean_social_url(url: str) -> str:
    """Clean and normalize a social URL."""
    # Remove trailing punctuation and quotes
    url = url.rstrip("\"'<>);,. ")
    # Remove tracking parameters for cleaner URLs
    if "?" in url:
        base, params = url.split("?", 1)
        # Keep only essential params (some KakaoTalk links need them)
        if "kakao" in base.lower():
            return url
        return base
    return url


def parse_social_from_html(
    html: str,
    base_url: str,
    extraction_method: ExtractionMethod = ExtractionMethod.DOM_STATIC,
) -> list[SocialLink]:
    """Extract social links from HTML content.

    Args:
        html: Raw HTML string
        base_url: Base URL for resolving relative links
        extraction_method: How the HTML was obtained
    """
    links: list[SocialLink] = []
    seen: set[str] = set()

    # Extract all href and src attributes
    url_pattern = re.compile(
        r'(?:href|src|data-url|data-link|onclick)\s*=\s*["\']([^"\']+)["\']',
        re.IGNORECASE,
    )

    for match in url_pattern.finditer(html):
        raw_url = match.group(1)

        # Resolve relative URLs
        if raw_url.startswith("/") or not raw_url.startswith("http"):
            raw_url = urljoin(base_url, raw_url)

        platform = identify_platform(raw_url)
        if platform is None:
            continue

        cleaned = clean_social_url(raw_url)
        if cleaned in seen:
            continue
        seen.add(cleaned)

        links.append(
            SocialLink(
                platform=platform,
                url=cleaned,
                extraction_method=extraction_method,
                confidence=0.9 if extraction_method == ExtractionMethod.DOM_STATIC else 0.85,
            )
        )

    return links


def detect_chat_widgets(html: str) -> bool:
    """Detect if the page has embedded chat widgets (Kakao Channel, etc.)."""
    html_lower = html.lower()
    return any(sig.lower() in html_lower for sig in WIDGET_SIGNATURES)


def detect_qr_images(html: str) -> list[str]:
    """Find potential QR code images in HTML."""
    qr_urls: list[str] = []
    # Look for img tags with QR-related attributes
    img_pattern = re.compile(
        r'<img[^>]+(?:src|data-src)\s*=\s*["\']([^"\']+)["\'][^>]*>',
        re.IGNORECASE,
    )
    for match in img_pattern.finditer(html):
        src = match.group(1)
        # Check if filename or alt suggests QR
        context = match.group(0).lower()
        if any(kw in context for kw in ("qr", "wechat", "위챗", "큐알")):
            qr_urls.append(src)
    return qr_urls


def build_social_channels(
    links: list[SocialLink],
    chat_widget: bool = False,
    qr_urls: list[str] | None = None,
) -> SocialChannels:
    """Build a SocialChannels object from extracted data."""
    return SocialChannels(
        links=links,
        chat_widget_detected=chat_widget,
        qr_image_urls=qr_urls or [],
    ).deduplicated()
