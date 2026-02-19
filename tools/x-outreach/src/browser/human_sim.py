"""Human-like interaction simulation for Playwright pages.

Provides functions that mimic natural mouse movement, scrolling,
typing speed, and pausing to reduce the risk of bot detection.
"""

from __future__ import annotations

import asyncio
import random

from playwright.async_api import Page


async def random_mouse_move(page: Page) -> None:
    """Move the mouse to a random position within the viewport.

    The movement uses a natural-looking speed by adding slight delays.
    """
    viewport = page.viewport_size
    if viewport is None:
        return

    target_x = random.randint(100, viewport["width"] - 100)
    target_y = random.randint(100, viewport["height"] - 100)

    await page.mouse.move(target_x, target_y, steps=random.randint(5, 15))
    await asyncio.sleep(random.uniform(0.1, 0.3))


async def human_scroll(
    page: Page,
    direction: str = "down",
    distance: int | None = None,
) -> None:
    """Scroll the page with natural speed variation.

    Parameters
    ----------
    page:
        The Playwright page to scroll.
    direction:
        ``"down"`` or ``"up"``.
    distance:
        Scroll distance in pixels.  Randomised when ``None``.
    """
    if distance is None:
        distance = random.randint(200, 600)

    delta = distance if direction == "down" else -distance

    # Split into smaller increments for a more natural feel
    increments = random.randint(3, 6)
    per_step = delta / increments

    for _ in range(increments):
        await page.mouse.wheel(0, per_step)
        await asyncio.sleep(random.uniform(0.05, 0.15))

    await asyncio.sleep(random.uniform(0.3, 0.8))


async def human_type(
    page: Page,
    selector: str,
    text: str,
    *,
    min_delay_ms: int = 50,
    max_delay_ms: int = 200,
) -> None:
    """Type *text* into the element matched by *selector* with per-character delays.

    Parameters
    ----------
    page:
        The Playwright page containing the target element.
    selector:
        CSS selector for the input element.
    text:
        The text to type.
    min_delay_ms / max_delay_ms:
        Range of random delays between keystrokes in milliseconds.
    """
    element = await page.wait_for_selector(selector, timeout=10_000)
    if element is None:
        return

    await element.click()
    await asyncio.sleep(random.uniform(0.2, 0.5))

    for char in text:
        await page.keyboard.type(char, delay=random.randint(min_delay_ms, max_delay_ms))


async def random_pause(min_s: float = 1.0, max_s: float = 3.0) -> float:
    """Pause for a random duration.

    Returns the actual number of seconds slept.
    """
    delay = random.uniform(min_s, max_s)
    await asyncio.sleep(delay)
    return delay
