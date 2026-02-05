# Crawler Scraping Reference

## URL Templates

| Scraper | URL Pattern |
|---------|-------------|
| Search | `https://m.search.naver.com/search.naver?query={hospital_name}` |
| Home | `https://m.place.naver.com/hospital/{place_id}/home` |
| Information | `https://m.place.naver.com/hospital/{place_id}/information` |
| Photos | `https://m.place.naver.com/hospital/{place_id}/photo` |

All URLs target Naver's mobile site (m.place.naver.com / m.search.naver.com).

---

## Search Scraper Selectors (search.py)

### Place Link Selectors

```python
PLACE_LINK_SELECTORS = [
    'a[href*="m.place.naver.com"]',
    'a[href*="place.naver.com"]',
    'a[data-type="place"]',
]
```

### Place ID Extraction Patterns

```python
# From URL path (hospital/place/restaurant + digits)
PLACE_ID_PATTERN = re.compile(
    r"place\.naver\.com/(?:hospital|place|restaurant)/(\d+)"
)

# From embedded page content (fallback)
EMBEDDED_PATTERNS = [
    re.compile(r'"placeId"\s*:\s*"(\d{8,})"'),
    re.compile(r"place_id[\"']?\s*[:=]\s*[\"'](\d{8,})[\"']"),
    re.compile(r"placeId[\"']?\s*[:=]\s*[\"'](\d{8,})[\"']"),
]
```

---

## Home Scraper Selectors (home.py)

### Data Extraction Selectors

| Field | Primary | Fallback 1 | Fallback 2 | Fallback 3 |
|-------|---------|-----------|-----------|-----------|
| Name | `span.GHAhO` | `#_title .Fc1rA` | `h2.place_section_header` | `[class*='name']` |
| Category | `span.lnJFt` | `[class*='category']` | `.place_section_header + span` | - |
| Address | `span.LDgIH` | `[class*='addr']` | `[class*='address']` | - |
| Phone | `span.xlx7Q` | `a[href^="tel:"]` | `[class*='phone']` | - |
| Hours | `[class*='bizHour'] tr` | `[class*='operationTime'] li` | `.place_section_content table tr` | - |
| Facilities | `[class*='facility'] li` | `[class*='convenience'] span` | `.place_section_content .chip` | - |
| Images | `[class*='place_thumb'] img` | `[class*='photo'] img` | `.K0PDV img` | - |

### Business Hours Parsing Logic

```python
def _parse_hour_row(text: str) -> Optional[dict[str, Any]]:
    # 1. Extract day name via day_map dict
    day_map = {"월": "MON", "화": "TUE", "수": "WED", "목": "THU",
               "금": "FRI", "토": "SAT", "일": "SUN", "공휴일": "HOLIDAY"}
    # Also maps full forms: "월요일" -> "MON", etc.

    # 2. Check for day off
    if "휴무" in text or "정기휴무" in text or "쉽니다" in text:
        return {"day_of_week": day, "is_day_off": True}

    # 3. Extract times (HH:MM pattern)
    times = re.findall(r'(\d{2}:\d{2})', text)

    # 4. Break detection keywords
    break_keywords = ["점심", "브레이크", "휴게"]

    # 5. Build result
    if len(times) >= 2:
        result = {"day_of_week": day, "is_day_off": False,
                  "open_time": times[0], "close_time": times[1]}
    if len(times) >= 4:
        if has_break_keyword:
            result["break_start"] = times[2]
            result["break_end"] = times[3]
        else:
            # Split sessions: rearrange times
            result["close_time"] = times[3]
            result["break_start"] = times[1]
            result["break_end"] = times[2]
```

### Korean Day Name Mapping

| Korean | English | DayOfWeek |
|--------|---------|-----------|
| 월 | Monday | MON |
| 화 | Tuesday | TUE |
| 수 | Wednesday | WED |
| 목 | Thursday | THU |
| 금 | Friday | FRI |
| 토 | Saturday | SAT |
| 일 | Sunday | SUN |
| 공휴일 | Holiday | HOLIDAY |

### Image CDN Domain Filter

```python
ALLOWED_IMAGE_DOMAINS = ["pstatic.net", "naver.net", "navercorp.com"]
```

---

## Information Scraper Selectors (information.py)

### Description Extraction

```python
DESCRIPTION_SELECTORS = [
    "[class*='desc'] .place_section_content",
    "[class*='intro'] p",
    ".T8RFa",
    "[class*='description']",
]
# Minimum 10 characters required
```

### Parking Extraction

```python
# Search scoped <li> elements for Korean "주차" (parking)
elements = await page.query_selector_all(
    "[class*='info'] li, [class*='detail'] li, .place_section_content li"
)
for el in elements:
    text = (await el.inner_text()).strip()
    if "주차" in text:
        parking_info = text.replace("주차", "").strip()
```

### Homepage Extraction

```python
HOMEPAGE_SELECTORS = [
    'a[href*="http"][class*="homepage"]',
    'a[href*="http"][class*="link"]',
]

_EXCLUDED_HOMEPAGE_DOMAINS = [
    "naver.com", "naver.me",
    "instagram.com", "youtube.com", "youtu.be",
    "facebook.com", "twitter.com", "x.com",
    "tiktok.com", "kakao.com", "band.us",
    "linkedin.com",
]
```

### Social Link Detection

```python
# Scoped to content sections via selectors:
#   .place_section_content a[href]
#   [class*='info'] a[href]
#   [class*='link_section'] a[href]
def _is_youtube_url(url):    # youtube.com, youtu.be
def _is_instagram_url(url):  # instagram.com
def _is_reservation_url(url): # booking.naver.com
def _is_homepage_url(url):   # Not in _EXCLUDED_HOMEPAGE_DOMAINS
```

---

## Photo Scraper Details (photos.py)

### Photo Collection Selectors

```python
PHOTO_SELECTORS = [
    "[class*='photo'] img",
    "[class*='grid'] img",
    ".place_section_content img",
    "img[src*='pstatic.net']",
]
```

### Video Filter Patterns

```python
VIDEO_PATTERNS = [
    re.compile(r"video", re.IGNORECASE),
    re.compile(r"\.mp4", re.IGNORECASE),
    re.compile(r"\.webm", re.IGNORECASE),
    re.compile(r"play_icon", re.IGNORECASE),
]
```

### DOM-Based Video Detection

```python
VIDEO_CONTAINER_SELECTORS = [
    "[class*='video']",
    "[class*='play']",
    "[data-type='video']",
]
# Images inside these containers are excluded
```

### URL Normalization

```python
def _normalize_photo_url(url: str) -> str:
    # Remove Naver image sizing parameter
    url = re.sub(r"\?type=[^&]*$", "", url)
    # Fix protocol-relative URLs
    if url.startswith("//"):
        url = f"https:{url}"
    return url
```

---

## Field Mapping Summary

### Home Page -> NaverHospitalPlace

| Scraped Field | Model Field | Type |
|---------------|-------------|------|
| Place name | name | str |
| Category text | category | str |
| Road address | road_address | str |
| Phone number | phone | KoreanPhone |
| Business hours | business_hours | list[NaverBusinessHour] |
| Facility list | facilities | list[str] |
| Image URLs | image_urls | list[str] |

### Information Page -> NaverHospitalPlace

| Scraped Field | Model Field | Type |
|---------------|-------------|------|
| Description | description | str |
| Parking text | parking_info | str |
| Homepage link | homepage_url | str |
| YouTube link | youtube_url | str |
| Instagram link | instagram_url | str |
| Booking link | reservation_url | str |

### Photo Page -> NaverHospitalPlace

| Scraped Field | Model Field | Type |
|---------------|-------------|------|
| Photo URLs (after download) | local_photo_paths | list[str] |
| URL count | photo_count | int (auto-synced) |

---

Version: 1.0.0
Last Updated: 2026-02-05
