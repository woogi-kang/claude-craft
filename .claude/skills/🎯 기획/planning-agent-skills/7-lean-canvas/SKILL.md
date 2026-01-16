---
name: plan-lean-canvas
description: |
  린 캔버스를 작성하는 스킬.
  비즈니스 모델을 한 페이지에 정리합니다.
triggers:
  - "린 캔버스"
  - "lean canvas"
  - "비즈니스 모델 요약"
input:
  - discovery 문서들
  - research 문서들
output:
  - 03-validation/lean-canvas.md
---

# Lean Canvas Skill

비즈니스 모델을 한 페이지에 정리하는 린 캔버스를 작성합니다.
스타트업의 핵심 가설과 리스크를 빠르게 파악할 수 있습니다.

## 린 캔버스 구조

```
┌─────────────┬─────────────┬─────────────┬─────────────┬─────────────┐
│  2. PROBLEM │ 4. SOLUTION │   3. UVP    │ 9. UNFAIR   │ 1. CUSTOMER │
│             │             │             │  ADVANTAGE  │  SEGMENTS   │
│  • 문제 1    │  • 해결책 1  │             │             │             │
│  • 문제 2    │  • 해결책 2  │ 차별화된    │  경쟁자가    │  • 세그먼트 1 │
│  • 문제 3    │  • 해결책 3  │ 가치 제안   │  쉽게 따라   │  • 세그먼트 2 │
│             │             │             │  할 수 없는  │             │
├─────────────┤             │             │  경쟁 우위   ├─────────────┤
│  EXISTING   │             │             │             │ EARLY       │
│ ALTERNATIVES│             │             │             │ ADOPTERS    │
│             │             │             │             │             │
│  현재 대안   │             │             │             │  초기 타겟   │
└─────────────┴─────────────┴─────────────┴─────────────┴─────────────┘
┌─────────────────────────────┬─────────────────────────────────────────┐
│       8. KEY METRICS        │            5. CHANNELS                  │
│                             │                                         │
│       핵심 지표               │            고객 도달 채널                │
└─────────────────────────────┴─────────────────────────────────────────┘
┌─────────────────────────────────────┬─────────────────────────────────┐
│         7. COST STRUCTURE           │        6. REVENUE STREAMS       │
│                                     │                                 │
│         비용 구조                    │         수익 구조                │
└─────────────────────────────────────┴─────────────────────────────────┘
```

## 작성 순서

```
권장 작성 순서:
1 → 2 → 3 → 4 → 5 → 6 → 7 → 8 → 9

1. Customer Segments (고객)    ← 누구를 위한 건가?
2. Problem (문제)             ← 그들의 문제는?
3. UVP (가치 제안)            ← 왜 우리를 선택?
4. Solution (해결책)          ← 어떻게 해결?
5. Channels (채널)            ← 어떻게 도달?
6. Revenue (수익)             ← 어떻게 벌?
7. Cost (비용)                ← 얼마나 들?
8. Metrics (지표)             ← 뭘 측정?
9. Unfair Advantage (경쟁 우위) ← 왜 따라오기 어려운가?
```

## 출력 템플릿

```markdown
# {Project Name} - 린 캔버스

## Version: {version} | Date: {date}

---

## 1. 고객 세그먼트 (Customer Segments)

### 주요 타겟
- **세그먼트 1**: {segment_1_description}
- **세그먼트 2**: {segment_2_description}

### 얼리 어답터 (Early Adopters)
> {early_adopter_description}

**특징**
- {characteristic_1}
- {characteristic_2}
- {characteristic_3}

---

## 2. 문제 (Problem)

### Top 3 문제

| # | 문제 | 심각도 | 빈도 |
|---|------|--------|------|
| 1 | {problem_1} | 🔴 High | 매일 |
| 2 | {problem_2} | 🔴 High | 주 2-3회 |
| 3 | {problem_3} | 🟡 Medium | 주 1회 |

### 현재 대안 (Existing Alternatives)

| 대안 | 사용률 | 한계점 |
|------|--------|--------|
| {alternative_1} | {usage}% | {limitation_1} |
| {alternative_2} | {usage}% | {limitation_2} |
| {alternative_3} | {usage}% | {limitation_3} |

---

## 3. 고유 가치 제안 (Unique Value Proposition)

### UVP Statement

> **"{uvp_statement}"**

### High-Level Concept

> "{service_name}은 {category}의 {comparison_service}다"
>
> 예: "YouTube는 비디오의 Flickr다"

### 차별화 포인트

1. **{diff_point_1}**: {description}
2. **{diff_point_2}**: {description}
3. **{diff_point_3}**: {description}

---

## 4. 솔루션 (Solution)

### 문제별 해결책

| 문제 | 해결책 | MVP 포함 |
|------|--------|----------|
| {problem_1} | {solution_1} | ✅ |
| {problem_2} | {solution_2} | ✅ |
| {problem_3} | {solution_3} | 🔜 |

### 핵심 기능 (MVP)

1. **{feature_1}**: {description}
2. **{feature_2}**: {description}
3. **{feature_3}**: {description}

---

## 5. 채널 (Channels)

### 고객 도달 채널

| 채널 | 유형 | 단계 | 우선순위 |
|------|------|------|----------|
| {channel_1} | Owned | 인지 | ⭐⭐⭐⭐⭐ |
| {channel_2} | Earned | 획득 | ⭐⭐⭐⭐ |
| {channel_3} | Paid | 획득 | ⭐⭐⭐ |

### 채널 전략

**초기 (0-100 고객)**
- {early_channel_strategy}

**성장기 (100-1000 고객)**
- {growth_channel_strategy}

---

## 6. 수익 구조 (Revenue Streams)

### 수익 모델

| 모델 | 설명 | 예상 비중 |
|------|------|----------|
| {model_1} | {description_1} | {ratio_1}% |
| {model_2} | {description_2} | {ratio_2}% |

### 가격 정책

| 플랜 | 가격 | 타겟 |
|------|------|------|
| Free | ₩0 | {free_target} |
| Pro | ₩{pro_price}/월 | {pro_target} |
| Enterprise | 문의 | {ent_target} |

### 수익 목표 (Year 1)

- **목표 매출**: {revenue_target}
- **고객 수**: {customer_target}
- **ARPU**: {arpu}

---

## 7. 비용 구조 (Cost Structure)

### 고정비

| 항목 | 월 비용 | 연 비용 |
|------|---------|---------|
| 인건비 | ₩{monthly} | ₩{yearly} |
| 인프라 | ₩{monthly} | ₩{yearly} |
| 툴/서비스 | ₩{monthly} | ₩{yearly} |
| **합계** | **₩{total_monthly}** | **₩{total_yearly}** |

### 변동비

| 항목 | 단위 비용 | 설명 |
|------|----------|------|
| 서버 | ₩{per_user}/user | 트래픽 기반 |
| 마케팅 | ₩{cac}/획득 | CAC |
| 거래 수수료 | {fee}% | PG 수수료 |

### 손익분기점

- **월 고정비**: ₩{fixed_cost}
- **객단가**: ₩{price}
- **손익분기 고객 수**: {breakeven_customers}명

---

## 8. 핵심 지표 (Key Metrics)

### North Star Metric

> **{north_star_metric}**
>
> 예: "주간 활성 사용자 수", "월 반복 매출(MRR)"

### AARRR 지표

| 단계 | 지표 | 목표 | 현재 |
|------|------|------|------|
| Acquisition | {acquisition_metric} | {target} | - |
| Activation | {activation_metric} | {target} | - |
| Retention | {retention_metric} | {target} | - |
| Revenue | {revenue_metric} | {target} | - |
| Referral | {referral_metric} | {target} | - |

---

## 9. 경쟁 우위 (Unfair Advantage)

### 따라하기 어려운 것

| 우위 | 설명 | 모방 난이도 |
|------|------|------------|
| {advantage_1} | {description_1} | 🔴 어려움 |
| {advantage_2} | {description_2} | 🟡 중간 |
| {advantage_3} | {description_3} | 🟢 쉬움 |

### 경쟁 우위 확보 계획

**단기 (0-6개월)**
- {short_term_advantage}

**중기 (6-18개월)**
- {mid_term_advantage}

**장기 (18개월+)**
- {long_term_advantage}

---

## 린 캔버스 요약 (한 페이지)

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                           {PROJECT_NAME} 린 캔버스                           │
├─────────────┬─────────────┬─────────────┬─────────────┬─────────────────────┤
│  PROBLEM    │  SOLUTION   │     UVP     │   UNFAIR    │ CUSTOMER SEGMENTS   │
│             │             │             │  ADVANTAGE  │                     │
│ • {p1_short}│ • {s1_short}│             │             │ • {c1_short}        │
│ • {p2_short}│ • {s2_short}│ {uvp_short} │ {ua_short}  │ • {c2_short}        │
│ • {p3_short}│ • {s3_short}│             │             │                     │
├─────────────┤             │             │             ├─────────────────────┤
│ EXISTING    │             │             │             │ EARLY ADOPTERS      │
│ ALTERNATIVES│             │             │             │                     │
│ {alt_short} │             │             │             │ {ea_short}          │
├─────────────┴─────────────┴─────────────┴─────────────┴─────────────────────┤
│  KEY METRICS                    │  CHANNELS                                 │
│  {metrics_short}                │  {channels_short}                         │
├─────────────────────────────────┴───────────────────────────────────────────┤
│  COST STRUCTURE                      │  REVENUE STREAMS                     │
│  {cost_short}                        │  {revenue_short}                     │
└──────────────────────────────────────┴──────────────────────────────────────┘
```

---

## 핵심 가설 & 리스크

### 가장 위험한 가설 Top 3

| # | 가설 | 리스크 | 검증 방법 |
|---|------|--------|----------|
| 1 | {hypothesis_1} | 🔴 | {validation_1} |
| 2 | {hypothesis_2} | 🔴 | {validation_2} |
| 3 | {hypothesis_3} | 🟡 | {validation_3} |

### 다음 실험

| 가설 | 실험 | 성공 기준 | 기간 |
|------|------|----------|------|
| {hypothesis} | {experiment} | {criteria} | {duration} |

---

*다음 단계: Business Model 상세화 → MVP Definition*
```

## 작성 팁

### 좋은 린 캔버스

```
✅ 한 페이지에 핵심만
✅ 가설 중심 (검증 필요한 것)
✅ 측정 가능한 지표
✅ 버전 관리 (지속 업데이트)
```

### 나쁜 린 캔버스

```
❌ 너무 상세함 (사업계획서처럼)
❌ 확정된 사실처럼 작성
❌ 한 번 쓰고 방치
❌ 팀 공유 안 함
```

## 퀄리티 체크리스트

```
□ 9개 블록이 모두 작성되었는가?
□ 문제가 구체적인가?
□ UVP가 차별화되었는가?
□ 얼리 어답터가 명확한가?
□ 현재 대안이 파악되었는가?
□ 핵심 지표가 정의되었는가?
□ 경쟁 우위가 진짜 따라하기 어려운가?
□ 검증할 가설이 식별되었는가?
```

## 🎯 인터랙티브 가이드

### 작성 전 확인 질문

**Q1. 린 캔버스를 처음 작성하나요?**
- 처음 → 9개 블록 순서대로 가이드
- 수정 → "어떤 블록을 업데이트하고 싶으세요?"

**Q2. 경쟁 우위(Unfair Advantage)가 있나요?**
- 있음 → 구체적 경쟁 우위 작성
- 없음/모름 → "시간이 지나면 생길 수 있는 우위는? (네트워크 효과, 데이터, 브랜드)"

**Q3. 핵심 지표(Key Metrics)를 정했나요?**
- 정함 → 지표 측정 방법 구체화
- 못 정함 → "성공을 어떻게 알 수 있을까요? (활성 사용자, 매출, 전환율)"

### 의사결정 포인트

| 시점 | 확인 내용 | 사용자 프롬프트 |
|------|----------|----------------|
| 문제 정의 | 구체성 | "이 문제를 겪는 구체적 상황은?" |
| 솔루션 | 핵심 기능 | "문제를 해결하는 핵심 기능 하나는?" |
| 채널 | 접근 방법 | "타겟 고객이 어디에 모여있나요?" |
| 완료 | 가설 우선순위 | "가장 먼저 검증해야 할 가설은?" |

---

## 다음 스킬 연결

린 캔버스 완료 후:

1. **수익 상세화** → Business Model Skill
2. **가격 설계** → Pricing Strategy Skill
3. **MVP 범위** → MVP Definition Skill

---

*린 캔버스는 살아있는 문서입니다. 학습할 때마다 업데이트하세요.*
