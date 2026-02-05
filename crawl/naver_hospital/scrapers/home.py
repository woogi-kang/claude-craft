"""
Home page scraper: extract basic info from m.place.naver.com.

Scrapes: name, category, address, phone, business hours, facilities.
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

HOME_URL = "https://m.place.naver.com/hospital/{place_id}/home"


async def scrape_home(
    page: Page,
    place_id: str,
    config: CrawlerConfig,
) -> dict[str, Any]:
    """Scrape the hospital home page.

    Args:
        page: Playwright page instance.
        place_id: Naver Place ID.
        config: Crawler configuration.

    Returns:
        Dict with keys: name, category, road_address, phone,
        business_hours, facilities, image_urls.
    """
    place_id = validate_place_id(place_id)
    url = HOME_URL.format(place_id=place_id)
    logger.info("Scraping home page: %s", url)

    try:
        response = await page.goto(url, wait_until="domcontentloaded")
    except (PlaywrightError, TimeoutError) as exc:
        logger.error("Navigation failed for home %s: %s", place_id, exc)
        return {"id": place_id}

    if response and response.status >= 400:
        logger.warning("HTTP %d for home %s", response.status, place_id)
        return {"id": place_id}

    await check_for_ban(page, response)
    await page_load_delay(config.delays, config.delay_multiplier)

    data: dict[str, Any] = {"id": place_id}

    # Extract basic info
    data["name"] = await _extract_name(page)
    data["category"] = await _extract_category(page)
    data["road_address"] = await _extract_address(page)
    data["phone"] = await _extract_phone(page)

    await action_delay(config.delays, config.delay_multiplier)

    # Extract structured data
    data["business_hours"] = await _extract_business_hours(page)
    data["facilities"] = await _extract_facilities(page)
    data["image_urls"] = await _extract_images(page)

    # Data completeness check
    if not data.get("name"):
        logger.warning(
            "Incomplete scrape for place %s: name missing. "
            "Page may have changed or been blocked.",
            place_id,
        )

    logger.info(
        "Home scraped for '%s': hours=%d, facilities=%d, images=%d",
        data.get("name", "?"),
        len(data.get("business_hours", [])),
        len(data.get("facilities", [])),
        len(data.get("image_urls", [])),
    )
    return data


async def _extract_name(page: Page) -> Optional[str]:
    """Extract hospital name from header."""
    selectors = [
        "span.GHAhO",
        "#_title .Fc1rA",
        "h2.place_section_header",
        "[class*='name']",
    ]
    for sel in selectors:
        el = await page.query_selector(sel)
        if el:
            text = (await el.inner_text()).strip()
            if text:
                return text
    return None


async def _extract_category(page: Page) -> str:
    """Extract category text."""
    selectors = [
        "span.lnJFt",
        "[class*='category']",
        ".place_section_header + span",
    ]
    for sel in selectors:
        el = await page.query_selector(sel)
        if el:
            text = (await el.inner_text()).strip()
            if text:
                return text
    return "병원"


async def _extract_address(page: Page) -> Optional[str]:
    """Extract road address."""
    selectors = [
        "span.LDgIH",
        "[class*='addr']",
        "[class*='address']",
    ]
    for sel in selectors:
        el = await page.query_selector(sel)
        if el:
            text = (await el.inner_text()).strip()
            if text:
                return text
    return None


async def _extract_phone(page: Page) -> Optional[str]:
    """Extract phone number."""
    selectors = [
        "span.xlx7Q",
        'a[href^="tel:"]',
        "[class*='phone']",
    ]
    for sel in selectors:
        el = await page.query_selector(sel)
        if el:
            text = (await el.inner_text()).strip()
            if not text:
                href = await el.get_attribute("href")
                if href and href.startswith("tel:"):
                    text = href.replace("tel:", "")
            if text and re.search(r"\d", text):
                return text
    return None


async def _extract_business_hours(page: Page) -> list[dict[str, Any]]:
    """Extract business hours from the expandable section."""
    hours: list[dict[str, Any]] = []

    # Try clicking the hours expand button
    expand_selectors = [
        "[class*='bizHour'] button",
        "[class*='time'] button",
        "a.gKP9i",
    ]
    for sel in expand_selectors:
        btn = await page.query_selector(sel)
        if btn:
            try:
                await btn.click()
                await page.wait_for_timeout(500)
            except (PlaywrightError, TimeoutError) as exc:
                logger.debug("Could not expand business hours: %s", exc)
            break

    # Parse hours rows
    row_selectors = [
        "[class*='bizHour'] tr",
        "[class*='operationTime'] li",
        ".place_section_content table tr",
    ]

    for sel in row_selectors:
        rows = await page.query_selector_all(sel)
        if not rows:
            continue

        for row in rows:
            text = (await row.inner_text()).strip()
            if not text:
                continue

            parsed = _parse_hour_row(text)
            if parsed:
                hours.append(parsed)

        if hours:
            break

    return hours


def _parse_hour_row(text: str) -> Optional[dict[str, Any]]:
    """Parse a single business hour row text.

    Expected formats:
    - '월요일 09:00 - 18:00'
    - '월 09:00 ~ 18:00 (점심 13:00 ~ 14:00)'
    - '토요일 휴무'
    """
    day_map = {
        "월": "MON", "월요일": "MON",
        "화": "TUE", "화요일": "TUE",
        "수": "WED", "수요일": "WED",
        "목": "THU", "목요일": "THU",
        "금": "FRI", "금요일": "FRI",
        "토": "SAT", "토요일": "SAT",
        "일": "SUN", "일요일": "SUN",
        "공휴일": "HOLIDAY",
    }

    # Find the day
    day = None
    for kor, eng in day_map.items():
        if text.startswith(kor):
            day = eng
            text = text[len(kor):].strip()
            break

    if not day:
        return None

    # Check for day off
    if "휴무" in text or "정기휴무" in text or "쉽니다" in text:
        return {"day_of_week": day, "is_day_off": True}

    # Extract times
    time_pattern = re.compile(r"(\d{2}:\d{2})")
    times = time_pattern.findall(text)

    result: dict[str, Any] = {"day_of_week": day, "is_day_off": False}

    if len(times) >= 2:
        result["open_time"] = times[0]
        result["close_time"] = times[1]

    # Detect break time: explicit keywords OR 4 time values
    has_break_keyword = any(kw in text for kw in ("점심", "브레이크", "휴게"))
    if len(times) >= 4:
        if has_break_keyword:
            result["break_start"] = times[2]
            result["break_end"] = times[3]
        else:
            # Split sessions: 09:00-13:00, 14:00-18:00
            result["close_time"] = times[3]
            result["break_start"] = times[1]
            result["break_end"] = times[2]

    return result if "open_time" in result or result.get("is_day_off") else None


async def _extract_facilities(page: Page) -> list[str]:
    """Extract facility tags (parking, wifi, etc.)."""
    facilities: list[str] = []

    selectors = [
        "[class*='facility'] li",
        "[class*='convenience'] span",
        ".place_section_content .chip",
    ]

    for sel in selectors:
        elements = await page.query_selector_all(sel)
        for el in elements:
            text = (await el.inner_text()).strip()
            if text and text not in facilities:
                facilities.append(text)
        if facilities:
            break

    return facilities


ALLOWED_IMAGE_DOMAINS = ["pstatic.net", "naver.net", "navercorp.com"]


async def _extract_images(page: Page) -> list[str]:
    """Extract thumbnail image URLs from the home page."""
    urls: list[str] = []

    img_elements = await page.query_selector_all(
        "[class*='place_thumb'] img, [class*='photo'] img, .K0PDV img"
    )
    for img in img_elements:
        src = await img.get_attribute("src")
        if src and any(domain in src for domain in ALLOWED_IMAGE_DOMAINS):
            clean = re.sub(r"\?type=.*$", "", src)
            if clean not in urls:
                urls.append(clean)

    return urls
