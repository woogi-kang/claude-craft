#!/usr/bin/env python3
"""Lightweight storage manager for clinic crawl results.

Uses Python stdlib only (sqlite3, json, csv, argparse).
No external dependencies required.

Usage:
    python storage_manager.py save --json '{"hospital_no": 6, ...}' --db hospitals.db
    python storage_manager.py save --json-file result.json --db hospitals.db
    python storage_manager.py export --db hospitals.db --output ./exports/
    python storage_manager.py stats --db hospitals.db
"""

import argparse
import csv
import json
import sqlite3
import sys
from datetime import datetime, timezone
from pathlib import Path

DB_DEFAULT = "data/clinic-results/hospitals.db"

SCHEMA_SQL = """
CREATE TABLE IF NOT EXISTS hospitals (
    hospital_no INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    url TEXT,
    category TEXT,
    phone TEXT,
    address TEXT,
    status TEXT DEFAULT 'pending',
    crawled_at TEXT,
    created_at TEXT DEFAULT (datetime('now')),
    updated_at TEXT DEFAULT (datetime('now'))
);

CREATE TABLE IF NOT EXISTS social_channels (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    hospital_no INTEGER NOT NULL,
    platform TEXT NOT NULL,
    url TEXT NOT NULL,
    extraction_method TEXT,
    confidence REAL DEFAULT 1.0,
    created_at TEXT DEFAULT (datetime('now')),
    FOREIGN KEY (hospital_no) REFERENCES hospitals(hospital_no),
    UNIQUE(hospital_no, platform, url)
);

CREATE TABLE IF NOT EXISTS doctors (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    hospital_no INTEGER NOT NULL,
    name TEXT,
    name_english TEXT,
    role TEXT DEFAULT 'specialist',
    photo_url TEXT,
    education_json TEXT DEFAULT '[]',
    career_json TEXT DEFAULT '[]',
    credentials_json TEXT DEFAULT '[]',
    ocr_source INTEGER DEFAULT 0,
    created_at TEXT DEFAULT (datetime('now')),
    FOREIGN KEY (hospital_no) REFERENCES hospitals(hospital_no)
);

CREATE TABLE IF NOT EXISTS crawl_errors (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    hospital_no INTEGER NOT NULL,
    error_type TEXT,
    message TEXT,
    created_at TEXT DEFAULT (datetime('now')),
    FOREIGN KEY (hospital_no) REFERENCES hospitals(hospital_no)
);
"""


def get_db(db_path: str) -> sqlite3.Connection:
    path = Path(db_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(str(path))
    conn.row_factory = sqlite3.Row
    conn.executescript(SCHEMA_SQL)
    return conn


def save_result(db_path: str, data: dict) -> None:
    conn = get_db(db_path)
    now = datetime.now(timezone.utc).isoformat()

    hospital_no = data["hospital_no"]
    name = data.get("name", "")
    url = data.get("url", "")
    category = data.get("category", "")
    phone = data.get("phone", "")
    address = data.get("address", "")
    status = data.get("status", "success")

    conn.execute(
        """INSERT INTO hospitals (hospital_no, name, url, category, phone, address, status, crawled_at, updated_at)
           VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
           ON CONFLICT(hospital_no) DO UPDATE SET
             name=excluded.name, url=excluded.url, category=excluded.category,
             phone=excluded.phone, address=excluded.address, status=excluded.status,
             crawled_at=excluded.crawled_at, updated_at=excluded.updated_at""",
        (hospital_no, name, url, category, phone, address, status, now, now),
    )

    for ch in data.get("social_channels", []):
        conn.execute(
            """INSERT OR IGNORE INTO social_channels
               (hospital_no, platform, url, extraction_method, confidence)
               VALUES (?, ?, ?, ?, ?)""",
            (
                hospital_no,
                ch.get("platform", ""),
                ch.get("url", ""),
                ch.get("extraction_method", ""),
                ch.get("confidence", 1.0),
            ),
        )

    # Remove existing doctors for this hospital before inserting new ones
    conn.execute("DELETE FROM doctors WHERE hospital_no = ?", (hospital_no,))
    for doc in data.get("doctors", []):
        conn.execute(
            """INSERT INTO doctors
               (hospital_no, name, name_english, role, photo_url,
                education_json, career_json, credentials_json, ocr_source)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
            (
                hospital_no,
                doc.get("name", ""),
                doc.get("name_english", ""),
                doc.get("role", ""),
                doc.get("photo_url", ""),
                json.dumps(doc.get("education", []), ensure_ascii=False),
                json.dumps(doc.get("career", []), ensure_ascii=False),
                json.dumps(doc.get("credentials", []), ensure_ascii=False),
                1 if doc.get("ocr_source") else 0,
            ),
        )

    for err in data.get("errors", []):
        if isinstance(err, str):
            conn.execute(
                "INSERT INTO crawl_errors (hospital_no, error_type, message) VALUES (?, ?, ?)",
                (hospital_no, "general", err),
            )
        elif isinstance(err, dict):
            conn.execute(
                "INSERT INTO crawl_errors (hospital_no, error_type, message) VALUES (?, ?, ?)",
                (hospital_no, err.get("type", "general"), err.get("message", "")),
            )
        else:
            conn.execute(
                "INSERT INTO crawl_errors (hospital_no, error_type, message) VALUES (?, ?, ?)",
                (hospital_no, "unknown", str(err)),
            )

    conn.commit()
    conn.close()
    print(f"Saved hospital #{hospital_no} ({name})")


def export_csv(db_path: str, output_dir: str) -> None:
    conn = get_db(db_path)
    out = Path(output_dir)
    out.mkdir(parents=True, exist_ok=True)

    # Hospitals CSV
    rows = conn.execute("SELECT * FROM hospitals ORDER BY hospital_no").fetchall()
    if rows:
        with open(out / "hospitals.csv", "w", newline="", encoding="utf-8-sig") as f:
            writer = csv.writer(f)
            writer.writerow(rows[0].keys())
            writer.writerows(rows)
        print(f"Exported {len(rows)} hospitals -> {out / 'hospitals.csv'}")

    # Social channels CSV
    rows = conn.execute(
        "SELECT sc.*, h.name as hospital_name FROM social_channels sc JOIN hospitals h ON sc.hospital_no = h.hospital_no ORDER BY sc.hospital_no"
    ).fetchall()
    if rows:
        with open(out / "social_channels.csv", "w", newline="", encoding="utf-8-sig") as f:
            writer = csv.writer(f)
            writer.writerow(rows[0].keys())
            writer.writerows(rows)
        print(f"Exported {len(rows)} social channels -> {out / 'social_channels.csv'}")

    # Doctors CSV
    rows = conn.execute(
        "SELECT d.*, h.name as hospital_name FROM doctors d JOIN hospitals h ON d.hospital_no = h.hospital_no ORDER BY d.hospital_no"
    ).fetchall()
    if rows:
        with open(out / "doctors.csv", "w", newline="", encoding="utf-8-sig") as f:
            writer = csv.writer(f)
            writer.writerow(rows[0].keys())
            writer.writerows(rows)
        print(f"Exported {len(rows)} doctors -> {out / 'doctors.csv'}")

    conn.close()


def show_stats(db_path: str) -> None:
    conn = get_db(db_path)

    total = conn.execute("SELECT COUNT(*) FROM hospitals").fetchone()[0]
    by_status = conn.execute(
        "SELECT status, COUNT(*) as cnt FROM hospitals GROUP BY status ORDER BY cnt DESC"
    ).fetchall()

    social_total = conn.execute("SELECT COUNT(*) FROM social_channels").fetchone()[0]
    by_platform = conn.execute(
        "SELECT platform, COUNT(*) as cnt FROM social_channels GROUP BY platform ORDER BY cnt DESC"
    ).fetchall()

    doctor_total = conn.execute("SELECT COUNT(*) FROM doctors").fetchone()[0]
    ocr_count = conn.execute("SELECT COUNT(*) FROM doctors WHERE ocr_source = 1").fetchone()[0]

    error_total = conn.execute("SELECT COUNT(*) FROM crawl_errors").fetchone()[0]

    print(f"\n{'='*50}")
    print(f"  Clinic Crawl Statistics")
    print(f"{'='*50}")
    print(f"\n  Hospitals: {total}")
    for row in by_status:
        print(f"    {row['status']}: {row['cnt']}")

    print(f"\n  Social Channels: {social_total}")
    for row in by_platform:
        print(f"    {row['platform']}: {row['cnt']}")

    print(f"\n  Doctors: {doctor_total}")
    if ocr_count:
        print(f"    OCR-extracted: {ocr_count}")
        print(f"    DOM-extracted: {doctor_total - ocr_count}")

    print(f"\n  Errors: {error_total}")
    print(f"{'='*50}\n")

    conn.close()


def main():
    parser = argparse.ArgumentParser(description="Clinic crawl storage manager")
    sub = parser.add_subparsers(dest="command", required=True)

    # save command
    p_save = sub.add_parser("save", help="Save crawl result to DB")
    p_save.add_argument("--json", help="JSON string of crawl result")
    p_save.add_argument("--json-file", help="Path to JSON file with crawl result")
    p_save.add_argument("--db", default=DB_DEFAULT, help=f"SQLite DB path (default: {DB_DEFAULT})")

    # export command
    p_export = sub.add_parser("export", help="Export DB to CSV files")
    p_export.add_argument("--db", default=DB_DEFAULT, help=f"SQLite DB path (default: {DB_DEFAULT})")
    p_export.add_argument("--output", default="data/clinic-results/exports/", help="Output directory")

    # stats command
    p_stats = sub.add_parser("stats", help="Show crawl statistics")
    p_stats.add_argument("--db", default=DB_DEFAULT, help=f"SQLite DB path (default: {DB_DEFAULT})")

    args = parser.parse_args()

    try:
        if args.command == "save":
            if args.json:
                try:
                    data = json.loads(args.json)
                except json.JSONDecodeError as e:
                    print(f"Error: Invalid JSON - {e}", file=sys.stderr)
                    sys.exit(1)
            elif args.json_file:
                try:
                    with open(args.json_file, encoding="utf-8") as f:
                        data = json.load(f)
                except FileNotFoundError:
                    print(f"Error: File not found - {args.json_file}", file=sys.stderr)
                    sys.exit(1)
                except json.JSONDecodeError as e:
                    print(f"Error: Invalid JSON in file - {e}", file=sys.stderr)
                    sys.exit(1)
            else:
                print("Error: --json or --json-file required", file=sys.stderr)
                sys.exit(1)
            if "hospital_no" not in data:
                print("Error: 'hospital_no' is required in JSON data", file=sys.stderr)
                sys.exit(1)
            save_result(args.db, data)

        elif args.command == "export":
            export_csv(args.db, args.output)

        elif args.command == "stats":
            show_stats(args.db)
    except PermissionError as e:
        print(f"Error: Permission denied - {e}", file=sys.stderr)
        sys.exit(1)
    except sqlite3.Error as e:
        print(f"Error: Database error - {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
