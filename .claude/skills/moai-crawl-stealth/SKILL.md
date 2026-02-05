---
name: moai-crawl-stealth
description: >
  Anti-detection techniques for Naver hospital crawler covering stealth JavaScript
  injections, human behavior simulation, request throttling, ban detection, and
  fingerprint spoofing strategies.
  Use when working with anti-bot evasion, delay configuration, or ban recovery.
  Do NOT use for browser lifecycle management (use moai-crawl-browser) or
  page scraping logic (use moai-crawl-scraping).
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
  tags: "crawler, naver, stealth, anti-detection, fingerprint, throttle, ban, captcha"

# MoAI Extension: Progressive Disclosure
progressive_disclosure:
  enabled: true
  level1_tokens: 100
  level2_tokens: 5000

# MoAI Extension: Triggers
triggers:
  keywords:
    - "stealth"
    - "anti-detection"
    - "ban"
    - "captcha"
    - "fingerprint"
    - "throttle"
    - "human behavior"
    - "webdriver"
    - "delay"
    - "cooldown"
  agents:
    - "naver-hospital-agent"
  phases:
    - "run"
---

# Crawler Stealth & Anti-Detection

Three-layer anti-detection system: JavaScript injection, human behavior simulation, and ban detection/recovery.

## Quick Reference

Source Files:
- `crawl/naver_hospital/stealth.py` - 7 stealth JavaScript payloads
- `crawl/naver_hospital/human_behavior.py` - Human-like delays, scrolling, typing, throttling
- `crawl/naver_hospital/scrapers/detection.py` - Ban/CAPTCHA detection with URL and text indicators

---

## Layer 1: Stealth JavaScript Injections (stealth.py)

Seven scripts injected via `page.add_init_script()` before any navigation:

| Script | Function | What It Spoofs |
|--------|----------|----------------|
| `_hide_webdriver()` | Override navigator.webdriver | Returns `undefined` |
| `_mock_plugins()` | Empty PluginArray | Hides Chrome automation plugins |
| `_mock_languages()` | Set navigator.languages | `['ko-KR', 'ko', 'en-US', 'en']` |
| `_mock_permissions()` | Override Permissions.query | Returns `{state: Notification.permission}` |
| `_mock_webgl()` | Spoof WebGL parameters | Vendor: Apple Inc., Renderer: Apple GPU |
| `_add_canvas_noise()` | Canvas fingerprint noise | Subtle pixel modification (non-destructive) |
| `_hide_automation_flags()` | Remove cdc_ globals | maxTouchPoints=5, platform=iPhone, vendor=Apple |

Key API:
- `get_stealth_scripts()` - Returns list of 7 script strings
- `get_combined_stealth_script()` - Single script with per-script try-catch isolation

Each script is wrapped in its own try-catch block to prevent one failure from breaking all stealth measures.

---

## Layer 2: Human Behavior Simulation (human_behavior.py)

### Delay Functions

| Function | Range | Purpose |
|----------|-------|---------|
| `random_delay(min_s, max_s, multiplier)` | Configurable | Base delay with multiplier |
| `page_load_delay()` | 2-5s | After page navigation |
| `action_delay()` | 0.5-2s | Between UI interactions |
| `between_places_delay()` | 3-8s | Between hospital crawls |

All delays support a `delay_multiplier` config for global speed adjustment.

### Human-Like Interactions

`human_type(page, selector, text, config, clear_first)`:
- Character-by-character typing with 50-200ms inter-key delay
- Optional field clearing before typing
- Uses `page.type()` with configurable delay range

`human_scroll(page, direction, distance)`:
- Chunked scrolling (2-4 random chunks)
- Random pause between chunks (100-300ms)
- Occasional overshoot correction (scroll back slightly)

`scroll_to_bottom(page, max_scrolls, timeout_seconds)`:
- Infinite scroll detection via stable scroll height
- Stability threshold: 3 consecutive scrolls with same height
- Used by photo scraper for lazy-loaded content

### Request Throttler

```
class RequestThrottler:
    min_interval: float (default 3.0s from config.delays.rate_limit_seconds)
    async wait() -> enforces minimum interval between requests (asyncio.Lock-safe)
```

Lazy lock creation inside event loop to avoid cross-loop issues.

---

## Layer 3: Ban Detection (scrapers/detection.py)

### Detection Indicators

URL indicators (checked against current page URL):
- `captcha`, `nidlogin`, `auth.naver`, `block`, `limit`

Text indicators (checked via `page.query_selector`):
- Korean: "비정상적인 접근", "자동 접근", "로봇", "보안 문자", "자동입력방지"

HTTP status codes: `403`, `429`, `503`

### Ban Recovery Flow

1. `check_for_ban(page, response)` raises `BanDetectedError`
2. Orchestrator catches and applies cooldown: 300-600s (from `config.retry.cooldown_on_ban_*`)
3. After cooldown, marks the place as failed and returns
4. Max consecutive bans: 3 (from `config.retry.max_consecutive_bans`)

---

## Configuration Reference

All delay values from `CrawlerConfig` (crawl/config.py):

| Config Path | Default | Purpose |
|-------------|---------|---------|
| delays.page_load_min/max | 2.0 / 5.0 | Post-navigation wait |
| delays.action_min/max | 0.5 / 2.0 | UI interaction wait |
| delays.between_places_min/max | 3.0 / 8.0 | Between hospitals |
| delays.typing_min_ms/typing_max_ms | 50 / 200 | Per-character typing (ms) |
| delays.rate_limit_seconds | 3.0 | Minimum request interval |
| retry.cooldown_on_ban_min/max | 300 / 600 | Ban recovery wait (seconds) |
| retry.max_consecutive_bans | 3 | Max consecutive bans allowed |
| retry.base_delay | 5.0 | Initial retry backoff |
| retry.max_delay | 60.0 | Maximum retry backoff |
| delay_multiplier | 1.0 | Global speed multiplier |

---

## Development Guidelines

When modifying anti-detection:

1. Never remove stealth scripts without testing - each targets a specific detection vector
2. Keep all 7 scripts independent (try-catch isolated) so one failure does not affect others
3. Test delay changes against rate limiting - too fast triggers bans, too slow wastes time
4. Ban indicators are Korean text - verify with actual Naver responses
5. Always maintain mobile device fingerprint consistency (iPhone Safari)

Status: Production Ready
Last Updated: 2026-02-05
