---
name: moai-crawl-browser
description: >
  Playwright browser management for Naver hospital crawler covering Chromium launch
  configuration, mobile viewport randomization, session persistence via cookies,
  stealth script injection, and screenshot capture.
  Use when working with browser lifecycle, launch arguments, cookie management,
  or viewport configuration.
  Do NOT use for anti-detection scripts (use moai-crawl-stealth) or page scraping
  (use moai-crawl-scraping).
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
  tags: "crawler, naver, playwright, browser, session, cookies, viewport, chrome"

# MoAI Extension: Progressive Disclosure
progressive_disclosure:
  enabled: true
  level1_tokens: 100
  level2_tokens: 4000

# MoAI Extension: Triggers
triggers:
  keywords:
    - "playwright"
    - "browser"
    - "session"
    - "cookies"
    - "viewport"
    - "chrome launch"
    - "BrowserController"
    - "screenshot"
    - "user agent"
  agents:
    - "naver-hospital-agent"
  phases:
    - "run"
---

# Crawler Browser Management

Playwright-based Chromium browser controller with mobile emulation, session persistence, and stealth integration.

## Quick Reference

Source File: `crawl/naver_hospital/browser.py`

Key Class: `BrowserController`
- Async context manager (`async with BrowserController(config) as browser:`)
- Mobile-first Chromium with randomized viewport
- Cookie-based session persistence across runs
- Stealth script injection on every new context

---

## BrowserController API

### Lifecycle Methods

| Method | Purpose | Returns |
|--------|---------|---------|
| `launch()` | Start Chromium with stealth config | None |
| `new_page()` | Create new page with timeout | Page |
| `close()` | Save session, then cleanup: context -> browser -> playwright | None |

### Session Methods

| Method | Purpose | Returns |
|--------|---------|---------|
| `save_session()` | Atomic write cookies to JSON file | None |
| `_restore_session()` | Load cookies from disk on launch | None |
| `get_cookies_for_httpx()` | Export cookies as dict for httpx | dict |

### Utility Methods

| Method | Purpose | Returns |
|--------|---------|---------|
| `take_screenshot(page, name)` | Save full-page PNG screenshot | Path |

---

## Launch Configuration

### Chromium Arguments

```
--disable-blink-features=AutomationControlled
--disable-dev-shm-usage
--no-first-run
--no-default-browser-check
```

### Viewport Randomization

| Parameter | Range | Purpose |
|-----------|-------|---------|
| Width | 375 - 430 px | Mobile device width |
| Height | 667 - 932 px | Mobile device height |

Randomized on each launch to avoid fingerprint consistency.

### Context Options

| Option | Value | Purpose |
|--------|-------|---------|
| locale | `ko-KR` | Korean locale for Naver |
| timezone_id | `Asia/Seoul` | Korean timezone |
| is_mobile | `True` | Mobile browser emulation |
| has_touch | `True` | Touch event support |
| java_script_enabled | `True` | Enable JavaScript |
| user_agent | Random from 3 variants | iPhone Safari rotation |

### Mobile User Agents (from config.py)

Three iPhone Safari variants rotated randomly:
1. iPhone (iOS 16.6) - Safari 605.1.15
2. iPhone (iOS 17.2) - Safari 605.1.15
3. iPhone (iOS 17.4.1) - Safari 605.1.15

---

## Session Persistence

### Cookie File Format

Location: `{config.browser.session_dir}/cookies.json`

Format: JSON array of Playwright cookie objects:
```json
[
  {
    "name": "NID_AUT",
    "value": "...",
    "domain": ".naver.com",
    "path": "/",
    "expires": 1234567890,
    "httpOnly": true,
    "secure": true,
    "sameSite": "None"
  }
]
```

### Session Flow

1. On `launch()`: Load cookies from file if exists (`_restore_session()`)
2. During crawl: Browser accumulates Naver session cookies naturally
3. On `save_session()`: Atomic write all current cookies to file
4. On next run: Restored cookies skip initial authentication gates

Atomic write: Write to temp file first, then rename (prevents corruption on crash).

---

## Stealth Integration

On context creation, `get_combined_stealth_script()` from `stealth.py` is injected via:
```python
await context.add_init_script(self._stealth_script)
```

This ensures all 7 stealth scripts execute before any page navigation, including restored sessions.

---

## Configuration Reference

From `BrowserConfig` in `crawl/config.py`:

| Field | Default | Purpose |
|-------|---------|---------|
| headless | False | Headed mode for anti-detection |
| channel | "chrome" | Use native Chrome installation |
| viewport_width_min/max | 375 / 430 | Random viewport width |
| viewport_height_min/max | 667 / 932 | Random viewport height |
| timeout_ms | 30000 | Page load timeout |
| session_dir | "crawl/output/.browser_session" | Cookie persistence directory |

---

## Development Guidelines

When modifying browser management:

1. Keep headed mode (`headless=False`) as default - critical for Naver anti-detection
2. Maintain mobile viewport ranges within iPhone dimensions
3. Always inject stealth scripts before first navigation
4. Use atomic writes for session persistence (write to temp, then rename)
5. Ensure `close()` saves session first, then cleans up in order: context -> browser -> playwright

Status: Production Ready
Last Updated: 2026-02-05
