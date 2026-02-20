"""X login automation extracted from session management.

Handles the multi-step X login flow using Playwright with human-like
typing and delays.
"""

from __future__ import annotations

from outreach_shared.browser.human_sim import human_type, random_pause
from outreach_shared.utils.logger import get_logger
from playwright.async_api import BrowserContext

from src.platform.selectors import (
    COMPOSE_TWEET_BUTTON,
    HOME_URL,
    LOGIN_BUTTON,
    LOGIN_URL,
    NEXT_BUTTON_EN,
    NEXT_BUTTON_JA,
    PASSWORD_INPUT,
    PROFILE_LINK,
    USERNAME_INPUT,
    VERIFY_INPUT,
)

logger = get_logger("login")


async def check_session_health(context: BrowserContext) -> bool:
    """Verify that the session is still authenticated on X.

    Navigates to the X home page and checks for indicators of a
    logged-in state.

    Parameters
    ----------
    context:
        Playwright browser context to check.

    Returns
    -------
    bool
        ``True`` if the session is authenticated.
    """
    page = context.pages[0] if context.pages else await context.new_page()
    try:
        await page.goto(HOME_URL, wait_until="domcontentloaded", timeout=30_000)
        await random_pause(1.0, 2.0)

        compose_btn = await page.query_selector(COMPOSE_TWEET_BUTTON)
        if compose_btn:
            return True

        avatar = await page.query_selector(PROFILE_LINK)
        if avatar:
            return True

        logger.warning("session_expired")
        return False
    except Exception as exc:
        logger.error("session_health_check_failed", error=str(exc))
        return False


async def _click_next(page: object) -> None:
    """Click the Next button (English or Japanese)."""
    next_btn = await page.query_selector(NEXT_BUTTON_EN)
    if next_btn is None:
        next_btn = await page.query_selector(NEXT_BUTTON_JA)
    if next_btn:
        await next_btn.click()
        await random_pause(1.5, 3.0)


async def login(
    context: BrowserContext,
    username: str,
    password: str,
) -> bool:
    """Perform X login using the given credentials.

    Handles the multi-step flow including the optional verification
    step where X asks for phone/email confirmation.

    Parameters
    ----------
    context:
        Playwright browser context.
    username:
        X account username (email or handle).
    password:
        X account password.

    Returns
    -------
    bool
        ``True`` on successful login.
    """
    page = context.pages[0] if context.pages else await context.new_page()
    try:
        await page.goto(LOGIN_URL, wait_until="domcontentloaded", timeout=30_000)
        await random_pause(2.0, 4.0)

        # Step 1: Enter username
        username_input = await page.wait_for_selector(USERNAME_INPUT, timeout=15_000)
        if username_input:
            await human_type(page, USERNAME_INPUT, username)
            await random_pause(0.5, 1.0)

        # Click Next
        await _click_next(page)

        # Step 2: Check for verification or password
        # X sometimes asks "Enter your phone number or email" before password
        password_el = await page.query_selector(PASSWORD_INPUT)
        verify_el = await page.query_selector(VERIFY_INPUT)

        if verify_el and not password_el:
            # Verification step: re-enter the username/email
            logger.info("verification_step_detected")
            await human_type(page, VERIFY_INPUT, username)
            await random_pause(0.5, 1.0)
            await _click_next(page)
            await random_pause(1.0, 2.0)

        # Step 3: Enter password
        password_input = await page.wait_for_selector(PASSWORD_INPUT, timeout=20_000)
        if password_input:
            await human_type(page, PASSWORD_INPUT, password)
            await random_pause(0.5, 1.0)

        # Click Log In
        login_btn = await page.query_selector(LOGIN_BUTTON)
        if login_btn:
            await login_btn.click()
            await random_pause(3.0, 5.0)

        # Verify login succeeded
        is_healthy = await check_session_health(context)
        if is_healthy:
            logger.info("login_success", username=username)
        else:
            logger.warning("login_failed", username=username)
        return is_healthy

    except Exception as exc:
        # Capture screenshot for debugging
        try:
            from pathlib import Path

            ss_path = Path("data/login_debug.png")
            ss_path.parent.mkdir(parents=True, exist_ok=True)
            await page.screenshot(path=str(ss_path), full_page=True)
            logger.info("debug_screenshot_saved", path=str(ss_path))
        except Exception:
            pass
        logger.error("login_error", username=username, error=str(exc))
        return False
