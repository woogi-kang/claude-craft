# Claude Code 2.0 완벽 활용 가이드
## AI 시대, 개발 생산성을 폭발시키는 방법

> **발표자**: Woogi (Flutter Tech Lead)  
> **대상**: 개발팀 전체  
> **목표**: Claude Code의 고급 기능을 활용하여 팀 생산성 2-3배 향상

---

## 📋 목차

1. [오프닝: 왜 Claude Code인가](#part-1-오프닝-왜-claude-code인가)
2. [Context Engineering: 토큰의 경제학](#part-2-context-engineering-토큰의-경제학)
3. [병렬 Sub-agents: 시간을 사는 방법](#part-3-병렬-sub-agents-시간을-사는-방법)
4. [Skills & Commands: 팀 지식의 자산화](#part-4-skills--commands-팀-지식의-자산화)
5. [MCP 통합: 개발 생태계 연결](#part-5-mcp-통합-개발-생태계-연결)
6. [실전 워크플로우](#part-6-실전-워크플로우)
7. [AI 시대의 마인드셋](#part-7-ai-시대의-마인드셋)
8. [액션 아이템 & 마무리](#part-8-액션-아이템--마무리)

---

## Part 1: 오프닝 - 왜 Claude Code인가

### 🎯 오늘의 목표

> "이 발표가 끝나면, 여러분의 개발 속도가 2-3배 빨라질 것입니다."

### 우리 팀의 변화

```
Before Claude Code (2024 초):
├─ 코드 작성: 개발자 100%
├─ 코드 리뷰: 수동
└─ 문서화: "나중에..."

After Claude Code (2024 말~현재):
├─ 코드 작성: LLM 80% + 개발자 20% (감독/수정)
├─ 코드 리뷰: 자동화 + 인간 최종 검토
└─ 문서화: 코드와 동시 생성
```

### Opus 4.5를 선택한 이유

| 항목 | Opus 4.5 | 경쟁 모델 |
|------|----------|----------|
| **속도** | 빠른 피드백 루프 ✅ | 상대적으로 느림 |
| **의도 감지** | 맥락 파악 탁월 ✅ | 지시 무시 경향 |
| **페어 프로그래밍** | 협업적 대화 ✅ | 일방적 실행 |
| **지식 컷오프** | May 2025 ✅ | 더 오래됨 |

### 핵심 인사이트

```
빠른 피드백 루프 → 진전이 체감됨 → 동기부여 → 더 많은 시도 → 생산성 폭발
```

---

## Part 2: Context Engineering - 토큰의 경제학

### Context Window란?

```
┌─────────────────────────────────────────────────────────────┐
│                    Context Window (200K tokens)             │
├─────────────────────────────────────────────────────────────┤
│ User: "커피숍 랜딩페이지 만들어줘"                            │
│ Assistant: [tool_call: web_search(...)]                     │
│ Tool result: [검색 결과]              ← ~1.5K tokens 추가    │
│ Assistant: [tool_call: read_file(...)]                      │
│ Tool result: [파일 내용]              ← ~4K tokens 추가      │
│ Assistant: [tool_call: create_file(...)]                    │
│ Tool result: [성공]                   ← ~50 tokens 추가     │
│ ...                                                         │
│                                                             │
│ ⚠️ 모든 대화 + Tool 결과가 누적됨!                           │
│ ⚠️ LLM은 stateless → 매번 전체를 다시 읽음                   │
└─────────────────────────────────────────────────────────────┘
```

### Context Rot (컨텍스트 부식) 문제

```
Context 사용률 vs 성능
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

성능 ▲
100% │████████████████
     │                ████████
 75% │                        ████████
     │                                ████
 50% │                                    ████
     │                                        ████
 25% │                                            ▼ 급격한 저하
     │
  0% └──────┬──────┬──────┬──────┬──────┬──────▶ Context 사용률
           20%    40%    60%    80%   100%
                         ↑
                    Sweet Spot
                   (50-60%에서 정리)
```

### ❌ 매번 `/context` 치지 마세요!

### ✅ Status Line으로 실시간 모니터링

**방법 1: `/statusline` 명령어 (가장 쉬움)**
```bash
/statusline show context percentage and model name
```

**방법 2: 직접 스크립트 설정**

`~/.claude/statusline.sh`:
```bash
#!/bin/bash
input=$(cat)

MODEL=$(echo "$input" | jq -r '.model.display_name')
CONTEXT_SIZE=$(echo "$input" | jq -r '.context_window.context_window_size')
USAGE=$(echo "$input" | jq '.context_window.current_usage')

if [ "$USAGE" != "null" ]; then
    CURRENT_TOKENS=$(echo "$USAGE" | jq '.input_tokens + .cache_creation_input_tokens + .cache_read_input_tokens')
    PERCENT_USED=$((CURRENT_TOKENS * 100 / CONTEXT_SIZE))
    
    # 색상 경고
    if [ $PERCENT_USED -ge 70 ]; then
        echo "[$MODEL] 🔴 Context: ${PERCENT_USED}%"
    elif [ $PERCENT_USED -ge 50 ]; then
        echo "[$MODEL] 🟡 Context: ${PERCENT_USED}%"
    else
        echo "[$MODEL] 🟢 Context: ${PERCENT_USED}%"
    fi
else
    echo "[$MODEL] Context: 0%"
fi
```

`~/.claude/settings.json`:
```json
{
  "statusLine": {
    "type": "command",
    "command": "~/.claude/statusline.sh",
    "padding": 0
  }
}
```

**결과 화면:**
```
📁 ~/my-project 🌿 main 🤖 Opus 4.5 🟡 Context: 45%
```

### 커뮤니티 도구 활용

| 도구 | 특징 | 설치 |
|------|------|------|
| **ccusage** | 비용 + 컨텍스트 + burn rate | `bun x ccusage statusline` |
| **ccstatusline** | Powerline 스타일, 테마 | `npx ccstatusline` |
| **cc-statusline** | 프로그레스 바, Git 통합 | `npm i -g @chongdashu/cc-statusline` |

### Context 관리 전략

| 상황 | 액션 | 명령어 |
|------|------|--------|
| 50% 도달 | 정리 고려 | `/compact` |
| 70% 도달 | 반드시 정리 | `/compact` 또는 새 대화 |
| 새 작업 시작 | 깨끗하게 | `/clear` |
| 이전 작업 이어가기 | 핸드오프 | `/handoff` → `/clear` |

---

## Part 3: 병렬 Sub-agents - 시간을 사는 방법

### Sub-agent란?

```
┌─────────────────────────────────────────────────────────────┐
│                    Main Agent (Opus 4.5)                    │
│                    - 작업 분배 및 조율                        │
│                    - Context: 200K tokens                   │
└─────────────────────┬───────────────────────────────────────┘
                      │ spawn
        ┌─────────────┼─────────────┬─────────────┐
        ▼             ▼             ▼             ▼
   ┌─────────┐   ┌─────────┐   ┌─────────┐   ┌─────────┐
   │ Agent 1 │   │ Agent 2 │   │ Agent 3 │   │ Agent 4 │
   │ 200K    │   │ 200K    │   │ 200K    │   │ 200K    │
   │ 독립 ctx │   │ 독립 ctx │   │ 독립 ctx │   │ 독립 ctx │
   └────┬────┘   └────┬────┘   └────┬────┘   └────┬────┘
        │             │             │             │
        └─────────────┴──────┬──────┴─────────────┘
                             ▼
                    ┌─────────────────┐
                    │  결과 종합/검증   │
                    │   Main Agent    │
                    └─────────────────┘
```

### 사전 정의된 Sub-agent 종류

| Agent | 용도 | 도구 접근 | Context |
|-------|------|----------|---------|
| **Explore** | 코드베이스 탐색 (읽기 전용) | Glob, Grep, Read | 새로 시작 |
| **Plan** | 구현 계획 설계 | 모든 도구 | 상속 |
| **General-purpose** | 복잡한 멀티스텝 작업 | 모든 도구 | 상속 |

### 🔥 토큰 경제학: 시간 vs 비용 트레이드오프

#### 시나리오: 4개 모듈 분석

**순차 처리 (Single Agent)**
```
┌────────────────────────────────────────────────────┐
│ Main Agent Context Window                          │
├────────────────────────────────────────────────────┤
│ 모듈 1 분석: +15K tokens                           │
│ 모듈 2 분석: +15K tokens (누적: 30K)               │
│ 모듈 3 분석: +15K tokens (누적: 45K)               │
│ 모듈 4 분석: +15K tokens (누적: 60K)               │
│ 종합 분석:   +10K tokens (누적: 70K)               │
├────────────────────────────────────────────────────┤
│ 📊 총 소비: ~70K tokens                            │
│ ⏱️ 소요 시간: ~8분                                 │
│ 📈 Context 사용률: 35%                             │
└────────────────────────────────────────────────────┘
```

**병렬 처리 (4 Sub-agents)**
```
┌─────────────────────────────────────────────────────────────────┐
│ Main Agent: 20K (오버헤드 + 조율)                                │
├─────────────────────────────────────────────────────────────────┤
│ Sub-agent 1: 20K (오버헤드) + 15K (분석) = 35K  ┐               │
│ Sub-agent 2: 20K (오버헤드) + 15K (분석) = 35K  ├─ 동시 실행     │
│ Sub-agent 3: 20K (오버헤드) + 15K (분석) = 35K  │               │
│ Sub-agent 4: 20K (오버헤드) + 15K (분석) = 35K  ┘               │
├─────────────────────────────────────────────────────────────────┤
│ Main Agent: +15K (종합)                                         │
├─────────────────────────────────────────────────────────────────┤
│ 📊 총 소비: ~175K tokens (2.5배 증가!)                          │
│ ⏱️ 소요 시간: ~3분 (62% 단축!)                                  │
│ 📈 Main Context 사용률: 17.5% (깨끗하게 유지!)                   │
└─────────────────────────────────────────────────────────────────┘
```

#### 비용 시뮬레이션

| 전략 | 토큰 소비 | 시간 | 비용 (API) | Main Context |
|------|----------|------|------------|--------------|
| 순차 처리 | 70K | 8분 | $0.21 | 35% 사용 |
| 2 병렬 | 110K | 5분 | $0.33 | 20% 사용 |
| **4 병렬** | **175K** | **3분** | **$0.52** | **17.5% 사용** |
| 10 병렬 | 400K | 1.5분 | $1.20 | 10% 사용 |

```
💡 Sweet Spot: 2~4개 병렬
   - 시간 50-60% 단축
   - 토큰 2-2.5배 증가
   - Main context 깨끗하게 유지
```

#### ⚠️ 극단적 사례: 비용 폭발 주의

```
📌 실제 발생 사례 (AICosts.ai 보고서)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
- 49개 Sub-agents 병렬 실행
- 세션 시간: 2.5시간
- 토큰 소비: 887,000 tokens/분 (!!)
- 추정 비용: $8,000~$15,000 (단일 세션)

⚠️ 교훈: 병렬화는 강력하지만, 모니터링 없이는 위험!
```

### 실전 프롬프트 예제

#### 예제 1: 코드베이스 동시 분석
```
Use 5 parallel subagents to analyze this codebase:
- Agent 1: Analyze the authentication flow in /lib/auth
- Agent 2: Analyze the state management in /lib/providers  
- Agent 3: Analyze the API layer in /lib/services
- Agent 4: Analyze the UI components in /lib/widgets
- Agent 5: Analyze the data models in /lib/models

Each agent should identify: dependencies, potential issues, 
and improvement opportunities.

After all complete, synthesize findings into a unified 
architecture report.
```

#### 예제 2: 멀티 관점 코드 리뷰
```
Launch 4 subagents to review this PR from different perspectives:

1. Security reviewer: Check for vulnerabilities, injection risks
2. Performance reviewer: Identify N+1 queries, memory leaks
3. Maintainability reviewer: Code duplication, SOLID violations
4. Test coverage reviewer: Missing test cases, edge cases

Use Sonnet 4.5 for cost efficiency. 
Compile all findings into a single review document.
```

#### 예제 3: 크로스 플랫폼 동시 구현
```
I need to implement a biometric authentication feature.
Use 3 parallel subagents:

1. Flutter/Dart agent: Implement the cross-platform abstraction
2. iOS agent: Write Swift code for Face ID/Touch ID  
3. Android agent: Write Kotlin code for BiometricPrompt

Coordinate the results into a cohesive implementation.
```

### 비용 최적화 전략

#### 1. 모델 믹싱
```bash
# 분석/탐색 → Sonnet (5배 저렴!)
"Use 4 Sonnet subagents to explore the codebase"

# 복잡한 추론 → Opus
"Synthesize findings with Opus for final architecture"
```

#### 2. 파일 기반 통신 (토큰 절약)
```
Use 4 parallel subagents to analyze the codebase.
Each agent should:
1. Analyze their assigned module
2. Write findings to /docs/tasks/{module}-analysis.md
3. Return only a 3-line summary

After all complete, read the markdown files and synthesize.
Do NOT pass full analysis through context.
```

```
┌──────────────────────────────────────────────────────┐
│ Sub-agent 1 → /docs/tasks/agent1-findings.md         │
│ Sub-agent 2 → /docs/tasks/agent2-findings.md         │
│ Sub-agent 3 → /docs/tasks/agent3-findings.md         │
│                                                      │
│ Main Agent: 파일만 읽음 (요약된 결과)                  │
│ ✅ 전체 context 상속 없이 핵심만 전달                  │
└──────────────────────────────────────────────────────┘
```

---

## Part 4: Skills & Commands - 팀 지식의 자산화

### 개인 노하우 → 팀 자산

```
개인의 노하우              →      팀 공용 Skills
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"난 이렇게 해"             →      SKILL.md로 문서화
"물어보면 알려줄게"         →      자동으로 적용
"코드 리뷰 때 지적"         →      작성 시점에 반영
"퇴사하면 사라짐"           →      Git에 영구 보존
```

### Skills 구조

```
.claude/
├── skills/
│   ├── flutter-conventions/
│   │   └── SKILL.md          # 코딩 컨벤션
│   ├── clean-architecture/
│   │   └── SKILL.md          # 아키텍처 패턴
│   ├── testing-standards/
│   │   └── SKILL.md          # 테스트 작성 규칙
│   ├── api-design/
│   │   └── SKILL.md          # API 설계 원칙
│   └── documentation/
│       └── SKILL.md          # 문서화 표준
├── commands/
│   ├── feature.md            # 새 기능 워크플로우
│   ├── bugfix.md             # 버그 수정 워크플로우
│   ├── review.md             # 코드 리뷰
│   └── release.md            # 릴리즈 워크플로우
└── CLAUDE.md                  # 프로젝트 컨텍스트
```

### SKILL.md 작성 예시

`.claude/skills/flutter-conventions/SKILL.md`:
```markdown
# Flutter Coding Conventions

description: Flutter 코드 작성 시 자동 활성화
triggers: ["flutter", "dart", "widget", "provider"]

## 파일 구조
- feature 단위로 폴더 구성
- 파일명: snake_case.dart
- 클래스명: PascalCase

## 네이밍 규칙
- private 변수: _underscorePrefix
- 상수: SCREAMING_SNAKE_CASE (static const만)
- 메서드: camelCase

## Widget 작성 규칙
```dart
// ✅ Good: const 생성자 사용
class MyWidget extends StatelessWidget {
  const MyWidget({super.key});
  
  @override
  Widget build(BuildContext context) {
    return const SizedBox();
  }
}

// ❌ Bad: const 누락
class MyWidget extends StatelessWidget {
  MyWidget({Key? key}) : super(key: key);
}
```

## State Management (Riverpod)
```dart
// Provider 정의
@riverpod
class FeatureController extends _$FeatureController {
  @override
  FutureOr<FeatureState> build() async {
    // 초기화 로직
  }
}
```

## 금지 사항
- `print()` 사용 금지 → `logger.d()` 사용
- 하드코딩된 문자열 금지 → l10n 사용
- `dynamic` 타입 사용 금지
```

### Custom Commands 예시

#### `/feature` - 새 기능 개발 자동화

`.claude/commands/feature.md`:
```markdown
# New Feature Workflow

When implementing a new feature, follow this automated workflow:

## Phase 1: Analysis (use explore subagents)
1. Analyze existing codebase for similar patterns
2. Identify affected modules and dependencies
3. Check for potential conflicts

## Phase 2: Planning (apply skills)
- Load `clean-architecture` skill for structure decisions
- Load `api-design` skill if API changes needed
- Create implementation plan with file list

## Phase 3: Implementation (parallel subagents)
Deploy subagents for:
- Core business logic implementation
- Repository/data layer changes  
- UI components (if applicable)
- Apply `flutter-conventions` skill to all code

## Phase 4: Quality (parallel subagents)
- Agent 1: Generate unit tests (apply `testing-standards`)
- Agent 2: Generate integration tests
- Agent 3: Update documentation (apply `documentation` skill)

## Phase 5: Review
- Self-review against all loaded skills
- Generate PR description with changes summary

## Output
- Implementation files
- Test files  
- Updated documentation
- PR-ready description
```

**사용법:**
```bash
/feature implement user profile editing with image upload
```

#### `/bugfix` - 버그 수정 자동화

`.claude/commands/bugfix.md`:
```markdown
# Bugfix Workflow

## Input Required
- Bug description or error log
- Steps to reproduce (if available)

## Phase 1: Investigation
Use 3 parallel explore subagents:
1. Search for error keywords in codebase
2. Trace the affected code path
3. Check recent changes in related files

## Phase 2: Root Cause Analysis
- Synthesize findings from all agents
- Identify the root cause
- Assess impact scope

## Phase 3: Fix Implementation
- Apply `flutter-conventions` skill
- Implement minimal fix
- Add defensive code if needed

## Phase 4: Verification
- Generate regression test (apply `testing-standards`)
- Verify fix doesn't break existing tests
- Document the fix

## Output Format
### Bug Summary
[One-line description]

### Root Cause
[Technical explanation]

### Fix Applied
[Files changed and why]

### Tests Added
[New test coverage]
```

#### `/review` - 종합 코드 리뷰

`.claude/commands/review.md`:
```markdown
# Comprehensive Code Review

Load all relevant skills for review criteria:
- `flutter-conventions` for style
- `clean-architecture` for structure
- `testing-standards` for test coverage

## Review Process (4 parallel agents with Sonnet)

### Agent 1: Convention Compliance
- Naming conventions
- File organization
- Documentation completeness

### Agent 2: Architecture Review  
- Layer separation
- Dependency direction
- SOLID principles

### Agent 3: Security & Performance
- Input validation
- Error handling
- Memory management

### Agent 4: Test Coverage
- Unit test coverage
- Edge cases handling
- Mock usage

## Output: Review Report
- ✅ Approved items
- ⚠️ Suggestions (nice to have)
- ❌ Required changes (must fix)
- 📊 Overall score (1-10)
```

### Skills 조합 프롬프트

```
I need to implement a new "favorites" feature.

Workflow:
1. Load skills: clean-architecture, flutter-conventions, testing-standards
2. Use 3 explore subagents to analyze existing bookmark/like features
3. Create implementation plan following clean-architecture
4. Implement with 3 parallel subagents:
   - Domain layer (entities, use cases)
   - Data layer (models, repository)
   - Presentation layer (UI, providers)
5. Generate tests following testing-standards
6. Run /review command on the implementation

Apply flutter-conventions throughout all generated code.
```

---

## Part 5: MCP 통합 - 개발 생태계 연결

### MCP란?

```
┌─────────────────────────────────────────────────────────┐
│  MCP = AI의 USB-C 포트                                  │
│                                                         │
│  Claude Code ←──MCP──→ 외부 서비스                       │
│      │                    │                             │
│      │                    ├─ Context7 (최신 문서)        │
│      │                    ├─ Playwright (브라우저)       │
│      │                    ├─ Notion (문서화)            │
│      │                    ├─ Linear (이슈 트래킹)        │
│      │                    ├─ GitHub (저장소)            │
│      │                    └─ PostgreSQL (DB)            │
└─────────────────────────────────────────────────────────┘
```

### MCP 설정

**글로벌 설정** (`~/.mcp.json`):
```json
{
  "mcpServers": {
    "context7": {
      "command": "npx",
      "args": ["-y", "@context7/mcp-server"]
    },
    "playwright": {
      "command": "npx",
      "args": ["-y", "@playwright/mcp-server"]
    },
    "notion": {
      "command": "npx",
      "args": ["-y", "mcp-remote", "https://mcp.notion.com/mcp"]
    },
    "linear": {
      "command": "npx",
      "args": ["-y", "mcp-remote", "https://mcp.linear.app/mcp"]
    }
  }
}
```

**프로젝트 설정** (`.mcp.json` - Git 커밋 가능!):
```json
{
  "mcpServers": {
    "context7": {
      "command": "npx",
      "args": ["-y", "@context7/mcp-server"]
    },
    "playwright": {
      "command": "npx",
      "args": ["-y", "@playwright/mcp-server"]
    }
  }
}
```

```
✅ 프로젝트 .mcp.json 장점:
- 팀 전체가 동일한 MCP 환경
- 새 팀원 온보딩 즉시 가능
- 워크플로우 표준화
```

### 주요 MCP 서버 활용

#### 1. Context7 - 최신 라이브러리 문서

**문제:**
```
Claude의 학습 데이터는 May 2025까지
→ Flutter 4.x, Riverpod 3.0 최신 API를 모를 수 있음
```

**해결:**
```bash
# 최신 문서 기반 코드 생성
"use context7 to check the latest Riverpod 3.0 patterns,
then implement a StateNotifier for user authentication"

# 마이그레이션 가이드
"use context7 to find breaking changes between 
Flutter 3.x and 4.x, then update our pubspec.yaml"
```

**워크플로우:**
```
1. 요청: "Implement OAuth with latest google_sign_in"
          ↓
2. Claude → Context7 MCP
   └─ google_sign_in 최신 문서 fetch
          ↓
3. Context7 → Claude
   └─ v6.2.1 API, 변경사항, 예제 코드 반환
          ↓
4. Claude
   └─ 최신 API 기반 구현 코드 생성
```

#### 2. Playwright - 브라우저 자동화 & E2E 테스트

**활용 예시:**
```bash
# E2E 테스트 자동 생성
"use playwright MCP to test the login flow:
1. Navigate to /login
2. Enter test credentials
3. Verify redirect to dashboard
4. Check user name is displayed"

# UI 스크린샷 비교
"use playwright to take a screenshot of our 
checkout page and compare with the Figma mockup"

# 폼 자동화 테스트
"use playwright to fill and submit the registration form,
then verify the confirmation email trigger"
```

#### 3. Notion - 문서화 & 지식 관리

**활용 예시:**
```bash
# 코드 리뷰 결과 자동 저장
"Review this PR for security issues, then save 
the findings to the 'Code Reviews' page in Notion"

# 기술 문서 자동 업데이트
"Update the API documentation in Notion based on 
the changes in /lib/services/api_client.dart"

# 회의록 + 액션 아이템 추출
"Read the meeting notes from Notion, extract 
action items, and create tasks in Linear"
```

#### 4. Linear - 이슈 트래킹

**활용 예시:**
```bash
# 버그 티켓 기반 작업
"Read bug PLA-123 from Linear, analyze the issue,
implement a fix, then update the ticket status"

# 중복 티켓 확인
"Check if there's already a ticket for the 404 error 
when users access /api/webhooks with invalid signatures"
```

### 🔥 MCP 조합 워크플로우

#### 워크플로우 1: 버그 수정 자동화 파이프라인

```
┌─────────────────────────────────────────────────────────────────┐
│                    Bug Fix Automation Pipeline                  │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  1. Linear MCP: 버그 티켓 읽기                                   │
│     └─ "Get details for bug PLA-123"                            │
│                                                                 │
│  2. Context7 MCP: 관련 라이브러리 최신 정보 확인                  │
│     └─ "use context7 to check if this is a known issue"         │
│                                                                 │
│  3. PostgreSQL MCP: 데이터 상태 확인                             │
│     └─ "check the user table for affected records"              │
│                                                                 │
│  4. 코드 수정 + 테스트 작성                                      │
│     └─ Skills: flutter-conventions, testing-standards           │
│                                                                 │
│  5. Playwright MCP: E2E 테스트로 수정 검증                       │
│     └─ "use playwright to verify the fix"                       │
│                                                                 │
│  6. GitHub MCP: PR 생성                                         │
│     └─ "create PR with fix for PLA-123"                         │
│                                                                 │
│  7. Linear MCP: 티켓 상태 업데이트                               │
│     └─ "update PLA-123 status to 'In Review'"                   │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

**통합 프롬프트:**
```
Fix bug PLA-123:

1. Use Linear MCP to get the bug details
2. Use context7 to check for known issues with the affected library
3. Implement the fix following our coding standards
4. Use playwright MCP to create and run an E2E test
5. Create a PR via GitHub MCP
6. Update the Linear ticket status

Apply flutter-conventions skill throughout.
```

#### 워크플로우 2: UI 컴포넌트 리뷰 자동화

`.claude/commands/ui-review.md`:
```markdown
# UI Component Review Workflow

## Input
- Component path: $1
- Live URL: $2
- Reference image: $3

## Process

### Step 1: Documentation Check
Use context7 MCP to verify we're using the latest:
- UI framework patterns
- Accessibility guidelines
- Component library APIs

### Step 2: Visual Testing
Use playwright MCP to:
1. Navigate to the live component URL
2. Take a screenshot
3. Compare with reference image
4. Report visual differences

### Step 3: Code Analysis
Analyze the component for:
- Semantic HTML structure
- Accessibility compliance
- Performance patterns
- Code style adherence

### Step 4: Documentation
Use notion MCP to:
1. Create a review entry in 'Component Reviews' database
2. Include: screenshots, findings, recommendations
3. Tag relevant team members

## Output
### Component Review: [name]
- Visual Accuracy: X/10
- Code Quality: X/10
- Accessibility: X/10
- Recommendations: [list]
```

**사용:**
```bash
/ui-review "lib/widgets/checkout_button.dart" \
           "http://localhost:3000/checkout" \
           "designs/checkout_button.png"
```

#### 워크플로우 3: 릴리즈 준비 자동화

```
┌─────────────────────────────────────────────────────────────────┐
│                    Release Preparation Pipeline                  │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  Phase 1: Pre-release Checks (4 parallel subagents)             │
│  ├─ Agent 1: Run all tests                                      │
│  ├─ Agent 2: Check TODO/FIXME comments                          │
│  ├─ Agent 3: Validate version consistency                       │
│  └─ Agent 4: Check dependency updates (use context7)            │
│                                                                 │
│  Phase 2: Changelog Generation                                  │
│  ├─ Analyze commits since last release                          │
│  ├─ Categorize: Features, Fixes, Breaking Changes               │
│  └─ Generate CHANGELOG.md entry                                 │
│                                                                 │
│  Phase 3: Documentation (use notion MCP)                        │
│  ├─ Update API documentation                                    │
│  ├─ Update README if needed                                     │
│  └─ Generate migration guide (if breaking changes)              │
│                                                                 │
│  Phase 4: Release Artifacts                                     │
│  ├─ Bump version numbers                                        │
│  ├─ Create GitHub release (use github MCP)                      │
│  └─ Generate release notes                                      │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## Part 6: 실전 워크플로우

### 시나리오 1: 새 기능 개발 (처음부터 끝까지)

```bash
# 1. 깨끗한 시작
/clear

# 2. 요구사항 분석 + 탐색
"I need to implement social login (Google, Apple, Kakao).
Use 3 explore subagents to:
- Check existing auth patterns in our codebase
- Find social login implementations in similar projects
- Review our current user model structure"

# 3. 계획 수립
/ultrathink
"Based on the exploration, create a detailed implementation plan.
Load clean-architecture skill."

# 4. 구현 (병렬)
"Implement social login with 3 parallel subagents:
- Domain layer: SocialAuthRepository interface, use cases
- Data layer: Firebase/native SDK integration
- Presentation: LoginPage UI updates

Apply flutter-conventions throughout."

# 5. 테스트 생성
"Generate tests for the social login feature.
Apply testing-standards skill.
Use context7 to check latest testing patterns."

# 6. 리뷰
/review

# 7. 문서화 + PR
"Update API docs and create PR.
Use notion MCP to update the Auth documentation.
Use github MCP to create the PR."

# 8. 핸드오프 (다음 세션용)
/handoff
```

### 시나리오 2: 레거시 코드 리팩토링

```bash
# 1. "Throw-away First Draft" 접근법
"Create a new branch 'refactor/auth-module'.
Let Claude refactor the entire auth module 
following clean-architecture.
I'll observe without interrupting."

# 2. 비교 분석
"Compare the refactored code with the original.
Highlight:
- What changed
- Why it changed
- Potential risks"

# 3. 더 날카로운 지시
"Based on the first draft analysis, 
refactor again with these constraints:
- Keep backward compatibility
- Add migration path for existing users
- Maintain current API signatures"
```

### 시나리오 3: 긴급 버그 수정

```bash
# 1. 에러 로그와 함께 시작
"Production error occurred:
[Error log here]

Use Linear MCP to check if there's an existing ticket.
Use 3 parallel explore subagents to investigate:
- Error location and stack trace
- Recent changes in affected area
- Similar past bugs"

# 2. 빠른 수정
"Implement the fix with:
- Minimal code change
- Defensive error handling
- Regression test

Apply flutter-conventions."

# 3. 검증
"Use playwright MCP to run the affected E2E tests.
Verify the fix doesn't break existing functionality."

# 4. 배포 준비
"Create hotfix PR via github MCP.
Update Linear ticket with fix details."
```

---

## Part 7: AI 시대의 마인드셋

### 1. "구현이 빨라졌으니, 취향 정제에 시간을 써라"

```
Before AI:
├─ 구현: 80% ────────────────────────
├─ 설계: 15% ───
└─ 리뷰: 5% ─

After AI:
├─ 구현: 30% ────────
├─ 설계: 40% ────────────────
├─ 리뷰: 20% ────────
└─ 취향/품질: 10% ───
```

**집중해야 할 것:**
- 좋은 시스템 설계
- 명확한 네이밍
- 철저한 문서화
- 포괄적인 테스트
- AI가 못하는 "왜?"에 대한 판단

### 2. "더 많이 놀고 실험하라"

```
AI에게 안 될 것 같은 것도 시도해보라:

❌ "이건 AI가 못할 거야" → 시도도 안 함
✅ "한번 해볼까?" → 놀라운 결과 발견

충분히 하면 직관이 생긴다:
- 어떤 프롬프트가 잘 동작하는지
- 어떤 작업을 위임해야 하는지
- 언제 개입해야 하는지
```

### 3. "도구는 계속 진화한다"

```
Claude Code 버전 히스토리:
├─ 1.0: 기본 코딩 지원
├─ 1.5: Sub-agents 도입
├─ 2.0: Skills, Hooks, 강화된 병렬 처리
└─ 2.x: MCP 통합, Ultrathink...

✅ 릴리스 노트 팔로우
✅ 커뮤니티 참여
✅ 새 기능 즉시 실험
```

### AI-Native 개발자가 되는 법

```
Level 1: AI 사용자
└─ "코드 작성해줘" → 복사/붙여넣기

Level 2: AI 협업자
└─ 프롬프트 엔지니어링, 컨텍스트 관리

Level 3: AI 오케스트레이터 ← 목표
└─ Skills/Commands로 워크플로우 자동화
└─ MCP로 도구 통합
└─ 병렬 처리로 시간 최적화
└─ 팀 지식을 AI에게 학습시킴
```

---

## Part 8: 액션 아이템 & 마무리

### 🚀 내일부터 바로 할 수 있는 것들

#### Day 1: 기본 설정
```bash
# 1. Status Line 설정 (Context 모니터링)
/statusline show context percentage and model name

# 2. CLAUDE.md 생성
echo "# Project Context
- 프로젝트: [이름]
- 기술 스택: Flutter, Riverpod, Clean Architecture
- 코딩 컨벤션: [링크]
" > CLAUDE.md
```

#### Day 2: 첫 번째 커스텀 커맨드
```bash
# .claude/commands/review.md 생성
mkdir -p .claude/commands
# 위에서 제공한 review.md 템플릿 복사
```

#### Day 3: MCP 연결
```bash
# Context7 연결 (최신 문서)
claude mcp add context7 npx -y @context7/mcp-server

# 테스트
"use context7 to check the latest Flutter 3.x features"
```

### 📋 팀 차원 액션 아이템

| 우선순위 | 액션 | 담당 | 기한 |
|----------|------|------|------|
| 🔴 높음 | 팀 공용 `.mcp.json` 작성 | Tech Lead | 1주 |
| 🔴 높음 | 코딩 컨벤션 SKILL.md 작성 | 시니어 | 1주 |
| 🟡 중간 | `/review` 커맨드 표준화 | 팀 전체 | 2주 |
| 🟡 중간 | Status Line 설정 공유 | 팀 전체 | 1주 |
| 🟢 낮음 | 주간 "AI 활용 팁 공유" 세션 | 로테이션 | 지속 |

### 팀 저장소 구조 제안

```
your-project/
├── .claude/
│   ├── commands/
│   │   ├── feature.md
│   │   ├── bugfix.md
│   │   ├── review.md
│   │   └── release.md
│   ├── skills/
│   │   ├── flutter-conventions/
│   │   │   └── SKILL.md
│   │   ├── clean-architecture/
│   │   │   └── SKILL.md
│   │   └── testing-standards/
│   │       └── SKILL.md
│   ├── statusline.sh
│   └── settings.json
├── .mcp.json              ← Git 커밋!
├── CLAUDE.md
└── ...
```

### 📚 참고 자료

**Anthropic 공식:**
- [Claude Code Docs](https://docs.anthropic.com/en/docs/claude-code)
- [Building Effective Agents](https://www.anthropic.com/engineering/building-effective-agents)
- [Context Engineering Guide](https://www.anthropic.com/engineering/effective-context-engineering)

**커뮤니티:**
- [awesome-claude-code](https://github.com/hesreallyhim/awesome-claude-code)
- [Claude Code System Prompts](https://github.com/Piebald-AI/claude-code-system-prompts)

**도구:**
- [ccusage](https://ccusage.com) - 사용량 분석
- [ccstatusline](https://github.com/sirmalloc/ccstatusline) - 커스텀 Status Line

---

## 핵심 테이크어웨이

```
┌─────────────────────────────────────────────────────────────────┐
│                     5가지 핵심 메시지                            │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  1️⃣ Context는 자산이다                                         │
│     → Status Line으로 모니터링, 50-60%에서 정리                  │
│                                                                 │
│  2️⃣ 병렬 처리는 시간을 사는 것                                  │
│     → 2-4개가 Sweet Spot, 토큰 비용 인지하기                    │
│                                                                 │
│  3️⃣ Skills = 팀 지식의 자산화                                   │
│     → 개인 노하우를 Git에 영구 보존                              │
│                                                                 │
│  4️⃣ MCP = 개발 생태계 통합                                     │
│     → 터미널을 떠나지 않고 전체 워크플로우 자동화                 │
│                                                                 │
│  5️⃣ AI-Native 개발자가 되어라                                   │
│     → 구현보다 설계와 취향에 시간 투자                           │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

> *"Claude Code는 내가 경험한 가장 즐거운 제품 경험 중 하나다."*
> 
> 우리 팀도 그렇게 만들어 봅시다. 🚀

---

## Q&A

질문 있으시면 편하게 해주세요!
