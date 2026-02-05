# Crawler Browser Reference

## BrowserController Class (browser.py)

### Constructor

```python
class BrowserController:
    def __init__(self, config: CrawlerConfig):
        self._config = config
        self._browser_config = config.browser
        self._playwright = None
        self._browser: Optional[Browser] = None
        self._context: Optional[BrowserContext] = None
        self._stealth_script = get_combined_stealth_script()
```

### Async Context Manager

```python
async with BrowserController(config) as browser:
    page = await browser.new_page()
    # ... use page
    await browser.save_session()
```

---

## Chromium Launch Arguments

```python
await playwright.chromium.launch(
    headless=config.browser.headless,  # Default: False
    channel=config.browser.channel,     # Default: "chrome"
    args=[
        "--disable-blink-features=AutomationControlled",
        "--disable-dev-shm-usage",
        "--no-first-run",
        "--no-default-browser-check",
    ],
)
```

---

## Context Configuration

```python
context = await browser.new_context(
    viewport={
        "width": random.randint(375, 430),
        "height": random.randint(667, 932),
    },
    user_agent=random.choice(MOBILE_USER_AGENTS),
    locale="ko-KR",
    timezone_id="Asia/Seoul",
    is_mobile=True,
    has_touch=True,
    java_script_enabled=True,
)
await context.add_init_script(self._stealth_script)
```

---

## Mobile User Agent Pool

```python
MOBILE_USER_AGENTS = [
    # iPhone (iOS 16.6)
    "Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) "
    "AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1",

    # iPhone (iOS 17.2)
    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_2 like Mac OS X) "
    "AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.2 Mobile/15E148 Safari/604.1",

    # iPhone (iOS 17.4.1)
    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_4_1 like Mac OS X) "
    "AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.4.1 Mobile/15E148 Safari/604.1",
]
```

---

## Session Cookie File Format

Location: `{session_dir}/cookies.json`

Playwright cookie format (JSON array):
```json
[
  {
    "name": "NID_AUT",
    "value": "cookie_value_here",
    "domain": ".naver.com",
    "path": "/",
    "expires": 1735689600.0,
    "httpOnly": true,
    "secure": true,
    "sameSite": "None"
  },
  {
    "name": "NID_SES",
    "value": "session_value_here",
    "domain": ".naver.com",
    "path": "/",
    "expires": -1,
    "httpOnly": true,
    "secure": true,
    "sameSite": "None"
  }
]
```

### Atomic Save Pattern

```python
async def save_session(self):
    cookies = await self._context.cookies()
    cookies_path = session_dir / "cookies.json"
    fd, tmp_path = tempfile.mkstemp(dir=session_dir, suffix=".tmp")
    with open(fd, "w", encoding="utf-8") as f:
        json.dump(cookies, f, ensure_ascii=False, indent=2)
    Path(tmp_path).replace(cookies_path)  # Atomic rename
```

---

## Screenshot API

```python
path = await browser.take_screenshot(page, "hospital_12345")
# Takes Page and name, saves full-page PNG, returns Path
```

---

## Cookie Export for httpx

```python
cookies_dict = await browser.get_cookies_for_httpx()
# Returns: {"NID_AUT": "value", "NID_SES": "value", ...}
# Used by PhotoDownloader for authenticated image downloads
```

---

## Lifecycle Sequence

1. `__aenter__()` -> `launch()`
2. `launch()`:
   - Start Playwright
   - Launch Chromium with args
   - Create context with mobile config
   - Inject stealth scripts
   - Restore session cookies (if file exists)
3. `new_page()` -> Create page with timeout
4. During operation: `save_session()` as needed
5. `__aexit__()` -> `close()`
6. `close()`:
   - Save session cookies to disk
   - Close context (releases pages)
   - Close browser (kills Chromium)
   - Stop Playwright

---

Version: 1.0.0
Last Updated: 2026-02-05
