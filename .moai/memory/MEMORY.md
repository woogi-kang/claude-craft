# MoAI Memory

## Clinic Crawler Agent

### Parallel Browser Isolation (2026-02-10)
- Playwright MCP shares ONE browser across all agents - parallel agents cause page conflicts
- Solution: `crawl_single.py` + `crawl_batch.py` using Python `playwright` library (each process gets its own Chromium)
- `asyncio.Semaphore` controls concurrency; `crawl_hospital()` is a standalone async function
- SQLite WAL mode allows concurrent writes from parallel workers

### DB Schema Drift Fix
- Existing DB was created with older schema missing columns: `final_url`, `cms_platform`, `schema_version`, `status` (social_channels), `step`/`retryable` (crawl_errors), `branch`/`branches_json`/`extraction_source` (doctors)
- Added migrations v5-v13 to `storage_manager.py` MIGRATIONS dict
- Always check actual DB columns with `PRAGMA table_info()` before assuming SCHEMA_SQL matches

### Phone URL Validation
- `tel:02-1234-5678` needs prefix stripping before regex validation
- Use `str.removeprefix("tel:")` (Python 3.9+)
- Korean phone regex must include `.` as separator: `[-\s.]?`

### CSV Column Names (skin_clinics.csv)
- Hospital name: `병원/약국명` or `naver_name`
- URL: `naver_website` (preferred, `홈페이지` often empty)
- Address: `소재지주소` or `naver_address`
- Hospital number: `NO`
- Encoding: `utf-8-sig` (BOM character in header)

### Python 3.9 Compatibility
- No `str | None` syntax - use `Optional[str]` from `typing`
- No `list[dict]` - use plain `list`
- `str.removeprefix()` works on 3.9+

### robots.txt False Positives
- Naver Blog/Cafe URLs (`blog.naver.com`, `cafe.naver.com`) block all crawling via robots.txt
- These aren't real clinic websites - they're social platform URLs used as homepage
- Consider classifying these as "social_only" rather than "robots_blocked"
