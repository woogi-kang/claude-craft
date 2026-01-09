# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**claude-craft** is a collection of Claude Code customizations including custom statusline for cost tracking, multi-skill agents, and hooks. All Claude Code compatible components are organized under the `.claude/` directory.

## Installation

```bash
# Default: Symbolic links (for development)
./scripts/install.sh

# Copy files (standalone installation)
./scripts/install.sh --copy

# Create distribution package
./scripts/install.sh --export
```

This installs:
1. `.claude/statusline.py` to `~/.claude/statusline.py`
2. Links/copies `.claude/agents/` to `~/.claude/agents/`
3. Links/copies `.claude/skills/` to `~/.claude/skills/`
4. Links/copies `.claude/hooks/` to `~/.claude/hooks/`
5. Configures `settings.json` with statusline and hooks

## Architecture

### Directory Structure

```
claude-craft/
├── .claude/                    # Claude Code compatible package
│   ├── agents/                 # Agent definitions
│   ├── skills/                 # Skill definitions
│   ├── hooks/                  # Hook scripts
│   └── statusline.py           # Cost tracking script
│
├── workspace/                  # Work outputs (gitignored)
│   ├── output/                 # PPT outputs
│   ├── work-blog/              # Blog drafts
│   ├── work-social/            # Social media drafts
│   ├── work-marketing/         # Marketing strategy & assets
│   ├── work-plan/              # Planning docs
│   └── flutter-migration/      # Flutter → Next.js migration outputs
│
├── scripts/
│   └── install.sh              # Installation script
│
└── memoriz/                    # Other projects
```

### Agents

Agents are multi-skill orchestrators that combine multiple skills into coherent workflows. Located in `.claude/agents/<category>/<agent-name>.md`.

**카테고리 구조:**
```
.claude/agents/
├── 콘텐츠/           # 콘텐츠 생성 관련
├── 마케팅/           # 마케팅 전략 및 실행
├── 개발/             # 개발 및 마이그레이션
└── (확장 가능)       # 관리, 설계, 품질보증, QA, 인프라, 문서화 등
```

| Category | Agent | Skills | Description |
|----------|-------|--------|-------------|
| **콘텐츠** | ppt-agent | 11 | 프레젠테이션 제작 (Research → Export) |
| **콘텐츠** | tech-blog-agent | 4 | Hashnode 블로그 작성 |
| **콘텐츠** | social-media-agent | 15 | 멀티플랫폼 소셜미디어 콘텐츠 |
| **마케팅** | marketing-agent | 15 | 마케팅 전략 및 실행물 제작 |
| **개발** | flutter-to-nextjs-agent | 8 | Flutter → Next.js 마이그레이션 |

### Skills

Skills are located in `.claude/skills/<agent-name>-skills/<number>-<skill-name>/SKILL.md`. Each skill defines:
- Trigger keywords
- Input/output specification
- Workflow steps

**Skill Directories:**
- `.claude/skills/ppt-agent-skills/` - PPT 제작 관련 skills (11개)
- `.claude/skills/tech-blog-agent-skills/` - 블로그 작성 관련 skills (4개)
- `.claude/skills/social-media-agent-skills/` - 소셜미디어 관련 skills (15개)
- `.claude/skills/marketing-agent-skills/` - 마케팅 전략 및 실행물 관련 skills (15개)
- `.claude/skills/flutter-to-nextjs-skills/` - Flutter → Next.js 마이그레이션 skills (8개)
- `.claude/skills/nextjs-boilerplate-skill/` - Next.js 프로젝트 보일러플레이트 생성 (Standalone)

### Standalone Skills

Agent에 속하지 않는 독립 Skill입니다.

| Skill | Description |
|-------|-------------|
| **nextjs-boilerplate** | AI 시대 최적화된 Next.js 15+ 프로젝트 보일러플레이트 생성. Clean Architecture, Supabase, Drizzle, Testing, Docker, MCP, CI/CD 선택적 지원. |

### PPT Design System

The PPT agent uses a comprehensive design system (`.claude/skills/ppt-agent-skills/5-design-system/`):
- **10 topic-based themes**: Healthcare, Education, Fintech, AI/Tech, Sustainability, Startup, Luxury, Creative, Real Estate, F&B
- **10 slide templates**: Cover, Contents, Section Divider, Content, Statistics, Split Layout, Team, Quote, Timeline, Closing
- **5 color palettes**: Executive Minimal, Sage Professional, Modern Dark, Corporate Blue, Warm Neutral
- **Typography system**: Pretendard (Korean) / Inter (English), 7-level hierarchy from Hero (72-96pt) to Label (10-12pt)

Theme files: `.claude/skills/ppt-agent-skills/5-design-system/themes/<number>-<theme>/THEME.md`

### Social Media Platforms

The Social Media agent supports 4 platforms:
- **Instagram**: 피드, 릴스, 스토리, 캐러셀
- **LinkedIn**: 텍스트 포스트, 아티클, 캐러셀
- **X (Twitter)**: 트윗, 스레드, 인용
- **Threads**: 텍스트, 이미지

Platform-specific content skills: `.claude/skills/social-media-agent-skills/4-content/<platform>/SKILL.md`

### Marketing Agent

The Marketing agent provides end-to-end marketing automation with 15 skills:

**Strategy Phase:**
- **Context Intake**: 브랜드/제품 정보 수집 (퀄리티 향상 핵심)
- **Market Research**: 3C 분석 (Customer, Competitor, Company)
- **Persona**: 고객 페르소나 & 공감 지도
- **Positioning**: STP 전략 & 포지셔닝 맵
- **Strategy**: PESO 미디어 믹스, North Star Metric

**Campaign Phase:**
- **Campaign**: SMART Goals 캠페인 기획
- **Funnel**: AARRR 퍼널 설계
- **Customer Journey**: 고객 여정 맵 & 터치포인트

**Content Phase:**
- **Copywriting**: AIDA, PAS, BAB 프레임워크 카피
- **Landing Page**: CRO 체크리스트 기반 LP 설계
- **Email Sequence**: 드립 캠페인 & 시퀀스
- **Ads Creative**: Google/Meta/LinkedIn 광고

**Optimization Phase:**
- **A/B Testing**: 테스트 가설 & 설계
- **Analytics KPI**: KPI 대시보드 설계
- **Review**: 최종 품질 검토

**Quality Expectation**: 80% 완성도 초안, 피드백 루프로 시니어 마케터 수준까지 개선 가능

### Flutter to Next.js Agent

Flutter 프로젝트를 Next.js로 마이그레이션하는 Agent입니다. 8개 Skills로 구성:

**Analysis Phase:**
- **Analyze**: Flutter 프로젝트 구조, 위젯, 상태관리, API, 라우팅 분석
- **Mapping**: Widget→Component, State→Zustand, Route 매핑 전략 수립

**Conversion Phase:**
- **Scaffold**: Next.js 15+ 프로젝트 스캐폴딩 (App Router, Zustand, React Query)
- **Components**: Flutter Widget → React 컴포넌트 변환 (shadcn/ui 기반)
- **State**: BLoC/Riverpod/Provider/GetX → Zustand 변환
- **Routing**: GoRouter/Navigator → App Router 변환

**Validation Phase:**
- **Validate**: TypeScript, ESLint, 빌드 검증
- **Review**: 기능 동일성, 코드 품질, 성능 최종 검토

**Tech Stack Mapping:**
| Flutter | Next.js |
|---------|---------|
| Widget | React Component (shadcn/ui) |
| BLoC/Riverpod/Provider/GetX | Zustand |
| Repository + Stream | React Query |
| GoRouter/Navigator | App Router |
| http/dio | Server Actions + fetch |

**Reference Files:**
- `WIDGET-MAP.md`: Flutter Widget → React/Tailwind 매핑
- `STATE-MAP.md`: 상태관리 패턴 매핑

### Hooks

Automated scripts that run on Claude Code events. Located in `.claude/hooks/`.

| Hook | Trigger | Description |
|------|---------|-------------|
| `post-write-hook.sh` | PostToolUse (Write/Edit) | Detects changes to AGENT.md or SKILL.md files |
| `sync-docs.sh` | Called by post-write-hook | Scans agents/skills and reports structure changes |

**Hook Configuration** (in `~/.claude/settings.json`):
```json
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

When a new agent or skill is added, the hook automatically:
1. Detects the file change in `.claude/agents/` or `.claude/skills/` directory
2. Runs `sync-docs.sh` to scan the current structure
3. Reports the updated agent/skill counts

### Statusline

`.claude/statusline.py` - Real-time cost tracking for Claude Code sessions displaying:
- Session cost, daily cost, block cost
- Time remaining in current block
- Hourly burn rate

Pricing data is embedded for Opus, Sonnet, and Haiku models.

### Output Structure

**PPT Output** - `workspace/output/<project-name>/`:
- `slides/` - HTML slide files
- `design-system/` - Project-specific design tokens
- `*.pptx` - Generated PowerPoint files
- `*.pdf` - Generated PDF files
- `build-pptx.js` - PPTX generation script
- `build-pdf.js` - PDF generation script
- `build-all.js` - Combined PPTX + PDF generation

**Blog Output** - `workspace/work-blog/`:
- `research/` - 리서치 노트
- `drafts/` - 초안
- `published/` - 발행 아카이브

**Social Media Output** - `workspace/work-social/`:
- `strategy/` - 브랜드 전략 문서
- `research/` - 리서치 노트
- `drafts/<platform>/` - 플랫폼별 드래프트
- `visuals/` - 비주얼 에셋
- `calendar/` - 콘텐츠 캘린더
- `analytics/` - 성과 리포트

**Marketing Output** - `workspace/work-marketing/`:
- `context/` - 브랜드/제품 컨텍스트 문서
- `research/` - 시장 분석 (3C)
- `personas/` - 고객 페르소나
- `strategy/` - 포지셔닝, 마케팅 전략, 캠페인 기획
- `campaigns/` - 퍼널, 고객 여정
- `copy/` - 헤드라인, 가치 제안, CTA
- `landing-pages/` - LP 구조 및 카피
- `email-sequences/` - 이메일 시퀀스
- `ads/` - 광고 크리에이티브 (Google, Meta, LinkedIn)
- `ab-tests/` - A/B 테스트 설계
- `reports/` - KPI 대시보드, 리뷰 리포트

**Flutter Migration Output** - `workspace/flutter-migration/{project-name}/`:
- `analysis/` - Flutter 프로젝트 분석 리포트
  - `flutter-analysis.md` - 구조, 위젯, 상태관리 분석
  - `mapping-strategy.md` - 변환 전략
  - `validation-report.md` - 검증 결과
  - `final-review.md` - 최종 품질 검토
- `nextjs/` - 변환된 Next.js 프로젝트

## Build Commands

### PPT Generation (pptxgenjs)

```bash
cd workspace/output/<project-name>
npm install

npm run build        # PPTX only
npm run build:pdf    # PDF only
npm run build:all    # Both PPTX + PDF
```

## Key Files

| Path | Purpose |
|------|---------|
| `.claude/agents/<category>/<name>.md` | Agent configuration and workflow |
| `.claude/skills/<agent>-skills/<n>-<skill>/SKILL.md` | Individual skill definition |
| `.claude/skills/ppt-agent-skills/5-design-system/THEMES.md` | Theme selection guide |
| `.claude/skills/ppt-agent-skills/5-design-system/themes/INDEX.md` | Theme keyword mapping |
| `.claude/hooks/post-write-hook.sh` | PostToolUse hook for detecting agent/skill changes |
| `.claude/hooks/sync-docs.sh` | Script to scan and report agent/skill structure |
| `.claude/statusline.py` | Cost tracking statusline script |
| `.claude/agents/마케팅/marketing-agent.md` | Marketing agent workflow and configuration |
| `.claude/skills/marketing-agent-skills/` | Marketing skills (15개) |
| `.claude/agents/개발/flutter-to-nextjs-agent.md` | Flutter → Next.js 마이그레이션 agent |
| `.claude/skills/flutter-to-nextjs-skills/` | Flutter → Next.js 마이그레이션 skills (8개) |
| `.claude/skills/flutter-to-nextjs-skills/4-components/WIDGET-MAP.md` | Flutter Widget → React 매핑 레퍼런스 |
| `.claude/skills/flutter-to-nextjs-skills/5-state/STATE-MAP.md` | 상태관리 패턴 매핑 레퍼런스 |
| `.claude/skills/nextjs-boilerplate-skill/` | Next.js 보일러플레이트 생성 skill |
| `workspace/work-blog/` | Tech blog drafts and research |
| `workspace/work-social/` | Social media drafts and calendar |
| `workspace/work-marketing/` | Marketing strategy and assets |
| `workspace/work-plan/` | Planning documents |

## Conventions

- Agent workflows: Korean documentation, YAML frontmatter
- Skill naming: `<number>-<name>` for execution order
- Skills directory: `<agent-name>-skills` suffix to distinguish from agents
- PPT themes: `<number>-<topic>/THEME.md` with full color specs and CSS
- PptxGenJS colors: Use HEX without `#` prefix (e.g., `667eea` not `#667eea`)

## memoriz-docs

- @./memoriz/docs/prd.md
- @./memoriz/docs/architecture.md
- @./memoriz/docs/design-guide.md
- @./memoriz/docs/ia.md
