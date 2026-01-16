---
name: plan-value-proposition
description: |
  서비스의 핵심 가치 제안을 정의하는 스킬.
  UVP, 차별점, Why Now를 체계적으로 정리합니다.
triggers:
  - "가치 제안"
  - "UVP"
  - "차별점 정리"
  - "왜 우리 서비스"
input:
  - idea-intake.md 결과
  - 경쟁사 정보 (선택)
output:
  - 01-discovery/value-proposition.md
---

# Value Proposition Skill

서비스가 왜 존재해야 하는지, 고객이 왜 선택해야 하는지를 정의합니다.

## 핵심 프레임워크

### UVP (Unique Value Proposition) 공식

```
[타겟 고객]을 위한
[카테고리]로,
[핵심 편익]을 제공합니다.
[경쟁사]와 달리 [차별점]이 있습니다.
```

### Value Proposition Canvas

```
┌─────────────────────────────────────────────────────────────────┐
│                    Customer Profile                              │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│   Jobs-to-be-Done        Pains              Gains               │
│   ┌─────────────┐       ┌─────────────┐    ┌─────────────┐     │
│   │ 고객이 하려는│       │ 고객의      │    │ 고객이 원하는│     │
│   │ 일/목표     │       │ 불편/고통   │    │ 혜택/결과    │     │
│   └─────────────┘       └─────────────┘    └─────────────┘     │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
                              ▼ FIT ▼
┌─────────────────────────────────────────────────────────────────┐
│                    Value Map                                     │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│   Products/Services    Pain Relievers      Gain Creators        │
│   ┌─────────────┐     ┌─────────────┐    ┌─────────────┐       │
│   │ 우리가 제공 │     │ 고통을 줄이는│    │ 혜택을 만드는│       │
│   │ 하는 것     │     │ 방법        │    │ 방법         │       │
│   └─────────────┘     └─────────────┘    └─────────────┘       │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

## 수집/분석 항목

### 1. Customer Profile 분석

```yaml
jobs_to_be_done:
  functional:                 # 기능적 Job
    - ""                      # 예: "문서를 빠르게 작성하고 싶다"
  emotional:                  # 감정적 Job
    - ""                      # 예: "전문가처럼 보이고 싶다"
  social:                     # 사회적 Job
    - ""                      # 예: "팀에서 인정받고 싶다"

pains:
  obstacles: []               # 현재 방해물
  risks: []                   # 두려움/리스크
  undesired_outcomes: []      # 원치 않는 결과

gains:
  required: []                # 필수 기대
  expected: []                # 당연히 기대
  desired: []                 # 원하는 것
  unexpected: []              # 기대 이상
```

### 2. Value Map 정의

```yaml
products_services:
  core: ""                    # 핵심 제품/서비스
  features: []                # 주요 기능
  services: []                # 부가 서비스

pain_relievers:
  - pain: ""
    reliever: ""
    how: ""

gain_creators:
  - gain: ""
    creator: ""
    how: ""
```

### 3. Why Now 분석

```yaml
why_now:
  market_timing:              # 시장 타이밍
    - trend: ""               # 트렌드
    - evidence: ""            # 증거
  technology_timing:          # 기술 타이밍
    - enabler: ""             # 가능하게 하는 기술
    - maturity: ""            # 기술 성숙도
  regulatory_timing:          # 규제 타이밍
    - change: ""              # 규제 변화
    - opportunity: ""         # 기회
```

## 워크플로우

```
1. Idea Intake 결과 확인
      │
      ▼
2. Customer Profile 작성
      │
      ├─ Jobs-to-be-Done 분석
      ├─ Pains 정리
      └─ Gains 정리
      │
      ▼
3. Value Map 작성
      │
      ├─ Pain Relievers 매핑
      └─ Gain Creators 매핑
      │
      ▼
4. UVP 문장 도출
      │
      ▼
5. Why Now 분석
      │
      ▼
6. 경쟁 차별점 정리
      │
      ▼
7. 최종 문서 저장
   → workspace/work-plan/{project}/01-discovery/value-proposition.md
```

## 출력 템플릿

```markdown
# {Project Name} - 가치 제안

## Unique Value Proposition

> **{UVP 한 문장}**

### UVP 분해
| 요소 | 내용 |
|------|------|
| 타겟 고객 | {target_customer} |
| 카테고리 | {category} |
| 핵심 편익 | {key_benefit} |
| 차별점 | {differentiation} |

## 1. Customer Profile

### Jobs-to-be-Done

| 유형 | Job | 중요도 |
|------|-----|--------|
| 기능적 | {functional_job} | ⭐⭐⭐⭐⭐ |
| 감정적 | {emotional_job} | ⭐⭐⭐⭐ |
| 사회적 | {social_job} | ⭐⭐⭐ |

### Pains (고통)

| # | Pain | 심각도 | 빈도 |
|---|------|--------|------|
| 1 | {pain_1} | 🔴 High | 매일 |
| 2 | {pain_2} | 🟡 Medium | 주 2-3회 |
| 3 | {pain_3} | 🟢 Low | 가끔 |

### Gains (기대 혜택)

| # | Gain | 유형 | 중요도 |
|---|------|------|--------|
| 1 | {gain_1} | Required | ⭐⭐⭐⭐⭐ |
| 2 | {gain_2} | Desired | ⭐⭐⭐⭐ |
| 3 | {gain_3} | Unexpected | ⭐⭐⭐ |

## 2. Value Map

### Pain Relievers

| Pain | 우리의 해결책 | 방법 |
|------|-------------|------|
| {pain_1} | {reliever_1} | {how_1} |
| {pain_2} | {reliever_2} | {how_2} |
| {pain_3} | {reliever_3} | {how_3} |

### Gain Creators

| Gain | 우리의 제공 가치 | 방법 |
|------|----------------|------|
| {gain_1} | {creator_1} | {how_1} |
| {gain_2} | {creator_2} | {how_2} |

## 3. Why Now?

### 시장 타이밍

| 트렌드 | 증거 | 기회 |
|--------|------|------|
| {trend_1} | {evidence_1} | {opportunity_1} |
| {trend_2} | {evidence_2} | {opportunity_2} |

### 기술 타이밍

| 기술 | 성숙도 | 활용 |
|------|--------|------|
| {tech_1} | 상용화 | {usage_1} |
| {tech_2} | 초기 | {usage_2} |

### 왜 지금인가? (요약)
{why_now_summary}

## 4. 경쟁 차별화

### 차별점 매트릭스

| 경쟁사 | 우리 | 차별점 |
|--------|------|--------|
| {competitor_1} | {us_vs_1} | {diff_1} |
| {competitor_2} | {us_vs_2} | {diff_2} |

### 핵심 차별화 메시지

> "{differentiation_message}"

### Only We Can

우리만 할 수 있는 것:
1. {only_we_1}
2. {only_we_2}

## 5. Value Proposition Statement

### For Customers

```
{target_customer}를 위한 {service_name}은
{category}입니다.

{key_benefit}을 제공하여
{pain}을 해결합니다.

{competitor}와 달리,
{differentiation}합니다.
```

### Elevator Pitch (30초)

```
"{problem_hook}

{service_name}은 {solution_brief}

{key_result}을 달성할 수 있습니다.

{why_different}"
```

## 6. Value Proposition Test

### 테스트 질문

| 질문 | 답변 | 점수 |
|------|------|------|
| 고객이 이해할 수 있는가? | {yes/no} | /5 |
| 차별점이 명확한가? | {yes/no} | /5 |
| 측정 가능한 가치인가? | {yes/no} | /5 |
| 신뢰할 수 있는가? | {yes/no} | /5 |

### 개선 필요 사항
{improvement_needed}

---

*다음 단계: Target User 상세 정의*
```

## UVP 작성 팁

### 좋은 UVP 특징

```
✅ 명확함 - 누구나 이해할 수 있음
✅ 구체적 - 추상적이지 않음
✅ 차별화 - 경쟁사와 구분됨
✅ 검증 가능 - 측정할 수 있음
```

### 나쁜 UVP 특징

```
❌ "최고의 솔루션" - 주관적
❌ "혁신적인" - 모호함
❌ "올인원" - 초점 없음
❌ 기능 나열 - 가치 없음
```

### UVP 예시

| 서비스 | UVP |
|--------|-----|
| Slack | "이메일을 25% 줄여주는 팀 커뮤니케이션 툴" |
| Stripe | "개발자가 7줄 코드로 결제를 받을 수 있는 API" |
| Notion | "팀의 모든 업무를 한 곳에서 관리하는 올인원 워크스페이스" |

## 퀄리티 체크리스트

```
□ UVP가 한 문장으로 정리되었는가?
□ Jobs-to-be-Done이 3가지 이상 식별되었는가?
□ 핵심 Pain 3가지가 정리되었는가?
□ Pain Reliever가 명확히 매핑되었는가?
□ Why Now가 설득력 있는가?
□ 경쟁 차별점이 구체적인가?
□ Elevator Pitch가 30초 내 전달 가능한가?
```

## 🎯 인터랙티브 가이드

### 작성 전 확인 질문

**Q1. UVP를 한 문장으로 말할 수 있나요?**
- 가능 → 바로 검증 진행
- 어려움 → "타겟 고객의 가장 큰 Pain은 무엇인가요?"

**Q2. 경쟁사 대비 차별점이 명확한가요?**
- 명확함 → 구체적 차별점 작성
- 불명확 → "경쟁사가 못하는 것 중 우리가 할 수 있는 건?"

**Q3. 고객이 이 가치에 돈을 낼까요?**
- 확신 있음 → 근거 확인 ("어떤 증거가 있나요?")
- 불확실 → 검증 방법 제안

### 의사결정 포인트

| 시점 | 확인 내용 | 사용자 프롬프트 |
|------|----------|----------------|
| Pain 분석 | 심각도 | "이 Pain이 얼마나 심각한가요? (1-10)" |
| Gain 분석 | 기대 수준 | "고객이 가장 원하는 결과는?" |
| 차별화 | 지속성 | "이 차별점을 경쟁사가 복제하기 어려운가요?" |
| 최종 확인 | 명확성 | "고객이 10초 안에 이해할 수 있나요?" |

---

## 다음 스킬 연결

Value Proposition 완료 후:

1. **타겟 구체화** → Target User Skill
2. **시장 규모 확인** → Market Research Skill
3. **경쟁사 심화 분석** → Competitor Analysis Skill

---

*강력한 Value Proposition은 모든 후속 기획의 나침반입니다.*
