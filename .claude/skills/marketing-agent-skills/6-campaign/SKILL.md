---
name: mkt-campaign
description: |
  마케팅 캠페인 기획 (SMART Goals, 채널, 예산).
  구체적인 캠페인 계획을 수립합니다.
triggers:
  - "캠페인 기획"
  - "캠페인 설계"
  - "프로모션 기획"
  - "런칭 캠페인"
input:
  - context/{project}-context.md
  - strategy/marketing-strategy.md
output:
  - strategy/campaign-plan.md
---

# Campaign Skill

SMART Goals 기반의 마케팅 캠페인을 기획합니다.

## 캠페인 유형

```yaml
campaign_types:
  awareness:                  # 인지도
    - brand_launch
    - product_launch
    - rebranding

  acquisition:                # 획득
    - lead_generation
    - signup_drive
    - trial_campaign

  conversion:                 # 전환
    - sales_promotion
    - upsell_campaign
    - seasonal_sale

  retention:                  # 유지
    - loyalty_program
    - reengagement
    - referral_program

  advocacy:                   # 옹호
    - ugc_campaign
    - review_campaign
    - ambassador_program
```

## SMART Goals 프레임워크

```
┌─────────────────────────────────────────────────────────────┐
│                       SMART Goals                            │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│   S - Specific (구체적)                                      │
│       "가입자 늘리기" ❌                                     │
│       "무료 체험 가입자 100명 확보" ✅                        │
│                                                              │
│   M - Measurable (측정 가능)                                 │
│       측정 방법과 도구 명시                                   │
│                                                              │
│   A - Achievable (달성 가능)                                 │
│       현실적인 목표, 리소스 고려                              │
│                                                              │
│   R - Relevant (관련성)                                      │
│       비즈니스 목표와 연결                                    │
│                                                              │
│   T - Time-bound (기한)                                      │
│       명확한 시작일과 종료일                                  │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

## 캠페인 구성 요소

```yaml
campaign_elements:
  objective:
    primary_goal: ""
    secondary_goals: []
    success_metrics: []

  target:
    primary_audience: ""
    secondary_audience: ""
    exclusions: []

  message:
    key_message: ""
    supporting_points: []
    cta: ""

  channels:
    primary: []
    secondary: []
    budget_split: {}

  creative:
    formats: []
    assets_needed: []

  timeline:
    start_date: ""
    end_date: ""
    milestones: []

  budget:
    total: ""
    breakdown: {}
    contingency: ""
```

## 워크플로우

```
1. 기존 전략 문서 확인
      │
      ▼
2. 캠페인 목표 설정 (SMART)
      │
      ▼
3. 타겟 오디언스 정의
      │
      ▼
4. 메시지 & CTA 설계
      │
      ▼
5. 채널 & 예산 배분
      │
      ▼
6. 타임라인 수립
      │
      ▼
7. 성공 지표 정의
      │
      ▼
8. 캠페인 기획서 저장
   → workspace/work-marketing/strategy/campaign-plan.md
```

## 출력 템플릿

```markdown
# {Campaign Name} Campaign Plan

## Campaign Overview

| 항목 | 내용 |
|------|------|
| 캠페인명 | {name} |
| 유형 | {type} |
| 기간 | {start_date} - {end_date} |
| 총 예산 | {total_budget} |

### Campaign Summary
{한 문단 요약}

---

## 1. Objectives (목표)

### Primary Goal (SMART)

| SMART | 내용 |
|-------|------|
| Specific | {specific} |
| Measurable | {measurable} |
| Achievable | {achievable} |
| Relevant | {relevant} |
| Time-bound | {time_bound} |

**목표 문장**: "{goal_statement}"

### Secondary Goals
1. {secondary_1}
2. {secondary_2}

### Success Metrics

| 지표 | 목표 | 측정 방법 |
|------|------|----------|
| {metric_1} | {target} | {method} |
| {metric_2} | {target} | {method} |
| {metric_3} | {target} | {method} |

---

## 2. Target Audience (타겟)

### Primary Audience
{primary_description}
→ Persona: {persona_name}

### Secondary Audience
{secondary_description}

### Exclusions (제외 대상)
- {exclusion_1}
- {exclusion_2}

---

## 3. Messaging (메시지)

### Key Message
> "{key_message}"

### Supporting Messages
1. {supporting_1}
2. {supporting_2}
3. {supporting_3}

### Call-to-Action
**Primary CTA**: {primary_cta}
**Secondary CTA**: {secondary_cta}

### Message by Stage

| 퍼널 단계 | 메시지 | CTA |
|----------|--------|-----|
| 인지 | {awareness_msg} | {cta} |
| 고려 | {consideration_msg} | {cta} |
| 결정 | {decision_msg} | {cta} |

---

## 4. Channels & Tactics (채널)

### Channel Mix

```
Channel Allocation
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
{channel_1}  ████████████████  40%
{channel_2}  ████████          25%
{channel_3}  ██████            20%
{channel_4}  ████              15%
```

### Channel Details

#### {Channel 1}

| 항목 | 내용 |
|------|------|
| 목적 | {purpose} |
| 타겟팅 | {targeting} |
| 포맷 | {format} |
| 예산 | {budget} |
| 예상 결과 | {expected_result} |

**Tactics**:
1. {tactic_1}
2. {tactic_2}

#### {Channel 2}
...

---

## 5. Creative Requirements (크리에이티브)

### 필요 에셋

| 에셋 | 규격 | 수량 | 담당 | 마감 |
|------|------|------|------|------|
| {asset_1} | {spec} | {qty} | {owner} | {deadline} |
| {asset_2} | {spec} | {qty} | {owner} | {deadline} |

### Creative Guidelines
- 톤앤매너: {tone}
- 컬러: {colors}
- 이미지 스타일: {image_style}

---

## 6. Timeline (타임라인)

### Overview

```
{month_1}          {month_2}          {month_3}
    │                  │                  │
    ▼                  ▼                  ▼
┌────────┐        ┌────────┐        ┌────────┐
│ Phase 1│   →    │ Phase 2│   →    │ Phase 3│
│ 준비   │        │ 런칭   │        │ 최적화 │
└────────┘        └────────┘        └────────┘
```

### Detailed Timeline

| 주차 | 단계 | 활동 | 담당 | 산출물 |
|------|------|------|------|--------|
| W1 | 준비 | {activity} | {owner} | {deliverable} |
| W2 | 준비 | {activity} | {owner} | {deliverable} |
| W3 | 런칭 | {activity} | {owner} | {deliverable} |
| W4 | 최적화 | {activity} | {owner} | {deliverable} |

### Key Milestones

| 날짜 | 마일스톤 | 상태 |
|------|----------|------|
| {date_1} | {milestone_1} | ⬜ |
| {date_2} | {milestone_2} | ⬜ |
| {date_3} | {milestone_3} | ⬜ |

---

## 7. Budget (예산)

### Budget Summary

| 항목 | 금액 | 비중 |
|------|------|------|
| 총 예산 | {total} | 100% |
| 미디어 비용 | {media} | {%} |
| 크리에이티브 | {creative} | {%} |
| 툴/소프트웨어 | {tools} | {%} |
| 예비비 | {contingency} | 10% |

### Channel Budget Breakdown

| 채널 | 예산 | CPM/CPC 예상 | 예상 도달 |
|------|------|-------------|----------|
| {channel_1} | {budget} | {cost} | {reach} |
| {channel_2} | {budget} | {cost} | {reach} |

---

## 8. Measurement & Optimization (측정)

### KPIs

| 단계 | KPI | 목표 | 측정 도구 |
|------|-----|------|----------|
| 인지 | {kpi} | {target} | {tool} |
| 참여 | {kpi} | {target} | {tool} |
| 전환 | {kpi} | {target} | {tool} |

### Optimization Plan

**Weekly Review**:
- {review_item_1}
- {review_item_2}

**Optimization Triggers**:
- If {metric} < {threshold} → {action}
- If {metric} > {threshold} → {action}

### A/B Tests Planned

| 테스트 | 변수 | 가설 |
|--------|------|------|
| {test_1} | {variable} | {hypothesis} |
| {test_2} | {variable} | {hypothesis} |

---

## 9. Risks & Contingencies (리스크)

| 리스크 | 확률 | 영향 | 대응 방안 |
|--------|------|------|----------|
| {risk_1} | High | High | {mitigation} |
| {risk_2} | Medium | Medium | {mitigation} |

---

## 10. Team & Responsibilities (팀)

| 역할 | 담당 | 책임 |
|------|------|------|
| 캠페인 매니저 | {name} | 전체 관리 |
| 크리에이티브 | {name} | 에셋 제작 |
| 미디어 바잉 | {name} | 광고 집행 |
| 분석 | {name} | 성과 측정 |

---

## 11. Appendix

### Checklist

**런칭 전**
- [ ] 크리에이티브 에셋 완료
- [ ] 랜딩페이지 라이브
- [ ] 트래킹 설정 완료
- [ ] 광고 계정 세팅
- [ ] 팀 브리핑 완료

**런칭 후**
- [ ] 첫 날 성과 확인
- [ ] 주간 리뷰 미팅
- [ ] 최적화 적용
- [ ] 최종 리포트

---

*Campaign Version: 1.0*
*Created: {date}*
*Owner: {owner}*
```

## 다음 스킬 연결

- **Funnel Skill**: 캠페인 퍼널 상세 설계
- **Copywriting Skill**: 캠페인 카피 제작
- **Ads Creative Skill**: 광고 에셋 제작
- **A/B Testing Skill**: 테스트 설계

---

*좋은 캠페인은 명확한 목표에서 시작합니다.*
*"무엇을 달성하고 싶은가?"에 SMART하게 답할 수 있어야 합니다.*
