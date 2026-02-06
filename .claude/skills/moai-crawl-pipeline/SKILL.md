---
name: moai-crawl-pipeline
description: >
  Pipeline orchestration for Naver hospital crawler covering CSV input parsing,
  retry logic with exponential backoff, configuration hierarchy, CLI arguments,
  environment variables, signal handling, and crawl lifecycle management.
  Use when working with crawler execution, configuration, CLI usage,
  or orchestrator logic.
  Do NOT use for individual scraper details (use moai-crawl-scraping) or
  storage internals (use moai-crawl-storage).
license: Apache-2.0
compatibility: Designed for Claude Code
allowed-tools: Read Grep Glob Bash
user-invocable: false
metadata:
  version: "1.0.0"
  category: "domain"
  status: "deprecated"
  updated: "2026-02-05"
  modularized: "true"
  tags: "crawler, naver, pipeline, orchestrator, csv, retry, config, cli"

# MoAI Extension: Progressive Disclosure
progressive_disclosure:
  enabled: true
  level1_tokens: 100
  level2_tokens: 5000

# MoAI Extension: Triggers
triggers:
  keywords:
    - "crawl pipeline"
    - "orchestrator"
    - "csv input"
    - "retry"
    - "crawler config"
    - "CrawlerConfig"
    - "HospitalCrawlOrchestrator"
    - "run crawler"
    - "signal handling"
    - "CLI"
  agents:
    - "naver-hospital-agent"
  phases:
    - "run"
---

> **DEPRECATED**: This skill references the deleted `crawl/` codebase. It has been superseded by `moai-clinic-*` skills which target the new `clinic-crawl/` codebase.

# Crawler Pipeline Orchestration

Main pipeline coordinating CSV input, scraping, downloading, and storage with retry and graceful shutdown.

## Quick Reference

Source Files:
- `crawl/naver_hospital/orchestrator.py` - HospitalCrawlOrchestrator: main pipeline
- `crawl/naver_hospital/__main__.py` - CLI entry point with argument parsing
- `crawl/config.py` - CrawlerConfig: nested configuration hierarchy

---

## Pipeline Flow

```
CSV Input -> Register -> For Each Hospital:
  mark_in_progress -> throttle -> search_place -> check_duplicate ->
  scrape_home -> scrape_information -> scrape_photos ->
  download_photos -> build_model -> save -> screenshot
```

### Detailed Steps

1. **Load CSV**: Parse first column as hospital names (UTF-8-SIG BOM support, auto-detect header)
2. **Initialize**: StorageManager setup, recover interrupted entries
3. **Register**: INSERT OR IGNORE all hospital names, get pending list
4. **Loop** (for each pending hospital):
   - `mark_in_progress(name)`
   - Retry up to `max_retries` times (default: 3)
   - `throttler.wait()` between requests
   - `search_place()` -> extract place_id
   - `is_place_crawled(place_id)` -> skip duplicates
   - `scrape_home()` -> name, category, address, phone, hours, facilities, images
   - `scrape_information()` -> description, parking, homepage, social URLs
   - `scrape_photos()` -> photo URL list
   - `download_all()` -> local file paths
   - Build `NaverHospitalPlace` model (Pydantic validation)
   - `save_hospital()` -> SQLite + JSON atomic write
   - `take_screenshot()` -> debug PNG
5. **Summary**: Rich table output with status counts

---

## HospitalCrawlOrchestrator API

### Constructor

```python
HospitalCrawlOrchestrator(config: CrawlerConfig)
```

### Key Methods

| Method | Purpose |
|--------|---------|
| `run(csv_path: str) -> dict` | Execute full pipeline (async) |
| `request_shutdown()` | Signal graceful exit (completes current hospital) |

### Internal Methods

| Method | Purpose |
|--------|---------|
| `_load_csv()` | Parse CSV, return list of hospital names |
| `_ensure_healthy_page()` | Recreate page if unresponsive |
| `_build_hospital()` | Merge scraped data into NaverHospitalPlace |
| `_print_summary()` | Rich table output with status counts |

---

## Retry Logic

### Standard Retry

```
for attempt in range(max_retries):
    try:
        # crawl operations
    except BanDetectedError:
        # special cooldown handling
    except Exception:
        delay = min(base_delay * (2 ** attempt), max_delay)
        await asyncio.sleep(delay)
```

### Ban-Specific Handling

When `BanDetectedError` is caught:
1. Mark hospital as FAILED (`mark_failed`)
2. Random cooldown: 300-600 seconds (from config.retry.cooldown_on_ban_min/max)
3. Return False immediately (no retry)

### Backoff Formula

```
delay = min(base_delay * (2 ^ attempt), max_delay)
```

Default values: base_delay=5s, max_delay=60s
- Attempt 0: 5s
- Attempt 1: 10s
- Attempt 2: 20s (capped at 60s)

---

## Configuration Hierarchy (config.py)

### CrawlerConfig (Root)

```python
class CrawlerConfig(BaseSettings):
    browser: BrowserConfig
    delays: DelayConfig
    storage: StorageConfig
    retry: RetryConfig
    photos: PhotoConfig
    delay_multiplier: float = 1.0
    max_places: Optional[int] = None
```

### Sub-Configurations

| Config | Key Fields | Defaults |
|--------|-----------|----------|
| BrowserConfig | headless, channel, viewport ranges, timeout_ms | False, "chrome", 375-430/667-932, 30000 |
| DelayConfig | page_load, action, between_places, typing_min_ms/typing_max_ms, rate_limit_seconds | 2-5s, 0.5-2s, 3-8s, 50-200ms, 3s |
| StorageConfig | output_dir, db_path, screenshot_dir | "crawl/output", "crawl/output/naver_places.db", "crawl/output/screenshots" |
| RetryConfig | max_retries, base_delay, max_delay, cooldown_on_ban_min/max | 3, 5s, 60s, 300-600s |
| PhotoConfig | max_concurrent_downloads, download_timeout_seconds, exclude_video, max_photos_per_place | 3, 30s, True, 500 |

### Validators

All range configs validate `min <= max` (e.g., viewport_width_min <= viewport_width_max).

---

## CLI Usage (__main__.py)

### Command

```bash
python -m crawl.naver_hospital <csv_file> [options]
```

### Arguments

| Argument | Type | Default | Description |
|----------|------|---------|-------------|
| csv_file | positional | required | Path to CSV with hospital names |
| --max-places | int | None | Limit number of hospitals |
| --delay-multiplier | float | 1.0 | Global delay multiplier (min: 0.1) |
| --output-dir | str | "crawl/output" | Output directory path |
| --headless | flag | False | Run in headless mode |
| --verbose | flag | False | Enable DEBUG logging |

### Signal Handling

- `SIGTERM` -> `orchestrator.request_shutdown()` via `signal.signal()`
- `SIGINT` (Ctrl+C) -> handled via `KeyboardInterrupt` try/except (exits with code 130)
- Completes current hospital before exiting
- Saves progress to SQLite (resume on next run)

### Logging

Uses Rich `RichHandler` with:
- INFO level by default
- DEBUG level with `--verbose`
- Formatted output with timestamps

---

## CSV Input Format

### Requirements

- UTF-8 or UTF-8-SIG (BOM) encoding
- First column contains hospital names
- Header row auto-detected and skipped
- Empty rows ignored

### Example

```csv
병원명
서울대학교병원
삼성서울병원
세브란스병원
```

---

## Graceful Shutdown

1. Signal received (SIGTERM via signal handler, or SIGINT via KeyboardInterrupt)
2. `request_shutdown()` sets shutdown flag (SIGTERM) or process exits with code 130 (SIGINT)
3. Current hospital crawl completes normally
4. Progress saved to SQLite
5. Summary printed
6. Clean exit

On next run, `recover_interrupted()` resets any `in_progress` entries and resumes from where it stopped.

---

## Development Guidelines

When modifying the pipeline:

1. Always maintain resume capability - never clear crawl_progress on startup
2. Keep graceful shutdown intact - complete current hospital before exit
3. Ban detection marks hospital as FAILED and returns False (with cooldown delay, but no retry)
4. CSV parsing must handle UTF-8-SIG BOM encoding (common in Korean Excel exports)
5. Use Rich for all terminal output (consistent formatting)
6. Test with `--max-places 1` for quick iteration

Status: Production Ready
Last Updated: 2026-02-05
