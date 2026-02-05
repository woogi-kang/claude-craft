"""
Search scraper: find hospital place ID from m.search.naver.com.

Navigates to Naver mobile search, types the hospital name,
and extracts the Naver Place ID from the search results.
"""

from __future__ import annotations

import logging
import re
from typing import Optional
from urllib.parse import quote_plus

from playwright.async_api import Error as PlaywrightError, Page

from crawl.config import CrawlerConfig
from crawl.naver_hospital.human_behavior import (
    action_delay,
    human_scroll,
    page_load_delay,
)
from crawl.naver_hospital.scrapers.detection import (
    BanDetectedError,
    check_for_ban,
)

logger = logging.getLogger(__name__)

SEARCH_URL = "https://m.search.naver.com/search.naver?query={query}"

# Selectors for place results on Naver mobile search
PLACE_LINK_SELECTORS = [
    'a[href*="m.place.naver.com"]',
    'a[href*="place.naver.com"]',
    'a[data-type="place"]',
]

PLACE_ID_PATTERN = re.compile(
    r"place\.naver\.com/(?:hospital|place|restaurant)/(\d+)"
)


async def _find_place_id_in_page(page: Page) -> Optional[str]:
    """Search visible links for a Naver Place ID."""
    for selector in PLACE_LINK_SELECTORS:
        links = await page.query_selector_all(selector)
        for link in links:
            href = await link.get_attribute("href")
            if not href:
                continue
            match = PLACE_ID_PATTERN.search(href)
            if match:
                return match.group(1)
    return None


async def search_place(
    page: Page,
    hospital_name: str,
    config: CrawlerConfig,
) -> Optional[str]:
    """Search Naver and extract the place ID for a hospital.

    Args:
        page: Playwright page instance.
        hospital_name: Hospital name to search for.
        config: Crawler configuration.

    Returns:
        Naver Place ID string, or None if not found.
    """
    query = quote_plus(hospital_name)
    url = SEARCH_URL.format(query=query)

    logger.info("Searching for: %s", hospital_name)

    try:
        response = await page.goto(url, wait_until="domcontentloaded")
    except (PlaywrightError, TimeoutError) as exc:
        logger.error("Navigation failed for search '%s': %s", hospital_name, exc)
        return None

    if response and response.status >= 400:
        logger.warning("HTTP %d for search '%s'", response.status, hospital_name)
        return None

    await check_for_ban(page, response)
    await page_load_delay(config.delays, config.delay_multiplier)

    # First attempt
    place_id = await _find_place_id_in_page(page)
    if place_id:
        logger.info("Found place ID: %s for '%s'", place_id, hospital_name)
        return place_id

    # Scroll down and retry (results might be below fold)
    logger.debug("No results in viewport, scrolling for '%s'", hospital_name)
    await human_scroll(page, "down", 800)
    await action_delay(config.delays, config.delay_multiplier)

    place_id = await _find_place_id_in_page(page)
    if place_id:
        logger.info("Found place ID after scroll: %s for '%s'", place_id, hospital_name)
        return place_id

    # Fallback: extract from embedded JSON in page
    place_id = await _extract_from_page_content(page)
    if place_id:
        logger.info("Found place ID from content: %s for '%s'", place_id, hospital_name)
        return place_id

    logger.warning("No place ID found for: %s", hospital_name)
    return None


async def _extract_from_page_content(page: Page) -> Optional[str]:
    """Try to extract place ID from embedded scripts or data attributes."""
    content = await page.content()

    # Targeted patterns anchored to Naver Place context
    patterns = [
        re.compile(r'"placeId"\s*:\s*"(\d{8,})"'),
        re.compile(r"place_id[\"']?\s*[:=]\s*[\"'](\d{8,})[\"']"),
        re.compile(r"placeId[\"']?\s*[:=]\s*[\"'](\d{8,})[\"']"),
    ]

    for pattern in patterns:
        match = pattern.search(content)
        if match:
            return match.group(1)

    return None
