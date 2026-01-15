---
name: plan-mvp-definition
description: |
  MVP 범위를 정의하는 스킬.
  MoSCoW 우선순위, 가설, 성공 기준을 설정합니다.
triggers:
  - "MVP 정의"
  - "MVP 범위"
  - "최소 기능"
  - "MoSCoW"
input:
  - lean-canvas.md 결과
  - feature-spec.md (선택)
output:
  - 03-validation/mvp-definition.md
---

# MVP Definition Skill

검증 가능한 최소 제품(MVP)의 범위를 정의합니다.
가설을 검증하기 위한 최소한의 기능만 포함합니다.

## MVP 원칙

### MVP란?

```
MVP ≠ 미완성 제품
MVP ≠ 버그 많은 제품
MVP ≠ 기능 적은 제품

MVP = 가설을 검증할 수 있는 최소 제품
MVP = 고객이 핵심 가치를 경험할 수 있는 제품
MVP = 학습을 위한 도구
```

### MVP vs 좋은 제품

```
┌─────────────────────────────────────────────────────────────────┐
│                                                                  │
│   나쁜 MVP (기능 덜어내기)                                        │
│   ─────────────────────────                                      │
│   🚗 → 🚙 → 🛺 → 🛞                                              │
│   (타이어 하나로는 이동 불가)                                      │
│                                                                  │
│   좋은 MVP (핵심 가치 검증)                                       │
│   ─────────────────────────                                      │
│   🛹 → 🛴 → 🚲 → 🏍️ → 🚗                                         │
│   (각 단계에서 '이동'이라는 가치 제공)                              │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

## MoSCoW 프레임워크

```
M - Must Have    : 없으면 MVP가 아님
S - Should Have  : 중요하지만 없어도 검증 가능
C - Could Have   : 있으면 좋지만 후순위
W - Won't Have   : 이번엔 안 함 (나중에)
```

## 출력 템플릿

```markdown
# {Project Name} - MVP 정의서

## 1. MVP 목표

### 검증할 핵심 가설

> **"우리가 {solution}을 제공하면, {target_user}가 {expected_behavior}할 것이다"**

### 가설 상세

| # | 가설 | 유형 | 리스크 | 검증 방법 |
|---|------|------|--------|----------|
| 1 | {hypothesis_1} | 가치 | 🔴 High | {validation_1} |
| 2 | {hypothesis_2} | 사용성 | 🟡 Medium | {validation_2} |
| 3 | {hypothesis_3} | 성장 | 🟡 Medium | {validation_3} |

### MVP 성공 기준

| 지표 | 목표 | 측정 방법 |
|------|------|----------|
| {metric_1} | {target_1} | {how_1} |
| {metric_2} | {target_2} | {how_2} |
| {metric_3} | {target_3} | {how_3} |

**성공 정의**
> {success_criteria_all}
>
> 예: "4주 내 100명 가입 + 30% 재방문율 달성 시 다음 단계 진행"

---

## 2. 타겟 사용자 (MVP)

### MVP 타겟 = 얼리 어답터

| 항목 | 내용 |
|------|------|
| 누구 | {early_adopter_description} |
| 왜 먼저 | {why_early_adopter} |
| 어디서 | {where_to_find} |
| 목표 수 | {target_count}명 |

### 얼리 어답터 특징

- {characteristic_1}
- {characteristic_2}
- {characteristic_3}

---

## 3. 핵심 사용자 플로우 (MVP)

### Happy Path

```
{step_1}
    │
    ▼
{step_2}
    │
    ▼
{step_3}
    │
    ▼
{step_4}  ← 핵심 가치 경험
    │
    ▼
{step_5}
```

### 플로우 상세

| # | 단계 | 사용자 행동 | MVP 필수 |
|---|------|-----------|----------|
| 1 | {step_1} | {action_1} | ✅ |
| 2 | {step_2} | {action_2} | ✅ |
| 3 | {step_3} | {action_3} | ✅ |
| 4 | {step_4} | {action_4} | ✅ |

---

## 4. MoSCoW 기능 분류

### Must Have (필수)

> MVP에 반드시 포함. 없으면 핵심 가치 검증 불가.

| # | 기능 | 설명 | 가설 연결 |
|---|------|------|----------|
| M1 | {feature_m1} | {description} | H1 |
| M2 | {feature_m2} | {description} | H1 |
| M3 | {feature_m3} | {description} | H2 |
| M4 | {feature_m4} | {description} | - |

**Must Have 체크리스트**
```
□ 이 기능 없이 핵심 가치를 경험할 수 있는가? → No면 Must
□ 이 기능 없이 가설을 검증할 수 있는가? → No면 Must
□ 이 기능이 법적으로 필수인가? → Yes면 Must
```

### Should Have (중요)

> 중요하지만 MVP에서 빠져도 검증 가능

| # | 기능 | 설명 | 포함 안 하는 이유 |
|---|------|------|------------------|
| S1 | {feature_s1} | {description} | {reason} |
| S2 | {feature_s2} | {description} | {reason} |
| S3 | {feature_s3} | {description} | {reason} |

**다음 버전 우선순위**: S1 → S2 → S3

### Could Have (있으면 좋음)

| # | 기능 | 설명 | 우선순위 |
|---|------|------|----------|
| C1 | {feature_c1} | {description} | v1.2 |
| C2 | {feature_c2} | {description} | v1.3 |
| C3 | {feature_c3} | {description} | v2.0 |

### Won't Have (이번엔 안 함)

| # | 기능 | 설명 | 재검토 시점 |
|---|------|------|------------|
| W1 | {feature_w1} | {description} | PMF 후 |
| W2 | {feature_w2} | {description} | 시리즈 A 후 |
| W3 | {feature_w3} | {description} | 미정 |

---

## 5. MVP 기능 상세

### M1: {Feature Name}

| 항목 | 내용 |
|------|------|
| 설명 | {description} |
| 검증 가설 | {hypothesis} |
| 사용자 스토리 | As a {user}, I want to {action} so that {benefit} |

**인수 조건 (Acceptance Criteria)**
- [ ] {ac_1}
- [ ] {ac_2}
- [ ] {ac_3}

**MVP 범위 (이것만)**
- {scope_included_1}
- {scope_included_2}

**MVP 범위 외 (나중에)**
- {scope_excluded_1}
- {scope_excluded_2}

### M2: {Feature Name}

(동일 구조 반복)

---

## 6. MVP 제외 사항

### 명시적으로 제외

| 영역 | 제외 항목 | 이유 |
|------|----------|------|
| 기능 | {excluded_feature} | {reason} |
| 플랫폼 | {excluded_platform} | {reason} |
| 사용자 | {excluded_user} | {reason} |
| 엣지케이스 | {excluded_edge} | {reason} |

### 기술적 절충

| 영역 | MVP | 이후 |
|------|-----|------|
| 성능 | {mvp_perf} | {later_perf} |
| 보안 | {mvp_security} | {later_security} |
| 확장성 | {mvp_scale} | {later_scale} |

---

## 7. MVP 검증 계획

### 실험 설계

**실험 1: {experiment_name}**

| 항목 | 내용 |
|------|------|
| 검증 가설 | {hypothesis} |
| 방법 | {method} |
| 대상 | {target}명 |
| 기간 | {duration} |
| 성공 기준 | {success_criteria} |
| 측정 지표 | {metrics} |

**결과 시나리오**

| 결과 | 의미 | 다음 액션 |
|------|------|----------|
| 성공 | 가설 검증됨 | {next_action_success} |
| 부분 성공 | 수정 필요 | {next_action_partial} |
| 실패 | 피벗 고려 | {next_action_fail} |

### 검증 일정

| 주차 | 활동 | 목표 |
|------|------|------|
| Week 1-2 | MVP 개발 | 핵심 기능 완성 |
| Week 3 | 소프트 런칭 | 얼리 어답터 {n}명 |
| Week 4 | 피드백 수집 | 인터뷰 {n}회 |
| Week 5 | 분석 & 결정 | Go/No-Go |

---

## 8. MVP 리스크

### 리스크 평가

| 리스크 | 확률 | 영향 | 대응 |
|--------|------|------|------|
| {risk_1} | 🔴 High | 🔴 High | {mitigation_1} |
| {risk_2} | 🟡 Med | 🔴 High | {mitigation_2} |
| {risk_3} | 🟢 Low | 🟡 Med | {mitigation_3} |

### 킬 스위치 (Abort Criteria)

> 다음 조건 발생 시 MVP 중단 및 재검토

- {abort_criteria_1}
- {abort_criteria_2}
- {abort_criteria_3}

---

## 9. MVP 요약

### One-Page Summary

```
┌─────────────────────────────────────────────────────────────────┐
│                    {PROJECT} MVP 요약                            │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  핵심 가설                                                       │
│  ─────────────────────                                          │
│  "{hypothesis_summary}"                                          │
│                                                                  │
│  MVP 범위                                                        │
│  ─────────────────────                                          │
│  Must Have: {must_count}개 기능                                  │
│  • {must_1}                                                      │
│  • {must_2}                                                      │
│  • {must_3}                                                      │
│                                                                  │
│  타겟                                                            │
│  ─────────────────────                                          │
│  {early_adopter_summary}                                         │
│  목표: {target_count}명                                          │
│                                                                  │
│  성공 기준                                                       │
│  ─────────────────────                                          │
│  • {kpi_1}: {target_1}                                          │
│  • {kpi_2}: {target_2}                                          │
│                                                                  │
│  일정                                                            │
│  ─────────────────────                                          │
│  개발: {dev_weeks}주                                             │
│  검증: {validation_weeks}주                                      │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### Go/No-Go 체크리스트

**Go 조건**
- [ ] Must Have 기능 모두 완성
- [ ] 핵심 플로우 동작 확인
- [ ] 얼리 어답터 {n}명 확보
- [ ] 측정 시스템 준비

**No-Go 신호**
- [ ] 핵심 기술 구현 불가
- [ ] 타겟 고객 접근 실패
- [ ] 법적/규제 이슈 발견

---

## 10. 다음 단계

### MVP 성공 시

```
MVP 성공
    │
    ▼
Should Have 기능 추가
    │
    ▼
타겟 확대 (얼리 어답터 → 얼리 매저리티)
    │
    ▼
Product-Market Fit 달성
```

### MVP 실패 시

```
MVP 실패
    │
    ├─ 가설 수정 → Pivot
    │
    ├─ 타겟 수정 → New Segment
    │
    └─ 솔루션 수정 → New Approach
```

---

*다음 단계: Legal Checklist → PRD 작성*
```

## MVP 체크리스트

```
□ 핵심 가설이 명확한가?
□ Must Have가 5개 이하인가?
□ 모든 Must Have가 가설 검증에 필요한가?
□ 성공 기준이 측정 가능한가?
□ 얼리 어답터가 명확한가?
□ 검증 기간이 합리적인가?
□ 킬 스위치가 정의되었는가?
```

## 다음 스킬 연결

MVP Definition 완료 후:

1. **법적 검토** → Legal Checklist Skill
2. **상세 기획** → PRD, Feature Spec Skill
3. **개발 시작** → Tech Stack, Effort Estimation Skill

---

*MVP는 완벽한 제품이 아니라 가장 빠르게 학습하는 도구입니다.*
