---
name: mkt-persona
description: |
  고객 페르소나 및 공감 지도 생성.
  타겟 고객을 구체적인 인물로 형상화합니다.
triggers:
  - "페르소나"
  - "타겟 고객"
  - "고객 프로필"
  - "공감 지도"
input:
  - context/{project}-context.md
  - research/{project}-3c-analysis.md (선택)
output:
  - personas/persona-{n}.md
---

# Persona Skill

추상적인 "타겟 고객"을 구체적인 인물로 형상화합니다.
마케팅 메시지와 채널 결정에 활용됩니다.

## 페르소나란?

```
추상적                          구체적
─────────────────────────────────────────────
"20-30대 개발자"     →     "스타트업에서 일하는
                           3년차 백엔드 개발자 민수.
                           야근이 잦고, 생산성 도구에
                           돈 쓰는 걸 아까워하지 않음"
```

## 페르소나 템플릿

### 기본 구조

```yaml
persona:
  name: ""                    # 가상 이름
  photo_description: ""       # 외모/분위기 설명

  demographics:
    age: ""
    gender: ""
    location: ""
    occupation: ""
    income: ""
    education: ""
    family: ""

  psychographics:
    personality: []           # 성격 특성
    values: []                # 가치관
    interests: []             # 관심사
    lifestyle: ""             # 라이프스타일

  professional:
    job_title: ""
    company_type: ""
    responsibilities: []
    challenges: []
    tools_used: []

  goals:
    primary: ""               # 핵심 목표
    secondary: []             # 부가 목표

  pain_points:
    primary: ""               # 핵심 문제
    secondary: []             # 부가 문제
    frustrations: []          # 좌절감

  behavior:
    information_sources: []   # 정보 습득 채널
    social_media: []          # 사용 SNS
    purchase_behavior: ""     # 구매 성향
    decision_factors: []      # 결정 요인

  quotes:                     # 이 사람이 할 법한 말
    - ""
    - ""

  objections:                 # 제품에 대한 반론
    - ""
    - ""
```

## 공감 지도 (Empathy Map)

```
┌─────────────────────────────────────────────────────────────┐
│                      THINKS & FEELS                          │
│                     (생각 & 감정)                             │
│  • 무엇이 정말 중요한가?                                      │
│  • 주요 걱정거리는?                                           │
│  • 꿈과 열망은?                                               │
├──────────────────────┬──────────────────────────────────────┤
│       SEES           │              HEARS                    │
│      (보는 것)        │             (듣는 것)                  │
│  • 환경은?           │  • 친구들이 하는 말?                    │
│  • 친구들은?         │  • 상사가 하는 말?                      │
│  • 시장에서 보는 것? │  • 인플루언서가 하는 말?                │
├──────────────────────┴──────────────────────────────────────┤
│                       SAYS & DOES                            │
│                     (말 & 행동)                               │
│  • 태도는?                                                    │
│  • 외모는?                                                    │
│  • 타인에게 어떤 행동?                                        │
├─────────────────────────────────────────────────────────────┤
│         PAIN                    │           GAIN             │
│        (고통)                    │          (이득)            │
│  • 두려움                        │  • 원하는 것               │
│  • 좌절감                        │  • 성공의 척도             │
│  • 장애물                        │  • 목표 달성 방법          │
└─────────────────────────────────────────────────────────────┘
```

## 워크플로우

```
1. 컨텍스트/리서치 문서 확인
      │
      ▼
2. 고객 세그먼트 파악 (3C 분석에서)
      │
      ▼
3. 세그먼트별 페르소나 생성 (보통 2-3개)
      │
      ├─ Primary Persona (핵심 타겟)
      ├─ Secondary Persona (부가 타겟)
      └─ Negative Persona (비타겟) - 선택
      │
      ▼
4. 공감 지도 작성
      │
      ▼
5. 페르소나 문서 저장
   → workspace/work-marketing/personas/persona-{n}.md
```

## 출력 템플릿

```markdown
# Persona: {Name}

> "{대표 인용문}"

## 기본 정보

| 항목 | 내용 |
|------|------|
| 이름 | {name} |
| 나이 | {age} |
| 직업 | {occupation} |
| 위치 | {location} |
| 소득 | {income} |

### 하루 일과
{typical_day_description}

---

## 프로필

### 성격 & 가치관
- **성격**: {personality}
- **가치관**: {values}
- **관심사**: {interests}

### 직업 정보
- **직책**: {job_title}
- **회사 유형**: {company_type}
- **주요 업무**: {responsibilities}
- **사용 도구**: {tools}

---

## Goals (목표)

### 핵심 목표
{primary_goal}

### 부가 목표
1. {secondary_goal_1}
2. {secondary_goal_2}

---

## Pain Points (문제점)

### 핵심 문제
> "{pain_point_quote}"

{pain_point_description}

### 부가 문제
1. {secondary_pain_1}
2. {secondary_pain_2}

### 좌절감
- {frustration_1}
- {frustration_2}

---

## 행동 패턴

### 정보 습득 채널
| 채널 | 사용 빈도 | 목적 |
|------|----------|------|
| {channel_1} | 매일 | {purpose} |
| {channel_2} | 주 2-3회 | {purpose} |

### 소셜 미디어
- **주 사용**: {primary_social}
- **부 사용**: {secondary_social}
- **사용 패턴**: {usage_pattern}

### 구매 행동
- **구매 성향**: {purchase_behavior}
- **결정 요인**: {decision_factors}
- **가격 민감도**: {price_sensitivity}

---

## 공감 지도

### Thinks & Feels (생각 & 감정)
- {think_1}
- {think_2}
- {feel_1}

### Sees (보는 것)
- {see_1}
- {see_2}

### Hears (듣는 것)
- {hear_1}
- {hear_2}

### Says & Does (말 & 행동)
- {say_1}
- {do_1}

### Pain (고통)
- {pain_1}
- {pain_2}

### Gain (이득)
- {gain_1}
- {gain_2}

---

## 대표 인용문

> "{quote_1}"

> "{quote_2}"

> "{quote_3}"

---

## 제품에 대한 반론 (Objections)

1. **{objection_1}**
   → 대응: {response_1}

2. **{objection_2}**
   → 대응: {response_2}

---

## 마케팅 시사점

### 이 페르소나에게 효과적인 것
- **메시지**: {effective_message}
- **채널**: {effective_channel}
- **톤**: {effective_tone}
- **CTA**: {effective_cta}

### 피해야 할 것
- {avoid_1}
- {avoid_2}

---

## 고객 여정 스냅샷

```
인지 → 고려 → 결정 → 구매 → 충성
  │      │      │      │      │
  │      │      │      │      └─ {loyalty_touchpoint}
  │      │      │      └─ {purchase_touchpoint}
  │      │      └─ {decision_touchpoint}
  │      └─ {consideration_touchpoint}
  └─ {awareness_touchpoint}
```

---

*Persona Type: {Primary/Secondary/Negative}*
*Created: {date}*
```

## 페르소나 예시

### B2B SaaS 예시

```markdown
# Persona: 개발자 민수

> "좋은 도구에는 돈 쓸 수 있어.
>  근데 세팅하는데 하루 걸리면 안 써."

## 기본 정보
- 32세, 남성
- 백엔드 개발자 (3년차)
- 스타트업 근무 (시리즈 A)
- 연봉 6,000만원

## Pain Points
1. 야근이 잦아서 생산성 도구가 절실
2. 좋은 도구 찾아도 세팅이 복잡하면 포기
3. 팀 설득하기 귀찮음

## 마케팅 시사점
- **메시지**: "5분 세팅, 바로 사용"
- **채널**: 개발자 커뮤니티, GitHub
- **톤**: 기술적이되 유머 섞기
```

## 퀄리티 vs 한계

### 강한 영역
- 프레임워크 기반 체계적 구조
- 일관된 페르소나 문서
- 마케팅 시사점 도출

### 한계
- 실제 고객 인터뷰 데이터 부재
- 타겟의 실제 언어/표현
- 깊은 심리적 인사이트

### 보완 방법
- 고객 리뷰/피드백 공유
- 기존 고객 인터뷰 내용 제공
- 커뮤니티 반응 공유

## 다음 스킬 연결

- **Positioning Skill**: 페르소나 기반 포지셔닝
- **Customer Journey Skill**: 페르소나별 여정 맵
- **Copywriting Skill**: 페르소나 언어로 카피 작성

---

*좋은 페르소나는 마케팅 결정을 쉽게 만듭니다.*
*"민수라면 이걸 클릭할까?"라고 물을 수 있어야 합니다.*
