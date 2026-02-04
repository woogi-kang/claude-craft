# Claude Craft

> MoAI-ADK: Claude Code를 위한 AI 개발 키트 - 37개 Agents, 303개 Skills, Hooks, Rules

Claude Craft는 [Claude Code](https://claude.ai/code) (Anthropic의 공식 CLI 도구)를 확장하여 복잡한 개발 워크플로우를 자동화하는 오픈소스 프로젝트입니다.

## Quick Start

```bash
# One-line 설치 (권장)
curl -LsSf https://raw.githubusercontent.com/woogi-kang/claude-craft/main/docs/install.sh | sh

# 또는 수동 설치
git clone https://github.com/woogi-kang/claude-craft.git ~/.claude-craft
cd ~/.claude-craft && ./scripts/install.sh
```

## 주요 기능

### MoAI Orchestrator

MoAI는 Claude Code의 전략적 오케스트레이터입니다. 자연어 요청을 분석하고 적절한 에이전트에 위임합니다.

```bash
# 자연어로 요청
"FastAPI로 사용자 인증 API 만들어줘"
"이 코드 리팩토링해줘"
"보안 취약점 분석해줘"

# 명시적 워크플로우
/moai plan "새로운 기능 설명"    # SPEC 문서 생성
/moai run SPEC-001              # DDD 기반 구현
/moai sync SPEC-001             # 문서화 및 PR 생성
```

### Agent System (37개)

#### MoAI Core Agents (20개)

| Category | Agents | 설명 |
|----------|--------|------|
| **Manager** (7) | manager-spec, manager-ddd, manager-docs, manager-quality, manager-project, manager-strategy, manager-git | 워크플로우 조율 및 프로젝트 관리 |
| **Expert** (9) | expert-backend, expert-frontend, expert-security, expert-devops, expert-performance, expert-debug, expert-testing, expert-refactoring, expert-chrome-extension | 도메인 전문 구현 |
| **Builder** (4) | builder-agent, builder-command, builder-skill, builder-plugin | Claude Code 확장 생성 |

#### Domain Agents (17개)

| Category | Agents | 설명 |
|----------|--------|------|
| **개발** | flutter-expert, nextjs-expert, fastapi-expert, flutter-to-nextjs | 프레임워크별 전문 개발 |
| **콘텐츠** | ppt-agent, tech-blog-agent, social-media-agent | 콘텐츠 제작 자동화 |
| **마케팅** | marketing-agent | 마케팅 전략 및 실행물 |
| **기획** | planning-agent, emoticon-orchestrator | 서비스 기획 및 자동화 |
| **법무** | legal-contract-agent, corporate-legal-agent | 계약서 검토 및 법인 운영 |
| **재무** | finance-orchestrator, payment-orchestrator | 재무 자동화 및 결제 관리 |
| **디자인** | frontend-design-agent | Anti-AI-Slop 독창적 디자인 |
| **리뷰** | review-orchestrator, review-code, review-security, review-architecture, review-content, review-design | 멀티-LLM 리뷰 시스템 |

### Skill System (303개)

#### MoAI Skills (52개)

| Category | Count | Examples |
|----------|-------|----------|
| **Foundation** | 5 | moai-foundation-claude, moai-foundation-core, moai-foundation-quality |
| **Languages** | 16 | Python, TypeScript, Go, Rust, Java, Kotlin, Swift, Flutter 등 |
| **Domains** | 4 | Backend, Frontend, Database, UI/UX |
| **Platforms** | 11 | Supabase, Firebase, Vercel, Railway, Neon, Auth0, Clerk 등 |
| **Workflows** | 9 | DDD, SPEC, Testing, Loop, Thinking 등 |
| **Libraries** | 3 | shadcn/ui, Mermaid, Nextra |
| **Tools** | 2 | AST-grep, SVG |

#### Domain Skills (251개)

개발, 콘텐츠, 마케팅, 법무, 재무, 디자인, 기획 각 도메인별 전문 Skills

### Quality Framework (TRUST 5)

모든 코드는 5가지 품질 기준을 충족해야 합니다:

- **T**ested: 85%+ 커버리지, 특성화 테스트
- **R**eadable: 명확한 네이밍, 영문 주석
- **U**nified: 일관된 스타일, 포매팅
- **S**ecured: OWASP 준수, 입력 검증
- **T**rackable: Conventional Commits, 이슈 참조

### Progressive Disclosure

토큰 효율성을 위한 3단계 로딩 시스템:

- **Level 1**: 메타데이터만 (~100 tokens)
- **Level 2**: 본문 로딩 (~5K tokens)
- **Level 3**: 번들 파일 (on-demand)

## 설치

### 자동 설치 (권장)

```bash
# 기본 설치 (심볼릭 링크)
curl -LsSf https://raw.githubusercontent.com/woogi-kang/claude-craft/main/docs/install.sh | sh

# 복사 모드 설치
INSTALL_MODE=copy curl -LsSf https://raw.githubusercontent.com/woogi-kang/claude-craft/main/docs/install.sh | sh

# 커스텀 디렉토리
INSTALL_DIR=~/my-claude-craft curl -LsSf https://raw.githubusercontent.com/woogi-kang/claude-craft/main/docs/install.sh | sh
```

### 수동 설치

```bash
git clone https://github.com/woogi-kang/claude-craft.git ~/.claude-craft
cd ~/.claude-craft
./scripts/install.sh          # 심볼릭 링크 (개발용)
./scripts/install.sh --copy   # 파일 복사 (독립 설치)
./scripts/install.sh --export # 배포 패키지 생성
```

### 설치되는 컴포넌트

| Component | Location | 설명 |
|-----------|----------|------|
| agents/ | ~/.claude/agents/ | 37개 에이전트 정의 |
| skills/ | ~/.claude/skills/ | 303개 스킬 정의 |
| hooks/ | ~/.claude/hooks/ | 자동화 훅 스크립트 |
| rules/ | ~/.claude/rules/ | 언어별/워크플로우 규칙 |
| commands/ | ~/.claude/commands/ | 슬래시 커맨드 |
| output-styles/ | ~/.claude/output-styles/ | 출력 스타일 (Alfred, Yoda, R2D2) |
| statusline.py | ~/.claude/statusline.py | 실시간 비용 추적 |

## 프로젝트 구조

```
claude-craft/
├── .claude/                      # Claude Code 호환 패키지
│   ├── agents/                   # 에이전트 정의 (37개)
│   │   ├── moai/                 # MoAI Core Agents (20개)
│   │   │   ├── manager-*.md      # Manager Agents (7개)
│   │   │   ├── expert-*.md       # Expert Agents (9개)
│   │   │   └── builder-*.md      # Builder Agents (4개)
│   │   ├── 💻 개발/              # Development Agents
│   │   ├── 📝 콘텐츠/            # Content Agents
│   │   ├── 📣 마케팅/            # Marketing Agents
│   │   ├── 🎯 기획/              # Planning Agents
│   │   ├── ⚖️ 법무/              # Legal Agents
│   │   ├── 💰 재무/              # Finance Agents
│   │   ├── 🎨 디자인/            # Design Agents
│   │   └── 🔍 리뷰/              # Review Agents
│   │
│   ├── skills/                   # 스킬 정의 (303개)
│   │   ├── moai-*/               # MoAI Skills (52개)
│   │   │   ├── moai-foundation-* # Foundation Skills (5개)
│   │   │   ├── moai-lang-*       # Language Skills (16개)
│   │   │   ├── moai-domain-*     # Domain Skills (4개)
│   │   │   ├── moai-platform-*   # Platform Skills (11개)
│   │   │   ├── moai-workflow-*   # Workflow Skills (9개)
│   │   │   └── moai-*/           # Other MoAI Skills
│   │   └── 💻 개발/ 등           # Domain Skills (251개)
│   │
│   ├── hooks/                    # Hook 스크립트
│   │   └── moai/                 # MoAI Hooks
│   │       ├── session_start__*  # 세션 시작 훅
│   │       ├── session_end__*    # 세션 종료 훅
│   │       ├── pre_tool__*       # 도구 실행 전 훅
│   │       ├── post_tool__*      # 도구 실행 후 훅
│   │       └── lib/              # 공통 라이브러리
│   │
│   ├── rules/                    # Rules 시스템
│   │   └── moai/
│   │       ├── core/             # 핵심 규칙 (TRUST 5, Constitution)
│   │       ├── workflow/         # 워크플로우 규칙
│   │       ├── development/      # 개발 규칙
│   │       └── languages/        # 언어별 규칙 (16개)
│   │
│   ├── commands/                 # 슬래시 커맨드
│   ├── output-styles/            # 출력 스타일
│   └── statusline.py             # 비용 추적
│
├── .moai/                        # MoAI 설정
│   ├── config/                   # YAML 설정
│   │   ├── config.yaml           # 메인 설정
│   │   └── sections/             # 분리된 설정
│   │       ├── language.yaml     # 언어 설정
│   │       ├── quality.yaml      # 품질 설정
│   │       └── user.yaml         # 사용자 설정
│   └── announcements/            # 다국어 공지
│
├── docs/
│   └── install.sh                # 원격 설치 스크립트
│
├── scripts/
│   └── install.sh                # 로컬 설치 스크립트
│
├── CLAUDE.md                     # MoAI 실행 지침
└── README.md
```

## 사용법

### 기본 사용

```bash
# Claude Code 실행 후 자연어로 요청
"Next.js로 대시보드 만들어줘"
"이 Flutter 앱을 Next.js로 마이그레이션해줘"
"API 보안 취약점 분석해줘"
```

### SPEC 워크플로우

```bash
# 1. 기획 (SPEC 문서 생성)
/moai plan "사용자 인증 시스템 구현"

# 2. 구현 (DDD 기반)
/moai run SPEC-001

# 3. 문서화 및 PR
/moai sync SPEC-001
```

### 특수 기능

```bash
# UltraThink 모드 (깊은 분석)
"아키텍처 설계해줘 --ultrathink"

# 특정 에이전트 지정
"expert-security 에이전트로 보안 분석해줘"

# 루프 모드 (자동 수정)
/moai loop "테스트 통과할 때까지 수정"
```

## Statusline

실시간 비용 추적 상태표시줄:

```
🤖 Opus 4.5 | 💰 $2.09 session / $28.03 today / $2.09 block (3h 58m left) | 🔥 $5.23/hr
```

## 업데이트

```bash
# 원격 업데이트
curl -LsSf https://raw.githubusercontent.com/woogi-kang/claude-craft/main/docs/install.sh | sh

# 로컬 업데이트
cd ~/.claude-craft && git pull && ./scripts/install.sh
```

## 제거

```bash
# 설치된 컴포넌트 제거
rm -rf ~/.claude/{agents,skills,hooks,rules,commands,output-styles}
rm ~/.claude/statusline.py

# 저장소 제거 (선택)
rm -rf ~/.claude-craft
```

## 기여하기

### 새 Agent 추가

```bash
# .claude/agents/<category>/<agent-name>.md 생성
# 또는 MoAI builder 사용
"새로운 데이터 분석 에이전트 만들어줘"
```

### 새 Skill 추가

```bash
# .claude/skills/<skill-name>/SKILL.md 생성
# 또는 MoAI builder 사용
"Pandas 데이터 분석 스킬 만들어줘"
```

## 라이선스

MIT

## 관련 링크

- [Claude Code](https://claude.ai/code) - Anthropic 공식 CLI
- [Claude Code Documentation](https://docs.anthropic.com/claude-code)

---

Made with Claude Code | MoAI-ADK v11.0.0
