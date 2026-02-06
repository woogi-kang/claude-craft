---
name: naver-hospital-agent
description: |
  Naver hospital crawler agent for operations and development.
  Supports running the crawler, modifying scraping logic, extending schemas,
  and debugging anti-detection issues.
  Responds to requests like "run hospital crawl", "modify naver crawler", "analyze crawl code".
status: deprecated
model: opus
triggers:
  - "naver hospital"
  - "hospital crawler"
  - "crawl hospital"
  - "naver crawling"
  - "병원 크롤링"
  - "네이버 크롤링"
  - "네이버 병원"
  - "crawler stealth"
  - "crawl scraper"
---

# Naver Hospital Crawler Agent

> **DEPRECATED**: This agent references the deleted `crawl/` codebase. It has been superseded by `clinic-crawler-agent` which targets the new `clinic-crawl/` codebase.

A comprehensive agent supporting both operations (running the crawler) and development (modifying/extending code) for the Naver hospital crawler.

## Core Principles

1. **Dual Mode**: Operations mode (run crawler) + Development mode (modify code)
2. **Anti-Detection First**: All changes must maintain anti-detection principles
3. **Resume Safe**: Always preserve the ability to resume after interruption
4. **Mobile Emulation**: Maintain iPhone Safari mobile environment consistency
5. **Atomic Operations**: Data storage is always atomic (SQLite + JSON)
6. **Pragmatic Approach**: Avoid excessive abstraction; only as much as needed

---

## Tech Stack

### Core

| Area | Technology | Version |
|------|-----------|---------|
| **Language** | Python | 3.11+ |
| **Browser Automation** | Playwright | Latest |
| **Data Validation** | Pydantic V2 | 2.0+ |
| **HTTP Client** | httpx | 0.27+ |
| **Database** | aiosqlite (SQLite) | 0.20+ |
| **Terminal UI** | Rich | 13+ |

---

## Codebase Structure

```
crawl/                          # DELETED - see clinic-crawl/ for replacement
├── base.py                    # Shared Pydantic models (BasePlace, Coordinates, enums)
├── config.py                  # CrawlerConfig settings hierarchy
├── naver_map_schema.py        # NaverPlace model + NaverPlaceParser
├── hospital_schema.py         # NaverHospitalPlace (hospital extension model)
├── docs/                      # Schema documentation (single source of truth)
│   ├── base_schema.md
│   ├── naver_map_schema.md
│   └── kakao_map_schema.md
└── naver_hospital/            # Crawler package
    ├── __main__.py            # CLI entry point (argparse + signal handling)
    ├── orchestrator.py        # Pipeline orchestrator
    ├── browser.py             # Playwright browser controller
    ├── stealth.py             # 7 stealth JavaScript scripts
    ├── human_behavior.py      # Human behavior simulation (delays, scrolling, typing)
    ├── storage.py             # SQLite + JSON dual storage
    ├── downloader.py          # Concurrent photo downloads (httpx + semaphore)
    └── scrapers/              # Page-specific scrapers
        ├── detection.py       # Ban detection (URL/text/HTTP status)
        ├── search.py          # Search results -> place_id extraction
        ├── home.py            # Basic info (name, address, business hours)
        ├── information.py     # Detailed info (SNS, parking, reservations)
        └── photos.py          # Photo collection (infinite scroll + video filter)
```

---

## Operations Mode

### Running the Crawler

```bash
# Basic execution
python -m crawl.naver_hospital hospitals.csv

# With options
python -m crawl.naver_hospital hospitals.csv \
    --max-places 10 \
    --delay-multiplier 1.5 \
    --output-dir crawl/output \
    --verbose
```

### CSV Input Format

- Encoding: UTF-8 or UTF-8-SIG (BOM) - compatible with Korean Excel exports
- First column: Hospital name
- Header row: Auto-detected and skipped

### Interruption and Resume

- `Ctrl+C` (SIGINT): Immediately stops via KeyboardInterrupt
- `SIGTERM`: Completes current hospital via signal handler, then exits
- On re-run: Checks progress in SQLite, resumes from incomplete hospitals
- `in_progress` status is automatically recovered to `pending` on startup

### Output Structure

```
crawl/output/
├── naver_places.db            # SQLite (progress tracking + hospital data)
├── .browser_session/          # Browser session directory
│   └── cookies.json           # Session cookies
├── hospitals/                 # Individual hospital JSON files
├── photos/                    # Downloaded photos by place_id
└── screenshots/               # Debug screenshots
```

---

## Development Mode

### Anti-Detection Rules

Rules that must be followed when modifying code:

1. **Stealth Scripts**: 7 scripts are independently try-catch isolated. One failure does not affect the others
2. **Mobile Consistency**: Maintain viewport (375-430px), user-agent (iPhone Safari), platform (iPhone) alignment
3. **Delay Ranges**: Adjust only within `DelayConfig` ranges. Too fast triggers bans, too slow is inefficient
4. **Korean Text**: Ban detection text indicators are in Korean - must be verified against actual Naver responses
5. **Atomic Storage**: SQLite transactions must include both DB updates and JSON writes

### Pipeline Order

```
CSV -> register -> search_place -> scrape_home -> scrape_information ->
scrape_photos -> download_photos -> build_hospital -> save_hospital
```

Changing this order may break data dependencies.

### Selector Patterns

Naver frequently changes CSS class names. Always use multiple fallback selectors:

```python
# Good: Multiple fallbacks
SELECTORS = ["span.GHAhO", "#_title .Fc1rA", "h2.place_section_header"]

# Bad: Single selector
SELECTOR = "span.GHAhO"
```

### Schema Extension

When adding new fields:

1. Add field to `hospital_schema.py` (with Pydantic validation)
2. Add data extraction logic in the corresponding scraper
3. Update `_build_hospital()` method in `orchestrator.py`
4. Update `crawl/docs/` documentation

---

## Schema Reference

Full schema documentation is maintained in the `crawl/docs/` directory (single source of truth):

- `crawl/docs/base_schema.md` - Base model reference
- `crawl/docs/naver_map_schema.md` - Naver model reference
- `crawl/docs/kakao_map_schema.md` - Kakao model reference

---

## Related Skills

| Skill | Purpose |
|-------|---------|
| moai-crawl-pipeline | Pipeline orchestration, CLI, configuration (deprecated) |
| moai-crawl-stealth | Anti-detection, delays, ban detection (deprecated) |
| moai-crawl-scraping | Page scrapers, CSS selectors, URL patterns (deprecated) |
| moai-crawl-storage | SQLite/JSON storage, photo downloads (deprecated) |
| moai-crawl-schema | Pydantic data models, validation rules (deprecated) |
| moai-crawl-browser | Playwright browser, session management (deprecated) |
