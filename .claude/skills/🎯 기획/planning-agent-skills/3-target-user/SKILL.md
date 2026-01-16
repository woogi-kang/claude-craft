---
name: plan-target-user
description: |
  타겟 사용자를 구체적으로 정의하는 스킬.
  페르소나, JTBD, 공감 지도를 작성합니다.
triggers:
  - "타겟 사용자"
  - "페르소나"
  - "고객 정의"
  - "사용자 분석"
input:
  - idea-intake.md 결과
  - value-proposition.md 결과
output:
  - 01-discovery/target-user.md
---

# Target User Skill

서비스의 핵심 타겟 사용자를 구체적으로 정의합니다.
추상적인 "타겟"이 아닌, 이름 붙일 수 있는 구체적인 인물상을 만듭니다.

## 핵심 프레임워크

### 1. Persona Framework

```
┌─────────────────────────────────────────────────────────────────┐
│                         PERSONA                                  │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│   이름, 나이, 직업                    사진/일러스트               │
│   ┌─────────────────────────┐        ┌─────────────┐           │
│   │ "김개발" (32)           │        │    👤       │           │
│   │ 스타트업 백엔드 개발자   │        │             │           │
│   └─────────────────────────┘        └─────────────┘           │
│                                                                  │
│   ─────────────────────────────────────────────────────────     │
│                                                                  │
│   목표 (Goals)                   고통 (Pains)                   │
│   • 빠른 개발                    • 반복 작업                     │
│   • 코드 품질                    • 문서화 시간                   │
│   • 성장                         • 야근                         │
│                                                                  │
│   ─────────────────────────────────────────────────────────     │
│                                                                  │
│   행동 (Behaviors)               영향력 (Influence)             │
│   • Stack Overflow              • 테크 블로그                   │
│   • GitHub Trending             • 동료 개발자                   │
│   • 유튜브 튜토리얼             • 밋업/컨퍼런스                  │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### 2. JTBD (Jobs-to-be-Done) Framework

```
When I [상황/맥락]
I want to [동기/Job]
So that I can [기대 결과]
```

### 3. 공감 지도 (Empathy Map)

```
┌─────────────────────────────────────────────────────────────────┐
│                     THINK & FEEL                                 │
│              실제로 무엇을 생각하고 느끼는가?                      │
│                                                                  │
│    걱정, 열망, 기대, 두려움, 희망                                 │
├────────────────────────┬────────────────────────────────────────┤
│         HEAR           │              SEE                        │
│                        │                                         │
│  주변에서 뭘 듣는가?    │         환경에서 뭘 보는가?              │
│                        │                                         │
│  친구, 동료, 미디어     │  시장, 경쟁, 트렌드                     │
├────────────────────────┼────────────────────────────────────────┤
│         SAY            │              DO                         │
│                        │                                         │
│  뭐라고 말하는가?       │         실제로 뭘 하는가?               │
│                        │                                         │
│  태도, 표현             │  행동, 습관                             │
├────────────────────────┴────────────────────────────────────────┤
│         PAIN                          GAIN                       │
│                                                                  │
│    두려움, 장애물, 리스크      원하는 것, 성공의 척도, 장애물 극복 │
└─────────────────────────────────────────────────────────────────┘
```

## 수집 항목

### 1. 인구통계학적 정보 (Demographics)

```yaml
demographics:
  age_range: ""               # 연령대
  gender: ""                  # 성별 (또는 무관)
  location: ""                # 지역
  income_level: ""            # 소득 수준
  education: ""               # 학력
  occupation: ""              # 직업/직군
  company_size: ""            # 회사 규모 (B2B)
  industry: ""                # 산업군 (B2B)
```

### 2. 심리학적 정보 (Psychographics)

```yaml
psychographics:
  values: []                  # 가치관
  interests: []               # 관심사
  lifestyle: ""               # 라이프스타일
  personality: ""             # 성향 (얼리어답터, 보수적 등)
  tech_savviness: ""          # 기술 친화도
```

### 3. 행동 정보 (Behaviors)

```yaml
behaviors:
  information_sources: []     # 정보 획득 채널
  purchase_triggers: []       # 구매/전환 트리거
  decision_factors: []        # 의사결정 요소
  usage_patterns: ""          # 사용 패턴
  brand_loyalty: ""           # 브랜드 충성도
```

### 4. JTBD 정보

```yaml
jobs:
  primary:
    situation: ""             # 상황
    motivation: ""            # 동기
    expected_outcome: ""      # 기대 결과
  secondary: []               # 부차적 Jobs

pains:
  functional: []              # 기능적 고통
  emotional: []               # 감정적 고통
  social: []                  # 사회적 고통

gains:
  required: []                # 필수 기대
  expected: []                # 당연한 기대
  desired: []                 # 바라는 것
```

## 워크플로우

```
1. 기존 정보 확인
      │
      ├─ idea-intake.md
      └─ value-proposition.md
      │
      ▼
2. 타겟 세그먼트 식별
      │
      ├─ Primary Target
      └─ Secondary Target
      │
      ▼
3. 페르소나 작성 (2-3개)
      │
      ▼
4. JTBD 정의
      │
      ▼
5. 공감 지도 작성
      │
      ▼
6. 타겟 우선순위 결정
      │
      ▼
7. 최종 문서 저장
   → workspace/work-plan/{project}/01-discovery/target-user.md
```

## 출력 템플릿

```markdown
# {Project Name} - 타겟 사용자 정의

## Target Overview

### Primary Target
> **{primary_target_one_liner}**

### Secondary Target
> **{secondary_target_one_liner}**

### Target Priority Matrix

| 세그먼트 | 시장 규모 | 접근성 | 가치 적합 | 우선순위 |
|----------|----------|--------|----------|----------|
| {segment_1} | 🟢 Large | 🟢 Easy | 🟢 High | ⭐⭐⭐⭐⭐ |
| {segment_2} | 🟡 Medium | 🟢 Easy | 🟡 Medium | ⭐⭐⭐⭐ |
| {segment_3} | 🟢 Large | 🔴 Hard | 🟡 Medium | ⭐⭐⭐ |

---

## Persona 1: {Persona Name}

### 기본 정보

| 항목 | 내용 |
|------|------|
| 이름 | {name} |
| 나이 | {age} |
| 직업 | {occupation} |
| 위치 | {location} |
| 회사 규모 | {company_size} |

### 프로필

```
"{persona_quote}"
```

**배경**
{background_story}

**일상**
{daily_routine}

### 목표 & 동기

| 목표 | 동기 | 중요도 |
|------|------|--------|
| {goal_1} | {motivation_1} | ⭐⭐⭐⭐⭐ |
| {goal_2} | {motivation_2} | ⭐⭐⭐⭐ |
| {goal_3} | {motivation_3} | ⭐⭐⭐ |

### 고통점 (Pains)

| Pain | 유형 | 빈도 | 심각도 |
|------|------|------|--------|
| {pain_1} | 기능적 | 매일 | 🔴 |
| {pain_2} | 감정적 | 주 2-3회 | 🟡 |
| {pain_3} | 사회적 | 가끔 | 🟢 |

### 정보 채널 & 행동

**정보 획득**
- {channel_1}
- {channel_2}
- {channel_3}

**의사결정 요소**
1. {factor_1}
2. {factor_2}
3. {factor_3}

**구매 트리거**
- {trigger_1}
- {trigger_2}

### 기술 친화도

| 영역 | 수준 | 사용 도구 |
|------|------|----------|
| 디바이스 | {level} | {tools} |
| 소프트웨어 | {level} | {tools} |
| 신기술 수용 | {level} | {examples} |

---

## Persona 2: {Persona Name}

(동일 구조 반복)

---

## Jobs-to-be-Done

### Primary Job

```
When I {situation}
I want to {motivation}
So that I can {expected_outcome}
```

### Job Map

| Job | Importance | Satisfaction | Opportunity |
|-----|------------|--------------|-------------|
| {job_1} | 🔴 High | 🔴 Low | ⭐⭐⭐⭐⭐ |
| {job_2} | 🟡 Medium | 🟡 Medium | ⭐⭐⭐ |
| {job_3} | 🔴 High | 🟢 High | ⭐⭐ |

### Job Stories

**Story 1**
> When I {context}, I want to {action} so that {outcome}.

**Story 2**
> When I {context}, I want to {action} so that {outcome}.

---

## Empathy Map

### Think & Feel
- {think_feel_1}
- {think_feel_2}
- {think_feel_3}

### Hear
- {hear_1}
- {hear_2}

### See
- {see_1}
- {see_2}

### Say & Do
- {say_do_1}
- {say_do_2}

### Pain
- {empathy_pain_1}
- {empathy_pain_2}

### Gain
- {empathy_gain_1}
- {empathy_gain_2}

---

## Customer Journey (간략)

| 단계 | 행동 | 감정 | 터치포인트 | 기회 |
|------|------|------|-----------|------|
| 인지 | {action} | {emotion} | {touchpoint} | {opportunity} |
| 고려 | {action} | {emotion} | {touchpoint} | {opportunity} |
| 결정 | {action} | {emotion} | {touchpoint} | {opportunity} |
| 사용 | {action} | {emotion} | {touchpoint} | {opportunity} |

---

## 타겟 사용자 요약

### 핵심 인사이트

1. **가장 큰 Pain**: {biggest_pain}
2. **가장 중요한 Job**: {most_important_job}
3. **의사결정 핵심 요소**: {key_decision_factor}
4. **최적 접근 채널**: {best_channel}

### Do's and Don'ts

| Do ✅ | Don't ❌ |
|-------|---------|
| {do_1} | {dont_1} |
| {do_2} | {dont_2} |
| {do_3} | {dont_3} |

---

*다음 단계: Market Research → Competitor Analysis*
```

## 페르소나 작성 팁

### 좋은 페르소나 특징

```
✅ 이름과 얼굴이 있음 - 실제 인물처럼 느껴짐
✅ 구체적인 상황 - 언제, 어디서, 왜
✅ 감정이 포함됨 - 좌절, 기쁨, 불안
✅ 행동 패턴 - 실제로 무엇을 하는지
✅ 인용구 - 그들의 언어로 표현
```

### 나쁜 페르소나 특징

```
❌ "20-40대 직장인" - 너무 넓음
❌ 인구통계만 있음 - 행동/심리 없음
❌ 데이터 없이 추측 - 근거 없음
❌ 팀 전체가 공유 안 함 - 활용 안 됨
```

## JTBD 작성 팁

### 좋은 Job Statement

```
❌ "문서를 작성한다" (기능)
✅ "빠르게 전문적인 보고서를 만들어 상사에게 인정받고 싶다" (Job)

❌ "앱을 다운로드한다" (액션)
✅ "출퇴근 시간에 새로운 지식을 습득해 성장하고 싶다" (Job)
```

## 퀄리티 체크리스트

```
□ 타겟 세그먼트가 명확히 구분되었는가?
□ 페르소나에 이름과 구체적 상황이 있는가?
□ Primary Job이 명확히 정의되었는가?
□ Pain이 3가지 이상 식별되었는가?
□ 정보 채널이 구체적인가?
□ 의사결정 요소가 파악되었는가?
□ 공감 지도가 균형 있게 작성되었는가?
□ 핵심 인사이트가 도출되었는가?
```

## 🎯 인터랙티브 가이드

### 작성 전 확인 질문

**Q1. 타겟 사용자를 직접 만나본 적 있나요?**
- 있음 → "그들의 가장 큰 불만은 무엇이었나요?"
- 없음 → 인터뷰 계획 수립 제안

**Q2. Primary Target이 명확한가요?**
- 명확함 → 페르소나 작성 진행
- 여러 후보 → "가장 Pain이 심한 그룹은 누구인가요?"

**Q3. 이 타겟이 돈을 지불할 의향/능력이 있나요?**
- 있음 → 지불 의향 근거 확인
- 불확실 → "누가 비용을 부담하나요? (B2B: 구매자 vs 사용자)"

### 의사결정 포인트

| 시점 | 확인 내용 | 사용자 프롬프트 |
|------|----------|----------------|
| 세그먼트 선정 | 우선순위 | "왜 이 세그먼트가 1순위인가요?" |
| 페르소나 작성 | 현실성 | "실제로 아는 사람 중 이런 분이 있나요?" |
| JTBD 정의 | 구체성 | "언제, 어디서 이 Job이 발생하나요?" |
| 최종 확인 | 공감 | "이 사람의 하루를 상상할 수 있나요?" |

---

## 다음 스킬 연결

Target User 정의 완료 후:

1. **시장 규모 검증** → Market Research Skill
2. **경쟁사 분석** → Competitor Analysis Skill
3. **사용자 리서치 설계** → User Research Skill

---

*명확한 타겟 정의 없이는 좋은 서비스를 만들 수 없습니다.*
