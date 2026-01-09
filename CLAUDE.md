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
│   ├── work-legal/             # Legal contract review & drafts
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
├── 📝 콘텐츠/         # 콘텐츠 생성 관련
├── 📣 마케팅/         # 마케팅 전략 및 실행
├── 💻 개발/           # 개발 및 마이그레이션
├── ⚖️ 법무/           # 계약서 검토 및 법무 지원
└── (확장 가능)        # 🎯 관리, 🏗️ 설계, ✅ 품질보증, 🔍 QA, 🚀 인프라, 📚 문서화 등
```

| Category | Agent | Skills | Description |
|----------|-------|--------|-------------|
| **📝 콘텐츠** | ppt-agent | 11 | 프레젠테이션 제작 (Research → Export) |
| **📝 콘텐츠** | tech-blog-agent | 4 | Hashnode 블로그 작성 |
| **📝 콘텐츠** | social-media-agent | 15 | 멀티플랫폼 소셜미디어 콘텐츠 |
| **📣 마케팅** | marketing-agent | 15 | 마케팅 전략 및 실행물 제작 |
| **💻 개발** | flutter-to-nextjs-agent | 8 | Flutter → Next.js 마이그레이션 |
| **💻 개발** | flutter-expert-agent | 26 | Flutter 앱 개발 (Clean Architecture + Riverpod 3 + TDD) |
| **⚖️ 법무** | legal-contract-agent | 12 | 계약서 검토, 위험 분석, 협상 지원 |

### Skills

Skills are located in `.claude/skills/<category>/<agent-name>-skills/<number>-<skill-name>/SKILL.md`. Each skill defines:
- Trigger keywords
- Input/output specification
- Workflow steps

**카테고리 구조:**
```
.claude/skills/
├── 📝 콘텐츠/
│   ├── ppt-agent-skills/           (11 skills)
│   ├── tech-blog-agent-skills/     (4 skills)
│   └── social-media-agent-skills/  (15 skills)
├── 📣 마케팅/
│   └── marketing-agent-skills/     (15 skills)
├── 💻 개발/
│   ├── flutter-to-nextjs-skills/   (8 skills)
│   ├── flutter-expert-agent-skills/ (26 skills + 6 references)
│   └── nextjs-boilerplate-skill/   (standalone)
└── ⚖️ 법무/
    └── legal-contract-agent-skills/ (12 skills)
```

### Standalone Skills

Agent에 속하지 않는 독립 Skill입니다. (💻 개발 카테고리에 위치)

| Skill | Description |
|-------|-------------|
| **nextjs-boilerplate** | AI 시대 최적화된 Next.js 15+ 프로젝트 보일러플레이트 생성. Clean Architecture, Supabase, Drizzle, Testing, Docker, MCP, CI/CD 선택적 지원. |

### PPT Design System

The PPT agent uses a comprehensive design system (`.claude/skills/📝 콘텐츠/ppt-agent-skills/5-design-system/`):
- **10 topic-based themes**: Healthcare, Education, Fintech, AI/Tech, Sustainability, Startup, Luxury, Creative, Real Estate, F&B
- **10 slide templates**: Cover, Contents, Section Divider, Content, Statistics, Split Layout, Team, Quote, Timeline, Closing
- **5 color palettes**: Executive Minimal, Sage Professional, Modern Dark, Corporate Blue, Warm Neutral
- **Typography system**: Pretendard (Korean) / Inter (English), 7-level hierarchy from Hero (72-96pt) to Label (10-12pt)

Theme files: `.claude/skills/📝 콘텐츠/ppt-agent-skills/5-design-system/themes/<number>-<theme>/THEME.md`

### Social Media Platforms

The Social Media agent supports 4 platforms:
- **Instagram**: 피드, 릴스, 스토리, 캐러셀
- **LinkedIn**: 텍스트 포스트, 아티클, 캐러셀
- **X (Twitter)**: 트윗, 스레드, 인용
- **Threads**: 텍스트, 이미지

Platform-specific content skills: `.claude/skills/📝 콘텐츠/social-media-agent-skills/4-content/<platform>/SKILL.md`

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

### Legal Contract Agent

계약서 검토 및 법무 지원을 위한 Agent입니다. 12개 Skills로 구성:

**Phase 1 - Analysis (분석):**
- **Context**: 계약 배경, 당사자 정보, 협상 목표 수집
- **Document Analysis**: 계약서 구조, 조항 분류, 핵심 조건 추출
- **Risk Assessment**: 4단계 위험 매트릭스 (Critical/High/Medium/Low)
- **Summary Extract**: 핵심 조항 요약, 1-Page 경영진 브리핑

**Phase 2 - Review (검토):**
- **Clause Library**: 업계 표준(Playbook) 대비 조항 비교
- **Version Compare**: 버전 간 변경사항 Diff 분석, 협상 추적
- **Compliance Check**: 규제 준수 검증 (하도급법, 개인정보보호법 등)

**Phase 3 - Execution (실행):**
- **Redline Suggest**: 수정 제안 및 레드라인 마크업
- **Negotiation Points**: BATNA 분석, Give-and-Take 전략
- **Document Generate**: 계약서 초안 생성 (NDA, SaaS, 용역계약서)

**Phase 4 - Validation (검증):**
- **Checklist**: 서명 전 최종 체크리스트
- **Final Review**: 종합 검토 및 권고사항

**Risk Matrix:**
| Level | Symbol | Action |
|-------|--------|--------|
| Critical | 🔴 | 즉시 수정 필요 |
| High | 🟠 | 협상 권고 |
| Medium | 🟡 | 검토 필요 |
| Low | 🟢 | 수용 가능 |

**Compliance Coverage:**
- 하도급법 (공정거래위원회)
- 개인정보보호법/GDPR
- 전자상거래법
- 근로기준법
- 업종별 규제 (금융, 의료, 건설 등)

### Flutter Expert Agent

현대적인 Flutter 앱 개발을 위한 종합 Agent입니다. 26개 Skills + 6개 References로 구성:

**Tech Stack:**
| Category | Technology | Version |
|----------|------------|---------|
| **상태관리** | Riverpod 3 (AsyncNotifier, Mutations) | ^3.1.0 |
| **라우팅** | GoRouter + Type-Safe Builder | ^17.0.1 |
| **네트워크** | Dio + Retrofit | ^5.9.0 |
| **로컬DB** | Drift (SQLite) | ^2.30.0 |
| **코드생성** | Freezed + JSON Serializable | ^3.2.4 |
| **반응형UI** | flutter_screenutil | ^5.9.3 |
| **다국어** | easy_localization | ^3.0.8 |
| **Flavor** | flutter_flavorizr | ^2.4.1 |
| **환경변수** | envied | ^1.3.2 |
| **Firebase** | firebase_core + 7 services | ^4.3.0 |

**Phase 1 - Setup (설정):**
- **Project Setup**: pubspec.yaml, 디렉토리 구조 (Clean Architecture)
- **Architecture**: Domain/Data/UI 레이어 설계
- **Flavor**: dev/staging/prod 환경 분리, envied 환경 변수
- **Firebase**: Auth, Firestore, FCM, Crashlytics, Analytics 등

**Phase 2 - Core (핵심):**
- **Design System**: Atomic Design + flutter_screenutil 반응형 토큰
- **Error Handling**: Either/Result 패턴 (fpdart)
- **Network**: Dio + Retrofit + Interceptors
- **Database**: Drift DAOs, 마이그레이션

**Phase 3 - State (상태관리):**
- **Riverpod 3**: AsyncNotifier, Mutations, Offline Persistence
- **DI**: Injectable + GetIt

**Phase 4 - Feature (기능):**
- **Feature**: Domain/Data/UI 레이어별 구현
- **Routing**: GoRouter + StatefulShellRoute
- **Form Validation**: Reactive Forms
- **Pagination**: 무한스크롤, Cursor 기반
- **Offline Mode**: 오프라인 큐, 동기화

**Phase 5 - Test (테스트):**
- **Unit Test**: Riverpod ProviderContainer.test()
- **Widget Test**: Robot Pattern
- **Golden Test**: Alchemist
- **E2E Test**: Patrol

**Phase 6 - DevOps:**
- **CI/CD**: GitHub Actions (Flutter 3.24+)
- **Widgetbook**: 컴포넌트 카탈로그 3.20.2
- **easy-localization**: JSON 번역 관리

**Testing Pyramid:**
| Level | Coverage | Tools |
|-------|----------|-------|
| Unit | 60-70% | mocktail, ProviderContainer.test() |
| Widget | 15-20% | Robot Pattern |
| Golden | 10-15% | Alchemist |
| E2E | 5-10% | Patrol |

**Architecture Pattern:**
```
lib/
├── core/
│   ├── design_system/          # Atomic Design
│   │   ├── tokens/             # Colors, Typography, Spacing
│   │   ├── atoms/              # Button, Text, Input
│   │   ├── molecules/          # SearchBar, LabeledInput
│   │   ├── organisms/          # Header, LoginForm
│   │   └── templates/          # Page layouts
│   ├── error/                  # Failure, Either
│   ├── network/                # Dio, Interceptors
│   └── database/               # Drift
├── features/{feature}/
│   ├── domain/                 # Entities, Repositories, UseCases
│   ├── data/                   # DTOs, DataSources, RepoImpl
│   └── presentation/           # Pages, Widgets, Providers
└── routes/                     # GoRouter configuration
```

**Reference Files:**
- `_references/ARCHITECTURE-PATTERN.md`: Clean Architecture 가이드
- `_references/RIVERPOD-PATTERN.md`: Riverpod 3 AsyncNotifier 패턴
- `_references/ATOMIC-DESIGN-PATTERN.md`: Atomic Design 체계
- `_references/TEST-PATTERN.md`: TDD 피라미드
- `_references/NETWORK-PATTERN.md`: Dio + Retrofit 패턴
- `_references/DATABASE-PATTERN.md`: Drift DAO 패턴

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

**Legal Output** - `workspace/work-legal/{project-name}/`:
- `context/` - 계약 배경 및 당사자 정보
  - `{project}-context.md` - 컨텍스트 문서
- `analysis/` - 분석 결과물
  - `{project}-document-analysis.md` - 문서 분석
  - `{project}-risk-assessment.md` - 위험 평가
  - `{project}-summary.md` - 핵심 요약
- `review/` - 검토 결과물
  - `{project}-clause-comparison.md` - 조항 비교
  - `{project}-version-diff.md` - 버전 비교
  - `{project}-compliance.md` - 규제 준수 검토
- `execution/` - 실행 산출물
  - `{project}-redline.md` - 수정 제안
  - `{project}-negotiation-strategy.md` - 협상 전략
- `drafts/` - 계약서 초안
- `checklist/` - 서명 전 체크리스트
- `reports/` - 최종 리뷰 리포트

**Flutter Project Output** - `{project-root}/`:
- `lib/` - Clean Architecture 구조
  - `core/` - 공통 모듈 (design_system, error, network, database)
  - `features/` - 피처별 domain/data/presentation
  - `routes/` - GoRouter 설정
- `test/` - 테스트 코드
  - `unit/` - 유닛 테스트
  - `widget/` - 위젯 테스트
  - `golden/` - 골든 테스트
  - `helpers/` - 테스트 헬퍼
- `integration_test/` - E2E 테스트 (Patrol)
- `widgetbook/` - 컴포넌트 카탈로그
- `assets/translations/` - easy_localization JSON 파일

## Build Commands

### PPT Generation (pptxgenjs)

```bash
cd workspace/output/<project-name>
npm install

npm run build        # PPTX only
npm run build:pdf    # PDF only
npm run build:all    # Both PPTX + PDF
```

### Flutter Project (flutter-expert-agent)

```bash
# 프로젝트 생성
flutter create --org com.example my_app
cd my_app

# 의존성 설치 및 코드 생성
flutter pub get
dart run build_runner build --delete-conflicting-outputs

# 테스트 실행
flutter test                           # 전체 테스트
flutter test test/unit/               # 유닛 테스트만
flutter test --update-goldens         # 골든 테스트 업데이트

# E2E 테스트 (Patrol)
patrol test

# Widgetbook 실행
cd widgetbook && flutter run -d chrome

# Flavor 설정
flutter pub run flutter_flavorizr         # Flavor 초기 설정

# Flavor별 실행
flutter run --flavor dev -t lib/main_dev.dart
flutter run --flavor staging -t lib/main_staging.dart
flutter run --flavor prod -t lib/main_prod.dart

# Flavor별 릴리스 빌드
flutter build apk --flavor prod -t lib/main_prod.dart --release
flutter build appbundle --flavor prod -t lib/main_prod.dart --release

# Firebase 설정 (FlutterFire CLI)
dart pub global activate flutterfire_cli
flutterfire configure --project=my-app-dev \
  --out=lib/firebase_options_dev.dart \
  --android-app-id=com.example.app.dev \
  --ios-bundle-id=com.example.app.dev
```

## Key Files

| Path | Purpose |
|------|---------|
| `.claude/agents/<category>/<name>.md` | Agent configuration and workflow |
| `.claude/skills/<category>/<agent>-skills/<n>-<skill>/SKILL.md` | Individual skill definition |
| `.claude/skills/📝 콘텐츠/ppt-agent-skills/5-design-system/THEMES.md` | Theme selection guide |
| `.claude/skills/📝 콘텐츠/ppt-agent-skills/5-design-system/themes/INDEX.md` | Theme keyword mapping |
| `.claude/hooks/post-write-hook.sh` | PostToolUse hook for detecting agent/skill changes |
| `.claude/hooks/sync-docs.sh` | Script to scan and report agent/skill structure |
| `.claude/statusline.py` | Cost tracking statusline script |
| `.claude/agents/📣 마케팅/marketing-agent.md` | Marketing agent workflow and configuration |
| `.claude/skills/📣 마케팅/marketing-agent-skills/` | Marketing skills (15개) |
| `.claude/agents/💻 개발/flutter-to-nextjs-agent.md` | Flutter → Next.js 마이그레이션 agent |
| `.claude/skills/💻 개발/flutter-to-nextjs-skills/` | Flutter → Next.js 마이그레이션 skills (8개) |
| `.claude/skills/💻 개발/flutter-to-nextjs-skills/4-components/WIDGET-MAP.md` | Flutter Widget → React 매핑 레퍼런스 |
| `.claude/skills/💻 개발/flutter-to-nextjs-skills/5-state/STATE-MAP.md` | 상태관리 패턴 매핑 레퍼런스 |
| `.claude/skills/💻 개발/nextjs-boilerplate-skill/` | Next.js 보일러플레이트 생성 skill |
| `.claude/agents/💻 개발/flutter-expert-agent.md` | Flutter Expert Agent workflow |
| `.claude/skills/💻 개발/flutter-expert-agent-skills/` | Flutter Expert skills (26개 + 6 references) |
| `.claude/skills/💻 개발/flutter-expert-agent-skills/_references/` | Architecture, Riverpod, Test 패턴 레퍼런스 |
| `.claude/agents/⚖️ 법무/legal-contract-agent.md` | Legal contract agent workflow |
| `.claude/skills/⚖️ 법무/legal-contract-agent-skills/` | Legal contract skills (12개) |
| `workspace/work-blog/` | Tech blog drafts and research |
| `workspace/work-social/` | Social media drafts and calendar |
| `workspace/work-marketing/` | Marketing strategy and assets |
| `workspace/work-legal/` | Legal contract review and drafts |
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
