# Multica 에이전트 + 스킬 연동 계획

> 작성일: 2026-04-10
> 상태: 계획 수립 완료, 실행 대기

---

## 현황

### 완료된 작업
- [x] Multica CLI 설치 (v0.1.22)
- [x] multica.ai 클라우드 로그인
- [x] 데몬 시작 — 런타임 2개 활성화
  - Claude (gangtaeug-ui-MacBookPro.local) — `a306dd18`
  - Codex (gangtaeug-ui-MacBookPro.local) — `f8c7cf86`
- [x] 스킬 380개 등록 완료 (349 기본 + 31 k-skill)

### 미완료 작업
- [ ] 도메인별 에이전트 생성
- [ ] 에이전트별 스킬 매핑
- [ ] 에이전트 instructions 작성
- [ ] 동기화 스크립트 작성

---

## Multica 오케스트레이션 이해

### 실행 흐름
```
이슈 할당/코멘트/@멘션 → 서버가 태스크 enqueue
  → 데몬이 3초 폴링으로 claim
  → 격리 디렉터리 생성
  → 스킬 파일 기록: {workdir}/.claude/skills/{name}/SKILL.md
  → CLAUDE.md 자동 생성 (instructions + 메타 + 스킬 목록)
  → claude -p --permission-mode bypassPermissions < prompt
  → 결과 스트리밍 → 완료/실패 보고
```

### 자동 생성되는 CLAUDE.md 구조
```markdown
# Multica Agent Runtime
## Agent Identity          ← --instructions 내용
## Available Commands       ← multica CLI 레퍼런스
## Repositories            ← 체크아웃 가능한 레포
## Workflow                ← 트리거별 작업 절차
## Skills                  ← 할당된 스킬 이름 목록
```

### 핵심 포인트
- **라우팅은 수동** — 사람이 이슈를 에이전트에 할당하여 결정
- **스킬은 파일 시스템 주입** — `.claude/skills/`에 SKILL.md를 기록하면 Claude Code가 네이티브 발견
- **instructions는 CLAUDE.md에 인라인** — "Agent Identity" 섹션으로 주입
- **세션 재사용** — 동일 (에이전트, 이슈) 쌍은 이전 세션을 `--resume`으로 이어서 실행

---

## 에이전트 생성 계획

### 도메인별 에이전트 매핑 (13개)

| # | 에이전트 이름 | 런타임 | 스킬 prefix | 스킬 수 | Instructions 핵심 |
|---|-------------|--------|------------|---------|------------------|
| 1 | **FastAPI Developer** | Claude | `fastapi-*`, `shared-*` | ~44 | Python API 전문. Clean Architecture + SQLAlchemy + pytest |
| 2 | **Flutter Developer** | Claude | `flutter-*`, `shared-*` | ~39 | Flutter 3.24+ 전문. Riverpod 3 + GoRouter + TDD |
| 3 | **Next.js Developer** | Claude | `nextjs-*`, `shared-*` | ~40 | Next.js App Router 전문. TanStack Query + Zustand + shadcn |
| 4 | **F2N Migrator** | Claude | `f2n-*` | 8 | Flutter → Next.js 마이그레이션 전문 |
| 5 | **Product Planner** | Claude | `plan-*` | 83 | 아이디어 → 출시까지 8단계 기획. PRD, 페르소나, OKR, 로드맵 |
| 6 | **UI/UX Designer** | Claude | `ui-*`, `design-*` | ~22 | 웹/모바일 UI 디자인. 50+ 스타일, 161 팔레트 |
| 7 | **Content Creator** | Claude | `presentation-*`, `social-*`, `tech-*` | ~32 | PPT, SNS, 블로그 콘텐츠 제작 |
| 8 | **Marketing Strategist** | Claude | `marketing-*`, `seo-*`, `cro-*`, `growth-*`, `sales-*` | ~43 | 마케팅 전략, SEO, CRO, 그로스, 세일즈 |
| 9 | **Legal Advisor** | Claude | `legal-*`, `corporate-*` | ~17 | 계약 검토, 법인 운영, 규제 관리 |
| 10 | **Finance Manager** | Claude | `finance-*`, `payment-*` | ~13 | 재무 보고, 결제 시스템, 구독 관리 |
| 11 | **K-Life Assistant** | Claude | `kr-*` | 31 | 한국생활 도우미. SRT/KTX, 날씨, 주식, 배송추적 등 |
| 12 | **Code Reviewer** | Claude | `shared-*`, `verification-*` | ~9 | 코드/아키텍처/보안 리뷰 |
| 13 | **General Assistant** | Claude | (전체) | 380 | 범용. 도메인 특화 에이전트가 없는 작업 처리 |

### 에이전트별 Instructions 설계

각 에이전트의 `--instructions`에는 다음을 포함:

```markdown
## 역할
{도메인 전문가 역할 정의}

## 작업 방식
1. `multica issue get <id> --output json`으로 이슈 파악
2. 필요 시 `multica repo checkout <url>`로 레포 체크아웃
3. 할당된 스킬을 참고하여 작업 수행
4. 진행 상황은 `multica issue comment add`로 보고
5. 완료 시 결과 요약 코멘트

## 코딩 컨벤션
- {도메인별 규칙 요약 — python/typescript coding-style에서 발췌}

## 제약
- 보안 민감 정보 커밋 금지
- 기존 패턴/컨벤션 준수
- 과도한 엔지니어링 금지
```

---

## 실행 스크립트 계획

### `scripts/setup-multica-agents.py`

```python
# 1. 에이전트 생성
multica agent create \
  --name "FastAPI Developer" \
  --runtime-id "a306dd18-..." \
  --instructions "$(cat agents/fastapi-instructions.md)" \
  --max-concurrent-tasks 6

# 2. 해당 도메인 스킬 ID 조회
skill_ids = multica skill list --output json | filter by prefix

# 3. 스킬 할당
multica agent skills set <agent-id> --skill-ids "id1,id2,..."
```

### 주요 기능
- 에이전트 13개 자동 생성
- 스킬 prefix 기반 자동 매핑
- `shared-*` 스킬은 개발 에이전트(FastAPI/Flutter/Next.js)에 공통 할당
- 이미 존재하는 에이전트는 스킵 (멱등성)
- `--dry-run` 지원

### 스킬 매핑 규칙

```python
AGENT_SKILL_MAP = {
    "FastAPI Developer": {
        "prefixes": ["fastapi-", "shared-"],
        "exact": ["agent-browser-test"],
    },
    "Flutter Developer": {
        "prefixes": ["flutter-", "shared-"],
    },
    "Next.js Developer": {
        "prefixes": ["nextjs-", "shared-"],
        "exact": ["remotion-video-production", "nextjs-boilerplate", "agent-browser-test"],
    },
    "F2N Migrator": {
        "prefixes": ["f2n-"],
    },
    "Product Planner": {
        "prefixes": ["plan-"],
    },
    "UI/UX Designer": {
        "prefixes": ["ui-", "design-"],
        "exact": ["banner-design", "brand"],
    },
    "Content Creator": {
        "prefixes": ["presentation-", "social-", "tech-"],
        "exact": ["slides", "social-content"],
    },
    "Marketing Strategist": {
        "prefixes": ["marketing-", "seo-", "cro-", "growth-", "sales-"],
    },
    "Legal Advisor": {
        "prefixes": ["legal-", "corporate-"],
        "exact": ["labor-law-advisor"],
    },
    "Finance Manager": {
        "prefixes": ["finance-", "payment-"],
    },
    "K-Life Assistant": {
        "prefixes": ["kr-"],
    },
    "Code Reviewer": {
        "prefixes": ["shared-"],
        "exact": ["verification-loop", "eval-harness"],
    },
    "General Assistant": {
        "prefixes": [],  # 전체 스킬 할당
    },
}
```

---

## 동기화 전략

### 스킬 추가/변경 시
```bash
# 새 스킬 추가 → 기존 스크립트 재실행 (중복은 자동 스킵)
python3 scripts/sync-skills-to-multica.py

# 에이전트 스킬 재매핑
python3 scripts/setup-multica-agents.py --update-skills
```

### 향후 자동화
- `scripts/sync-to-projects.sh`에 Multica 동기화 추가 고려
- 스킬 CRUD 시 자동 Multica 반영 (hook 연동 가능)

---

## 실행 순서

```
Phase 1: 에이전트 생성 + 스킬 매핑 스크립트 작성
  └ scripts/setup-multica-agents.py

Phase 2: 에이전트별 instructions 작성
  └ .claude/multica/instructions/{agent-name}.md

Phase 3: 스크립트 실행 → 에이전트 13개 생성 + 스킬 할당

Phase 4: 테스트 이슈 생성 → 에이전트 할당 → 동작 확인

Phase 5: (선택) sync-to-projects.sh에 Multica 동기화 통합
```

---

## 참고

- Multica CLI: `multica --help`
- 등록된 스킬 목록: `multica skill list`
- 런타임 상태: `multica daemon status`
- 동기화 스크립트: `scripts/sync-skills-to-multica.py`
- Multica 소스: https://github.com/multica-ai/multica
