# TestCraft - Lean Canvas

> PRD 기반 QA 테스트케이스 자동 생성 SaaS

---

## 1. Problem (문제)

### Top 3 Problems

| # | 문제 | 현재 대안 | 불만족 이유 |
|---|------|----------|------------|
| 1 | PRD → TC 변환에 과도한 시간 소요 | 수동 작성, Excel 템플릿 | 3-5일 소요, 반복 작업 |
| 2 | 플랫폼별 엣지케이스 누락 | QA 경험에 의존 | 속인적, 일관성 없음 |
| 3 | TC 품질 편차 | 리뷰 프로세스 | 리뷰어 역량에 의존 |

### Existing Alternatives (기존 대안)

- **수동 작성**: Excel, Notion에 직접 작성
- **Jira/TestRail**: 관리 도구일 뿐, 생성 기능 없음
- **Copilot/ChatGPT**: 범용 AI, QA 특화 아님

---

## 2. Customer Segments (고객 세그먼트)

### Primary Target

```
┌─────────────────────────────────────────────────────────┐
│  스타트업/중소 IT기업 QA 팀 (1-10명 규모)                │
│                                                         │
│  특성:                                                  │
│  - 빠른 릴리즈 주기 (2주 스프린트)                       │
│  - 제한된 QA 인력                                       │
│  - 멀티플랫폼 지원 필요 (Android/iOS/Web)               │
│  - TC 작성에 전체 QA 시간의 40-60% 소요                 │
└─────────────────────────────────────────────────────────┘
```

### Early Adopters

| 세그먼트 | 특성 | 접근 채널 |
|---------|------|----------|
| **스타트업 QA Lead** | 혼자 or 소규모 팀 운영, 효율 극대화 필요 | LinkedIn, QA 커뮤니티 |
| **IT서비스 중견기업 QA팀** | 프로젝트 단위 TC 대량 필요 | 기술 블로그, 컨퍼런스 |
| **프리랜서 QA 엔지니어** | 생산성 = 수익, 도구 투자 의향 높음 | 크몽, 위시켓 |

---

## 3. Unique Value Proposition (고유 가치 제안)

### Single Clear Message

```
┌─────────────────────────────────────────────────────────┐
│                                                         │
│   "PRD 업로드 한 번으로                                  │
│    플랫폼별 엣지케이스까지 완성된 테스트케이스"           │
│                                                         │
│   기존 3-5일 → 30분                                     │
│   누락률 30% → 5% 이하                                  │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

### High-Level Concept

> "PRD를 위한 GitHub Copilot"
>
> Copilot이 코드 자동완성이라면,
> TestCraft는 TC 자동생성

---

## 4. Solution (솔루션)

### Top 3 Features

| # | 기능 | 해결하는 문제 | MVP 포함 |
|---|------|-------------|---------|
| 1 | **PRD 파싱 & TC 자동 생성** | 시간 소요 | Yes |
| 2 | **플랫폼별 엣지케이스 라이브러리** | 누락 | Yes |
| 3 | **TC 품질 일관성 검증** | 품질 편차 | Yes |

### MVP Solution Flow

```
PRD 업로드 → 플랫폼 선택 → AI 분석 → TC 초안 생성 → 엣지케이스 추가 → Export
    │              │            │            │              │           │
    │              │            │            │              │           │
    ▼              ▼            ▼            ▼              ▼           ▼
 PDF/MD/Word   Android     기능 추출      TC 구조화      플랫폼별      Excel
              iOS/Web/PC  요구사항 매핑   우선순위 태깅   특화 케이스   CSV
```

---

## 5. Channels (채널)

### Customer Acquisition

| 채널 | 단계 | 예상 CAC | 우선순위 |
|-----|------|---------|---------|
| **콘텐츠 마케팅** | Awareness → Interest | $20-30 | High |
| **QA 커뮤니티** | Interest → Trial | $10-15 | High |
| **Product Hunt** | Awareness → Trial | $5-10 | Medium |
| **LinkedIn Ads** | Awareness → Interest | $50-80 | Low (초기) |

### Distribution Strategy

```
Phase 1 (0-6개월): Organic
├── 기술 블로그 SEO (TC 작성 가이드)
├── QA Korea 커뮤니티 활동
└── Product Hunt 런칭

Phase 2 (6-12개월): Paid + Partnership
├── LinkedIn B2B 타겟 광고
├── TestRail/Jira 연동 마켓플레이스
└── QA 컨퍼런스 스폰서
```

---

## 6. Revenue Streams (수익원)

### Primary Revenue Model: SaaS Subscription

| 플랜 | 월 가격 | 타겟 | 예상 비중 |
|-----|--------|------|----------|
| **Free** | $0 | 개인, 평가용 | 60% (전환 퍼널) |
| **Pro** | $12/user | 스타트업 | 25% |
| **Team** | $22/user | 중견기업 | 15% |

### Revenue Projection (Year 1)

```
Month 1-3:   Free 사용자 확보 집중
Month 4-6:   유료 전환 시작 (5% 목표)
Month 7-12:  MRR 성장

Target MRR (Month 12): $30,000
├── Pro: 150 users × $12 = $1,800
├── Team: 100 users × $22 = $2,200
└── 총 유료 사용자: 250명
```

---

## 7. Cost Structure (비용 구조)

### Fixed Costs (월간)

| 항목 | 금액 | 비고 |
|-----|------|------|
| 인건비 (3명) | $15,000 | 개발 2, PM 1 |
| 클라우드 인프라 | $500 | AWS/Vercel |
| AI API (OpenAI) | $1,000 | GPT-4 사용량 |
| SaaS 도구 | $300 | Slack, Notion 등 |
| **Total** | **$16,800** | |

### Variable Costs (사용량 비례)

| 항목 | 단가 | 비고 |
|-----|------|------|
| AI API 호출 | $0.03/TC생성 | GPT-4 토큰 |
| 스토리지 | $0.01/GB | PRD 파일 저장 |

### Break-even Point

```
고정비 $16,800 / ARPU $15 = 1,120 유료 사용자
예상 달성 시점: Month 18-24
```

---

## 8. Key Metrics (핵심 지표)

### North Star Metric

> **월간 TC 생성 수 (Monthly Test Cases Generated)**
>
> 이유: 핵심 가치 전달의 직접 지표

### Supporting Metrics

| 카테고리 | 지표 | 목표 (Month 12) |
|---------|------|-----------------|
| **Acquisition** | MAU | 5,000 |
| **Activation** | First TC 생성률 | 60% |
| **Retention** | M1 Retention | 40% |
| **Revenue** | Free→Paid 전환율 | 5% |
| **Referral** | NPS | 40+ |

### Pirate Metrics (AARRR)

```
Acquisition:  가입자 수, 유입 채널별 CAC
Activation:   첫 TC 생성까지 시간, 완료율
Retention:    주간 활성 사용자, 재방문율
Referral:     초대 기능 사용률, 바이럴 계수
Revenue:      MRR, ARPU, LTV
```

---

## 9. Unfair Advantage (불공정 우위)

### 장기 경쟁 우위 요소

| 요소 | 설명 | 모방 난이도 |
|-----|------|------------|
| **플랫폼별 엣지케이스 DB** | Android/iOS/Web 특화 케이스 축적 | High |
| **QA 도메인 Fine-tuned AI** | 일반 AI 대비 TC 품질 우위 | Medium |
| **TC 품질 피드백 데이터** | 사용자 수정 패턴 학습 | High |
| **TestRail/Jira 깊은 연동** | 워크플로우 락인 | Medium |

### Defensibility Timeline

```
Year 1: 제품 차별화 (엣지케이스 라이브러리)
Year 2: 데이터 해자 (TC 품질 학습 데이터)
Year 3: 네트워크 효과 (TC 템플릿 마켓플레이스)
```

---

## Lean Canvas 요약 (1-Page)

```
┌─────────────────┬─────────────────┬─────────────────┐
│    PROBLEM      │   SOLUTION      │    UVP          │
│                 │                 │                 │
│ 1. TC 작성 시간 │ 1. PRD→TC 자동  │ "PRD 한 번으로  │
│ 2. 엣지케이스   │ 2. 플랫폼별     │  플랫폼별 TC    │
│    누락         │    엣지케이스   │  30분 완성"     │
│ 3. 품질 편차    │ 3. 품질 검증    │                 │
├─────────────────┼─────────────────┼─────────────────┤
│  KEY METRICS    │                 │ UNFAIR ADV.     │
│                 │                 │                 │
│ - 월간 TC 생성  │                 │ - 엣지케이스 DB │
│ - Free→Paid 5% │                 │ - Fine-tuned AI │
│ - M1 Ret. 40%  │                 │ - 학습 데이터   │
├─────────────────┼─────────────────┼─────────────────┤
│   CHANNELS      │ CUSTOMER SEG.   │ COST STRUCTURE  │
│                 │                 │                 │
│ - 콘텐츠 마케팅 │ 스타트업/중소   │ 인건비: $15K    │
│ - QA 커뮤니티  │ IT기업 QA팀     │ 인프라: $500    │
│ - Product Hunt │ (1-10명 규모)   │ AI API: $1K     │
├─────────────────┴─────────────────┴─────────────────┤
│                  REVENUE STREAMS                     │
│                                                      │
│  Free ($0) → Pro ($12/user) → Team ($22/user)       │
│  Target MRR Month 12: $30,000                        │
└──────────────────────────────────────────────────────┘
```

---

## 다음 단계

1. **Business Model**: 단위 경제학 상세 분석
2. **Pricing Strategy**: 가격 민감도 테스트 설계
3. **MVP Definition**: 핵심 기능 범위 확정

---

*Generated by Planning Agent - Lean Canvas Skill*
*Last Updated: 2026-01-16*
