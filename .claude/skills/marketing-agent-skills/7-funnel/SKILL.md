---
name: mkt-funnel
description: |
  AARRR(Pirate Metrics) 기반 성장 퍼널 설계.
  각 단계별 전환율 목표와 최적화 전략을 수립합니다.
triggers:
  - "퍼널 설계"
  - "AARRR"
  - "성장 퍼널"
  - "전환 퍼널"
input:
  - context/{project}-context.md
  - strategy/campaign-plan.md
output:
  - campaigns/{project}-funnel.md
---

# Funnel Skill

AARRR(Pirate Metrics) 프레임워크 기반의 성장 퍼널을 설계합니다.

## AARRR 프레임워크

```
┌─────────────────────────────────────────────────────────────┐
│                    AARRR Pirate Metrics                      │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│   ┌──────────────────────────────────────────────────────┐  │
│   │ Acquisition (획득)                                    │  │
│   │ "사용자가 어떻게 우리를 발견하는가?"                    │  │
│   └──────────────────────────────────────────────────────┘  │
│                           │                                  │
│                           ▼                                  │
│   ┌──────────────────────────────────────────────────────┐  │
│   │ Activation (활성화)                                   │  │
│   │ "사용자의 첫 경험이 좋은가?"                           │  │
│   └──────────────────────────────────────────────────────┘  │
│                           │                                  │
│                           ▼                                  │
│   ┌──────────────────────────────────────────────────────┐  │
│   │ Retention (유지)                                      │  │
│   │ "사용자가 다시 돌아오는가?"                            │  │
│   └──────────────────────────────────────────────────────┘  │
│                           │                                  │
│                           ▼                                  │
│   ┌──────────────────────────────────────────────────────┐  │
│   │ Revenue (수익)                                        │  │
│   │ "사용자가 돈을 지불하는가?"                            │  │
│   └──────────────────────────────────────────────────────┘  │
│                           │                                  │
│                           ▼                                  │
│   ┌──────────────────────────────────────────────────────┐  │
│   │ Referral (추천)                                       │  │
│   │ "사용자가 다른 사람에게 추천하는가?"                    │  │
│   └──────────────────────────────────────────────────────┘  │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

## 단계별 상세

### 1. Acquisition (획득)

```yaml
acquisition:
  definition: "사용자가 처음 우리 제품/서비스를 발견하는 단계"

  channels:
    paid:
      - google_ads
      - facebook_ads
      - linkedin_ads
    organic:
      - seo
      - content_marketing
      - social_media
    referral:
      - word_of_mouth
      - affiliate
      - partnerships

  metrics:
    - visitors
    - channel_traffic
    - cost_per_visit
    - traffic_sources

  typical_conversion: "2-5%"  # 방문자 → 다음 단계
```

### 2. Activation (활성화)

```yaml
activation:
  definition: "사용자가 첫 '아하 모먼트'를 경험하는 단계"

  aha_moment_examples:
    - "첫 프로젝트 생성"
    - "핵심 기능 사용"
    - "첫 결과물 확인"

  metrics:
    - signup_rate
    - onboarding_completion
    - first_action_rate
    - time_to_value

  optimization:
    - simplify_onboarding
    - reduce_friction
    - guide_to_value

  typical_conversion: "20-40%"  # 가입 → 활성화
```

### 3. Retention (유지)

```yaml
retention:
  definition: "사용자가 지속적으로 제품을 사용하는 단계"

  cohort_periods:
    - day_1
    - day_7
    - day_30
    - day_90

  metrics:
    - daily_active_users
    - weekly_active_users
    - churn_rate
    - session_frequency

  strategies:
    - email_engagement
    - push_notifications
    - feature_education
    - habit_formation

  typical_rates:
    day_1: "40-60%"
    day_7: "20-30%"
    day_30: "10-20%"
```

### 4. Revenue (수익)

```yaml
revenue:
  definition: "사용자가 유료 고객으로 전환하는 단계"

  models:
    - subscription
    - one_time_purchase
    - freemium_upgrade
    - usage_based

  metrics:
    - conversion_rate
    - average_revenue_per_user
    - lifetime_value
    - monthly_recurring_revenue

  strategies:
    - pricing_optimization
    - upsell_campaigns
    - trial_to_paid

  typical_conversion: "2-10%"  # 무료 → 유료
```

### 5. Referral (추천)

```yaml
referral:
  definition: "사용자가 다른 사람에게 제품을 추천하는 단계"

  types:
    - organic_wom
    - referral_program
    - social_sharing
    - reviews

  metrics:
    - referral_rate
    - viral_coefficient
    - nps_score
    - review_count

  strategies:
    - referral_incentives
    - share_triggers
    - review_requests

  viral_coefficient: "> 1.0 = viral growth"
```

## 워크플로우

```
1. 현재 퍼널 상태 파악
      │
      ▼
2. 각 단계별 지표 정의
      │
      ▼
3. 전환율 목표 설정
      │
      ▼
4. 병목 지점 파악
      │
      ▼
5. 최적화 전략 수립
      │
      ▼
6. 퍼널 문서 저장
   → workspace/work-marketing/campaigns/{project}-funnel.md
```

## 출력 템플릿

```markdown
# {Project Name} Growth Funnel

## Funnel Overview

```
           Acquisition
          ┌───────────┐
          │  100,000  │  방문자
          └─────┬─────┘
                │ 3%
                ▼
           Activation
          ┌───────────┐
          │   3,000   │  가입자
          └─────┬─────┘
                │ 40%
                ▼
            Retention
          ┌───────────┐
          │   1,200   │  활성 사용자
          └─────┬─────┘
                │ 8%
                ▼
            Revenue
          ┌───────────┐
          │     96    │  유료 고객
          └─────┬─────┘
                │ 20%
                ▼
            Referral
          ┌───────────┐
          │     19    │  추천자
          └───────────┘
```

---

## 1. Acquisition (획득)

### 현재 상태

| 지표 | 현재 | 목표 | Gap |
|------|------|------|-----|
| 월간 방문자 | {current} | {target} | {gap} |
| 채널별 비중 | - | - | - |
| CAC | {current_cac} | {target_cac} | {gap} |

### 채널 분석

| 채널 | 트래픽 | 비용 | CPA | ROI |
|------|--------|------|-----|-----|
| {channel_1} | {traffic} | {cost} | {cpa} | {roi} |
| {channel_2} | {traffic} | {cost} | {cpa} | {roi} |

### 최적화 전략

1. **{strategy_1}**
   - 현재: {current_state}
   - 목표: {target_state}
   - 액션: {action}

2. **{strategy_2}**
   ...

---

## 2. Activation (활성화)

### Aha Moment 정의

> "{aha_moment_description}"
>
> 예: "첫 API 호출 성공 시"

### 현재 상태

| 지표 | 현재 | 목표 | Gap |
|------|------|------|-----|
| 가입 전환율 | {current}% | {target}% | {gap} |
| 온보딩 완료율 | {current}% | {target}% | {gap} |
| Time to Value | {current} | {target} | {gap} |

### Activation Funnel

```
Landing Page    가입 시작     온보딩 완료     Aha Moment
    100%    →     60%     →     40%      →     25%
     │            │              │              │
     │   -40%     │    -33%      │    -37%      │
     ▼            ▼              ▼              ▼
   DROP         DROP           DROP          SUCCESS
```

### 병목 지점

| 단계 | 이탈률 | 원인 추정 | 우선순위 |
|------|--------|----------|---------|
| {step_1} | {drop}% | {cause} | High |
| {step_2} | {drop}% | {cause} | Medium |

### 최적화 전략

1. **{strategy_1}**
   - 문제: {problem}
   - 가설: {hypothesis}
   - 액션: {action}
   - 예상 개선: {expected_improvement}

---

## 3. Retention (유지)

### 현재 상태

| 코호트 | 현재 | 벤치마크 | 상태 |
|--------|------|---------|------|
| Day 1 | {current}% | 40-60% | {status} |
| Day 7 | {current}% | 20-30% | {status} |
| Day 30 | {current}% | 10-20% | {status} |

### Retention Curve

```
100% │●
     │ ╲
 75% │  ╲
     │   ╲
 50% │    ●──
     │       ╲
 25% │        ●───●───●
     │
  0% └────────────────────
     D1   D7   D14  D30  D60
```

### 이탈 분석

| 이탈 시점 | 비율 | 주요 원인 |
|----------|------|----------|
| Day 1-3 | {%} | {reason} |
| Day 7-14 | {%} | {reason} |
| Day 30+ | {%} | {reason} |

### 최적화 전략

1. **{strategy_1}**
   - 타겟: {target_cohort}
   - 트리거: {trigger}
   - 액션: {action}

---

## 4. Revenue (수익)

### 현재 상태

| 지표 | 현재 | 목표 | Gap |
|------|------|------|-----|
| 유료 전환율 | {current}% | {target}% | {gap} |
| ARPU | ${current} | ${target} | {gap} |
| LTV | ${current} | ${target} | {gap} |
| LTV:CAC | {ratio} | 3:1+ | {gap} |

### 전환 퍼널

```
무료 사용자    트라이얼 시작    결제 시도    유료 고객
   1000    →     100      →     50     →    30
    │            │              │            │
    │  -90%      │   -50%       │   -40%     │
```

### 가격 구조

| 플랜 | 가격 | 전환율 | 비중 |
|------|------|--------|------|
| {plan_1} | ${price} | {rate}% | {share}% |
| {plan_2} | ${price} | {rate}% | {share}% |

### 최적화 전략

1. **{strategy_1}**
   - 현재: {current_state}
   - 액션: {action}
   - 예상 효과: {expected_effect}

---

## 5. Referral (추천)

### 현재 상태

| 지표 | 현재 | 목표 | Gap |
|------|------|------|-----|
| 추천율 | {current}% | {target}% | {gap} |
| Viral Coefficient | {current} | 1.0+ | {gap} |
| NPS | {current} | 50+ | {gap} |

### 추천 채널

| 채널 | 추천 수 | 전환율 |
|------|---------|--------|
| {channel_1} | {referrals} | {rate}% |
| {channel_2} | {referrals} | {rate}% |

### 최적화 전략

1. **{strategy_1}**
   - 트리거: {trigger}
   - 인센티브: {incentive}
   - 메커니즘: {mechanism}

---

## 6. Priority Matrix

### 영향도 vs 난이도

```
      High Impact
           │
     ┌─────┼─────┐
     │ ②  │  ①  │
Easy ├─────┼─────┤ Hard
     │ ④  │  ③  │
     └─────┼─────┘
           │
      Low Impact

① Quick Wins (먼저!)
② Major Projects (계획적으로)
③ Fill-ins (시간 될 때)
④ Thankless Tasks (후순위)
```

### 우선순위 액션 리스트

| 순위 | 단계 | 액션 | 예상 효과 | 난이도 |
|------|------|------|----------|--------|
| 1 | {stage} | {action} | {impact} | {effort} |
| 2 | {stage} | {action} | {impact} | {effort} |
| 3 | {stage} | {action} | {impact} | {effort} |

---

## 7. Implementation Roadmap

### Phase 1: Quick Wins (Week 1-2)
- [ ] {action_1}
- [ ] {action_2}

### Phase 2: Core Improvements (Week 3-4)
- [ ] {action_1}
- [ ] {action_2}

### Phase 3: Advanced Optimization (Week 5-8)
- [ ] {action_1}
- [ ] {action_2}

---

*Created: {date}*
*Last Updated: {update_date}*
```

## 다음 스킬 연결

- **Customer Journey Skill**: 퍼널을 고객 관점 여정으로 전환
- **A/B Testing Skill**: 퍼널 최적화 테스트 설계
- **Analytics KPI Skill**: 퍼널 지표 대시보드 구축

---

*퍼널의 핵심은 "어디서 새는가?"를 찾는 것입니다.*
*가장 큰 이탈 지점을 먼저 막으세요.*
