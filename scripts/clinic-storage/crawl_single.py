#!/usr/bin/env python3
"""Standalone single-hospital crawler with its own isolated browser.

Each invocation launches a headless Chromium browser, performs the full crawl
workflow, saves results to SQLite, and exits. Safe for parallel execution.

Dependencies: playwright (pip install playwright && python -m playwright install chromium)

Usage:
    python3 crawl_single.py --no 123 --name "고은미인의원" --url "https://example.com"
    python3 crawl_single.py --no 123 --name "병원" --url "https://..." --db hospitals.db --timeout 60
"""

import argparse
import asyncio
import json
import sys
from pathlib import Path

# Add parent dir to path for storage_manager import
sys.path.insert(0, str(Path(__file__).parent))
from clinic_crawler.log import log
from clinic_crawler.steps import (
    CrawlContext,
    step_collect_candidates,
    step_determine_status,
    step_dismiss_popups,
    step_extract_doctors,
    step_extract_social,
    step_navigate,
    step_preflight,
    step_save_results,
    step_spa_wait,
)
from storage_manager import DB_DEFAULT, export_unified_csv

CSV_SOURCE = "data/clinic-results/skin_clinics.csv"
CSV_UNIFIED_OUTPUT = "data/clinic-results/exports/clinic_results.csv"

# ---------------------------------------------------------------------------
# Main crawl function
# ---------------------------------------------------------------------------


async def crawl_hospital(hospital_no: int, name: str, url: str, db_path: str,
                         timeout: int = 45, headless: bool = True) -> dict:
    """Crawl a single hospital website with an isolated browser instance."""
    from playwright.async_api import async_playwright

    result = {
        "hospital_no": hospital_no,
        "name": name,
        "url": url,
        "final_url": "",
        "status": "success",
        "cms_platform": "",
        "schema_version": "2.0.0",
        "social_channels": [],
        "doctors": [],
        "errors": [],
        "doctor_page_exists": None,
    }

    async with async_playwright() as pw:
        browser = await pw.chromium.launch(headless=headless)
        context = await browser.new_context(
            viewport={"width": 1280, "height": 800},
            locale="ko-KR",
            user_agent=(
                "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/120.0.0.0 Safari/537.36"
            ),
            ignore_https_errors=True,
        )
        page = await context.new_page()
        page.set_default_timeout(timeout * 1000)
        page.set_default_navigation_timeout(timeout * 1000)

        ctx = CrawlContext(
            hospital_no=hospital_no, name=name, url=url,
            base_url="", result=result, page=page,
            context=context, browser=browser, timeout=timeout,
        )

        try:
            if not await step_preflight(ctx):
                return result
            if not await step_navigate(ctx):
                return result
            await step_dismiss_popups(ctx)
            await step_spa_wait(ctx)
            await step_extract_social(ctx)
            candidates = await step_collect_candidates(ctx)
            await step_extract_doctors(ctx, candidates)
            step_determine_status(ctx)

        except Exception as e:
            result["status"] = "failed"
            result["errors"].append({  # type: ignore[union-attr]
                "type": "unexpected", "message": str(e)[:300],
                "step": "unknown", "retryable": True,
            })
            log(f"#{hospital_no} Unexpected error: {e}")

        finally:
            await browser.close()

    step_save_results(result, db_path)
    return result


# ---------------------------------------------------------------------------
# CLI entry point
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(description="Crawl a single hospital with isolated browser")
    parser.add_argument("--no", type=int, required=True, help="Hospital number")
    parser.add_argument("--name", required=True, help="Hospital name")
    parser.add_argument("--url", required=True, help="Hospital website URL")
    parser.add_argument("--db", default=DB_DEFAULT, help=f"SQLite DB path (default: {DB_DEFAULT})")
    parser.add_argument("--timeout", type=int, default=45, help="Page timeout in seconds (default: 45)")
    parser.add_argument("--headed", action="store_true", help="Run with visible browser (for debugging)")
    args = parser.parse_args()

    result = asyncio.run(
        crawl_hospital(
            hospital_no=args.no,
            name=args.name,
            url=args.url,
            db_path=args.db,
            timeout=args.timeout,
            headless=not args.headed,
        )
    )

    # Output JSON to stdout
    print(json.dumps(result, ensure_ascii=False, indent=2))

    # Auto-export unified CSV after crawl completion
    if result["status"] in ("success", "partial"):
        try:
            export_unified_csv(args.db, CSV_SOURCE, CSV_UNIFIED_OUTPUT)
        except Exception as e:
            print(f"[crawl] CSV export failed: {e}", file=sys.stderr, flush=True)

    sys.exit(0 if result["status"] in ("success", "partial") else 1)


if __name__ == "__main__":
    main()
