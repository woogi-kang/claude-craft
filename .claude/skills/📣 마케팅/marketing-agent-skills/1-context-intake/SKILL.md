---
name: mkt-context-intake
description: |
  마케팅 퀄리티 향상의 핵심 스킬.
  브랜드/제품/타겟 정보를 체계적으로 수집하여 모든 후속 스킬의 품질을 높입니다.
triggers:
  - "컨텍스트 수집"
  - "브랜드 정보"
  - "제품 정보 정리"
  - "마케팅 시작"
input:
  - 제품/서비스 설명
  - 목표 (선택)
  - 기존 자료 (선택)
output:
  - context/{project}-context.md
---

# Context Intake Skill

마케팅 결과물 퀄리티를 결정하는 가장 중요한 스킬입니다.
충분한 컨텍스트 수집 = 높은 퀄리티 산출물

## 왜 중요한가?

```
컨텍스트 없이 시작
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"마케팅해줘" → Generic한 결과물

컨텍스트 충분히 수집
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Context Intake → 브랜드에 맞는 결과물
```

## 수집 항목

### 1. 필수 정보 (Must Have)

```yaml
product:
  name: ""                    # 제품/서비스 이름
  one_liner: ""               # 한 줄 설명
  category: ""                # 카테고리 (SaaS, 이커머스, B2B 등)
  price: ""                   # 가격대
  key_features:               # 핵심 기능/특징 3가지
    - ""
    - ""
    - ""

goal:
  primary: ""                 # 주요 목표 (가입, 매출, 인지도)
  metric: ""                  # 목표 수치 (100명, 1000만원)
  timeline: ""                # 기간 (1개월, 분기)
```

### 2. 권장 정보 (Should Have)

```yaml
target:
  description: ""             # 타겟 고객 설명
  demographics: ""            # 연령, 직업, 지역
  pain_points:                # 해결하려는 문제
    - ""
    - ""
  current_solutions: ""       # 현재 사용 중인 대안

competition:
  direct:                     # 직접 경쟁사
    - name: ""
      positioning: ""
  indirect:                   # 간접 경쟁사
    - ""

differentiation: ""           # 경쟁사 대비 차별점
```

### 3. 선택 정보 (Nice to Have)

```yaml
brand:
  tone:                       # 톤앤매너
    - ""                      # 예: "친근한", "전문적인", "유머러스한"
  voice_examples:             # 기존 카피 예시
    - ""
  words_to_use:               # 사용할 단어
    - ""
  words_to_avoid:             # 피할 단어
    - ""

existing_assets:
  website: ""                 # 웹사이트 URL
  social: []                  # 소셜 채널
  previous_campaigns: []      # 이전 캠페인 자료

constraints:
  budget: ""                  # 예산 범위
  legal: []                   # 법적 제약 (의료, 금융 등)
  platform_restrictions: []   # 플랫폼 제한
```

## 인터뷰 질문 템플릿

### Quick Start (5분)

```
1. 무엇을 파는 건가요? (제품/서비스)
2. 누구에게 파는 건가요? (타겟)
3. 왜 당신 제품을 사야 하나요? (차별점)
4. 이번 마케팅의 목표는 뭔가요? (목표)
5. 경쟁사는 누구인가요? (경쟁)
```

### Deep Dive (15분)

```
제품/서비스
─────────────────────────────────
1. 제품을 한 문장으로 설명해주세요.
2. 핵심 기능 3가지는 무엇인가요?
3. 가격은 얼마인가요? 경쟁사 대비 어떤가요?
4. 고객이 가장 좋아하는 점은 무엇인가요?
5. 고객이 가장 불만인 점은 무엇인가요?

타겟 고객
─────────────────────────────────
6. 이상적인 고객은 누구인가요?
7. 그들은 어떤 문제를 겪고 있나요?
8. 현재 그 문제를 어떻게 해결하고 있나요?
9. 구매 결정에 영향을 주는 요소는?
10. 어디서 정보를 얻나요? (채널)

브랜드
─────────────────────────────────
11. 브랜드 톤을 3단어로 표현하면?
12. 좋아하는 브랜드/마케팅 예시가 있나요?
13. 절대 하고 싶지 않은 마케팅 스타일은?

목표
─────────────────────────────────
14. 이번 마케팅의 구체적 목표는?
15. 예산 범위가 있나요?
16. 언제까지 결과를 보고 싶나요?
```

## 워크플로우

```
1. 사용자 요청 수신
      │
      ▼
2. 필수 정보 확인
      │
      ├─ 부족 → 인터뷰 질문
      │
      ▼
3. 권장 정보 수집 (가능한 만큼)
      │
      ▼
4. 컨텍스트 문서 생성
      │
      ▼
5. 사용자 확인 & 보완
      │
      ▼
6. 최종 컨텍스트 저장
   → workspace/work-marketing/context/{project}-context.md
```

## 출력 템플릿

```markdown
# {Project Name} Marketing Context

## 1. 제품/서비스 개요

| 항목 | 내용 |
|------|------|
| 이름 | {name} |
| 한 줄 설명 | {one_liner} |
| 카테고리 | {category} |
| 가격 | {price} |

### 핵심 기능/특징
1. {feature_1}
2. {feature_2}
3. {feature_3}

## 2. 마케팅 목표

| 항목 | 내용 |
|------|------|
| 주요 목표 | {primary_goal} |
| 목표 수치 | {metric} |
| 기간 | {timeline} |

## 3. 타겟 고객

### 고객 프로필
- **인구통계**: {demographics}
- **설명**: {description}

### Pain Points
1. {pain_point_1}
2. {pain_point_2}

### 현재 대안
{current_solutions}

## 4. 경쟁 환경

### 직접 경쟁사
| 경쟁사 | 포지셔닝 |
|--------|----------|
| {competitor_1} | {positioning_1} |
| {competitor_2} | {positioning_2} |

### 우리의 차별점
{differentiation}

## 5. 브랜드 가이드

### 톤앤매너
- {tone_1}
- {tone_2}
- {tone_3}

### 사용할 단어
{words_to_use}

### 피할 단어
{words_to_avoid}

### 기존 카피 예시
> {voice_example_1}
> {voice_example_2}

## 6. 제약 조건

- **예산**: {budget}
- **법적 제약**: {legal_constraints}
- **기타**: {other_constraints}

---

*이 문서는 모든 마케팅 스킬에서 참조됩니다.*
*정보가 부족하거나 변경되면 업데이트해주세요.*
```

## 퀄리티 체크리스트

```
□ 제품/서비스 한 줄 설명 명확
□ 핵심 기능 3가지 정리
□ 마케팅 목표 수치화
□ 타겟 고객 Pain Points 파악
□ 경쟁사 최소 1개 파악
□ 차별점 명확
□ 톤앤매너 정의
```

## 정보 부족 시 대응

### 최소 정보로 시작

```yaml
minimum_viable_context:
  product: "한 줄 설명"
  goal: "목표"
  target_hint: "타겟 힌트"
```

이 정도만 있어도 시작 가능. 단, 결과물이 generic할 수 있음을 안내.

### 점진적 수집

```
1차 산출물 → 사용자 피드백 → 컨텍스트 보완 → 2차 산출물 (개선)
```

## 다음 스킬 연결

컨텍스트 수집 완료 후:

1. **전략 중심** → Market Research Skill
2. **바로 실행** → Copywriting Skill
3. **특정 채널** → Landing Page / Email / Ads Skill

---

*Context Intake는 마케팅 퀄리티의 80%를 결정합니다. 충분한 시간을 투자하세요.*
