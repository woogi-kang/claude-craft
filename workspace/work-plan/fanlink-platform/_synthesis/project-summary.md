# FanLink 프로젝트 기획 종합 리포트

> 생성일: 2026-01-16
> 버전: 1.0 (Final)

---

## Executive Summary

### 프로젝트 개요

**FanLink**는 인플루언서/크리에이터와 팬을 연결하는 **양면 플랫폼**입니다.

| 항목 | 내용 |
|------|------|
| **핵심 가치** | "팬이 곧 파트너다" - 팬의 응원을 기록하고 보상하는 시스템 |
| **타겟 시장** | 한국 크리에이터 이코노미 (TAM $3B, SAM $300M, SOM $50M) |
| **차별점** | FanRank 시스템 - 팬 레벨, 배지, 히스토리 기반 Lock-in |
| **수익 모델** | 플랫폼 수수료 10% (업계 최저) |
| **MVP 기간** | 12주 / 5명 / ₩120M |

### 핵심 성공 요소

```
1. 양면 네트워크 효과
   ├── 크리에이터 → 팬 유입 (콘텐츠)
   └── 팬 활성화 → 크리에이터 유입 (수익)

2. 바이럴 성장 구조
   ├── 팬: 레벨업 공유, 배지 자랑
   └── 크리에이터: 팬 감사 콘텐츠

3. Lock-in 메커니즘
   ├── 팬 레벨 (Bronze → Legend)
   ├── 배지 컬렉션 (이전 불가)
   └── 응원 히스토리 (누적 데이터)
```

---

## 1. 기획 문서 인덱스

### Phase 1: Discovery (발견)

| 문서 | 경로 | 핵심 내용 |
|------|------|----------|
| 아이디어 정의 | `01-discovery/idea-intake.md` | 문제/솔루션 정의, 가설 |
| 가치 제안 | `01-discovery/value-proposition.md` | UVP, FanRank 시스템 |
| 타겟 사용자 | `01-discovery/target-user.md` | 페르소나, JTBD |

### Phase 2: Research (리서치)

| 문서 | 경로 | 핵심 내용 |
|------|------|----------|
| 시장 조사 | `02-research/market-research.md` | TAM/SAM/SOM, 트렌드 |
| 경쟁사 분석 | `02-research/competitor-analysis.md` | Patreon, YouTube, Twitch |

### Phase 3: Validation (검증)

| 문서 | 경로 | 핵심 내용 |
|------|------|----------|
| 린 캔버스 | `03-validation/lean-canvas.md` | 9블록 캔버스 |
| 비즈니스 모델 | `03-validation/business-model.md` | 수익 구조, Unit Economics |
| MVP 정의 | `03-validation/mvp-definition.md` | MoSCoW, 스프린트 계획 |

### Phase 4: Specification (명세)

| 문서 | 경로 | 핵심 내용 |
|------|------|----------|
| PRD | `04-specification/prd.md` | 기능 요구사항, 플로우 |

### Phase 5: Estimation (산정)

| 문서 | 경로 | 핵심 내용 |
|------|------|----------|
| 기술 스택 | `05-estimation/tech-stack.md` | Next.js, Supabase, Vercel |
| 공수 산정 | `05-estimation/effort-estimation.md` | 464 SP, 200 MD |

### Phase 7: Execution (실행)

| 문서 | 경로 | 핵심 내용 |
|------|------|----------|
| 로드맵 | `07-execution/roadmap.md` | 18개월 계획, 마일스톤 |

---

## 2. 핵심 숫자 요약

### 시장 기회

| 지표 | 값 | 출처 |
|------|------|------|
| TAM (전세계) | $3B | Goldman Sachs 2024 |
| SAM (아시아) | $300M | 크리에이터 이코노미 리포트 |
| SOM (한국, 3년) | $50M | 자체 추정 |
| CAGR | 22.4% | Statista |

### 비즈니스 모델

| 지표 | 값 | 비고 |
|------|------|------|
| 플랫폼 수수료 | 10% | 업계 최저 (YouTube 30%, Twitch 50%) |
| 팬 LTV | ₩7,000 | 12개월 기준 |
| CAC | ₩650 | 초기 추정 |
| LTV/CAC | 10.8x | 건전한 수준 |
| 손익분기점 | 18-20개월 | 크리에이터 200명, 팬 10,000명 |

### MVP 계획

| 지표 | 값 |
|------|------|
| 개발 기간 | 12주 |
| 팀 규모 | 5명 |
| 총 공수 | 200 MD |
| 예산 | ₩120M |
| 목표 크리에이터 | 50명 |
| 목표 팬 | 2,000명 |

### 18개월 로드맵

| 단계 | 기간 | 목표 |
|------|------|------|
| MVP | Month 1-3 | 출시, 크리에이터 50명 |
| PMF | Month 4-9 | MAU 20K, MRR $30K |
| Growth | Month 10-18 | MAU 100K, MRR $100K, 시리즈 A |

---

## 3. 기술 스택 요약

### 아키텍처

```
┌─────────────────────────────────────────────────────────────┐
│                        Frontend                              │
│  Next.js 15 + TypeScript + Tailwind CSS + shadcn/ui         │
│                         (Vercel)                             │
└─────────────────────────┬───────────────────────────────────┘
                          │ REST API / Realtime
┌─────────────────────────┴───────────────────────────────────┐
│                        Backend                               │
│                       Supabase                               │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐       │
│  │PostgreSQL│ │   Auth   │ │ Storage  │ │  Edge    │       │
│  │    DB    │ │          │ │  (S3)    │ │Functions │       │
│  └──────────┘ └──────────┘ └──────────┘ └──────────┘       │
└─────────────────────────────────────────────────────────────┘
                          │
┌─────────────────────────┴───────────────────────────────────┐
│                    External Services                         │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐       │
│  │  Toss    │ │ Mixpanel │ │  Resend  │ │  Sentry  │       │
│  │ Payments │ │Analytics │ │  Email   │ │  Error   │       │
│  └──────────┘ └──────────┘ └──────────┘ └──────────┘       │
└─────────────────────────────────────────────────────────────┘
```

### 기술 선택 근거

| 기술 | 선택 이유 |
|------|----------|
| **Next.js 15** | App Router, Server Actions, 빠른 개발 |
| **Supabase** | 올인원 백엔드, PostgreSQL, 실시간 지원 |
| **Vercel** | Next.js 최적화, 글로벌 Edge |
| **TossPayments** | 한국 시장 최적화, 정기결제 지원 |

### 월 운영 비용 (MVP)

| 항목 | 비용 |
|------|------|
| Vercel Pro | $20 |
| Supabase Pro | $25 |
| 도메인 | $2 |
| 기타 | $50 |
| **합계** | ~$100/월 |

---

## 4. 핵심 기능 요약

### MVP 필수 기능 (Must Have)

| 카테고리 | 기능 |
|----------|------|
| **인증** | 소셜 로그인, 역할 기반 접근 |
| **크리에이터** | 페이지 생성, 멤버십 티어 설정 |
| **팬** | 멤버십 가입, 레벨 시스템 |
| **결제** | 정기결제, 구독 관리 |
| **대시보드** | 크리에이터 수익/팬 통계 |

### FanRank 시스템

```
레벨 구조:
Bronze (0-999점) → Silver (1,000-4,999점) → Gold (5,000-14,999점)
    → Platinum (15,000-49,999점) → Diamond (50,000-99,999점) → Legend (100,000점+)

포인트 획득:
- 멤버십 가입: 1,000점
- 월 구독 유지: 500점/월
- 콘텐츠 댓글: 10점
- 콘텐츠 좋아요: 5점
- 추천 가입: 500점
```

### 화면 목록 (MVP)

| # | 화면 | 설명 |
|---|------|------|
| 1 | 랜딩 페이지 | 서비스 소개 |
| 2 | 로그인/가입 | 소셜 로그인 |
| 3 | 크리에이터 페이지 | 프로필, 멤버십 |
| 4 | 멤버십 결제 | 티어 선택, 결제 |
| 5 | 팬 마이페이지 | 구독, 레벨 |
| 6 | 크리에이터 대시보드 | 수익, 통계 |
| 7 | 멤버십 설정 | 티어 관리 |
| 8 | 팬 목록 | 구독자 관리 |

---

## 5. 리스크 & 대응

### 주요 리스크

| 리스크 | 영향 | 대응 전략 |
|--------|------|----------|
| 크리에이터 확보 실패 | 치명적 | 초기 인플루언서 제휴, 낮은 수수료 |
| 결제 연동 지연 | MVP 지연 | Week 5부터 조기 시작 |
| 경쟁사 대응 | 성장 저해 | 차별화 기능 강화 |
| 기술 부채 | 개발 속도 | 리팩토링 스프린트 배정 |

### 검증 필요 사항

| 가설 | 검증 방법 | 성공 기준 |
|------|----------|----------|
| 팬 레벨 시스템이 Lock-in에 효과적 | D30 리텐션 측정 | 30% 이상 |
| 10% 수수료가 크리에이터 유인 | 온보딩 전환율 | 20% 이상 |
| 배지 시스템이 바이럴 유도 | 공유율 측정 | 10% 이상 |

---

## 6. 다음 단계 (Immediate Actions)

### Week 0 체크리스트

- [ ] 개발팀 구성 확정
- [ ] Supabase 프로젝트 생성
- [ ] Vercel 계정 셋업
- [ ] TossPayments 가맹 신청
- [ ] 디자인 시스템 초안

### 의사결정 필요 사항

| 항목 | 옵션 | 추천 |
|------|------|------|
| 초기 크리에이터 확보 | 직접 영업 vs 제휴 | 제휴 + 직접 영업 병행 |
| 법인 설립 | 개인 vs 법인 | 법인 (투자 대비) |
| 베타 테스트 | 오픈 vs 클로즈드 | 클로즈드 (50명) |

---

## 7. 문서 품질 체크

### 완성도 평가

| Phase | 문서 | 완성도 | 비고 |
|-------|------|--------|------|
| Discovery | idea-intake.md | 100% | - |
| Discovery | value-proposition.md | 100% | - |
| Discovery | target-user.md | 100% | - |
| Research | market-research.md | 100% | - |
| Research | competitor-analysis.md | 100% | - |
| Validation | lean-canvas.md | 100% | - |
| Validation | business-model.md | 100% | - |
| Validation | mvp-definition.md | 100% | - |
| Specification | prd.md | 100% | - |
| Estimation | tech-stack.md | 100% | - |
| Estimation | effort-estimation.md | 100% | - |
| Execution | roadmap.md | 100% | - |

### 추가 검토 권장 사항

1. **법적 검토**: 정기결제 약관, 개인정보처리방침 → 법무 전문가 검토
2. **시장 데이터**: TAM/SAM/SOM 수치 → 외부 리서치 보완
3. **가격 정책**: 10% 수수료 → 초기 크리에이터 피드백 반영
4. **기술 PoC**: TossPayments 정기결제 연동 → 사전 테스트

---

## Appendix: 프로젝트 구조

```
fanlink-platform/
├── 01-discovery/
│   ├── idea-intake.md
│   ├── value-proposition.md
│   └── target-user.md
├── 02-research/
│   ├── market-research.md
│   └── competitor-analysis.md
├── 03-validation/
│   ├── lean-canvas.md
│   ├── business-model.md
│   └── mvp-definition.md
├── 04-specification/
│   └── prd.md
├── 05-estimation/
│   ├── tech-stack.md
│   └── effort-estimation.md
├── 07-execution/
│   └── roadmap.md
└── _synthesis/
    └── project-summary.md  ← 현재 문서
```

---

*FanLink - 팬이 곧 파트너다*
*기획 완료: 2026-01-16*
*다음 단계: 개발 착수*
