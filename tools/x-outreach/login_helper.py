"""Open a headed browser for manual X login.

Session persists to data/sessions/nandemo/ automatically.
The browser stays open until a signal file is created or timeout.
"""

import asyncio
from pathlib import Path

from playwright.async_api import async_playwright
from playwright_stealth import Stealth

SIGNAL_FILE = Path(__file__).parent / "data" / ".login_done"
SESSION_DIR = Path(__file__).parent / "data" / "sessions" / "nandemo"


async def main() -> None:
    SESSION_DIR.mkdir(parents=True, exist_ok=True)
    SIGNAL_FILE.unlink(missing_ok=True)

    async with async_playwright() as pw:
        context = await pw.chromium.launch_persistent_context(
            user_data_dir=str(SESSION_DIR),
            headless=False,
            args=[
                "--disable-blink-features=AutomationControlled",
                "--no-sandbox",
            ],
            viewport={"width": 1280, "height": 800},
            user_agent=(
                "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/131.0.0.0 Safari/537.36"
            ),
            locale="ja-JP",
            timezone_id="Asia/Tokyo",
        )

        stealth = Stealth()
        page = context.pages[0] if context.pages else await context.new_page()
        await stealth.apply_stealth_async(page)

        # Navigate to X login
        print("BROWSER_OPEN", flush=True)
        await page.goto("https://x.com/i/flow/login", wait_until="domcontentloaded", timeout=30_000)
        print("LOGIN_PAGE_READY", flush=True)

        # Wait for signal file or timeout (10 min)
        for _ in range(600):
            await asyncio.sleep(1)
            if SIGNAL_FILE.exists():
                print("SIGNAL_RECEIVED", flush=True)
                break

        # Verify login
        await page.goto("https://x.com/home", wait_until="domcontentloaded", timeout=30_000)
        await asyncio.sleep(3)

        compose_btn = await page.query_selector('[data-testid="SideNav_NewTweet_Button"]')
        profile_link = await page.query_selector('[data-testid="AppTabBar_Profile_Link"]')

        if compose_btn or profile_link:
            print("LOGIN_SUCCESS", flush=True)
        else:
            print("LOGIN_NOT_VERIFIED", flush=True)

        await context.close()

    SIGNAL_FILE.unlink(missing_ok=True)
    print("DONE", flush=True)


if __name__ == "__main__":
    asyncio.run(main())
