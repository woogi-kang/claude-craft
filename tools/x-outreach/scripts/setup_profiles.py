"""Setup persona profiles: inject Chrome cookies into Playwright and post.

Workflow:
    1. Log into each X account in real Chrome
    2. Export cookies via EditThisCookie extension (JSON) or DevTools
    3. Save as data/cookies/<account_id>.json
    4. Run this script to post pinned tweets

Usage:
    cd tools/x-outreach

    # Export cookies (see --help-export for instructions)
    .venv/bin/python scripts/setup_profiles.py --help-export

    # Post using saved cookies
    .venv/bin/python scripts/setup_profiles.py --account master_a
    .venv/bin/python scripts/setup_profiles.py              # all accounts

Flags:
    --account ID      Only process a single account (e.g. master_a)
    --dry-run         Show posts but do not open browser
    --help-export     Show cookie export instructions
"""

from __future__ import annotations

import argparse
import asyncio
import json
import random
import sys
from pathlib import Path

# Ensure project root is on sys.path
_PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(_PROJECT_ROOT))

from outreach_shared.browser.human_sim import random_pause  # noqa: E402
from playwright.async_api import BrowserContext, async_playwright  # noqa: E402

from src.platform.selectors import (  # noqa: E402
    COMPOSE_TEXT_INPUT,
)

COOKIES_DIR = _PROJECT_ROOT / "data" / "cookies"

# ---------------------------------------------------------------------------
# Persona pinned posts (self-introduction tweets in Japanese)
# ---------------------------------------------------------------------------

PINNED_POSTS: dict[str, str] = {
    "master_a": (
        "韓国美容の価格、メモし続けてる人です。\n"
        "\n"
        "同じ施術名でも\n"
        "薬剤・ショット数・立地で\n"
        "2〜3倍の差が出ることが多い。\n"
        "\n"
        "数字ベースで比較したい人向けに\n"
        "気づいたことを整理してる。\n"
        "\n"
        "どの価格帯を想定してる？\n"
        "\n"
        "#渡韓美容 #韓国クリニック"
    ),
    "master_b": (
        "初めての韓国美容、どこから始めるかわからなくて当然だよ。\n"
        "\n"
        "予約・通訳・術後ケアまで\n"
        "一通りの流れを整理してる。\n"
        "\n"
        "失敗しにくい順番があるから\n"
        "最初の1歩を一緒に確認しよ。\n"
        "\n"
        "初めてなら、何が一番不安？\n"
        "\n"
        "#渡韓美容 #韓国皮膚科"
    ),
    "master_c": (
        "韓国美容、施術の選び方を整理してる人です。\n"
        "\n"
        "同じ悩みでも\n"
        "目的・ダウンタイム・効果の持続で\n"
        "向く施術が変わる傾向がある。\n"
        "\n"
        "比較の軸を作っておくと\n"
        "選びやすくなると考えるとわかりやすい。\n"
        "\n"
        "気になるのは効果速度？ダウンタイム？\n"
        "\n"
        "#渡韓美容 #韓国肌管理"
    ),
    "master_d": (
        "施術後に不安になったとき、一人で抱えなくていいよ。\n"
        "\n"
        "副作用・対応・術後ケアについて\n"
        "実際に調べたことを記録してる。\n"
        "\n"
        "困ったことの整理や\n"
        "確認しておくべき点を一緒に見ていく。\n"
        "\n"
        "今いちばん困ってるのは痛み？対応？\n"
        "\n"
        "#渡韓美容 #韓国皮膚科"
    ),
    "master_e": (
        "ソウルに住んでて、ときどき皮膚科に行く人です。\n"
        "\n"
        "美容情報より先に\n"
        "日常の話が多めかも。\n"
        "\n"
        "でも同じ悩みがあるなら\n"
        "体感ベースで正直に話せると思う、って感じ。\n"
        "\n"
        "気になることあればいつでも聞いて。\n"
        "\n"
        "#韓国美容 #渡韓美容"
    ),
}

ACCOUNTS = ["master_a", "master_b", "master_c", "master_d", "master_e"]

DISPLAY_NAMES = {
    "master_a": "みく｜韓国美容の値段メモ",
    "master_b": "あや｜初めての韓国美容ナビ",
    "master_c": "りこ｜施術の違いを整理する人",
    "master_d": "なつみ｜施術後ケアの記録",
    "master_e": "ゆい｜ソウルときどき美容",
}


def weighted_char_count(text: str) -> int:
    """Count weighted characters as X does (CJK=2, ASCII=1)."""
    count = 0
    for ch in text:
        cp = ord(ch)
        if (
            0x3000 <= cp <= 0x9FFF
            or 0xF900 <= cp <= 0xFAFF
            or 0xFF00 <= cp <= 0xFFEF
            or 0x20000 <= cp <= 0x2FA1F
        ):
            count += 2
        else:
            count += 1
    return count


def load_cookies(account_id: str) -> list[dict] | None:
    """Load cookies from JSON file.

    Supports two formats:
    - EditThisCookie format (array of {name, value, domain, path, ...})
    - DevTools format (same structure)
    """
    cookie_file = COOKIES_DIR / f"{account_id}.json"
    if not cookie_file.exists():
        return None

    with open(cookie_file, encoding="utf-8") as f:
        raw = json.load(f)

    # Normalize to Playwright cookie format
    cookies = []
    for c in raw:
        cookie: dict = {
            "name": c["name"],
            "value": c["value"],
            "domain": c.get("domain", ".x.com"),
            "path": c.get("path", "/"),
        }
        # EditThisCookie uses 'secure', 'httpOnly' as booleans
        if "secure" in c:
            cookie["secure"] = bool(c["secure"])
        if "httpOnly" in c:
            cookie["httpOnly"] = bool(c["httpOnly"])
        if "sameSite" in c:
            ss = str(c["sameSite"]).capitalize()
            if ss in ("Strict", "Lax", "None"):
                cookie["sameSite"] = ss
        # Skip expired cookies
        if c.get("expirationDate"):
            cookie["expires"] = float(c["expirationDate"])

        cookies.append(cookie)

    return cookies


async def inject_cookies_and_verify(context: BrowserContext, cookies: list[dict]) -> bool:
    """Inject cookies and verify the session is authenticated."""
    await context.add_cookies(cookies)

    page = context.pages[0] if context.pages else await context.new_page()
    await page.goto("https://x.com/home", wait_until="domcontentloaded", timeout=30_000)
    await asyncio.sleep(4.0)

    compose_btn = await page.query_selector('[data-testid="SideNav_NewTweet_Button"]')
    profile_link = await page.query_selector('[data-testid="AppTabBar_Profile_Link"]')
    return bool(compose_btn or profile_link)


async def post_tweet(context: BrowserContext, tweet_text: str) -> bool:
    """Compose and publish a tweet via Playwright."""
    page = context.pages[0] if context.pages else await context.new_page()

    try:
        # Navigate to home
        if "/home" not in page.url:
            await page.goto(
                "https://x.com/home",
                wait_until="domcontentloaded",
                timeout=30_000,
            )
            await random_pause(3.0, 5.0)

        # Dismiss common X popups (notifications, premium, onboarding)
        print("    [INFO] Dismissing popups...")
        for _ in range(3):
            await page.keyboard.press("Escape")
            await asyncio.sleep(0.8)

        # Try clicking common dismiss buttons
        for dismiss_sel in [
            'button[aria-label="Close"]',
            '[data-testid="app-bar-close"]',
            'text="Not now"',
            'text="今はしない"',
            'text="Skip for now"',
            'text="後で"',
        ]:
            btn = await page.query_selector(dismiss_sel)
            if btn:
                print(f"    [INFO] Dismissing popup: {dismiss_sel}")
                await btn.click(force=True)
                await asyncio.sleep(1.0)

        await random_pause(1.0, 2.0)

        # Open compose via JS click (bypasses overlay pointer interception)
        print("    [INFO] Opening compose dialog via JS...")
        await page.evaluate("""
            const btn = document.querySelector('[data-testid="SideNav_NewTweet_Button"]');
            if (btn) btn.click();
        """)
        await random_pause(2.0, 4.0)

        text_input = await page.wait_for_selector(COMPOSE_TEXT_INPUT, timeout=15_000)
        if text_input is None:
            print("    [ERROR] Text input not found")
            return False

        # Focus the text area via JS (more reliable than force click)
        await page.evaluate("""
            const el = document.querySelector('[data-testid="tweetTextarea_0"]');
            if (el) { el.focus(); el.click(); }
        """)
        await random_pause(0.5, 1.0)

        # Clear any existing content
        await page.keyboard.press("Meta+a")
        await asyncio.sleep(0.3)
        await page.keyboard.press("Backspace")
        await asyncio.sleep(0.5)

        # Insert text line by line (Draft.js needs Enter key for newlines)
        lines = tweet_text.split("\n")
        for i, line in enumerate(lines):
            if line:
                await page.evaluate(
                    "(text) => document.execCommand('insertText', false, text)",
                    line,
                )
            if i < len(lines) - 1:
                await page.keyboard.press("Enter")
                await asyncio.sleep(0.1)
        await random_pause(2.0, 3.0)

        # Debug: screenshot to verify text was entered
        ss_dir = _PROJECT_ROOT / "data" / "debug"
        ss_dir.mkdir(parents=True, exist_ok=True)
        await page.screenshot(path=str(ss_dir / "compose_before_submit.png"))

        # Submit via JS click (bypasses overlay)
        print("    [INFO] Submitting post via JS...")
        submitted = await page.evaluate("""(() => {
            const btn = document.querySelector('[data-testid="tweetButton"]');
            if (btn && !btn.disabled) { btn.click(); return true; }
            return false;
        })()""")
        if not submitted:
            print("    [ERROR] Submit button not found or disabled")
            return False

        await random_pause(4.0, 7.0)
        return True

    except Exception as exc:
        print(f"    [ERROR] Posting failed: {exc}")
        try:
            ss_dir = _PROJECT_ROOT / "data" / "debug"
            ss_dir.mkdir(parents=True, exist_ok=True)
            await page.screenshot(path=str(ss_dir / "post_error.png"), full_page=True)
        except Exception:
            pass
        return False


async def process_account(
    playwright,
    account_id: str,
) -> dict[str, str | bool]:
    """Inject cookies and post pinned tweet for one account."""
    display = DISPLAY_NAMES.get(account_id, account_id)
    tweet = PINNED_POSTS.get(account_id, "")

    result: dict[str, str | bool] = {
        "account_id": account_id,
        "display_name": display,
        "session_ok": False,
        "post_ok": False,
        "error": "",
    }

    wc = weighted_char_count(tweet)
    print(f"\n{'=' * 60}")
    print(f"  Account: {account_id} ({display})")
    print(f"  Tweet ({wc} weighted chars):")
    print(f"    {tweet}")
    print(f"{'=' * 60}")

    # Load cookies
    cookies = load_cookies(account_id)
    if cookies is None:
        result["error"] = f"No cookie file: data/cookies/{account_id}.json"
        print(f"  [SKIP] {result['error']}")
        return result

    print(f"  Loaded {len(cookies)} cookies")

    # Create a non-persistent browser context
    browser = await playwright.chromium.launch(
        headless=False,
        args=[
            "--disable-blink-features=AutomationControlled",
            "--disable-dev-shm-usage",
        ],
    )
    context = await browser.new_context(
        viewport={"width": 1280, "height": 720},
        locale="ja-JP",
        timezone_id="Asia/Tokyo",
    )

    try:
        # Inject cookies and verify
        print("  [1/2] Injecting cookies and verifying session...")
        session_ok = await inject_cookies_and_verify(context, cookies)
        result["session_ok"] = session_ok

        if not session_ok:
            result["error"] = "Session invalid (cookies expired?)"
            print("  [FAIL] Session verification failed")
            page = context.pages[0] if context.pages else await context.new_page()
            ss_dir = _PROJECT_ROOT / "data" / "debug"
            ss_dir.mkdir(parents=True, exist_ok=True)
            await page.screenshot(
                path=str(ss_dir / f"session_fail_{account_id}.png"), full_page=True
            )
            return result

        print("  [OK] Session is valid")
        await random_pause(1.0, 2.0)

        # Post tweet
        print("  [2/2] Posting pinned tweet...")
        post_ok = await post_tweet(context, tweet)
        result["post_ok"] = post_ok

        if post_ok:
            print("  [OK] Tweet posted!")
        else:
            result["error"] = "Post failed"
            print("  [FAIL] Tweet posting failed")

    finally:
        await context.close()
        await browser.close()

    return result


EXPORT_HELP = """
==============================================================
  Cookie Export Instructions
==============================================================

Method 1: EditThisCookie Chrome Extension (Recommended)
---------------------------------------------------------
1. Install "EditThisCookie" from Chrome Web Store
   https://chromewebstore.google.com/detail/editthiscookie/fngmhnnpilhplaeedifhccceomclgfbg

2. Log into X (x.com) with the target account in Chrome

3. Click the EditThisCookie icon -> Export (copy icon)
   This copies all x.com cookies as JSON to clipboard

4. Save to file:
   pbpaste > data/cookies/master_a.json

5. Repeat for each account (master_b, master_c, master_d, master_e)


Method 2: Chrome DevTools Console
---------------------------------------------------------
1. Log into X in Chrome
2. Open DevTools (Cmd+Option+I) -> Console
3. Run:
   copy(document.cookie.split(';').map(c => {
     const [name, ...v] = c.trim().split('=');
     return {name, value: v.join('='), domain: '.x.com', path: '/'};
   }))
4. Paste into data/cookies/master_a.json

Note: Method 2 only captures non-httpOnly cookies.
      Method 1 (EditThisCookie) captures ALL cookies including
      auth_token and ct0 which are httpOnly.


Key cookies needed:
  - auth_token  (main session token)
  - ct0         (CSRF token)
  - twid        (user ID)

File structure:
  data/cookies/
    master_a.json
    master_b.json
    master_c.json
    master_d.json
    master_e.json
==============================================================
"""


async def main() -> None:
    parser = argparse.ArgumentParser(description="Setup persona profiles on X (cookie injection)")
    parser.add_argument("--account", type=str, help="Only process a single account (e.g. master_a)")
    parser.add_argument("--dry-run", action="store_true", help="Show posts but do not open browser")
    parser.add_argument(
        "--help-export",
        action="store_true",
        help="Show cookie export instructions",
    )
    args = parser.parse_args()

    if args.help_export:
        print(EXPORT_HELP)
        return

    accounts_to_process = ACCOUNTS
    if args.account:
        if args.account not in ACCOUNTS:
            print(f"Unknown account: {args.account}")
            print(f"Available: {', '.join(ACCOUNTS)}")
            sys.exit(1)
        accounts_to_process = [args.account]

    print("\n" + "=" * 60)
    print("  X Persona Profile Setup (Cookie Injection)")
    print(f"  Accounts: {len(accounts_to_process)}")
    print(f"  Mode: {'DRY RUN' if args.dry_run else 'LIVE'}")
    print("=" * 60)

    if args.dry_run:
        for account_id in accounts_to_process:
            display = DISPLAY_NAMES.get(account_id, account_id)
            tweet = PINNED_POSTS.get(account_id, "")
            wc = weighted_char_count(tweet)
            cookie_exists = (COOKIES_DIR / f"{account_id}.json").exists()
            cookie_s = "found" if cookie_exists else "MISSING"
            print(f"\n  {account_id} ({display}) [cookies: {cookie_s}]")
            print(f"    [{wc} chars] {tweet}")
        print("\n  [DRY-RUN] No browser opened.")
        return

    # Ensure cookies dir exists
    COOKIES_DIR.mkdir(parents=True, exist_ok=True)

    results = []
    async with async_playwright() as pw:
        for account_id in accounts_to_process:
            result = await process_account(pw, account_id)
            results.append(result)

            # Pause between accounts
            if account_id != accounts_to_process[-1]:
                wait = random.uniform(5.0, 10.0)
                print(f"\n  Waiting {wait:.0f}s before next account...")
                await asyncio.sleep(wait)

    print("\n" + "=" * 60)
    print("  RESULTS SUMMARY")
    print("=" * 60)
    for r in results:
        session_s = "OK" if r["session_ok"] else "FAIL"
        post_s = "OK" if r["post_ok"] else "FAIL"
        error = f" ({r['error']})" if r["error"] else ""
        print(f"  {r['account_id']:12s} | Session: {session_s:4s} | Post: {post_s:4s}{error}")
    print("=" * 60)

    if any(not r["session_ok"] or not r["post_ok"] for r in results):
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())
