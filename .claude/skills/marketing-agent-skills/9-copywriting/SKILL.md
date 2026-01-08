---
name: mkt-copywriting
description: |
  AIDA, PAS, BAB 등 프레임워크 기반 카피라이팅.
  헤드라인, 가치 제안, CTA 등 다양한 카피를 생성합니다.
triggers:
  - "카피라이팅"
  - "헤드라인"
  - "광고 문구"
  - "카피 써줘"
input:
  - context/{project}-context.md
  - strategy/positioning.md
  - personas/*.md
output:
  - copy/headlines.md
  - copy/value-propositions.md
  - copy/cta-variations.md
---

# Copywriting Skill

프레임워크 기반의 마케팅 카피를 생성합니다.

## 카피라이팅 프레임워크

### 1. AIDA

```
┌─────────────────────────────────────────────────────────────┐
│                         AIDA                                 │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│   A - Attention (주의)                                       │
│       헤드라인으로 시선을 끈다                                 │
│                                                              │
│   I - Interest (관심)                                        │
│       문제나 기회를 제시한다                                   │
│                                                              │
│   D - Desire (욕구)                                          │
│       해결책의 혜택을 보여준다                                 │
│                                                              │
│   A - Action (행동)                                          │
│       구체적인 다음 단계를 제시한다                            │
│                                                              │
└─────────────────────────────────────────────────────────────┘

적합한 용도: 랜딩페이지, 이메일, 긴 형식 광고
```

**예시:**
```
[A] 개발자, 아직도 모니터링에 시간 쓰세요?
[I] 하루 1시간을 알림 확인에 쓰고 있다면...
[D] DevMonitor는 중요한 알림만 골라서 전달합니다.
    이미 500개 팀이 시간을 아끼고 있어요.
[A] 5분 만에 시작하기 →
```

### 2. PAS

```
┌─────────────────────────────────────────────────────────────┐
│                          PAS                                 │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│   P - Problem (문제)                                         │
│       고객의 문제를 명확히 짚는다                              │
│                                                              │
│   A - Agitation (자극)                                       │
│       문제의 심각성을 강조한다                                 │
│                                                              │
│   S - Solution (해결책)                                      │
│       우리 제품이 해결책임을 제시한다                          │
│                                                              │
└─────────────────────────────────────────────────────────────┘

적합한 용도: 짧은 광고, 이메일 제목, 긴급 제안
```

**예시:**
```
[P] 서버 장애, 또 새벽에 알게 됐나요?
[A] 고객이 먼저 알고, 슬랙에 불만이 쏟아지고,
    당신은 그제서야 달려갑니다.
[S] DevMonitor는 장애 30초 전에 알려드립니다.
    더 이상 새벽 콜에 시달리지 마세요.
```

### 3. BAB

```
┌─────────────────────────────────────────────────────────────┐
│                          BAB                                 │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│   B - Before (이전)                                          │
│       현재의 고통스러운 상황                                   │
│                                                              │
│   A - After (이후)                                           │
│       제품 사용 후의 이상적인 상황                             │
│                                                              │
│   B - Bridge (다리)                                          │
│       Before에서 After로 가는 방법 = 우리 제품                 │
│                                                              │
└─────────────────────────────────────────────────────────────┘

적합한 용도: 케이스 스터디, 변화 강조, 스토리텔링
```

**예시:**
```
[Before]
매번 수동으로 로그 확인. 장애 발견까지 평균 30분.
팀원들의 야근은 일상.

[After]
실시간 알림으로 1분 내 대응. 장애 해결 시간 80% 단축.
팀원들이 퇴근 후에도 쉴 수 있게 됐습니다.

[Bridge]
DevMonitor 하나면 됩니다.
지금 시작하세요 →
```

### 4. FAB

```
┌─────────────────────────────────────────────────────────────┐
│                          FAB                                 │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│   F - Features (기능)                                        │
│       제품이 가진 것                                          │
│                                                              │
│   A - Advantages (장점)                                      │
│       그 기능이 좋은 이유                                     │
│                                                              │
│   B - Benefits (혜택)                                        │
│       고객이 얻는 가치                                        │
│                                                              │
└─────────────────────────────────────────────────────────────┘

적합한 용도: 제품 설명, 기능 소개
```

**예시:**
```
[F] AI 기반 이상 탐지
[A] 수동 임계값 설정 불필요
[B] 세팅 시간 90% 절약, 바로 사용 가능
```

### 5. 4P's

```
┌─────────────────────────────────────────────────────────────┐
│                          4P's                                │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│   Promise (약속) - 핵심 혜택 약속                             │
│   Picture (그림) - 혜택의 생생한 묘사                         │
│   Proof (증거) - 약속의 증거                                  │
│   Push (촉구) - 행동 유도                                     │
│                                                              │
└─────────────────────────────────────────────────────────────┘

적합한 용도: 세일즈 레터, 긴 형식 설득
```

## 카피 유형별 템플릿

### 헤드라인

```yaml
headline_formulas:
  question:
    - "아직도 {old_way} 하세요?"
    - "{target}, {pain_point} 겪고 있나요?"

  how_to:
    - "{result}하는 방법"
    - "어떻게 {company}는 {result}했을까"

  number:
    - "{number}가지 {benefit} 방법"
    - "{company}가 {result}한 {number}가지 비밀"

  comparison:
    - "{competitor} vs {us}: {differentiator}"
    - "{old_way} 대신 {new_way}"

  proof:
    - "{number}개 팀이 선택한 {product}"
    - "{result}을 달성한 {number}명의 {target}"

  urgency:
    - "지금 {action}하면 {benefit}"
    - "{deadline}까지만 {offer}"

  curiosity:
    - "{target}이 모르는 {topic}의 진실"
    - "왜 {unexpected_thing}이 {result}을 만들까"
```

### 가치 제안 (Value Proposition)

```yaml
value_prop_structure:
  headline: "{target}를 위한 {category}"
  subheadline: "{key_benefit}을 {how}"
  bullets:
    - "{feature} → {benefit}"
    - "{feature} → {benefit}"
    - "{feature} → {benefit}"
  proof: "{social_proof}"
  cta: "{action}"
```

### CTA (Call-to-Action)

```yaml
cta_types:
  direct:
    - "지금 시작하기"
    - "무료로 체험하기"
    - "데모 신청하기"

  benefit_focused:
    - "시간 아끼기 시작"
    - "생산성 높이기"
    - "성장 시작하기"

  low_commitment:
    - "둘러보기"
    - "더 알아보기"
    - "무료로 확인하기"

  urgency:
    - "오늘만 50% 할인"
    - "선착순 100명"
    - "마감 임박"
```

## 워크플로우

```
1. 컨텍스트 & 포지셔닝 확인
      │
      ▼
2. 타겟 페르소나 확인
      │
      ▼
3. 카피 유형 결정
   ├─ 헤드라인
   ├─ 가치 제안
   ├─ CTA
   └─ 풀 카피
      │
      ▼
4. 프레임워크 선택
   ├─ AIDA (긴 형식)
   ├─ PAS (긴급/문제 중심)
   ├─ BAB (변화 강조)
   └─ FAB (기능 설명)
      │
      ▼
5. 카피 변형 생성 (10개+)
      │
      ▼
6. 문서 저장
   → workspace/work-marketing/copy/*.md
```

## 출력 템플릿

```markdown
# {Project Name} Copy Library

## Context Recap

| 항목 | 내용 |
|------|------|
| 제품 | {product} |
| 타겟 | {target} |
| 핵심 혜택 | {key_benefit} |
| 톤 | {tone} |
| 차별점 | {differentiator} |

---

## Headlines (헤드라인)

### AIDA 스타일

1. {headline_1}
2. {headline_2}
3. {headline_3}

### 질문형

1. {headline_1}
2. {headline_2}
3. {headline_3}

### 숫자형

1. {headline_1}
2. {headline_2}
3. {headline_3}

### 비교형

1. {headline_1}
2. {headline_2}
3. {headline_3}

### 증거형

1. {headline_1}
2. {headline_2}
3. {headline_3}

---

## Subheadlines (서브 헤드라인)

1. {subheadline_1}
2. {subheadline_2}
3. {subheadline_3}
4. {subheadline_4}
5. {subheadline_5}

---

## Value Propositions (가치 제안)

### Version 1

> **{headline}**
>
> {subheadline}
>
> - {bullet_1}
> - {bullet_2}
> - {bullet_3}

### Version 2
...

### Version 3
...

---

## Full Copy Examples

### AIDA Format

**Attention:**
{attention_copy}

**Interest:**
{interest_copy}

**Desire:**
{desire_copy}

**Action:**
{action_copy}

---

### PAS Format

**Problem:**
{problem_copy}

**Agitation:**
{agitation_copy}

**Solution:**
{solution_copy}

---

### BAB Format

**Before:**
{before_copy}

**After:**
{after_copy}

**Bridge:**
{bridge_copy}

---

## CTA Variations

### Direct

1. {cta_1}
2. {cta_2}
3. {cta_3}

### Benefit-Focused

1. {cta_1}
2. {cta_2}
3. {cta_3}

### Low Commitment

1. {cta_1}
2. {cta_2}
3. {cta_3}

---

## Bullets & Features

### Feature → Benefit

| Feature | Benefit |
|---------|---------|
| {feature_1} | {benefit_1} |
| {feature_2} | {benefit_2} |
| {feature_3} | {benefit_3} |

### Power Words to Use

{power_words_list}

### Words to Avoid

{words_to_avoid}

---

## A/B Test Suggestions

| Element | Version A | Version B | Hypothesis |
|---------|-----------|-----------|------------|
| Headline | {a} | {b} | {hypothesis} |
| CTA | {a} | {b} | {hypothesis} |
| Social Proof | {a} | {b} | {hypothesis} |

---

## Usage Guide

| 용도 | 추천 카피 |
|------|----------|
| 랜딩페이지 Hero | Headline #{n}, Value Prop #{n} |
| 광고 | Headline #{n}, CTA #{n} |
| 이메일 제목 | Headline #{n} (질문형) |
| 버튼 | CTA #{n} |

---

*Created: {date}*
*Persona: {persona_name}*
```

## 퀄리티 팁

### 좋은 카피의 특징

```
✅ 타겟이 명확함
✅ 혜택 중심 (기능 X)
✅ 구체적인 숫자/증거
✅ 감정을 자극
✅ 행동을 유도
✅ 간결함
```

### 피해야 할 것

```
❌ 모호한 표현 ("혁신적인", "최고의")
❌ 전문 용어 남발
❌ 기능만 나열
❌ 너무 긴 문장
❌ CTA 없음
```

## 다음 스킬 연결

- **Landing Page Skill**: 카피를 LP 구조에 배치
- **Email Sequence Skill**: 이메일 카피 작성
- **Ads Creative Skill**: 광고 카피 작성
- **A/B Testing Skill**: 카피 테스트 설계

---

*좋은 카피는 "우리가 뭘 파는가"가 아니라*
*"고객이 뭘 얻는가"를 말합니다.*
