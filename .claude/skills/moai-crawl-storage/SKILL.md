---
name: moai-crawl-storage
description: >
  SQLite and JSON dual storage system for Naver hospital crawler covering
  crawl progress tracking, hospital data persistence, resume capability,
  concurrent photo downloading, and atomic file operations.
  Use when working with storage, database schema, download management,
  or resume/recovery logic.
  Do NOT use for data model definitions (use moai-crawl-schema) or
  pipeline orchestration (use moai-crawl-pipeline).
license: Apache-2.0
compatibility: Designed for Claude Code
allowed-tools: Read Grep Glob Bash
user-invocable: false
metadata:
  version: "1.0.0"
  category: "domain"
  status: "active"
  updated: "2026-02-05"
  modularized: "true"
  tags: "crawler, naver, storage, sqlite, json, download, photos, resume, progress"

# MoAI Extension: Progressive Disclosure
progressive_disclosure:
  enabled: true
  level1_tokens: 100
  level2_tokens: 5000

# MoAI Extension: Triggers
triggers:
  keywords:
    - "storage"
    - "sqlite"
    - "json output"
    - "download photos"
    - "resume"
    - "progress"
    - "StorageManager"
    - "PhotoDownloader"
    - "crawl database"
  agents:
    - "naver-hospital-agent"
  phases:
    - "run"
---

# Crawler Storage & Downloads

Dual storage system (SQLite + JSON) with resume capability and concurrent photo downloading.

## Quick Reference

Source Files:
- `crawl/naver_hospital/storage.py` - StorageManager: SQLite progress + JSON hospital data
- `crawl/naver_hospital/downloader.py` - PhotoDownloader: concurrent image downloads

---

## StorageManager API (storage.py)

### Initialization

| Method | Purpose |
|--------|---------|
| `initialize()` | Create directories + SQLite tables with WAL mode |
| `recover_interrupted()` | Reset `in_progress` -> `pending` on startup |

### Progress Tracking

| Method | Purpose |
|--------|---------|
| `register_hospitals(names)` | INSERT OR IGNORE, return new count |
| `get_pending_hospitals()` | Get pending/failed/in_progress entries |
| `mark_in_progress(name)` | Set status to `in_progress` |
| `mark_completed_duplicate(name, place_id)` | Mark as `completed` with error_message='duplicate' |
| `mark_failed(name, error)` | Set status to `failed` with error message |

### Data Persistence

| Method | Purpose |
|--------|---------|
| `is_place_crawled(place_id)` | Check if place_id exists in hospitals table |
| `save_hospital(hospital, search_name)` | Atomic: SQLite first, JSON second |
| `get_summary()` | Count by status + total_photos |
| `close()` | Clean database connection |

---

## SQLite Schema

### crawl_progress Table

```sql
CREATE TABLE IF NOT EXISTS crawl_progress (
    search_name TEXT PRIMARY KEY,
    place_id    TEXT,
    status      TEXT NOT NULL DEFAULT 'pending',
    error_message TEXT,
    created_at  TEXT NOT NULL DEFAULT (datetime('now')),
    updated_at  TEXT NOT NULL DEFAULT (datetime('now'))
);

CREATE INDEX IF NOT EXISTS idx_progress_status ON crawl_progress(status);
```

Status values: `pending`, `in_progress`, `completed`, `failed`

Duplicates use status `completed` with error_message set to `'duplicate'`.

### hospitals Table

```sql
CREATE TABLE IF NOT EXISTS hospitals (
    place_id    TEXT PRIMARY KEY,
    search_name TEXT NOT NULL,
    name        TEXT NOT NULL,
    category    TEXT,
    road_address TEXT,
    phone       TEXT,
    photo_count INTEGER NOT NULL DEFAULT 0,
    data_json   TEXT NOT NULL,
    created_at  TEXT NOT NULL DEFAULT (datetime('now'))
);

CREATE INDEX IF NOT EXISTS idx_hospitals_search ON hospitals(search_name);
```

Database uses `PRAGMA journal_mode=WAL` for concurrent read/write safety and `PRAGMA busy_timeout=5000` for lock contention.

---

## JSON Output Format

### File Naming Convention

```
{place_id}_{search_name}_{md5_hash}.json
```

- `place_id`: Naver numeric place ID (from `hospital.id`)
- `search_name`: Sanitized (non-alphanumeric chars replaced with `_`)
- `md5_hash`: First 8 chars of MD5(search_name) for uniqueness

### Output Directory Structure

```
{output_dir}/
├── naver_places.db            # SQLite database
├── session_cookies.json       # Browser session
├── hospitals/                 # JSON files
│   ├── 12345_서울병원_a1b2c3d4.json
│   └── 67890_강남의원_e5f6g7h8.json
├── photos/                    # Downloaded images
│   ├── 12345/
│   │   ├── 0000.jpg
│   │   └── 0001.jpg
│   └── 67890/
│       └── 0000.jpg
└── screenshots/               # Debug screenshots
```

---

## PhotoDownloader API (downloader.py)

### Key Methods

| Method | Purpose |
|--------|---------|
| `download_all(place_id, photo_urls)` | Async batch download with semaphore |
| `_download_one(client, url, place_dir, index)` | Single download with 3x retry |
| `update_cookies(cookies)` | Update for authenticated requests |

### Download Features

| Feature | Implementation |
|---------|---------------|
| Concurrency | asyncio.Semaphore (default: 3 concurrent) |
| Staggered Start | 0.2s delay between task launches |
| Retry | 3 attempts with exponential backoff (1s, 2s, 4s) |
| Validation | Content-Type must start with `image/` |
| Skip Existing | Skip if file exists and size > 0 bytes |
| Atomic Write | Write to temp file, then rename |
| Extension | Regex extraction from URL path, fallback to `.jpg` |

### Download Timeout

Default: 30 seconds per file (from `config.photos.download_timeout_seconds`).

---

## Resume Capability

### How Resume Works

1. **Startup**: `recover_interrupted()` resets any `in_progress` entries back to `pending`
2. **Registration**: `register_hospitals(names)` uses INSERT OR IGNORE (existing entries preserved)
3. **Pending Query**: `get_pending_hospitals()` returns `pending`, `failed`, and `in_progress` entries
4. **Duplicate Check**: `is_place_crawled(place_id)` prevents re-crawling same place
5. **Result**: Only uncrawled hospitals are processed on re-run

### Atomic Save Flow

1. INSERT OR REPLACE into `hospitals` table with `data_json`
2. UPDATE `crawl_progress` to `completed` with `place_id`
3. Commit (rollback on any error)
4. Write JSON file to disk (best-effort, DB is source of truth)

---

## Configuration Reference

From `StorageConfig` and `PhotoConfig` in `crawl/config.py`:

| Field | Default | Purpose |
|-------|---------|---------|
| storage.output_dir | "crawl/output" | Base output directory |
| storage.db_path | "crawl/output/naver_places.db" | SQLite database file |
| storage.screenshot_dir | "crawl/output/screenshots" | Screenshot directory |
| photos.max_concurrent_downloads | 3 | Concurrent download limit |
| photos.download_timeout_seconds | 30 | Per-file timeout (seconds) |
| photos.max_photos_per_place | 500 | Maximum photos per hospital |
| photos.exclude_video | True | Filter video content |

---

## Development Guidelines

When modifying storage:

1. Always use WAL mode for SQLite (concurrent read safety)
2. Maintain atomic save: SQLite transaction wraps both DB update and JSON write
3. Keep resume capability intact - never delete crawl_progress on startup
4. Photo downloads must be idempotent (skip existing files)
5. Use MD5 hash in JSON filenames to prevent collisions

Status: Production Ready
Last Updated: 2026-02-05
