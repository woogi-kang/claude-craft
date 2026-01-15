---
name: plan-pitch-deck
description: |
  피치덱 구조를 기획하는 스킬.
  투자 유치용 또는 사업 소개용 피치덱 구조를 설계합니다.
triggers:
  - "피치덱"
  - "Pitch Deck"
  - "투자 제안서"
  - "IR 자료"
input:
  - 모든 기획 문서
  - business-model.md 결과
  - market-research.md 결과
output:
  - 08-launch/pitch-deck-structure.md
---

# Pitch Deck Skill

투자 유치용 피치덱 구조와 콘텐츠를 기획합니다.

## 피치덱 유형

| 유형 | 용도 | 슬라이드 | 시간 |
|------|------|---------|------|
| 티저 덱 | 초기 관심 유도 | 5-7장 | 2분 |
| 미팅 덱 | 투자자 미팅 | 10-15장 | 10-20분 |
| 풀 덱 | 상세 검토용 | 20-30장 | 읽기용 |

## 출력 템플릿

```markdown
# {Project Name} - 피치덱 구조

## 1. 피치덱 Overview

### 버전

| 항목 | 내용 |
|------|------|
| 회사명 | {company_name} |
| 라운드 | Pre-Seed / Seed / Series A |
| 목표 금액 | {amount} |
| 용도 | 투자 유치 / 사업 소개 / 파트너십 |
| 버전 | v{n} |
| 업데이트 | {date} |

### 핵심 메시지

> **One-liner: "{one_liner}"**

**엘리베이터 피치 (30초)**
```
{company_name}는 {target_customer}가 겪는 {problem}를
{solution}으로 해결합니다.
우리의 {unique_value}로 {market_size} 시장에서
{traction}을 달성했습니다.
```

---

## 2. 슬라이드 구조

### 표준 구조 (12장)

| # | 슬라이드 | 핵심 질문 | 시간 |
|---|----------|----------|------|
| 1 | Cover | 우리가 누구인가? | 15초 |
| 2 | Problem | 어떤 문제를 해결하나? | 1분 |
| 3 | Solution | 어떻게 해결하나? | 1분 |
| 4 | Market | 시장은 얼마나 큰가? | 1분 |
| 5 | Product | 제품은 어떻게 작동하나? | 2분 |
| 6 | Business Model | 어떻게 돈을 버나? | 1분 |
| 7 | Traction | 지금까지 무엇을 달성했나? | 1분 |
| 8 | Go-to-Market | 어떻게 성장할 것인가? | 1분 |
| 9 | Competition | 경쟁사 대비 우위는? | 1분 |
| 10 | Team | 왜 이 팀이 할 수 있나? | 1분 |
| 11 | Financials | 재무 계획은? | 1분 |
| 12 | Ask | 무엇이 필요한가? | 30초 |

### 슬라이드 흐름

```
Story Arc:
─────────────────────────────────────────────────────────────────

 Attention    Problem     Solution    Validation   Action
     │           │            │            │          │
  Cover →   Problem →  Solution →  Traction →    Ask
     │           │            │            │          │
     │       Market       Product      Team      Financials
     │                   Business    Competition
     │                    Model        GTM
     │
     └──► Hook: 왜 지금 들어야 하는가?
```

---

## 3. 슬라이드 상세

### Slide 1: Cover

**목적**: 첫인상, 기억에 남는 훅

**포함 요소**
- 로고
- 회사명
- 태그라인 (One-liner)
- 발표자 이름
- 연락처

**권장 내용**
```
{Company Logo}

{Company Name}
"{Tagline}"

{Presenter Name}
{Date}
```

---

### Slide 2: Problem

**목적**: 공감할 수 있는 문제 제시

**핵심 질문**
- 누가 이 문제를 겪는가?
- 얼마나 심각한 문제인가?
- 기존 해결책의 한계는?

**권장 구조**

| 섹션 | 내용 |
|------|------|
| 헤드라인 | "{pain_statement}" |
| 고객 인용 | "{customer_quote}" |
| 현 상황 | {current_situation} |
| 페인 포인트 | 1. {pain_1} 2. {pain_2} 3. {pain_3} |
| 비용 | {cost_of_problem} |

**팁**
```
✅ 구체적인 숫자로 표현
✅ 고객의 언어로 설명
✅ 감정적 공감 유도
❌ 너무 많은 문제 나열
```

---

### Slide 3: Solution

**목적**: 명확하고 간결한 해결책 제시

**핵심 질문**
- 어떻게 문제를 해결하는가?
- 왜 이 방식이 효과적인가?
- 고객에게 어떤 가치를 주는가?

**권장 구조**

| 섹션 | 내용 |
|------|------|
| 헤드라인 | "{solution_statement}" |
| How it works | 3단계로 설명 |
| Before/After | 변화 비교 |
| 핵심 가치 | {key_benefit} |

**Before → After**
```
Before (기존)              After (우리)
─────────────              ─────────────
{old_way_1}       →       {new_way_1}
{old_way_2}       →       {new_way_2}
{old_way_3}       →       {new_way_3}
```

---

### Slide 4: Market

**목적**: 충분히 큰 시장 기회 입증

**핵심 질문**
- TAM/SAM/SOM은 얼마인가?
- 시장은 성장하고 있는가?
- 왜 지금인가?

**권장 구조**

```
TAM (전체 시장)
  │
  └─► ${TAM_amount} - {definition}
       │
       ├─► SAM (접근 가능 시장)
       │    │
       │    └─► ${SAM_amount} - {definition}
       │         │
       │         └─► SOM (목표 시장)
       │              │
       │              └─► ${SOM_amount} - {definition}
       │
       └─► 연 성장률: {CAGR}%
```

**시장 타이밍 (Why Now)**
- {timing_factor_1}
- {timing_factor_2}
- {timing_factor_3}

---

### Slide 5: Product

**목적**: 제품이 어떻게 작동하는지 보여주기

**핵심 질문**
- 실제로 어떻게 동작하는가?
- 핵심 기능은 무엇인가?
- 사용자 경험은 어떤가?

**권장 구조**

| 섹션 | 내용 |
|------|------|
| 스크린샷/데모 | 실제 제품 화면 |
| 핵심 기능 3개 | 간결하게 |
| 사용 흐름 | Step 1 → 2 → 3 |

**데모 가이드**
```
Demo Flow:
1. {user_action_1} - {benefit_1}
2. {user_action_2} - {benefit_2}
3. {user_action_3} - {benefit_3}
4. 결과 확인 - Aha Moment
```

**팁**
```
✅ 실제 작동하는 데모
✅ 핵심 기능에 집중
✅ 고객 관점에서 설명
❌ 모든 기능 나열
```

---

### Slide 6: Business Model

**목적**: 수익화 방식과 단위 경제 설명

**핵심 질문**
- 어떻게 돈을 버는가?
- 가격 구조는 어떤가?
- 단위 경제가 성립하는가?

**권장 구조**

| 요소 | 내용 |
|------|------|
| 수익 모델 | {model}: Subscription / Transaction / etc |
| 가격 | {pricing_structure} |
| LTV | ${ltv} |
| CAC | ${cac} |
| LTV/CAC | {ratio}x |

**Unit Economics**
```
Revenue per Customer
─────────────────────────────────────
ARPU:        ${arpu}/월
Retention:   {months}개월
LTV:         ${ltv}

Cost to Acquire
─────────────────────────────────────
CAC:         ${cac}
Payback:     {months}개월
LTV/CAC:     {ratio}x
```

---

### Slide 7: Traction

**목적**: 검증된 성과와 모멘텀 보여주기

**핵심 질문**
- 지금까지 무엇을 달성했는가?
- 성장하고 있는가?
- 검증된 것은 무엇인가?

**권장 구조**

| 지표 | 수치 | 성장률 |
|------|------|--------|
| 사용자 | {n} | +{%} MoM |
| 매출 | ${n} | +{%} MoM |
| 고객사 | {n} | +{%} MoM |
| 리텐션 | {%} | - |

**성장 그래프**
```
Revenue Growth
     │
{max}├────────────────────────●
     │                      ╱
     │                    ╱
     │                  ╱
     │                ╱
     │              ╱
     │            ╱
{min}├──────────●
     └────────────────────────►
          Jan    Mar    Jun
```

**주요 마일스톤**
- ✅ {milestone_1} - {date}
- ✅ {milestone_2} - {date}
- 🔜 {milestone_3} - {date}

---

### Slide 8: Go-to-Market

**목적**: 성장 전략과 채널 설명

**핵심 질문**
- 어떻게 고객을 획득하는가?
- 확장 가능한 전략인가?
- 경쟁 우위를 활용하는가?

**권장 구조**

| 채널 | 전략 | 비중 |
|------|------|------|
| {channel_1} | {strategy} | {%} |
| {channel_2} | {strategy} | {%} |
| {channel_3} | {strategy} | {%} |

**성장 레버**
```
1. {lever_1} → {expected_impact}
2. {lever_2} → {expected_impact}
3. {lever_3} → {expected_impact}
```

---

### Slide 9: Competition

**목적**: 경쟁 환경과 차별화 설명

**핵심 질문**
- 경쟁사는 누구인가?
- 차별점은 무엇인가?
- 왜 이길 수 있는가?

**권장 구조: 2x2 매트릭스**

```
              {Axis Y Label}
                    │
            ┌───────┼───────┐
            │       │{Us} ★ │
    {Comp A}│●      │       │
            │       │       │
    ────────┼───────┼───────┼──── {Axis X Label}
            │       │       │
            │  ●    │       │
            │{Comp B}   ●   │
            └───────┼{Comp C}┘
                    │
```

**경쟁 우위**
| 우리의 강점 | 경쟁사 약점 |
|------------|-----------|
| {strength_1} | {weakness_1} |
| {strength_2} | {weakness_2} |

**방어 가능성 (Moat)**
- {moat_1}
- {moat_2}

---

### Slide 10: Team

**목적**: 실행력과 신뢰성 입증

**핵심 질문**
- 왜 이 팀이 성공할 수 있는가?
- 관련 경험이 있는가?
- 팀이 완전한가?

**권장 구조**

| 멤버 | 역할 | 배경 | 특징 |
|------|------|------|------|
| {name} | CEO | {background} | {highlight} |
| {name} | CTO | {background} | {highlight} |
| {name} | {role} | {background} | {highlight} |

**Founder-Market Fit**
```
왜 우리인가?
─────────────────────────────────────
- {unique_insight_1}
- {unique_insight_2}
- {relevant_experience}
```

**어드바이저**
- {advisor_1}: {background}
- {advisor_2}: {background}

---

### Slide 11: Financials

**목적**: 재무 전망과 자금 사용 계획

**핵심 질문**
- 향후 재무 전망은?
- 자금을 어떻게 사용할 것인가?
- 다음 마일스톤은?

**권장 구조**

| 연도 | 매출 | 비용 | Net |
|------|------|------|-----|
| Year 1 | ${n} | ${n} | ${n} |
| Year 2 | ${n} | ${n} | ${n} |
| Year 3 | ${n} | ${n} | ${n} |

**자금 사용 계획**
```
총 ${amount} 사용 계획:

Product/Engineering:  {%}%  ████████████████
Sales/Marketing:      {%}%  ██████████
Operations:           {%}%  ████
```

**Key Milestones (with funding)**
- 6개월: {milestone_6m}
- 12개월: {milestone_12m}
- 18개월: {milestone_18m}

---

### Slide 12: Ask

**목적**: 명확한 요청과 다음 단계

**권장 구조**

| 항목 | 내용 |
|------|------|
| 투자 요청 | ${amount} |
| 라운드 | {round_type} |
| 밸류에이션 | ${valuation} (목표) |
| 용도 | {use_of_funds} |
| 기존 투자자 | {existing_investors} |

**Contact**
```
{Founder Name}
{Email}
{Phone}
{LinkedIn}
```

**다음 단계**
- 제품 데모
- 자료 공유
- 팔로업 미팅

---

## 4. 버전별 변형

### 티저 덱 (5장)

| # | 슬라이드 | 포커스 |
|---|----------|--------|
| 1 | Cover | 훅 |
| 2 | Problem + Solution | 핵심 |
| 3 | Market + Traction | 기회 |
| 4 | Team | 신뢰 |
| 5 | Ask | CTA |

### 이메일용 원페이저

```
One-Pager Structure:
─────────────────────────────────────
[Problem] + [Solution] - 2문장
[Traction] - 핵심 숫자 3개
[Team] - 핵심 멤버 1줄
[Ask] - 금액 + 용도
[Contact] - 연락처
```

---

## 5. 디자인 가이드

### 일반 원칙

```
✅ Do
- 한 슬라이드 한 메시지
- 큰 폰트 (24pt 이상)
- 충분한 여백
- 일관된 디자인
- 고품질 이미지

❌ Don't
- 텍스트로 가득 채우기
- 불필요한 애니메이션
- 복잡한 차트
- 저해상도 이미지
```

### 폰트 & 컬러

| 요소 | 권장 |
|------|------|
| 제목 | 32-44pt, Bold |
| 본문 | 18-24pt, Regular |
| 캡션 | 14-16pt, Light |
| 메인 컬러 | 브랜드 컬러 |
| 강조 | 브랜드 보조색 |

---

## 6. 피치 준비

### 발표 연습

| 항목 | 체크 |
|------|------|
| 시간 내 완료 (10분) | ⬜ |
| 핵심 메시지 암기 | ⬜ |
| Q&A 준비 | ⬜ |
| 데모 리허설 | ⬜ |
| 백업 슬라이드 | ⬜ |

### 예상 질문

| 질문 | 준비된 답변 |
|------|-----------|
| 경쟁사와 차이점은? | {answer} |
| 왜 지금인가? | {answer} |
| 팀이 왜 적합한가? | {answer} |
| CAC/LTV는? | {answer} |
| Exit 전략은? | {answer} |

---

## 7. 결론

### 체크리스트

```
□ 핵심 메시지가 명확한가?
□ 스토리가 논리적인가?
□ 숫자가 정확한가?
□ 디자인이 깔끔한가?
□ 10분 안에 발표 가능한가?
□ Q&A가 준비되었는가?
```

### 다음 액션

1. **PPT Agent 연계** → 실제 피치덱 제작
2. **발표 연습** → 팀 리허설
3. **피드백** → 어드바이저 리뷰

---

*다음 단계: GTM Strategy → 실행*
```

## 퀄리티 체크리스트

```
□ 핵심 메시지 (One-liner)가 명확한가?
□ Problem-Solution이 연결되는가?
□ 시장 규모가 충분한가?
□ Traction이 설득력 있는가?
□ 팀의 Founder-Market Fit이 있는가?
□ Ask가 명확한가?
```

## 다음 스킬 연결

Pitch Deck 완료 후:

1. **실제 제작** → PPT Agent 연계
2. **GTM 전략** → GTM Strategy Skill
3. **투자자 미팅** → 네트워킹

---

*좋은 피치덱은 이야기입니다. 숫자가 아니라 비전을 팔아야 합니다.*
