---
name: mkt-email-sequence
description: |
  이메일 마케팅 시퀀스 및 드립 캠페인 설계.
  웰컴, 온보딩, 너처링, 리인게이지먼트 시퀀스를 작성합니다.
triggers:
  - "이메일 시퀀스"
  - "드립 캠페인"
  - "이메일 마케팅"
  - "뉴스레터"
input:
  - context/{project}-context.md
  - campaigns/{project}-journey.md
  - copy/*.md
output:
  - email-sequences/*.md
---

# Email Sequence Skill

목적별 이메일 시퀀스를 설계합니다.

## 시퀀스 유형

```yaml
sequence_types:
  welcome:                    # 웰컴 시리즈
    purpose: "신규 가입자 환영 & 관계 구축"
    emails: 3-5
    duration: "7-10일"
    trigger: "가입 완료"

  onboarding:                 # 온보딩 시리즈
    purpose: "제품 사용법 교육 & 활성화"
    emails: 5-7
    duration: "14일"
    trigger: "가입 완료"

  nurturing:                  # 너처링 시리즈
    purpose: "리드 교육 & 신뢰 구축"
    emails: 7-10
    duration: "3-4주"
    trigger: "리드 마그넷 다운로드"

  abandoned_cart:             # 장바구니 이탈
    purpose: "구매 완료 유도"
    emails: 3
    duration: "3일"
    trigger: "장바구니 이탈"

  reengagement:               # 리인게이지먼트
    purpose: "비활성 사용자 재활성화"
    emails: 3-4
    duration: "2주"
    trigger: "30일 비활성"

  upsell:                     # 업셀
    purpose: "상위 플랜 전환"
    emails: 3-5
    duration: "1-2주"
    trigger: "특정 사용량 도달"
```

## 이메일 구조

### 기본 이메일 템플릿

```yaml
email_structure:
  subject_line:
    length: "40자 이하"
    personalization: true
    curiosity_gap: true

  preview_text:
    length: "90자 이하"
    extends_subject: true

  body:
    greeting: "개인화"
    hook: "첫 문장이 핵심"
    value: "핵심 메시지"
    cta: "명확한 행동 유도"
    ps: "추가 포인트 (선택)"

  design:
    width: "600px"
    single_column: true
    mobile_first: true
```

## 시퀀스별 템플릿

### Welcome Sequence (웰컴)

```
Day 0: 환영 & 기대 설정
Day 1: 핵심 가치 소개
Day 3: 시작 가이드 / Quick Win
Day 5: 성공 스토리 / 소셜 프루프
Day 7: 다음 단계 / CTA
```

### Onboarding Sequence (온보딩)

```
Day 0: 가입 환영 & 첫 단계 안내
Day 1: 핵심 기능 #1 튜토리얼
Day 3: 핵심 기능 #2 튜토리얼
Day 5: 고급 팁 & 트릭
Day 7: 체크인 & 도움 필요?
Day 10: 마일스톤 축하 / 다음 목표
Day 14: 피드백 요청 / 업그레이드 제안
```

### Nurturing Sequence (너처링)

```
Day 0: 리드 마그넷 전달 & 소개
Day 2: 추가 가치 콘텐츠 #1
Day 5: 문제 심화 & 공감
Day 8: 솔루션 교육
Day 12: 케이스 스터디
Day 16: 반론 처리
Day 21: 제안 & CTA
```

## 워크플로우

```
1. 시퀀스 목적 정의
      │
      ▼
2. 트리거 & 타겟 정의
      │
      ▼
3. 이메일 수 & 간격 결정
      │
      ▼
4. 각 이메일 목표 설정
      │
      ▼
5. 제목줄 & 본문 작성
      │
      ▼
6. CTA & 다음 이메일 연결
      │
      ▼
7. 시퀀스 문서 저장
   → workspace/work-marketing/email-sequences/*.md
```

## 출력 템플릿

```markdown
# {Sequence Name} Email Sequence

## Sequence Overview

| 항목 | 내용 |
|------|------|
| 유형 | {type} |
| 목적 | {purpose} |
| 이메일 수 | {email_count} |
| 기간 | {duration} |
| 트리거 | {trigger} |
| 타겟 | {target} |

### Success Metrics

| 지표 | 목표 |
|------|------|
| 오픈율 | {open_rate}% |
| 클릭률 | {click_rate}% |
| 전환율 | {conversion_rate}% |

---

## Sequence Flow

```
┌─────────┐     ┌─────────┐     ┌─────────┐
│ Email 1 │ ──▶ │ Email 2 │ ──▶ │ Email 3 │ ──▶ ...
│  Day 0  │     │  Day 2  │     │  Day 5  │
└─────────┘     └─────────┘     └─────────┘
     │               │               │
     ▼               ▼               ▼
  {goal_1}       {goal_2}       {goal_3}
```

---

## Email 1: {Email Title}

### Meta

| 항목 | 내용 |
|------|------|
| 발송 시점 | Day 0 (즉시) |
| 목표 | {goal} |
| CTA | {cta} |

### Subject Line Options

1. {subject_1}
2. {subject_2}
3. {subject_3}

### Preview Text

> {preview_text}

### Body Copy

```
Hi {first_name},

{opening_hook}

{main_content}

{value_proposition}

{cta_section}

{closing}

{signature}

P.S. {ps_line}
```

### Full Email Draft

---

**Subject**: {chosen_subject}

**Preview**: {preview_text}

---

{first_name}님, 반갑습니다!

{body_paragraph_1}

{body_paragraph_2}

**{highlighted_point}**

{body_paragraph_3}

[{cta_button_text}]({cta_link})

{closing_line}

{signature_name}
{signature_title}

P.S. {ps_content}

---

### A/B Test Ideas

| 요소 | Version A | Version B |
|------|-----------|-----------|
| Subject | {a} | {b} |
| CTA | {a} | {b} |

---

## Email 2: {Email Title}

### Meta

| 항목 | 내용 |
|------|------|
| 발송 시점 | Day {n} |
| 목표 | {goal} |
| CTA | {cta} |

### Subject Line Options

1. {subject_1}
2. {subject_2}
3. {subject_3}

### Preview Text

> {preview_text}

### Full Email Draft

---

**Subject**: {chosen_subject}

**Preview**: {preview_text}

---

{body_content}

---

## Email 3: {Email Title}

(동일 형식 반복)

---

## Email 4: {Email Title}

---

## Email 5: {Email Title}

---

## Sequence Logic

### Branching Rules

```
Email 1 발송
     │
     ├─ 오픈 O ──▶ Email 2 (Day 2)
     │
     └─ 오픈 X ──▶ Email 1-B 재발송 (Day 1)
                        │
                        └─▶ Email 2 (Day 3)
```

### Exit Conditions

- [ ] 목표 액션 완료 (전환)
- [ ] 수신 거부
- [ ] 하드 바운스
- [ ] {custom_condition}

### Segment Rules

| 세그먼트 | 조건 | 다음 액션 |
|---------|------|----------|
| Engaged | 오픈 3회+ | 빠른 진행 |
| Cold | 오픈 0회 | 재참여 시도 |

---

## Technical Setup

### Required Tags/Fields

| 필드 | 용도 |
|------|------|
| {first_name} | 개인화 |
| {company} | 개인화 |
| {signup_date} | 타이밍 |

### Automation Triggers

| 트리거 | 조건 | 액션 |
|--------|------|------|
| {trigger_1} | {condition} | {action} |
| {trigger_2} | {condition} | {action} |

### UTM Parameters

```
utm_source=email
utm_medium=sequence
utm_campaign={sequence_name}
utm_content=email_{n}
```

---

## Metrics & Optimization

### Benchmark Comparison

| 이메일 | 오픈율 | 클릭률 | 목표 |
|--------|--------|--------|------|
| Email 1 | {%} | {%} | {%} |
| Email 2 | {%} | {%} | {%} |
| Email 3 | {%} | {%} | {%} |

### Optimization Roadmap

| 우선순위 | 이메일 | 개선 영역 | 액션 |
|---------|--------|----------|------|
| 1 | Email {n} | Subject | A/B 테스트 |
| 2 | Email {n} | CTA | 문구 변경 |

---

*Created: {date}*
*Last Updated: {update_date}*
```

## 이메일 카피 팁

### 제목줄 공식

```yaml
subject_formulas:
  question: "{question}?"
  how_to: "{result}하는 방법"
  number: "{n}가지 {topic}"
  curiosity: "이것 때문에 {result}..."
  personalized: "{first_name}님, {message}"
  urgency: "[마감 임박] {offer}"
  story: "어떻게 {person}이 {result}했는지"
```

### 본문 구조

```
1. Hook (첫 문장) - 계속 읽게 만들기
2. Empathy - 공감 형성
3. Value - 핵심 가치/정보
4. Proof - 증거/예시
5. CTA - 명확한 행동 유도
```

## 다음 스킬 연결

- **Ads Creative Skill**: 이메일 가입 유도 광고
- **A/B Testing Skill**: 이메일 테스트 설계
- **Analytics KPI Skill**: 이메일 성과 측정

---

*좋은 이메일 시퀀스는 "판매"가 아니라 "관계 구축"에 집중합니다.*
*먼저 가치를 주고, 나중에 요청하세요.*
