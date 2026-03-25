# Harness Evolution Plan: Anthropic GAN-Loop 패턴 도입

> **출처**: [Anthropic Engineering — Harness Design for Long-Running Apps](https://www.anthropic.com/engineering/harness-design-long-running-apps)
> **작성일**: 2026-03-25
> **목적**: Anthropic이 제시한 Generator-Evaluator 패턴을 claude-craft에 도입하여 장기 실행 작업의 품질과 자율성을 높인다

---

## 1. Executive Summary

Anthropic은 장기 실행 에이전트(4시간+, $124-200/세션)에서 **3가지 핵심 문제**를 발견하고 해법을 제시했다:

| 문제 | Anthropic 해법 | claude-craft 현재 상태 |
|------|---------------|----------------------|
| 자체 평가 편향 | 독립 Evaluator 에이전트 (GAN식) | `/verify`는 정적 검증만. 라이브 QA 없음 |
| 컨텍스트 불안감 | 컨텍스트 리셋 + 구조화된 핸드오프 | worktree 병렬화로 자연 리셋되나, 단일 에이전트 장기작업에선 미대응 |
| 표면적 검증 | 반복적 Evaluator 튜닝 + 하드 임계값 | eval-harness 프레임워크 있으나 도메인별 루브릭 부재 |

**도입 전략**: 기존 아키텍처(25+ 에이전트, DAG 오케스트레이션, handoff.md)를 유지하면서 Anthropic 패턴을 **4단계로 점진 도입**한다.

---

## 2. 현재 아키텍처 vs Anthropic 아키텍처

### 2.1 아키텍처 비교 다이어그램

```
[Anthropic 3-에이전트 모델]

  User (1-4문장)
       │
       ▼
  ┌─────────┐
  │ Planner │ ─── 제품 스펙 + 스프린트 분해
  └────┬────┘
       │ spec.md
       ▼
  ┌───────────┐     contract.md      ┌───────────┐
  │ Generator │ ◄──────────────────► │ Evaluator │
  │ (구현)     │     feedback.md      │ (QA)      │
  └───────────┘                      └───────────┘
       │                                   │
       │ 코드 생성                          │ Playwright 라이브 테스트
       │                                   │ 스크린샷 + 상호작용
       ▼                                   ▼
  스프린트 N 완료 ◄─── 합격/불합격 ────► 스프린트 N 재작업
```

```
[claude-craft 현재 모델]

  User (자연어)
       │
       ▼
  ┌──────────────────┐
  │ agent-orchestration│ ─── 라우팅 매트릭스
  └────────┬─────────┘
           │
    ┌──────┴──────────────────────┐
    ▼                             ▼
  단일 에이전트              /team (DAG)
  (fastapi, nextjs, etc.)    ┌───────────┐
                             │ plan.json │
                             └─────┬─────┘
                           ┌───────┼───────┐
                           ▼       ▼       ▼
                        Worker1 Worker2 Worker3
                        (worktree + tmux)
                           │       │       │
                           ▼       ▼       ▼
                        handoff  handoff  handoff
                          .md      .md      .md
                                   │
                                   ▼
                              /verify (정적)
```

### 2.2 상세 Gap 분석

#### Gap A: 독립 Evaluator 부재 (Critical)

**Anthropic의 발견**:
> "에이전트에게 자신의 작업을 평가하라고 하면, 자신감 있게 칭찬하는 경향이 있다"
> "Claude는 기본 상태에서 QA 에이전트로 좋지 않다 — 합법적인 문제를 발견한 후 크지 않다고 자기 설득한다"

**claude-craft 현재 상태**:
- `/verify`: 빌드/타입/린트/테스트/보안/diff 리뷰 — 모두 **정적 검증**
- `quality-gate.sh`: 파일 저장 시 자동 포맷팅 — **실시간이지만 표면적**
- `review-orchestrator`: 코드/아키텍처/보안 리뷰 — **코드 읽기 기반, 라이브 동작 검증 아님**
- `figma-to-prod.toml`의 `Visual-Tester`: 시각적 검증 명세는 있지만 **Playwright 통합 없음**

**Gap**: 구현된 코드가 **실제로 브라우저에서 작동하는지** 확인하는 독립 에이전트가 없다.

#### Gap B: 스프린트 계약 협상 부재 (Major)

**Anthropic의 패턴**:
```
Generator: "이걸 만들겠습니다. 검증 기준은 이것입니다."
Evaluator: "기준이 불충분합니다. 이 케이스도 추가하세요."
→ 합의될 때까지 반복
→ 합의된 계약으로 구현 시작
```

**claude-craft 현재 상태**:
- `/team`에서 task를 **일방적으로 할당** (plan.json → 실행)
- 워커 간 사전 협상 과정 없음
- `success_criteria`가 plan.json 스키마에 없음
- `handoff.md`는 **완료 후** 결과 전달용 (사전 합의용이 아님)

**Gap**: "무엇을 만들지"는 정의하지만, "어떻게 검증할지"를 사전에 합의하지 않는다.

#### Gap C: 컨텍스트 리셋 전략 부재 (Major)

**Anthropic의 발견**:
> "컨텍스트 리셋이 컨텍스트 컴팩션보다 우월하다"
> "컨텍스트 불안감 — 모델이 컨텍스트 한계에 가까워지면 조기 종료하려는 경향"

**claude-craft 현재 상태**:
- `/orchestrate`의 워커들은 별도 프로세스 → **자연스러운 컨텍스트 리셋** (강점)
- 단일 에이전트 장기 작업(planning-agent 75스킬, figma 변환 등)은 **컴팩션에 의존**
- `/save-session` + `/resume-session`은 수동 리셋 — **자동화되지 않음**
- `autonomous-loops` 스킬에 리셋 패턴이 문서화되어 있으나 **구현체 없음**

**Gap**: 단일 에이전트가 장시간 작업할 때 **자동 컨텍스트 리셋 + 핸드오프** 메커니즘이 없다.

#### Gap D: 도메인별 평가 루브릭 부재 (Moderate)

**Anthropic의 패턴**:
```
UI/디자인 평가 4축:
- Design Quality (35%): 통합된 전체로 느껴지는가
- Originality (35%): AI 생성 패턴에서 벗어났는가
- Craft (15%): 기술적 실행 품질
- Functionality (15%): 사용성

→ 가중치를 주관적 기준에 두어 "전형적 AI 생성물" 탈피
```

**claude-craft 현재 상태**:
- `eval-harness`: 범용 pass/fail + pass@k 프레임워크
- `/review`: 멀티 LLM 리뷰에 4가지 기준(clarity/completeness/practicality/consistency)
- 도메인 특화(UI, API, 콘텐츠) 루브릭은 없음

**Gap**: 범용 평가 프레임워크는 있으나, 도메인별로 **무엇이 "좋은" 결과인지** 정의되지 않았다.

#### Gap E: 반복 정제 루프 미통합 (Moderate)

**Anthropic의 패턴**:
```
for 5..15 iterations:
    생성 → Playwright 상호작용 → 스크린샷 → 채점 → 피드백 → 재생성
```

**claude-craft 현재 상태**:
- `tdd-loop-agent`: 테스트 100% 패스까지 루프 (코드용)
- `figma-to-nextjs-ralph-pure`: 자기참조 루프 (디자인용) — 하지만 **자체 평가**
- `Continuous PR Loop`: CI 통과까지 루프 — CI가 Evaluator 역할
- **라이브 UI 정제 루프**: 없음

**Gap**: 코드와 CI에 대한 루프는 있으나, **UI/UX 정제 루프**(라이브 스크린샷 비교 → 피드백 → 재생성)가 없다.

---

## 3. 도입 계획 (4단계)

### Phase 1: Evaluator 에이전트 신설 (Week 1-2)

**목표**: 독립적인 라이브 QA 에이전트를 만들어 자체 평가 편향을 제거한다.

#### 3.1.1 `live-qa-agent` 신설

```
.claude/agents/💻 개발/live-qa-agent.md
```

**역할**: Playwright MCP를 사용하여 구현된 코드를 실제 브라우저에서 테스트

**핵심 설계**:
```markdown
# Live QA Agent

## 입력
- success_criteria: 검증해야 할 기준 목록
- app_url: 테스트할 애플리케이션 URL
- reference_screenshots: (선택) 비교할 원본 디자인 스크린샷

## 도구
- mcp__playwright__browser_navigate
- mcp__playwright__browser_click
- mcp__playwright__browser_fill_form
- mcp__playwright__browser_take_screenshot
- mcp__playwright__browser_snapshot
- mcp__playwright__browser_evaluate

## 검증 프로세스
1. 앱 시작 확인 (URL 접속 가능 여부)
2. success_criteria 순회:
   - 각 기준에 대해 Playwright로 실제 상호작용
   - 스크린샷 촬영
   - 결과 판정 (PASS/FAIL + 상세 사유)
3. 종합 QA 리포트 생성

## 출력
- qa-report.md:
  - 각 기준별 PASS/FAIL
  - 실패 항목의 상세 버그 리포트
  - 스크린샷 경로
  - 재작업 필요 여부 판정
```

**안티패턴 방지 (Anthropic 교훈 적용)**:
```markdown
## QA 판정 규칙

1. FAIL에 대한 자기 설득 금지
   - 문제를 발견했으면 절대 "크지 않다"고 재평가하지 않는다
   - 발견 즉시 FAIL로 기록하고 넘어간다

2. 표면적 테스트 금지
   - 페이지 로딩 확인만으로 PASS 불가
   - 반드시 사용자 플로우를 끝까지 수행한다
   - 에지 케이스도 테스트한다 (빈 입력, 긴 텍스트, 특수문자)

3. 하드 임계값
   - 한 개라도 critical FAIL이면 → 전체 FAIL (재작업)
   - major FAIL 2개 이상이면 → 전체 FAIL
   - minor FAIL만 있으면 → PASS with warnings
```

#### 3.1.2 `plan.json` 스키마 확장

기존:
```json
{
  "workers": [
    { "name": "Backend", "task": "..." }
  ]
}
```

확장:
```json
{
  "workers": [
    {
      "name": "Backend",
      "task": "...",
      "success_criteria": [
        "POST /auth/login이 유효한 credentials로 JWT 토큰을 반환한다",
        "잘못된 비밀번호로 401 응답을 반환한다",
        "만료된 토큰으로 refresh 요청 시 새 토큰을 발급한다",
        "토큰 없이 보호된 엔드포인트 접근 시 401을 반환한다"
      ],
      "eval_type": "api"
    },
    {
      "name": "Frontend",
      "task": "...",
      "success_criteria": [
        "로그인 폼에 이메일과 비밀번호를 입력하고 제출할 수 있다",
        "로그인 성공 시 대시보드로 리다이렉트된다",
        "로그인 실패 시 에러 메시지가 표시된다",
        "로그아웃 버튼 클릭 시 로그인 페이지로 이동한다"
      ],
      "eval_type": "ui"
    }
  ]
}
```

#### 3.1.3 `orchestrate-worktrees.py` 수정

QA 워커를 자동 주입하는 로직 추가:

```python
def inject_qa_worker(plan: dict) -> dict:
    """success_criteria가 있는 워커들에 대해 QA 워커를 자동 생성."""
    workers_with_criteria = [
        w for w in plan["workers"]
        if w.get("success_criteria")
    ]
    if not workers_with_criteria:
        return plan

    qa_worker = {
        "name": "QA",
        "task": build_qa_task(workers_with_criteria),
        "depends_on": [w["name"] for w in workers_with_criteria],
    }
    plan["workers"].append(qa_worker)
    return plan
```

#### 3.1.4 `fullstack-dev.toml` 업데이트

```toml
[[agents]]
name = "QA"
role = "라이브 QA — Playwright로 기능 검증 및 버그 리포트"
blocked_by = ["Backend", "Frontend"]
task_template = """
구현된 기능을 Playwright로 라이브 테스트하세요.

## 검증 대상
- 선행 워커들의 handoff.md에서 구현 내용 확인
- 각 워커의 success_criteria를 기준으로 테스트

## 판정 기준
- critical FAIL 1개 → 전체 FAIL
- major FAIL 2개+ → 전체 FAIL
- 문제 발견 시 즉시 FAIL로 기록 (자기 설득 금지)

## 산출물
- qa-report.md: 기준별 PASS/FAIL + 상세 버그 리포트
- 재작업 필요 항목 목록 (워커별로 분류)
"""
```

#### 3.1.5 기존 `figma-to-prod.toml`의 `Visual-Tester` 강화

현재의 추상적인 "시각적 검증"을 Playwright 기반 구체적 검증으로 교체:

```toml
[[agents]]
name = "Visual-Tester"
role = "Playwright 기반 시각적 + 기능적 검증"
blocked_by = ["Implementer"]
task_template = """
{goal} 구현의 시각적/기능적 품질을 검증하세요.

## 도구
Playwright MCP를 사용하여:
1. 구현된 페이지를 브라우저에서 열기
2. 반응형 뷰포트 테스트 (375px, 768px, 1440px)
3. 각 컴포넌트 스크린샷 촬영
4. 사용자 인터랙션 테스트 (클릭, 호버, 입력)

## 평가 기준 (Anthropic 4축)
- Design Quality (35%): 색상/타이포/레이아웃 일관성, 통합된 느낌
- Originality (35%): 템플릿/기본값/AI 패턴 탈피 여부
- Craft (15%): 간격, 정렬, 대비, 계층 구조
- Functionality (15%): 주요 플로우 완료 가능 여부

## 판정
- 각 축 1-10 점수, 가중 평균 7.0 이상이면 PASS
- Design Quality 또는 Originality가 5 미만이면 무조건 FAIL

## 산출물
- visual-qa-report.md: 축별 점수 + 상세 피드백
- 스크린샷 (before/after 비교용)
- 재작업 지시사항 (FAIL 시)
"""
```

---

### Phase 2: 스프린트 계약 협상 도입 (Week 2-3)

**목표**: 구현 전에 Generator와 Evaluator가 성공 기준을 합의하는 프로토콜을 추가한다.

#### 3.2.1 계약 협상 프로토콜

```
[현재]
plan.json 생성 → 확인 → 실행 → handoff.md

[개선]
plan.json 생성 → 확인 → 계약 협상 → 합의 → 실행 → 검증
```

**파일 기반 협상 프로토콜**:

```
.orchestration/{session}/
├── plan.json                    # 전체 계획
├── contracts/
│   ├── Backend-proposal.md      # Generator 제안
│   ├── Backend-review.md        # Evaluator 리뷰
│   ├── Backend-contract.md      # 최종 합의 계약
│   ├── Frontend-proposal.md
│   ├── Frontend-review.md
│   └── Frontend-contract.md
├── workers/
│   ├── Backend/
│   │   ├── task.md
│   │   └── handoff.md
│   └── Frontend/
│       ├── task.md
│       └── handoff.md
└── qa/
    └── qa-report.md
```

#### 3.2.2 계약 구조

```markdown
# Sprint Contract: Backend — JWT 인증 API

## 구현 범위
- POST /auth/login — JWT 토큰 발급
- POST /auth/refresh — 토큰 갱신
- GET /auth/me — 현재 사용자 정보

## 성공 기준 (Evaluator 합의)
| ID | 기준 | 검증 방법 | 중요도 |
|----|------|----------|--------|
| C1 | 유효한 credentials로 로그인 시 JWT 반환 | API 호출 | critical |
| C2 | 잘못된 비밀번호 → 401 | API 호출 | critical |
| C3 | 만료된 토큰 → refresh 성공 | API 호출 | major |
| C4 | 토큰 없이 보호 엔드포인트 → 401 | API 호출 | critical |
| C5 | 응답 시간 < 500ms | 성능 측정 | minor |

## 제외 사항
- 소셜 로그인 (다음 스프린트)
- 비밀번호 재설정 (다음 스프린트)

## 합의일시
2026-03-25T14:30:00Z
```

#### 3.2.3 `/team` 커맨드 확장

Step 3 (Decompose) 이후에 계약 협상 단계 추가:

```
Step 3: Decompose → Workers
Step 3.5: Contract Negotiation (NEW)
  - 각 워커의 task에서 success_criteria 추출
  - QA 워커가 criteria를 리뷰
  - 부족한 기준 보완 제안
  - 합의된 contract.md 생성
Step 4: Generate Plan (with contracts)
```

**구현 방식**: `/team` 실행 시 `--negotiate` 플래그로 활성화 (기본 비활성화로 기존 동작 유지)

```bash
/team "JWT 인증 구현" --negotiate    # 계약 협상 포함
/team "JWT 인증 구현"                # 기존 동작 (빠른 실행)
```

---

### Phase 3: 컨텍스트 리셋 루프 구현 (Week 3-4)

**목표**: 단일 에이전트 장기 작업에서 자동 컨텍스트 리셋 + 구조화된 핸드오프를 구현한다.

#### 3.3.1 문제 정의

현재 **단일 에이전트 장기 작업** 시나리오:
- `planning-agent`: 8단계 75스킬 순차 실행 → 컨텍스트 누적
- `figma-to-nextjs`: 8페이즈 변환 → 컨텍스트 누적
- `marketing-agent`: 리서치 → 전략 → 카피 → 캠페인 → 컨텍스트 누적

이들은 `/orchestrate`로 병렬화하기 어렵다 (순차 의존성).

#### 3.3.2 Sprint-Reset 패턴

```
autonomous-loops 스킬의 새 패턴: "Sprint-Reset Loop"

Sprint 1 (새 Claude 인스턴스):
  입력: sprint-1-input.md (초기 요구사항)
  실행: 작업 수행
  출력: sprint-1-output.md (결과 + 다음 스프린트 입력)
  → 인스턴스 종료 (컨텍스트 완전 리셋)

Sprint 2 (새 Claude 인스턴스):
  입력: sprint-1-output.md (이전 결과)
  실행: 이어서 작업
  출력: sprint-2-output.md
  → 인스턴스 종료

... 반복 ...

최종 Sprint:
  입력: sprint-N-output.md
  실행: 마무리 + 통합
  출력: final-output.md
```

#### 3.3.3 구현: `scripts/sprint-reset-loop.sh`

```bash
#!/bin/bash
# Sprint-Reset Loop — 컨텍스트 리셋으로 장기 작업 품질 유지
#
# Usage:
#   bash scripts/sprint-reset-loop.sh \
#     --sprints 5 \
#     --initial-prompt "marketing-strategy.md" \
#     --session "jwt-auth"

SESSION="$1"
MAX_SPRINTS="${2:-5}"
INITIAL_INPUT="$3"

WORK_DIR=".orchestration/${SESSION}/sprints"
mkdir -p "$WORK_DIR"

# Sprint 1: 초기 입력
cp "$INITIAL_INPUT" "$WORK_DIR/sprint-0-output.md"

for i in $(seq 1 "$MAX_SPRINTS"); do
  PREV_OUTPUT="$WORK_DIR/sprint-$((i-1))-output.md"
  CURRENT_OUTPUT="$WORK_DIR/sprint-${i}-output.md"

  # 스프린트 프롬프트 구성
  PROMPT=$(cat <<EOF
이전 스프린트 결과를 이어받아 작업합니다.

## 이전 스프린트 결과
$(cat "$PREV_OUTPUT")

## 이번 스프린트 지시
Sprint ${i}/${MAX_SPRINTS}을 수행하세요.
완료 후 다음 스프린트에 필요한 컨텍스트를 구조화하여 출력하세요.

## 출력 형식
### 완료된 작업
(이번 스프린트에서 완료한 것)

### 생성/수정된 파일
(파일 경로와 변경 내용)

### 다음 스프린트 입력
(다음 스프린트가 알아야 할 모든 컨텍스트)

### 남은 작업
(아직 완료하지 못한 것)
EOF
  )

  echo "=== Sprint ${i}/${MAX_SPRINTS} ==="
  claude -p "$PROMPT" --output-file "$CURRENT_OUTPUT"

  # 남은 작업이 없으면 조기 종료
  if grep -q "남은 작업.*없음\|남은 작업.*완료" "$CURRENT_OUTPUT"; then
    echo "=== All sprints completed at Sprint ${i} ==="
    break
  fi
done
```

#### 3.3.4 `autonomous-loops` 스킬에 패턴 추가

기존 6개 패턴에 7번째 패턴 추가:

```markdown
### 7. Sprint-Reset Loop (컨텍스트 리셋)
```bash
bash scripts/sprint-reset-loop.sh {session} {max_sprints} {initial_input}
```
- 각 스프린트가 독립 Claude 인스턴스에서 실행
- 이전 결과를 파일로 전달 (구조화된 핸드오프)
- 컨텍스트 불안감 제거 — 항상 깨끗한 시작
- 순차 의존성 작업에 적합 (기획, 마이그레이션 등)
- **주의**: 각 스프린트 시작에 토큰 오버헤드 발생
```

의사결정 매트릭스 업데이트:
```
작업이 독립적으로 분할 가능한가?
├── Yes → (기존 트리)
└── No → 반복 개선이 필요한가?
    ├── Yes → CI가 있는가?
    │   ├── Yes → Continuous PR Loop
    │   └── No → 컨텍스트 윈도우 초과 예상?    ← NEW
    │       ├── Yes → Sprint-Reset Loop
    │       └── No → Persistent REPL + /verify
    └── No → 단순 구현 후 De-Sloppify
```

---

### Phase 4: 도메인별 Eval 루브릭 + 정제 루프 (Week 4-5)

**목표**: eval-harness에 도메인 특화 루브릭을 추가하고, UI/디자인 정제 루프를 구현한다.

#### 3.4.1 도메인별 Eval 프리셋

```
.claude/evals/
├── presets/
│   ├── ui-design.md          # UI/디자인 평가 루브릭
│   ├── api-backend.md        # API 백엔드 평가 루브릭
│   ├── content-quality.md    # 콘텐츠 품질 평가 루브릭
│   └── fullstack-app.md      # 풀스택 앱 종합 루브릭
```

**UI/디자인 루브릭** (Anthropic 4축 기반):

```markdown
# UI/Design Eval Preset

## 평가 축 (가중치)

### Design Quality (35%)
통합된 전체로 느껴지는가? 색상, 타이포그래피, 레이아웃이 일관된 무드를 만드는가?

| 점수 | 기준 |
|------|------|
| 9-10 | 전문 디자이너 수준의 일관성, 독자적 무드 |
| 7-8 | 대부분 일관적, 사소한 불일치 |
| 5-6 | 기본적 일관성은 있지만 "조립된" 느낌 |
| 3-4 | 불일치가 눈에 띄고 산만함 |
| 1-2 | 색상/폰트/레이아웃이 충돌 |

### Originality (35%)
사용자 정의 결정의 증거가 있는가? 템플릿/라이브러리 기본값/AI 생성 패턴?

| 점수 | 기준 |
|------|------|
| 9-10 | 독창적 레이아웃, 커스텀 그래픽, 독특한 인터랙션 |
| 7-8 | 기본 컴포넌트를 창의적으로 조합 |
| 5-6 | shadcn/ui 기본값에 약간의 커스텀 |
| 3-4 | 전형적인 AI 생성 패턴 (centered hero, card grid) |
| 1-2 | 기본 템플릿과 구분 불가 |

### Craft (15%)
기술적 실행 — 타이포그래피 계층, 간격 일관성, 색상 조화, 명암 비율

| 점수 | 기준 |
|------|------|
| 9-10 | 완벽한 정렬, 8px 그리드, WCAG AA 대비 |
| 7-8 | 대부분 정확, 미세한 간격 불일치 |
| 5-6 | 눈에 띄는 정렬 오류 2-3곳 |
| 3-4 | 간격/정렬이 체계 없음 |
| 1-2 | 기본적인 CSS 문제 (overflow, z-index) |

### Functionality (15%)
사용자가 인터페이스를 이해하고 주요 작업을 완료할 수 있는가?

| 점수 | 기준 |
|------|------|
| 9-10 | 모든 플로우 완벽, 에지 케이스 처리, 로딩/에러 상태 |
| 7-8 | 주요 플로우 작동, 사소한 UX 문제 |
| 5-6 | 주요 플로우 작동하나 예외 처리 부족 |
| 3-4 | 일부 핵심 기능 미작동 |
| 1-2 | 주요 플로우 불가 |

## 합격 기준
- 가중 평균 ≥ 7.0: PASS
- Design Quality 또는 Originality < 5: FAIL (가중 평균 무관)
- Functionality < 3: FAIL (사용 불가)
```

**API 백엔드 루브릭**:

```markdown
# API Backend Eval Preset

## 평가 축

### Correctness (40%)
모든 엔드포인트가 스펙대로 작동하는가?

- 정상 요청 → 올바른 응답
- 잘못된 입력 → 적절한 에러 코드
- 경계값 → 예상대로 처리
- DB 상태 → 올바르게 변경

### Robustness (25%)
비정상 상황에서 안전하게 처리하는가?

- 중복 요청 → 멱등성
- 동시 요청 → 레이스 컨디션 없음
- 대용량 입력 → 타임아웃/페이지네이션
- 누락 필드 → 명확한 422 에러

### Security (20%)
인증/인가가 올바르게 적용되는가?

- 인증 없는 접근 → 401
- 권한 없는 접근 → 403
- SQL 인젝션/XSS → 차단
- 민감 정보 → 응답에서 제외

### Performance (15%)
응답 시간과 리소스 사용이 적절한가?

- P95 응답 시간 < 500ms
- N+1 쿼리 없음
- 불필요한 조인/풀 테이블 스캔 없음

## 합격 기준
- 가중 평균 ≥ 7.0: PASS
- Correctness critical 항목 FAIL: 전체 FAIL
- Security 이슈 발견: 전체 FAIL
```

#### 3.4.2 UI 정제 루프

Anthropic의 5-15회 반복 정제 패턴을 구현:

```
scripts/ui-refine-loop.sh

Flow:
  1. Generator가 UI 구현
  2. dev 서버 시작
  3. Evaluator가 Playwright로 접속 + 스크린샷
  4. 4축 루브릭으로 채점
  5. 점수 < 7.0이면 → 피드백 작성 → Generator에게 전달 → 2번으로
  6. 점수 ≥ 7.0이면 → PASS → 종료
  7. 최대 10회 반복 (안전장치)
```

**구현 아이디어** — 기존 `figma-to-nextjs-ralph-pure`를 확장:

현재의 "자기참조 루프"를 "독립 Evaluator 루프"로 업그레이드:

```
현재 (Ralph Pure — 자체 평가):
  Generator 생성 → Generator 자체 채점 → Generator 재생성

개선 (Ralph + Independent Evaluator):
  Generator 생성 → Evaluator 채점 (별도 인스턴스) → Generator 재생성
```

이는 기존 `/orchestrate`의 `depends_on`과 `--watch`를 활용하여 구현 가능:

```json
{
  "session": "ui-refine-loop",
  "workers": [
    {
      "name": "Generator",
      "task": "UI 구현 + dev 서버 시작",
      "iteration": 1
    }
  ],
  "watch_script": "scripts/ui-refine-watch.sh"
}
```

`--watch`가 Generator 완료를 감지하면 → Evaluator 스폰 → Evaluator 완료 시 점수 확인 → 미달이면 Generator 재스폰 (새 컨텍스트).

---

## 4. 구현 우선순위 매트릭스

| 순위 | 항목 | 임팩트 | 난이도 | 기존 자산 활용 | 예상 소요 |
|------|------|--------|--------|--------------|----------|
| **P0** | plan.json에 success_criteria 추가 | 높음 | 낮음 | orchestrate-worktrees.py | 2시간 |
| **P0** | fullstack-dev.toml에 QA 워커 추가 | 높음 | 낮음 | 기존 TOML 패턴 | 1시간 |
| **P1** | live-qa-agent 신설 | 매우 높음 | 중간 | Playwright MCP, review-orchestrator | 1일 |
| **P1** | figma-to-prod.toml Visual-Tester 강화 | 높음 | 중간 | 기존 템플릿 | 3시간 |
| **P2** | 도메인별 eval 루브릭 (UI/API) | 높음 | 낮음 | eval-harness 프레임워크 | 3시간 |
| **P2** | sprint-reset-loop.sh | 중간 | 중간 | autonomous-loops 패턴 | 4시간 |
| **P3** | 계약 협상 프로토콜 | 중간 | 높음 | /team, handoff.md | 1일 |
| **P3** | UI 정제 루프 통합 | 높음 | 높음 | ralph-pure, playwright | 2일 |
| **P4** | autonomous-loops 패턴 7번 추가 | 낮음 | 낮음 | 기존 문서 | 30분 |
| **P4** | 비용/시간 추적 개선 | 낮음 | 중간 | usage-tracker.sh | 3시간 |

---

## 5. 리스크 및 완화 전략

### 5.1 비용 증가 리스크

**Anthropic 사례**: 단일 에이전트 $9 → 전체 하네스 $200 (22배)

**완화**:
- QA 워커는 `haiku` 모델 사용 가능 (채점은 상대적으로 단순)
- `--negotiate` 플래그로 계약 협상은 **선택적** 활성화
- Sprint-Reset 루프의 최대 반복 횟수 제한 (기본 5회)
- 기존 `/verify`가 이미 정적 검증을 커버 → QA는 라이브 검증에만 집중

### 5.2 오버엔지니어링 리스크

**Anthropic의 교훈**:
> "모든 하네스 성분은 모델이 독립적으로 수행할 수 없다는 가정을 인코딩한다. 이 가정들은 스트레스 테스트할 가치가 있다"
> "더 나은 모델은 일부 스캐폴딩을 불필요하게 만들 수 있다"

**완화**:
- 각 Phase 도입 후 **A/B 비교** 수행 (하네스 有 vs 無)
- 모델 업그레이드 시 각 성분의 필요성 재검증
- 불필요해진 성분은 과감히 제거 (Anthropic도 Opus 4.6에서 스프린트 구조 간소화)

### 5.3 실행 시간 증가 리스크

**Anthropic 사례**: 20분 → 6시간 (풀스택 앱)

**완화**:
- 기존 DAG 병렬화가 이미 강점 — Generator와 QA를 제외한 워커들은 병렬 실행
- QA는 모든 워커 완료 후 1회만 실행 (매 스프린트가 아님)
- `/team`의 기본 동작은 변경 없음 — 새 기능은 opt-in

### 5.4 Playwright MCP 의존성 리스크

- Playwright MCP 서버가 비활성화된 환경에서는 live-qa-agent가 작동 불가
- **완화**: QA 에이전트가 Playwright 없이도 API 테스트(curl/httpie)로 폴백

---

## 6. 성공 지표

### 6.1 정량적 지표

| 지표 | 현재 (예상) | 목표 | 측정 방법 |
|------|------------|------|----------|
| 장기 작업 완성도 | ~60% (자체 평가) | 85%+ (독립 평가) | QA 리포트의 success_criteria 통과율 |
| 재작업 횟수 | 측정 안됨 | < 2회/세션 | QA FAIL → 재구현 횟수 추적 |
| 라이브 버그 발견율 | 0 (정적만) | 80%+ | Playwright가 발견한 버그 / 전체 버그 |
| eval pass@1 | 측정 안됨 | > 70% | eval-harness 결과 |

### 6.2 정성적 지표

- Generator의 자체 평가 vs Evaluator 평가의 **불일치율** 추적
  - 불일치가 높을수록 독립 Evaluator의 가치가 높음
- 계약 협상에서 추가된 기준이 실제 버그를 잡는 비율
- Sprint-Reset 루프에서 각 스프린트의 품질 변화 추이

---

## 7. 단계별 검증 계획

### Phase 1 검증 (Evaluator 도입 후)

**테스트 시나리오**: 동일한 풀스택 작업을 두 가지 방식으로 실행

```
A: /team "TODO 앱 구현"                    (기존 — QA 없음)
B: /team "TODO 앱 구현" (QA 워커 포함)      (개선 — QA 있음)
```

**비교 항목**:
- A에서 "완료"라고 판단한 시점의 실제 작동 상태
- B에서 QA가 발견한 버그 수
- 최종 결과물의 기능 완성도 차이

### Phase 2 검증 (계약 협상 도입 후)

**테스트**: `/team "채팅 앱 구현" --negotiate` vs `/team "채팅 앱 구현"`

- 계약 협상에서 추가된 기준이 실제 누락을 방지했는지
- 협상에 소요된 시간 대비 재작업 감소 효과

### Phase 3 검증 (Sprint-Reset 도입 후)

**테스트**: planning-agent로 동일 기획 작업을 두 방식으로 실행

- 컴팩션 모드 vs Sprint-Reset 모드
- 후반부(Phase 6-8) 산출물 품질 비교
- 컨텍스트 윈도우 사용량 추적

---

## 8. 장기 비전: 하네스 자동 진화

Anthropic의 핵심 통찰:
> "모델이 개선되면서 흥미로운 하네스 조합의 공간이 축소되지 않는다. 대신 움직인다."

**claude-craft 적용**:

```
/skill-audit 주기적 실행 → 각 하네스 성분의 ROI 측정
→ ROI 낮은 성분 제거 (모델이 자체 해결 가능해진 경우)
→ 새로운 가능성 탐색 (모델 능력 확장으로 가능해진 패턴)
```

예시:
- Opus 5가 컨텍스트 불안감을 해결하면 → Sprint-Reset 제거
- Opus 5가 자체 평가를 정확히 하면 → 독립 Evaluator 간소화
- 새 모델이 멀티모달 비교에 강해지면 → 시각적 정제 루프 강화

---

## 부록 A: 파일 변경 목록

### 신규 생성

| 파일 | 설명 |
|------|------|
| `.claude/agents/💻 개발/live-qa-agent.md` | 라이브 QA 에이전트 |
| `.claude/evals/presets/ui-design.md` | UI/디자인 평가 루브릭 |
| `.claude/evals/presets/api-backend.md` | API 백엔드 평가 루브릭 |
| `.claude/evals/presets/content-quality.md` | 콘텐츠 평가 루브릭 |
| `scripts/sprint-reset-loop.sh` | 컨텍스트 리셋 루프 스크립트 |

### 수정

| 파일 | 변경 내용 |
|------|----------|
| `scripts/orchestrate-worktrees.py` | success_criteria 필드 지원, QA 워커 자동 주입 |
| `.claude/templates/fullstack-dev.toml` | QA 워커 추가 |
| `.claude/templates/figma-to-prod.toml` | Visual-Tester Playwright 통합 |
| `.claude/skills/autonomous-loops/SKILL.md` | Sprint-Reset 패턴 추가 |
| `.claude/skills/eval-harness/SKILL.md` | 도메인별 프리셋 참조 추가 |
| `.claude/commands/team.md` | --negotiate 플래그 지원 |
| `.claude/rules/common/agent-orchestration.md` | live-qa-agent 라우팅 추가 |

---

## 부록 B: Anthropic vs claude-craft 최종 비교

| 차원 | Anthropic | claude-craft (현재) | claude-craft (개선 후) |
|------|-----------|--------------------|-----------------------|
| 에이전트 수 | 3 (고정) | 25+ (도메인별) | 26+ (QA 추가) |
| 병렬 실행 | 순차 | DAG + worktree + tmux | 유지 + QA 통합 |
| 평가 독립성 | 독립 Evaluator | 자체 평가 | 독립 Evaluator |
| 라이브 QA | Playwright | 없음 | Playwright MCP |
| 계약 협상 | 파일 기반 | 없음 | 파일 기반 (opt-in) |
| 컨텍스트 관리 | 리셋 | 컴팩션 | 리셋 + 컴팩션 선택 |
| 평가 기준 | 4축 도메인별 | 범용 pass/fail | 도메인별 루브릭 |
| 정제 루프 | 5-15회 자동 | TDD만 | UI/API 포함 |
| 비용 최적화 | $124-200 | worktree 분산 | 유지 + haiku QA |
| 멀티 LLM | Claude만 | Claude+Gemini+Codex | 유지 |
| 도메인 범위 | 코딩/UI | 기획/법무/재무/마케팅/콘텐츠 | 유지 |
