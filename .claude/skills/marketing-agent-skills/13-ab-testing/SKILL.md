---
name: mkt-ab-testing
description: |
  A/B 테스트 설계 및 가설 수립.
  테스트 계획, 표본 크기, 기간을 계산합니다.
triggers:
  - "A/B 테스트"
  - "테스트 설계"
  - "실험 설계"
  - "전환 테스트"
input:
  - 테스트 대상 (LP, 이메일, 광고 등)
  - 현재 전환율
output:
  - ab-tests/{test-name}-design.md
---

# A/B Testing Skill

체계적인 A/B 테스트를 설계합니다.

## A/B 테스트란?

```
┌─────────────────────────────────────────────────────────────┐
│                       A/B Test                               │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│                      트래픽 100%                             │
│                          │                                   │
│               ┌──────────┴──────────┐                       │
│               │                     │                        │
│               ▼                     ▼                        │
│         ┌─────────┐           ┌─────────┐                   │
│         │ Control │           │ Variant │                   │
│         │   (A)   │           │   (B)   │                   │
│         │  50%    │           │   50%   │                   │
│         └─────────┘           └─────────┘                   │
│               │                     │                        │
│               ▼                     ▼                        │
│          전환율 3%             전환율 3.5%                   │
│                                                              │
│         → B가 16.7% 더 높음 = 통계적으로 유의미?            │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

## 테스트 가능 요소

### 랜딩페이지

```yaml
landing_page_tests:
  high_impact:
    - headline
    - cta_button_text
    - cta_button_color
    - hero_image
    - form_fields

  medium_impact:
    - subheadline
    - social_proof_placement
    - pricing_display
    - testimonial_selection

  low_impact:
    - font_size
    - button_shape
    - icon_style
```

### 이메일

```yaml
email_tests:
  high_impact:
    - subject_line
    - sender_name
    - send_time
    - cta_text

  medium_impact:
    - preview_text
    - personalization
    - email_length
    - image_vs_no_image
```

### 광고

```yaml
ad_tests:
  high_impact:
    - headline
    - image/video
    - cta
    - audience

  medium_impact:
    - ad_copy
    - ad_format
    - placement
```

## 가설 템플릿

```
만약 [변경 사항]을 하면,
[지표]가 [방향]할 것이다.
왜냐하면 [이유]이기 때문이다.

예시:
만약 CTA 버튼을 "무료 체험" → "지금 시작하기"로 바꾸면,
클릭률이 증가할 것이다.
왜냐하면 더 행동 지향적이고 긴급성을 주기 때문이다.
```

## 표본 크기 계산

### 필요 정보

```yaml
sample_size_inputs:
  baseline_conversion_rate: ""    # 현재 전환율 (%)
  minimum_detectable_effect: ""   # 탐지하려는 최소 변화 (%)
  statistical_significance: 95%   # 신뢰 수준
  statistical_power: 80%          # 검정력
```

### 간이 계산표

| 현재 전환율 | 10% 개선 탐지 | 20% 개선 탐지 |
|------------|--------------|--------------|
| 1% | 156,000 | 39,000 |
| 2% | 77,000 | 19,000 |
| 5% | 30,000 | 7,500 |
| 10% | 14,500 | 3,600 |
| 20% | 6,800 | 1,700 |

*각 변형(A, B)당 필요 방문자 수*

### 테스트 기간 계산

```
필요 기간 = 필요 표본 크기 ÷ 일일 트래픽

예: 10,000명 필요, 일일 500명 방문
→ 10,000 ÷ 500 = 20일 (최소)
```

## 워크플로우

```
1. 테스트 대상 & 목표 정의
      │
      ▼
2. 가설 수립
      │
      ▼
3. 변수 & 변형 정의
      │
      ▼
4. 표본 크기 계산
      │
      ▼
5. 테스트 기간 결정
      │
      ▼
6. 성공 기준 정의
      │
      ▼
7. 테스트 설계 문서 저장
   → workspace/work-marketing/ab-tests/{test-name}-design.md
```

## 출력 템플릿

```markdown
# {Test Name} A/B Test Design

## Test Overview

| 항목 | 내용 |
|------|------|
| 테스트명 | {test_name} |
| 테스트 대상 | {subject} (LP / Email / Ad) |
| 테스트 변수 | {variable} |
| 시작일 | {start_date} |
| 예상 종료일 | {end_date} |
| 상태 | 계획 / 진행 중 / 완료 |

---

## Hypothesis (가설)

### 가설 문장

> 만약 **{change}**을 하면,
> **{metric}**이 **{direction}**할 것이다.
> 왜냐하면 **{reason}**이기 때문이다.

### 배경

{why_this_test}

---

## Test Design

### Control (A) vs Variant (B)

| 요소 | Control (A) | Variant (B) |
|------|-------------|-------------|
| {element} | {a_version} | {b_version} |

### Visual Comparison

```
┌─────────────────┐     ┌─────────────────┐
│   Control (A)   │     │   Variant (B)   │
├─────────────────┤     ├─────────────────┤
│                 │     │                 │
│  {description}  │     │  {description}  │
│                 │     │                 │
└─────────────────┘     └─────────────────┘
```

---

## Traffic Allocation

| 변형 | 트래픽 비율 |
|------|-----------|
| Control (A) | 50% |
| Variant (B) | 50% |

---

## Sample Size Calculation

### Inputs

| 항목 | 값 |
|------|-----|
| 현재 전환율 | {baseline_rate}% |
| 최소 탐지 효과 | {mde}% (상대적) |
| 신뢰 수준 | 95% |
| 검정력 | 80% |

### Required Sample

| 항목 | 값 |
|------|-----|
| 변형당 필요 샘플 | {sample_per_variant} |
| 총 필요 샘플 | {total_sample} |
| 일일 트래픽 | {daily_traffic} |
| **예상 테스트 기간** | **{duration}일** |

---

## Success Metrics

### Primary Metric

| 지표 | 현재 | 목표 (최소) | 측정 방법 |
|------|------|------------|----------|
| {primary_metric} | {current}% | {target}% | {method} |

### Secondary Metrics

| 지표 | 현재 | 모니터링 |
|------|------|---------|
| {secondary_1} | {current} | {notes} |
| {secondary_2} | {current} | {notes} |

### Guardrail Metrics (보호 지표)

| 지표 | 허용 범위 | 의미 |
|------|----------|------|
| {guardrail_1} | ±{threshold}% | {meaning} |

---

## Decision Framework

### 결과 해석

| 시나리오 | 액션 |
|---------|------|
| B가 통계적으로 유의미하게 우수 | B로 전환 |
| A가 통계적으로 유의미하게 우수 | A 유지 |
| 차이 없음 (Inconclusive) | 더 오래 테스트 또는 다른 변수 |
| B가 우수하나 guardrail 위반 | 추가 분석 |

### 통계적 유의성 기준

- **p-value**: < 0.05
- **신뢰 구간**: 0을 포함하지 않음
- **최소 테스트 기간**: {min_duration}일

---

## Implementation Checklist

### Pre-Launch

- [ ] 가설 문서화 완료
- [ ] A/B 버전 구현 완료
- [ ] 트래킹 설정 확인
- [ ] 테스트 도구 설정 (Optimizely, VWO, GA4 등)
- [ ] QA 테스트 완료
- [ ] 팀 공유 & 승인

### During Test

- [ ] 일일 모니터링
- [ ] 이상 징후 확인
- [ ] 외부 요인 기록 (휴일, 프로모션 등)

### Post-Test

- [ ] 결과 분석
- [ ] 통계적 유의성 확인
- [ ] 결과 문서화
- [ ] 승자 구현
- [ ] 팀 공유

---

## Timeline

```
Week 1          Week 2          Week 3          Week 4
   │               │               │               │
   ▼               ▼               ▼               ▼
┌──────┐       ┌──────┐       ┌──────┐       ┌──────┐
│ 준비 │   →   │ 실행 │   →   │ 실행 │   →   │ 분석 │
│      │       │ 모니터│       │ 모니터│       │ 결정 │
└──────┘       └──────┘       └──────┘       └──────┘
```

---

## Notes & Risks

### 주의사항

- {note_1}
- {note_2}

### 리스크

| 리스크 | 대응 |
|--------|------|
| {risk_1} | {mitigation} |
| {risk_2} | {mitigation} |

---

## Results (테스트 완료 후 작성)

### Raw Data

| 변형 | 방문자 | 전환 | 전환율 |
|------|--------|------|--------|
| Control (A) | {visitors} | {conversions} | {rate}% |
| Variant (B) | {visitors} | {conversions} | {rate}% |

### Statistical Analysis

| 항목 | 값 |
|------|-----|
| 상대적 개선 | {improvement}% |
| p-value | {p_value} |
| 통계적 유의성 | Yes / No |

### Conclusion

{conclusion_summary}

### Next Steps

1. {next_step_1}
2. {next_step_2}

---

*Created: {date}*
*Owner: {owner}*
```

## 테스트 우선순위 매트릭스

```
      High Impact
           │
     ┌─────┼─────┐
     │ ②  │  ①  │  ← 먼저 테스트
Easy ├─────┼─────┤ Hard
     │ ④  │  ③  │
     └─────┼─────┘
           │
      Low Impact
```

## 다음 스킬 연결

- **Analytics KPI Skill**: 테스트 결과 분석
- **Landing Page Skill**: LP 테스트 적용
- **Email Sequence Skill**: 이메일 테스트 적용

---

*A/B 테스트의 핵심은 "한 번에 하나만" 테스트하는 것입니다.*
*여러 변수를 동시에 바꾸면 뭐가 효과인지 모릅니다.*
