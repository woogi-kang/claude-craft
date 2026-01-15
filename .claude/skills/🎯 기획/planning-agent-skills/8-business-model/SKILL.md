---
name: plan-business-model
description: |
  비즈니스 모델을 상세하게 설계하는 스킬.
  수익 구조, 비용 구조, 단위 경제학을 분석합니다.
triggers:
  - "비즈니스 모델"
  - "수익 모델"
  - "단위 경제학"
  - "유닛 이코노믹스"
input:
  - lean-canvas.md 결과
  - 가격 정보 (선택)
output:
  - 03-validation/business-model.md
---

# Business Model Skill

비즈니스의 지속 가능성을 분석합니다.
수익/비용 구조와 단위 경제학(Unit Economics)을 상세하게 설계합니다.

## 비즈니스 모델 유형

### 주요 수익 모델

| 모델 | 설명 | 예시 |
|------|------|------|
| **구독 (Subscription)** | 정기 결제 | Netflix, Spotify |
| **프리미엄 (Freemium)** | 무료 + 유료 업그레이드 | Slack, Dropbox |
| **거래 수수료 (Transaction)** | 거래당 수수료 | Stripe, PayPal |
| **마켓플레이스** | 판매자/구매자 매칭 수수료 | 쿠팡, 에어비앤비 |
| **광고 (Advertising)** | 노출/클릭 기반 광고 | Google, Facebook |
| **라이선스** | 사용권 판매 | Microsoft, Adobe |
| **하드웨어 + 서비스** | 기기 판매 + 서비스 | Apple, Tesla |

### 모델 선택 기준

```
구독 모델이 적합한 경우:
✅ 지속적 가치 제공
✅ 높은 고객 유지율 가능
✅ 예측 가능한 매출 원함

프리미엄 모델이 적합한 경우:
✅ 바이럴 성장 필요
✅ 네트워크 효과 있음
✅ 낮은 한계 비용

거래 수수료 모델이 적합한 경우:
✅ 거래 촉진 플랫폼
✅ 양면 시장
✅ 가치가 거래에서 발생
```

## 단위 경제학 (Unit Economics)

### 핵심 지표

```
┌─────────────────────────────────────────────────────────────────┐
│                    Unit Economics 공식                          │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│   LTV (고객 생애 가치)                                           │
│   ────────────────────                                          │
│   LTV = ARPU × Gross Margin % × Customer Lifetime               │
│                                                                  │
│   또는                                                           │
│                                                                  │
│   LTV = ARPU × Gross Margin % / Churn Rate                      │
│                                                                  │
│                                                                  │
│   CAC (고객 획득 비용)                                           │
│   ────────────────────                                          │
│   CAC = 총 마케팅/영업 비용 / 획득 고객 수                        │
│                                                                  │
│                                                                  │
│   LTV:CAC 비율                                                   │
│   ────────────────────                                          │
│   건전한 비즈니스: LTV:CAC > 3:1                                  │
│   CAC 회수 기간: < 12개월                                        │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

## 출력 템플릿

```markdown
# {Project Name} - 비즈니스 모델

## 1. 비즈니스 모델 개요

### 선택한 수익 모델

| 모델 | 비중 | 설명 |
|------|------|------|
| {model_1} | {ratio_1}% | {description_1} |
| {model_2} | {ratio_2}% | {description_2} |

### 모델 선택 이유
{model_rationale}

### 벤치마크

| 비교 서비스 | 모델 | ARPU | 전환율 |
|------------|------|------|--------|
| {benchmark_1} | {model} | ${arpu} | {conv}% |
| {benchmark_2} | {model} | ${arpu} | {conv}% |

---

## 2. 수익 구조 (Revenue Streams)

### 수익원 상세

#### 수익원 1: {revenue_stream_1}

| 항목 | 내용 |
|------|------|
| 유형 | {type} (구독/일회성/거래) |
| 타겟 | {target_customer} |
| 가격 | {price} |
| 결제 주기 | {billing_cycle} |

**수익 계산**
```
월 수익 = 유료 고객 수 × 월 가격
       = {customers} × ₩{price}
       = ₩{monthly_revenue}
```

#### 수익원 2: {revenue_stream_2}

(동일 구조)

### 수익 믹스 목표

| 수익원 | Year 1 | Year 2 | Year 3 |
|--------|--------|--------|--------|
| {stream_1} | {y1}% | {y2}% | {y3}% |
| {stream_2} | {y1}% | {y2}% | {y3}% |
| **Total** | 100% | 100% | 100% |

---

## 3. 비용 구조 (Cost Structure)

### 고정비 (Fixed Costs)

| 항목 | 월 비용 | 연 비용 | 비고 |
|------|---------|---------|------|
| 인건비 | ₩{cost} | ₩{cost} | {headcount}명 |
| 오피스 | ₩{cost} | ₩{cost} | {note} |
| 인프라 (기본) | ₩{cost} | ₩{cost} | AWS/GCP |
| SaaS 툴 | ₩{cost} | ₩{cost} | {tools} |
| 법인 유지비 | ₩{cost} | ₩{cost} | 회계, 세무 |
| **합계** | **₩{total}** | **₩{total}** | |

### 변동비 (Variable Costs)

| 항목 | 단위 비용 | 드라이버 |
|------|----------|----------|
| 서버 비용 | ₩{cost}/user | MAU |
| 결제 수수료 | {fee}% | 거래액 |
| 마케팅 | ₩{cac}/획득 | 신규 고객 |
| CS | ₩{cost}/ticket | 문의 수 |

### 비용 시뮬레이션

| 고객 수 | 고정비 | 변동비 | 총 비용 |
|---------|--------|--------|---------|
| 100명 | ₩{fixed} | ₩{var} | ₩{total} |
| 500명 | ₩{fixed} | ₩{var} | ₩{total} |
| 1,000명 | ₩{fixed} | ₩{var} | ₩{total} |
| 5,000명 | ₩{fixed} | ₩{var} | ₩{total} |

---

## 4. 단위 경제학 (Unit Economics)

### 핵심 지표 정의

| 지표 | 공식 | 목표 |
|------|------|------|
| ARPU | 총 매출 / 총 고객 | ₩{arpu} |
| ARPPU | 총 매출 / 유료 고객 | ₩{arppu} |
| Gross Margin | (매출 - 변동비) / 매출 | {gm}% |
| LTV | ARPU × GM% × Lifetime | ₩{ltv} |
| CAC | 마케팅비 / 신규 고객 | ₩{cac} |
| LTV:CAC | LTV / CAC | {ratio}:1 |
| Payback Period | CAC / (ARPU × GM%) | {months}개월 |

### LTV 계산

```
ARPU (월평균 매출/고객)     : ₩{arpu}
Gross Margin               : {gm}%
평균 고객 유지 기간         : {lifetime}개월
월 이탈률 (Churn Rate)     : {churn}%

LTV = ARPU × GM% / Churn Rate
    = ₩{arpu} × {gm}% / {churn}%
    = ₩{ltv}
```

### CAC 계산

```
마케팅 채널별 CAC:

| 채널 | 비용 | 획득 고객 | CAC |
|------|------|----------|-----|
| {channel_1} | ₩{cost} | {customers} | ₩{cac} |
| {channel_2} | ₩{cost} | {customers} | ₩{cac} |
| {channel_3} | ₩{cost} | {customers} | ₩{cac} |
| **Blended** | **₩{total}** | **{total}** | **₩{blended_cac}** |
```

### LTV:CAC 분석

```
LTV:CAC = ₩{ltv} : ₩{cac} = {ratio}:1

평가:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
[ ] < 1:1  → 🔴 지속 불가능 (돈 쓸수록 손해)
[ ] 1-3:1  → 🟡 개선 필요
[✓] 3-5:1  → 🟢 건전한 비즈니스
[ ] > 5:1  → 🟢 매우 건전 (or 성장 기회 놓침)

현재 상태: {assessment}
```

### Payback Period

```
CAC 회수 기간 = CAC / (ARPU × GM%)
             = ₩{cac} / (₩{arpu} × {gm}%)
             = {months}개월

평가:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
[ ] > 18개월  → 🔴 현금 흐름 위험
[ ] 12-18개월 → 🟡 개선 권장
[✓] < 12개월  → 🟢 건전

현재 상태: {assessment}
```

---

## 5. 수익성 분석

### 손익분기점 (Break-even)

```
월 고정비        : ₩{fixed_cost}
고객당 공헌이익   : ₩{contribution_margin}
                  (ARPU × GM% = ₩{arpu} × {gm}%)

손익분기 고객 수 = 고정비 / 공헌이익
                = ₩{fixed_cost} / ₩{contribution_margin}
                = {breakeven_customers}명
```

### 손익분기 시뮬레이션

| 시나리오 | ARPU | GM% | 고정비 | BEP 고객 |
|----------|------|-----|--------|----------|
| 보수적 | ₩{arpu_low} | {gm_low}% | ₩{fixed} | {bep_high} |
| 기본 | ₩{arpu_base} | {gm_base}% | ₩{fixed} | {bep_base} |
| 낙관적 | ₩{arpu_high} | {gm_high}% | ₩{fixed} | {bep_low} |

### 월별 손익 예측 (Year 1)

| 월 | 고객 수 | 매출 | 비용 | 손익 |
|---|--------|------|------|------|
| M1 | {n} | ₩{rev} | ₩{cost} | ₩{profit} |
| M3 | {n} | ₩{rev} | ₩{cost} | ₩{profit} |
| M6 | {n} | ₩{rev} | ₩{cost} | ₩{profit} |
| M9 | {n} | ₩{rev} | ₩{cost} | ₩{profit} |
| M12 | {n} | ₩{rev} | ₩{cost} | ₩{profit} |

---

## 6. 확장성 분석 (Scalability)

### 규모의 경제

| 규모 | 고정비/고객 | 변동비/고객 | 총 비용/고객 |
|------|------------|------------|-------------|
| 100명 | ₩{fixed_per} | ₩{var_per} | ₩{total_per} |
| 1,000명 | ₩{fixed_per} | ₩{var_per} | ₩{total_per} |
| 10,000명 | ₩{fixed_per} | ₩{var_per} | ₩{total_per} |

### 한계 비용 분석

```
한계 비용 (Marginal Cost): ₩{marginal_cost}/고객

고객 1명 추가 시:
- 서버 비용: +₩{server_cost}
- CS 비용: +₩{cs_cost}
- 기타: +₩{other_cost}
- 합계: +₩{marginal_cost}

한계 수익 (Marginal Revenue): ₩{marginal_revenue}/고객

한계 이익 = ₩{marginal_revenue} - ₩{marginal_cost}
          = ₩{marginal_profit} (✅ 양수)
```

---

## 7. 코호트 분석 (예상)

### 월별 이탈률 예상

| 월 | 잔존율 | 이탈률 |
|---|--------|--------|
| M1 | 100% | - |
| M2 | {retention}% | {churn}% |
| M3 | {retention}% | {churn}% |
| M6 | {retention}% | {churn}% |
| M12 | {retention}% | {churn}% |

### 코호트 수익 예상

| 코호트 | M1 | M3 | M6 | M12 | LTV |
|--------|-----|-----|-----|------|-----|
| 100명 시작 | ₩{rev} | ₩{rev} | ₩{rev} | ₩{rev} | ₩{ltv} |

---

## 8. 리스크 & 민감도 분석

### 핵심 가정

| 가정 | 기본값 | 민감도 |
|------|--------|--------|
| ARPU | ₩{arpu} | ±20% → 손익 ±{impact}% |
| Churn | {churn}% | ±5%p → LTV ±{impact}% |
| CAC | ₩{cac} | ±30% → ROI ±{impact}% |
| GM% | {gm}% | ±10%p → 손익 ±{impact}% |

### 시나리오 분석

| 시나리오 | ARPU | Churn | CAC | LTV:CAC | 평가 |
|----------|------|-------|-----|---------|------|
| 최악 | ₩{low} | {high}% | ₩{high} | {low_ratio}:1 | 🔴 |
| 기본 | ₩{base} | {base}% | ₩{base} | {base_ratio}:1 | 🟢 |
| 최선 | ₩{high} | {low}% | ₩{low} | {high_ratio}:1 | 🟢 |

---

## 9. 결론 & 권장사항

### 비즈니스 모델 건전성

| 지표 | 현재 (예상) | 목표 | 상태 |
|------|------------|------|------|
| LTV:CAC | {current}:1 | 3:1+ | {status} |
| Payback | {current}개월 | <12개월 | {status} |
| Gross Margin | {current}% | 70%+ | {status} |
| Break-even | {current}명 | - | - |

### 개선 우선순위

1. **{priority_1}**: {action_1}
2. **{priority_2}**: {action_2}
3. **{priority_3}**: {action_3}

### 모니터링 지표

| 지표 | 측정 주기 | 알람 기준 |
|------|----------|----------|
| MRR | 주간 | < 목표 80% |
| Churn | 월간 | > {threshold}% |
| CAC | 월간 | > ₩{threshold} |
| LTV:CAC | 분기 | < 2.5:1 |

---

*다음 단계: Pricing Strategy → MVP Definition*
```

## 퀄리티 체크리스트

```
□ 수익 모델이 명확한가?
□ LTV가 계산되었는가?
□ CAC가 추정되었는가?
□ LTV:CAC가 3:1 이상인가?
□ 손익분기점이 계산되었는가?
□ 핵심 가정이 명시되었는가?
□ 민감도 분석이 되었는가?
□ 리스크가 식별되었는가?
```

## 다음 스킬 연결

Business Model 완료 후:

1. **가격 상세화** → Pricing Strategy Skill
2. **MVP 범위 확정** → MVP Definition Skill
3. **투자 계획** → Pitch Deck Skill

---

*숫자는 예측일 뿐입니다. 실제 데이터로 지속 검증하세요.*
