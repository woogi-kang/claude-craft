"""
Human behavior simulation for anti-detection.

Provides realistic delays, scrolling, typing, and mouse movement
to avoid bot detection by Naver's anti-scraping systems.
"""

from __future__ import annotations

import asyncio
import logging
import random
import sys
import time

from playwright.async_api import Page

from crawl.config import DelayConfig

logger = logging.getLogger(__name__)


async def random_delay(min_s: float, max_s: float, multiplier: float = 1.0) -> None:
    """Sleep for a random duration between min and max seconds."""
    if min_s > max_s:
        min_s, max_s = max_s, min_s
    delay = random.uniform(min_s, max_s) * max(multiplier, 0.0)
    await asyncio.sleep(delay)


async def page_load_delay(config: DelayConfig, multiplier: float = 1.0) -> None:
    """Wait after a page navigation."""
    await random_delay(config.page_load_min, config.page_load_max, multiplier)


async def action_delay(config: DelayConfig, multiplier: float = 1.0) -> None:
    """Wait between user actions (clicks, scrolls)."""
    await random_delay(config.action_min, config.action_max, multiplier)


async def between_places_delay(config: DelayConfig, multiplier: float = 1.0) -> None:
    """Wait between crawling different places."""
    await random_delay(
        config.between_places_min, config.between_places_max, multiplier
    )


async def human_type(
    page: Page,
    selector: str,
    text: str,
    config: DelayConfig,
    clear_first: bool = True,
) -> None:
    """Type text character by character with variable inter-key delays."""
    await page.click(selector)
    await asyncio.sleep(random.uniform(0.2, 0.5))

    if clear_first:
        modifier = "Meta" if sys.platform == "darwin" else "Control"
        await page.keyboard.press(f"{modifier}+a")
        await asyncio.sleep(random.uniform(0.05, 0.15))
        await page.keyboard.press("Backspace")
        await asyncio.sleep(random.uniform(0.1, 0.3))

    for char in text:
        await page.keyboard.type(char)
        delay_ms = random.randint(config.typing_min_ms, config.typing_max_ms)
        await asyncio.sleep(delay_ms / 1000.0)


async def human_scroll(
    page: Page,
    direction: str = "down",
    distance: int | None = None,
) -> None:
    """Scroll page with variable speed and occasional pauses."""
    if distance is None:
        distance = random.randint(300, 800)

    dy = distance if direction == "down" else -distance

    # Scroll in 2-4 smaller chunks for realism
    chunks = random.randint(2, 4)
    chunk_size = dy // chunks
    remainder = dy % chunks

    for i in range(chunks):
        extra = 1 if i < abs(remainder) else 0
        step = chunk_size + (extra if dy > 0 else -extra)
        await page.mouse.wheel(0, step)
        await asyncio.sleep(random.uniform(0.1, 0.3))

    # Occasional small overshoot correction
    if random.random() < 0.3:
        await asyncio.sleep(random.uniform(0.2, 0.5))
        correction = random.randint(20, 80)
        await page.mouse.wheel(0, -correction if direction == "down" else correction)


async def scroll_to_bottom(
    page: Page,
    max_scrolls: int = 50,
    timeout_seconds: float = 120.0,
) -> int:
    """Scroll to bottom with infinite scroll detection.

    Returns the number of scrolls performed.
    """
    previous_height = 0
    stable_count = 0
    scroll_count = 0

    try:
        async with asyncio.timeout(timeout_seconds):
            for _ in range(max_scrolls):
                await human_scroll(page, "down", random.randint(500, 1000))
                await asyncio.sleep(random.uniform(1.0, 2.0))

                try:
                    current_height = await page.evaluate(
                        "document.body.scrollHeight"
                    )
                except Exception:
                    logger.debug("Failed to evaluate scroll height")
                    break

                scroll_count += 1

                if current_height == previous_height:
                    stable_count += 1
                    if stable_count >= 3:
                        break
                else:
                    stable_count = 0
                    previous_height = current_height
    except TimeoutError:
        logger.warning(
            "scroll_to_bottom timed out after %.1fs (%d scrolls)",
            timeout_seconds,
            scroll_count,
        )

    return scroll_count


class RequestThrottler:
    """Enforces minimum time between requests (concurrency-safe)."""

    def __init__(self, min_interval: float = 3.0, multiplier: float = 1.0) -> None:
        self._min_interval = min_interval * max(multiplier, 0.0)
        self._last_request_time: float = 0
        self._lock: asyncio.Lock | None = None

    def _get_lock(self) -> asyncio.Lock:
        """Lazily create lock inside event loop."""
        if self._lock is None:
            self._lock = asyncio.Lock()
        return self._lock

    async def wait(self) -> None:
        """Wait until enough time has passed since last request."""
        async with self._get_lock():
            now = time.monotonic()
            elapsed = now - self._last_request_time
            if elapsed < self._min_interval:
                wait_time = self._min_interval - elapsed
                wait_time += random.uniform(0, 0.5)
                logger.debug("Throttler waiting %.2fs", wait_time)
                await asyncio.sleep(wait_time)
            self._last_request_time = time.monotonic()
