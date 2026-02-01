# Personal Vault - 개발자용 구조

개발자를 위한 Personal Vault 구조 및 템플릿.

## Folder Structure

```
Personal-Vault (Developer)/
├── 00-Inbox/                 # 빠른 캡처
│
├── 10-Projects/              # 진행 중인 프로젝트
│   ├── project-alpha/
│   │   ├── _index.md         # 프로젝트 허브
│   │   ├── specs/            # 기술 스펙
│   │   ├── dev-notes/        # 개발 노트
│   │   ├── meetings/         # 회의록
│   │   ├── troubleshooting/  # 트러블슈팅
│   │   └── references/       # 참고자료
│   └── side-project/
│
├── 20-Areas/                 # 지속 관리 영역
│   ├── Career/               # 커리어 (이력서, 포트폴리오)
│   ├── Learning/             # 학습 계획
│   ├── Side-Projects/        # 사이드 프로젝트 아이디어
│   └── Tools/                # 개발 도구 설정
│
├── 30-Resources/             # 참조 자료 (Zettelkasten)
│   ├── Development/
│   │   ├── Flutter/
│   │   ├── Backend/
│   │   ├── DevOps/
│   │   ├── Architecture/
│   │   └── Best-Practices/
│   ├── Books/                # 독서 노트
│   ├── Courses/              # 강의 노트
│   └── Articles/             # 아티클 스크랩
│
├── 40-Archives/              # 완료/보관
│   ├── 2025/
│   └── 2026/
│
├── 50-Daily/                 # 일간 노트
│   └── 2026/
│
├── 60-Journal/               # 개인 일기/회고
│
├── 90-Meta/
│   ├── Templates/
│   └── Attachments/
│
└── _Dashboard.md
```

---

## 핵심 템플릿

### Dev Note (개발 노트)

```markdown
---
title: "{{title}}"
date: {{date:YYYY-MM-DD}}
tags:
  - type/dev-note
  - tech/{{technology}}
  - status/draft
author: woogi
project: "[[Project 링크]]"
---

# {{title}}

## Context
> 이 노트를 작성하게 된 배경/맥락

---

## Problem
> 해결하려는 문제 또는 구현하려는 기능

---

## Solution

### Approach
> 접근 방법 설명

### Implementation

```{{language}}
// 파일: {{file-path}}
// 핵심 코드
```

### Key Points
- 포인트 1
- 포인트 2

---

## Learnings

> [!tip] 배운 점
> -

> [!warning] 주의할 점
> -

---

## Related

- [[관련 노트]]
- [외부 링크]()

---

## References

- [공식 문서]()
- [참고 블로그]()
```

---

### TIL (Today I Learned)

```markdown
---
title: "TIL: {{title}}"
date: {{date:YYYY-MM-DD}}
tags:
  - type/til
  - tech/{{technology}}
author: woogi
---

# TIL: {{title}}

## What I Learned
> 오늘 배운 것 요약

---

## Details

### The Problem
> 어떤 상황/문제에서 이걸 배웠나

### The Solution
> 해결책 또는 새로 알게 된 내용

```{{language}}
// 코드 예시
```

---

## Key Takeaways

1. 핵심 1
2. 핵심 2

---

## Further Reading

- [[관련 노트]]
- [참고 링크]()
```

---

### Troubleshooting Note

```markdown
---
title: "Fix: {{error-name}}"
date: {{date:YYYY-MM-DD}}
tags:
  - type/troubleshooting
  - tech/{{technology}}
  - error/{{error-type}}
author: woogi
---

# Fix: {{error-name}}

## Error

```
에러 메시지 전문
```

---

## Environment

| 항목 | 버전 |
|------|------|
| OS | |
| Language | |
| Framework | |
| 기타 | |

---

## Symptoms
- 증상 1
- 증상 2

---

## Root Cause
> 원인 분석

---

## Solution

### Quick Fix
```{{language}}
// 빠른 해결책
```

### Proper Fix
> 근본적인 해결책 설명

```{{language}}
// 코드
```

---

## Prevention
> 재발 방지를 위한 조치

- [ ] 체크리스트 1
- [ ] 체크리스트 2

---

## Related

- [[관련 에러]]
- [Stack Overflow]()
- [GitHub Issue]()
```

---

### Code Snippet

```markdown
---
title: "Snippet: {{title}}"
date: {{date:YYYY-MM-DD}}
tags:
  - type/snippet
  - tech/{{technology}}
  - lang/{{language}}
author: woogi
---

# Snippet: {{title}}

## Use Case
> 언제 사용하는가

---

## Code

```{{language}}
// {{title}}
// 사용법:

{{code}}
```

---

## Usage Example

```{{language}}
// 실제 사용 예시
```

---

## Notes

- 주의사항 1
- 주의사항 2

---

## Source

- [원본]()
```

---

### Tech Research Note

```markdown
---
title: "Research: {{topic}}"
date: {{date:YYYY-MM-DD}}
tags:
  - type/research
  - tech/{{category}}
  - status/draft
author: woogi
---

# Research: {{topic}}

## Overview
> 이 기술/라이브러리/패턴이 무엇인가

---

## Why Consider This?
> 왜 이것을 조사하게 되었나

---

## Pros & Cons

| Pros | Cons |
|------|------|
| 장점 1 | 단점 1 |
| 장점 2 | 단점 2 |

---

## Comparison

| 항목 | {{option1}} | {{option2}} | {{option3}} |
|------|-------------|-------------|-------------|
| 성능 | | | |
| 학습곡선 | | | |
| 커뮤니티 | | | |
| 문서화 | | | |

---

## Getting Started

```{{language}}
// 기본 사용법
```

---

## Key Concepts

1. **개념 1**: 설명
2. **개념 2**: 설명

---

## Resources

- [공식 문서]()
- [튜토리얼]()
- [예제 레포]()

---

## Verdict

> [!note] 결론
> 사용할지 말지, 언제 사용할지에 대한 결론
```

---

## Developer Dashboard

```markdown
---
title: Dev Dashboard
tags:
  - type/moc
---

# Dev Dashboard

## Quick Links

| 바로가기 | 설명 |
|----------|------|
| [[00-Inbox/]] | 빠른 캡처 |
| [[10-Projects/]] | 프로젝트 |
| [[50-Daily/]] | Daily Log |

---

## Active Projects

```dataview
TABLE
  status as "상태",
  file.mtime as "최근 수정"
FROM "10-Projects"
WHERE contains(file.name, "_index")
SORT file.mtime DESC
```

---

## Recent Dev Notes

```dataview
TABLE
  tags as "기술",
  file.mtime as "수정일"
FROM #type/dev-note
SORT file.mtime DESC
LIMIT 10
```

---

## Recent TILs

```dataview
LIST
FROM #type/til
SORT file.ctime DESC
LIMIT 5
```

---

## Unresolved Issues

```dataview
TASK
FROM "10-Projects"
WHERE !completed AND contains(text, "TODO") OR contains(text, "FIXME")
LIMIT 10
```

---

## This Week's Focus

> [!note] 이번 주 목표
> - [ ] 목표 1
> - [ ] 목표 2

---

## Learning Queue

```dataview
LIST
FROM "20-Areas/Learning"
WHERE contains(tags, "status/todo")
LIMIT 5
```
```

---

## Daily Note (개발자용)

```markdown
---
title: {{date:YYYY-MM-DD}} Daily Log
date: {{date:YYYY-MM-DD}}
tags:
  - type/daily
author: woogi
---

# {{date:YYYY-MM-DD}} {{date:dddd}}

## Today's Focus
- [ ] 최우선 과제:

---

## Work Log

### Morning


### Afternoon


### Evening


---

## Code Written

```
// 오늘 작성한 주요 코드 또는 커밋 요약
```

---

## Learnings / TIL

> 오늘 배운 것

---

## Blockers

> 막힌 것, 내일 해결할 것

---

## Tomorrow

- [ ]

---

[[{{date-1d:YYYY-MM-DD}}]] | [[{{date+1d:YYYY-MM-DD}}]]
```
