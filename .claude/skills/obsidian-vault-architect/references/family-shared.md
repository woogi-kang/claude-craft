# Family Vault - 공유 구조

가족 공유 Vault 구조 및 핵심 템플릿.

## Folder Structure

```
Family-Vault/
├── 00-Inbox/                 # 빠른 공유 메모
│
├── 10-Todo/                  # 공유 할일 (핵심!)
│   ├── _Todo-Board.md        # 칸반 보드 (MOC)
│   ├── 2026-01-Todo.md       # 월별 Todo
│   └── Recurring/            # 반복 할일
│
├── 20-Home/                  # 가정 관리
│   ├── Chores/               # 집안일 분담
│   ├── Maintenance/          # 집 수리/관리
│   └── Appliances/           # 가전제품 매뉴얼
│
├── 30-Finance/               # 가계 재정
│   ├── Budget/               # 월별 예산
│   ├── Subscriptions/        # 구독 서비스
│   └── Goals/                # 재정 목표
│
├── 40-Plans/                 # 계획
│   ├── Travel/               # 여행 계획
│   ├── Events/               # 이벤트/기념일
│   └── Goals/                # 가족 목표
│
├── 50-Wishlist/              # 위시리스트
│   ├── Shopping.md
│   ├── Restaurants.md
│   └── Activities.md
│
├── 60-Memories/              # 추억
│   └── 2026/
│
├── 90-Meta/
│   ├── Templates/
│   └── Attachments/
│
└── _Dashboard.md             # Family Hub
```

---

## Shared Todo System

### Todo Board (칸반 스타일 MOC)

```markdown
---
title: Family Todo Board
tags:
  - type/moc
  - owner/both
cssclass: kanban
---

# Family Todo Board

## Quick Add
> [!tip] 빠른 추가
> 새 할일: [[10-Todo/{{date:YYYY-MM}}-Todo#New Tasks]]

---

## By Status

### Backlog (예정)

```dataview
TASK
FROM "10-Todo"
WHERE !completed AND contains(tags, "status/backlog")
SORT due ASC
```

### In Progress (진행 중)

```dataview
TASK
FROM "10-Todo"
WHERE !completed AND contains(tags, "status/doing")
SORT due ASC
```

### Done This Week (완료)

```dataview
TASK
FROM "10-Todo"
WHERE completed AND completion >= date(today) - dur(7 days)
SORT completion DESC
LIMIT 10
```

---

## By Owner

### woogi 담당

```dataview
TASK
FROM "10-Todo"
WHERE !completed AND contains(text, "@woogi")
SORT due ASC
```

### wife 담당

```dataview
TASK
FROM "10-Todo"
WHERE !completed AND contains(text, "@wife")
SORT due ASC
```

### 함께 할 일

```dataview
TASK
FROM "10-Todo"
WHERE !completed AND contains(text, "@both")
SORT due ASC
```

---

## Overdue (기한 지남)

```dataview
TASK
FROM "10-Todo"
WHERE !completed AND due < date(today)
SORT due ASC
```
```

---

### Monthly Todo Template

```markdown
---
title: {{date:YYYY년 MM월}} 할일
date: {{date:YYYY-MM-01}}
tags:
  - type/todo
  - owner/both
---

# {{date:YYYY년 MM월}} 할일

## New Tasks
> 여기에 새 할일 추가 (아래 형식 사용)

- [ ] 할일 내용 @담당자 📅 YYYY-MM-DD #status/backlog


---

## Weekly Breakdown

### Week 1 (1일 ~ 7일)

- [ ] @woogi 예시 할일 📅 2026-01-05 #status/backlog
- [ ] @wife 예시 할일 📅 2026-01-06 #status/backlog
- [ ] @both 함께 할 일 📅 2026-01-07 #status/backlog

### Week 2 (8일 ~ 14일)

- [ ]

### Week 3 (15일 ~ 21일)

- [ ]

### Week 4 (22일 ~ 말일)

- [ ]

---

## Recurring (매월 반복)

- [ ] @woogi 월세 납부 📅 {{date:YYYY-MM}}-25 #status/backlog
- [ ] @wife 공과금 확인 📅 {{date:YYYY-MM}}-20 #status/backlog
- [ ] @both 가계부 정리 📅 {{date:YYYY-MM}}-01 #status/backlog

---

## Completed

> 완료된 항목은 여기로 이동 (또는 그대로 두면 Dataview가 필터링)

---

## Notes

> [!note] 이번 달 메모
> - 특이사항 기록
```

---

### Single Todo Item (상세 할일)

복잡한 할일은 별도 노트로:

```markdown
---
title: "{{todo-title}}"
date: {{date:YYYY-MM-DD}}
tags:
  - type/todo-item
  - status/backlog
  - priority/{{priority}}
owner: "@{{owner}}"
due: {{due-date}}
related:
  -
---

# {{todo-title}}

## Overview

| 항목 | 내용 |
|------|------|
| 담당자 | @{{owner}} |
| 기한 | {{due-date}} |
| 우선순위 | High / Medium / Low |
| 상태 | Backlog / Doing / Done |

---

## Description
> 할일 상세 설명

---

## Checklist

- [ ] 세부 항목 1
- [ ] 세부 항목 2
- [ ] 세부 항목 3

---

## Notes

> [!note] 진행 메모
> -

---

## Related

- [[관련 노트]]
```

---

## Todo 문법 규칙

### 기본 형식

```markdown
- [ ] 할일 내용 @담당자 📅 YYYY-MM-DD #status/태그
```

### 담당자 표기

| 표기 | 의미 |
|------|------|
| `@woogi` | woogi 담당 |
| `@wife` | wife 담당 |
| `@both` | 함께 할 일 |

### 상태 태그

| 태그 | 의미 |
|------|------|
| `#status/backlog` | 예정 (아직 시작 안 함) |
| `#status/doing` | 진행 중 |
| `#status/blocked` | 막힘 (대기 중) |
| (체크 완료) | 완료 |

### 우선순위 표기

| 표기 | 의미 |
|------|------|
| `#priority/high` 또는 `🔴` | 긴급/중요 |
| `#priority/medium` 또는 `🟡` | 보통 |
| `#priority/low` 또는 `🟢` | 낮음 |

### 예시

```markdown
- [ ] 세탁기 AS 신청 @woogi 📅 2026-02-01 #status/backlog #priority/high
- [ ] 여행 숙소 예약 @wife 📅 2026-02-15 #status/doing
- [ ] 주말 대청소 @both 📅 2026-02-03 #status/backlog
- [x] 공과금 납부 @woogi 📅 2026-01-25 ✅ 2026-01-24
```

---

## Family Dashboard

```markdown
---
title: Family Hub
tags:
  - type/moc
  - owner/both
---

# Family Hub

## Quick Actions

| 액션 | 바로가기 |
|------|----------|
| 할일 추가 | [[10-Todo/_Todo-Board]] |
| 이번 달 가계부 | [[30-Finance/Budget/{{date:YYYY-MM}}-Budget]] |
| 여행 계획 | [[40-Plans/Travel/]] |

---

## Urgent (이번 주)

```dataview
TASK
FROM "10-Todo"
WHERE !completed AND due <= date(today) + dur(7 days)
SORT due ASC
LIMIT 10
```

---

## Overdue (기한 지남)

```dataview
TASK
FROM "10-Todo"
WHERE !completed AND due < date(today)
SORT due ASC
```

---

## This Month Summary

### 할일 현황

```dataview
TABLE WITHOUT ID
  length(filter(rows, (r) => !r.completed)) as "남은 할일",
  length(filter(rows, (r) => r.completed)) as "완료"
FROM "10-Todo"
WHERE file.name = "{{date:YYYY-MM}}-Todo"
FLATTEN file.tasks as tasks
GROUP BY file.name
```

### 지출 현황

> [[30-Finance/Budget/{{date:YYYY-MM}}-Budget|이번 달 가계부 보기]]

---

## Upcoming Events

```dataview
TABLE date as "날짜", WITHOUT ID
FROM "40-Plans/Events"
WHERE date >= date(today)
SORT date ASC
LIMIT 5
```

---

## Recent Activity

```dataview
LIST
FROM "10-Todo" OR "30-Finance" OR "40-Plans"
SORT file.mtime DESC
LIMIT 5
```
```

---

## 반복 할일 관리

### Recurring Todo Template

```markdown
---
title: 반복 할일 목록
tags:
  - type/recurring
  - owner/both
---

# 반복 할일

## Daily (매일)

- [ ] 분리수거 확인 @both

## Weekly (매주)

| 요일 | 할일 | 담당 |
|------|------|------|
| 월 | 화분 물주기 | @wife |
| 수 | 음식물 쓰레기 | @woogi |
| 금 | 청소기 돌리기 | @both |
| 일 | 다음 주 식단 계획 | @both |

## Monthly (매월)

| 날짜 | 할일 | 담당 |
|------|------|------|
| 1일 | 가계부 정산 | @both |
| 10일 | 카드값 확인 | @wife |
| 25일 | 월세/관리비 | @woogi |
| 말일 | 다음 달 예산 | @both |

## Yearly (매년)

| 날짜 | 할일 | 담당 |
|------|------|------|
| 1월 | 연간 재정 계획 | @both |
| 3월 | 봄맞이 대청소 | @both |
| 5월 | 에어컨 점검 | @woogi |
| 11월 | 보일러 점검 | @woogi |
| 12월 | 연말 정산 준비 | @both |
```
