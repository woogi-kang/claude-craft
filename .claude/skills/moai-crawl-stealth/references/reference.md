# Crawler Stealth Reference

## Stealth Script Details (stealth.py)

### Script 1: _hide_webdriver()
```javascript
Object.defineProperty(navigator, 'webdriver', {
  get: () => undefined
});
```
Target: `navigator.webdriver` detection (standard Selenium/Playwright check).

### Script 2: _mock_plugins()
```javascript
Object.defineProperty(navigator, 'plugins', {
  get: () => []
});
Object.defineProperty(navigator, 'mimeTypes', {
  get: () => []
});
```
Target: Empty plugin array indicates automated browser.

### Script 3: _mock_languages()
```javascript
Object.defineProperty(navigator, 'languages', {
  get: () => ['ko-KR', 'ko', 'en-US', 'en']
});
```
Target: Korean locale consistency with mobile emulation.

### Script 4: _mock_permissions()
```javascript
const originalQuery = window.navigator.permissions.query;
window.navigator.permissions.query = (parameters) =>
  parameters.name === 'notifications'
    ? Promise.resolve({ state: Notification.permission })
    : originalQuery(parameters);
```
Target: Permissions API fingerprinting.

### Script 5: _mock_webgl()
```javascript
const getParameter = WebGLRenderingContext.prototype.getParameter;
WebGLRenderingContext.prototype.getParameter = function(parameter) {
  if (parameter === 37445) return 'Apple Inc.';      // UNMASKED_VENDOR
  if (parameter === 37446) return 'Apple GPU';        // UNMASKED_RENDERER
  return getParameter.call(this, parameter);
};
```
Target: WebGL vendor/renderer fingerprinting. Returns Apple GPU to match iPhone emulation.

### Script 6: _add_canvas_noise()
Injects subtle random noise into canvas `toDataURL()` and `toBlob()` without affecting visual rendering. Each call produces slightly different fingerprint.

### Script 7: _hide_automation_flags()
```javascript
// Remove specific Chromium DevTools Protocol artifacts
delete window.cdc_adoQpoasnfa76pfcZLmcfl_Array;
delete window.cdc_adoQpoasnfa76pfcZLmcfl_Promise;
delete window.cdc_adoQpoasnfa76pfcZLmcfl_Symbol;
Object.defineProperty(navigator, 'maxTouchPoints', { get: () => 5 });
Object.defineProperty(navigator, 'platform', { get: () => 'iPhone' });
Object.defineProperty(navigator, 'vendor', { get: () => 'Apple Computer, Inc.' });
```
Target: Chrome DevTools Protocol artifacts + device consistency.

---

## Delay Configuration Table

| Delay Type | Config Path | Min | Max | Unit |
|-----------|-------------|-----|-----|------|
| Page Load | delays.page_load_min/max | 2.0 | 5.0 | seconds |
| Action | delays.action_min/max | 0.5 | 2.0 | seconds |
| Between Places | delays.between_places_min/max | 3.0 | 8.0 | seconds |
| Typing | delays.typing_min_ms/typing_max_ms | 50 | 200 | ms |
| Rate Limit | delays.rate_limit_seconds | 3.0 | - | seconds |
| Ban Cooldown | retry.cooldown_on_ban_min/max | 300 | 600 | seconds |
| Retry Base | retry.base_delay | 5.0 | - | seconds |
| Retry Max | retry.max_delay | 60.0 | - | seconds |

Global multiplier: `delay_multiplier` (default: 1.0) applies to all random delays.

---

## Human Behavior Functions

### random_delay(min_s, max_s, multiplier=1.0)
```python
actual_delay = random.uniform(min_s, max_s) * multiplier
await asyncio.sleep(actual_delay)
```

### human_type(page, selector, text, config, clear_first=True)
- Optionally clears field first (Cmd/Ctrl+A + Backspace)
- Types character by character
- Inter-key delay: random.randint(typing_min_ms, typing_max_ms) milliseconds

### human_scroll(page, direction="down", distance=None)
- Default distance: random.randint(300, 800) when None
- Splits distance into 2-4 random chunks
- Each chunk: `page.mouse.wheel(0, chunk_distance)`
- Random pause between chunks: 100-300ms
- 30% chance of slight overshoot correction (scroll back 20-80px)

### scroll_to_bottom(page, max_scrolls=50, timeout_seconds=120.0)
- Scrolls repeatedly until page height stabilizes
- Stability = 3 consecutive scrolls with identical scrollHeight
- Returns early if timeout exceeded

### RequestThrottler
```python
class RequestThrottler:
    def __init__(self, min_interval: float):
        self._min_interval = min_interval
        self._last_request_time = 0.0
        self._lock: Optional[asyncio.Lock] = None

    async def wait(self):
        # Creates lock lazily inside event loop
        elapsed = time.monotonic() - self._last_request_time
        if elapsed < self._min_interval:
            await asyncio.sleep(self._min_interval - elapsed)
        self._last_request_time = time.monotonic()
```

---

## Ban Detection Indicators

### URL Indicators
```python
BAN_URL_INDICATORS = ["captcha", "nidlogin", "auth.naver", "block", "limit"]
```

### Text Indicators (Korean)
```python
BAN_TEXT_INDICATORS = [
    "비정상적인 접근",    # Abnormal access
    "자동 접근",          # Automated access
    "로봇",              # Robot
    "보안 문자",          # Security characters (CAPTCHA)
    "자동입력방지",       # Auto-input prevention
]
```

### HTTP Status Detection
- `403` Forbidden
- `429` Too Many Requests
- `503` Service Unavailable

---

Version: 1.0.0
Last Updated: 2026-02-05
