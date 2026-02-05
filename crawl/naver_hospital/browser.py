"""
Playwright browser controller with anti-detection and session persistence.
"""

from __future__ import annotations

import json
import logging
import random
import tempfile
from pathlib import Path
from typing import Optional

from playwright.async_api import Browser, BrowserContext, Page, async_playwright

from crawl.config import CrawlerConfig
from crawl.naver_hospital.stealth import get_combined_stealth_script

logger = logging.getLogger(__name__)


class BrowserController:
    """Manages headed Playwright browser with anti-detection."""

    def __init__(self, config: CrawlerConfig) -> None:
        self._config = config
        self._browser_config = config.browser
        self._playwright = None
        self._browser: Optional[Browser] = None
        self._context: Optional[BrowserContext] = None
        self._stealth_script = get_combined_stealth_script()

    async def __aenter__(self) -> BrowserController:
        await self.launch()
        return self

    async def __aexit__(self, *exc) -> None:
        await self.close()

    async def launch(self) -> None:
        """Launch browser with anti-detection settings."""
        if self._browser is not None:
            raise RuntimeError("Browser already launched. Call close() first.")

        self._playwright = await async_playwright().start()

        try:
            self._browser = await self._playwright.chromium.launch(
                headless=self._browser_config.headless,
                channel=self._browser_config.channel,
                args=[
                    "--disable-blink-features=AutomationControlled",
                    "--disable-dev-shm-usage",
                    "--no-first-run",
                    "--no-default-browser-check",
                ],
            )
        except Exception:
            await self._playwright.stop()
            self._playwright = None
            raise

        # Randomize viewport within configured range
        viewport_width = random.randint(
            self._browser_config.viewport_width_min,
            self._browser_config.viewport_width_max,
        )
        viewport_height = random.randint(
            self._browser_config.viewport_height_min,
            self._browser_config.viewport_height_max,
        )

        try:
            self._context = await self._browser.new_context(
                viewport={"width": viewport_width, "height": viewport_height},
                user_agent=self._browser_config.user_agent,
                locale="ko-KR",
                timezone_id="Asia/Seoul",
                is_mobile=True,
                has_touch=True,
                java_script_enabled=True,
            )

            # Apply stealth scripts to every new page
            await self._context.add_init_script(self._stealth_script)

            # Restore session cookies if available
            await self._restore_session()
        except Exception:
            await self._browser.close()
            self._browser = None
            raise

        logger.info(
            "Browser launched: headless=%s, viewport=%dx%d",
            self._browser_config.headless,
            viewport_width,
            viewport_height,
        )

    async def new_page(self) -> Page:
        """Create a new page with stealth settings applied."""
        if not self._context:
            raise RuntimeError("Browser not launched. Call launch() first.")

        page = await self._context.new_page()
        page.set_default_timeout(self._browser_config.timeout_ms)
        return page

    async def save_session(self) -> None:
        """Persist cookies to disk for session reuse (atomic write)."""
        if not self._context:
            return

        session_dir = self._browser_config.session_dir
        session_dir.mkdir(parents=True, exist_ok=True)

        cookies = await self._context.cookies()
        cookies_path = session_dir / "cookies.json"

        # Atomic write: write to temp then rename
        fd, tmp_path = tempfile.mkstemp(dir=session_dir, suffix=".tmp")
        try:
            with open(fd, "w", encoding="utf-8") as f:
                json.dump(cookies, f, ensure_ascii=False, indent=2)
            Path(tmp_path).replace(cookies_path)
            logger.debug("Session saved: %d cookies", len(cookies))
        except Exception:
            Path(tmp_path).unlink(missing_ok=True)
            raise

    async def _restore_session(self) -> None:
        """Restore cookies from disk if available."""
        if not self._context:
            return

        cookies_path = self._browser_config.session_dir / "cookies.json"
        if not cookies_path.exists():
            return

        try:
            cookies = json.loads(cookies_path.read_text())
            if cookies:
                await self._context.add_cookies(cookies)
                logger.debug("Session restored: %d cookies", len(cookies))
        except (json.JSONDecodeError, ValueError) as exc:
            logger.warning("Failed to restore session cookies: %s", exc)

    async def get_cookies_for_httpx(self) -> dict[str, str]:
        """Export cookies as a simple dict for httpx client."""
        if not self._context:
            return {}

        cookies = await self._context.cookies()
        return {c["name"]: c["value"] for c in cookies}

    async def close(self) -> None:
        """Save session and close browser with independent cleanup."""
        try:
            await self.save_session()
        except Exception:
            logger.exception("Failed to save session during close")

        if self._context:
            try:
                await self._context.close()
            except Exception:
                logger.exception("Failed to close browser context")
            finally:
                self._context = None

        if self._browser:
            try:
                await self._browser.close()
            except Exception:
                logger.exception("Failed to close browser")
            finally:
                self._browser = None

        if self._playwright:
            try:
                await self._playwright.stop()
            except Exception:
                logger.exception("Failed to stop playwright")
            finally:
                self._playwright = None

        logger.info("Browser closed")

    async def take_screenshot(self, page: Page, name: str) -> Path:
        """Take debug screenshot and return path."""
        screenshot_dir = self._config.storage.screenshot_dir
        screenshot_dir.mkdir(parents=True, exist_ok=True)
        path = screenshot_dir / f"{name}.png"
        await page.screenshot(path=str(path), full_page=True)
        return path
