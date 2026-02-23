# Data Guide

JSON schema reference and search patterns for the Korean dermatology dataset.

## File Inventory

| File | Size | Records | Format |
|------|------|---------|--------|
| `dermatology_procedure_details_complete.json` | 1.5MB / 31,525 lines | 679 details | `{version, updated_at, total_count, complete_count, details: [...]}` |
| `dermatology_procedures.json` | 151KB / 7,899 lines | 518 procedures | `{version, updated_at, total_count, procedures: [...]}` |
| `dermatology_category.json` | 7KB / 306 lines | 30 categories | `{version, updated_at, categories: [...]}` |
| `dermatology_tags.json` | 7KB / 104 lines | 87 tags | `{version, updated_at, tag_types: [...], tags: [...]}` |

## Procedure Details Schema (25 fields)

```
procedure_id        : int       — Unique ID, matches procedures.json id
procedure_name      : string    — Korean name (e.g., "135부스터 (NCTF 135HA)")
alias               : string[]  — Alternative names (e.g., ["샤넬주사", "필로르가 135"])
principle           : string    — How it works, explained simply
method              : string    — Step-by-step procedure description
not_recommended     : string[]  — Who should NOT get this treatment
side_effects        : {summary: string, details: [{symptom, management}]}
reverse_effects     : string    — What happens when effects wear off
pain_anesthesia     : string    — Pain level (X/5) and anesthesia info
differences         : string    — Comparison with similar treatments
golden_time         : string    — When results become visible
downtime            : string    — Recovery time
duration            : string    — How long results last
recommended_cycle   : string    — Recommended treatment frequency
combination         : string[]  — Good combination treatments
contraindications   : string[]  — Post-treatment restrictions
average_capacity    : string    — Standard dosage/amount
average_price       : string    — Price range in KRW (2025 basis)
price_reason        : string    — Why prices vary
hospital_caution    : string    — What to watch for at clinics
doctor_dependency   : int       — Doctor skill importance (1-5)
popularity_2025     : string    — Current popularity context
comment_to_friend   : string    — Casual recommendation (friend tone)
is_complete         : bool      — Whether all fields are filled
is_rich             : bool      — Whether content is detailed
```

## Procedure Index Schema (9 fields)

```
id                    : int       — Procedure ID
name                  : string    — Short Korean name
grade                 : int       — Popularity: 1=top, 2=popular, 3=standard
primary_category_id   : int       — Main category ID
secondary_category_ids: int[]     — Additional category IDs
tag_ids               : int[]     — Associated tag IDs
is_leaf               : bool      — Whether this is a leaf procedure
parent_id             : int|null  — Parent procedure ID (for variants)
is_active             : bool      — Whether currently active
```

## Category Schema

```
id            : int         — Category ID
level         : int         — 1=top-level, 2=sub-category
parent_id     : int|null    — Parent category (null for level 1)
name          : string      — Korean name
name_en       : string      — English name
description   : string      — Category description
icon          : string|null — Icon identifier
display_order : int         — Sort order
```

### Category Hierarchy

| ID | Name | English | Sub-categories |
|----|------|---------|---------------|
| 1 | 안티에이징 | Anti-aging | 101 리프팅, 102 스킨부스터, 103 주름보톡스 |
| 2 | 윤곽/볼륨 | Contouring/Volume | 201 필러, 202 지방이식, 203 윤곽보톡스 |
| 3 | 색소/미백 | Pigment/Whitening | 301 레이저토닝, 302 색소레이저, 303 미백시술 |
| 4 | 모공/흉터 | Pores/Scars | 401 MTS/더마펜, 402 프락셀, 403 모공관리 |
| 5 | 여드름/피지 | Acne/Sebum | 501 여드름치료, 502 피지관리 |
| 6 | 제모 | Hair Removal | 601 레이저제모, 602 IPL제모 |
| 7 | 필링/스케일링 | Peeling/Scaling | 701 케미컬필링, 702 물리적필링 |
| 8 | 재생/관리 | Regeneration/Care | 801 재생관리, 802 수분관리, 803 영양관리 |
| 9 | 체형/바디 | Body/Shape | 901 지방분해, 902 바디리프팅, 903 다이어트 |
| 10 | 기타 | Other | 1001 아트메이크, 1002 기타시술 |

## Tag Types

| Type | Korean | Count | ID Range |
|------|--------|-------|----------|
| concern | 고민 | 20 | 1-20 |
| effect | 효과 | 14 | 101-114 |
| body_part | 부위 | 20 | 201-220 |
| tech | 기술 | varies | 301+ |
| device | 장비 | varies | 401+ |

## Search Patterns

### Find procedure by name (Korean)
```
Grep pattern: "procedure_name": "포텐자"
File: data/dermatology/dermatology_procedure_details_complete.json
Then: Read with offset (matched line - 1) and limit 60
```

### Find procedure by ID
```
Grep pattern: "procedure_id": 42,
File: data/dermatology/dermatology_procedure_details_complete.json
Then: Read with offset (matched line - 1) and limit 60
```

### Find procedures by concern tag
```
Step 1: Look up tag_id from concern-mapping.md (e.g., wrinkle = 1)
Step 2: Grep tag ID in procedures index
  Grep pattern: "tag_ids":.*\b1\b
  File: data/dermatology/dermatology_procedures.json
Step 3: Extract matched procedure IDs
Step 4: Fetch each procedure's details by ID
```

### Find procedures by category
```
Grep pattern: "primary_category_id": 101
File: data/dermatology/dermatology_procedures.json
```

## Hospitals DB Schema (SQLite)

### hospitals table
```sql
hospital_no    INTEGER PRIMARY KEY
name           TEXT NOT NULL
url            TEXT
final_url      TEXT
category       TEXT
phone          TEXT
address        TEXT
status         TEXT DEFAULT 'pending'  -- 'done' = successfully crawled
cms_platform   TEXT
doctor_page_exists INTEGER
```

### social_channels table
```sql
hospital_no    INTEGER  -- FK to hospitals
platform       TEXT     -- kakao, naver_talk, line, etc.
url            TEXT
confidence     REAL DEFAULT 1.0
```

### doctors table
```sql
hospital_no     INTEGER  -- FK to hospitals
name            TEXT
name_english    TEXT
role            TEXT DEFAULT 'specialist'
photo_url       TEXT
education_json  TEXT DEFAULT '[]'
career_json     TEXT DEFAULT '[]'
credentials_json TEXT DEFAULT '[]'
```

### Useful queries

```sql
-- Count clinics by area
SELECT substr(address, 1, instr(address, ' ')) AS area, COUNT(*) FROM hospitals WHERE status='done' GROUP BY area;

-- Find clinics with KakaoTalk
SELECT h.name, h.address, sc.url FROM hospitals h JOIN social_channels sc ON h.hospital_no = sc.hospital_no WHERE sc.platform = 'kakao' AND h.status = 'done';

-- Clinics with doctor info
SELECT h.name, d.name, d.role, d.credentials_json FROM hospitals h JOIN doctors d ON h.hospital_no = d.hospital_no WHERE h.address LIKE '%강남%';
```
