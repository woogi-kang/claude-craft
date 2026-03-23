# Agent Orchestration

사용자 요청을 분석하여 적절한 에이전트, 스킬, 커맨드로 라우팅하는 규칙.

---

## 1. 라우팅 의사결정 트리

사용자 요청을 받으면 아래 순서로 판단한다:

```
1. 슬래시 커맨드와 매칭되는가? → Skill 도구로 실행
2. 여러 도메인 병렬 협업이 필요한가? → /team 제안 (자동 DAG)
3. 단일 도메인 에이전트가 필요한 복합 작업인가? → Agent 도구로 위임
4. 스킬 자동 트리거에 해당하는가? → Skill 도구로 실행
5. 단순 코드 작업인가? → 직접 처리 (Glob/Grep/Read/Edit)
6. 탐색이 필요한가? → Explore 서브에이전트
```

---

## 2. 도메인 에이전트 라우팅 매트릭스

### 💻 개발

| 키워드/의도 | 에이전트 | 언제 사용 |
|-------------|----------|-----------|
| FastAPI, Python API, async API | `fastapi-agent` | API 설계/구현/테스트 전 과정 |
| Flutter, Dart, Riverpod, 모바일 앱 | `flutter-agent` | Flutter 앱 설계/구현/테스트 |
| Next.js, React, App Router, 웹 앱 | `nextjs-agent` | Next.js 웹 앱 설계/구현/테스트 |
| Figma → Next.js, 피그마 웹 변환 | `figma-to-nextjs` | Figma 디자인을 Next.js 코드로 변환 |
| Figma → Flutter, 피그마 앱 변환 | `figma-to-flutter` | Figma 디자인을 Flutter 코드로 변환 |
| Flutter → Next.js, 마이그레이션 | `flutter-to-nextjs` | Flutter 앱을 Next.js로 전환 |
| TDD, 테스트 루프, 100% 패스 | `tdd-loop-agent` | 테스트가 모두 통과할 때까지 자율 루프 |
| 빌드 에러, 타입 에러, 컴파일 에러 | `build-resolver-agent` | 최소 diff로 빌드 에러 수정 |
| 데드코드, 정리, cleanup | `deadcode-cleaner-agent` | 미사용 코드/임포트/의존성 제거 |

### 🎯 기획

| 키워드/의도 | 에이전트 | 언제 사용 |
|-------------|----------|-----------|
| 서비스 기획, 아이디어 검증, PRD, MVP | `planning-agent` | 아이디어 → 출시까지 8단계 기획 |
| 비즈니스 모델, 시장조사, 경쟁 분석 | `planning-agent` | 디스커버리/리서치 단계 |
| 공수 산정, 로드맵, GTM | `planning-agent` | 실행 계획 수립 |

### 🎨 디자인

| 키워드/의도 | 에이전트 | 언제 사용 |
|-------------|----------|-----------|
| UI/UX 디자인, 프론트엔드 디자인 | `ui-design-agent` | 독창적 웹/모바일 UI 디자인 생성 |
| Figma MCP, 디자인 추출 | `figma-flutter-agent` | Figma에서 디자인 컨텍스트 추출 → Flutter 코드 |

### 📝 콘텐츠

| 키워드/의도 | 에이전트 | 언제 사용 |
|-------------|----------|-----------|
| PPT, 발표자료, 프레젠테이션 | `presentation-agent` | PPT 리서치 → 제작 전 과정 |
| 소셜 미디어, SNS 콘텐츠 | `social-media-agent` | 멀티 플랫폼 소셜 콘텐츠 제작 |
| 기술 블로그, Hashnode | `tech-blog-agent` | 블로그 글 작성 → 발행 |
| 이모티콘, 캐릭터, 스티커 | `emoticon-orchestrator` | AI 이모티콘 제작 워크플로우 |

### 📣 마케팅

| 키워드/의도 | 에이전트 | 언제 사용 |
|-------------|----------|-----------|
| 마케팅 전략, 광고 카피, 캠페인 | `marketing-agent` | 마케팅 리서치 → 실행 산출물 |
| SEO, 키워드, 트래픽, 콘텐츠 최적화 | `seo-orchestrator` | SEO + 콘텐츠 마케팅 통합 |

### ⚖️ 법무

| 키워드/의도 | 에이전트 | 언제 사용 |
|-------------|----------|-----------|
| 계약서 검토, NDA, 위험 분석 | `legal-contract-agent` | 계약 검토/초안/위험 분석 |
| 법인 설립, 등기, 주총, 정관 | `corporate-legal-agent` | 법인 운영 전반 |

### 💰 재무

| 키워드/의도 | 에이전트 | 언제 사용 |
|-------------|----------|-----------|
| 결제, 구독, 매출, Lemon Squeezy | `payment-orchestrator` | 결제 시스템 구축/관리 |
| 재무, 영수증, 세금계산서, 비용 분석 | `finance-orchestrator` | 재무 보고/영수증 처리 |

### 🔍 리뷰

| 키워드/의도 | 에이전트 | 언제 사용 |
|-------------|----------|-----------|
| 리뷰, 피드백, 평가, 검토 | `review-orchestrator` | 멀티 관점 리뷰 오케스트레이션 |

> **리뷰 오케스트레이터**는 요청을 분석하여 하위 리뷰어(code, architecture, security, design, content)에게 자동 분배한다. 직접 하위 리뷰어를 호출하지 않는다.

---

## 3. 스킬 자동 트리거

아래 키워드가 사용자 요청에 포함되면 해당 스킬을 **자동으로** 실행한다:

| 키워드 | 스킬 | 설명 |
|--------|------|------|
| UI 구현, 컴포넌트, shadcn, Tailwind, 다크모드 | `ui-ux-pro-max` | 10개 스택 대응 UI/UX 인텔리전스 |
| 디자인 시스템, 토큰, 컴포넌트 스펙 | `design-system` | 3-레이어 토큰 아키텍처 |
| 로고 만들기, logo, brand mark, favicon, 앱 아이콘 | `logo-creator` | AI 로고 생성 전용 (배치 20개 + 프리뷰 + 후처리) |
| 브랜드 아이덴티티, CIP, 배너, 아이콘 | `design` | 종합 디자인 (CIP, 배너, 아이콘 등) |
| 배너, 소셜 배너, 광고 배너 | `banner-design` | 22가지 스타일 배너 디자인 |
| 슬라이드, 프레젠테이션 | `slides` | Chart.js 기반 HTML 프레젠테이션 |
| 브랜드 보이스, 톤앤매너, 메시징 | `brand` | 브랜드 일관성 관리 |
| LinkedIn, Twitter, SNS, 바이럴, 게시물 | `social-content` | 소셜 미디어 콘텐츠 제작 |
| App Store 스크린샷, 마케팅 에셋 | `app-store-screenshots` | iOS 스크린샷 생성 |
| Notion 문서 | `notion-core` | Notion 포맷팅 |
| Obsidian 문서, vault | `obsidian-core` | Obsidian 마크다운 |
| NotebookLM, 팟캐스트 생성 | `notebooklm` | Google NotebookLM API |
| 이력서, 경력기술서, 포트폴리오 | `resume-writer` | 이력서 변환 |

---

## 4. 슬래시 커맨드 추천

사용자의 작업 흐름에서 아래 커맨드를 **적절한 시점에 제안**한다:

### 개발 흐름
```
코드 작성 → /verify (6단계 검증) → /commit (스마트 커밋)
            /tdd (TDD 사이클)    /test-coverage (커버리지 분석)
```

### 기획/리뷰 흐름
```
기획 완료 → /review (멀티 LLM 리뷰)
         → /multi-plan (멀티 LLM 기획)
```

### 팀 오케스트레이션
```
/team "작업 설명"          → 자연어 → DAG 자동 구성 + 실행
/team-launch <tmpl> --goal → 템플릿 기반 원커맨드 실행
/orchestrate               → 병렬 워크트리 실행 (수동 plan.json)
대시보드: python3 scripts/orchestrate-dashboard.py --open
```

### 멀티 LLM 협업
```
/multi-plan → 기획 (Claude + Gemini + Codex 분석)
/multi-execute → 구현 (프로토타입 정제)
```

### 세션/상태 관리
```
/save-session → 작업 중단 시 세션 저장
/resume-session → 이전 세션 복원
/checkpoint → 작업 전후 상태 비교
```

### 관리/감사
```
/audit → 하니스 설정 감사 (0-100)
/skill-audit → 스킬 품질 감사
/today → 데일리 컨텍스트 기반 작업 실행
```

---

## 5. 워크플로우 체인 패턴

자주 사용되는 에이전트/스킬 연계 패턴:

### 새 서비스 기획 → 구현
```
planning-agent (기획)
  → ui-design-agent (UI 디자인)
  → nextjs-agent 또는 flutter-agent (구현)
  → /verify (검증)
  → /review (리뷰)
```

### Figma 디자인 → 프로덕션 코드
```
figma-to-nextjs 또는 figma-to-flutter (변환)
  → /verify (빌드/타입/린트 검증)
  → review-orchestrator (코드 + 디자인 리뷰)
```

### 기존 코드 개선
```
deadcode-cleaner-agent (데드코드 정리)
  → build-resolver-agent (빌드 에러 수정)
  → /verify → /commit
```

### 콘텐츠 제작 파이프라인
```
marketing-agent (전략 수립)
  → social-media-agent (SNS 콘텐츠)
  → tech-blog-agent (블로그)
  → seo-orchestrator (SEO 최적화)
```

---

## 6. 모델 라우팅

| 작업 유형 | 모델 | 예시 |
|-----------|------|------|
| 아키텍처 설계, 복잡한 추론 | Opus | 기획, 리뷰, 전략 수립 |
| 일반 구현, 코드 작성 | Sonnet | 기능 구현, 리팩토링 |
| 탐색, 단순 검색, 분류 | Haiku | 파일 탐색, 키워드 검색 |

---

## 7. 직접 처리 vs 에이전트 위임

| 상황 | 처리 방식 |
|------|-----------|
| 특정 파일/함수 찾기 | Glob/Grep 직접 사용 |
| 파일 1-3개 수정 | Read/Edit 직접 사용 |
| 단순 질문 답변 | 직접 응답 |
| 복합 탐색 (3+ 쿼리 예상) | Explore 서브에이전트 |
| 도메인 전문성 필요 | 도메인 에이전트 위임 |
| 여러 도메인 병렬 작업 (자연어) | /team (자동 DAG 구성) |
| 여러 도메인 병렬 작업 (템플릿) | /team-launch (TOML 기반) |
| 여러 도메인 병렬 작업 (수동) | /orchestrate (직접 plan.json) |

---

## 8. 병렬 실행 원칙

- 독립적인 조회/탐색은 **항상 병렬** 실행
- 에이전트 간 의존성이 없으면 **동시 호출**
- 리뷰 오케스트레이터는 내부적으로 하위 리뷰어를 병렬 실행

---

## 9. 컨텍스트 관리

- 컨텍스트의 마지막 20%에서는 대규모 작업을 시작하지 않는다
- 큰 파일은 필요한 부분만 읽기 (offset/limit 활용)
- 서브에이전트로 컨텍스트를 보호한다 (탐색 결과가 메인 컨텍스트를 오염시키지 않도록)
- 중간 결과는 파일에 저장하여 컨텍스트 절약
