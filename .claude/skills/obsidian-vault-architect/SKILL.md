---
name: obsidian-vault-architect
description: Obsidian Vault 구조 설계 전문 Skill. 폴더 구조, 파일명 규칙, 태그 체계, 템플릿 설계 등 Vault 아키텍처를 설계하고 관리할 때 활성화. 개인/공유 Vault 하이브리드 구성 지원.
version: 1.0.0
user-invocable: true
triggers:
  keywords:
    - vault 구조
    - vault structure
    - 폴더 구조
    - folder structure
    - 옵시디언 설계
    - obsidian setup
    - 태그 체계
    - 템플릿
dependencies:
  - obsidian-core
updated: 2026-01-30
---

# Obsidian Vault Architect

Vault 구조 설계 및 관리 전문 Skill.

부부/가족 공동 사용 환경에 최적화된 하이브리드 구성 지원.

## Vault Types

| 유형 | 설명 | 동기화 |
|------|------|--------|
| **Personal** | 개인 전용 (업무, 일기, 개인 프로젝트) | 본인 디바이스만 |
| **Family** | 가족 공유 (가계부, 여행, 공유 문서) | 모든 가족 디바이스 |

## Architecture Overview

```
NAS: /volume1/obsidian/
├── woogi/          # Personal Vault (나)
├── wife/           # Personal Vault (와이프)
└── family/         # Family Vault (공유)
```

---

## Personal Vault Structure

```
Personal-Vault/
├── 00-Inbox/                 # 빠른 캡처, 미분류
│   └── (임시 노트들)
│
├── 10-Projects/              # 진행 중인 프로젝트
│   ├── project-alpha/
│   │   ├── _index.md         # 프로젝트 허브
│   │   ├── meetings/
│   │   ├── tasks/
│   │   └── references/
│   └── project-beta/
│
├── 20-Areas/                 # 지속 관리 영역
│   ├── Career/               # 커리어, 이력서
│   ├── Health/               # 건강, 운동
│   ├── Finance/              # 개인 재정
│   ├── Learning/             # 학습, 자기계발
│   └── Side-Projects/        # 사이드 프로젝트
│
├── 30-Resources/             # 참조 자료
│   ├── Development/          # 개발 지식
│   │   ├── Flutter/
│   │   ├── Backend/
│   │   └── DevOps/
│   ├── Books/                # 독서 노트
│   ├── Courses/              # 강의 노트
│   └── Articles/             # 아티클 스크랩
│
├── 40-Archives/              # 완료/보관
│   ├── 2025/
│   └── 2026/
│
├── 50-Daily/                 # 일간 노트
│   ├── 2026/
│   │   ├── 01-January/
│   │   │   ├── 2026-01-01.md
│   │   │   └── 2026-01-02.md
│   │   └── 02-February/
│   └── Templates/
│
├── 60-Journal/               # 개인 저널/일기
│   └── (비공개 일기)
│
├── 90-Meta/                  # Vault 관리
│   ├── Templates/            # 템플릿 파일
│   ├── Attachments/          # 첨부파일
│   └── Scripts/              # Dataview 등 스크립트
│
└── _Dashboard.md             # Vault 홈 (MOC)
```

---

## Family Vault Structure

```
Family-Vault/
├── 00-Inbox/                 # 빠른 공유 캡처
│
├── 10-Home/                  # 가정 관리
│   ├── Chores/               # 집안일 분담
│   ├── Maintenance/          # 집 수리/관리
│   ├── Appliances/           # 가전제품 매뉴얼
│   └── Contacts/             # 공유 연락처
│
├── 20-Finance/               # 가계 재정
│   ├── Budget/               # 월별 예산
│   │   ├── 2026-01-Budget.md
│   │   └── 2026-02-Budget.md
│   ├── Expenses/             # 지출 기록
│   ├── Subscriptions/        # 구독 서비스 관리
│   └── Goals/                # 재정 목표
│
├── 30-Plans/                 # 계획
│   ├── Travel/               # 여행 계획
│   │   ├── 2026-Japan/
│   │   └── 2026-Jeju/
│   ├── Events/               # 이벤트/기념일
│   └── Goals/                # 가족 목표
│
├── 40-Documents/             # 공유 문서
│   ├── Receipts/             # 영수증/보증서
│   ├── Contracts/            # 계약서
│   └── Medical/              # 의료 기록
│
├── 50-Wishlist/              # 위시리스트
│   ├── Shopping/             # 구매 희망
│   ├── Restaurants/          # 가고 싶은 식당
│   └── Activities/           # 하고 싶은 활동
│
├── 60-Memories/              # 추억
│   ├── 2026/
│   └── Albums/
│
├── 90-Meta/
│   ├── Templates/
│   └── Attachments/
│
└── _Dashboard.md             # Family Hub
```

---

## Naming Conventions

### 폴더 명명 규칙

| 패턴 | 용도 | 예시 |
|------|------|------|
| `XX-Name/` | 정렬용 번호 접두사 | `10-Projects/` |
| `lowercase-kebab/` | 프로젝트/토픽 폴더 | `flutter-app/` |
| `YYYY/MM-Month/` | 날짜 기반 폴더 | `2026/01-January/` |

### 파일 명명 규칙

| 타입 | 패턴 | 예시 |
|------|------|------|
| Daily Note | `YYYY-MM-DD.md` | `2026-01-30.md` |
| Meeting | `YYYY-MM-DD-meeting-topic.md` | `2026-01-30-meeting-sprint-review.md` |
| Project Index | `_index.md` | `_index.md` |
| Dashboard | `_Dashboard.md` | `_Dashboard.md` |
| 일반 노트 | `제목-그대로.md` | `Flutter 상태관리 비교.md` |
| Budget | `YYYY-MM-Budget.md` | `2026-01-Budget.md` |

### 특수 접두사

| 접두사 | 의미 | 예시 |
|--------|------|------|
| `_` | 메타/인덱스 파일 | `_Dashboard.md`, `_index.md` |
| `!` | 중요/긴급 | `!긴급-서버점검.md` |
| `@` | 사람 관련 | `@홍길동.md` |

---

## Tag System

### Personal Vault Tags

```yaml
# 상태 태그
tags:
  - status/inbox        # 미처리
  - status/active       # 진행 중
  - status/done         # 완료
  - status/archived     # 보관

# 타입 태그
  - type/note           # 일반 노트
  - type/meeting        # 회의록
  - type/project        # 프로젝트
  - type/reference      # 참조 자료
  - type/daily          # 일간 노트

# 도메인 태그 (개인)
  - dev/flutter
  - dev/backend
  - career/resume
  - learning/course
```

### Family Vault Tags

```yaml
# 공유 태그
tags:
  - owner/woogi         # 담당자
  - owner/wife
  - owner/both

# 카테고리 태그
  - finance/expense
  - finance/budget
  - travel/plan
  - travel/review
  - home/maintenance
  - home/chores

# 우선순위
  - priority/high
  - priority/medium
  - priority/low
```

---

## Template Patterns

### Daily Note Template

```markdown
---
title: {{date:YYYY-MM-DD}} Daily Note
date: {{date:YYYY-MM-DD}}
tags:
  - type/daily
  - status/active
author: {{author}}
---

# {{date:YYYY-MM-DD}} {{date:dddd}}

## Morning Intention
- [ ] 오늘의 최우선 과제:

## Tasks
- [ ]

## Notes


## Evening Reflection
- 오늘 잘한 것:
- 내일 개선할 것:

---
[[{{date-1d:YYYY-MM-DD}}]] | [[{{date+1d:YYYY-MM-DD}}]]
```

### Meeting Note Template

```markdown
---
title: {{date:YYYY-MM-DD}} Meeting - {{title}}
date: {{date:YYYY-MM-DD}}
tags:
  - type/meeting
  - status/active
author: {{author}}
attendees:
  -
related:
  -
---

# {{title}}

## Info
| 항목 | 내용 |
|------|------|
| 일시 | {{date:YYYY-MM-DD HH:mm}} |
| 참석자 | |
| 장소 | |

## Agenda
1.

## Notes


## Action Items
- [ ] @담당자: 할 일 (기한: YYYY-MM-DD)

## Next Steps

```

### Budget Template (Family)

```markdown
---
title: {{date:YYYY-MM}} Budget
date: {{date:YYYY-MM-01}}
tags:
  - finance/budget
  - owner/both
---

# {{date:YYYY년 MM월}} 가계부

## Summary
| 항목 | 금액 |
|------|------|
| 수입 | |
| 지출 | |
| 잔액 | |

## Income
| 날짜 | 내용 | 금액 | 담당 |
|------|------|------|------|
| | | | |

## Fixed Expenses (고정 지출)
| 항목 | 금액 | 결제일 |
|------|------|--------|
| 월세/관리비 | | |
| 통신비 | | |
| 보험 | | |
| 구독 서비스 | | |

## Variable Expenses (변동 지출)
| 날짜 | 카테고리 | 내용 | 금액 | 담당 |
|------|----------|------|------|------|
| | 식비 | | | |
| | 교통 | | | |
| | 생활 | | | |

## Notes

```

### Travel Plan Template (Family)

```markdown
---
title: {{destination}} 여행 계획
date: {{date:YYYY-MM-DD}}
tags:
  - travel/plan
  - owner/both
trip-dates:
  start:
  end:
destination: {{destination}}
budget:
---

# {{destination}} 여행

## Overview
| 항목 | 내용 |
|------|------|
| 기간 | ~ |
| 예산 | |
| 테마 | |

## Checklist
- [ ] 숙소 예약
- [ ] 교통편 예약
- [ ] 여행자 보험
- [ ] 짐 싸기

## Itinerary

### Day 1 (날짜)
| 시간 | 일정 | 장소 | 비용 |
|------|------|------|------|
| | | | |

### Day 2 (날짜)
| 시간 | 일정 | 장소 | 비용 |
|------|------|------|------|
| | | | |

## Packing List
- [ ] 여권
- [ ] 충전기
- [ ]

## Budget Breakdown
| 카테고리 | 예산 | 실제 |
|----------|------|------|
| 교통 | | |
| 숙박 | | |
| 식비 | | |
| 활동 | | |
| 쇼핑 | | |
| **합계** | | |

## Notes & Memories

```

---

## Dashboard (MOC) Pattern

### Personal Dashboard

```markdown
---
title: Dashboard
tags:
  - type/moc
---

# My Dashboard

## Quick Capture
> [!tip] Inbox
> [[00-Inbox/|Inbox로 이동]] - {{dataview로 Inbox 개수 표시}}

## Active Projects
```dataview
TABLE status, due
FROM "10-Projects"
WHERE status = "active"
SORT due ASC
```

## Recent Notes
```dataview
LIST
FROM ""
SORT file.mtime DESC
LIMIT 10
```

## Areas
- [[20-Areas/Career/|Career]]
- [[20-Areas/Health/|Health]]
- [[20-Areas/Finance/|Finance]]
- [[20-Areas/Learning/|Learning]]
```

### Family Dashboard

```markdown
---
title: Family Dashboard
tags:
  - type/moc
  - owner/both
---

# Family Hub

## This Month
- [[20-Finance/Budget/{{date:YYYY-MM}}-Budget|이번 달 가계부]]
- 다가오는 일정: (Dataview)

## Quick Links
| 영역 | 바로가기 |
|------|----------|
| 가계부 | [[20-Finance/Budget/]] |
| 여행 계획 | [[30-Plans/Travel/]] |
| 위시리스트 | [[50-Wishlist/]] |
| 집 관리 | [[10-Home/]] |

## To-Do (공유)
```dataview
TASK
FROM "10-Home" OR "30-Plans"
WHERE !completed
LIMIT 10
```

## Recent Updates
```dataview
LIST
FROM ""
SORT file.mtime DESC
LIMIT 5
```
```

---

## Plugin Recommendations

### Essential Plugins

| 플러그인 | 용도 | Personal | Family |
|----------|------|:--------:|:------:|
| **Dataview** | 동적 쿼리, 대시보드 | O | O |
| **Templater** | 고급 템플릿 | O | O |
| **Calendar** | 일간 노트 네비게이션 | O | - |
| **Periodic Notes** | 일간/주간/월간 노트 | O | - |
| **Obsidian LiveSync** | NAS 동기화 | O | O |
| **obsidian-claude-code-mcp** | Claude Code 연동 | O | O |

### Optional Plugins

| 플러그인 | 용도 |
|----------|------|
| **Kanban** | 프로젝트 보드 |
| **Excalidraw** | 다이어그램/스케치 |
| **Tasks** | 고급 태스크 관리 |
| **Minimal Theme** | 깔끔한 UI |

---

## Workflow Patterns

### PARA Method Integration

```
P - Projects   → 10-Projects/
A - Areas      → 20-Areas/
R - Resources  → 30-Resources/
A - Archives   → 40-Archives/
```

### Daily Workflow

```
1. Morning: Daily Note 생성 → Intention 작성
2. During Day: Inbox에 빠른 캡처
3. Evening: Inbox 정리 → 적절한 폴더로 이동
4. Weekly: Weekly Review → Archives 정리
```

### Family Sync Workflow

```
1. 각자 개인 Vault에서 작업
2. 공유할 내용 → Family Vault로 이동/복사
3. 가계부, 여행 계획 → Family Vault에서 공동 편집
4. 민감한 개인 정보 → 절대 Family Vault에 저장 안 함
```

---

## Security Guidelines

| Vault | 저장 가능 | 저장 금지 |
|-------|----------|----------|
| **Personal** | 개인 일기, 업무 노트, 커리어 | - |
| **Family** | 가계부, 여행, 공유 문서 | 개인 비밀번호, 민감한 개인정보 |

> [!warning] 보안 주의
> - Family Vault에 개인 비밀번호, 금융 인증 정보 저장 금지
> - 민감 정보는 Personal Vault + 암호화 플러그인 사용 권장

---

## Quick Setup Checklist

- [ ] NAS에 Vault 폴더 3개 생성 (woogi, wife, family)
- [ ] CouchDB + LiveSync 설정
- [ ] 각 Vault에 기본 폴더 구조 생성
- [ ] Templates 폴더에 템플릿 파일 추가
- [ ] 필수 플러그인 설치
- [ ] Dashboard 생성
- [ ] Claude Code MCP 연동 테스트
