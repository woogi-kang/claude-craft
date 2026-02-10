# Storage Workflow

Save crawl results to SQLite database and export to CSV.

## Storage Script Location

```
scripts/clinic-storage/storage_manager.py
```

No external dependencies required (Python stdlib only: sqlite3, json, csv, argparse).

## Commands

### Save Result

```bash
python scripts/clinic-storage/storage_manager.py save \
  --json '{"hospital_no": 6, "name": "...", "social_channels": [...], "doctors": [...]}' \
  --db data/clinic-results/hospitals.db
```

Or pipe from file:
```bash
python scripts/clinic-storage/storage_manager.py save \
  --json-file data/clinic-results/hospital_6.json \
  --db data/clinic-results/hospitals.db
```

### Export CSV

```bash
python scripts/clinic-storage/storage_manager.py export \
  --db data/clinic-results/hospitals.db \
  --output data/clinic-results/exports/
```

Generates 3 CSV files:
- `hospitals.csv` - Hospital summary
- `social_channels.csv` - All social channels
- `doctors.csv` - All doctors with credentials

### Show Statistics

```bash
python scripts/clinic-storage/storage_manager.py stats \
  --db data/clinic-results/hospitals.db
```

## JSON Result Schema

The save command expects JSON matching this structure:

```json
{
  "hospital_no": 6,
  "name": "Hospital Name",
  "url": "https://example.com",
  "category": "custom_domain",
  "phone": "02-123-4567",
  "address": "Seoul ...",
  "status": "success",
  "social_channels": [
    {
      "platform": "KakaoTalk",
      "url": "https://pf.kakao.com/...",
      "extraction_method": "dom_static",
      "confidence": 0.95
    }
  ],
  "doctors": [
    {
      "name": "Doctor Name",
      "role": "director",
      "photo_url": "https://...",
      "education": ["edu1", "edu2"],
      "career": ["career1"],
      "credentials": ["cred1"],
      "ocr_source": false
    }
  ],
  "errors": ["error message if any"]
}
```

### Dashboard

```bash
python scripts/clinic-storage/storage_manager.py dashboard \
  --db data/clinic-results/hospitals.db \
  --target 4256
```

Shows: progress %, success rate, today's crawls, status breakdown, platform discovery rates, recent failure patterns.

### Retry Queue

```bash
python scripts/clinic-storage/storage_manager.py retry-queue \
  --db data/clinic-results/hospitals.db
```

Shows up to 50 hospitals eligible for retry, prioritized: partial > failed(transient), sorted by retry count and age.

### Incremental Export

```bash
python scripts/clinic-storage/storage_manager.py export \
  --db data/clinic-results/hospitals.db \
  --output data/clinic-results/exports/ \
  --since 2026-02-09
```

Exports only hospitals changed since the given date. Files suffixed with `_since_YYYYMMDD`.

## SQLite Schema

- `hospitals` - One row per hospital (hospital_no PK)
- `social_channels` - One row per channel (unique by hospital_no + platform + url)
- `doctors` - One row per doctor (education/career/credentials as JSON arrays)
- `crawl_errors` - Error log
- `ocr_cache` - Image hash to OCR result cache (30-day TTL)

## Schema Migrations

Migrations are applied automatically via `PRAGMA user_version` tracking.
New columns/tables are added incrementally without breaking existing data.

Current migrations:
- v1: `social_channels.verified_at` column
- v2: `doctors.ocr_confidence` column
- v3: `crawl_errors.retry_count` column
- v4: `ocr_cache` table
