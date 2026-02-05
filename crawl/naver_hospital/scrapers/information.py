"""
Information page scraper: extract details from /information tab.

Scrapes: description, parking info, YouTube URL, Instagram URL,
reservation URL, and homepage URL.
"""

from __future__ import annotations

import logging
import re
from typing import Any, Optional

from playwright.async_api import Error as PlaywrightError, Page

from crawl.config import CrawlerConfig
from crawl.naver_hospital.human_behavior import action_delay, page_load_delay
from crawl.naver_hospital.scrapers.detection import (
    BanDetectedError,
    check_for_ban,
    validate_place_id,
)

logger = logging.getLogger(__name__)

INFO_URL = "https://m.place.naver.com/hospital/{place_id}/information"


async def scrape_information(
    page: Page,
    place_id: str,
    config: CrawlerConfig,
) -> dict[str, Any]:
    """Scrape the hospital information page.

    Args:
        page: Playwright page instance.
        place_id: Naver Place ID.
        config: Crawler configuration.

    Returns:
        Dict with keys: description, parking_info, youtube_url,
        instagram_url, reservation_url, homepage_url.
    """
    place_id = validate_place_id(place_id)
    url = INFO_URL.format(place_id=place_id)
    logger.info("Scraping information page: %s", url)

    try:
        response = await page.goto(url, wait_until="domcontentloaded")
    except (PlaywrightError, TimeoutError) as exc:
        logger.error("Navigation failed for info %s: %s", place_id, exc)
        return {}

    if response and response.status >= 400:
        logger.warning("HTTP %d for info %s", response.status, place_id)
        return {}

    await check_for_ban(page, response)
    await page_load_delay(config.delays, config.delay_multiplier)

    data: dict[str, Any] = {}

    data["description"] = await _extract_description(page)

    await action_delay(config.delays, config.delay_multiplier)

    data["parking_info"] = await _extract_parking(page)
    data["homepage_url"] = await _extract_homepage(page)

    # Extract social media and reservation links (scoped to content)
    links = await _extract_all_links(page)
    data["youtube_url"] = links.get("youtube")
    data["instagram_url"] = links.get("instagram")
    data["reservation_url"] = links.get("reservation")

    logger.info(
        "Information scraped for %s: desc=%s, parking=%s, links=%d",
        place_id,
        "yes" if data.get("description") else "no",
        "yes" if data.get("parking_info") else "no",
        sum(1 for v in links.values() if v),
    )
    return data


async def _extract_description(page: Page) -> Optional[str]:
    """Extract place description/introduction text."""
    selectors = [
        "[class*='desc'] .place_section_content",
        "[class*='intro'] p",
        ".T8RFa",
        "[class*='description']",
    ]

    for sel in selectors:
        el = await page.query_selector(sel)
        if el:
            text = (await el.inner_text()).strip()
            if text and len(text) > 10:
                return text

    return None


async def _extract_parking(page: Page) -> Optional[str]:
    """Extract parking information."""
    elements = await page.query_selector_all(
        "[class*='info'] li, [class*='detail'] li, .place_section_content li"
    )

    for el in elements:
        text = (await el.inner_text()).strip()
        if "주차" in text:
            parking_text = text.replace("주차", "").strip()
            if parking_text.startswith((":", " ")):
                parking_text = parking_text.lstrip(": ")
            return parking_text if parking_text else "주차 가능"

    return None


async def _extract_homepage(page: Page) -> Optional[str]:
    """Extract official homepage URL."""
    selectors = [
        'a[href*="http"][class*="homepage"]',
        'a[href*="http"][class*="link"]',
    ]

    for sel in selectors:
        elements = await page.query_selector_all(sel)
        for el in elements:
            href = await el.get_attribute("href")
            if href and _is_homepage_url(href):
                return href

    return None


async def _extract_all_links(page: Page) -> dict[str, Optional[str]]:
    """Extract social media and reservation links from content sections."""
    result: dict[str, Optional[str]] = {
        "youtube": None,
        "instagram": None,
        "reservation": None,
    }

    # Scope to content sections to avoid matching ads/navigation
    content_selectors = [
        ".place_section_content a[href]",
        "[class*='info'] a[href]",
        "[class*='link_section'] a[href]",
    ]

    for content_sel in content_selectors:
        all_links = await page.query_selector_all(content_sel)
        for link in all_links:
            href = await link.get_attribute("href")
            if not href:
                continue

            if not result["youtube"] and _is_youtube_url(href):
                result["youtube"] = href
            if not result["instagram"] and _is_instagram_url(href):
                result["instagram"] = href
            if not result["reservation"] and _is_reservation_url(href):
                result["reservation"] = href

        if all(v is not None for v in result.values()):
            break

    return result


def _is_youtube_url(url: str) -> bool:
    return bool(re.search(r"youtube\.com|youtu\.be", url, re.IGNORECASE))


def _is_instagram_url(url: str) -> bool:
    return bool(re.search(r"instagram\.com", url, re.IGNORECASE))


def _is_reservation_url(url: str) -> bool:
    return "booking.naver.com" in url


_EXCLUDED_HOMEPAGE_DOMAINS = [
    "naver.com", "naver.me",
    "instagram.com", "youtube.com", "youtu.be",
    "facebook.com", "twitter.com", "x.com",
    "tiktok.com", "kakao.com", "band.us",
    "linkedin.com",
]


def _is_homepage_url(url: str) -> bool:
    """Check if URL looks like a business homepage (not social media)."""
    return not any(domain in url.lower() for domain in _EXCLUDED_HOMEPAGE_DOMAINS)
