---
name: moai-crawl-schema
description: >
  Pydantic v2 data models for Naver hospital crawler covering BasePlace,
  NaverPlace, NaverHospitalPlace hierarchy, annotated types (KoreanPhone, TimeStr),
  enums, coordinate validation, and schema documentation references.
  Use when working with crawler data models, validation rules, or schema extensions.
  Do NOT use for scraping logic (use moai-crawl-scraping) or pipeline orchestration
  (use moai-crawl-pipeline).
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
  tags: "crawler, naver, hospital, pydantic, schema, data-model, validation"

# MoAI Extension: Progressive Disclosure
progressive_disclosure:
  enabled: true
  level1_tokens: 100
  level2_tokens: 4000

# MoAI Extension: Triggers
triggers:
  keywords:
    - "schema"
    - "pydantic"
    - "NaverPlace"
    - "NaverHospitalPlace"
    - "BasePlace"
    - "data model"
    - "hospital schema"
    - "KoreanPhone"
    - "TimeStr"
    - "CrawlMetadata"
  agents:
    - "naver-hospital-agent"
  phases:
    - "run"
---

# Crawler Data Schema

Pydantic v2 data models powering the Naver hospital crawler with strict validation and type safety.

## Quick Reference

Model Hierarchy:
- `BasePlace` (shared) -> `NaverPlace` (Naver-specific) -> `NaverHospitalPlace` (hospital extension)

Source Files:
- `crawl/base.py` - Shared base models, enums, coordinates, errors, jobs, pagination
- `crawl/naver_map_schema.py` - Naver Map place models with business hours and menu parsing
- `crawl/hospital_schema.py` - Hospital-specific fields (social URLs, parking, photos)
- `crawl/docs/` - Comprehensive schema documentation (single source of truth)

---

## Model Architecture

### BasePlace (crawl/base.py)

Shared fields across all crawl sources (Naver, Kakao):

| Field | Type | Description |
|-------|------|-------------|
| name | str | Place name |
| category | str | Business category |
| road_address | Optional[str] | Road address |
| parcel_address | Optional[str] | Old parcel address |
| phone | Optional[str] | Contact phone number |
| coordinates | Optional[Coordinates] | WGS84 lat/lng |

### NaverPlace (crawl/naver_map_schema.py)

Extends BasePlace with Naver-specific fields:

| Field | Type | Validation |
|-------|------|------------|
| id | NaverPlaceId | Numeric string pattern `^\d+$` |
| description | Optional[str] | Place description |
| homepage_url | Optional[str] | Auto-prepend https://, strip // |
| image_urls | list[str] | Auto-deduplicated |
| facilities | list[str] | Amenities list |
| business_hours | list[NaverBusinessHour] | Unique days enforced |
| review_stats | NaverReviewStats | Visitor + blog reviews (default_factory) |
| menu_info | Optional[NaverMenuInfo] | TAB (items) or TEXT (price_text) |
| crawl | CrawlMetadata | Source, URL, query, duration (default_factory) |

### NaverHospitalPlace (crawl/hospital_schema.py)

Extends NaverPlace with 6 hospital-specific fields:

| Field | Type | Validation |
|-------|------|------------|
| youtube_url | Optional[str] | youtube.com, www.youtube.com, youtu.be, m.youtube.com |
| instagram_url | Optional[str] | instagram.com, www.instagram.com |
| reservation_url | Optional[str] | booking.naver.com |
| parking_info | Optional[str] | Free text |
| local_photo_paths | list[str] | Downloaded file paths |
| photo_count | int | Auto-synced with local_photo_paths length |

---

## Annotated Types

| Type | Pattern | Usage |
|------|---------|-------|
| KoreanPhone | `^0\d{1,2}-?\d{3,4}-?\d{4}$` | Phone validation |
| TimeStr | `^([01]\d\|2[0-3]):[0-5]\d$` | Business hours |
| NaverPlaceId | `^\d+$` | Numeric place identifier |

## Support Models

| Model | Purpose | Location |
|-------|---------|----------|
| CrawlSource | Enum: NAVER, KAKAO | base.py |
| CrawlJobStatus | Enum: PENDING, RUNNING, COMPLETED, FAILED, PARTIAL | base.py |
| Coordinates | Frozen, WGS84 with Kakao conversion | base.py |
| CrawlMetadata | Source, URL, query, hash, duration | base.py |
| CrawlError | Error tracking with timestamp | base.py |
| CrawlJob | Batch tracking with progress_pct/success_rate | base.py |
| CrawlResult | Success/error wrapper with cross-field validation | base.py |
| DayOfWeek | Enum: MON-SUN + HOLIDAY, from_korean() classmethod | naver_map_schema.py |
| NaverBusinessHour | Day, open/close times, break period, is_day_off | naver_map_schema.py |
| NaverReviewStats | visitor_reviews, blog_reviews, total/has properties | naver_map_schema.py |
| NaverMenuItem | Name, price string, parsed price_value via regex | naver_map_schema.py |
| NaverMenuInfo | TAB (items list) vs TEXT (price_text) | naver_map_schema.py |

## NaverPlaceParser Utility

Static methods in `naver_map_schema.py` for parsing raw API responses:

- `_safe_get()` - Nested dict traversal
- `parse_business_hours()` - Korean day names + break time parsing
- `parse_menu_info()` - TAB/TEXT discrimination with type inference
- `parse_review_stats()` - Field name flexibility (snake_case vs camelCase)
- `parse_coordinates()` - x/y or lat/lng
- `parse()` - Full NaverPlace construction with error handling

---

## Schema Documentation

Full schema documentation lives at `crawl/docs/` (single source of truth):

- `crawl/docs/base_schema.md` - Base models reference (328 lines)
- `crawl/docs/naver_map_schema.md` - Naver models reference (500 lines)
- `crawl/docs/kakao_map_schema.md` - Kakao models reference (335 lines)

When extending schemas, always update both the Python model and corresponding docs.

---

## Development Guidelines

When modifying data models:

1. Value objects (Coordinates, CrawlMetadata, NaverBusinessHour, etc.) use `frozen=True`; entity models (BasePlace, NaverPlace, NaverHospitalPlace) are mutable
2. Add field validators for any new URL fields (see youtube_url pattern)
3. Maintain the inheritance chain: BasePlace -> NaverPlace -> NaverHospitalPlace
4. Update `crawl/docs/` when adding or changing fields
5. Run existing tests to verify backward compatibility

Status: Production Ready
Last Updated: 2026-02-05
