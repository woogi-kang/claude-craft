# Marketing Skills 업그레이드 종합 계획

**Date**: 2026-03-17
**Source**: `coreyhaines31/marketingskills` (v1.2.0, ⭐14K) vs 로컬 마케팅 스킬 41개
**분석 방법**: 4개 병렬 에이전트 (Local Audit, Remote Analysis, Gap Analysis, Integration Strategy)

---

## 1. 현재 상태 진단

### 로컬 스킬 품질 등급 요약

| 등급 | 스킬 수 | 해당 스킬 |
|:----:|:-------:|----------|
| **A** | 20개 | context-intake, persona, positioning, strategy, campaign, copywriting, landing-page, email-sequence, analytics-kpi, compliance, repurpose, brand-direction, pitch-deck, revenue-analytics, dunning-manager 등 |
| **A-** | 12개 | market-research, funnel, customer-journey, ab-testing, review, research, validation, visual, hashtag, schedule, engagement, analytics 등 |
| **B+** | 5개 | ads-creative(TikTok 누락), social-strategy(TikTok 누락), content-4(TikTok 누락), approval, growth-strategy |
| **B~C+** | 4개 | gtm-strategy(B), competitor-analysis(B), marketing-ideas(C+), positioning-ideas(C+) |

### 핵심 발견

**강점** (유지해야 할 것):
- 마케팅 파이프라인(1→15) 순차 워크플로우 — 체계적이고 production-grade
- 소셜미디어 12개 스킬 — remote의 1개 스킬 대비 압도적
- 2025 트렌드 반영 (숏폼, AI 도구, 커뮤니티)
- 한국 시장 특화 (KST 스케줄링, 네이버/카카오, 한국 규정)

**약점** (업그레이드 필요):
- SEO 전무 — seo-audit, ai-seo, schema-markup, programmatic-seo 없음
- CRO 부족 — 1개 LP 스킬 vs remote의 6개 전문 CRO 스킬
- 콜드 아웃리치 없음 — B2B 영업 채널 부재
- 가격 전략 미흡 — Van Westendorp, Good-Better-Best 없음
- 이탈 방지 미흡 — dunning만 있고 cancel flow/save offer/health score 없음
- 마케팅 심리학 없음 — 39+ 멘탈 모델 부재
- RevOps 없음 — 리드 스코어링/라우팅/MQL 정의 부재
- 세일즈 자료 없음 — 피치덱/원페이저/반론 대응 부재

---

## 2. 액션 플랜: 3단계 접근

### Phase 1: 신규 스킬 도입 (중복 없는 순수 추가)

로컬에 전혀 없는 17개 스킬을 새 카테고리로 추가.

```
.claude/skills/📣 마케팅/
├── marketing-agent-skills/     # 기존 15개 (유지)
├── seo-agent-skills/           # 기존 5개 (유지)
│
├── cro-skills/                 # NEW: 6개
│   ├── page-cro/
│   ├── signup-flow-cro/
│   ├── onboarding-cro/
│   ├── form-cro/
│   ├── popup-cro/
│   └── paywall-upgrade-cro/
│
├── growth-skills/              # NEW: 5개
│   ├── churn-prevention/
│   ├── referral-program/
│   ├── free-tool-strategy/
│   ├── lead-magnets/
│   └── marketing-psychology/
│
├── sales-skills/               # NEW: 4개
│   ├── cold-email/
│   ├── revops/
│   ├── sales-enablement/
│   └── competitor-alternatives/
│
└── _shared/                    # NEW: 컨텍스트 브릿지
    └── product-marketing-context.md
```

**도입 우선순위:**

| 우선순위 | 스킬 | 핵심 가치 |
|:--------:|------|----------|
| 🔴 즉시 | **marketing-psychology** | 39+ 멘탈 모델 — 모든 마케팅 활동의 기반 |
| 🔴 즉시 | **pricing-strategy** | Van Westendorp + Good-Better-Best — 수익 직결 |
| 🔴 즉시 | **churn-prevention** | Cancel flow + Save offer + Health score — SaaS 생존 |
| 🔴 즉시 | **cold-email** | B2B 아웃바운드 — 완전 신규 채널 |
| 🔴 즉시 | **sales-enablement** | 피치덱/원페이저/반론 대응 — B2B 필수 |
| 🟠 빠른 | **page-cro** | CRO 분석 프레임워크 — LP보다 깊은 전환 최적화 |
| 🟠 빠른 | **signup-flow-cro** | 가입 플로우 전문 최적화 |
| 🟠 빠른 | **onboarding-cro** | Aha moment + 활성화 메트릭 |
| 🟠 빠른 | **revops** | 리드 스코어링/라우팅/MQL-SQL 정의 |
| 🟡 계획 | **ai-seo** | AI 검색 최적화 (Princeton GEO 연구 기반) |
| 🟡 계획 | **seo-audit** | 기술 SEO 감사 |
| 🟡 계획 | **schema-markup** | JSON-LD 구조화 데이터 |
| 🟡 계획 | **programmatic-seo** | 12개 플레이북 대규모 SEO |
| 🟡 계획 | **site-architecture** | 사이트 구조/IA |
| 🟡 계획 | **form-cro** / **popup-cro** / **paywall-upgrade-cro** | CRO 세분화 |
| 🟡 계획 | **referral-program** / **free-tool-strategy** / **lead-magnets** | 성장 전술 |
| 🟡 계획 | **competitor-alternatives** | 비교 페이지 SEO |

### Phase 2: 기존 스킬 강화 (MERGE)

겹치지만 remote가 더 깊은 7개 영역에서 핵심 내용을 로컬에 흡수.

| 로컬 스킬 | 흡수할 Remote 내용 | 예상 효과 |
|----------|-------------------|----------|
| **1-context-intake** | 코드베이스 자동 초안, JTBD Four Forces, 안티 페르소나, Proof Points, 고객 언어 강조 | A → A+ |
| **5-strategy** | Searchable vs Shareable 프레임워크, Topic Cluster, 콘텐츠 우선순위 스코어링 모델 | A → A+ |
| **6-campaign** | ORB 프레임워크(Owned/Rented/Borrowed), 5단계 런치, Product Hunt 플레이북 | A → A+ |
| **9-copywriting** | Writing Style Rules, 페이지별 카피 가이드, + `copy-editing`(Seven Sweeps) 신규 추가 | A → A+ |
| **11-email-sequence** | "One Email One Job" 원칙, 전달률 가이드, 법적 준수(CAN-SPAM/GDPR) | A → A+ |
| **12-ads-creative** | TikTok/X 광고 스펙 추가, 캠페인 아키텍처, 스케일링 프레임워크, 어트리뷰션 | B+ → A |
| **14-analytics-kpi** | GA4 구현 가이드, 데이터 레이어, 어트리뷰션 모델, 디버깅 | A → A+ |

### Phase 3: 노후 스킬 정리

| 스킬 | 현재 등급 | 조치 |
|------|:--------:|------|
| `70-marketing-ideas` | C+ | **교체** → remote의 139개 아이디어 라이브러리로 대체 |
| `71-positioning-ideas` | C+ | **삭제** → `4-positioning`과 완전 중복 |
| `44-monetization-strategy` | B- | **교체** → remote `pricing-strategy`로 대체 |
| `29-gtm-strategy` | B | **강화** → remote `launch-strategy` 내용 흡수 |

---

## 3. 컨텍스트 브릿지 패턴

Remote 스킬은 모두 `.agents/product-marketing-context.md`를 참조합니다.
기존 로컬은 `context/{project}-context.md`를 사용합니다.

**통합 방안:**

```
[1-context-intake 실행]
    ↓ 기존 출력
    context/{project}-context.md
    ↓ 추가 출력 (NEW)
    .agents/product-marketing-context.md
    ↓
[모든 스킬이 양쪽 경로 모두 확인]
```

`1-context-intake`가 두 위치에 모두 출력하도록 업데이트하면, 기존 파이프라인 스킬과 새로 도입한 remote 스킬이 모두 컨텍스트를 찾을 수 있습니다.

---

## 4. 도구 생태계 (선택적)

Remote 레포에는 51개 CLI 도구 + 72개 통합 가이드가 포함되어 있습니다.

**Tier 1 (즉시 가치):**

| 도구 | 용도 |
|------|------|
| `ga4.js` | GA4 데이터 직접 쿼리 |
| `stripe.js` | 결제/구독 데이터 |
| `resend.js` | 이메일 발송 (Vercel 생태계) |
| `google-search-console.js` | SEO 성과 |

**Tier 2 (성장 단계):**
`google-ads.js`, `meta-ads.js`, `buffer.js`, `semrush.js`, `ahrefs.js`

**Composio MCP**: OAuth 복잡한 도구(HubSpot, Salesforce, Meta Ads)용 — 현재는 불필요, 필요 시 도입

---

## 5. 유지해야 할 로컬 강점 (건드리지 말 것)

| 영역 | 스킬 | 이유 |
|------|------|------|
| 소셜미디어 운영 | 12개 전체 | Remote 1개 vs 로컬 12개 — 압도적 |
| 시장 조사 | 2-market-research | Remote에 없는 3C/SWOT/TAM |
| 페르소나 | 3-persona | Empathy Map + 반론 대응 — Remote보다 깊음 |
| 포지셔닝 | 4-positioning | STP 전체 + 포지셔닝 맵 — Remote보다 포괄적 |
| 고객 여정 | 8-customer-journey | Remote에 없는 통합 여정 맵 |
| 리뷰 | 15-review | Remote에 없는 품질 게이트 |
| 한국 시장 | KST 스케줄링, 네이버/카카오, 한국 규정 | Remote는 영어 SaaS만 |

---

## 6. 최종 요약

```
현재: 41개 스킬 (A등급 20, A-등급 12, B+이하 9)
목표: 55~58개 스킬 (신규 17 + 기존 강화 7 + 노후 정리 3)

신규 추가: +17 (CRO 6, Growth 5, Sales 4, SEO 2~5)
기존 강화:  7개 스킬에 remote 핵심 내용 흡수
노후 정리:  3개 교체/삭제

결과: SEO/CRO/Sales/Retention 역량 확보
      + 기존 한국 시장/소셜미디어 강점 유지
```

---

## 참고 상세 분석 문서

- `docs/260317-marketing-skills-overlap-gap-analysis.md` — 15개 비교 쌍 1:1 심층 분석
- `docs/260317-marketingskills-deep-analysis.md` — Remote 33개 스킬 상세 분석
