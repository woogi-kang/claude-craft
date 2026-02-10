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
import re
import sqlite3
import sys
import unicodedata
from datetime import datetime, timezone
from pathlib import Path

VALID_PLATFORMS = {
    "KakaoTalk", "NaverTalk", "Line", "WeChat", "WhatsApp",
    "Telegram", "FacebookMessenger", "Instagram", "YouTube",
    "NaverBlog", "NaverBooking", "Facebook", "Phone", "SMS",
}

VALID_STATUSES = {
    "success", "partial", "failed", "archived",
    "requires_manual", "age_restricted", "unsupported",
    "encoding_error", "robots_blocked",
}

DB_DEFAULT = "data/clinic-results/hospitals.db"

SCHEMA_SQL = """
CREATE TABLE IF NOT EXISTS hospitals (
    hospital_no INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    url TEXT,
    final_url TEXT,
    category TEXT,
    phone TEXT,
    address TEXT,
    status TEXT DEFAULT 'pending',
    cms_platform TEXT,
    schema_version TEXT DEFAULT '2.0.0',
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
    status TEXT DEFAULT 'active',
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
    branch TEXT,
    branches_json TEXT DEFAULT '[]',
    extraction_source TEXT,
    ocr_source INTEGER DEFAULT 0,
    created_at TEXT DEFAULT (datetime('now')),
    FOREIGN KEY (hospital_no) REFERENCES hospitals(hospital_no)
);

CREATE TABLE IF NOT EXISTS crawl_errors (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    hospital_no INTEGER NOT NULL,
    error_type TEXT,
    message TEXT,
    step TEXT,
    retryable INTEGER DEFAULT 0,
    created_at TEXT DEFAULT (datetime('now')),
    FOREIGN KEY (hospital_no) REFERENCES hospitals(hospital_no)
);

CREATE INDEX IF NOT EXISTS idx_hospitals_status ON hospitals(status);
CREATE INDEX IF NOT EXISTS idx_hospitals_crawled_at ON hospitals(crawled_at);
CREATE INDEX IF NOT EXISTS idx_social_hospital ON social_channels(hospital_no);
CREATE INDEX IF NOT EXISTS idx_doctors_hospital ON doctors(hospital_no);
CREATE INDEX IF NOT EXISTS idx_errors_hospital ON crawl_errors(hospital_no);
"""

# Schema migrations: version -> SQL statement
# Applied incrementally via PRAGMA user_version tracking
MIGRATIONS = {
    1: "ALTER TABLE social_channels ADD COLUMN verified_at TEXT",
    2: "ALTER TABLE doctors ADD COLUMN ocr_confidence REAL DEFAULT 0.0",
    3: "ALTER TABLE crawl_errors ADD COLUMN retry_count INTEGER DEFAULT 0",
    4: """CREATE TABLE IF NOT EXISTS ocr_cache (
        image_hash TEXT PRIMARY KEY,
        result_json TEXT NOT NULL,
        created_at TEXT DEFAULT (datetime('now'))
    )""",
    5: "ALTER TABLE hospitals ADD COLUMN final_url TEXT",
    6: "ALTER TABLE hospitals ADD COLUMN cms_platform TEXT",
    7: "ALTER TABLE hospitals ADD COLUMN schema_version TEXT DEFAULT '2.0.0'",
    8: "ALTER TABLE social_channels ADD COLUMN status TEXT DEFAULT 'active'",
    9: "ALTER TABLE crawl_errors ADD COLUMN step TEXT",
    10: "ALTER TABLE crawl_errors ADD COLUMN retryable INTEGER DEFAULT 0",
    11: "ALTER TABLE doctors ADD COLUMN branch TEXT",
    12: "ALTER TABLE doctors ADD COLUMN branches_json TEXT DEFAULT '[]'",
    13: "ALTER TABLE doctors ADD COLUMN extraction_source TEXT",
    14: "ALTER TABLE hospitals ADD COLUMN doctor_page_exists INTEGER",
}


def _run_migrations(conn: sqlite3.Connection) -> None:
    """Apply pending schema migrations based on PRAGMA user_version."""
    current = conn.execute("PRAGMA user_version").fetchone()[0]
    for ver in sorted(MIGRATIONS):
        if ver > current:
            try:
                conn.execute(MIGRATIONS[ver])
                conn.execute(f"PRAGMA user_version = {ver}")
                print(f"Migration v{ver} applied", file=sys.stderr)
            except sqlite3.OperationalError as e:
                # Skip if column/table already exists (idempotent)
                if "duplicate column" not in str(e).lower() and "already exists" not in str(e).lower():
                    raise


def get_db(db_path: str) -> sqlite3.Connection:
    path = Path(db_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(str(path))
    conn.row_factory = sqlite3.Row
    # WAL mode for concurrent read/write performance during batch crawls
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("PRAGMA busy_timeout=5000")
    conn.executescript(SCHEMA_SQL)
    _run_migrations(conn)
    return conn


def _normalize(text: str) -> str:
    """Normalize Unicode to NFC form for consistent storage/comparison."""
    if text:
        return unicodedata.normalize("NFC", text)
    return text


def _escape_csv_formula(value: str) -> str:
    """Escape CSV injection prefixes (=, +, -, @) for safe Excel import."""
    if isinstance(value, str) and value and value[0] in ("=", "+", "-", "@"):
        return "'" + value
    return value


_KOREAN_PHONE_RE = re.compile(
    r"^(\+82|0)\d{1,2}[-\s.]?\d{3,4}[-\s.]?\d{4}$"
)
_VALID_URL_SCHEMES = ("http://", "https://", "tel:", "sms:", "kakao://", "line://", "weixin://")


def _validate_channel_url(url: str, platform: str) -> bool:
    """Validate URL format based on platform type."""
    if not url:
        return False
    if platform == "Phone":
        # Strip tel: prefix before regex validation
        phone = url.removeprefix("tel:").removeprefix("tel://").strip()
        return bool(_KOREAN_PHONE_RE.match(phone))
    if platform == "SMS":
        return url.startswith("sms:")
    return url.startswith(_VALID_URL_SCHEMES)


def _validate_channel(ch: dict) -> dict:
    """Validate and sanitize social channel data."""
    platform = ch.get("platform", "")
    if platform and platform not in VALID_PLATFORMS:
        print(f"Warning: Unknown platform '{platform}', storing as-is", file=sys.stderr)
    url = ch.get("url", "")
    if url and not _validate_channel_url(url, platform):
        print(f"Warning: Invalid URL format for {platform}: {url[:80]}", file=sys.stderr)
    confidence = ch.get("confidence", 1.0)
    if not (0.0 <= confidence <= 1.0):
        confidence = max(0.0, min(1.0, confidence))
    ch["confidence"] = confidence
    return ch


def save_result(db_path: str, data: dict) -> None:
    conn = get_db(db_path)
    now = datetime.now(timezone.utc).isoformat()

    hospital_no = data["hospital_no"]
    name = _normalize(data.get("name", ""))
    url = data.get("url", "")
    category = data.get("category", "")
    phone = data.get("phone", "")
    address = _normalize(data.get("address", ""))
    status = data.get("status", "success")
    if status not in VALID_STATUSES:
        print(f"Warning: Unknown status '{status}', defaulting to 'partial'", file=sys.stderr)
        status = "partial"

    doctors = data.get("doctors", [])
    new_status = status

    # Case 2 guard: Don't overwrite successful crawl with failed one that has no data
    existing = conn.execute(
        "SELECT status, crawled_at FROM hospitals WHERE hospital_no = ?",
        (hospital_no,),
    ).fetchone()
    if existing and existing["status"] == "success" and new_status == "failed":
        if not doctors and not data.get("social_channels", []):
            print(
                f"Warning: Skipping failed overwrite of successful hospital #{hospital_no}",
                file=sys.stderr,
            )
            conn.close()
            return

    # Case 1 & 3: Wrap ALL operations in a single transaction
    try:
        conn.execute("BEGIN IMMEDIATE")

        final_url = data.get("final_url", "")
        cms_platform = data.get("cms_platform", "")
        schema_version = data.get("schema_version", "2.0.0")

        doctor_page_exists = data.get("doctor_page_exists")

        conn.execute(
            """INSERT INTO hospitals (hospital_no, name, url, final_url, category, phone, address, status, cms_platform, schema_version, doctor_page_exists, crawled_at, updated_at)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
               ON CONFLICT(hospital_no) DO UPDATE SET
                 name=excluded.name, url=excluded.url, final_url=excluded.final_url,
                 category=excluded.category, phone=excluded.phone, address=excluded.address,
                 status=excluded.status, cms_platform=excluded.cms_platform,
                 schema_version=excluded.schema_version, doctor_page_exists=excluded.doctor_page_exists,
                 crawled_at=excluded.crawled_at, updated_at=excluded.updated_at""",
            (hospital_no, name, url, final_url, category, phone, address, new_status, cms_platform, schema_version, doctor_page_exists, now, now),
        )

        # Remove old social channels then insert new
        conn.execute("DELETE FROM social_channels WHERE hospital_no = ?", (hospital_no,))
        for ch in data.get("social_channels", []):
            ch = _validate_channel(ch)
            conn.execute(
                """INSERT OR IGNORE INTO social_channels
                   (hospital_no, platform, url, extraction_method, confidence, status)
                   VALUES (?, ?, ?, ?, ?, ?)""",
                (
                    hospital_no,
                    ch.get("platform", ""),
                    ch.get("url", ""),
                    ch.get("extraction_method", ""),
                    ch.get("confidence", 1.0),
                    ch.get("status", "active"),
                ),
            )

        # Case 2: Always clear old doctors on re-crawl, then insert new ones
        conn.execute("DELETE FROM doctors WHERE hospital_no = ?", (hospital_no,))
        if doctors:
            for doc in doctors:
                doc_name = _normalize(doc.get("name", ""))
                conn.execute(
                    """INSERT INTO doctors
                       (hospital_no, name, name_english, role, photo_url,
                        education_json, career_json, credentials_json,
                        branch, branches_json, extraction_source, ocr_source)
                       VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                    (
                        hospital_no,
                        doc_name,
                        doc.get("name_english", ""),
                        doc.get("role", ""),
                        doc.get("photo_url", ""),
                        json.dumps(doc.get("education") or [], ensure_ascii=False),
                        json.dumps(doc.get("career") or [], ensure_ascii=False),
                        json.dumps(doc.get("credentials") or [], ensure_ascii=False),
                        doc.get("branch", ""),
                        json.dumps(doc.get("branches") or [], ensure_ascii=False),
                        doc.get("extraction_source", ""),
                        1 if doc.get("ocr_source") else 0,
                    ),
                )

        # Clear old errors and insert new
        conn.execute("DELETE FROM crawl_errors WHERE hospital_no = ?", (hospital_no,))
        for err in data.get("errors", []):
            if isinstance(err, str):
                conn.execute(
                    "INSERT INTO crawl_errors (hospital_no, error_type, message, step, retryable) VALUES (?, ?, ?, ?, ?)",
                    (hospital_no, "general", err, "", 0),
                )
            elif isinstance(err, dict):
                conn.execute(
                    "INSERT INTO crawl_errors (hospital_no, error_type, message, step, retryable) VALUES (?, ?, ?, ?, ?)",
                    (hospital_no, err.get("type", "general"), err.get("message", ""),
                     err.get("step", ""), 1 if err.get("retryable") else 0),
                )
            else:
                conn.execute(
                    "INSERT INTO crawl_errors (hospital_no, error_type, message, step, retryable) VALUES (?, ?, ?, ?, ?)",
                    (hospital_no, "unknown", str(err), "", 0),
                )

        conn.commit()
        print(f"Saved hospital #{hospital_no} ({name})")

    except Exception as e:
        conn.rollback()
        print(f"Error: Transaction failed for hospital #{hospital_no}: {e}", file=sys.stderr)
        raise
    finally:
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


def show_dashboard(db_path: str, total_target: int = 4256) -> None:
    """Show detailed crawl progress dashboard."""
    conn = get_db(db_path)

    total = conn.execute("SELECT COUNT(*) FROM hospitals").fetchone()[0]
    by_status = dict(
        conn.execute(
            "SELECT status, COUNT(*) FROM hospitals GROUP BY status"
        ).fetchall()
    )
    success = by_status.get("success", 0)
    partial = by_status.get("partial", 0)
    failed = by_status.get("failed", 0)

    # Success rate
    attempted = success + partial + failed
    success_rate = (success / attempted * 100) if attempted else 0

    # Today's crawls
    today_count = conn.execute(
        "SELECT COUNT(*) FROM hospitals WHERE date(crawled_at) = date('now')"
    ).fetchone()[0]

    # Platform discovery rates (among successful crawls)
    platform_rates = conn.execute(
        """SELECT sc.platform, COUNT(DISTINCT sc.hospital_no) as cnt
           FROM social_channels sc
           JOIN hospitals h ON sc.hospital_no = h.hospital_no
           WHERE h.status IN ('success', 'partial')
           GROUP BY sc.platform ORDER BY cnt DESC"""
    ).fetchall()
    success_partial = success + partial

    # Recent failure patterns
    recent_errors = conn.execute(
        """SELECT error_type, COUNT(*) as cnt
           FROM crawl_errors
           WHERE created_at > datetime('now', '-7 days')
           GROUP BY error_type ORDER BY cnt DESC LIMIT 5"""
    ).fetchall()

    # OCR stats
    doctor_total = conn.execute("SELECT COUNT(*) FROM doctors").fetchone()[0]
    ocr_count = conn.execute("SELECT COUNT(*) FROM doctors WHERE ocr_source = 1").fetchone()[0]

    progress_pct = total / total_target * 100 if total_target else 0

    print(f"\n{'='*55}")
    print(f"  Clinic Crawl Dashboard")
    print(f"{'='*55}")
    print(f"\n  Progress: {total}/{total_target} ({progress_pct:.1f}%)")
    print(f"  Success rate: {success_rate:.0f}% ({success}/{attempted} attempted)")
    print(f"  Today: {today_count} crawls")
    print(f"\n  Status breakdown:")
    for status, cnt in sorted(by_status.items(), key=lambda x: -x[1]):
        print(f"    {status}: {cnt}")
    if success_partial:
        print(f"\n  Platform discovery rates (of {success_partial} crawled):")
        for row in platform_rates:
            rate = row["cnt"] / success_partial * 100
            print(f"    {row['platform']}: {row['cnt']} ({rate:.0f}%)")
    print(f"\n  Doctors: {doctor_total} (OCR: {ocr_count}, DOM: {doctor_total - ocr_count})")
    if recent_errors:
        print(f"\n  Recent failure patterns (7 days):")
        for row in recent_errors:
            print(f"    {row['error_type']}: {row['cnt']}")
    print(f"{'='*55}\n")
    conn.close()


def show_retry_queue(db_path: str) -> None:
    """Show hospitals eligible for retry, prioritized."""
    conn = get_db(db_path)

    rows = conn.execute(
        """SELECT h.hospital_no, h.name, h.status, h.url, h.crawled_at,
                  GROUP_CONCAT(DISTINCT ce.error_type) as error_types,
                  MAX(ce.retry_count) as max_retries
           FROM hospitals h
           LEFT JOIN crawl_errors ce ON h.hospital_no = ce.hospital_no
           WHERE h.status IN ('partial', 'failed')
           GROUP BY h.hospital_no
           ORDER BY
             CASE h.status WHEN 'partial' THEN 0 ELSE 1 END,
             COALESCE(MAX(ce.retry_count), 0) ASC,
             h.crawled_at ASC
           LIMIT 50"""
    ).fetchall()

    print(f"\n{'='*55}")
    print(f"  Retry Queue ({len(rows)} hospitals)")
    print(f"{'='*55}")
    if not rows:
        print("  No hospitals to retry.")
    for row in rows:
        retries = row["max_retries"] or 0
        errors = row["error_types"] or "unknown"
        print(f"  #{row['hospital_no']} {row['name']}")
        print(f"    status={row['status']} retries={retries} errors={errors}")
        print(f"    url={row['url']}")
    print(f"{'='*55}\n")
    conn.close()


def export_csv(db_path: str, output_dir: str, since: str = None) -> None:
    conn = get_db(db_path)
    out = Path(output_dir)
    out.mkdir(parents=True, exist_ok=True)

    since_clause = ""
    since_params = ()
    if since:
        since_clause = " WHERE h.updated_at >= ?"
        since_params = (since,)
        print(f"Incremental export: changes since {since}")

    def _safe_row(row):
        return [_escape_csv_formula(str(v) if v is not None else "") for v in row]

    # Hospitals CSV
    query = f"SELECT * FROM hospitals h{since_clause.replace('h.', '')} ORDER BY hospital_no"
    rows = conn.execute(query.replace("h.", ""), since_params).fetchall()
    if rows:
        suffix = f"_since_{since.replace('-', '')}" if since else ""
        fname = f"hospitals{suffix}.csv"
        with open(out / fname, "w", newline="", encoding="utf-8-sig") as f:
            writer = csv.writer(f)
            writer.writerow(rows[0].keys())
            for row in rows:
                writer.writerow(_safe_row(row))
        print(f"Exported {len(rows)} hospitals -> {out / fname}")

    # Social channels CSV
    if since:
        rows = conn.execute(
            "SELECT sc.*, h.name as hospital_name FROM social_channels sc JOIN hospitals h ON sc.hospital_no = h.hospital_no WHERE h.updated_at >= ? ORDER BY sc.hospital_no",
            since_params,
        ).fetchall()
    else:
        rows = conn.execute(
            "SELECT sc.*, h.name as hospital_name FROM social_channels sc JOIN hospitals h ON sc.hospital_no = h.hospital_no ORDER BY sc.hospital_no"
        ).fetchall()
    if rows:
        suffix = f"_since_{since.replace('-', '')}" if since else ""
        fname = f"social_channels{suffix}.csv"
        with open(out / fname, "w", newline="", encoding="utf-8-sig") as f:
            writer = csv.writer(f)
            writer.writerow(rows[0].keys())
            for row in rows:
                writer.writerow(_safe_row(row))
        print(f"Exported {len(rows)} social channels -> {out / fname}")

    # Doctors CSV
    if since:
        rows = conn.execute(
            "SELECT d.*, h.name as hospital_name FROM doctors d JOIN hospitals h ON d.hospital_no = h.hospital_no WHERE h.updated_at >= ? ORDER BY d.hospital_no",
            since_params,
        ).fetchall()
    else:
        rows = conn.execute(
            "SELECT d.*, h.name as hospital_name FROM doctors d JOIN hospitals h ON d.hospital_no = h.hospital_no ORDER BY d.hospital_no"
        ).fetchall()
    if rows:
        suffix = f"_since_{since.replace('-', '')}" if since else ""
        fname = f"doctors{suffix}.csv"
        with open(out / fname, "w", newline="", encoding="utf-8-sig") as f:
            writer = csv.writer(f)
            writer.writerow(rows[0].keys())
            for row in rows:
                writer.writerow(_safe_row(row))
        print(f"Exported {len(rows)} doctors -> {out / fname}")

    conn.close()


# ---------------------------------------------------------------------------
# Platform name normalization
# ---------------------------------------------------------------------------
_PLATFORM_NORMALIZE = {
    "kakao": "KakaoTalk", "kakaotalk": "KakaoTalk",
    "naver_blog": "NaverBlog", "naverblog": "NaverBlog",
    "naver_talk": "NaverTalk", "navertalk": "NaverTalk",
    "naver_booking": "NaverBooking", "naverbooking": "NaverBooking",
    "instagram": "Instagram",
    "youtube": "YouTube",
    "facebook": "Facebook",
    "facebookmessenger": "FacebookMessenger",
    "phone": "Phone",
    "sms": "SMS",
    "line": "Line",
    "whatsapp": "WhatsApp",
    "wechat": "WeChat",
    "telegram": "Telegram",
    "online_consultation": "OnlineConsultation",
}

# Ordered social columns for unified CSV
_SOCIAL_COLUMNS = [
    "KakaoTalk", "NaverTalk", "Line", "WhatsApp", "WeChat",
    "Telegram", "Instagram", "NaverBlog", "YouTube",
    "Facebook", "NaverBooking", "Phone",
]


def _normalize_platform(name: str) -> str:
    """Normalize platform name to canonical form."""
    return _PLATFORM_NORMALIZE.get(name.lower(), name)


def export_unified_csv(db_path: str, csv_source: str, output_path: str) -> None:
    """Export a single unified CSV merging original CSV + crawl DB.

    One row per doctor (expanded). Hospitals with no doctors get one row.
    All hospitals from csv_source are included (uncrawled = not_crawled).

    Column order: identification -> contact -> social channels -> doctor -> meta
    """
    import csv as csv_mod

    conn = get_db(db_path)
    out = Path(output_path)
    out.parent.mkdir(parents=True, exist_ok=True)

    # Load original CSV (all hospitals)
    source_hospitals = {}
    with open(csv_source, encoding="utf-8-sig") as f:
        reader = csv_mod.DictReader(f)
        for row in reader:
            clean = {k.strip(): (v.strip() if v else "") for k, v in row.items() if k}
            no = int(clean.get("NO", clean.get("no", 0)))
            source_hospitals[no] = {
                "name": clean.get("병원/약국명") or clean.get("naver_name") or "",
                "phone": clean.get("전화번호") or "",
                "address": clean.get("소재지주소") or clean.get("naver_address") or "",
                "website": clean.get("naver_website") or clean.get("홈페이지") or "",
            }

    # Load crawl results from DB
    crawled = {}
    for row in conn.execute("SELECT * FROM hospitals").fetchall():
        crawled[row["hospital_no"]] = dict(row)

    # Load social channels grouped by hospital
    social_map = {}  # hospital_no -> {platform: url}
    for row in conn.execute("SELECT hospital_no, platform, url FROM social_channels ORDER BY id"):
        hno = row["hospital_no"]
        platform = _normalize_platform(row["platform"])
        if hno not in social_map:
            social_map[hno] = {}
        # Keep first URL per platform (de-dup)
        if platform not in social_map[hno]:
            social_map[hno][platform] = row["url"]

    # Load doctors grouped by hospital
    doctor_map = {}  # hospital_no -> [doctor_dict, ...]
    for row in conn.execute("SELECT * FROM doctors ORDER BY hospital_no, id"):
        hno = row["hospital_no"]
        if hno not in doctor_map:
            doctor_map[hno] = []
        edu = json.loads(row["education_json"] or "[]")
        career = json.loads(row["career_json"] or "[]")
        creds = json.loads(row["credentials_json"] or "[]")
        doctor_map[hno].append({
            "name": row["name"] or "",
            "role": row["role"] or "",
            "education": " | ".join(edu) if edu else "",
            "career": " | ".join(career) if career else "",
            "credentials": " | ".join(creds) if creds else "",
            "ocr": "OCR" if row["ocr_source"] else "DOM",
        })

    # Build unified CSV
    headers = [
        # Identification
        "no", "name", "status",
        # Contact
        "phone", "address",
        # Social channels (ordered)
        *[p.lower() for p in _SOCIAL_COLUMNS],
        # Doctor info (expanded)
        "doctor_count", "doctor_name", "doctor_role",
        "doctor_education", "doctor_career", "doctor_credentials",
        "doctor_source",
        # Meta
        "website", "cms", "crawled_at",
    ]

    rows_written = 0
    with open(out, "w", newline="", encoding="utf-8-sig") as f:
        writer = csv_mod.writer(f)
        writer.writerow(headers)

        for hno in sorted(source_hospitals.keys()):
            src = source_hospitals[hno]
            crawl = crawled.get(hno, {})
            socials = social_map.get(hno, {})
            doctors = doctor_map.get(hno, [])

            # Determine status
            if hno in crawled:
                status = crawl.get("status", "unknown")
            else:
                status = "not_crawled"

            # Base row (everything except doctor fields)
            base = [
                hno,
                src["name"],
                status,
                src["phone"],
                src["address"],
            ]

            # Social columns in order
            for platform in _SOCIAL_COLUMNS:
                url = socials.get(platform, "")
                base.append(_escape_csv_formula(url))

            doctor_count = len(doctors)

            if doctors:
                # Expanded: one row per doctor
                for doc in doctors:
                    row = base + [
                        doctor_count,
                        _escape_csv_formula(doc["name"]),
                        doc["role"],
                        _escape_csv_formula(doc["education"]),
                        _escape_csv_formula(doc["career"]),
                        _escape_csv_formula(doc["credentials"]),
                        doc["ocr"],
                        _escape_csv_formula(src["website"]),
                        crawl.get("cms_platform", ""),
                        crawl.get("crawled_at", ""),
                    ]
                    writer.writerow(row)
                    rows_written += 1
            else:
                # Single row, empty doctor fields
                row = base + [
                    doctor_count, "", "", "", "", "", "",
                    _escape_csv_formula(src["website"]),
                    crawl.get("cms_platform", ""),
                    crawl.get("crawled_at", ""),
                ]
                writer.writerow(row)
                rows_written += 1

    conn.close()
    total_hospitals = len(source_hospitals)
    crawled_count = len(crawled)
    total_doctors = sum(len(d) for d in doctor_map.values())
    print(f"Exported unified CSV -> {out}")
    print(f"  {rows_written} rows ({total_hospitals} hospitals, {crawled_count} crawled, {total_doctors} doctors)")


def main():
    parser = argparse.ArgumentParser(description="Clinic crawl storage manager")
    sub = parser.add_subparsers(dest="command", required=True)

    # save command
    p_save = sub.add_parser("save", help="Save crawl result to DB")
    p_save.add_argument("--json", help="JSON string of crawl result")
    p_save.add_argument("--json-file", help="Path to JSON file with crawl result")
    p_save.add_argument("--db", default=DB_DEFAULT, help=f"SQLite DB path (default: {DB_DEFAULT})")

    # export command (legacy: separate CSV files)
    p_export = sub.add_parser("export", help="Export DB to CSV files")
    p_export.add_argument("--db", default=DB_DEFAULT, help=f"SQLite DB path (default: {DB_DEFAULT})")
    p_export.add_argument("--output", default="data/clinic-results/exports/", help="Output directory")
    p_export.add_argument("--since", help="Incremental export: only changes since date (YYYY-MM-DD)")

    # unified command (single merged CSV)
    p_unified = sub.add_parser("unified", help="Export single unified CSV (all hospitals + crawl results)")
    p_unified.add_argument("--db", default=DB_DEFAULT, help=f"SQLite DB path (default: {DB_DEFAULT})")
    p_unified.add_argument("--csv", default="data/clinic-results/skin_clinics.csv", help="Source hospital CSV")
    p_unified.add_argument("--output", default="data/clinic-results/exports/clinic_results.csv", help="Output CSV path")

    # stats command
    p_stats = sub.add_parser("stats", help="Show crawl statistics")
    p_stats.add_argument("--db", default=DB_DEFAULT, help=f"SQLite DB path (default: {DB_DEFAULT})")

    # dashboard command
    p_dash = sub.add_parser("dashboard", help="Show detailed crawl progress dashboard")
    p_dash.add_argument("--db", default=DB_DEFAULT, help=f"SQLite DB path (default: {DB_DEFAULT})")
    p_dash.add_argument("--target", type=int, default=4256, help="Total target hospital count")

    # retry-queue command
    p_retry = sub.add_parser("retry-queue", help="Show hospitals eligible for retry")
    p_retry.add_argument("--db", default=DB_DEFAULT, help=f"SQLite DB path (default: {DB_DEFAULT})")

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
            export_csv(args.db, args.output, since=args.since)

        elif args.command == "unified":
            export_unified_csv(args.db, args.csv, args.output)

        elif args.command == "stats":
            show_stats(args.db)

        elif args.command == "dashboard":
            show_dashboard(args.db, total_target=args.target)

        elif args.command == "retry-queue":
            show_retry_queue(args.db)
    except PermissionError as e:
        print(f"Error: Permission denied - {e}", file=sys.stderr)
        sys.exit(1)
    except sqlite3.Error as e:
        print(f"Error: Database error - {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
