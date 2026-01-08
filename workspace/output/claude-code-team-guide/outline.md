# Claude Code 팀 가이드 PPT

## 개요
- **발표 제목:** Claude Code 완벽 가이드: 팀을 위한 AI 개발 도구 마스터하기
- **부제:** 왜 Claude Code인가? 어떻게 사용하는가? 팀으로 어떻게 협업하는가?
- **청중:** 개발팀 전체 (주니어, 시니어, 신입)
- **프레임워크:** SCQA + 순차적 구조
- **총 슬라이드:** 50장
- **예상 발표 시간:** 60-75분

## 청중 분석
- **유형:** 개발팀 (Claude Code 미사용자)
- **레벨:** 주니어, 시니어, 신규 입사자 혼합
- **관심사:** 왜 써야 하는지, 어떻게 쓰는지, 팀 협업 방법
- **선호 구조:** 비교 → 기초 → 심화 → 실전

## 핵심 메시지 (5개)
1. **Agentic Coding** - Claude Code는 자동완성이 아닌 자율 에이전트
2. **CLAUDE.md** - 팀의 지식을 코드로 자산화
3. **Skills & Agents** - 반복 작업을 자동화하고 공유
4. **MCP** - 외부 도구와 무한 연결
5. **팀 일관성** - 설정 공유로 모든 팀원이 같은 경험

---

## Part 1: 소개 (슬라이드 1-4)

### Slide 1: 타이틀
**헤드라인:** Claude Code 완벽 가이드
**서브헤드:** 팀을 위한 AI 개발 도구 마스터하기
**비주얼:** Claude 로고 + 코드 에디터 이미지

### Slide 2: 목차
**헤드라인:** 오늘 다룰 내용
**콘텐츠:**
1. 왜 Claude Code인가? (vs 다른 도구)
2. Claude Code 시작하기
3. 팀 협업 기능
4. Skills & Agents
5. MCP 통합
6. 워크플로우 & Best Practices
7. 팀 도입 가이드

### Slide 3: 오늘의 목표
**헤드라인:** 이 발표가 끝나면...
**콘텐츠:**
- Claude Code가 왜 다른 AI 도구와 다른지 이해
- 기본 사용법부터 고급 기능까지 숙지
- 팀으로서 일관되게 사용하는 방법 습득
- 내일부터 바로 적용 가능한 실전 스킬 확보

### Slide 4: AI 코딩 도구의 현재
**헤드라인:** 2025년 AI 코딩 도구 시장
**콘텐츠:**
- GitHub Copilot: 55% 생산성 향상 주장
- Cursor: "Copilot보다 2배 빠르다" 주장
- Claude Code: "Agentic Coding의 새로운 패러다임"
- **질문:** 어떤 걸 선택해야 할까?

---

## Part 2: 왜 Claude Code인가? (슬라이드 5-12)

### Slide 5: 두 가지 철학
**헤드라인:** IDE-First vs Agent-First
**콘텐츠:**
| | IDE-First (Copilot, Cursor) | Agent-First (Claude Code) |
|---|---|---|
| 접근법 | 라인별 자동완성 | 전체 작업 수행 |
| 컨텍스트 | 현재 파일 중심 | 전체 코드베이스 |
| 역할 | 코드 제안 | 작업 완료 |
| 예시 | "이 줄 다음에 뭐?" | "이 기능 전체 구현해줘" |

### Slide 6: 기능 비교 테이블
**헤드라인:** Claude Code vs GitHub Copilot vs Cursor
**콘텐츠:**
| 기능 | Claude Code | Copilot | Cursor |
|------|-------------|---------|--------|
| 자동완성 | - | ✓ | ✓ |
| 다중 파일 수정 | ✓✓✓ | △ | ✓✓ |
| 터미널 통합 | ✓✓✓ | - | △ |
| 에이전트 | ✓✓✓ | △ | ✓ |
| MCP 에코시스템 | ✓✓✓ | - | - |
| 무료 티어 | ✓ | ✓ | ✓ |

### Slide 7: 차별점 1 - Agentic Approach
**헤드라인:** 코드 생성기가 아닌 '동료 개발자'
**콘텐츠:**
- 계획 → 실행 → 검증 → 반복
- 스스로 파일 탐색, 테스트 실행, 버그 수정
- 다단계 작업을 자율적으로 완료
- **예:** "인증 기능 추가해줘" → 파일 생성, 테스트 작성, PR 생성까지

### Slide 8: 차별점 2 - 전체 코드베이스 이해
**헤드라인:** "이 프로젝트가 어떻게 동작하는지 알아"
**콘텐츠:**
- 한 번에 전체 코드베이스 분석
- 아키텍처, 의존성, 패턴 파악
- 기존 코드 스타일 학습 및 적용
- 온보딩 시간: 몇 주 → 1-2일

### Slide 9: 차별점 3 - MCP 에코시스템
**헤드라인:** AI의 USB-C 포트
**콘텐츠:**
- 외부 도구와 표준 프로토콜로 연결
- GitHub, Jira, Confluence, DB 등 직접 접근
- 커뮤니티에서 수천 개 MCP 서버 제공
- **예:** "Jira ENG-4521 이슈 기능 구현하고 GitHub PR 만들어"

### Slide 10: 실제 생산성 수치
**헤드라인:** 숫자로 보는 효과
**콘텐츠:**
- Augment Code 고객: 4-8개월 작업 → 2주
- Altana: 개발 속도 2-10x 향상
- Rakuten: 7시간 자율 코딩 (기존 몇 주 작업)
- Anthropic 보안팀: 스택 트레이스 분석 10-15분 → 5분

### Slide 11: 온보딩 혁명
**헤드라인:** "신입 개발자의 첫날"
**콘텐츠:**
- **기존:** 코드베이스 파악에 몇 주 소요
- **Claude Code:** 전체 코드베이스를 Claude에게 넘김
- 아키텍처 설명, 패턴 이해, 기능 위치 파악
- 시니어 엔지니어 시간 절약 → 생산성 향상

### Slide 12: 주의사항
**헤드라인:** 알아야 할 것들
**콘텐츠:**
- METR 연구: 숙련 개발자 작업 시간 19% 증가 사례
- GitClear: 코드 중복 8배 증가 (2024년)
- Harness: 67% 개발자가 AI 코드 디버깅에 더 많은 시간
- **핵심:** 도구를 이해하고 올바르게 사용해야 함

---

## Part 3: Claude Code 시작하기 (슬라이드 13-22)

### Slide 13: 설치
**헤드라인:** 5분 안에 시작하기
**콘텐츠:**
```bash
# 설치
npm install -g @anthropic-ai/claude-code
# 또는
curl -fsSL https://code.claude.com/install.sh | sh

# 시작
claude
```

### Slide 14: 기본 CLI 명령어
**헤드라인:** 핵심 CLI 명령어
**콘텐츠:**
| 명령어 | 설명 |
|--------|------|
| `claude` | 대화 시작 |
| `claude "질문"` | 질문과 함께 시작 |
| `claude -c` | 이전 대화 재개 |
| `claude -p "질문"` | 답변 후 종료 (SDK 모드) |
| `claude update` | 업데이트 |
| `claude mcp list` | MCP 서버 목록 |

### Slide 15: 핵심 슬래시 커맨드
**헤드라인:** 자주 쓰는 슬래시 커맨드
**콘텐츠:**
| 커맨드 | 용도 |
|--------|------|
| `/help` | 도움말 |
| `/cost` | 비용 확인 |
| `/model opus` | 모델 변경 |
| `/clear` | 대화 초기화 |
| `/compact` | 대화 압축 |
| `/context` | 컨텍스트 사용량 |
| `/config` | 설정 열기 |
| `/init` | CLAUDE.md 초기화 |

### Slide 16: 키보드 단축키
**헤드라인:** 생산성 10배 올리는 단축키
**콘텐츠:**
| 단축키 | 동작 |
|--------|------|
| `Ctrl+C` | 취소 |
| `Ctrl+L` | 화면 클리어 |
| `Esc + Esc` | 되돌리기 |
| `Shift+Tab` | 권한 모드 전환 |
| `#` 시작 | CLAUDE.md에 메모리 추가 |
| `@` | 파일 경로 자동완성 |
| `!` 시작 | Bash 모드 |

### Slide 17: 권한 설정
**헤드라인:** 안전하게 사용하기
**콘텐츠:**
**권한 모드:**
- `default`: 모든 권한 확인
- `acceptEdits`: 파일 편집만 자동 승인
- `plan`: 미리보기 모드 (실행 안 함)

**설정:**
```json
{
  "permissions": {
    "allow": ["Bash(npm:*)", "Bash(git:*)"],
    "deny": ["Bash(rm:*)", "Read(.env)"]
  }
}
```

### Slide 18: IDE 통합
**헤드라인:** VS Code & JetBrains에서 사용
**콘텐츠:**
**VS Code:**
- 마켓플레이스에서 "Claude Code" 설치
- `Cmd+Shift+E` (Mac) / `Ctrl+Shift+E` (Windows)

**JetBrains:**
- IDE Marketplace에서 설치
- 터미널 내 Claude Code 사용

### Slide 19: 샌드박스 모드
**헤드라인:** 안전한 실험 환경
**콘텐츠:**
```bash
claude --sandbox
# 또는
/sandbox
```
- 파일 시스템 격리
- 네트워크 격리
- 프롬프트 주입 방지

### Slide 20: 첫 번째 대화
**헤드라인:** 실습: Hello Claude Code
**콘텐츠:**
```bash
# 1. 시작
claude

# 2. 프로젝트 이해 요청
> "이 프로젝트 구조와 아키텍처 설명해줘"

# 3. 간단한 작업 요청
> "README.md에 설치 방법 추가해줘"

# 4. 비용 확인
> /cost
```

### Slide 21: 효과적인 프롬프트
**헤드라인:** 좋은 프롬프트 vs 나쁜 프롬프트
**콘텐츠:**
**나쁜 예:**
❌ "왜 이 API가 이상해?"
❌ "테스트 추가해"

**좋은 예:**
✅ "ExecutionFactory의 git 히스토리를 분석하고 API 설계 결정 과정 요약해줘"
✅ "로그아웃 사용자 시나리오를 커버하는 테스트 케이스 작성해줘. 목(mock) 사용하지 말고"

### Slide 22: 탐색-계획-코딩-커밋
**헤드라인:** 권장 워크플로우
**콘텐츠:**
1. **탐색:** 파일 읽기, 구조 파악 (코딩 금지)
2. **계획:** "think hard" 사용, 계획 수립
3. **코딩:** 구현 실행
4. **커밋:** 커밋 및 PR 생성

**예:**
> "먼저 이 모듈 구조를 분석해줘. 아직 코드는 수정하지 마"

---

## Part 4: 팀 협업 기능 (슬라이드 23-32)

### Slide 23: CLAUDE.md - 팀의 두뇌
**헤드라인:** 프로젝트 지식을 코드로 저장
**콘텐츠:**
- 프로젝트 개요, 기술 스택
- 코드 규칙, 테스트 요구사항
- 자주 쓰는 명령어
- 팀 워크플로우
- **Git에 커밋 → 팀 전체가 같은 컨텍스트**

### Slide 24: CLAUDE.md 계층 구조
**헤드라인:** 여러 레벨의 설정
**콘텐츠:**
```
~/.claude/CLAUDE.md        ← 개인 전역 설정
.claude/CLAUDE.md          ← 프로젝트 공유 설정 (Git)
.claude/CLAUDE.local.md    ← 개인 프로젝트 설정 (gitignored)
```
**우선순위:** 프로젝트 > 개인

### Slide 25: CLAUDE.md 예시
**헤드라인:** 실전 CLAUDE.md 템플릿
**콘텐츠:**
```markdown
# 프로젝트: MyApp

## 기술 스택
- React 18, TypeScript
- Node.js, Express
- PostgreSQL

## 코드 규칙
- 2칸 들여쓰기
- Prettier + ESLint
- 테스트 필수

## 명령어
npm run dev    # 개발 서버
npm test       # 테스트
npm run lint   # 린트
```

### Slide 26: 경로별 규칙
**헤드라인:** .claude/rules/ 디렉토리
**콘텐츠:**
```
.claude/rules/
├── general.md      # 전체 적용
├── typescript.md   # *.ts, *.tsx에만
└── api.md          # src/api/**에만
```

**typescript.md:**
```yaml
---
paths: src/**/*.{ts,tsx}
---
- `any` 타입 금지
- 모든 함수에 반환 타입 명시
```

### Slide 27: 설정 파일 구조
**헤드라인:** .claude 폴더 완전 분석
**콘텐츠:**
```
.claude/
├── settings.json       # 프로젝트 설정
├── settings.local.json # 개인 설정 (gitignored)
├── CLAUDE.md          # 팀 메모리
├── agents/            # 커스텀 에이전트
├── commands/          # 슬래시 커맨드
├── skills/            # 스킬
├── rules/             # 경로별 규칙
└── .mcp.json          # MCP 서버 설정
```

### Slide 28: settings.json 핵심 설정
**헤드라인:** 팀 전체 설정 관리
**콘텐츠:**
```json
{
  "model": "claude-sonnet-4-5-20250929",
  "permissions": {
    "allow": ["Bash(npm:*)", "Bash(git:*)"],
    "deny": ["Bash(curl:*)", "Read(.env*)"]
  },
  "hooks": {
    "PostToolUse": [...]
  },
  "enabledMcpjsonServers": ["github"]
}
```

### Slide 29: 팀 온보딩 설정
**헤드라인:** 신규 팀원을 위한 원클릭 설정
**콘텐츠:**
1. 저장소 클론
2. `claude` 실행
3. CLAUDE.md 자동 로드
4. MCP 서버 자동 설정
5. 권한 규칙 적용

**결과:** 모든 팀원이 동일한 Claude 경험

### Slide 30: Git 통합
**헤드라인:** Claude Code + Git 워크플로우
**콘텐츠:**
```bash
# 커밋 생성
> "변경사항 커밋해줘"

# PR 생성
> "GitHub에 PR 만들어줘"

# 이슈 연동
> "JIRA ENG-4521 이슈 해결하고 PR 만들어"
```

### Slide 31: 엔터프라이즈 설정
**헤드라인:** 대규모 조직을 위한 관리
**콘텐츠:**
**managed-settings.json:**
- 사용자가 변경 불가
- 중앙 관리 MCP 서버
- 조직 전체 권한 정책

**managed-mcp.json:**
- 허용된 MCP 서버만 사용 가능
- 보안 정책 적용

### Slide 32: 팀 일관성 체크리스트
**헤드라인:** 우리 팀 설정 체크리스트
**콘텐츠:**
- [ ] CLAUDE.md 작성 및 Git 커밋
- [ ] .claude/rules/ 규칙 정의
- [ ] settings.json 권한 설정
- [ ] MCP 서버 설정 공유
- [ ] 팀 온보딩 문서 작성
- [ ] 커스텀 커맨드 정의

---

## Part 5: Skills & Commands (슬라이드 33-40)

### Slide 33: Skills 개념
**헤드라인:** 반복 작업을 자동화하라
**콘텐츠:**
- **Skill** = 특정 작업에 특화된 지침 세트
- 한 번 작성, 모든 팀원이 사용
- Git에 커밋하여 영구 보존
- 트리거 키워드로 자동 활성화

### Slide 34: Skill 파일 구조
**헤드라인:** SKILL.md 작성법
**콘텐츠:**
```
~/.claude/skills/explaining-code/
├── SKILL.md          # 필수: 스킬 정의
├── reference.md      # 선택: 상세 문서
└── examples.md       # 선택: 예시
```

**SKILL.md:**
```yaml
---
name: explaining-code
description: 코드를 다이어그램으로 설명
allowed-tools: Read, Grep, Glob
---
```

### Slide 35: Skill 예시 - 코드 리뷰
**헤드라인:** 실전 Skill: 코드 리뷰
**콘텐츠:**
```yaml
---
name: code-review
description: 팀 표준 코드 리뷰
---

# 코드 리뷰 프로세스
1. git diff로 변경 확인
2. 각 파일 검토
3. 우선순위별 피드백:
   - 🔴 Critical: 반드시 수정
   - 🟡 Warning: 수정 권장
   - 🟢 Suggestion: 개선 고려
```

### Slide 36: 커스텀 슬래시 커맨드
**헤드라인:** 팀 전용 명령어 만들기
**콘텐츠:**
```
.claude/commands/
├── deploy.md         # /deploy
├── security-check.md # /security-check
└── feature.md        # /feature
```

**deploy.md:**
```yaml
---
description: 스테이징 배포
allowed-tools: Bash(npm:*), Bash(git:*)
---
npm run build && npm run test && npm run deploy:staging
```

### Slide 37: Hooks 시스템
**헤드라인:** 이벤트 기반 자동화
**콘텐츠:**
| 이벤트 | 시기 | 용도 |
|--------|------|------|
| PreToolUse | 도구 실행 전 | 검증, 차단 |
| PostToolUse | 도구 실행 후 | 포맷팅, 로깅 |
| SessionStart | 세션 시작 | 환경 설정 |
| UserPromptSubmit | 프롬프트 제출 | 검증, 강화 |

### Slide 38: Hook 예시 - 자동 포맷팅
**헤드라인:** 파일 수정 후 자동 Prettier
**콘텐츠:**
```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Edit|Write",
        "hooks": [{
          "type": "command",
          "command": "npx prettier --write \"$file_path\""
        }]
      }
    ]
  }
}
```

### Slide 39: Hook 예시 - 민감 파일 보호
**헤드라인:** .env 파일 수정 방지
**콘텐츠:**
```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Edit|Write",
        "hooks": [{
          "type": "command",
          "command": "python3 -c \"import json,sys; ... exit(2 if '.env' in path else 0)\""
        }]
      }
    ]
  }
}
```

### Slide 40: Skills 공유 워크플로우
**헤드라인:** 팀 Skill 관리 프로세스
**콘텐츠:**
1. **작성:** `.claude/skills/` 에 SKILL.md 작성
2. **테스트:** 로컬에서 동작 확인
3. **커밋:** Git에 커밋
4. **공유:** 팀원 pull
5. **개선:** 피드백 반영, 반복

---

## Part 6: Agent & Subagent (슬라이드 41-46)

### Slide 41: Agent 개념
**헤드라인:** 자율적으로 작업하는 AI
**콘텐츠:**
- **Agent** = 여러 Skills를 조합한 워크플로우
- 복잡한 다단계 작업 자동화
- 독립된 컨텍스트에서 실행
- 결과만 메인 대화에 반환

### Slide 42: 내장 Subagent 타입
**헤드라인:** 기본 제공 에이전트
**콘텐츠:**
| 타입 | 용도 | 도구 |
|------|------|------|
| General | 다단계 작업 | 모두 |
| Explore | 코드베이스 탐색 | Read, Grep, Glob |
| Plan | 계획 수립 | Read, Grep, Glob |

**사용:**
```
> "Explore 에이전트로 인증 관련 코드 찾아줘"
```

### Slide 43: Task Tool 활용
**헤드라인:** 병렬 작업 실행
**콘텐츠:**
```
> "3개 파일을 병렬로 분석해줘"

Claude: Task tool로 3개 Subagent 생성
        → 각각 독립 컨텍스트에서 실행
        → 결과 종합하여 반환
```

**장점:**
- 시간 단축 (62%까지)
- 메인 컨텍스트 보존
- 독립적 작업 수행

### Slide 44: 커스텀 Agent 생성
**헤드라인:** .claude/agents/ 폴더
**콘텐츠:**
```yaml
# .claude/agents/code-reviewer.md
---
name: code-reviewer
description: 코드 리뷰 전문가
tools: Read, Grep, Glob, Bash
model: sonnet
---

당신은 시니어 코드 리뷰어입니다.
...
```

### Slide 45: Agent 체이닝
**헤드라인:** 에이전트 연결 사용
**콘텐츠:**
```
> "먼저 코드 분석 에이전트로 문제점 찾고,
   그 다음 최적화 에이전트로 수정해줘"

Claude: 1. code-analyzer 에이전트 실행
        2. 결과를 optimizer 에이전트에 전달
        3. 최종 결과 반환
```

### Slide 46: 실전 예시 - PPT Agent
**헤드라인:** 9개 Skill 조합 Agent
**콘텐츠:**
```
PPT Agent
├── 1. Research Skill     → 자료 조사
├── 2. Validation Skill   → 팩트체크
├── 3. Structure Skill    → 구조 설계
├── 4. Content Skill      → 내용 작성
├── 5. Design System Skill → 디자인
├── 6. Visual Skill       → 차트 생성
├── 7. Review Skill       → 품질 검토
├── 8. Refinement Skill   → 수정 반영
└── 9. Export Skill       → PPTX 출력
```

---

## Part 7: MCP 통합 (슬라이드 47-52)

### Slide 47: MCP 개념
**헤드라인:** Model Context Protocol
**콘텐츠:**
- **MCP** = AI가 외부 도구와 소통하는 표준 프로토콜
- USB-C처럼 한 번 연결하면 모든 기능 사용
- 2024년 11월 출시 후 수천 개 서버 구축
- 업계 표준으로 자리잡음

### Slide 48: MCP 서버 설정
**헤드라인:** 외부 도구 연결하기
**콘텐츠:**
```bash
# HTTP 서버 추가
claude mcp add --transport http github \
  https://api.githubcopilot.com/mcp/

# 환경 변수와 함께
claude mcp add --transport http stripe \
  --header "Authorization: Bearer $STRIPE_KEY" \
  https://mcp.stripe.com/mcp

# 목록 확인
claude mcp list
```

### Slide 49: 주요 MCP 서버
**헤드라인:** 추천 MCP 서버
**콘텐츠:**
| 서버 | 용도 |
|------|------|
| GitHub | 이슈, PR, 코드 리뷰 |
| Atlassian | Jira, Confluence |
| Playwright | 브라우저 자동화 |
| Context7 | 라이브러리 문서 |
| PostgreSQL | DB 쿼리 |
| Stripe | 결제 API |

### Slide 50: Context7 활용
**헤드라인:** 공식 문서 조회
**콘텐츠:**
```
> "React useEffect 공식 문서 찾아줘"

Claude: [Context7 MCP 사용]
        공식 React 문서에서 useEffect 패턴 조회
        최신 버전 기준 정확한 정보 제공
```

**장점:**
- 오래된 학습 데이터 대신 최신 문서
- 버전별 정확한 API 정보

### Slide 51: Playwright 활용
**헤드라인:** 브라우저 자동화
**콘텐츠:**
```
> "로그인 플로우 E2E 테스트 만들어줘"

Claude: [Playwright MCP 사용]
        1. 브라우저 열기
        2. 로그인 페이지 접속
        3. 폼 입력
        4. 검증
        5. 스크린샷 캡처
```

### Slide 52: 엔터프라이즈 MCP 관리
**헤드라인:** 조직 전체 MCP 제어
**콘텐츠:**
**managed-mcp.json:**
```json
{
  "mcpServers": {
    "github": { "url": "..." },
    "jira": { "url": "..." }
  }
}
```
- 사용자 수정 불가
- 중앙 관리 보안 정책
- 승인된 서버만 허용

---

## Part 8: 워크플로우 & Best Practices (슬라이드 53-60)

### Slide 53: 탐색-계획-코딩-커밋
**헤드라인:** 권장 워크플로우 #1
**콘텐츠:**
```
1. 탐색
   > "이 모듈 구조 분석해줘 (코딩 금지)"

2. 계획
   > "think hard로 구현 계획 세워줘"

3. 코딩
   > "계획대로 구현해줘"

4. 커밋
   > "커밋하고 PR 만들어줘"
```

### Slide 54: TDD 워크플로우
**헤드라인:** 권장 워크플로우 #2
**콘텐츠:**
```
1. 테스트 작성
   > "이 기능의 테스트 먼저 작성해줘"

2. 실패 확인
   > "테스트 실행해봐"

3. 구현
   > "테스트 통과하도록 구현해줘"

4. 리팩토링
   > "코드 정리하고 테스트 다시 확인해줘"
```

### Slide 55: 다중 Claude 인스턴스
**헤드라인:** 권장 워크플로우 #3
**콘텐츠:**
```
Terminal 1: 코드 작성
Terminal 2: 코드 검증
Terminal 3: 테스트 실행
```

**Git Worktree 활용:**
```bash
git worktree add ../feature-auth feature/auth
cd ../feature-auth
claude
```

### Slide 56: 병렬 Subagent 전략
**헤드라인:** 시간 단축의 비밀
**콘텐츠:**
**Sweet Spot: 2-4개 병렬**

```
> "이 3개 파일을 병렬로 분석해줘"

시간 비교:
순차: 30분
병렬: 12분 (60% 단축)
```

**주의:** 49개 병렬 → 비용 폭발 사례

### Slide 57: Context 관리
**헤드라인:** 200K 토큰 활용법
**콘텐츠:**
```
/context          # 사용량 확인

관리 전략:
1. 정기적으로 /compact
2. 완료된 작업 후 /clear
3. 중요 정보는 CLAUDE.md에 저장
4. 대규모 작업은 Subagent 활용
```

### Slide 58: 비용 최적화
**헤드라인:** 효율적인 토큰 사용
**콘텐츠:**
**모델 믹싱:**
- 탐색: Haiku (저렴)
- 코딩: Sonnet (균형)
- 복잡한 설계: Opus (고성능)

**파일 통신:**
- 긴 데이터는 파일로 전달
- 컨텍스트 낭비 방지

### Slide 59: 헤드리스 모드
**헤드라인:** CI/CD 통합
**콘텐츠:**
```bash
# 자동화 스크립트
claude -p "lint 오류 수정해줘" \
  --output-format stream-json

# Pre-commit hook
claude -p "변경사항 검토해줘" \
  --dangerously-skip-permissions
```

### Slide 60: 피해야 할 것들
**헤드라인:** 흔한 실수
**콘텐츠:**
❌ 탐색 없이 바로 코딩 요청
❌ 모호한 프롬프트 ("테스트 추가해")
❌ 과도한 CLAUDE.md (검증 없이)
❌ --dangerously-skip-permissions 남용
❌ 컨텍스트 관리 미흡

---

## Part 9: 팀 도입 가이드 (슬라이드 61-66)

### Slide 61: 도입 로드맵
**헤드라인:** 4주 마스터 플랜
**콘텐츠:**
```
Week 1: 개인 숙달
  - 설치 및 기본 사용
  - 핵심 커맨드 습득

Week 2: 팀 설정
  - CLAUDE.md 공동 작성
  - 권한 설정 표준화

Week 3: 고급 기능
  - Skills, Agents 구축
  - MCP 연동

Week 4: 최적화
  - 워크플로우 정립
  - 비용 최적화
```

### Slide 62: Day 1-3 체크리스트
**헤드라인:** 첫 3일 완료 목표
**콘텐츠:**
**Day 1:**
- [ ] Claude Code 설치
- [ ] 첫 대화 시작
- [ ] /help, /cost 사용해보기

**Day 2:**
- [ ] 프로젝트에서 사용
- [ ] 간단한 작업 요청
- [ ] 권한 설정 이해

**Day 3:**
- [ ] CLAUDE.md 작성
- [ ] 슬래시 커맨드 활용
- [ ] 팀원과 설정 공유

### Slide 63: Week 1-2 목표
**헤드라인:** 기본 숙달 체크리스트
**콘텐츠:**
- [ ] 탐색-계획-코딩-커밋 워크플로우 적용
- [ ] 효과적인 프롬프트 작성
- [ ] Context 관리 습관화
- [ ] CLAUDE.md Git 커밋
- [ ] 팀 settings.json 표준화
- [ ] 첫 번째 커스텀 커맨드 작성

### Slide 64: Month 1 목표
**헤드라인:** 팀 협업 구축
**콘텐츠:**
- [ ] 팀 공용 Skills 3개 이상 작성
- [ ] 팀 공용 Agent 1개 이상 작성
- [ ] MCP 서버 2개 이상 연동
- [ ] 코드 리뷰에 Claude 활용
- [ ] 온보딩 문서 Claude로 자동 생성
- [ ] 주간 회고: 효과 측정

### Slide 65: 성공 지표
**헤드라인:** 무엇을 측정할 것인가
**콘텐츠:**
| 지표 | 측정 방법 |
|------|----------|
| 작업 완료 시간 | 티켓 사이클 타임 |
| 코드 품질 | PR 리뷰 코멘트 수 |
| 온보딩 시간 | 신규 팀원 첫 PR까지 |
| 팀원 만족도 | 정기 설문 |
| 비용 효율 | 월간 토큰 사용량 |

### Slide 66: 지속적 개선
**헤드라인:** 계속 발전하기
**콘텐츠:**
1. **주간 회고**
   - 효과적이었던 프롬프트 공유
   - 새로운 Skills 아이디어

2. **월간 정비**
   - CLAUDE.md 업데이트
   - Skills 라이브러리 정리

3. **분기별 평가**
   - 생산성 지표 분석
   - 새로운 기능 도입 검토

---

## Part 10: 마무리 (슬라이드 67-70)

### Slide 67: 5가지 핵심 테이크어웨이
**헤드라인:** 오늘 기억할 것
**콘텐츠:**
1. **Agentic Coding** - 자동완성이 아닌 자율 에이전트
2. **CLAUDE.md** - 팀 지식을 코드로 자산화
3. **Skills & Agents** - 반복 작업 자동화
4. **MCP** - 외부 도구와 무한 연결
5. **탐색→계획→코딩→커밋** - 워크플로우의 기본

### Slide 68: 내일 할 수 있는 3가지
**헤드라인:** 바로 시작하기
**콘텐츠:**
1. **오늘:** Claude Code 설치하고 "이 프로젝트 설명해줘"
2. **내일:** CLAUDE.md 작성하고 Git 커밋
3. **이번 주:** 첫 번째 커스텀 커맨드 만들기

### Slide 69: 리소스
**헤드라인:** 더 알아보기
**콘텐츠:**
- **공식 문서:** docs.claude.com
- **Best Practices:** anthropic.com/engineering/claude-code-best-practices
- **MCP 서버 목록:** mcpcat.io
- **커뮤니티:** github.com/anthropics/claude-code
- **팀 Slack 채널:** #claude-code-help

### Slide 70: Q&A
**헤드라인:** 질문 & 답변
**콘텐츠:**
- 궁금한 점이 있으신가요?
- 특정 사용 사례 논의
- 팀 도입 관련 질문

---

## 디자인 가이드

### 색상
- Primary: #667eea (보라)
- Secondary: #764ba2 (진보라)
- Accent: #f093fb (핑크)
- Background: #0f0f23 (다크)
- Text: #ffffff (흰색)

### 폰트
- 제목: Pretendard Bold
- 본문: Pretendard Regular
- 코드: JetBrains Mono

### 레이아웃
- 16:9 비율
- 최대 7줄/슬라이드
- 코드 블록은 최대 10줄
- 다이어그램 적극 활용
