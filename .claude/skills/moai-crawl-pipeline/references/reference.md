# Crawler Pipeline Reference

## CLI Usage

### Basic Usage

```bash
# Run crawler with CSV input
python -m crawl.naver_hospital hospitals.csv

# With options
python -m crawl.naver_hospital hospitals.csv \
    --max-places 10 \
    --delay-multiplier 1.5 \
    --output-dir ./output \
    --verbose
```

### CLI Arguments

| Argument | Type | Required | Default | Description |
|----------|------|----------|---------|-------------|
| `csv_file` | positional | Yes | - | Path to CSV file with hospital names |
| `--max-places` | int | No | None (all) | Maximum hospitals to crawl |
| `--delay-multiplier` | float | No | 1.0 | Multiply all delays (min: 0.1) |
| `--output-dir` | str | No | "crawl/output" | Output directory path |
| `--headless` | flag | No | False | Run browser in headless mode |
| `--verbose` | flag | No | False | Enable DEBUG level logging |

---

## CSV Input Format

### Requirements

- Encoding: UTF-8 or UTF-8-SIG (BOM) - common in Korean Excel exports
- First column: hospital names
- Header row: auto-detected and skipped
- Empty rows: ignored

### Example CSV

```csv
병원명
서울대학교병원
삼성서울병원
세브란스병원
강남세브란스병원
서울아산병원
```

---

## Configuration Reference (config.py)

### CrawlerConfig (Root)

```python
class CrawlerConfig(BaseSettings):
    browser: BrowserConfig = BrowserConfig()
    delays: DelayConfig = DelayConfig()
    storage: StorageConfig = StorageConfig()
    retry: RetryConfig = RetryConfig()
    photos: PhotoConfig = PhotoConfig()
    delay_multiplier: float = 1.0
    max_places: Optional[int] = None
```

### BrowserConfig

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| headless | bool | False | Headed for anti-detection |
| channel | str | "chrome" | Native Chrome |
| viewport_width_min | int | 375 | Min mobile width |
| viewport_width_max | int | 430 | Max mobile width |
| viewport_height_min | int | 667 | Min mobile height |
| viewport_height_max | int | 932 | Max mobile height |
| timeout_ms | int | 30000 | Page load timeout |

### DelayConfig

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| page_load_min | float | 2.0 | Min page load delay |
| page_load_max | float | 5.0 | Max page load delay |
| action_min | float | 0.5 | Min action delay |
| action_max | float | 2.0 | Max action delay |
| between_places_min | float | 3.0 | Min between-hospital delay |
| between_places_max | float | 8.0 | Max between-hospital delay |
| typing_min_ms | int | 50 | Min per-character delay (ms) |
| typing_max_ms | int | 200 | Max per-character delay (ms) |
| rate_limit_seconds | float | 3.0 | Minimum request interval |

### StorageConfig

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| output_dir | Path | "crawl/output" | Base output directory |
| db_path | Path | "crawl/output/naver_places.db" | SQLite database file |
| screenshot_dir | Path | "crawl/output/screenshots" | Screenshot directory |

### RetryConfig

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| max_retries | int | 3 | Maximum retry attempts |
| base_delay | float | 5.0 | Initial backoff delay |
| max_delay | float | 60.0 | Maximum backoff delay |
| cooldown_on_ban_min | float | 300.0 | Min ban recovery wait |
| cooldown_on_ban_max | float | 600.0 | Max ban recovery wait |

### PhotoConfig

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| max_concurrent_downloads | int | 3 | Concurrent downloads |
| download_timeout_seconds | int | 30 | Per-file timeout |
| exclude_video | bool | True | Filter video content |
| max_photos_per_place | int | 500 | Max photos per hospital |
| max_scroll_attempts | int | 50 | Photo page scroll limit |

---

## Retry Backoff Formula

```python
delay = min(base_delay * (2 ** attempt), max_delay)
```

| Attempt | Delay | Capped |
|---------|-------|--------|
| 0 | 5s | 5s |
| 1 | 10s | 10s |
| 2 | 20s | 20s |
| 3+ | 40s+ | 60s |

### Ban-Specific Handling

```python
except BanDetectedError as e:
    await self._storage.mark_failed(hospital_name, f"Ban: {e}")
    cooldown = random.uniform(
        config.retry.cooldown_on_ban_min,  # 300s = 5min
        config.retry.cooldown_on_ban_max,  # 600s = 10min
    )
    await asyncio.sleep(cooldown)
    return False  # No retry, mark as FAILED
```

---

## Signal Handling (__main__.py)

```python
async def run_crawl(args):
    config = CrawlerConfig(...)
    orchestrator = HospitalCrawlOrchestrator(config)

    def handle_signal(sig, frame):
        orchestrator.request_shutdown()

    signal.signal(signal.SIGTERM, handle_signal)
    # SIGINT is NOT registered via signal.signal()

    summary = await orchestrator.run(str(args.csv_file))

def main():
    try:
        return asyncio.run(run_crawl(args))
    except KeyboardInterrupt:  # SIGINT handled here
        return 130
```

### Graceful Shutdown Sequence

1. SIGTERM: `request_shutdown()` sets `_shutdown_requested = True`, current hospital completes, then loop exits gracefully
2. SIGINT (Ctrl+C): `KeyboardInterrupt` caught in `main()`, process exits with code 130
3. On SIGTERM graceful path: current hospital completes all steps (search -> home -> info -> photos -> save)
4. Loop exits after current hospital
5. Summary table printed
6. Browser closed, database closed
7. Process exits cleanly

---

## Pipeline State Machine

```
For each hospital in pending list:

  IDLE -> IN_PROGRESS
    |
    ├── search_place() -> place_id found?
    │     NO  -> mark_failed("Place ID not found")
    │     YES -> check duplicate
    │              |
    │              ├── is_place_crawled(place_id)?
    │              │     YES -> mark_completed_duplicate()
    │              │     NO  -> continue
    │              │
    │              ├── scrape_home() -> basic data
    │              ├── scrape_information() -> contact data
    │              ├── scrape_photos() -> photo URLs
    │              ├── download_all() -> local paths
    │              ├── build NaverHospitalPlace model
    │              ├── save_hospital() -> SQLite + JSON
    │              └── take_screenshot()
    │
    └── COMPLETED / FAILED

  If BanDetectedError:
    -> mark_failed -> cooldown (300-600s) -> return False (no retry)
  If other Exception:
    -> backoff (5-60s) -> retry (up to 3x)
  If shutdown requested:
    -> complete current -> exit loop
```

---

Version: 1.0.0
Last Updated: 2026-02-05
