"""Playwright browser launch with stealth patches.

Wraps ``playwright-stealth`` to provide a pre-configured, persistent
browser context that resists basic bot-detection techniques.
"""

from __future__ import annotations

import json
import random
from pathlib import Path

from playwright.async_api import Browser, BrowserContext, Playwright, async_playwright
from playwright_stealth import stealth_async


_USER_AGENTS_PATH = (
    Path(__file__).resolve().parent.parent.parent / "data" / "user_agents.json"
)


def _load_user_agents(path: Path | None = None) -> list[str]:
    """Load the user-agent pool from the JSON data file."""
    ua_path = path or _USER_AGENTS_PATH
    if not ua_path.exists():
        return [
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/131.0.0.0 Safari/537.36"
        ]
    with open(ua_path, encoding="utf-8") as f:
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
            locale="ja-JP",
            timezone_id="Asia/Tokyo",
        )
        # For persistent contexts the browser is accessed via context.browser
        browser = context.browser  # type: ignore[assignment]
        await stealth_async(context.pages[0] if context.pages else await context.new_page())
        return browser, context  # type: ignore[return-value]

    browser = await playwright.chromium.launch(
        headless=headless,
        args=launch_args,
    )

    context = await browser.new_context(
        viewport={"width": viewport_width, "height": viewport_height},
        user_agent=selected_ua,
        locale="ja-JP",
        timezone_id="Asia/Tokyo",
    )

    # Apply stealth to a new page (patches the context-level JS)
    page = await context.new_page()
    await stealth_async(page)

    return browser, context
