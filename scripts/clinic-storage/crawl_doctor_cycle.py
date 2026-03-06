#!/usr/bin/env python3
"""Batch crawl pipeline with LLM quality assessment and auto-retry.

Workflow:
  1. --reset: Clear DB + pre-populate from hospitals_with_address.csv
  2. Batch crawl pending hospitals
  3. Quality assessment (good / suspicious / failed)
  4. Auto re-crawl suspicious hospitals once
  5. Still suspicious after retry -> needs_review
  6. Export flat CSV (1 row per hospital)

Usage:
    # Full reset + crawl:
    python3 crawl_doctor_cycle.py --csv data/clinic-results/hospitals_with_address.csv --reset

    # Continue crawling (no reset):
    python3 crawl_doctor_cycle.py --csv data/clinic-results/hospitals_with_address.csv

    # Dry run (preview):
    python3 crawl_doctor_cycle.py --csv data/clinic-results/hospitals_with_address.csv --dry-run

    # Skip auto-retry:
    python3 crawl_doctor_cycle.py --csv data/clinic-results/hospitals_with_address.csv --no-retry

    # Re-crawl specific hospitals:
    python3 crawl_doctor_cycle.py --csv data/clinic-results/hospitals_with_address.csv --recrawl 20951918,1721660349
"""

import argparse
import asyncio
import sys
from datetime import datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from crawl_batch import filter_hospitals, load_csv, log, parse_hospital, run_batch
from storage_manager import (
    DB_DEFAULT,
    export_unified_csv,
    get_db,
    prepopulate_hospitals,
    reset_db,
)

CSV_DEFAULT = str(Path(__file__).resolve().parent.parent.parent / "data" / "clinic-results" / "hospitals_with_address.csv")
CSV_OUTPUT = str(Path(__file__).resolve().parent.parent.parent / "data" / "clinic-results" / "exports" / "clinic_results.csv")


def assess_quality(db_path: str, place_ids: list) -> dict:
    """Assess crawl quality for a set of hospitals.

    Returns dict with keys: good, suspicious, failed (each a list of place_ids).

    - good: doctor_count >= 1 AND has >= 2 credential items
    - suspicious: site accessible but 0 doctors, or no credentials at all
    - failed: DNS error, robots_blocked, encoding_error, etc.
    """
    conn = get_db(db_path)
    result = {"good": [], "suspicious": [], "failed": []}

    failed_statuses = {"failed", "robots_blocked", "encoding_error", "unsupported", "age_restricted"}

    for pid in place_ids:
        hosp = conn.execute("SELECT status FROM hospitals WHERE place_id = ?", (pid,)).fetchone()
        if not hosp:
            result["failed"].append(pid)
            continue

        status = hosp["status"]
        if status in failed_statuses:
            result["failed"].append(pid)
            continue

        # Count doctors and credentials
        doctors = conn.execute(
            "SELECT name, profile_raw_json FROM doctors WHERE place_id = ?", (pid,)
        ).fetchall()

        doctor_count = len(doctors)
        total_creds = 0
        for doc in doctors:
            try:
                import json
                raw = json.loads(doc["profile_raw_json"] or "[]")
                total_creds += len(raw)
            except Exception:
                pass

        if doctor_count >= 1 and total_creds >= 2:
            result["good"].append(pid)
        elif status in ("success", "partial", "empty"):
            result["suspicious"].append(pid)
        else:
            result["failed"].append(pid)

    conn.close()
    return result


def mark_needs_review(db_path: str, place_ids: list) -> None:
    """Mark hospitals as needs_review after failed retry."""
    if not place_ids:
        return
    conn = get_db(db_path)
    for pid in place_ids:
        conn.execute(
            "UPDATE hospitals SET status = 'needs_review', updated_at = datetime('now') WHERE place_id = ?",
            (pid,),
        )
    conn.commit()
    conn.close()
    log(f"Marked {len(place_ids)} hospitals as needs_review")


def main():
    parser = argparse.ArgumentParser(
        description="Batch crawl pipeline with quality assessment and auto-retry",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Workflow:
  1. --reset: Clear DB + pre-populate from CSV
  2. Crawl pending hospitals in batches
  3. Assess quality -> auto retry suspicious
  4. Export flat CSV (1 row per hospital)
        """,
    )
    parser.add_argument("--csv", default=CSV_DEFAULT, help=f"Source CSV (default: {CSV_DEFAULT})")
    parser.add_argument("--db", default=DB_DEFAULT, help=f"SQLite DB path (default: {DB_DEFAULT})")
    parser.add_argument("--batch-size", type=int, default=10, help="Hospitals per batch (default: 10)")
    parser.add_argument("--parallel", type=int, default=3, help="Max concurrent crawlers (default: 3)")
    parser.add_argument("--timeout", type=int, default=45, help="Per-page timeout seconds (default: 45)")
    parser.add_argument("--headed", action="store_true", help="Show browser windows (debug)")
    parser.add_argument("--reset", action="store_true", help="Reset DB and pre-populate from CSV")
    parser.add_argument("--no-retry", action="store_true", help="Skip auto-retry of suspicious hospitals")
    parser.add_argument("--recrawl", help="Comma-separated place IDs to force re-crawl")
    parser.add_argument("--district", help="Filter by district (e.g. 강남구, 서초구)")
    parser.add_argument("--dry-run", action="store_true", help="Preview next batch without crawling")
    parser.add_argument("--export-only", action="store_true", help="Only export CSV, no crawling")
    args = parser.parse_args()

    # Step 1: Reset if requested
    if args.reset:
        log("Resetting database...")
        reset_db(args.db)
        log(f"Pre-populating from {args.csv}...")
        count = prepopulate_hospitals(args.db, args.csv)
        log(f"Pre-populated {count} hospitals")

    # Export-only mode
    if args.export_only:
        log("Exporting flat CSV...")
        export_unified_csv(args.db, args.csv, CSV_OUTPUT)
        sys.exit(0)

    # Load CSV
    log(f"Loading CSV: {args.csv}")
    all_hospitals = load_csv(args.csv)
    log(f"Total hospitals in CSV: {len(all_hospitals)}")

    # Handle re-crawl mode
    if args.recrawl:
        recrawl_ids = [pid.strip() for pid in args.recrawl.split(",")]
        pid_set = set(recrawl_ids)
        # Match by both old and new column names
        hospitals = [
            h for h in all_hospitals
            if (h.get("naver_place_id") or h.get("place_id", "")) in pid_set
        ]

        if not hospitals:
            log(f"No matching hospitals found for place IDs: {recrawl_ids}")
            sys.exit(1)

        log(f"Re-crawl mode: {len(hospitals)} hospitals")

        if args.dry_run:
            _print_dry_run(hospitals, "RE-CRAWL")
            sys.exit(0)

        results = asyncio.run(run_batch(
            hospitals=hospitals,
            db_path=args.db,
            parallel=args.parallel,
            timeout=args.timeout,
            headless=not args.headed,
        ))
        _print_summary("Re-crawl", results, len(hospitals))
        log("Exporting flat CSV...")
        export_unified_csv(args.db, args.csv, CSV_OUTPUT)
        sys.exit(0)

    # Filter by district if specified
    if args.district:
        all_hospitals = [
            h for h in all_hospitals
            if args.district in (h.get("sggu", "") or h.get("address", ""))
        ]
        log(f"Filtered to {args.district}: {len(all_hospitals)} hospitals")

    # Normal batch mode: filter out already-crawled
    hospitals = filter_hospitals(
        all_hospitals,
        skip_crawled=True,
        homepage_only=True,
        db_path=args.db,
    )
    log(f"Remaining uncrawled: {len(hospitals)}")

    if not hospitals:
        log("All hospitals have been crawled. Nothing to do.")
        log("Exporting flat CSV...")
        export_unified_csv(args.db, args.csv, CSV_OUTPUT)
        sys.exit(0)

    # Take next batch
    batch = hospitals[:args.batch_size]

    if args.dry_run:
        _print_dry_run(batch, f"NEXT BATCH ({len(batch)} of {len(hospitals)} remaining)")
        sys.exit(0)

    # Step 2: Batch crawl
    log(f"\n--- Crawling {len(batch)} hospitals ---\n")
    results = asyncio.run(run_batch(
        hospitals=batch,
        db_path=args.db,
        parallel=args.parallel,
        timeout=args.timeout,
        headless=not args.headed,
    ))

    # Step 3: Quality assessment
    batch_pids = [parse_hospital(h)["place_id"] for h in batch]
    quality = assess_quality(args.db, batch_pids)
    log(f"Quality: good={len(quality['good'])} suspicious={len(quality['suspicious'])} failed={len(quality['failed'])}")

    # Step 4: Auto-retry suspicious
    if quality["suspicious"] and not args.no_retry:
        log(f"\n--- Auto-retrying {len(quality['suspicious'])} suspicious hospitals ---\n")
        retry_hospitals = [
            h for h in batch
            if parse_hospital(h)["place_id"] in set(quality["suspicious"])
        ]
        asyncio.run(run_batch(
            hospitals=retry_hospitals,
            db_path=args.db,
            parallel=args.parallel,
            timeout=args.timeout,
            headless=not args.headed,
        ))

        # Re-assess after retry
        quality2 = assess_quality(args.db, quality["suspicious"])
        log(f"After retry: good={len(quality2['good'])} still_suspicious={len(quality2['suspicious'])} failed={len(quality2['failed'])}")

        # Step 5: Mark still-suspicious as needs_review
        still_bad = quality2["suspicious"] + quality2["failed"]
        mark_needs_review(args.db, still_bad)

    elif quality["suspicious"]:
        log(f"Skipping retry (--no-retry). Marking {len(quality['suspicious'])} as needs_review")
        mark_needs_review(args.db, quality["suspicious"])

    # Step 6: Export flat CSV
    remaining = len(hospitals) - len(batch)
    _print_summary("Batch", results, remaining)

    log("Exporting flat CSV...")
    export_unified_csv(args.db, args.csv, CSV_OUTPUT)


def _print_dry_run(hospitals: list, label: str):
    print(f"\n{'='*60}")
    print(f"  DRY RUN - {label}")
    print(f"{'='*60}\n")
    for h in hospitals:
        info = parse_hospital(h)
        print(f"  {info['place_id']:>12}  {info['name']:<25}  {info['url']}")
    print()


def _print_summary(label: str, results: dict, remaining: int):
    print(f"\n{'='*60}")
    print(f"  {label} Complete")
    print(f"  Success: {results['success']}  Partial: {results['partial']}  Failed: {results['failed']}")
    if remaining > 0:
        print(f"  Remaining: {remaining} hospitals")
    print(f"{'='*60}")


if __name__ == "__main__":
    main()
