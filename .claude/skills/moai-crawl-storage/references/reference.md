# Crawler Storage Reference

## SQLite DDL

### crawl_progress Table

```sql
CREATE TABLE IF NOT EXISTS crawl_progress (
    search_name   TEXT PRIMARY KEY,
    place_id      TEXT,
    status        TEXT NOT NULL DEFAULT 'pending',
    error_message TEXT,
    created_at    TEXT NOT NULL DEFAULT (datetime('now')),
    updated_at    TEXT NOT NULL DEFAULT (datetime('now'))
);

CREATE INDEX IF NOT EXISTS idx_progress_status ON crawl_progress(status);
```

Status flow: `pending` -> `in_progress` -> `completed` | `failed`

Duplicates use status `completed` with error_message set to `'duplicate'`.

### hospitals Table

```sql
CREATE TABLE IF NOT EXISTS hospitals (
    place_id      TEXT PRIMARY KEY,
    search_name   TEXT NOT NULL,
    name          TEXT NOT NULL,
    category      TEXT,
    road_address  TEXT,
    phone         TEXT,
    photo_count   INTEGER NOT NULL DEFAULT 0,
    data_json     TEXT NOT NULL,
    created_at    TEXT NOT NULL DEFAULT (datetime('now'))
);

CREATE INDEX IF NOT EXISTS idx_hospitals_search ON hospitals(search_name);
```

### Database Pragmas

```sql
PRAGMA journal_mode = WAL;    -- Write-Ahead Logging for concurrent access
PRAGMA busy_timeout = 5000;   -- 5s timeout for lock contention
```

---

## StorageManager Methods

### initialize()
```python
async def initialize(self):
    # Create directories (pathlib)
    self._output_dir.mkdir(parents=True, exist_ok=True)
    self._json_dir.mkdir(parents=True, exist_ok=True)   # output_dir / "hospitals"
    self._db_path.parent.mkdir(parents=True, exist_ok=True)
    # Connect and configure SQLite
    self._db = await aiosqlite.connect(str(self._db_path))
    await self._db.execute("PRAGMA journal_mode=WAL")
    await self._db.execute("PRAGMA busy_timeout=5000")
    await self._db.executescript(_CREATE_TABLES)
```

### recover_interrupted()
```python
async def recover_interrupted(self):
    await db.execute(
        "UPDATE crawl_progress SET status='pending' WHERE status='in_progress'"
    )
```

### register_hospitals(names)
```python
async def register_hospitals(self, names: list[str]) -> int:
    # INSERT OR IGNORE - preserves existing entries for resume
    for name in names:
        await db.execute(
            "INSERT OR IGNORE INTO crawl_progress (search_name) VALUES (?)",
            (name,)
        )
    return new_count
```

### save_hospital(hospital, search_name)
```python
async def save_hospital(self, hospital: NaverHospitalPlace, search_name: str) -> Path:
    # Atomic: SQLite first, then JSON
    data = hospital.model_dump(mode="json")
    try:
        # 1. Insert into hospitals
        await db.execute(
            "INSERT OR REPLACE INTO hospitals (...) VALUES (...)",
            (hospital.id, search_name, hospital.name, ..., json.dumps(data))
        )
        # 2. Update crawl_progress
        await db.execute(
            "UPDATE crawl_progress SET place_id=?, status='completed' WHERE search_name=?",
            (hospital.id, search_name)
        )
        await db.commit()
    except Exception:
        await db.rollback()
        raise
    # 3. Write JSON file (best-effort, DB is source of truth)
    json_path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
```

---

## File Naming Convention

### JSON Files
```
{place_id}_{search_name}_{hash}.json
```

Example: `12345_서울대학교병원_a1b2c3d4.json`

- `place_id`: Naver numeric ID (from `hospital.id`)
- `search_name`: Sanitized (non-alphanumeric chars replaced with `_`)
- `hash`: First 8 characters of MD5(search_name)

### Photo Files
```
photos/{place_id}/{index:04d}{ext}
```

Example: `photos/12345/0001.jpg`

- Extension guessed from URL path via regex, fallback `.jpg`
- Index is zero-padded to 4 digits

---

## Output Directory Structure

```
{output_dir}/
├── naver_places.db                # SQLite: progress + hospital data
├── session_cookies.json           # Browser session persistence
├── hospitals/                     # Individual hospital JSON files
│   ├── 12345_서울병원_a1b2c3d4.json
│   ├── 67890_강남의원_e5f6g7h8.json
│   └── ...
├── photos/                        # Downloaded photos by place_id
│   ├── 12345/
│   │   ├── 0000.jpg
│   │   ├── 0001.jpg
│   │   └── 0002.png
│   └── 67890/
│       ├── 0000.jpg
│       └── 0001.jpg
└── screenshots/                   # Debug screenshots
    ├── hospital_12345.png
    └── hospital_67890.png
```

---

## PhotoDownloader Details

### Download Flow per Photo

```
1. Check if file exists (size > 0) -> skip
2. Create temp file: 0001.jpg.tmp
3. httpx.AsyncClient.get(url, timeout=30s)
4. Validate Content-Type starts with "image/"
5. Write response content to temp file
6. Rename temp -> final (atomic)
```

### Retry with Backoff

```python
# Retry logic inside _download_one(self, client, url, place_dir, index):
for attempt in range(3):
    try:
        response = await client.get(url)
        response.raise_for_status()
        # write temp, rename to final
        return str(filepath)
    except (httpx.TransportError, httpx.HTTPStatusError, ValueError):
        tmp_path.unlink(missing_ok=True)
        if attempt < 2:
            await asyncio.sleep(1 * (2 ** attempt))  # 1s, 2s, 4s
```

### Concurrent Download Control

```python
semaphore = asyncio.Semaphore(config.photos.max_concurrent_downloads)  # Default: 3

async def _download_one(self, client, url, place_dir, index):
    async with self._get_semaphore():
        # Only N concurrent downloads at a time
        ...
```

### Staggered Launch

```python
tasks = []
for idx, url in enumerate(photo_urls):
    if idx > 0:
        await asyncio.sleep(0.2)  # 200ms between task launches
    tasks.append(
        asyncio.create_task(self._download_one(client, url, place_dir, idx))
    )
results = await asyncio.gather(*tasks, return_exceptions=True)
```

### Extension Detection

```python
def _guess_extension(url: str) -> str:  # module-level function
    path = urlparse(url).path
    match = re.search(r"\.(jpe?g|png|webp|gif|bmp)$", path, re.IGNORECASE)
    if match:
        ext = match.group(1).lower()
        return f".{ext}" if ext != "jpeg" else ".jpg"
    return ".jpg"
```

---

Version: 1.0.0
Last Updated: 2026-02-05
