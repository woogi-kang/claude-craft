#!/usr/bin/env python3
"""Batch-review cycling wrapper for doctor crawling.

Crawls hospitals in batches of N (default 10), generates a review Excel
after each batch, and waits for user approval before continuing.

Usage:
    # Convert Excel first (one-time):
    python3 convert_excel.py --xlsx data/hospitals_for_crawl.xlsx

    # Crawl next 10 hospitals:
    python3 crawl_doctor_cycle.py --csv data/clinic-results/place_data_doctors.csv

    # Custom batch size:
    python3 crawl_doctor_cycle.py --csv data/clinic-results/place_data_doctors.csv --batch-size 5

    # Re-crawl specific hospitals:
    python3 crawl_doctor_cycle.py --csv data/clinic-results/place_data_doctors.csv --recrawl 20951918,1721660349

    # Dry run (preview next batch):
    python3 crawl_doctor_cycle.py --csv data/clinic-results/place_data_doctors.csv --dry-run
"""

import argparse
import asyncio
import sys
from datetime import datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from crawl_batch import filter_hospitals, load_csv, log, parse_hospital, run_batch
from generate_review import generate_review_excel
from storage_manager import DB_DEFAULT, get_db


REVIEWS_DIR = str(Path(__file__).resolve().parent.parent.parent / "data" / "clinic-results" / "reviews")


def count_crawled_from_csv(db_path: str, csv_place_ids: set) -> int:
    """Count how many hospitals from the CSV are already crawled."""
    try:
        conn = get_db(db_path)
        rows = conn.execute(
            "SELECT place_id FROM hospitals WHERE status IN ('success', 'robots_blocked')"
        ).fetchall()
        conn.close()
        return sum(1 for r in rows if r["place_id"] in csv_place_ids)
    except Exception:
        return 0


def next_batch_number(reviews_dir: str) -> int:
    """Determine next batch number from existing review files."""
    p = Path(reviews_dir)
    if not p.exists():
        return 1
    existing = sorted(p.glob("batch_*.xlsx"))
    if not existing:
        return 1
    last = existing[-1].stem  # e.g. "batch_003"
    try:
        return int(last.split("_")[1]) + 1
    except (IndexError, ValueError):
        return len(existing) + 1


def main():
    parser = argparse.ArgumentParser(
        description="Batch-review cycling wrapper for doctor crawling",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Workflow:
  1. Crawls next N hospitals (skips already-crawled)
  2. Generates review Excel in data/clinic-results/reviews/
  3. User reviews the Excel, then re-runs for next batch

Re-crawl: Use --recrawl to force re-crawl specific place IDs.
        """,
    )
    parser.add_argument("--csv", required=True, help="Path to converted CSV (place_data_doctors.csv)")
    parser.add_argument("--db", default=DB_DEFAULT, help=f"SQLite DB path (default: {DB_DEFAULT})")
    parser.add_argument("--batch-size", type=int, default=10, help="Hospitals per batch (default: 10)")
    parser.add_argument("--parallel", type=int, default=3, help="Max concurrent crawlers (default: 3)")
    parser.add_argument("--timeout", type=int, default=45, help="Per-page timeout seconds (default: 45)")
    parser.add_argument("--headed", action="store_true", help="Show browser windows (debug)")
    parser.add_argument("--recrawl", help="Comma-separated place IDs to force re-crawl")
    parser.add_argument("--dry-run", action="store_true", help="Preview next batch without crawling")
    args = parser.parse_args()

    # Load CSV
    log(f"Loading CSV: {args.csv}")
    all_hospitals = load_csv(args.csv)
    all_place_ids = {h.get("place_id", "") for h in all_hospitals}
    log(f"Total hospitals in CSV: {len(all_hospitals)}")

    # Handle re-crawl mode
    if args.recrawl:
        recrawl_ids = [pid.strip() for pid in args.recrawl.split(",")]
        pid_set = set(recrawl_ids)
        hospitals = [h for h in all_hospitals if h.get("place_id", "") in pid_set]

        if not hospitals:
            log(f"No matching hospitals found for place IDs: {recrawl_ids}")
            sys.exit(1)

        log(f"Re-crawl mode: {len(hospitals)} hospitals")

        if args.dry_run:
            _print_dry_run(hospitals, "RE-CRAWL")
            sys.exit(0)

        # Run crawl (no skip-crawled filter)
        results = asyncio.run(run_batch(
            hospitals=hospitals,
            db_path=args.db,
            parallel=args.parallel,
            timeout=args.timeout,
            headless=not args.headed,
        ))

        # Generate review
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        review_path = str(Path(REVIEWS_DIR) / f"recrawl_{ts}.xlsx")
        batch_pids = [parse_hospital(h)["place_id"] for h in hospitals]
        generate_review_excel(args.db, batch_pids, review_path)

        _print_summary("Re-crawl", results, review_path, 0, args)
        sys.exit(0)

    # Normal batch mode: filter out already-crawled
    hospitals = filter_hospitals(
        all_hospitals,
        skip_crawled=True,
        homepage_only=True,
        db_path=args.db,
    )
    log(f"Remaining uncrawled: {len(hospitals)}")

    if not hospitals:
        crawled = count_crawled_from_csv(args.db, all_place_ids)
        log(f"All {crawled} hospitals have been crawled. Nothing to do.")
        sys.exit(0)

    # Take next batch
    batch = hospitals[:args.batch_size]
    batch_num = next_batch_number(REVIEWS_DIR)

    if args.dry_run:
        _print_dry_run(batch, f"BATCH {batch_num}")
        remaining = len(hospitals) - len(batch)
        print(f"\nRemaining after this batch: {remaining}")
        print(f"Estimated batches left: {(remaining + args.batch_size - 1) // args.batch_size}")
        sys.exit(0)

    # Run crawl
    log(f"\n--- Batch {batch_num}: Crawling {len(batch)} hospitals ---\n")
    results = asyncio.run(run_batch(
        hospitals=batch,
        db_path=args.db,
        parallel=args.parallel,
        timeout=args.timeout,
        headless=not args.headed,
    ))

    # Generate review Excel
    review_path = str(Path(REVIEWS_DIR) / f"batch_{batch_num:03d}.xlsx")
    batch_pids = [parse_hospital(h)["place_id"] for h in batch]
    generate_review_excel(args.db, batch_pids, review_path)

    remaining = len(hospitals) - len(batch)
    _print_summary(f"Batch {batch_num}", results, review_path, remaining, args)


def _print_dry_run(hospitals: list, label: str):
    print(f"\n{'='*60}")
    print(f"  DRY RUN - {label}: {len(hospitals)} hospitals")
    print(f"{'='*60}\n")
    for h in hospitals:
        info = parse_hospital(h)
        print(f"  {info['place_id']:>12}  {info['name']:<25}  {info['url']}")
    print()


def _print_summary(label: str, results: dict, review_path: str, remaining: int, args):
    print(f"\n{'='*60}")
    print(f"  {label} Complete")
    print(f"  Success: {results['success']}  Partial: {results['partial']}  Failed: {results['failed']}")
    print(f"  Review: {review_path}")
    if remaining > 0:
        print(f"  Remaining: {remaining} hospitals")
    print(f"{'='*60}")
    print(f"\nNext steps:")
    print(f"  1. Review:   open {review_path}")
    print(f"  2. Continue: python3 crawl_doctor_cycle.py --csv {args.csv} --batch-size {args.batch_size}")
    print(f"  3. Re-crawl: python3 crawl_doctor_cycle.py --csv {args.csv} --recrawl <place_ids>")


if __name__ == "__main__":
    main()
