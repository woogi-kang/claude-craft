# OpenClaw × Obsidian × 코레일 자동화 블루프린트 (v1)

헴 운영 환경 기준으로 바로 적용 가능한 실전 설계.

---

## 0) 목표

1. **Obsidian 지식OS 구축**
   - 대화/결정/할 일/인물정보를 구조화
2. **OpenClaw 자동 요약/브리핑 루프**
   - daily/weekly 노트 자동 생성
3. **코레일 티켓 모니터링/예약 워크플로우**
   - 승인형(권장) → 필요 시 완전자동

---

## 1) Obsidian Vault 구조 (권장)

```text
vault/
  00-inbox/
    inbox.md
  01-daily/
    2026-02-22.md
  02-topics/
    product.md
    trading.md
    hiring.md
  03-entities/
    people/
      woogi.md
    orgs/
      memoriz.md
      korail.md
  04-tasks/
    inbox.md
    this-week.md
    waiting.md
  05-reports/
    ceo-brief/
      2026-02-22.md
    weekly/
      2026-W08.md
  99-archive/
```

### 운영 규칙
- Hot/Cold 분리: `01-daily`는 60일 지나면 `99-archive`로 이동
- 모든 노트는 Frontmatter 필수
- 위키링크(`[[...]]`)로 topic/entity 연결 강제

---

## 2) 노트 템플릿

### 2-1) Daily Note

```markdown
---
title: 2026-02-22
date: 2026-02-22
tags: [daily, ops]
status: in-progress
source: openclaw
related:
  - "[[02-topics/product]]"
  - "[[03-entities/people/woogi]]"
---

# Daily Log - 2026-02-22

## Summary
- 핵심 요약 3줄

## Decisions
- [D-001] 내용

## Tasks
- [ ] 해야 할 일 1
- [ ] 해야 할 일 2

## Mentions
- [[03-entities/people/woogi]]
- [[03-entities/orgs/memoriz]]
```
```

### 2-2) Topic Hub

```markdown
---
title: Product
date: 2026-02-22
tags: [topic, product]
status: active
---

# Product

## Current Focus
- 현재 집중 이슈

## Linked Notes
- [[01-daily/2026-02-22]]
- [[05-reports/ceo-brief/2026-02-22]]

## Open Tasks
- [ ] TODO
```
```

### 2-3) Entity (Person/Org)

```markdown
---
title: memoriz
date: 2026-02-22
tags: [entity, org]
status: active
aliases: [Memoriz]
---

# memoriz

## Context
- 회사/프로젝트 설명

## Recent Mentions
- [[01-daily/2026-02-22]]

## Related Topics
- [[02-topics/product]]
- [[02-topics/growth]]
```
```

---

## 3) OpenClaw 자동화 설계 (cron)

> 원칙: 정밀 시간 작업은 cron, 컨텍스트성 체크는 heartbeat.

### 3-1) Cron Job A: Daily Capture
- 시간: 매일 00:30
- 목적: 하루 대화 요약 + inbox/task 갱신
- session: isolated
- delivery: none (내부 기록)

### 3-2) Cron Job B: CEO Morning Brief
- 시간: 매일 07:00
- 목적: 전일 핵심 성과/리스크/오늘 우선순위
- session: isolated
- delivery: announce (디스코드 메인 채널)

### 3-3) Cron Job C: Weekly Review
- 시간: 매주 월요일 08:00
- 목적: 주간 KPI, 실패요인, 다음주 액션
- session: isolated
- delivery: announce

### 3-4) Cron Job D: Archive Compaction
- 시간: 매일 03:30
- 목적: 60일 경과 daily를 archive로 이동 + 인덱스 재생성
- session: isolated
- delivery: none

---

## 4) 코레일 봇 워크플로우 (승인형 권장)

### 4-1) 입력 파라미터
- 출발역/도착역
- 날짜/시간대
- 좌석 타입(일반/특실)
- 인원
- 최대 허용 가격/대체열차 허용 여부

### 4-2) 상태 머신
1. `WATCHING` 모니터링 중
2. `CANDIDATE_FOUND` 조건 맞는 좌석 발견
3. `AWAITING_APPROVAL` 승인 대기 (기본)
4. `BOOKING` 예약 시도
5. `BOOKED` 성공
6. `FAILED_RETRY` 실패 후 재시도
7. `HALTED` 계정/레이트 제한 감지

### 4-3) 필수 가드레일
- 1일 최대 시도 횟수 제한
- 동일 열차 중복 시도 방지
- 연속 실패 N회 시 자동 중단
- 레이트리밋/차단 신호 감지 시 `HALTED`
- 예약 실행 전 마지막 확인 메시지(승인형)

### 4-4) 알림 포맷 (디스코드/텔레그램)
- 발견 알림: 열차명, 출발시각, 잔여석, 가격
- 승인 버튼/명령: `approve`, `skip`, `halt`
- 실행 결과: 성공/실패 + 이유 + 다음 재시도 시간

---

## 5) 보안/정책 가이드

- 자격증명은 `.env` 또는 비밀 저장소만 사용
- 예약/결제 직결 액션은 초기엔 승인형으로 운영
- 계정 차단/약관 위반 가능성 있는 고빈도 요청 금지
- 모든 자동 실행은 감사로그(시간, 인자, 결과) 남기기

---

## 6) 1주 도입 플랜

### Day 1-2
- Vault 구조 생성
- 템플릿 파일 등록
- 수동으로 1일치 로그 구조화 테스트

### Day 3-4
- Daily/CEO/Weekly cron 연결
- Obsidian 노트 자동 생성 스크립트 붙이기

### Day 5-6
- 코레일 모니터링 + 승인형 알림 구현
- 실패/중단/재시도 시나리오 테스트

### Day 7
- 실사용 드라이런
- 회고 후 완전자동 전환 여부 결정

---

## 7) 바로 실행 체크리스트

- [ ] Vault 폴더 생성
- [ ] Daily/Topic/Entity 템플릿 저장
- [ ] cron 4개 등록
- [ ] 코레일 봇 입력 파라미터 문서화
- [ ] 승인형 알림 채널 연결
- [ ] 감사로그 파일/DB 스키마 확정

---

## 8) 다음 단계

- OpenClaw `ops` 채널에 코레일 승인형 명령 세트 연결
- topic/entity 오토태깅 정확도 측정 지표 추가
- 2주 후: 승인형 → 부분 자동 승인 정책 전환 검토
