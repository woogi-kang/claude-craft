"""Session management for X (Twitter) browser automation.

Manages persistent browser sessions with cookie storage, health checks,
and automatic re-login when sessions expire.
"""

from __future__ import annotations

from pathlib import Path

from outreach_shared.browser.human_sim import human_type, random_pause
from outreach_shared.browser.stealth import create_stealth_browser
from outreach_shared.utils.logger import get_logger
from playwright.async_api import BrowserContext, Page, Playwright

logger = get_logger("session")

# Default session storage root
_SESSIONS_DIR = Path(__file__).resolve().parent.parent.parent / "data" / "sessions"


class SessionManager:
    """Manage named browser sessions with persistent storage.

    Each session is stored in its own sub-directory under the sessions
    root so cookies and local storage survive across runs.
    """

    def __init__(
        self,
        playwright: Playwright,
        *,
        sessions_dir: str | Path | None = None,
        headless: bool = True,
        viewport_width: int = 1280,
        viewport_height: int = 720,
    ) -> None:
        self._playwright = playwright
        self._sessions_dir = Path(sessions_dir) if sessions_dir else _SESSIONS_DIR
        self._headless = headless
        self._viewport_width = viewport_width
        self._viewport_height = viewport_height
        self._contexts: dict[str, BrowserContext] = {}

    async def get_session(self, account_name: str) -> BrowserContext:
        """Return a browser context for *account_name*.

        If no context is currently open, a new one is created with
        persistent storage.  The caller must still check session health
        and call :meth:`login` if the session has expired.
        """
        if account_name in self._contexts:
            return self._contexts[account_name]

        user_data_dir = self._sessions_dir / account_name
        _, context = await create_stealth_browser(
            self._playwright,
            headless=self._headless,
            user_data_dir=user_data_dir,
            viewport_width=self._viewport_width,
            viewport_height=self._viewport_height,
        )
        self._contexts[account_name] = context
        logger.info("session_created", account=account_name)
        return context

    async def check_session_health(self, context: BrowserContext) -> bool:
        """Verify that the session is still authenticated on X.

        Navigates to the X home page and checks for indicators of a
        logged-in state.  Returns ``True`` when healthy.
        """
        page = context.pages[0] if context.pages else await context.new_page()
        try:
            await page.goto("https://x.com/home", wait_until="domcontentloaded", timeout=30_000)
            await random_pause(1.0, 2.0)

            # Look for the compose-tweet button which is only visible when logged in
            compose_btn = await page.query_selector('[data-testid="SideNav_NewTweet_Button"]')
            if compose_btn:
                logger.info("session_healthy")
                return True

            # Alternative check: look for the user avatar in the sidebar
            avatar = await page.query_selector('[data-testid="AppTabBar_Profile_Link"]')
            if avatar:
                logger.info("session_healthy")
                return True

            logger.warning("session_expired")
            return False
        except Exception as exc:
            logger.error("session_health_check_failed", error=str(exc))
            return False

    async def login(
        self,
        context: BrowserContext,
        username: str,
        password: str,
    ) -> bool:
        """Perform X login using the given credentials.

        Returns ``True`` on successful login.
        """
        page = context.pages[0] if context.pages else await context.new_page()
        try:
            login_url = "https://x.com/i/flow/login"
            await page.goto(login_url, wait_until="domcontentloaded", timeout=30_000)
            await random_pause(2.0, 4.0)

            # Enter username
            username_input = await page.wait_for_selector(
                'input[autocomplete="username"]', timeout=15_000
            )
            if username_input:
                await human_type(page, 'input[autocomplete="username"]', username)
                await random_pause(0.5, 1.0)

            # Click Next
            next_btn = await page.query_selector('text="Next"')
            if next_btn is None:
                next_btn = await page.query_selector('text="次へ"')
            if next_btn:
                await next_btn.click()
                await random_pause(1.5, 3.0)

            # Enter password
            password_input = await page.wait_for_selector('input[type="password"]', timeout=15_000)
            if password_input:
                await human_type(page, 'input[type="password"]', password)
                await random_pause(0.5, 1.0)

            # Click Log In
            login_btn = await page.query_selector('[data-testid="LoginForm_Login_Button"]')
            if login_btn:
                await login_btn.click()
                await random_pause(3.0, 5.0)

            # Verify login succeeded
            is_healthy = await self.check_session_health(context)
            if is_healthy:
                logger.info("login_success", username=username)
            else:
                logger.warning("login_failed", username=username)
            return is_healthy

        except Exception as exc:
            logger.error("login_error", username=username, error=str(exc))
            return False

    async def close_all(self) -> None:
        """Close all open browser contexts."""
        for name, ctx in self._contexts.items():
            try:
                await ctx.close()
                logger.info("session_closed", account=name)
            except Exception:
                pass
        self._contexts.clear()

    async def _ensure_page(self, context: BrowserContext) -> Page:
        """Return the first page or create a new one."""
        if context.pages:
            return context.pages[0]
        return await context.new_page()
