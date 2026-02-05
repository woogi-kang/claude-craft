# Crawler Schema Reference

## Documentation Pointers

Full schema documentation is maintained as single source of truth in:

- `crawl/docs/base_schema.md` - Base models, enums, coordinates, metadata (328 lines)
- `crawl/docs/naver_map_schema.md` - Naver-specific models, business hours, menus (500 lines)
- `crawl/docs/kakao_map_schema.md` - Kakao models reference (335 lines)

Always refer to these docs for complete field definitions. This reference provides quick-access patterns only.

---

## Source File Map

| File | Models | Lines |
|------|--------|-------|
| `crawl/base.py` | BasePlace, Coordinates, CrawlMetadata, CrawlError, CrawlJob, CrawlResult, PaginatedResponse | ~287 |
| `crawl/naver_map_schema.py` | NaverPlace, NaverBusinessHour, NaverReviewStats, NaverMenuItem, NaverMenuInfo, NaverPlaceParser | ~502 |
| `crawl/hospital_schema.py` | NaverHospitalPlace | ~105 |

---

## Inheritance Chain

```
BasePlace (crawl/base.py)
├── name: str
├── category: str
├── road_address: Optional[str]
├── parcel_address: Optional[str]
├── phone: Optional[str]
└── coordinates: Optional[Coordinates]
    │
    ▼
NaverPlace (crawl/naver_map_schema.py)
├── id: NaverPlaceId (^\d+$)
├── description: Optional[str]
├── homepage_url: Optional[str]
├── image_urls: list[str]
├── facilities: list[str]
├── business_hours: list[NaverBusinessHour]
├── review_stats: NaverReviewStats
├── menu_info: Optional[NaverMenuInfo]
└── crawl: CrawlMetadata
    │
    ▼
NaverHospitalPlace (crawl/hospital_schema.py)
├── youtube_url: Optional[str]
├── instagram_url: Optional[str]
├── reservation_url: Optional[str]
├── parking_info: Optional[str]
├── local_photo_paths: list[str]
└── photo_count: int
```

---

## Key Validators

### NaverPlace Validators

| Validator | Field | Behavior |
|-----------|-------|----------|
| `validate_unique_days` | business_hours | Reject duplicate day_of_week entries |
| `deduplicate_images` | image_urls | Remove duplicate URLs |
| `validate_homepage` | homepage_url | Auto-prepend https://, strip //, validate scheme |

### NaverHospitalPlace Validators

| Validator | Field | Behavior |
|-----------|-------|----------|
| youtube_url | URL | Must match youtube.com, www.youtube.com, youtu.be, or m.youtube.com |
| instagram_url | URL | Must match instagram.com or www.instagram.com |
| reservation_url | URL | Must start with https://booking.naver.com |
| `sync_photo_count` | photo_count | Post-validator: auto-sync with len(local_photo_paths) |

### Annotated Type Patterns

```python
KoreanPhone = Annotated[str, Field(pattern=r"^0\d{1,2}-?\d{3,4}-?\d{4}$")]
TimeStr = Annotated[str, Field(pattern=r"^([01]\d|2[0-3]):[0-5]\d$")]
NaverPlaceId = Annotated[str, Field(pattern=r"^\d+$")]
```

---

## Enum Reference

### CrawlSource (base.py)
- `NAVER` - Naver Map source
- `KAKAO` - Kakao Map source

### CrawlJobStatus (base.py)
- `PENDING` - Not yet started
- `RUNNING` - In progress
- `COMPLETED` - Finished successfully
- `FAILED` - Finished with error
- `PARTIAL` - Partially completed

### DayOfWeek (naver_map_schema.py)
- `MON`, `TUE`, `WED`, `THU`, `FRI`, `SAT`, `SUN`, `HOLIDAY`
- `from_korean()` classmethod maps Korean day names

### NaverMenuType (naver_map_schema.py)
- `TAB` - Menu items with individual prices
- `TEXT` - Single price text block

---

## NaverPlaceParser Methods

| Method | Input | Output | Notes |
|--------|-------|--------|-------|
| `_safe_get(data, *keys)` | Nested dict + key path | Any or None | Safe nested access |
| `parse_business_hours(raw)` | List of raw dicts | list[NaverBusinessHour] | Korean day name mapping |
| `parse_menu_info(raw)` | Raw menu data | NaverMenuInfo or None | TAB/TEXT discrimination |
| `parse_review_stats(raw)` | Raw stats data | NaverReviewStats | snake_case + camelCase |
| `parse_coordinates(raw)` | Raw coord data | Coordinates or None | x/y or lat/lng format |
| `parse(raw_data)` | Complete raw dict | NaverPlace | Full construction |

---

Version: 1.0.0
Last Updated: 2026-02-05
