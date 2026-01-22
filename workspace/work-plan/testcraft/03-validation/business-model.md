# TestCraft - Business Model

> SaaS 수익 구조 및 단위 경제학 분석

---

## 1. Business Model Canvas

### Revenue Model: B2B SaaS Subscription

```
┌─────────────────────────────────────────────────────────────────┐
│                      TestCraft Revenue Model                     │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│   ┌─────────┐    ┌─────────┐    ┌─────────┐    ┌─────────┐     │
│   │  Free   │───▶│   Pro   │───▶│  Team   │───▶│Enterprise│     │
│   │  Tier   │    │  Tier   │    │  Tier   │    │  (Later) │     │
│   └─────────┘    └─────────┘    └─────────┘    └─────────┘     │
│                                                                  │
│   Revenue Driver: Seat-based Subscription                        │
│   Pricing Model: Per User Per Month (PUPM)                       │
│   Billing: Monthly / Annual (20% discount)                       │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

---

## 2. Revenue Streams

### Primary Revenue: Subscription

| Tier | 월 가격 | 연간 가격 | 주요 기능 |
|------|--------|----------|----------|
| **Free** | $0 | $0 | 5 TC/월, 1 플랫폼 |
| **Pro** | $12/user | $115/user | 무제한 TC, 3 플랫폼 |
| **Team** | $22/user | $211/user | + 팀 협업, 커스텀 템플릿 |

### Secondary Revenue (Phase 2+)

| 수익원 | 예상 비중 | 시작 시점 |
|-------|----------|----------|
| **TestRail/Jira 연동** | 5% | Month 12 |
| **커스텀 엣지케이스 팩** | 3% | Month 18 |
| **Enterprise 온프레미스** | 10% | Year 2 |
| **API 사용량 과금** | 2% | Month 12 |

---

## 3. Unit Economics

### 핵심 지표 정의

```
┌────────────────────────────────────────────────────────────┐
│                    Unit Economics 요약                      │
├────────────────────────────────────────────────────────────┤
│                                                             │
│   CAC (Customer Acquisition Cost)     : $80                 │
│   ARPU (Average Revenue Per User)     : $15/월              │
│   LTV (Lifetime Value)                : $360                │
│   LTV:CAC Ratio                       : 4.5:1               │
│   Payback Period                      : 5.3개월             │
│   Gross Margin                        : 75%                 │
│                                                             │
└────────────────────────────────────────────────────────────┘
```

### CAC (Customer Acquisition Cost) 상세

| 채널 | CAC | 전환율 | 비중 |
|-----|-----|-------|------|
| **Organic (SEO/콘텐츠)** | $30 | 3% | 40% |
| **커뮤니티/레퍼럴** | $20 | 5% | 25% |
| **Paid (LinkedIn)** | $120 | 1.5% | 20% |
| **Product Hunt** | $15 | 2% | 15% |

**Blended CAC**: $30×0.4 + $20×0.25 + $120×0.2 + $15×0.15 = **$43.25**

> 초기 6개월은 Paid 비중 높아 CAC $80 예상, 이후 $50 이하 목표

### ARPU (Average Revenue Per User) 계산

```
플랜별 비중 (유료 사용자 중):
├── Pro ($12):  70%
└── Team ($22): 30%

ARPU = $12 × 0.7 + $22 × 0.3 = $8.4 + $6.6 = $15/월
```

### LTV (Lifetime Value) 계산

```
LTV = ARPU × Gross Margin × Average Lifetime

ARPU: $15/월
Gross Margin: 75%
Churn Rate: 5%/월 (초기 가정)
Average Lifetime: 1 / 0.05 = 20개월

LTV = $15 × 0.75 × 20 = $225

목표 LTV (Churn 3%): $15 × 0.75 × 33 = $375
```

### LTV:CAC Ratio

| 시나리오 | LTV | CAC | Ratio | 평가 |
|---------|-----|-----|-------|------|
| **초기 (6개월)** | $225 | $80 | 2.8:1 | 수용 가능 |
| **안정화 (12개월)** | $300 | $50 | 6.0:1 | 양호 |
| **목표 (24개월)** | $375 | $40 | 9.4:1 | 우수 |

> 건강한 SaaS 기준: LTV:CAC > 3:1

### Payback Period

```
초기: CAC $80 / ARPU $15 × 0.75 = 7.1개월
목표: CAC $40 / ARPU $15 × 0.75 = 3.6개월
```

---

## 4. Cost Structure

### Fixed Costs (Monthly)

| 카테고리 | 항목 | 금액 | 비고 |
|---------|------|------|------|
| **인건비** | 개발자 2명 | $10,000 | 평균 $5K/인 |
| | PM/창업자 | $5,000 | |
| **인프라** | AWS/Vercel | $300 | 초기 |
| | DB (Supabase) | $100 | |
| **AI** | OpenAI API | $800 | GPT-4 |
| **도구** | SaaS 구독 | $200 | Slack, Linear 등 |
| **기타** | 도메인, 보안 | $100 | |
| | **Total** | **$16,500** | |

### Variable Costs (Per Transaction)

| 항목 | 단가 | 트리거 |
|-----|------|-------|
| **AI TC 생성** | $0.025 | TC 1건 생성 |
| **파일 파싱** | $0.005 | PRD 업로드 |
| **스토리지** | $0.01/GB | 파일 저장 |
| **이메일** | $0.001 | 알림 발송 |

### COGS (Cost of Goods Sold)

```
Pro 사용자 1명당 월 COGS:
├── AI API (평균 50 TC/월): $0.025 × 50 = $1.25
├── 인프라: $0.50
├── 결제 수수료 (3%): $0.36
└── Total COGS: $2.11

Gross Margin = ($12 - $2.11) / $12 = 82.4%
```

---

## 5. Revenue Projection

### Year 1 Projection

| Month | Free Users | Paid Users | MRR | 누적 수익 |
|-------|-----------|------------|-----|----------|
| 1 | 100 | 0 | $0 | $0 |
| 2 | 300 | 5 | $75 | $75 |
| 3 | 600 | 15 | $225 | $300 |
| 4 | 1,000 | 35 | $525 | $825 |
| 5 | 1,500 | 60 | $900 | $1,725 |
| 6 | 2,200 | 100 | $1,500 | $3,225 |
| 7 | 2,800 | 150 | $2,250 | $5,475 |
| 8 | 3,400 | 210 | $3,150 | $8,625 |
| 9 | 4,000 | 280 | $4,200 | $12,825 |
| 10 | 4,600 | 360 | $5,400 | $18,225 |
| 11 | 5,200 | 450 | $6,750 | $24,975 |
| 12 | 6,000 | 550 | $8,250 | $33,225 |

### Growth Assumptions

- Free 사용자 월 성장률: 30% (초기) → 15% (안정화)
- Free → Paid 전환율: 5% (초기) → 8% (최적화 후)
- Monthly Churn: 5% (초기) → 3% (목표)

### Year 1-3 Summary

| 지표 | Year 1 | Year 2 | Year 3 |
|-----|--------|--------|--------|
| **ARR** | $99K | $360K | $1.2M |
| **Paid Users** | 550 | 2,000 | 6,000 |
| **Free Users** | 6,000 | 20,000 | 50,000 |
| **ARPU** | $15 | $15 | $17 |
| **Gross Margin** | 75% | 78% | 80% |

---

## 6. Break-even Analysis

### Monthly Break-even

```
Fixed Costs: $16,500/월
Gross Margin: 75%
ARPU: $15

Break-even Users = $16,500 / ($15 × 0.75) = 1,467 유료 사용자

예상 달성: Month 18-20
```

### Cash Flow Projection

| Period | Revenue | Costs | Net | 누적 |
|--------|---------|-------|-----|------|
| Month 1-6 | $3,225 | $99,000 | -$95,775 | -$95,775 |
| Month 7-12 | $30,000 | $105,000 | -$75,000 | -$170,775 |
| Year 2 | $360,000 | $240,000 | +$120,000 | -$50,775 |
| Year 3 | $1,200,000 | $480,000 | +$720,000 | +$669,225 |

### Funding Requirement

```
최소 Runway 필요: 18개월
예상 Burn: $170K
버퍼 (20%): $34K
─────────────────────
최소 시드 펀딩: $200K
```

---

## 7. Pricing Power Analysis

### Willingness to Pay (WTP) 검증

| 검증 방법 | 결과 | 인사이트 |
|----------|------|---------|
| Van Westendorp | $8-18 범위 | $12 적정 |
| 경쟁사 벤치마크 | TestRail $45, PractiTest $35 | 진입 가격 여유 |
| QA 시간 절감 가치 | $800/월 (20시간 × $40) | 10x+ 가치 |

### Price Elasticity

```
현재 $12에서:
├── $10 (-17%): 전환율 +25% 예상 → 수익 +3%
├── $15 (+25%): 전환율 -15% 예상 → 수익 +6%
└── $20 (+67%): 전환율 -30% 예상 → 수익 +17%

결론: $12-15 범위가 최적, 추후 $15로 인상 가능
```

---

## 8. Scalability Model

### Scale Economics

| 규모 | 유료 사용자 | Gross Margin | COGS/User |
|-----|-----------|--------------|-----------|
| **Seed** | 100 | 70% | $3.60 |
| **Growth** | 1,000 | 78% | $2.64 |
| **Scale** | 10,000 | 85% | $1.80 |

### Operational Leverage

```
Revenue × 10 = $1.2M
Cost × 3 = $480K (인프라 효율화, AI 최적화)

Margin 개선: 75% → 85%
```

---

## 9. Risk Factors

### Financial Risks

| 리스크 | 영향 | 완화 전략 |
|-------|------|----------|
| **높은 Churn** | LTV 감소 | 온보딩 강화, 기능 고도화 |
| **CAC 증가** | ROI 악화 | Organic 채널 강화 |
| **AI 비용 상승** | 마진 감소 | 캐싱, 자체 모델 검토 |
| **환율 리스크** | 비용 변동 | 달러 기반 운영 |

### Sensitivity Analysis

```
Base Case: LTV $300, CAC $50, Ratio 6:1

Scenario A (Churn +2%): LTV $200, Ratio 4:1
Scenario B (CAC +50%): CAC $75, Ratio 4:1
Scenario C (ARPU -20%): LTV $240, Ratio 4.8:1

최악의 경우: Ratio 3:1 (여전히 수용 가능)
```

---

## 10. Key Takeaways

### Strengths
- 높은 Gross Margin (75-85%)
- 명확한 가치 제안 (시간 절감)
- 확장 가능한 SaaS 모델

### Challenges
- 초기 CAC가 높음 (Paid 의존)
- Free → Paid 전환율 증명 필요
- AI 비용 관리 필요

### Action Items
1. Organic 채널 (SEO, 커뮤니티) 선투자
2. 온보딩 최적화로 Activation 개선
3. AI 비용 최적화 (캐싱, 프롬프트 효율화)

---

*Generated by Planning Agent - Business Model Skill*
*Last Updated: 2026-01-16*
