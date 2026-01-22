# Claude Code Agent 극한 활용 가이드

> 네임드 개발자들이 연구하고 검증한 50+ 고급 활용 사례 모음

---

## 목차

1. [핵심 철학 및 마인드셋](#1-핵심-철학-및-마인드셋)
2. [멀티에이전트 오케스트레이션](#2-멀티에이전트-오케스트레이션)
3. [병렬 에이전트 실행](#3-병렬-에이전트-실행)
4. [TDD(테스트 주도 개발) 워크플로우](#4-tdd테스트-주도-개발-워크플로우)
5. [SPARC 방법론](#5-sparc-방법론)
6. [컨텍스트 최적화 전략](#6-컨텍스트-최적화-전략)
7. [CLAUDE.md 마스터링](#7-claudemd-마스터링)
8. [Hooks 자동화](#8-hooks-자동화)
9. [MCP 서버 통합](#9-mcp-서버-통합)
10. [CI/CD 헤드리스 자동화](#10-cicd-헤드리스-자동화)
11. [보안 스캐닝 및 코드 리뷰](#11-보안-스캐닝-및-코드-리뷰)
12. [비코딩 활용 사례](#12-비코딩-활용-사례)
13. [브라우저 자동화 (Playwright)](#13-브라우저-자동화-playwright)
14. [지식 관리 통합 (Obsidian/Notion)](#14-지식-관리-통합-obsidiannotion)
15. [디자인-투-코드 (Figma)](#15-디자인-투-코드-figma)
16. [대규모 코드베이스 전략](#16-대규모-코드베이스-전략)
17. [컨테이너화 및 격리](#17-컨테이너화-및-격리)
18. [자가 치유 에이전트](#18-자가-치유-에이전트)
19. [커뮤니티 리소스 및 Skills 레지스트리](#19-커뮤니티-리소스-및-skills-레지스트리)
20. [핵심 참고 자료](#20-핵심-참고-자료)

---

## 1. 핵심 철학 및 마인드셋

### Armin Ronacher의 에이전틱 코딩 원칙 (Flask 창시자)

**출처**: [Agentic Coding Recommendations](https://lucumr.pocoo.org/2025/6/12/agentic-coding/)

1. **`--dangerously-skip-permissions` 활용**
   - 컨테이너 내에서 사용하면 생산성 폭발적 증가
   - 인터넷 접근 없는 Docker 컨테이너에서 실행 권장

2. **언어 선택의 중요성**
   - Go, PHP, "기본 Python"이 에이전트에 최적
   - 심플한 프로젝트 구조, 잘 알려진 프레임워크가 최상의 결과

3. **로깅 및 관측가능성**
   - 터미널 출력 + 파일 로깅 병행
   - 에이전트가 로그 파일을 읽어 디버깅 가능하게 설계

4. **MCP 대신 CLI 도구 활용**
   - MCP 추가보다 스크립트/Makefile 명령어 작성이 효율적
   - 에이전트는 코드 작성을 MCP 상호작용보다 잘 이해함

5. **"가장 멍청하지만 동작하는 코드" 작성**
   - 상속과 과도한 트릭 회피
   - 명확하고 긴 함수명 선호
   - Plain SQL 사용 (ORM보다 에이전트 친화적)

### Simon Willison의 통찰

**출처**: [Agentic Coding: The Future](https://simonwillison.net/2025/Jun/29/agentic-coding/)

- Claude Code는 "코딩 도구"가 아닌 **범용 컴퓨터 자동화 도구**
- Skills가 MCP보다 더 중요할 수 있음
- Playwright를 통해 브라우저 내 디버깅, CI 디버깅까지 가능

---

## 2. 멀티에이전트 오케스트레이션

### Claude Flow - 최고의 오케스트레이션 플랫폼

**출처**: [GitHub - ruvnet/claude-flow](https://github.com/ruvnet/claude-flow)

```bash
# 설치
npx claude-flow@alpha init --force
```

**핵심 기능:**
- 64개 에이전트 시스템
- Hive-mind 아키텍처로 실시간 협업
- 17개 SPARC 모드 (Architect, Coder, TDD, Security, DevOps 등)
- 87개 MCP 도구 통합
- 100+ 에이전트 병렬 실행 지원

### Claude Squad - tmux 기반 멀티에이전트

**출처**: [GitHub - smtg-ai/claude-squad](https://github.com/smtg-ai/claude-squad)

```bash
brew install claude-squad
# 또는
curl -fsSL https://raw.githubusercontent.com/smtg-ai/claude-squad/main/install.sh | bash
```

**특징:**
- tmux로 격리된 터미널 세션 생성
- git worktree로 각 세션별 독립 브랜치
- 백그라운드 작업 완료 (yolo/auto-accept 모드 포함)

### ccswarm - Rust 기반 고성능 오케스트레이션

**출처**: [GitHub - nwiizo/ccswarm](https://github.com/nwiizo/ccswarm)

- 제로 코스트 추상화
- 채널 기반 통신
- Claude Code ACP(Agent Client Protocol) 기본 지원

---

## 3. 병렬 에이전트 실행

### 기본 개념

**출처**: [How to Use Claude Code Subagents to Parallelize Development](https://zachwills.net/how-to-use-claude-code-subagents-to-parallelize-development/)

```bash
# 병렬 수준 최대 10 (초과시 큐잉)
# 각 서브에이전트는 독립적 컨텍스트 윈도우 보유
```

### Git Worktree + tmux 패턴

```bash
# 병렬 작업용 워크트리 생성
git worktree add ../project-feature-a feature-a
git worktree add ../project-feature-b feature-b

# 각 워크트리에서 Claude Code 실행
cd ../project-feature-a && claude
cd ../project-feature-b && claude
```

### 실제 성과 사례

**100-태스크 예시 결과:**
- Agent-1, Agent-2: 서로 다른 컴포넌트 폴더 병렬 작업
- Agent-3, Agent-4: 테스트 업데이트
- Agent-5: 문서 재생성
- Agent-6: 성능 벤치마크

**결과**: 2시간 (수작업 예상 2일), 12,000+ 라인 변경, 100% 테스트 통과, 0 충돌

---

## 4. TDD(테스트 주도 개발) 워크플로우

### TDD Guard - 자동 TDD 강제

**출처**: [GitHub - nizos/tdd-guard](https://github.com/nizos/tdd-guard)

**문제점:**
- Claude Code는 기본적으로 구현 먼저, Happy Path만 작성
- 단일 컨텍스트에서 TDD 강제시 구현이 테스트 로직으로 오염

**해결책:**
- 격리된 컨텍스트의 서브에이전트 사용
- "진정한 테스트 우선 개발을 LLM에서 얻는 유일한 방법"

### 멀티에이전트 TDD 워크플로우

**출처**: [Claude-Flow TDD Template](https://github.com/ruvnet/claude-flow/wiki/CLAUDE-MD-TDD)

```yaml
agents:
  - test_designer: 종합 테스트 스위트 및 엣지 케이스
  - red_phase_agent: 실패하는 테스트 작성
  - green_phase_agent: 최소 구현
  - refactor_agent: 코드 품질 개선
```

### CLAUDE.md에 TDD 설정

```markdown
## Testing

- 항상 TDD 원칙 준수
- 구현 전 테스트 작성
- PostToolUse 훅으로 파일 수정 후 자동 테스트 실행
```

---

## 5. SPARC 방법론

### SPARC = Specification, Pseudocode, Architecture, Refinement, Completion

**출처**: [SPARC Methodology Wiki](https://github.com/ruvnet/claude-flow/wiki/SPARC-Methodology)

**5단계:**

1. **Specification (명세)**
   - 목표, 요구사항, 사용자 시나리오 정의

2. **Pseudocode (수도코드)**
   - 구현 로드맵 역할의 고수준 수도코드

3. **Architecture (아키텍처)**
   - 확장성과 유지보수성 있는 시스템 설계

4. **Refinement (정제)**
   - 반복적 개선으로 성능/안정성 향상

5. **Completion (완료)**
   - 최종 검증 및 배포

### 17개 전문 모드

| 모드 | 역할 |
|------|------|
| Architect | 시스템 아키텍처 설계 |
| Coder | 코드 구현 |
| TDD | 테스트 주도 개발 |
| Security | 취약점 평가 |
| DevOps | 배포 및 CI/CD |
| ... | (17개 모드) |

---

## 6. 컨텍스트 최적화 전략

### R&D 프레임워크 (Reduce & Delegate)

**출처**: [Context Window Optimization](https://www.geeky-gadgets.com/claude-code-ai-context-engineering-strategies/)

**Reduce (축소):**
- 불필요한 데이터 제거
- 관련 정보만 처리

**Delegate (위임):**
- 특정 작업을 서브에이전트에 할당
- 기본 에이전트는 핵심 작업에 집중

### 핵심 명령어

```bash
/clear      # 세션 리셋 (작업 전환시 필수)
/compact    # 대화 요약으로 토큰 절약
/context    # 200k 토큰 윈도우 사용량 확인
```

### Context Editing (자동 컨텍스트 정리)

- 토큰 한도 접근시 오래된 도구 호출/결과 자동 제거
- 대화 흐름 유지하면서 관련 컨텍스트만 보존
- **100턴 평가에서 토큰 소비 84% 감소**

### 전략적 청킹

- 큰 작업을 작은 조각으로 분할
- **컨텍스트 윈도우 마지막 1/5 회피** (메모리 집약적 작업 시)

---

## 7. CLAUDE.md 마스터링

### 최적의 구조

**출처**: [Writing a good CLAUDE.md](https://www.humanlayer.dev/blog/writing-a-good-claude-md)

```markdown
# CLAUDE.md

## WHAT (기술 스택)
- 프로젝트 구조
- 기술/버전 정보
- 코드베이스 맵

## WHY (프로젝트 목적)
- 비즈니스 컨텍스트
- 아키텍처 결정 이유

## HOW (작업 방법)
- 빌드/테스트 명령어
- bun vs node 등 도구 선택
- 변경사항 검증 방법
```

### 핵심 지침

**지침 개수 제한:**
- 프론티어 모델: ~150-200개 지침까지 일관성 유지
- Claude Code 시스템 프롬프트가 이미 ~50개 지침 포함
- **CLAUDE.md는 최소한의 보편적 지침만 포함**

**크기 제한:**
- **10k 단어 이하** 권장
- 47k 단어 파일 = 경고 트리거

### 모노레포 전략

**출처**: [How I Organized My CLAUDE.md in a Monorepo](https://dev.to/anvodev/how-i-organized-my-claudemd-in-a-monorepo-with-too-many-contexts-37k7)

```
project/
├── CLAUDE.md           # 루트 설정
├── frontend/
│   └── CLAUDE.md       # 프론트엔드 전용
├── backend/
│   └── CLAUDE.md       # 백엔드 전용
└── shared/
    └── CLAUDE.md       # 공유 설정
```

- 각 서비스에 필요한 컨텍스트만 로드
- 백엔드는 프론트엔드 가이드 불필요 (역도 마찬가지)

---

## 8. Hooks 자동화

### 훅 타입

**출처**: [Claude Code Hooks Guide](https://code.claude.com/docs/en/hooks-guide)

| 훅 | 설명 |
|----|------|
| PreToolUse | 도구 실행 전 (차단 가능) |
| PostToolUse | 도구 완료 후 |
| PermissionRequest | 권한 요청시 자동 승인/거부 |
| SessionStart | 세션 시작시 |

### Exit 코드

| 코드 | 의미 |
|------|------|
| 0 | 허용/OK |
| 2 | 차단 (PreToolUse만, stderr로 설명) |
| 기타 | 비차단 에러 |

### 실용 예시

**자동 포매팅:**
```json
{
  "hooks": {
    "PostToolUse": [{
      "matcher": "Write|Edit",
      "hooks": [{
        "type": "command",
        "command": "prettier --write \"$CLAUDE_TOOL_USE_FILE_PATH\""
      }]
    }]
  }
}
```

**위험 명령 차단:**
```bash
# PreToolUse에서 rm -rf, git reset --hard, 네트워크 curl 차단
```

**테스트 자동 실행:**
```json
{
  "PostToolUse": [{
    "matcher": "Write|Edit",
    "hooks": [{
      "command": "npm test"
    }]
  }]
}
```

---

## 9. MCP 서버 통합

### 필수 MCP 서버

**출처**: [Best MCP Servers for Claude Code](https://mcpcat.io/guides/best-mcp-servers-for-claude-code/)

| MCP 서버 | 용도 |
|----------|------|
| GitHub | 저장소, 이슈, PR, CI/CD 직접 상호작용 |
| Figma | 디자인 토큰, 컴포넌트, 레이아웃 접근 |
| Notion | 페이지 생성, 데이터베이스 접근 |
| Cloudflare | Workers, R2, D1 등 엣지 컴퓨팅 관리 |
| Firecrawl | 웹 스크래핑 및 컨텐츠 추출 |
| Playwright | 브라우저 자동화 및 테스트 |
| Atlassian | Jira/Confluence 통합 |

### MCP 설치 예시

```bash
# Playwright MCP
claude mcp add --transport stdio playwright npx @executeautomation/playwright-mcp-server

# 비디오 편집 MCP
claude mcp add-json "video-editor" '{"command":"uv","args":["run","video-editor"]}'
```

### 실제 사례

**하루만에 인보이스 플랫폼 구축:**
- Neon MCP로 Postgres 데이터베이스 자동 설정
- 수동 설정/연결 문자열 복사 불필요
- **기존 2-3주 → 1일**

---

## 10. CI/CD 헤드리스 자동화

### 기본 사용법

**출처**: [Run Claude Code Programmatically](https://code.claude.com/docs/en/headless)

```bash
# 기본 헤드리스 모드
claude -p "프롬프트 내용"

# 스트리밍 JSON 출력
claude -p "프롬프트" --output-format stream-json

# 대화 이어가기
claude --continue
claude --resume abc123
```

### GitHub Actions 통합

```yaml
name: Claude Code Review
on:
  pull_request:
    types: [opened, synchronize]

jobs:
  review:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Install Claude Code
        run: npm install -g @anthropic-ai/claude-code
      - name: Run Review
        env:
          ANTHROPIC_API_KEY: ${{ secrets.ANTHROPIC_API_KEY }}
        run: |
          claude -p "Review the changes in this PR for security issues"
```

### 대규모 마이그레이션 패턴 (Fan-out)

```bash
# 1. 작업 목록 생성
claude -p "List all files that need migration from A to B" > tasks.txt

# 2. 병렬 처리
cat tasks.txt | xargs -P 10 -I {} claude -p "Migrate file {} from A to B"
```

### 도구 권한 제한

```bash
# 읽기 전용
claude -p "..." --allowedTools Read,Grep,Glob

# 제한된 쓰기
claude -p "..." --allowedTools Read,Write,Edit

# 풀 권한 (격리 환경 필수)
claude --dangerously-skip-permissions
```

---

## 11. 보안 스캐닝 및 코드 리뷰

### 내장 보안 리뷰

**출처**: [GitHub - claude-code-security-review](https://github.com/anthropics/claude-code-security-review)

```bash
# 내장 슬래시 명령어
/security-review
```

**기능:**
- AI 기반 취약점 탐지
- Diff 인식 스캐닝 (변경 파일만)
- 자동 PR 코멘트
- 언어 불문 지원
- 오탐 필터링

### 한계점

**출처**: [Semgrep Blog - Finding vulnerabilities](https://semgrep.dev/blog/2025/finding-vulnerabilities-in-modern-web-apps-using-claude-code-and-openai-codex/)

- **14% 진양성률, 86% 오탐률** (Semgrep 테스트 결과)
- 주입 이슈에 대한 깊은 시맨틱 이해 부족
- **AI 보안 리뷰는 1차 패스만, 최종 감사 아님**

### 권장 파이프라인

```
AI 리뷰 (1차) → 전통 SAST (Semgrep, StackHawk) → 동적 테스트 (OWASP ZAP)
```

---

## 12. 비코딩 활용 사례

### 마케팅 자동화

**출처**: [How Anthropic teams use Claude Code](https://www.anthropic.com/news/how-anthropic-teams-use-claude-code)

**광고 생성 워크플로우:**
- CSV 파일로 수백 개 광고 처리
- 저성과 광고 식별
- 문자 제한 내 새 변형 생성
- **수 시간 → 수 분**

### 채용 프로세스 자동화

```
인터뷰 트랜스크립트 붙여넣기
→ 구조화된 분석
→ Notion 카드 자동 생성
→ 다음 단계 정의
```

### 비디오/오디오 처리

**출처**: [Claude Code FFmpeg Integration](https://claude-blog.setec.rs/blog/claude-code-ffmpeg-video-audio-processing/)

```bash
# 자연어로 FFmpeg 명령 실행
"이 동영상에서 오디오를 추출하고 MP3로 변환해줘"
"영상에 자막 추가해줘"
```

**ButterCut 프로젝트:**
- WhisperX로 자동 오디오 전사
- 비디오 프레임 분석
- 시각적 트랜스크립트 생성

### 문서 자동화

**자가 주행 문서화:**
- Playwright로 소프트웨어 독립적 탐색
- 문서 갭 자동 식별
- 변경사항 자체 생성

---

## 13. 브라우저 자동화 (Playwright)

### Playwright Skill

**출처**: [GitHub - lackeyjb/playwright-skill](https://github.com/lackeyjb/playwright-skill)

**기능:**
- 웹페이지 테스트
- 복잡한 멀티스텝 플로우 자동화
- 스크린샷 및 콘솔 출력 반환

### 공식 Playwright 에이전트

**출처**: [Playwright Agents](https://playwright.dev/docs/test-agents)

```bash
# Playwright 에이전트 초기화
npx playwright init-agents --loop=claude
```

**3개 전문 에이전트:**

| 에이전트 | 역할 |
|----------|------|
| Planner | 앱 탐색, 마크다운 테스트 계획 생성 |
| Generator | 마크다운 계획 → Playwright 테스트 변환 |
| Healer | 테스트 실행 및 실패 자동 수정 |

---

## 14. 지식 관리 통합 (Obsidian/Notion)

### Obsidian + Claude Code

**출처**: [Using Claude Code with Obsidian](https://kyleygao.com/blog/2025/using-claude-code-with-obsidian/)

**핵심 이점:**
- Obsidian = 마크다운 파일 기반 (파일시스템 접근 가능)
- Claude Code가 파일 구조 탐색 및 편집 가능

**활용 사례:**
```
"오늘 저널에서 모든 인물, 장소, 책에 백링크 추가해줘"
→ 기존 노트 검색 → 새 노트 생성 → 위키링크 자동 추가
```

### Agent Client 플러그인

**출처**: [Obsidian Forum - Agent Client](https://forum.obsidian.md/t/new-plugin-agent-client-bring-claude-code-codex-gemini-cli-inside-obsidian/108448)

- Claude Code, Codex, Gemini CLI를 Obsidian 내에서 실행
- 지식 관리와 에이전트 워크플로우 통합

### Obsidian Claude Code MCP

**출처**: [GitHub - obsidian-claude-code-mcp](https://github.com/iansinnott/obsidian-claude-code-mcp)

- WebSocket으로 자동 연결
- Claude Code가 Obsidian vault와 상호작용

---

## 15. 디자인-투-코드 (Figma)

### Figma MCP 서버

**출처**: [Claude Code + Figma MCP Server](https://www.builder.io/blog/claude-code-figma-mcp-server)

**기능:**
- Figma 파일 직접 참조
- 디자인 토큰, 컴포넌트, 레이아웃 추출
- dev mode 코드 스니펫 접근
- **1:1 비주얼 충실도로 프로덕션 코드 생성**

### 설정

```bash
# Figma Desktop 앱 필요
# 서버: http://127.0.0.1:3845/sse
```

### 한계점

- 기존 코드 업데이트는 어려움 (재생성 또는 수동 편집 필요)
- 멀티프레임 플로우 (캐러셀 등)는 개별 변환 후 결합 필요

---

## 16. 대규모 코드베이스 전략

### 컨텍스트 관리

**출처**: [Claude Code Plugin Best Practices for Large Codebases](https://skywork.ai/blog/claude-code-plugin-best-practices-large-codebases-2025/)

```bash
/context     # 200k 토큰 중 사용량 확인
# 새 세션 기본 비용: ~20k 토큰 (10%)
# 남은 180k로 작업
```

### 세션별 하나의 목표

```markdown
# 좋은 예
"web-frontend 전체에서 auth 미들웨어를 v2로 마이그레이션"

# 목표 변경시 리셋
/clear + /catchup
```

### 대규모 리팩토링 전략

```bash
# 병렬 bash 스크립트로 처리 (메인 에이전트 부담 경감)
for file in /pathA/*.js; do
  claude -p "change all refs from foo to bar in $file" &
done
wait
```

### 배치 편집 권장사항

- 배치 크기: 5-10개 파일
- 배치 간 체크포인트 활성화
- grep으로 심볼 검색 후 3-5개 관련 파일만 오픈

---

## 17. 컨테이너화 및 격리

### Docker 공식 지원

**출처**: [Docker Docs - Claude Code](https://docs.docker.com/ai/sandboxes/claude-code/)

**포함 도구:**
- Docker CLI, GitHub CLI
- Node.js, Go, Python 3
- Git, ripgrep, jq

### 보안 강화 설정

```dockerfile
docker run \
  --cap-drop ALL \
  --security-opt no-new-privileges \
  --read-only \
  --network none \
  claude-code-image
```

### ClaudeBox

**출처**: [GitHub - RchGrav/claudebox](https://github.com/RchGrav/claudebox)

- 완전 컨테이너화된 재현 가능 환경
- 사전 구성된 개발 프로필
- 프로젝트별 Docker 이미지 격리

### Kubernetes 오케스트레이션

**출처**: [GitHub Issue #5045](https://github.com/anthropics/claude-code/issues/5045)

**목표:**
- 단일 CI 컨테이너 → 분산 자가치유 시스템
- 병렬 처리, 리소스 탄력성
- 상태 관리, 워크플로우 오케스트레이션

---

## 18. 자가 치유 에이전트

### Loki Mode

**출처**: [GitHub - claudeskill-loki-mode](https://github.com/asklokesh/claudeskill-loki-mode)

**RARV 사이클:**
- **R**eason (추론)
- **A**ct (행동)
- **R**eflect (반성)
- **V**erify (검증)

**특징:**
- 2-3x 품질 향상
- 100+ 에이전트 대규모 병렬
- 실수에서 학습, 연속성 로그 업데이트
- 5초마다 상태 체크포인트

### 에러 복구

- 지수 백오프로 레이트 리밋 처리
- 서킷 브레이커, 데드 레터 큐, 재시도 로직
- 상태 체크포인트로 중단 복구

### E2E 테스트 자가 치유

**출처**: [Self-Healing Agents through E2E Testing](https://beyondthehype.dev/p/self-healing-agents-through-e2e-testing)

**자율 피드백 루프 적용 후:**
- 테스트 작성률: 11% → 95%
- 첫 실행 성공률: 29% → 71%
- 에이전트 자체 수정률: 34% → 79%

---

## 19. 커뮤니티 리소스 및 Skills 레지스트리

### 주요 컬렉션

| 리소스 | 설명 | 링크 |
|--------|------|------|
| VoltAgent/awesome-claude-code-subagents | 100+ 서브에이전트 | [GitHub](https://github.com/VoltAgent/awesome-claude-code-subagents) |
| wshobson/agents | 99 에이전트, 15 오케스트레이터, 107 스킬 | [GitHub](https://github.com/wshobson/agents) |
| travisvn/awesome-claude-skills | 큐레이션된 스킬 목록 | [GitHub](https://github.com/travisvn/awesome-claude-skills) |
| anthropics/skills | 공식 스킬 저장소 | [GitHub](https://github.com/anthropics/skills) |
| Skills Marketplace | 51,100+ 스킬 검색 | [skillsmp.com](https://skillsmp.com/) |
| Claude Plugins Directory | 자동 인덱싱된 스킬 | [claude-plugins.dev](https://claude-plugins.dev/skills) |

### Skills 설치 위치

```
~/.claude/skills/           # 개인용
.claude/skills/             # 프로젝트용
```

---

## 20. 핵심 참고 자료

### 공식 문서

- [Claude Code Best Practices](https://www.anthropic.com/engineering/claude-code-best-practices)
- [Subagents Documentation](https://code.claude.com/docs/en/sub-agents)
- [Agent Skills](https://code.claude.com/docs/en/skills)
- [Hooks Guide](https://code.claude.com/docs/en/hooks-guide)
- [Headless Mode](https://code.claude.com/docs/en/headless)
- [MCP Integration](https://code.claude.com/docs/en/mcp)
- [Claude Agent SDK](https://platform.claude.com/docs/en/agent-sdk/overview)

### 개발자 블로그

- [Armin Ronacher - Agentic Coding Recommendations](https://lucumr.pocoo.org/2025/6/12/agentic-coding/)
- [Armin Ronacher - Things That Didn't Work](https://lucumr.pocoo.org/2025/7/30/things-that-didnt-work/)
- [Simon Willison - Agentic Coding](https://simonwillison.net/2025/Jun/29/agentic-coding/)
- [Builder.io - How I use Claude Code](https://www.builder.io/blog/claude-code)
- [Shrivu Shankar - How I Use Every Claude Code Feature](https://blog.sshh.io/p/how-i-use-every-claude-code-feature)

### 프레임워크 & 도구

- [Claude Flow](https://github.com/ruvnet/claude-flow) - 최고의 오케스트레이션 플랫폼
- [Claude Squad](https://github.com/smtg-ai/claude-squad) - tmux 기반 멀티에이전트
- [Tasker](https://github.com/Dowwie/tasker) - 태스크 분해 기반 플래닝
- [CCPM](https://github.com/automazeio/ccpm) - GitHub Issues + Git Worktree
- [TDD Guard](https://github.com/nizos/tdd-guard) - TDD 자동 강제

---

## 결론: 극한 활용을 위한 핵심 원칙

1. **심플함 유지**: 복잡한 언어/프레임워크보다 Go, 기본 Python
2. **격리 활용**: Docker/컨테이너에서 `--dangerously-skip-permissions`
3. **병렬화**: git worktree + tmux로 멀티에이전트 실행
4. **컨텍스트 관리**: `/clear`, `/compact` 적극 활용
5. **TDD 강제**: 서브에이전트로 컨텍스트 오염 방지
6. **관측가능성**: 파일 로깅으로 에이전트 자체 디버깅 가능하게
7. **CLAUDE.md 최적화**: 10k 단어 이하, 보편적 지침만
8. **MCP 최소화**: CLI 도구/스크립트가 더 효율적
9. **자동화 훅**: PostToolUse로 포매팅/테스트 자동화
10. **지속적 학습**: 실수에서 배우고 CLAUDE.md 업데이트

---

*이 가이드는 2026년 1월 기준으로 수집된 50+ 웹 소스의 정보를 바탕으로 작성되었습니다.*
