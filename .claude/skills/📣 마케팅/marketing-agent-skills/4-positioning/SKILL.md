---
name: mkt-positioning
description: |
  STP 전략 및 포지셔닝 맵 수립.
  경쟁사 대비 차별화된 위치를 정의합니다.
triggers:
  - "포지셔닝"
  - "STP 전략"
  - "차별화"
  - "타겟팅"
input:
  - context/{project}-context.md
  - research/{project}-3c-analysis.md
  - personas/*.md
output:
  - strategy/positioning.md
---

# Positioning Skill

STP(Segmentation, Targeting, Positioning) 전략을 수립합니다.
경쟁사 대비 명확한 차별화 위치를 정의합니다.

## STP 프레임워크

```
┌─────────────────────────────────────────────────────────────┐
│                         STP                                  │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│   ┌──────────────┐   ┌──────────────┐   ┌──────────────┐   │
│   │ Segmentation │ → │  Targeting   │ → │ Positioning  │   │
│   │   (세분화)    │   │   (타겟팅)   │   │  (포지셔닝)   │   │
│   └──────────────┘   └──────────────┘   └──────────────┘   │
│                                                              │
│   시장을 나눈다      어디에 집중할지    어떻게 인식될지      │
│                      결정한다          정의한다             │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

## 1. Segmentation (시장 세분화)

### 세분화 기준

```yaml
demographic:              # 인구통계적
  - age
  - gender
  - income
  - occupation
  - company_size (B2B)

geographic:               # 지리적
  - region
  - urban/rural
  - climate

psychographic:            # 심리적
  - lifestyle
  - values
  - personality
  - interests

behavioral:               # 행동적
  - usage_rate
  - loyalty
  - benefits_sought
  - purchase_occasion
```

### 세그먼트 평가 기준

```
□ Measurable (측정 가능)  - 규모 파악 가능?
□ Accessible (접근 가능)  - 마케팅 도달 가능?
□ Substantial (규모 충분) - 수익성 있는 규모?
□ Differentiable (차별화) - 세그먼트간 차이?
□ Actionable (실행 가능)  - 마케팅 프로그램 개발 가능?
```

## 2. Targeting (타겟팅)

### 타겟팅 전략

```
1. Undifferentiated (비차별화)
   └─ 전체 시장에 하나의 제안

2. Differentiated (차별화)
   └─ 여러 세그먼트에 각각 다른 제안

3. Concentrated (집중)
   └─ 하나의 세그먼트에 집중

4. Micromarketing (마이크로)
   └─ 개인 수준 맞춤화
```

### 타겟 세그먼트 선정 기준

```yaml
attractiveness:
  market_size: ""         # 시장 규모
  growth_rate: ""         # 성장률
  profitability: ""       # 수익성
  competition: ""         # 경쟁 강도

fit:
  company_resources: ""   # 자사 역량 적합성
  strategic_fit: ""       # 전략 적합성
  competitive_advantage: "" # 경쟁 우위 발휘 가능성
```

## 3. Positioning (포지셔닝)

### 포지셔닝 공식

```
For [타겟 고객],
[브랜드]는 [카테고리]로서,
[핵심 편익]을 제공합니다.
왜냐하면 [차별화 이유]이기 때문입니다.
```

### 포지셔닝 맵

```
                     High Price
                         │
                         │
           Premium       │      Luxury
           (고급형)       │      (럭셔리)
                         │
    ─────────────────────┼─────────────────────
    Low                  │                High
    Functionality        │          Functionality
                         │
           Budget        │      Value
           (저가형)       │      (가성비)
                         │
                     Low Price
```

### 차별화 영역

```yaml
product_differentiation:
  - features              # 기능
  - performance           # 성능
  - design                # 디자인
  - reliability           # 신뢰성

service_differentiation:
  - delivery              # 배송
  - installation          # 설치
  - customer_support      # 고객 지원
  - training              # 교육

channel_differentiation:
  - coverage              # 커버리지
  - expertise             # 전문성
  - performance           # 성과

people_differentiation:
  - competence            # 역량
  - courtesy              # 친절
  - credibility           # 신뢰

image_differentiation:
  - symbols               # 심볼
  - media                 # 미디어
  - atmosphere            # 분위기
```

## 워크플로우

```
1. 기존 문서 확인
   ├─ 컨텍스트
   ├─ 3C 분석
   └─ 페르소나
      │
      ▼
2. Segmentation
   └─ 시장 세분화, 세그먼트 정의
      │
      ▼
3. Targeting
   └─ 타겟 세그먼트 선정, 우선순위
      │
      ▼
4. Positioning
   ├─ 포지셔닝 공식 작성
   ├─ 포지셔닝 맵 생성
   └─ 차별화 메시지 도출
      │
      ▼
5. 문서 저장
   → workspace/work-marketing/strategy/positioning.md
```

## 출력 템플릿

```markdown
# {Project Name} Positioning Strategy

## Executive Summary

{포지셔닝 한 줄 요약}

---

## 1. Segmentation (시장 세분화)

### 세분화 기준

| 기준 | 변수 | 세그먼트 |
|------|------|----------|
| 인구통계 | {variable} | {segments} |
| 행동 | {variable} | {segments} |
| 심리 | {variable} | {segments} |

### 세그먼트 정의

#### Segment A: {Name}

| 항목 | 내용 |
|------|------|
| 규모 | {size} |
| 특성 | {characteristics} |
| 니즈 | {needs} |
| 현재 행동 | {behavior} |

#### Segment B: {Name}
...

### 세그먼트 비교

| 세그먼트 | 규모 | 성장률 | 경쟁 | 접근성 | 총점 |
|---------|------|--------|------|--------|------|
| A | ⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐ | ⭐⭐⭐ | 11 |
| B | ⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐ | 11 |
| C | ⭐⭐⭐⭐ | ⭐⭐ | ⭐⭐⭐⭐ | ⭐ | 11 |

---

## 2. Targeting (타겟팅)

### 타겟팅 전략

**선택**: {Concentrated/Differentiated/...}

**근거**: {rationale}

### 타겟 우선순위

| 순위 | 세그먼트 | 이유 | 마케팅 비중 |
|------|---------|------|------------|
| 1 | {primary} | {reason} | 60% |
| 2 | {secondary} | {reason} | 30% |
| 3 | {tertiary} | {reason} | 10% |

### Primary Target 상세

```yaml
who: "{target_description}"
what_they_need: "{need}"
where_they_are: "{channels}"
when_they_buy: "{timing}"
why_they_choose_us: "{reason}"
```

---

## 3. Positioning (포지셔닝)

### 포지셔닝 공식

```
For [타겟 고객]
─────────────────────────────────────────
{target_customer}

[브랜드]는 [카테고리]로서
─────────────────────────────────────────
{brand}는 {category}로서

[핵심 편익]을 제공합니다
─────────────────────────────────────────
{key_benefit}을 제공합니다

왜냐하면 [차별화 이유]이기 때문입니다
─────────────────────────────────────────
왜냐하면 {reason_to_believe}이기 때문입니다
```

### 한 줄 포지셔닝

> "{one_line_positioning}"

### 포지셔닝 맵

```
            High {axis_1}
                 │
     ┌───────────┼───────────┐
     │           │           │
     │   [경쟁사A]│           │
     │           │    ★      │ ← 우리 위치
     │           │  [우리]    │
─────┼───────────┼───────────┼─────
Low  │           │           │  High
{axis_2}        │    [경쟁사B]│  {axis_2}
     │           │           │
     │           │           │
     └───────────┼───────────┘
                 │
            Low {axis_1}
```

**축 설명**:
- {axis_1}: {description}
- {axis_2}: {description}

### 경쟁사 대비 포지셔닝

| 브랜드 | 포지셔닝 | 핵심 메시지 |
|--------|----------|------------|
| 우리 | {positioning} | {message} |
| 경쟁사 A | {positioning_a} | {message_a} |
| 경쟁사 B | {positioning_b} | {message_b} |

---

## 4. 차별화 전략

### 핵심 차별화 포인트 (3개)

1. **{differentiator_1}**
   - 설명: {description}
   - 증거: {proof}
   - 고객 가치: {value}

2. **{differentiator_2}**
   - 설명: {description}
   - 증거: {proof}
   - 고객 가치: {value}

3. **{differentiator_3}**
   - 설명: {description}
   - 증거: {proof}
   - 고객 가치: {value}

### 차별화 유형

| 유형 | 내용 | 강도 |
|------|------|------|
| 제품 | {product_diff} | ⭐⭐⭐ |
| 서비스 | {service_diff} | ⭐⭐ |
| 가격 | {price_diff} | ⭐⭐⭐⭐ |
| 채널 | {channel_diff} | ⭐⭐ |

---

## 5. 메시징 가이드

### 핵심 메시지

**Primary Message**:
> "{primary_message}"

**Supporting Messages**:
1. {supporting_1}
2. {supporting_2}
3. {supporting_3}

### 메시지 프레임워크

| 타겟 | 핵심 메시지 | 지원 포인트 | 톤 |
|------|------------|------------|-----|
| {target_1} | {message} | {support} | {tone} |
| {target_2} | {message} | {support} | {tone} |

### 사용할 단어 vs 피할 단어

| 사용할 단어 | 피할 단어 |
|------------|----------|
| {word_1} | {avoid_1} |
| {word_2} | {avoid_2} |
| {word_3} | {avoid_3} |

---

## 6. 다음 단계

1. [ ] Strategy Skill로 마케팅 전략 수립
2. [ ] Copywriting Skill로 메시지 구체화
3. [ ] Campaign Skill로 캠페인 기획

---

*Created: {date}*
```

## 포지셔닝 예시

### SaaS 제품 예시

```
For 스타트업의 3-5년차 백엔드 개발자,

DevMonitor는 API 모니터링 도구로서,

복잡한 세팅 없이 5분 만에 시작할 수 있는
간편함을 제공합니다.

왜냐하면 우리는 개발자가 도구 세팅이 아닌
개발에 집중해야 한다고 믿기 때문입니다.

한 줄: "Datadog의 핵심 기능만, 10분의 1 가격으로"
```

## 다음 스킬 연결

- **Strategy Skill**: 포지셔닝 기반 마케팅 전략
- **Copywriting Skill**: 포지셔닝 메시지를 카피로 전환
- **Campaign Skill**: 타겟별 캠페인 기획

---

*명확한 포지셔닝 없이는 모든 마케팅이 흔들립니다.*
*"우리는 누구에게 무엇인가?"에 답할 수 있어야 합니다.*
