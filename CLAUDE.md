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
│   ├── work-design/            # Frontend design projects
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
├── 🎨 디자인/         # 프론트엔드 디자인
├── 🎯 기획/           # 서비스 기획 및 전략
└── (확장 가능)        # 🏗️ 설계, ✅ 품질보증, 🔍 QA, 🚀 인프라, 📚 문서화 등
```

| Category | Agent | Skills | Description |
|----------|-------|--------|-------------|
| **📝 콘텐츠** | ppt-agent | 11 | 프레젠테이션 제작 (Research → Export) |
| **📝 콘텐츠** | tech-blog-agent | 4 | Hashnode 블로그 작성 |
| **📝 콘텐츠** | social-media-agent | 15 | 멀티플랫폼 소셜미디어 콘텐츠 |
| **📣 마케팅** | marketing-agent | 15 | 마케팅 전략 및 실행물 제작 |
| **💻 개발** | flutter-to-nextjs-agent | 8 | Flutter → Next.js 마이그레이션 |
| **💻 개발** | flutter-expert-agent | 31 | Flutter 앱 개발 (Clean Architecture + Riverpod 3 + TDD) |
| **💻 개발** | nextjs-expert-agent | 31 | Next.js 웹앱 개발 (Clean Architecture + TanStack Query + Zustand + TDD + Vercel Best Practices) |
| **💻 개발** | fastapi-expert-agent | 37 | FastAPI 백엔드 개발 (Clean Architecture + SQLAlchemy 2.0 + TDD) |
| **⚖️ 법무** | legal-contract-agent | 12 | 계약서 검토, 위험 분석, 협상 지원 |
| **🎨 디자인** | frontend-design-agent | 18 | 독창적 웹/모바일 프론트엔드 디자인 |
| **🎯 기획** | planning-agent | 29 | 아이디어→런칭까지 서비스 기획 (Lean Canvas, PRD, GTM) |

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
│   ├── flutter-expert-agent-skills/ (31 skills + 6 references)
│   ├── nextjs-expert-agent-skills/  (31 skills + 8 references)
│   ├── fastapi-expert-agent-skills/ (37 skills + 6 references)
│   └── nextjs-boilerplate-skill/   (standalone)
├── ⚖️ 법무/
│   └── legal-contract-agent-skills/ (12 skills)
├── 🎨 디자인/
│   └── frontend-design-agent-skills/ (18 skills + 8 references)
└── 🎯 기획/
    └── planning-agent-skills/       (29 skills + 6 references)
```

### Standalone Skills

Agent에 속하지 않는 독립 Skill입니다. (💻 개발 카테고리에 위치)

| Skill | Description |
|-------|-------------|
| **nextjs-boilerplate** | AI 시대 최적화된 Next.js 15+ 프로젝트 보일러플레이트 생성. Clean Architecture, Supabase, Drizzle, Testing, Docker, MCP, CI/CD 선택적 지원. |
| **agent-browser-test** | Vercel agent-browser CLI 기반 AI 친화적 E2E 테스트 자동화. Refs 시스템으로 결정론적 요소 선택, 접근성 트리 기반 테스트. |

### PPT Design System

The PPT agent uses a comprehensive design system (`.claude/skills/📝 콘텐츠/ppt-agent-skills/5-design-system/`):
- **10 topic-based themes**: Healthcare, Education, Fintech, AI/Tech, Sustainability, Startup, Luxury, Creative, Real Estate, F&B
- **10 slide templates**: Cover, Contents, Section Divider, Content, Statistics, Split Layout, Team, Quote, Timeline, Closing
- **5 color palettes**: Executive Minimal, Sage Professional, Modern Dark, Corporate Blue, Warm Neutral
- **Typography system**: Pretendard (Korean) / Inter (English), 7-level hierarchy from Hero (72-96pt) to Label (10-12pt)

Theme files: `.claude/skills/📝 콘텐츠/ppt-agent-skills/5-design-system/themes/<number>-<theme>/THEME.md`

### Agent Browser Test Skill

Vercel Labs의 **agent-browser** CLI를 활용한 AI 친화적 E2E 테스트 자동화 스킬입니다.

**핵심 특징:**
- **Refs 시스템**: 결정론적 요소 선택 (`@e1`, `@e2` 등)
- **접근성 트리 기반**: LLM 워크플로우 최적화
- **세션 관리 내장**: `--session` 플래그로 상태 유지
- **JSON 출력**: `--json` 플래그로 프로그래밍 가능

**vs Playwright:**
| 항목 | agent-browser | Playwright |
|------|--------------|------------|
| 요소 선택 | Refs (결정론적) | CSS/XPath |
| AI 최적화 | 접근성 트리 | DOM 기반 |
| 사용 사례 | AI 에이전트 | 전통적 E2E |

**핵심 명령어:**
```bash
# 설치
npm install -g agent-browser
agent-browser install

# 스냅샷 (요소 맵 획득)
agent-browser open http://localhost:3000
agent-browser snapshot -i  # 상호작용 요소만

# Refs로 상호작용
agent-browser fill @e2 "user@example.com"
agent-browser click @e1
agent-browser screenshot result.png
```

**테스트 템플릿:**
- `templates/auth/login.sh`: 로그인 테스트
- `templates/auth/logout.sh`: 로그아웃 테스트
- `templates/forms/validation.sh`: 폼 검증 테스트
- `templates/crud/create-item.sh`: CRUD 테스트
- `templates/a11y/accessibility.sh`: 접근성 분석

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

**Best Practices 자동 적용:**
변환 시 Vercel Best Practices가 자동으로 적용됩니다:
| Flutter | Next.js | 규칙 |
|---------|---------|------|
| `GestureDetector(onTap:)` | `<button aria-label="">` | 접근성 |
| `FutureBuilder` | `<Suspense>` + async | Waterfall 제거 |
| `AnimatedContainer` | `motion.div` + GPU속성 | 성능 |
| 병렬 API 호출 | `Promise.all()` | 성능 |

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

### Frontend Design Agent

독창적이고 트렌디한 웹/모바일 프론트엔드 디자인을 생성하는 Agent입니다. 18개 Skills + 7개 References로 구성:

**핵심 철학 - Anti-AI-Slop:**
- **금지 폰트**: Inter, Roboto, Arial, Open Sans, Poppins
- **금지 패턴**: 보라색 그라데이션 on 흰배경, 동일 카드 나열
- **목표**: 매번 다른 독창적인 디자인, 맥락에 맞는 미적 방향

**Tech Stack:**
| Category | Technology | Version |
|----------|------------|---------|
| **Framework** | Next.js (App Router) | 15+ |
| **Styling** | Tailwind CSS | v4 |
| **Animation** | tw-animate-css + Framer Motion | 12+ |
| **Components** | shadcn/ui + Motion Primitives | latest |
| **Color Space** | oklch (perceptually uniform) | - |
| **Typography** | Variable fonts (wght, wdth) | - |

**12개 Aesthetic Templates:**
| # | 템플릿 | 특징 | 적용 분야 |
|---|--------|------|----------|
| 1 | Barely-There Minimal | 극도의 절제, 여백 | SaaS, AI |
| 2 | Soft Maximalism | 대담하지만 통제된 | 브랜드 |
| 3 | Anti-Design Chaos | 규칙 파괴, 비정형 | 포트폴리오 |
| 4 | Liquid Glass | Apple 스타일, 블러 | 앱 |
| 5 | Editorial Magazine | 매거진, 타이포 중심 | 미디어 |
| 6 | Retro-Futuristic | 90s + 사이버 | 게임 |
| 7 | Organic Natural | 자연, 부드러운 곡선 | 웰니스 |
| 8 | Luxury Refined | 고급, 세련된 | 럭셔리 |
| 9 | Tech Documentation | 매뉴얼 스타일 | 개발자 도구 |
| 10 | Brutalist Raw | 거친, 원시적 | 갤러리 |
| 11 | Playful Rounded | 친근한, 둥근 | 교육 |
| 12 | Grade-School Bold | 기본 색상, 명확한 | 스타트업 |

**Phase 1 - Discovery (탐색):**
- **Context**: 프로젝트 목적, 타겟 유저, 제약사항 파악
- **Inspiration**: 레퍼런스 수집, 트렌드 분석
- **Direction**: 12개 템플릿 중 미적 방향 결정

**Phase 2 - Foundation (기반):**
- **Typography**: 폰트 선택/페어링, Variable font
- **Color**: oklch 팔레트, 다크모드, 시맨틱 컬러
- **Spacing**: 간격 시스템, 그리드, 레이아웃
- **Motion**: 애니메이션 원칙, 이징, 지속시간

**Phase 3 - Components (컴포넌트):**
- **Primitives**: 버튼, 인풋, 배지 등 기본 요소
- **Patterns**: 카드, 모달, 드롭다운 복합 패턴
- **Effects**: 배경 효과, 글래스모피즘, 노이즈
- **Interactions**: 마이크로인터랙션, 호버/탭 피드백

**Phase 4 - Pages (페이지):**
- **Landing**: 랜딩 페이지, 히어로, CTA
- **Dashboard**: 대시보드, 데이터 시각화, SaaS
- **Content**: 블로그, 아티클, 에디토리얼
- **Mobile**: 모바일 퍼스트, 앱 스타일

**Phase 5 - Polish (완성):**
- **Accessibility**: WCAG 2.2, 신경다양성, 모션 감도
- **Responsive**: 반응형 검증, 브레이크포인트
- **Performance**: Core Web Vitals, 폰트/애니메이션 최적화

**다양성 보장 메커니즘:**
- Template Rotation: 이전에 사용하지 않은 템플릿 우선 선택
- Font Variation Matrix: 템플릿 내 폰트 조합 로테이션
- Color Palette Shuffle: 같은 템플릿이라도 accent color 변형
- Layout Variation Rules: Hero 섹션 6가지 변형
- Anti-Repetition Checklist: 매 디자인 생성 시 확인

**Command Guide:**
```
# 전체 프로세스
"UI 디자인해줘", "랜딩페이지 만들어줘", "대시보드 디자인 해줘"

# 개별 Skill 호출
/fd-context        # 컨텍스트 파악
/fd-inspiration    # 레퍼런스 수집
/fd-direction      # 미적 방향 결정
/fd-typography     # 타이포그래피
/fd-color          # 색상 팔레트
/fd-spacing        # 스페이싱
/fd-motion         # 애니메이션
/fd-primitives     # 기본 컴포넌트
/fd-patterns       # 복합 패턴
/fd-effects        # 배경 효과
/fd-interactions   # 마이크로인터랙션
/fd-landing        # 랜딩 페이지
/fd-dashboard      # 대시보드
/fd-content        # 콘텐츠 페이지
/fd-mobile         # 모바일 최적화
/fd-a11y           # 접근성 검증
/fd-responsive     # 반응형 검증
/fd-perf           # 성능 최적화
```

**Reference Files:**
- `_references/TYPOGRAPHY-RECIPES.md`: 50+ 폰트 조합, 금지 목록
- `_references/COLOR-SYSTEM.md`: oklch 팔레트, 다크모드
- `_references/MOTION-PATTERNS.md`: Framer Motion 레시피 30+ (GPU 가속 필수)
- `_references/BACKGROUND-EFFECTS.md`: 그래디언트, 노이즈, 글래스
- `_references/LAYOUT-TECHNIQUES.md`: 비대칭, 오버랩, Bento
- `_references/ANTI-PATTERNS.md`: AI Slop 체크리스트
- `_references/ACCESSIBILITY-CHECKLIST.md`: WCAG 2.2, 신경다양성
- `nextjs-expert-agent-skills/_references/UI-GUIDELINES.md`: 웹 인터페이스 100+ 규칙 (Cross-reference)

### Planning Agent

아이디어에서 런칭까지 서비스 기획을 지원하는 종합 Agent입니다. 29개 Skills + 6개 References로 구성:

**타겟 사용자:**
- 1인 창업자 / 사이드 프로젝트
- 스타트업 PM / 기획자
- 팀 단위 프로젝트

**출력 형식:** Markdown (Notion 호환)

**Phase 1 - Discovery (발견):**
- **Idea Intake**: Problem-Solution Fit 분석, 아이디어 구체화
- **Value Proposition**: UVP Canvas, Why Now, Differentiation
- **Target User**: 페르소나, JTBD, 공감 지도

**Phase 2 - Research (조사):**
- **Market Research**: TAM/SAM/SOM, Porter's 5 Forces, Why Now
- **Competitor Analysis**: Feature Matrix, Positioning Map
- **User Research**: 인터뷰 가이드, 설문 설계

**Phase 3 - Validation (검증):**
- **Lean Canvas**: 9블록 비즈니스 모델
- **Business Model**: Unit Economics, LTV/CAC
- **Pricing Strategy**: 가격 모델, 플랜 설계
- **MVP Definition**: MoSCoW 우선순위, 가설 검증
- **Legal Checklist**: 서비스 유형별 법적 요구사항

**Phase 4 - Specification (명세):**
- **PRD**: Product Requirements Document
- **Feature Spec**: User Stories, Acceptance Criteria
- **Information Architecture**: 사이트맵, 네비게이션
- **User Flow**: 플로우 다이어그램, 상태 전이
- **Wireframe Guide**: 레이아웃, 컴포넌트
- **Data Strategy**: 이벤트 트래킹, 메트릭

**Phase 5 - Estimation (산정):**
- **Tech Stack**: 기술 추천, Make vs Buy
- **Effort Estimation**: T-Shirt Sizing, 마일스톤
- **Team Structure**: 역할 정의, 채용 계획

**Phase 6 - Design Direction (디자인 방향):**
- **UX Strategy**: UX 원칙, Aha Moment
- **Brand Direction**: 톤앤매너, 시각적 방향

**Phase 7 - Execution (실행):**
- **Roadmap**: 마일스톤, Phase 전환 기준
- **Risk Management**: 리스크 매트릭스, 대응 계획
- **KPI/OKR**: North Star Metric, AARRR
- **Operation Plan**: 운영 체계, 인시던트 관리

**Phase 8 - Launch Prep (런칭 준비):**
- **Growth Strategy**: AARRR 퍼널, 채널 전략
- **Pitch Deck**: 투자 유치용 12장 구조
- **GTM Strategy**: Go-to-Market, 런칭 타임라인

**Frameworks Used:**
| Framework | 용도 |
|-----------|------|
| Lean Canvas | 비즈니스 모델 |
| TAM/SAM/SOM | 시장 규모 |
| MoSCoW | 우선순위 |
| JTBD | 고객 이해 |
| Unit Economics | 수익성 분석 |
| AARRR | 성장 지표 |
| OKR | 목표 설정 |

**Reference Files:**
- `_references/LEAN-CANVAS-TEMPLATE.md`: Lean Canvas 템플릿
- `_references/PRD-TEMPLATE.md`: PRD 템플릿
- `_references/PRICING-MODELS.md`: 가격 모델 가이드
- `_references/LEGAL-CHECKLIST.md`: 법적 요구사항
- `_references/TECH-STACK-GUIDE.md`: 기술 스택 가이드
- `_references/PITCH-DECK-STRUCTURE.md`: 피치덱 구조

**Output Structure:** `workspace/work-plan/{project-name}/`
```
01-discovery/           # 아이디어, 가치제안, 타겟유저
02-research/            # 시장조사, 경쟁분석, 사용자조사
03-validation/          # Lean Canvas, 비즈니스모델, MVP
04-specification/       # PRD, 기능명세, IA, 플로우
05-estimation/          # 기술스택, 공수, 팀구성
06-design/              # UX전략, 브랜드방향
07-execution/           # 로드맵, 리스크, KPI, 운영
08-launch/              # 성장전략, 피치덱, GTM
```

**Agent 연계:**
- Frontend Design Agent: 실제 UI 디자인
- Marketing Agent: GTM 실행
- PPT Agent: 피치덱 제작
- Development Agents: 개발 착수

### Flutter Expert Agent

현대적인 Flutter 앱 개발을 위한 종합 Agent입니다. 31개 Skills + 6개 References로 구성:

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
| **Supabase** | supabase_flutter (PostgreSQL) | ^2.12.0 |
| **보안** | flutter_secure_storage, local_auth | ^9.2.0 |
| **딥링크** | app_links | ^6.3.2 |
| **배포** | Fastlane, Shorebird | - |

**Phase 1 - Setup (설정):**
- **Project Setup**: pubspec.yaml, 디렉토리 구조 (Clean Architecture)
- **Architecture**: Domain/Data/UI 레이어 설계
- **Flavor**: dev/staging/prod 환경 분리, envied 환경 변수
- **Firebase**: Auth, Firestore, FCM, Crashlytics, Analytics 등
- **Supabase**: PostgreSQL, Auth, Storage, Realtime, Edge Functions

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
- **Deployment**: Fastlane 자동 배포, Shorebird OTA

**Phase 7 - Security & Accessibility:**
- **Security**: Secure Storage, SSL Pinning, 난독화, Root 탐지
- **Deep Link**: app_links, Universal/App Links
- **Accessibility**: Semantics, 색상 대비, 터치 타겟

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

### Next.js Expert Agent

현대적인 Next.js 웹앱 개발을 위한 종합 Agent입니다. 31개 Skills + 8개 References로 구성:

**Vercel Best Practices 통합:**
- Impact Level 시스템: CRITICAL(🔴) → HIGH(🟠) → MEDIUM(🟡) → LOW(🔵)
- 45가지 React/Next.js 성능 규칙 내장
- 100+ 웹 인터페이스 가이드라인 (접근성, 폼, 애니메이션)

**Tech Stack:**
| Category | Technology | Version |
|----------|------------|---------|
| **Framework** | Next.js 15+ (App Router, Server Components) | ^15.1.0 |
| **Server State** | TanStack Query (useQuery, useMutation) | ^5.62.0 |
| **Client State** | Zustand (with persist, immer) | ^5.0.2 |
| **URL State** | nuqs (type-safe query params) | ^2.2.3 |
| **UI** | shadcn/ui + Tailwind CSS v4 | latest |
| **Forms** | React Hook Form + Zod | ^7.54.0 |
| **Auth** | Auth.js v5 or Clerk | ^5.0.0 |
| **Database** | Drizzle ORM + PostgreSQL (Neon) | ^0.36.4 |
| **Server Actions** | next-safe-action | ^7.10.0 |
| **Testing** | Vitest + Playwright + MSW | ^2.1.8 |
| **Animation** | Framer Motion | ^11.15.0 |
| **i18n** | next-intl | ^3.26.3 |

**Phase 1 - Setup (설정):**
- **Project Setup**: package.json, 디렉토리 구조 (Clean Architecture)
- **Architecture**: UI/Domain/Data 레이어 설계, Feature 모듈
- **Design System**: shadcn/ui 설정, Tailwind v4, Dark Mode
- **Database**: Drizzle ORM, 스키마, 마이그레이션
- **Auth**: Auth.js v5 또는 Clerk 설정
- **Env**: T3 Env 타입 안전 환경 변수
- **i18n**: next-intl 다국어 설정

**Phase 2 - Core (핵심):**
- **Schema**: Zod 스키마 패턴
- **API Client**: TanStack Query Provider, Query/Mutation 훅
- **State**: Zustand Store 패턴, Selectors
- **Server Action**: next-safe-action 미들웨어 체인
- **Error Handling**: Error Boundary, Sentry
- **Middleware**: Edge Middleware 패턴

**Phase 3 - Feature (기능):**
- **Feature**: Feature 기반 모듈 구조
- **Form**: React Hook Form + Zod 통합
- **Routing**: App Router, Parallel/Intercepting Routes
- **Pagination**: Offset/Cursor 기반, 무한 스크롤
- **File Upload**: Vercel Blob, S3
- **Realtime**: SSE, Pusher

**Phase 4 - Test (테스트):**
- **Unit Test**: Vitest, MSW, Service/Schema/Hook 테스트
- **Integration Test**: RTL, 컴포넌트 통합 테스트
- **E2E Test**: Playwright, Page Object Model
- **Visual Test**: Storybook, Snapshot

**Phase 5-6 - Optimization & DevOps:**
- **Performance**: 이미지/폰트 최적화, Core Web Vitals
- **SEO**: Metadata API, Sitemap, Structured Data
- **CI/CD**: GitHub Actions, Vercel 배포
- **Monorepo**: Turborepo, 공유 패키지

**Phase 7 - Integration:**
- **Analytics**: Google Analytics 4, Vercel Analytics
- **Email**: Resend, React Email 템플릿
- **Payment**: Stripe 일회성/구독 결제
- **Security**: Rate Limiting, CSRF, 보안 헤더

**Testing Pyramid:**
| Level | Coverage | Tools |
|-------|----------|-------|
| Unit | 60-70% | Vitest, MSW |
| Integration | 15-20% | RTL, custom render |
| E2E | 10-15% | Playwright |
| Visual | 5% | Storybook, Chromatic |

**Architecture Pattern:**
```
app/
├── (auth)/                     # Auth 레이아웃 그룹
├── (dashboard)/                # Dashboard 레이아웃 그룹
├── api/                        # API Routes
├── layout.tsx                  # Root Layout
└── providers.tsx               # Client Providers

features/{feature}/
├── api/                        # API Service
├── components/                 # Feature Components
├── hooks/                      # Query/Mutation Hooks
├── actions/                    # Server Actions
├── schemas/                    # Zod Schemas
├── stores/                     # Zustand Stores
└── types/                      # TypeScript Types

lib/
├── db/                         # Drizzle Client & Schema
├── auth/                       # Auth.js Config
├── actions/                    # safe-action Client
└── utils.ts                    # Utilities
```

**Reference Files:**
- `_references/ARCHITECTURE-PATTERN.md`: Clean Architecture 가이드
- `_references/STATE-PATTERN.md`: TanStack Query + Zustand 패턴
- `_references/COMPONENT-PATTERN.md`: Atomic Design + shadcn/ui
- `_references/TEST-PATTERN.md`: TDD 피라미드
- `_references/SERVER-ACTION-PATTERN.md`: next-safe-action 패턴
- `_references/DATABASE-PATTERN.md`: Drizzle ORM 패턴
- `_references/REACT-PERF-RULES.md`: Vercel 45가지 성능 규칙 (Impact Level 시스템)
- `_references/UI-GUIDELINES.md`: 웹 인터페이스 100+ 규칙 (접근성, 폼, 애니메이션)

### FastAPI Expert Agent

현대적인 FastAPI 백엔드 개발을 위한 종합 Agent입니다. 37개 Skills + 6개 References로 구성:

**Tech Stack:**
| Category | Technology | Version |
|----------|------------|---------|
| **Framework** | FastAPI (async, Pydantic V2) | ^0.115.4 |
| **Database** | SQLAlchemy 2.0 (asyncpg) | ^2.0.36 |
| **Migrations** | Alembic | ^1.14.0 |
| **Validation** | Pydantic V2 | ^2.10.0 |
| **Auth** | OAuth2 + JWT (PyJWT) | ^2.10.1 |
| **Background Tasks** | Celery / ARQ | ^5.4.0 |
| **Caching** | Redis (redis-py) | ^5.2.0 |
| **Logging** | structlog | ^24.4.0 |
| **Testing** | pytest + pytest-asyncio | ^8.3.0 |
| **Container** | Docker + Kubernetes | - |
| **Observability** | Prometheus + OpenTelemetry | - |

**Phase 1 - Setup (설정):**
- **Project Setup**: pyproject.toml, uv, 디렉토리 구조 (Clean Architecture)
- **Architecture**: API/Application/Domain/Infrastructure 레이어 설계
- **Database Setup**: SQLAlchemy 2.0 async, asyncpg, 연결 풀링
- **Environment**: pydantic-settings, 환경 변수 관리
- **DI Container**: FastAPI Depends, 의존성 주입

**Phase 2 - Core (핵심):**
- **Service Layer**: Application Services, Use Cases
- **Error Handling**: Result 패턴, Exception Hierarchy
- **Logging**: structlog, 요청 추적
- **Middleware**: CORS, GZip, Request ID
- **Health Check**: Liveness/Readiness probes
- **Validation**: Pydantic V2 스키마, 커스텀 Validators

**Phase 3 - Security (보안):**
- **Authentication**: OAuth2 + JWT, 토큰 관리
- **Authorization**: RBAC, Permission Guards
- **API Keys**: 키 발급, 해싱, 환경별 관리
- **Security Hardening**: CSP, Rate Limiting, HTTPS

**Phase 4 - Data Layer (데이터):**
- **Repository Pattern**: Abstract Repository, SQLAlchemy 구현
- **Unit of Work**: 트랜잭션 관리
- **Query Optimization**: 인덱싱, N+1 방지, Eager Loading
- **Caching**: Redis 캐싱, 캐시 무효화

**Phase 5 - Feature (기능):**
- **Feature Implementation**: Clean Architecture 피처 구현
- **File Upload**: Local/S3 스토리지
- **WebSocket**: ConnectionManager, Redis Pub/Sub 스케일링
- **Background Tasks**: Celery/ARQ, 비동기 작업
- **Scheduled Jobs**: APScheduler, Cron 작업

**Phase 6 - API Design (API 설계):**
- **OpenAPI Docs**: Swagger UI, ReDoc, 커스텀 문서화
- **API Versioning**: URL Path/Header 버저닝
- **Response Design**: 표준 응답 래퍼, 페이지네이션, 에러 응답

**Phase 7 - Testing (테스트):**
- **Unit Test**: pytest, Factory Boy, Mock
- **Integration Test**: TestClient, DB 트랜잭션 롤백
- **E2E Test**: Testcontainers, Docker Compose

**Phase 8 - DevOps (배포):**
- **Docker**: 멀티스테이지 빌드, Docker Compose
- **Kubernetes**: Deployment, HPA, Ingress, Helm
- **CI/CD**: GitHub Actions, GitLab CI
- **Observability**: Prometheus 메트릭, OpenTelemetry 트레이싱, Sentry

**Testing Pyramid:**
| Level | Coverage | Tools |
|-------|----------|-------|
| Unit | 60-70% | pytest, Factory Boy, mock |
| Integration | 20-25% | TestClient, respx |
| E2E | 5-10% | testcontainers |

**Architecture Pattern:**
```
app/
├── api/                        # Presentation Layer
│   ├── v1/
│   │   ├── routes/             # API endpoints
│   │   └── dependencies.py     # FastAPI Depends
│   └── router.py               # Main router
├── application/                # Application Layer
│   ├── services/               # Business logic
│   ├── use_cases/              # Use case handlers
│   └── schemas/                # Pydantic DTOs
├── domain/                     # Domain Layer
│   ├── entities/               # Domain entities
│   ├── repositories/           # Repository interfaces
│   └── value_objects/          # Value objects
├── infrastructure/             # Infrastructure Layer
│   ├── database/               # SQLAlchemy models, session
│   ├── repositories/           # Repository implementations
│   ├── security/               # Password, JWT
│   ├── cache/                  # Redis
│   └── services/               # External services
├── core/                       # Shared/Core
│   ├── config.py               # Settings
│   └── exceptions.py           # Exception hierarchy
└── main.py                     # Application entry
```

**Reference Files:**
- `_references/ARCHITECTURE-PATTERN.md`: Clean Architecture 가이드
- `_references/REPOSITORY-PATTERN.md`: Repository 패턴
- `_references/AUTH-PATTERN.md`: 인증/인가 패턴
- `_references/TEST-PATTERN.md`: TDD 피라미드
- `_references/API-PATTERN.md`: REST API 설계 패턴
- `_references/DEPLOYMENT-PATTERN.md`: 배포 패턴

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

**Planning Output** - `workspace/work-plan/{project-name}/`:
- `01-discovery/` - 아이디어, 가치제안, 타겟유저
  - `idea-intake.md` - Problem-Solution Fit
  - `value-proposition.md` - UVP Canvas
  - `target-user.md` - 페르소나, JTBD
- `02-research/` - 시장조사, 경쟁분석, 사용자조사
  - `market-research.md` - TAM/SAM/SOM
  - `competitor-analysis.md` - 경쟁사 분석
  - `user-research.md` - 인터뷰, 설문
- `03-validation/` - 검증 단계
  - `lean-canvas.md` - 9블록 캔버스
  - `business-model.md` - Unit Economics
  - `pricing-strategy.md` - 가격 전략
  - `mvp-definition.md` - MVP 범위
  - `legal-checklist.md` - 법적 요구사항
- `04-specification/` - 명세 단계
  - `prd.md` - Product Requirements
  - `feature-spec.md` - 기능 명세
  - `information-architecture.md` - IA
  - `user-flow.md` - 사용자 플로우
  - `wireframe-guide.md` - 와이어프레임
  - `data-strategy.md` - 데이터 전략
- `05-estimation/` - 산정 단계
  - `tech-stack.md` - 기술 스택
  - `effort-estimation.md` - 공수 산정
  - `team-structure.md` - 팀 구성
- `06-design/` - 디자인 방향
  - `ux-strategy.md` - UX 전략
  - `brand-direction.md` - 브랜드 방향
- `07-execution/` - 실행 단계
  - `roadmap.md` - 로드맵
  - `risk-management.md` - 리스크 관리
  - `kpi-okr.md` - KPI/OKR
  - `operation-plan.md` - 운영 계획
- `08-launch/` - 런칭 준비
  - `growth-strategy.md` - 성장 전략
  - `pitch-deck-structure.md` - 피치덱 구조
  - `gtm-strategy.md` - GTM 전략

**Design Output** - `workspace/work-design/{project-name}/`:
- `context/` - 프로젝트 컨텍스트 문서
  - `{project}-context.md` - 브리핑 및 요구사항
- `inspiration/` - 레퍼런스 및 영감
  - `mood-board.md` - 무드보드
  - `trend-analysis.md` - 트렌드 분석
  - `competitor-analysis.md` - 경쟁사 분석
- `direction/` - 미적 방향 결정
  - `aesthetic-direction.md` - 선택된 디자인 방향
  - `decision-rationale.md` - 결정 근거
- `tokens/` - 디자인 토큰
  - `typography.css` - 타이포그래피 토큰
  - `colors.css` - 색상 토큰
  - `spacing.css` - 간격 토큰
  - `motion.css` - 애니메이션 토큰
- `components/` - 생성된 컴포넌트
- `pages/` - 페이지 레이아웃

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
| `.claude/skills/💻 개발/agent-browser-test-skill/` | Vercel agent-browser E2E 테스트 skill |
| `.claude/skills/💻 개발/agent-browser-test-skill/templates/` | 테스트 스크립트 템플릿 (auth, forms, crud, a11y) |
| `.claude/agents/💻 개발/flutter-expert-agent.md` | Flutter Expert Agent workflow |
| `.claude/skills/💻 개발/flutter-expert-agent-skills/` | Flutter Expert skills (31개 + 6 references) |
| `.claude/skills/💻 개발/flutter-expert-agent-skills/_references/` | Architecture, Riverpod, Test 패턴 레퍼런스 |
| `.claude/agents/💻 개발/nextjs-expert-agent.md` | Next.js Expert Agent workflow |
| `.claude/skills/💻 개발/nextjs-expert-agent-skills/` | Next.js Expert skills (31개 + 6 references) |
| `.claude/skills/💻 개발/nextjs-expert-agent-skills/_references/` | Architecture, State, Test 패턴 + Vercel Best Practices 레퍼런스 |
| `.claude/skills/💻 개발/nextjs-expert-agent-skills/_references/REACT-PERF-RULES.md` | Vercel 45가지 React 성능 규칙 (Impact Level 시스템) |
| `.claude/skills/💻 개발/nextjs-expert-agent-skills/_references/UI-GUIDELINES.md` | 웹 인터페이스 100+ 가이드라인 (접근성, 폼, 애니메이션) |
| `.claude/agents/💻 개발/fastapi-expert-agent.md` | FastAPI Expert Agent workflow |
| `.claude/skills/💻 개발/fastapi-expert-agent-skills/` | FastAPI Expert skills (37개 + 6 references) |
| `.claude/skills/💻 개발/fastapi-expert-agent-skills/_references/` | Architecture, Repository, Auth, API 패턴 레퍼런스 |
| `.claude/agents/⚖️ 법무/legal-contract-agent.md` | Legal contract agent workflow |
| `.claude/skills/⚖️ 법무/legal-contract-agent-skills/` | Legal contract skills (12개) |
| `.claude/agents/🎨 디자인/frontend-design-agent.md` | Frontend Design Agent workflow |
| `.claude/skills/🎨 디자인/frontend-design-agent-skills/` | Frontend Design skills (18개 + 7 references) |
| `.claude/agents/🎯 기획/planning-agent.md` | Planning agent workflow and configuration |
| `.claude/skills/🎯 기획/planning-agent-skills/` | Planning skills (29개 + 6 references) |
| `.claude/skills/🎯 기획/planning-agent-skills/_references/` | Lean Canvas, PRD, Pricing, Legal, Tech Stack 레퍼런스 |
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
