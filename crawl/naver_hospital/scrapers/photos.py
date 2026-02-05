"""
Photo page scraper: extract photo URLs with infinite scroll.

Navigates to the photo tab, scrolls to load all images,
and collects URLs while filtering out video content.
"""

from __future__ import annotations

import logging
import re

from playwright.async_api import Error as PlaywrightError, Page

from crawl.config import CrawlerConfig
from crawl.naver_hospital.human_behavior import (
    action_delay,
    page_load_delay,
    scroll_to_bottom,
)
from crawl.naver_hospital.scrapers.detection import (
    BanDetectedError,
    check_for_ban,
    validate_place_id,
)

logger = logging.getLogger(__name__)

PHOTO_URL = "https://m.place.naver.com/hospital/{place_id}/photo"

# Video indicators in URLs
VIDEO_PATTERNS = [
    re.compile(r"video", re.IGNORECASE),
    re.compile(r"\.mp4", re.IGNORECASE),
    re.compile(r"\.webm", re.IGNORECASE),
    re.compile(r"play_icon", re.IGNORECASE),
]

ALLOWED_IMAGE_DOMAINS = ["pstatic.net", "naver.net", "navercorp.com"]


async def scrape_photos(
    page: Page,
    place_id: str,
    config: CrawlerConfig,
) -> list[str]:
    """Scrape photo URLs from the hospital photo page.

    Handles infinite scroll pagination and filters out videos.

    Args:
        page: Playwright page instance.
        place_id: Naver Place ID.
        config: Crawler configuration.

    Returns:
        List of unique photo URLs.
    """
    place_id = validate_place_id(place_id)
    url = PHOTO_URL.format(place_id=place_id)
    logger.info("Scraping photos: %s", url)

    try:
        response = await page.goto(url, wait_until="domcontentloaded")
    except (PlaywrightError, TimeoutError) as exc:
        logger.error("Navigation failed for photos %s: %s", place_id, exc)
        return []

    if response and response.status >= 400:
        logger.warning("HTTP %d for photos %s", response.status, place_id)
        return []

    await check_for_ban(page, response)
    await page_load_delay(config.delays, config.delay_multiplier)

    # Check if photo page exists
    no_content = await page.query_selector("[class*='no_data'], [class*='empty']")
    if no_content:
        logger.info("No photos found for place %s", place_id)
        return []

    await action_delay(config.delays, config.delay_multiplier)

    # Scroll to load all photos (infinite scroll)
    scroll_count = await scroll_to_bottom(
        page, max_scrolls=config.photos.max_scroll_attempts
    )
    logger.debug("Scrolled %d times for place %s", scroll_count, place_id)

    # Wait for lazy-loaded images to resolve
    await page.wait_for_timeout(2000)
    try:
        await page.wait_for_load_state("networkidle", timeout=5000)
    except TimeoutError:
        logger.debug("Network did not reach idle after scrolling for %s", place_id)

    # Collect all image URLs
    photo_urls = await _collect_photo_urls(page, config)

    logger.info(
        "Collected %d photos for place %s (scrolled %d times)",
        len(photo_urls),
        place_id,
        scroll_count,
    )
    return photo_urls


async def _collect_photo_urls(
    page: Page,
    config: CrawlerConfig,
) -> list[str]:
    """Extract unique photo URLs from loaded content."""
    seen: set[str] = set()
    urls: list[str] = []

    # Main photo grid selectors
    img_selectors = [
        "[class*='photo'] img",
        "[class*='grid'] img",
        ".place_section_content img",
        "img[src*='pstatic.net']",
    ]

    for selector in img_selectors:
        elements = await page.query_selector_all(selector)
        for el in elements:
            src = await el.get_attribute("src")
            if not src:
                src = await el.get_attribute("data-src")
            if not src:
                continue

            # Only allow known image CDN domains
            if not any(domain in src for domain in ALLOWED_IMAGE_DOMAINS):
                continue

            # Filter out videos
            if _is_video(src):
                continue

            clean_url = _normalize_photo_url(src)
            if clean_url and clean_url not in seen:
                seen.add(clean_url)
                urls.append(clean_url)

                if len(urls) >= config.photos.max_photos_per_place:
                    break

        if urls:
            break

    # Also check for video overlays and remove those entries
    if config.photos.exclude_video:
        urls = await _filter_video_items(page, urls)

    return urls


def _is_video(src: str) -> bool:
    """Check if a source URL belongs to video content."""
    for pattern in VIDEO_PATTERNS:
        if pattern.search(src):
            return True
    return False


async def _filter_video_items(page: Page, urls: list[str]) -> list[str]:
    """Remove URLs that belong to video content by checking parent elements."""
    video_containers = await page.query_selector_all(
        "[class*='video'], [class*='play'], [data-type='video']"
    )

    video_srcs: set[str] = set()
    for container in video_containers:
        imgs = await container.query_selector_all("img")
        for img in imgs:
            src = await img.get_attribute("src")
            if src:
                video_srcs.add(_normalize_photo_url(src))

    return [u for u in urls if u not in video_srcs]


def _normalize_photo_url(url: str) -> str:
    """Remove size/quality parameters for full resolution URL."""
    # Naver uses ?type=xxx for image sizing - primary pattern
    url = re.sub(r"\?type=[^&]*$", "", url)
    if url.startswith("//"):
        url = f"https:{url}"
    return url
