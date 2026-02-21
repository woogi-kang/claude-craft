"""Non-interactive full cycle runner.

Uses saved session from login_helper.py.
Mode 3: Smart Search -> Reply -> DM (auto-accept all).
"""

from __future__ import annotations

import asyncio
import random
import sys
from pathlib import Path

from dotenv import load_dotenv
from playwright.async_api import async_playwright

import verify  # noqa: E402
from verify import (  # noqa: E402
    browse_timeline,
    compose_dm,
    compose_reply,
    create_browser,
    human_wait,
    idle_behavior,
    smart_search,
    step_dm,
    step_reply,
)

load_dotenv(Path(__file__).parent / ".env")

# Monkey-patch ask() to auto-accept (no interactive stdin)
verify.ask = lambda prompt: True

SESSION_DIR = Path(__file__).parent / "data" / "sessions" / "nandemo"


async def main() -> None:
    print("=" * 60)
    print("  X Outreach - Full Cycle (Auto Mode)")
    print("  Mode 3: Search -> Reply -> DM")
    print("  Session: nandemo (saved)")
    print("=" * 60)

    import shutil

    if not shutil.which("codex"):
        print("\n  ERROR: codex CLI not found.")
        sys.exit(1)

    target_count = 3

    async with async_playwright() as pw:
        # Reuse saved session
        print("\n[1/5] Opening saved session...")
        ctx = await create_browser(pw, "nandemo")
        page = ctx.pages[0]

        # Verify session is alive
        await page.goto("https://x.com/home", wait_until="domcontentloaded", timeout=30_000)
        await asyncio.sleep(random.uniform(3, 6))

        compose_btn = await page.query_selector('[data-testid="SideNav_NewTweet_Button"]')
        profile_link = await page.query_selector('[data-testid="AppTabBar_Profile_Link"]')

        if compose_btn or profile_link:
            print("  Session alive - logged in!")
        else:
            print("  ERROR: Session expired. Run login_helper.py first.")
            await ctx.close()
            sys.exit(1)

        # Casual browse before starting
        await browse_timeline(page)

        # ── Smart Search ──
        print(f"\n[2/5] Smart Search (target: {target_count} tweets)...")
        qualified = await smart_search(ctx, target_count)

        if not qualified:
            print("\n  No qualified tweets found. Exiting.")
            await ctx.close()
            return

        print(f"\n{'=' * 60}")
        print(f"  RESULTS: {len(qualified)} qualified tweets")
        print(f"{'=' * 60}")
        for i, t in enumerate(qualified, 1):
            cls = t.get("classification", "?")
            conf = t.get("confidence", 0)
            print(f"\n  [{i}] @{t.get('username', '?')} ({cls}, {conf:.0%})")
            print(f"      {t.get('content', '')[:100]}")
            if t.get("url"):
                print(f"      {t['url']}")

        # Pick first qualified tweet for reply + DM
        target = qualified[0]
        print(f"\n  Selected: @{target.get('username', '?')}")

        # ── Reply ──
        print(f"\n[3/5] Composing reply to @{target.get('username', '?')}...")
        reply_text = compose_reply(target)

        if reply_text:
            print(f"\n  Draft reply: {reply_text}")
            print("  Auto-sending reply...")
            success = await step_reply(ctx, target, reply_text)
            if success:
                print("  Reply sent successfully!")
            else:
                print("  Reply failed.")
        else:
            print("  LLM failed to compose reply. Skipping.")

        # ── Wait between reply and DM ──
        print("\n[4/5] Waiting before DM...")
        await human_wait("cooling down between reply and DM", 60, 180)

        # Some idle behavior
        await idle_behavior(page)

        # ── DM ──
        dm_user = target.get("username", "")
        if dm_user:
            print(f"\n[5/5] Composing DM to @{dm_user}...")
            dm_text = compose_dm(target)

            if dm_text:
                print(f"\n  Draft DM: {dm_text}")
                print("  Auto-sending DM...")
                success = await step_dm(ctx, dm_user, dm_text)
                if success:
                    print("  DM sent successfully!")
                else:
                    print("  DM failed.")
            else:
                print("  LLM failed to compose DM. Skipping.")
        else:
            print("  No username for DM. Skipping.")

        # Keep browser open briefly for verification
        print("\n  Browser stays open 30s for verification...")
        await asyncio.sleep(30)
        await ctx.close()

    print("\n" + "=" * 60)
    print("  Full cycle complete!")
    print("=" * 60)


if __name__ == "__main__":
    asyncio.run(main())
