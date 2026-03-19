# Craft Orchestra — 자체 오케스트레이션 시스템

> **Status**: Phase 1 구현 중
> **Date**: 2026-03-19
> **Decision**: ClawTeam 사용 안 함 → 기존 orchestrate-worktrees.py 확장 + Pixel Agents 활용

---

## 기술 리스크 분석 결과 (2026-03-19)

### 1. ClawTeam 패키지 상태

| 항목 | 결과 |
|------|------|
| PyPI 존재 여부 | **존재** (pypi.org/project/clawteam) |
| 버전 | 0.1.1, 0.1.2 (2026-03-18 릴리스 — **어제 공개**) |
| 개발 상태 | **Alpha** (Development Status 3) |
| 라이선스 | MIT |
| 출처 | HKUDS (Hong Kong University Data Intelligence Lab) |
| GitHub Stars | ~1,200 |
| API 존재 확인 | TaskStore, MailboxManager, CostStore, SpawnBackend, WorkspaceManager — **모두 존재** |

**리스크**: 릴리스 1일차. 안정성/하위호환 보장 없음. 버전 0.1.x에서 API 파괴적 변경 가능성 높음.

### 2. Claude Code 내장 Agent Teams — 핵심 발견

**Claude Code가 이미 ClawTeam의 핵심 기능을 내장하고 있다:**

| 기능 | ClawTeam | Claude Code Agent Teams | 중복도 |
|------|----------|------------------------|--------|
| 태스크 의존성 | TaskStore | TaskCreate + dependencies | **높음** |
| 에이전트 간 메시징 | MailboxManager | SendMessage / broadcast | **높음** |
| Worktree 격리 | WorkspaceManager | `isolation: "worktree"` | **높음** |
| 비용 추적 | CostStore | 내장 토큰 추적 | **중간** |
| 프로세스 관리 | SpawnBackend (tmux) | Agent tool (내장) | **높음** |
| 모니터링 | `board serve` (웹 UI) | Shift+Down / tmux 패인 | **중간** |

**Claude Code Agent Teams 제공 기능:**
- 직접 에이전트 간 메시징 (message, broadcast)
- 태스크 의존성 자동 해소 (pending → unblock)
- 백그라운드 에이전트 실행 + 모니터링
- Worktree 격리 (isolation: "worktree")
- 팀 생성/관리/정리

**Claude Code Agent Teams 제약:**
- 세션 재개 시 in-process 팀원 복원 안 됨
- 팀원이 태스크 완료 표시 누락하는 경우 있음
- 팀당 1개 세션만 가능
- 중첩 팀 불가
- Split pane은 tmux/iTerm2에서만 작동
- **아직 실험적(experimental) 기능**

### 3. 기존 Orchestration 시스템

- `scripts/orchestrate-worktrees.py`: tmux + worktree 기반 병렬 실행 — 잘 작동 중
- `/orchestrate`, `/multi-plan`, `/multi-execute`: 독립 워크플로우 존재
- `usage-tracker.sh`: 비용 추적 훅 존재

### 4. 결론: 기능 중복이 심각

```
ClawTeam이 해결하려는 문제:
  ├── 태스크 의존성    → Claude Code Agent Teams이 이미 제공
  ├── 에이전트 메시징   → Claude Code Agent Teams이 이미 제공
  ├── Worktree 격리   → Claude Code Agent Teams + 기존 orchestrate 이미 제공
  ├── 비용 추적       → 내장 토큰 추적 + usage-tracker.sh 이미 제공
  └── 프로세스 관리    → Agent tool이 이미 제공
```

**ClawTeam만의 차별화:**
- 웹 대시보드 (`board serve`)
- TOML 템플릿 기반 팀 런치
- 크로스 머신 지원 (SSHFS, 향후 Redis)
- agent-agnostic (Claude 외 다른 AI CLI도 지원)

**그러나:**
- v0.1.2 Alpha — 프로덕션 사용 위험
- 브릿지 레이어(19개 파일)가 양쪽 변경에 취약한 중간 계층이 됨
- Claude Code Agent Teams도 실험적이지만, Anthropic이 직접 유지보수하므로 안정성 우위

---

## 대안 제안

### Option A: ClawTeam 통합 (원래 계획)
- **장점**: 완성된 DAG/메시징/비용 인프라
- **단점**: 1일차 Alpha 패키지 의존, 19개 브릿지 파일, 기능 중복 심각
- **리스크**: 높음

### Option B: Claude Code Agent Teams 네이티브 활용 (권장)
- **장점**: 외부 의존성 없음, Anthropic 유지보수, 이미 내장
- **단점**: 아직 실험적, 웹 대시보드 없음
- **구현**: `/team` 커맨드 + TOML 템플릿만 추가 (Agent Teams API 래핑)
- **리스크**: 낮음

### Option C: 하이브리드 (관망)
- ClawTeam이 v0.3+ 안정화될 때까지 대기
- 지금은 Option B로 진행, 나중에 ClawTeam으로 백엔드 교체
- **구현**: 추상화 레이어만 얇게 만들고, 백엔드 교체 가능하게

---

## 배경

claude-craft는 25+ 도메인 에이전트와 340+ 스킬로 **"무엇을 할 수 있는가"** (두뇌)에 강하지만,
에이전트 간 조율 인프라가 부족하다.

현재 `/orchestrate`는 tmux + worktree 병렬 실행만 지원하고,
태스크 의존성, 에이전트 간 통신, 실시간 모니터링, 비용 추적이 없다.

**ClawTeam**(HKUDS)은 **"어떻게 협업하는가"** (신경계)를 제공:
- TaskStore: 의존성 DAG
- MailboxManager: 에이전트 간 메시징
- CostStore: 비용 추적
- SpawnBackend: 프로세스 관리
- WorkspaceManager: worktree 격리

**목표**: ClawTeam을 claude-craft의 조율 인프라로 통합하여,
도메인 전문성을 가진 에이전트들이 진정한 병렬로 자율 협업하는 시스템을 구축한다.

---

## 아키텍처

```
┌─────────────────────────────────────────┐
│         Claude-Craft Layer (두뇌)        │
│  agents/ skills/ commands/ rules/        │
│  agent-orchestration.md 라우팅 매트릭스    │
└──────────────────┬──────────────────────┘
                   │
┌──────────────────▼──────────────────────┐
│       Bridge Layer (새로 생성)            │
│  scripts/clawteam_bridge/                │
│  agent_mapper / plan_converter /         │
│  prompt_injector / orchestrator /        │
│  cost_bridge / template_generator        │
└──────────────────┬──────────────────────┘
                   │
┌──────────────────▼──────────────────────┐
│      ClawTeam Runtime (pip install)      │
│  TaskStore  MailboxManager  CostStore    │
│  SpawnBackend  WorkspaceManager          │
└─────────────────────────────────────────┘
```

---

## Phase 1: Foundation (설치 + 브릿지 레이어)

**목표**: ClawTeam 설치, 브릿지 모듈 생성, claude-craft 에이전트를 ClawTeam 팀 멤버로 매핑

**가치**: 기존 워크플로우 변경 없이 ClawTeam 인프라 위에서 에이전트 추적/관리 가능

### 생성 파일

| 파일 | 역할 |
|------|------|
| `pyproject.toml` | 최소 프로젝트 정의, `clawteam>=0.1.2` optional dependency |
| `scripts/clawteam_bridge/__init__.py` | 패키지 초기화, ClawTeam 설치 여부 감지 |
| `scripts/clawteam_bridge/compat.py` | ClawTeam 미설치 시 graceful fallback |
| `scripts/clawteam_bridge/agent_mapper.py` | 에이전트 .md 파싱 → ClawTeam TeamMember 변환 |
| `scripts/clawteam_bridge/prompt_injector.py` | 도메인 지식(에이전트/스킬/규칙) → 스폰 프롬프트 주입 |

### 핵심 설계

**agent_mapper.py**: 에이전트 .md 파일의 YAML frontmatter를 파싱하여 레지스트리 구축
```
.claude/agents/💻 개발/fastapi-expert-agent.md
  → AgentDef(name="fastapi-expert-agent", model="opus", category="개발")
  → TeamMember(name="fastapi-expert", agent_type="domain-expert")
```

**prompt_injector.py**: ClawTeam 스폰 시 claude-craft 지식 주입
```
ClawTeam 기본 프롬프트 (identity + task + coordination)
  + 에이전트 .md 본문 (도메인 전문성)
  + 매칭된 스킬 요약 (관련 스킬)
  + 프로젝트 규칙 (coding-style, git-workflow 등)
```

### 수정 파일

| 파일 | 변경 |
|------|------|
| `.gitignore` | `.clawteam/` 추가 |

### 호환성
- `scripts/orchestrate-worktrees.py` 변경 없음
- ClawTeam 미설치 시 `compat.py`가 `ImportError` + 설치 안내 반환

---

## Phase 2: Task Dependencies (DAG 오케스트레이션)

**목표**: plan.json에 `depends_on` 추가, ClawTeam TaskStore로 의존성 자동 해소

**가치**: "Tests는 Backend+Frontend 완료 후 실행" 같은 순차/병렬 하이브리드 워크플로우

### 확장된 plan.json 스키마 (하위 호환)

```json
{
  "session": "feature-auth",
  "use_clawteam": true,
  "budget_cents": 500,
  "workers": [
    { "name": "Backend", "task": "...", "agent": "fastapi-expert-agent" },
    { "name": "Frontend", "task": "...", "agent": "nextjs-expert-agent" },
    { "name": "Tests", "task": "...", "agent": "tdd-ralph",
      "depends_on": ["Backend", "Frontend"] }
  ]
}
```

- `use_clawteam`: 생략/false → 기존 orchestrate-worktrees.py 경로
- `depends_on`: ClawTeam TaskStore의 blocked_by로 변환
- `agent`: claude-craft 에이전트 참조 (prompt_injector로 지식 주입)

### 생성 파일

| 파일 | 역할 |
|------|------|
| `scripts/clawteam_bridge/plan_converter.py` | plan.json ↔ ClawTeam TaskStore DAG 변환 |
| `.claude/commands/team.md` | `/team` 슬래시 커맨드 |

### `/team` 커맨드

```
/team "백엔드 API + 프론트 UI + 테스트를 병렬로"  → 팀 스폰
/team --status feature-auth                       → DAG 시각화 + 상태
/team --cleanup feature-auth                      → 정리
```

### DAG 시각화 (--status)

```
Backend  [completed] $0.28 ──┐
                              ├──→ Tests [blocked] $0.00
Frontend [running]   $0.14 ──┘

Tasks: 3 total | 1 completed | 1 running | 1 blocked
Cost:  $0.42 / $5.00 budget
```

### 수정 파일

| 파일 | 변경 |
|------|------|
| `.claude/rules/common/agent-orchestration.md` | `/team`, `/team-launch` 라우팅 추가 |
| `CLAUDE.md` | `/team` 커맨드 문서화 |

---

## Phase 3: Inter-Agent Communication (에이전트 간 메시징)

**목표**: MailboxManager로 에이전트 간 직접 통신, 이벤트 기반 의존성 해소

**가치**: 에이전트가 결과 공유, 도움 요청, 완료 알림을 자율적으로 수행

### 생성 파일

| 파일 | 역할 |
|------|------|
| `scripts/clawteam_bridge/orchestrator.py` | 리더 에이전트 루프: 메시지/태스크 폴링, 스폰/언블록 |

### 통신 프로토콜

스폰된 에이전트 프롬프트에 주입:
```
## Communication Protocol
- 완료 보고: clawteam inbox send {team} leader "HANDOFF: <요약>"
- 도움 요청: clawteam inbox send {team} leader "HELP: <설명>"
- 결과 공유: clawteam inbox send {team} <peer> "RESULT: <요약>"
```

### 오케스트레이터 루프 (리더)

```python
while not all_tasks_completed():
    # 1. 메시지 처리
    messages = mailbox.receive("leader")
    for msg in messages:
        if "HELP:" in msg.content: route_to_user(msg)
        if "HANDOFF:" in msg.content: mark_completed(msg.from_agent)

    # 2. 언블록된 태스크 스폰
    for task in task_store.list_tasks(status="pending"):
        if not is_spawned(task.owner):
            spawn_with_domain_knowledge(task)

    # 3. 예산 체크 (Phase 6)
    sleep(10)
```

---

## Phase 4: Monitoring Dashboard (실시간 모니터링)

**목표**: 팀 실행 상태, 태스크 진행, 비용을 실시간으로 확인

**가치**: 10개 에이전트 동시 실행 시 단일 뷰에서 전체 상황 파악

### 접근 방식

ClawTeam 내장 기능 활용 (커스텀 대시보드 불필요):

| 모드 | 명령 | 용도 |
|------|------|------|
| tmux 타일 | `clawteam board attach <team>` | 모든 에이전트 터미널 동시 보기 |
| 웹 대시보드 | `clawteam board serve --port 8080` | 브라우저에서 원격 모니터링 |

### `/team --status` 강화

Phase 2의 DAG 시각화에 추가:
- `TaskStore.get_stats()` → 태스크 통계 (완료율, 평균 소요 시간)
- `CostStore.summary()` → 에이전트별 비용 분해
- `AgentRegistry` → 에이전트 생존 여부 (liveness)

---

## Phase 5: Templates & Automation (원커맨드 팀 런치)

**목표**: TOML 템플릿으로 자주 쓰는 팀 구성을 한 명령에 실행

**가치**: `/team-launch fullstack-dev --goal "JWT 인증"` 한 줄로 4인 팀 스폰

### 생성 파일

| 파일 | 역할 |
|------|------|
| `scripts/clawteam_bridge/template_generator.py` | TOML 파싱 + 팀 스폰 |
| `.claude/commands/team-launch.md` | `/team-launch` 슬래시 커맨드 |
| `.claude/templates/fullstack-dev.toml` | 백엔드 + 프론트엔드 + 테스터 |
| `.claude/templates/content-pipeline.toml` | 전략가 + 작성자 + SEO + 리뷰어 |
| `.claude/templates/multi-reviewer.toml` | 코드 + 아키텍처 + 보안 + 디자인 리뷰 |
| `.claude/templates/figma-to-prod.toml` | 디자인 추출 + 변환 + 구현 + 테스트 |
| `.claude/templates/planning.toml` | 리서처 + 분석가 + 전략가 |

### 템플릿 예시

```toml
# .claude/templates/fullstack-dev.toml
[team]
name = "fullstack-dev"
description = "Full-stack: architect + backend + frontend + tester"

[[agents]]
name = "backend"
claude_craft_agent = "fastapi-expert-agent"
role = "API 엔드포인트 구현"

[[agents]]
name = "frontend"
claude_craft_agent = "nextjs-expert-agent"
role = "UI 컴포넌트 구현"

[[agents]]
name = "tester"
claude_craft_agent = "tdd-ralph"
role = "테스트 작성 및 실행"
blocked_by = ["backend", "frontend"]

[budget]
max_cents = 1000
warn_at_pct = 80
```

---

## Phase 6: Cost Intelligence (예산 인식 오케스트레이션)

**목표**: 세션/에이전트별 비용 추적, 예산 경고/중단

**가치**: 멀티 에이전트 세션의 비용 폭주 방지

### 생성 파일

| 파일 | 역할 |
|------|------|
| `scripts/clawteam_bridge/cost_bridge.py` | CostStore 통합, BudgetMonitor |

### BudgetMonitor

```python
class BudgetMonitor:
    def check(self) -> BudgetStatus:
        summary = cost_store.summary()
        pct = summary.total / budget * 100
        if pct >= 100: broadcast("BUDGET EXCEEDED"); return exceeded
        if pct >= warn_pct: broadcast(f"Budget {pct}%"); return warning
        return ok
```

- Phase 3 오케스트레이터 루프에 통합
- 기존 `usage-tracker.sh`와 병행 (대체하지 않음)
- `scripts/usage-report.py`에 `--team` 플래그 추가

---

## 실행 순서 및 의존성

```
Phase 1 (Foundation)
    │
    ▼
Phase 2 (DAG Tasks)
    │
    ▼
Phase 3 (Messaging)
    │
    ├──→ Phase 4 (Monitoring)  ← 병렬 가능
    ├──→ Phase 5 (Templates)   ← 병렬 가능
    └──→ Phase 6 (Cost)        ← 병렬 가능
```

---

## 전체 파일 변경 요약

### 신규 생성 (19개)

| Phase | 파일 | 유형 |
|-------|------|------|
| 1 | `pyproject.toml` | 프로젝트 정의 |
| 1 | `scripts/clawteam_bridge/__init__.py` | 패키지 |
| 1 | `scripts/clawteam_bridge/compat.py` | 호환성 |
| 1 | `scripts/clawteam_bridge/agent_mapper.py` | 에이전트 매핑 |
| 1 | `scripts/clawteam_bridge/prompt_injector.py` | 프롬프트 주입 |
| 2 | `scripts/clawteam_bridge/plan_converter.py` | DAG 변환 |
| 2 | `.claude/commands/team.md` | 슬래시 커맨드 |
| 3 | `scripts/clawteam_bridge/orchestrator.py` | 오케스트레이터 |
| 5 | `scripts/clawteam_bridge/template_generator.py` | 템플릿 파서 |
| 5 | `.claude/commands/team-launch.md` | 슬래시 커맨드 |
| 5 | `.claude/templates/fullstack-dev.toml` | 템플릿 |
| 5 | `.claude/templates/content-pipeline.toml` | 템플릿 |
| 5 | `.claude/templates/multi-reviewer.toml` | 템플릿 |
| 5 | `.claude/templates/figma-to-prod.toml` | 템플릿 |
| 5 | `.claude/templates/planning.toml` | 템플릿 |
| 6 | `scripts/clawteam_bridge/cost_bridge.py` | 비용 관리 |

### 수정 (3개)

| Phase | 파일 | 변경 내용 |
|-------|------|-----------|
| 1 | `.gitignore` | `.clawteam/` 추가 |
| 2 | `.claude/rules/common/agent-orchestration.md` | `/team`, `/team-launch` 라우팅 추가 |
| 2 | `CLAUDE.md` | `/team` 커맨드 문서화 |

### 변경하지 않는 파일 (호환성 보장)

| 파일 | 이유 |
|------|------|
| `scripts/orchestrate-worktrees.py` | 기존 `/orchestrate` 유지 |
| `.claude/commands/orchestrate.md` | 기존 워크플로우 보존 |
| `.claude/commands/multi-plan.md` | 독립 워크플로우 |
| `.claude/commands/multi-execute.md` | 독립 워크플로우 |
| 모든 에이전트 .md 파일 | 읽기 전용 (브릿지가 파싱만 함) |
| 모든 스킬 .md 파일 | 읽기 전용 |

---

## 검증 계획

### Phase 1
```bash
pip install clawteam
python -c "from scripts.clawteam_bridge import agent_mapper; print(agent_mapper.list_agents())"
```

### Phase 2
```bash
/team "Backend API + Frontend UI + Tests (depends on both)"
/team --status <session>  # DAG 시각화 확인
/team --cleanup <session>
```

### Phase 3
- 에이전트 스폰 후 `clawteam inbox peek leader` → HANDOFF 메시지 수신 확인
- blocked 태스크가 선행 완료 시 자동 스폰 확인

### Phase 4
- `clawteam board serve --port 8080` → 브라우저에서 대시보드 확인

### Phase 5
```bash
/team-launch fullstack-dev --goal "JWT 인증 시스템 구현"
# 4개 에이전트 자동 스폰 + 의존성 순서 확인
```

### Phase 6
- `budget_cents: 100` 설정 → 초과 시 에이전트 중단 확인

---

## 리스크 & 고려사항

### 기술적 리스크
- **ClawTeam 성숙도**: v0.1.2 — API 변경 가능성 높음
- **Claude Code 제약**: 서브에이전트가 `clawteam` CLI를 직접 호출할 수 있는지 검증 필요
- **worktree 충돌**: ClawTeam WorkspaceManager와 기존 orchestrate-worktrees.py의 worktree 관리 중복

### 복잡도
- 6 Phase, 19개 신규 파일 — 단계적 검증 없이 진행하면 디버깅 어려움
- 브릿지 레이어가 두 시스템의 변경에 모두 영향받는 취약 계층이 될 수 있음

### 대안 검토 필요
- ClawTeam 없이 기존 `/orchestrate` + Claude Code `Task`/`SendMessage` API만으로 충분한가?
- TaskStore DAG를 자체 구현하는 것이 외부 의존성보다 나은가?
