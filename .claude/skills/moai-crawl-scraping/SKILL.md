---
name: moai-crawl-scraping
description: >
  Four page-specific scrapers for Naver hospital crawler covering search
  (place ID extraction), home (basic info), information (social/contact),
  and photos (infinite scroll collection with video filtering).
  Use when working with CSS selectors, URL patterns, extraction logic,
  or page navigation for specific Naver pages.
  Do NOT use for anti-detection (use moai-crawl-stealth) or data models
  (use moai-crawl-schema).
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
  tags: "crawler, naver, scraper, selector, search, photos, business-hours, place-id"

# MoAI Extension: Progressive Disclosure
progressive_disclosure:
  enabled: true
  level1_tokens: 100
  level2_tokens: 6000

# MoAI Extension: Triggers
triggers:
  keywords:
    - "scraper"
    - "selector"
    - "naver page"
    - "place ID"
    - "business hours"
    - "photos"
    - "search page"
    - "information page"
    - "home page"
    - "infinite scroll"
    - "CSS selector"
  agents:
    - "naver-hospital-agent"
  phases:
    - "run"
---

> **DEPRECATED**: This skill references the deleted `crawl/` codebase. It has been superseded by `moai-clinic-*` skills which target the new `clinic-crawl/` codebase.

# Crawler Page Scrapers

Four specialized scrapers for Naver's mobile pages: search, home, information, and photos.

## Quick Reference

Source Files:
- `crawl/naver_hospital/scrapers/search.py` - Search result -> place ID extraction
- `crawl/naver_hospital/scrapers/home.py` - Basic hospital info (name, address, hours)
- `crawl/naver_hospital/scrapers/information.py` - Contact, social media, reservation URLs
- `crawl/naver_hospital/scrapers/photos.py` - Photo collection with infinite scroll

Shared:
- `crawl/naver_hospital/scrapers/detection.py` - Ban detection (used by all scrapers)

---

## Scraper 1: Search (search.py)

**Purpose**: Find Naver place ID from hospital name.

### URL Pattern

```
https://m.search.naver.com/search.naver?query={hospital_name}
```

### Extraction Strategy

Three-tier place ID extraction:

1. **Link selectors** - CSS selectors for place links in search results:
   - `a[href*="m.place.naver.com"]`
   - `a[href*="place.naver.com"]`
   - `a[data-type="place"]`

2. **URL regex** - Extract place ID from href:
   ```
   PLACE_ID_PATTERN = r"place\.naver\.com/(?:hospital|place|restaurant)/(\d+)"
   ```

3. **Embedded JSON** - Fallback: search page content for embedded data:
   - Pattern 1: `r'"placeId"\s*:\s*"(\d{8,})"'`
   - Pattern 2: `r"place_id[\"']?\s*[:=]\s*[\"'](\d{8,})[\"']"`
   - Pattern 3: `r"placeId[\"']?\s*[:=]\s*[\"'](\d{8,})[\"']"`

### Flow

```
navigate(SEARCH_URL) -> check_for_ban -> find_in_viewport -> scroll_and_retry -> extract_from_content
```

---

## Scraper 2: Home (home.py)

**Purpose**: Extract basic hospital data from place home page.

### URL Pattern

```
https://m.place.naver.com/hospital/{place_id}/home
```

### Selector Table

| Data | Primary Selector | Fallback Selectors |
|------|-----------------|-------------------|
| Name | `span.GHAhO` | `#_title .Fc1rA`, `h2.place_section_header`, `[class*='name']` |
| Category | `span.lnJFt` | `[class*='category']`, `.place_section_header + span` |
| Address | `span.LDgIH` | `[class*='addr']`, `[class*='address']` |
| Phone | `span.xlx7Q` | `a[href^="tel:"]`, `[class*='phone']` |
| Hours | `[class*='bizHour'] tr` | `[class*='operationTime'] li`, `.place_section_content table tr` |
| Facilities | `[class*='facility'] li` | `[class*='convenience'] span`, `.place_section_content .chip` |
| Images | `[class*='place_thumb'] img` | `[class*='photo'] img`, `.K0PDV img` + CDN domain filter |

### Business Hours Parsing

`_parse_hour_row()` logic:
1. Extract Korean day name via `day_map` dict (월->MON, 화->TUE, ... 공휴일->HOLIDAY)
2. Check for day off: "휴무", "정기휴무", or "쉽니다"
3. Extract HH:MM times via regex
4. Detect break periods via keywords: "점심", "브레이크", "휴게"
5. 4 time values with break keyword = open/close + break_start/break_end; without keyword = split sessions

### Image URL Filtering

Only allow CDN domains: `pstatic.net`, `naver.net`, `navercorp.com`

---

## Scraper 3: Information (information.py)

**Purpose**: Extract detailed contact and social media information.

### URL Pattern

```
https://m.place.naver.com/hospital/{place_id}/information
```

### Extraction Fields

| Field | Extraction Method | Validation |
|-------|-------------------|------------|
| Description | `[class*='desc'] .place_section_content`, `[class*='intro'] p`, `.T8RFa`, `[class*='description']` | Min 10 chars |
| Parking | Search `li` elements for "주차" | Clean prefix text |
| Homepage | `a[href*="http"][class*="homepage"]`, `a[href*="http"][class*="link"]` | Exclude social/Naver domains |
| YouTube URL | Link matching `youtube.com`, `youtu.be` | URL validation |
| Instagram URL | Link matching `instagram.com` | URL validation |
| Reservation URL | Link matching `booking.naver.com` | URL validation |

### Homepage Domain Exclusions

These domains are filtered out of homepage extraction:
- naver.com, naver.me, instagram.com, youtube.com, youtu.be
- facebook.com, twitter.com, x.com, tiktok.com
- kakao.com, band.us, linkedin.com

---

## Scraper 4: Photos (photos.py)

**Purpose**: Collect photo URLs with infinite scroll and video filtering.

### URL Pattern

```
https://m.place.naver.com/hospital/{place_id}/photo
```

### Collection Strategy

1. Navigate to photo page
2. `scroll_to_bottom()` - Infinite scroll until height stabilizes (3 consecutive stable scrolls)
3. Wait 2s for lazy-loaded images
4. Collect URLs from multiple selectors
5. Filter by CDN domain (pstatic.net, naver.net, navercorp.com)
6. Filter out video content
7. Normalize URLs (remove `?type=xxx` sizing params)
8. Deduplicate and cap at `max_photos_per_place` (default: 500)

### Video Filtering

Two-pass video detection:

1. **URL-based**: Regex patterns for video indicators:
   - `video`, `.mp4`, `.webm`, `play_icon`

2. **DOM-based**: Check parent containers:
   - `[class*='video']`, `[class*='play']`, `[data-type='video']`
   - Remove URLs found inside these containers

### URL Normalization

```python
# Remove Naver image sizing parameters
url = re.sub(r"\?type=[^&]*$", "", url)
# Add https to protocol-relative URLs
if url.startswith("//"):
    url = f"https:{url}"
```

---

## Shared: Ban Detection (detection.py)

All scrapers call `check_for_ban(page, response)` after navigation:

| Check | Indicators |
|-------|-----------|
| HTTP Status | 403, 429, 503 |
| URL Keywords | captcha, nidlogin, auth.naver, block, limit |
| Page Text | 비정상적인 접근, 자동 접근, 로봇, 보안 문자, 자동입력방지 |

Raises `BanDetectedError` which triggers cooldown in orchestrator.

`validate_place_id(place_id)`: Ensures numeric string before URL construction.

---

## Development Guidelines

When modifying scrapers:

1. Naver frequently changes CSS class names - always use multiple fallback selectors
2. Test with real Naver pages (class names like `GHAhO`, `LDgIH` are Naver-generated)
3. All scrapers must call `check_for_ban()` after navigation
4. Use `validate_place_id()` before constructing any Naver URL
5. Photo scraper must filter both by CDN domain AND video content
6. Keep URL normalization consistent across all scrapers

Status: Production Ready
Last Updated: 2026-02-05
