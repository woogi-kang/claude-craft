"""Playwright browser launch with stealth patches.

Wraps ``playwright-stealth`` to provide a pre-configured, persistent
browser context that resists basic bot-detection techniques.
"""

from __future__ import annotations

import json
import random
from pathlib import Path

from playwright.async_api import Browser, BrowserContext, Playwright
from playwright_stealth import Stealth

_stealth = Stealth()


_DEFAULT_USER_AGENTS = [
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/131.0.0.0 Safari/537.36"
]


def _load_user_agents(path: Path | None = None) -> list[str]:
    """Load the user-agent pool from a JSON file.

    Returns a sensible default when no file is available.
    """
    if path is None or not path.exists():
        return list(_DEFAULT_USER_AGENTS)
    with open(path, encoding="utf-8") as f:
        agents: list[str] = json.load(f)
    return agents


async def create_stealth_browser(
    playwright: Playwright,
    *,
    headless: bool = True,
    user_data_dir: str | Path | None = None,
    viewport_width: int = 1280,
    viewport_height: int = 720,
    user_agents_path: Path | None = None,
    locale: str = "ja-JP",
    timezone_id: str = "Asia/Tokyo",
    proxy: dict[str, str] | None = None,
) -> tuple[Browser, BrowserContext]:
    """Launch a Chromium browser with stealth patches applied.

    Parameters
    ----------
    playwright:
        A running ``Playwright`` instance (from ``async_playwright``).
    headless:
        Run in headless mode.
    user_data_dir:
        Directory for persistent browser data (cookies, local storage).
        When ``None``, a temporary profile is used.
    viewport_width / viewport_height:
        Browser viewport dimensions.
    user_agents_path:
        Override path for the user-agent pool JSON file.
    locale:
        Browser locale (e.g. ``"ja-JP"``, ``"zh-CN"``).
    timezone_id:
        Browser timezone (e.g. ``"Asia/Tokyo"``, ``"Asia/Shanghai"``).
    proxy:
        Proxy configuration dict with ``server`` key and optional
        ``username``/``password`` keys.  ``None`` means no proxy.

    Returns
    -------
    tuple[Browser, BrowserContext]
        The launched browser and its first context.
    """
    user_agents = _load_user_agents(user_agents_path)
    selected_ua = random.choice(user_agents)

    launch_args = [
        "--disable-blink-features=AutomationControlled",
        "--disable-dev-shm-usage",
        "--no-sandbox",
    ]

    if user_data_dir is not None:
        user_data_dir = Path(user_data_dir)
        user_data_dir.mkdir(parents=True, exist_ok=True)

        context = await playwright.chromium.launch_persistent_context(
            user_data_dir=str(user_data_dir),
            headless=headless,
            args=launch_args,
            viewport={"width": viewport_width, "height": viewport_height},
            user_agent=selected_ua,
            locale=locale,
            timezone_id=timezone_id,
            proxy=proxy,
        )
        # For persistent contexts the browser is accessed via context.browser
        browser = context.browser  # type: ignore[assignment]
        await _stealth.apply_stealth_async(
            context.pages[0] if context.pages else await context.new_page()
        )
        return browser, context  # type: ignore[return-value]

    browser = await playwright.chromium.launch(
        headless=headless,
        args=launch_args,
    )

    context = await browser.new_context(
        viewport={"width": viewport_width, "height": viewport_height},
        user_agent=selected_ua,
        locale=locale,
        timezone_id=timezone_id,
        proxy=proxy,
    )

    # Apply stealth to a new page (patches the context-level JS)
    page = await context.new_page()
    await _stealth.apply_stealth_async(page)

    return browser, context
