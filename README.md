# Claude Craft

> Claude Code를 위한 커스텀 확장 컬렉션 - Agents, Skills, Statusline, Hooks

Claude Craft는 [Claude Code](https://claude.ai/code) (Anthropic의 공식 CLI 도구)를 확장하여 복잡한 콘텐츠 제작 워크플로우를 자동화하는 오픈소스 프로젝트입니다.

## 주요 기능

### 1. Multi-Skill Agents

여러 Skills를 조합하여 복잡한 작업을 자동화하는 Agent 시스템

| Agent | 설명 | Skills |
|-------|------|--------|
| **PPT Agent** | 프레젠테이션 제작 자동화 | 11개 (리서치 → 검증 → 구조 → 콘텐츠 → 디자인 → 시각화 → AI이미지 → 검토 → 개선 → PPTX → PDF) |
| **Tech Blog Agent** | Hashnode 블로그 작성 자동화 | 4개 (리서치 → 초안 → 검토 → 발행) |
| **Social Media Agent** | 멀티플랫폼 SNS 콘텐츠 제작 | 15개 (전략 → 리서치 → 검증 → 컴플라이언스 → 콘텐츠 → 비주얼 → 해시태그 → 승인 → 스케줄 → 리퍼포징 → 참여 → 분석) |
| **Marketing Agent** | 마케팅 전략 및 실행물 제작 | 15개 (컨텍스트 → 리서치 → 페르소나 → 포지셔닝 → 전략 → 캠페인 → 퍼널 → 여정 → 카피 → LP → 이메일 → 광고 → AB테스트 → KPI → 리뷰) |
| **Flutter to Next.js Agent** | Flutter → Next.js 마이그레이션 | 8개 (분석 → 매핑 → 스캐폴딩 → 컴포넌트 → 상태관리 → 라우팅 → 검증 → 리뷰) |
| **Flutter Expert Agent** | Flutter 앱 개발 (Clean Architecture + Riverpod 3 + TDD) | 31개 (Setup → Core → State → Feature → Test → DevOps → Security) |
| **Next.js Expert Agent** | Next.js 웹앱 개발 (Clean Architecture + TanStack Query + Zustand + TDD) | 31개 (Setup → Core → Feature → Test → Optimization → DevOps → Integration) |
| **Legal Contract Agent** | 계약서 검토, 위험 분석, 협상 지원 | 12개 (분석 → 검토 → 실행 → 검증) |

### Standalone Skills

Agent에 속하지 않는 독립 Skill:

| Skill | 설명 |
|-------|------|
| **Next.js Boilerplate** | AI 시대 최적화된 Next.js 15+ 프로젝트 보일러플레이트 생성 (Clean Architecture, Auth, Supabase, Drizzle, Testing, Docker, MCP, CI/CD 선택적 지원) |

### 2. Real-time Cost Statusline

Claude Code 세션의 비용을 실시간으로 추적하는 커스텀 상태표시줄

```
🤖 Opus 4.5 | 💰 $2.09 session / $28.03 today / $2.09 block (3h 58m left) | 🔥 $5.23/hr
```

- 세션별, 일별, 블록별 비용 추적
- 현재 블록 남은 시간 표시
- 시간당 소모율 계산
- Opus, Sonnet, Haiku 모델 지원

### 3. PPT Design System

10개 산업 테마 × 10개 슬라이드 템플릿 × 5개 컬러 팔레트의 체계적인 디자인 시스템

**산업별 테마:**
- Healthcare, Education, Fintech, AI/Tech, Sustainability
- Startup, Luxury, Creative, Real Estate, F&B

**슬라이드 템플릿:**
- Cover, Contents, Section Divider, Content, Statistics
- Split Layout, Team, Quote, Timeline, Closing

### 4. Social Media Multi-Platform Support

4개 플랫폼에 최적화된 콘텐츠 제작

- **Instagram**: 피드, 릴스, 스토리, 캐러셀
- **LinkedIn**: 텍스트 포스트, 아티클, 캐러셀
- **X (Twitter)**: 트윗, 스레드, 인용 트윗
- **Threads**: 텍스트, 이미지 포스트

### 5. Automation Hooks

새로운 Agent/Skill 추가 시 자동으로 구조를 감지하고 보고하는 Hook 시스템

- **PostToolUse Hook**: Write/Edit 작업 후 자동 실행
- **sync-docs.sh**: Agent/Skill 구조 스캔 및 보고
- Agent나 Skill 파일 변경 시 자동으로 프로젝트 구조 파악

## 설치

```bash
# 저장소 클론
git clone https://github.com/woogi-kang/claude-craft.git ~/Development/claude-craft

# 설치 스크립트 실행 (기본: 심볼릭 링크)
cd ~/Development/claude-craft
./scripts/install.sh

# 또는 복사 모드로 설치 (독립 설치)
./scripts/install.sh --copy

# 배포 패키지 생성
./scripts/install.sh --export
```

설치 스크립트는 다음을 수행합니다:
1. `.claude/statusline.py`를 `~/.claude/`에 복사
2. `.claude/agents/`를 `~/.claude/agents/`에 링크/복사
3. `.claude/skills/`를 `~/.claude/skills/`에 링크/복사
4. `.claude/hooks/`를 `~/.claude/hooks/`에 링크/복사
5. `settings.json`에 statusline 및 hooks 설정

## 프로젝트 구조

```
claude-craft/
├── .claude/                         # Claude Code 호환 패키지
│   ├── agents/                      # Agent 정의
│   │   ├── 📝 콘텐츠/
│   │   │   ├── ppt-agent.md
│   │   │   ├── tech-blog-agent.md
│   │   │   └── social-media-agent.md
│   │   ├── 📣 마케팅/
│   │   │   └── marketing-agent.md
│   │   ├── 💻 개발/
│   │   │   ├── flutter-to-nextjs-agent.md
│   │   │   ├── flutter-expert-agent.md
│   │   │   └── nextjs-expert-agent.md
│   │   └── ⚖️ 법무/
│   │       └── legal-contract-agent.md
│   │
│   ├── skills/                      # Skill 정의
│   │   ├── 📝 콘텐츠/
│   │   │   ├── ppt-agent-skills/        # PPT Skills (11개)
│   │   │   ├── tech-blog-agent-skills/  # Blog Skills (4개)
│   │   │   └── social-media-agent-skills/ # SNS Skills (15개)
│   │   ├── 📣 마케팅/
│   │   │   └── marketing-agent-skills/  # Marketing Skills (15개)
│   │   ├── 💻 개발/
│   │   │   ├── flutter-to-nextjs-skills/
│   │   │   ├── flutter-expert-agent-skills/
│   │   │   ├── nextjs-expert-agent-skills/
│   │   │   └── nextjs-boilerplate-skill/
│   │   └── ⚖️ 법무/
│   │       └── legal-contract-agent-skills/ # Legal Skills (12개)
│   │
│   ├── hooks/                       # Hook 스크립트
│   │   ├── post-write-hook.sh
│   │   └── sync-docs.sh
│   │
│   └── statusline.py                # 비용 추적 스크립트
│
├── workspace/                       # 작업 결과물
│   ├── output/                      # PPT 결과물
│   │   └── <project-name>/
│   │       ├── slides/
│   │       ├── design-system/
│   │       ├── *.pptx
│   │       └── *.pdf
│   ├── work-blog/                   # 블로그 작업
│   │   ├── research/
│   │   ├── drafts/
│   │   └── published/
│   ├── work-social/                 # SNS 작업
│   ├── work-marketing/              # 마케팅 작업
│   │   ├── context/
│   │   ├── research/
│   │   ├── personas/
│   │   ├── strategy/
│   │   ├── copy/
│   │   ├── landing-pages/
│   │   ├── email-sequences/
│   │   ├── ads/
│   │   └── reports/
│   ├── work-plan/                   # 기획 문서
│   └── flutter-migration/           # Flutter → Next.js 변환
│       └── <project-name>/
│           ├── analysis/            # 분석 리포트
│           └── nextjs/              # 변환된 프로젝트
│
├── scripts/
│   └── install.sh                   # 설치 스크립트
│
├── CLAUDE.md                        # Claude Code 가이드
└── README.md
```

## 사용법

### PPT Agent

```bash
# Claude Code 실행 후
"AI 스타트업 투자 피치덱 만들어줘"
"Flutter vs React Native 비교 발표자료 만들어줘"
```

**워크플로우:**
```
Research → Validation → Structure → Content → Design System
    ↓
Visual + Image Gen → Review → Refinement → Export (PPTX + PDF)
```

**빌드:**
```bash
cd workspace/output/<project-name>
npm install
npm run build:all    # PPTX + PDF 동시 생성
```

### Tech Blog Agent

```bash
# Claude Code 실행 후
"React Server Components에 대한 블로그 작성해줘"
"/blog-research TypeScript patterns"
"/blog-publish"
```

**워크플로우:**
```
Research → Draft → Review → Publish (Hashnode)
```

### Social Media Agent

```bash
# Claude Code 실행 후
"AI 트렌드에 대한 소셜 콘텐츠 만들어줘"
"LinkedIn용 포스트 써줘"
"이번 주 콘텐츠 캘린더 만들어줘"
```

**워크플로우:**
```
Strategy → Research → Validation → Compliance
    ↓
Content (Instagram/LinkedIn/X/Threads) → Visual → Hashtag
    ↓
Approval → Schedule → Publish → Engagement → Analytics
```

### Marketing Agent

```bash
# Claude Code 실행 후
"개발자용 API 모니터링 툴 마케팅해줘. 경쟁사는 Datadog."
"랜딩페이지 카피 써줘"
"이메일 온보딩 시퀀스 만들어줘"
```

**워크플로우:**
```
Context Intake → Market Research → Persona → Positioning → Strategy
    ↓
Campaign → Funnel → Customer Journey
    ↓
Copywriting → Landing Page → Email Sequence → Ads Creative
    ↓
A/B Testing → Analytics KPI → Review
```

**주요 프레임워크:**
- 전략: 3C, STP, PESO, AARRR, SMART Goals
- 카피: AIDA, PAS, BAB, FAB
- 최적화: CRO 체크리스트, A/B 테스트

**퀄리티 기대치:** 80% 완성도 초안, 피드백 루프로 시니어 마케터 수준까지 개선 가능

### Flutter to Next.js Agent

```bash
# Claude Code 실행 후
"이 Flutter 앱을 Next.js로 마이그레이션해줘"
"Flutter BLoC을 Zustand로 변환해줘"
"GoRouter를 App Router로 변환해줘"
```

**워크플로우:**
```
Analyze → Mapping → Scaffold → Components → State → Routing → Validate → Review
```

**기술 스택 변환:**
| Flutter | Next.js |
|---------|---------|
| Widget | React Component (shadcn/ui) |
| BLoC/Riverpod/Provider/GetX | Zustand |
| Repository + Stream | React Query |
| GoRouter/Navigator | App Router |
| http/dio | Server Actions + fetch |

**주요 특징:**
- Zustand로 상태관리 통일 (BLoC, Riverpod, Provider, GetX 모두 지원)
- shadcn/ui 기반 UI 컴포넌트 (필요시 커스텀)
- 1:1 기능 동일성 유지
- 모바일 웹 + 데스크탑 웹 반응형 지원
- 점진적 변환 (화면/기능 단위)

### Flutter Expert Agent

```bash
# Claude Code 실행 후
"Flutter 앱 만들어줘"
"Riverpod으로 상태관리 설정해줘"
"로그인 피처 구현해줘"
"유닛 테스트 작성해줘"
```

**워크플로우:**
```
Setup → Architecture → Flavor → Firebase/Supabase
    ↓
Design System → Error Handling → Network → Database
    ↓
Riverpod → DI → Feature → Routing → Form → Pagination → Offline
    ↓
Unit Test → Widget Test → Golden Test → E2E Test
    ↓
CI/CD → Widgetbook → i18n → Security → Deep Link → Accessibility
```

**기술 스택:**
| Category | Technology |
|----------|------------|
| 상태관리 | Riverpod 3 (AsyncNotifier, Mutations) |
| 라우팅 | GoRouter + Type-Safe Builder |
| 네트워크 | Dio + Retrofit |
| 로컬DB | Drift (SQLite) |
| 테스트 | Vitest, Robot Pattern, Alchemist, Patrol |
| 백엔드 | Firebase 또는 Supabase |

### Next.js Expert Agent

```bash
# Claude Code 실행 후
"Next.js 앱 만들어줘"
"사용자 피처 구현해줘"
"TanStack Query로 API 연동해줘"
"Playwright E2E 테스트 작성해줘"
```

**워크플로우:**
```
Project Setup → Architecture → Design System → Database → Auth → Env → i18n
    ↓
Schema → API Client → State → Server Action → Error Handling → Middleware
    ↓
Feature → Form → Routing → Pagination → File Upload → Realtime
    ↓
Unit Test → Integration Test → E2E Test → Visual Test
    ↓
Performance → SEO → CI/CD → Monorepo
    ↓
Analytics → Email → Payment → Security
```

**기술 스택:**
| Category | Technology |
|----------|------------|
| Framework | Next.js 15+ (App Router, Server Components) |
| Server State | TanStack Query |
| Client State | Zustand (with persist, immer) |
| URL State | nuqs |
| UI | shadcn/ui + Tailwind CSS v4 |
| Forms | React Hook Form + Zod |
| Auth | Auth.js v5 or Clerk |
| Database | Drizzle ORM + PostgreSQL (Neon) |
| Server Actions | next-safe-action |
| Testing | Vitest + Playwright + MSW |

### Next.js Boilerplate Skill

```bash
# Claude Code 실행 후
"Next.js 프로젝트 만들어줘"
"/nextjs-boilerplate"
```

**옵션:**
- Clean Architecture, Auth (NextAuth), Supabase, Drizzle ORM
- Testing (Vitest + Playwright), Docker, MCP Server, CI/CD

## Statusline 설정

설치 후 자동으로 설정됩니다. 수동 설정이 필요한 경우:

```json
// ~/.claude/settings.json
{
  "statusLine": {
    "type": "command",
    "command": "python3 ~/.claude/statusline.py"
  }
}
```

## Hooks 설정

Agent/Skill 파일 변경 시 자동으로 구조를 감지하는 hook입니다.

```json
// ~/.claude/settings.json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Write|Edit",
        "hooks": [
          {
            "type": "command",
            "command": "bash ~/.claude/hooks/post-write-hook.sh \"$CLAUDE_TOOL_USE_FILE_PATH\""
          }
        ]
      }
    ]
  }
}
```

**Hook 동작 방식:**
1. Claude Code에서 Write/Edit 도구 사용
2. `post-write-hook.sh`가 파일 경로 확인
3. `.claude/agents/` 또는 `.claude/skills/` 경로의 AGENT.md/SKILL.md 변경 감지
4. `sync-docs.sh` 실행하여 구조 보고

**수동 실행:**
```bash
# 현재 agent/skill 구조 확인
bash .claude/hooks/sync-docs.sh
```

## 다른 머신에서 동기화

```bash
cd ~/Development/claude-craft
git pull
./scripts/install.sh
```

## 기여하기

새로운 Agent나 Skill을 추가하려면:

1. **Agent 추가**: `.claude/agents/<agent-name>/AGENT.md` 생성
2. **Skill 추가**: `.claude/skills/<agent-name>-skills/<number>-<skill-name>/SKILL.md` 생성

### Skill 작성 규칙

```yaml
---
name: skill-name
description: |
  스킬 설명

  활성화 조건:
  - "트리거 키워드 1"
  - "트리거 키워드 2"
---

# Skill Title

## 핵심 기능
...

## 다음 단계
1. → `next-skill`: 설명
```

## 라이선스

MIT

## 관련 링크

- [Claude Code](https://claude.ai/code) - Anthropic 공식 CLI
- [Claude Code Documentation](https://docs.anthropic.com/claude-code)
- [PptxGenJS](https://gitbrent.github.io/PptxGenJS/) - PPTX 생성 라이브러리

---

Made with Claude Code
