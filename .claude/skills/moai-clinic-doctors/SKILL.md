---
name: moai-clinic-doctors
description: >
  Doctor and medical staff information extraction patterns for Korean skin
  clinic websites. Covers menu navigation (의료진/원장/전문의 labels),
  data extraction selectors, credential parsing, photo URL extraction,
  and role classification. Use when extracting doctor information from
  clinic websites.
license: Apache-2.0
compatibility: Designed for Claude Code
allowed-tools: Read Grep Glob Bash
user-invocable: false
metadata:
  version: "1.0.0"
  category: "domain"
  status: "active"
  updated: "2026-02-06"
  modularized: "false"
  tags: "clinic, doctor, medical-staff, credentials, photo, 의료진, 원장"

# MoAI Extension: Progressive Disclosure
progressive_disclosure:
  enabled: true
  level1_tokens: 100
  level2_tokens: 4000

# MoAI Extension: Triggers
triggers:
  keywords:
    - "doctor"
    - "medical staff"
    - "의료진"
    - "원장"
    - "전문의"
    - "credentials"
    - "doctor photo"
  agents:
    - "clinic-crawler-agent"
  phases:
    - "run"
---

# Doctor Information Extraction

## Step 1: Find Doctor Page

### Menu Label Patterns (Priority Order)

Primary (exact match):
- 의료진, 의료진 소개, 의료진소개
- 원장 소개, 원장소개
- 전문의 소개, 전문의소개
- DOCTOR, Doctor, Medical Staff

Secondary (fuzzy match):
- 원장님, 대표원장, 의료팀
- 진료진, Staff, Team
- About Us, 클리닉 소개

Submenu parents (check children):
- 병원 소개, 소개, About, 클리닉 안내

### URL Patterns in href
- /doctor, /doctors, /staff, /team
- /about, /introduce
- /sub/doctor, /page/doctor

## Step 2: Navigate to Doctor Page

1. Take browser snapshot to find navigation menu
2. Look for menu items matching label patterns above
3. Click the matching menu item
4. Wait for page load (snapshot again)
5. If not found in main nav, check submenu/dropdown menus

## Step 3: Extract Doctor Data

### Target Fields

| Field | Source | Notes |
|-------|--------|-------|
| name | heading, strong, .name class | 2-20 char Korean name |
| role | surrounding text | 원장/전문의/간호사 |
| photo | img src/data-src | Resolve relative URLs |
| credentials | list items | 전문의 certifications |
| education | list items | 대학/대학원/졸업 keywords |
| career | list items | 병원/클리닉/수련 keywords |

### Common HTML Structures

Pattern A - Card layout:
```
.doctor-card > img + .info > h3.name + ul.career
```

Pattern B - Table layout:
```
table > tr > td > img + td > dl > dt (name) + dd (credentials)
```

Pattern C - Section layout:
```
.doctor-section > .photo > img + .detail > .name + .career-list
```

### Credential Parsing

Korean medical credentials follow patterns:
- "피부과 전문의" -> credential_type: "전문의"
- "대한피부과학회 정회원" -> credential_type: "학회"
- "서울대학교 의과대학 졸업" -> credential_type: "학력"
- "삼성서울병원 피부과 전공의" -> credential_type: "경력"

### Role Classification

| Pattern | Role |
|---------|------|
| 대표원장, 원장 | director |
| 전문의 | specialist |
| 전공의, 레지던트 | resident |
| 간호사 | nurse |
| 스태프 | staff |

## Edge Cases

1. **Single doctor clinics**: Doctor info may be on the main page, not a separate page
2. **Photo in CSS background**: Use background-image instead of img src
3. **Lazy loaded images**: Check data-src, data-lazy-src attributes
4. **Career as single text block**: Split by newlines/bullets, not separate list items
5. **No dedicated page**: Doctor section embedded in "About" or main page

## Reference

See: clinic-crawl/clinic_crawl/scripts/extract_doctors.py
See: clinic-crawl/patterns/doctor_menu.json
