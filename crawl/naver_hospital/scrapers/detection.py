"""
Ban and CAPTCHA detection for Naver scraping.

Detects when Naver has blocked the request with rate limiting,
CAPTCHA, or login redirect instead of serving actual content.
"""

from __future__ import annotations

import logging
from typing import Optional

from playwright.async_api import Page, Response

logger = logging.getLogger(__name__)


class BanDetectedError(Exception):
    """Raised when Naver blocks the request."""

    pass


BAN_URL_INDICATORS = ["captcha", "nidlogin", "auth.naver", "block", "limit"]
BAN_TEXT_INDICATORS = ["비정상적인 접근", "자동 접근", "로봇", "보안 문자", "자동입력방지"]


async def check_for_ban(page: Page, response: Optional[Response]) -> None:
    """Check if current page indicates a ban or CAPTCHA.

    Raises:
        BanDetectedError: If ban or CAPTCHA is detected.
    """
    # Check HTTP status
    if response and response.status in (403, 429, 503):
        raise BanDetectedError(f"HTTP {response.status}")

    current_url = page.url

    # Check for known redirect patterns
    for indicator in BAN_URL_INDICATORS:
        if indicator in current_url.lower():
            raise BanDetectedError(f"Redirected to {current_url}")

    # Check page content for ban messages
    for ban_text in BAN_TEXT_INDICATORS:
        el = await page.query_selector(f"text={ban_text}")
        if el:
            raise BanDetectedError(f"Ban text detected: {ban_text}")


def validate_place_id(place_id: str) -> str:
    """Ensure place_id is a numeric string.

    Raises:
        ValueError: If place_id contains non-numeric characters.
    """
    if not place_id or not place_id.isdigit():
        raise ValueError(f"Invalid place_id: {place_id!r}")
    return place_id
