#!/usr/bin/env python3
"""Parallel batch crawler with isolated browser per hospital.

Reads hospital list from CSV, filters by criteria, and runs multiple
crawl_single.py processes concurrently. Each process gets its own
headless Chromium browser - no shared state, no conflicts.

Dependencies: playwright (pip install playwright && python -m playwright install chromium)

Usage:
    # Crawl all Seoul clinics, 5 in parallel:
    python3 crawl_batch.py --csv skin_clinics.csv --filter-city 서울 --parallel 5

    # Crawl specific hospital numbers:
    python3 crawl_batch.py --csv skin_clinics.csv --numbers 123,456,789 --parallel 3

    # Crawl first 10, dry-run (show what would be crawled):
    python3 crawl_batch.py --csv skin_clinics.csv --limit 10 --dry-run

    # Random sample of 10 Seoul clinics:
    python3 crawl_batch.py --csv skin_clinics.csv --filter-city 서울 --sample 10 --parallel 5
"""

import argparse
import asyncio
import csv
import json
import random
import sys
import time
from datetime import datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
# Import the crawl function directly for in-process parallel execution
from crawl_single import crawl_hospital
from storage_manager import DB_DEFAULT, export_unified_csv, get_db

CSV_SOURCE = "data/clinic-results/skin_clinics.csv"
CSV_UNIFIED_OUTPUT = "data/clinic-results/exports/clinic_results.csv"


def load_csv(csv_path: str) -> list:
    """Load hospital list from CSV file."""
    hospitals = []
    with open(csv_path, encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        for row in reader:
            # Normalize column names (strip BOM, whitespace)
            clean = {k.strip(): v.strip() for k, v in row.items() if k}
            hospitals.append(clean)
    return hospitals


def filter_hospitals(hospitals: list, city: str = None, numbers: list = None,
                     skip_crawled: bool = True, db_path: str = DB_DEFAULT) -> list:
    """Filter hospital list by criteria."""
    result = hospitals

    # Filter by city (address contains city name)
    if city:
        result = [h for h in result if city in (
            h.get("소재지주소") or h.get("naver_address") or h.get("주소") or h.get("address") or ""
        )]

    # Filter by specific numbers
    if numbers:
        num_set = set(numbers)
        result = [h for h in result if int(h.get("NO", h.get("no", 0))) in num_set]

    # Skip already-crawled hospitals
    # success = both social+doctors → skip
    # robots_blocked = can't crawl → skip
    # partial/empty/failed = re-crawlable
    if skip_crawled:
        try:
            conn = get_db(db_path)
            crawled = set()
            rows = conn.execute(
                "SELECT hospital_no FROM hospitals WHERE status IN ('success', 'robots_blocked')"
            ).fetchall()
            for row in rows:
                crawled.add(row["hospital_no"])
            conn.close()
            before = len(result)
            result = [h for h in result if int(h.get("NO", h.get("no", 0))) not in crawled]
            skipped = before - len(result)
            if skipped:
                log(f"Skipped {skipped} already-crawled hospitals (success/robots_blocked)")
        except Exception:
            pass  # DB not available, don't skip

    return result


# Platform domains that often block robots.txt or aren't real hospital sites
_PLATFORM_DOMAINS = {
    "blog.naver.com", "cafe.naver.com", "post.naver.com",
    "facebook.com", "www.facebook.com", "m.facebook.com",
    "instagram.com", "www.instagram.com",
    "youtube.com", "www.youtube.com",
    "pf.kakao.com", "open.kakao.com",
    "twitter.com", "x.com",
}


def _pick_best_url(row: dict) -> str:
    """Pick the best crawlable URL: prefer custom domain over platform URLs."""
    naver = (row.get("naver_website") or "").strip()
    homepage = (row.get("홈페이지") or row.get("url") or row.get("website") or "").strip()

    # Check if naver_website is a platform URL
    naver_is_platform = False
    if naver:
        try:
            from urllib.parse import urlparse
            host = urlparse(naver).netloc.lower()
            naver_is_platform = any(host == d or host.endswith("." + d) for d in _PLATFORM_DOMAINS)
        except Exception:
            pass

    # Priority: custom domain first, then platform URL as fallback
    if homepage and not naver_is_platform:
        return naver or homepage  # naver custom domain > homepage
    if homepage:
        return homepage  # homepage > naver platform URL
    return naver  # fallback to naver even if platform


def parse_hospital(row: dict) -> dict:
    """Parse a CSV row into hospital parameters."""
    return {
        "hospital_no": int(row.get("NO", row.get("no", 0))),
        "name": row.get("병원/약국명") or row.get("naver_name") or row.get("이름") or row.get("name") or "",
        "url": _pick_best_url(row),
        "address": row.get("소재지주소") or row.get("naver_address") or row.get("주소") or row.get("address") or "",
        "phone": row.get("전화번호") or row.get("phone") or "",
        "category": row.get("naver_category") or row.get("분류") or row.get("category") or "",
    }


def log(msg: str) -> None:
    ts = datetime.now().strftime("%H:%M:%S")
    print(f"[{ts}] {msg}", file=sys.stderr, flush=True)


async def run_batch(hospitals: list, db_path: str, parallel: int,
                    timeout: int, headless: bool) -> dict:
    """Run crawl tasks with bounded parallelism using asyncio semaphore."""
    semaphore = asyncio.Semaphore(parallel)
    results = {"success": 0, "partial": 0, "failed": 0, "errors": 0, "total": len(hospitals)}
    start_time = time.time()

    async def crawl_with_semaphore(hosp: dict) -> dict:
        async with semaphore:
            info = parse_hospital(hosp)
            if not info["url"]:
                log(f"#{info['hospital_no']} Skipping - no URL")
                results["errors"] += 1
                return {"hospital_no": info["hospital_no"], "status": "failed", "reason": "no_url"}

            try:
                result = await crawl_hospital(
                    hospital_no=info["hospital_no"],
                    name=info["name"],
                    url=info["url"],
                    db_path=db_path,
                    timeout=timeout,
                    headless=headless,
                )
                status = result.get("status", "failed")
                results[status] = results.get(status, 0) + 1

                channels = len(result.get("social_channels", []))
                doctors = len(result.get("doctors", []))
                log(f"#{info['hospital_no']} Done: status={status} channels={channels} doctors={doctors}")
                return result

            except Exception as e:
                results["errors"] += 1
                log(f"#{info['hospital_no']} Error: {e}")
                return {"hospital_no": info["hospital_no"], "status": "failed", "error": str(e)}

    log(f"Starting batch: {len(hospitals)} hospitals, {parallel} parallel workers")
    log(f"Database: {db_path}")

    tasks = [crawl_with_semaphore(h) for h in hospitals]
    await asyncio.gather(*tasks, return_exceptions=True)

    elapsed = time.time() - start_time
    avg = elapsed / max(len(hospitals), 1)

    log("")
    log("=" * 55)
    log(f"  Batch Complete: {len(hospitals)} hospitals in {elapsed:.0f}s ({avg:.1f}s avg)")
    log(f"  Success: {results['success']}  Partial: {results['partial']}  "
        f"Failed: {results['failed']}  Errors: {results['errors']}")
    log("=" * 55)

    return results


def main():
    parser = argparse.ArgumentParser(
        description="Parallel batch crawler with isolated browsers",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # All Seoul clinics, 5 parallel:
  python3 crawl_batch.py --csv skin_clinics.csv --filter-city 서울 --parallel 5

  # Specific hospitals:
  python3 crawl_batch.py --csv skin_clinics.csv --numbers 123,456,789

  # Random sample:
  python3 crawl_batch.py --csv skin_clinics.csv --filter-city 서울 --sample 10 --seed 42
        """,
    )
    parser.add_argument("--csv", required=True, help="Path to hospital CSV file")
    parser.add_argument("--db", default=DB_DEFAULT, help=f"SQLite DB path (default: {DB_DEFAULT})")
    parser.add_argument("--parallel", type=int, default=3, help="Max concurrent crawlers (default: 3)")
    parser.add_argument("--timeout", type=int, default=45, help="Per-page timeout seconds (default: 45)")
    parser.add_argument("--filter-city", help="Filter by city name in address (e.g., 서울)")
    parser.add_argument("--numbers", help="Comma-separated hospital numbers to crawl")
    parser.add_argument("--sample", type=int, help="Random sample N hospitals from filtered list")
    parser.add_argument("--seed", type=int, default=42, help="Random seed for --sample (default: 42)")
    parser.add_argument("--limit", type=int, help="Limit to first N hospitals")
    parser.add_argument("--skip-crawled", action="store_true", default=True, help="Skip already-crawled (default: true)")
    parser.add_argument("--no-skip-crawled", dest="skip_crawled", action="store_false", help="Re-crawl everything")
    parser.add_argument("--headed", action="store_true", help="Show browser windows (debug)")
    parser.add_argument("--dry-run", action="store_true", help="Show what would be crawled without running")
    parser.add_argument("--output-json", help="Write batch results to JSON file")

    args = parser.parse_args()

    # Load and filter hospitals
    log(f"Loading CSV: {args.csv}")
    hospitals = load_csv(args.csv)
    log(f"Loaded {len(hospitals)} hospitals")

    numbers = None
    if args.numbers:
        numbers = [int(n.strip()) for n in args.numbers.split(",")]

    hospitals = filter_hospitals(
        hospitals,
        city=args.filter_city,
        numbers=numbers,
        skip_crawled=args.skip_crawled,
        db_path=args.db,
    )
    log(f"After filtering: {len(hospitals)} hospitals")

    # Remove hospitals without URLs
    hospitals = [h for h in hospitals if parse_hospital(h).get("url")]
    log(f"With valid URLs: {len(hospitals)} hospitals")

    # Random sample
    if args.sample:
        random.seed(args.seed)
        hospitals = random.sample(hospitals, min(args.sample, len(hospitals)))
        log(f"Random sample (seed={args.seed}): {len(hospitals)} hospitals")

    # Limit
    if args.limit:
        hospitals = hospitals[:args.limit]
        log(f"Limited to: {len(hospitals)} hospitals")

    if not hospitals:
        log("No hospitals to crawl. Exiting.")
        sys.exit(0)

    # Dry run
    if args.dry_run:
        print("\nDry run - would crawl these hospitals:\n")
        for h in hospitals:
            info = parse_hospital(h)
            print(f"  #{info['hospital_no']:>5}  {info['name']:<20}  {info['url']}")
        print(f"\nTotal: {len(hospitals)} hospitals, {args.parallel} parallel workers")
        sys.exit(0)

    # Run batch
    batch_results = asyncio.run(
        run_batch(
            hospitals=hospitals,
            db_path=args.db,
            parallel=args.parallel,
            timeout=args.timeout,
            headless=not args.headed,
        )
    )

    # Output results
    if args.output_json:
        with open(args.output_json, "w", encoding="utf-8") as f:
            json.dump(batch_results, f, ensure_ascii=False, indent=2)
        log(f"Results written to {args.output_json}")

    # Auto-export unified CSV after batch completion
    if batch_results["success"] + batch_results["partial"] > 0:
        log(f"Exporting unified CSV to {CSV_UNIFIED_OUTPUT}")
        try:
            csv_src = args.csv if hasattr(args, "csv") else CSV_SOURCE
            export_unified_csv(args.db, csv_src, CSV_UNIFIED_OUTPUT)
        except Exception as e:
            log(f"CSV export failed: {e}")

    # Exit code: 0 if any success, 1 if all failed
    if batch_results["success"] + batch_results["partial"] > 0:
        sys.exit(0)
    else:
        sys.exit(1)


if __name__ == "__main__":
    main()
