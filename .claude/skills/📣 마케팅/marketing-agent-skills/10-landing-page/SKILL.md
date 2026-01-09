---
name: mkt-landing-page
description: |
  랜딩페이지 기획 및 CRO 체크리스트.
  전환 최적화된 랜딩페이지 구조와 카피를 설계합니다.
triggers:
  - "랜딩페이지"
  - "LP 기획"
  - "전환 페이지"
  - "CRO"
input:
  - context/{project}-context.md
  - copy/*.md
  - personas/*.md
output:
  - landing-pages/{page-name}/structure.md
  - landing-pages/{page-name}/copy.md
  - landing-pages/{page-name}/cro-checklist.md
---

# Landing Page Skill

전환 최적화된 랜딩페이지를 설계합니다.

## 랜딩페이지 유형

```yaml
landing_page_types:
  lead_gen:                   # 리드 수집
    goal: "이메일/연락처 수집"
    form: true
    cta: "다운로드", "신청하기"

  click_through:              # 클릭 유도
    goal: "다음 페이지로 유도"
    form: false
    cta: "자세히 보기", "시작하기"

  sales:                      # 직접 판매
    goal: "구매 전환"
    form: true (결제)
    cta: "구매하기", "가입하기"

  squeeze:                    # 간단 수집
    goal: "이메일만 수집"
    form: minimal
    cta: "받아보기"
```

## 랜딩페이지 구조

### 표준 섹션 순서

```
┌─────────────────────────────────────────────────────────────┐
│                         HERO                                 │
│  • 헤드라인 (가치 제안)                                       │
│  • 서브헤드라인                                               │
│  • CTA 버튼                                                  │
│  • Hero 이미지/영상                                          │
├─────────────────────────────────────────────────────────────┤
│                      SOCIAL PROOF                            │
│  • 로고 배너                                                  │
│  • 숫자 (사용자 수, 리뷰 수)                                  │
├─────────────────────────────────────────────────────────────┤
│                       PROBLEM                                │
│  • 고객의 Pain Point 설명                                    │
│  • 공감 형성                                                  │
├─────────────────────────────────────────────────────────────┤
│                       SOLUTION                               │
│  • 우리 제품이 해결책                                         │
│  • 핵심 기능 3가지                                           │
├─────────────────────────────────────────────────────────────┤
│                       BENEFITS                               │
│  • Feature → Benefit                                        │
│  • 아이콘 + 설명                                             │
├─────────────────────────────────────────────────────────────┤
│                     HOW IT WORKS                             │
│  • 3단계 프로세스                                            │
│  • 간단함 강조                                               │
├─────────────────────────────────────────────────────────────┤
│                    TESTIMONIALS                              │
│  • 고객 후기                                                  │
│  • 사진 + 이름 + 직책                                        │
├─────────────────────────────────────────────────────────────┤
│                       PRICING                                │
│  • 가격 테이블 (선택)                                         │
│  • 가치 강조                                                  │
├─────────────────────────────────────────────────────────────┤
│                         FAQ                                  │
│  • 자주 묻는 질문 5-7개                                      │
│  • 반론 처리                                                  │
├─────────────────────────────────────────────────────────────┤
│                      FINAL CTA                               │
│  • 마지막 설득                                               │
│  • CTA 버튼                                                  │
│  • 보장/위험 제거                                            │
├─────────────────────────────────────────────────────────────┤
│                       FOOTER                                 │
│  • 링크들                                                     │
│  • 연락처                                                     │
└─────────────────────────────────────────────────────────────┘
```

## CRO 체크리스트

### Hero 섹션

```
□ 헤드라인이 3초 내 가치 전달
□ 서브헤드라인이 헤드라인 보완
□ CTA 버튼이 눈에 띔 (대비 색상)
□ CTA 문구가 행동 지향적
□ Above the fold에 핵심 요소 배치
□ 배경 이미지가 메시지 방해 안 함
```

### 신뢰 요소

```
□ 로고 배너 (고객사/미디어)
□ 구체적인 숫자 ("500개 팀", "50,000명")
□ 실제 고객 후기 (사진 + 이름)
□ 보안 배지 (SSL, 결제 보안)
□ 보장 문구 (환불 보장 등)
```

### 폼 최적화

```
□ 필드 수 최소화 (3개 이하 권장)
□ 필수/선택 명확히 표시
□ 에러 메시지 친절하게
□ 자동 완성 지원
□ 모바일 키보드 최적화
```

### 기술 요소

```
□ 로딩 속도 3초 이하
□ 모바일 반응형
□ 트래킹 코드 설치 (GA, FB Pixel)
□ A/B 테스트 도구 연동
□ 폼 제출 후 Thank You 페이지
```

### 카피

```
□ 혜택 중심 (기능 X)
□ 구체적인 숫자 사용
□ 스캔하기 쉬운 구조 (불릿, 소제목)
□ 한 가지 메시지에 집중
□ 반론/objection 처리
```

## 워크플로우

```
1. 목적 & 타입 결정
      │
      ▼
2. 섹션 구조 설계
      │
      ▼
3. 섹션별 카피 작성
      │
      ▼
4. CRO 체크리스트 적용
      │
      ▼
5. A/B 테스트 계획
      │
      ▼
6. 문서 저장
   → workspace/work-marketing/landing-pages/{page-name}/
```

## 출력 템플릿

### structure.md

```markdown
# {Page Name} Landing Page Structure

## Page Info

| 항목 | 내용 |
|------|------|
| 유형 | {type} |
| 목표 | {goal} |
| 타겟 | {target} |
| 주요 CTA | {primary_cta} |

---

## Section Structure

### 1. Hero

| 요소 | 내용 |
|------|------|
| 헤드라인 | {headline} |
| 서브헤드라인 | {subheadline} |
| CTA 버튼 | {cta_text} |
| CTA 링크 | {cta_link} |
| 비주얼 | {visual_description} |

**레이아웃**: {layout_description}

---

### 2. Social Proof Bar

| 요소 | 내용 |
|------|------|
| 로고 수 | {logo_count} |
| 수치 | {stats} |

**배치**: {placement}

---

### 3. Problem Section

| 요소 | 내용 |
|------|------|
| 소제목 | {section_title} |
| Pain Point 1 | {pain_1} |
| Pain Point 2 | {pain_2} |
| Pain Point 3 | {pain_3} |

---

### 4. Solution Section

| 요소 | 내용 |
|------|------|
| 소제목 | {section_title} |
| 솔루션 설명 | {solution_description} |
| 핵심 기능 1 | {feature_1} |
| 핵심 기능 2 | {feature_2} |
| 핵심 기능 3 | {feature_3} |

---

### 5. Benefits Section

| Feature | Benefit | 아이콘 |
|---------|---------|--------|
| {feature_1} | {benefit_1} | {icon} |
| {feature_2} | {benefit_2} | {icon} |
| {feature_3} | {benefit_3} | {icon} |

---

### 6. How It Works

| 단계 | 제목 | 설명 |
|------|------|------|
| 1 | {step_1_title} | {step_1_desc} |
| 2 | {step_2_title} | {step_2_desc} |
| 3 | {step_3_title} | {step_3_desc} |

---

### 7. Testimonials

#### Testimonial 1

| 항목 | 내용 |
|------|------|
| 인용문 | "{quote}" |
| 이름 | {name} |
| 직책 | {title} |
| 회사 | {company} |

#### Testimonial 2
...

---

### 8. Pricing (선택)

| 플랜 | 가격 | 특징 | CTA |
|------|------|------|-----|
| {plan_1} | {price} | {features} | {cta} |
| {plan_2} | {price} | {features} | {cta} |

---

### 9. FAQ

| 질문 | 답변 |
|------|------|
| {q1} | {a1} |
| {q2} | {a2} |
| {q3} | {a3} |
| {q4} | {a4} |
| {q5} | {a5} |

---

### 10. Final CTA

| 요소 | 내용 |
|------|------|
| 헤드라인 | {final_headline} |
| 서브텍스트 | {final_subtext} |
| CTA 버튼 | {cta_text} |
| 보장 문구 | {guarantee} |

---

## Wireframe

```
┌────────────────────────────────┐
│           HERO                 │
│  [Headline]                    │
│  [Subheadline]                 │
│  [CTA Button]                  │
├────────────────────────────────┤
│  Logo | Logo | Logo | Logo     │
├────────────────────────────────┤
│         PROBLEM                │
│  [Pain points]                 │
├────────────────────────────────┤
│         SOLUTION               │
│  [Features grid]               │
├────────────────────────────────┤
│       HOW IT WORKS             │
│  [1] → [2] → [3]               │
├────────────────────────────────┤
│      TESTIMONIALS              │
│  [Quote cards]                 │
├────────────────────────────────┤
│          FAQ                   │
│  [Accordion]                   │
├────────────────────────────────┤
│        FINAL CTA               │
│  [CTA Button]                  │
└────────────────────────────────┘
```
```

### copy.md

```markdown
# {Page Name} Landing Page Copy

## Hero Section

### Headline
> {headline}

### Subheadline
> {subheadline}

### CTA Button
> {cta_text}

---

## Social Proof

### Stats
- {stat_1}
- {stat_2}
- {stat_3}

---

## Problem Section

### Section Title
> {title}

### Body Copy
{problem_description}

### Pain Points
1. **{pain_1_title}**: {pain_1_desc}
2. **{pain_2_title}**: {pain_2_desc}
3. **{pain_3_title}**: {pain_3_desc}

---

## Solution Section

### Section Title
> {title}

### Body Copy
{solution_description}

### Feature Highlights

#### {feature_1_title}
{feature_1_desc}

#### {feature_2_title}
{feature_2_desc}

#### {feature_3_title}
{feature_3_desc}

---

## Benefits Section

| Icon | Title | Description |
|------|-------|-------------|
| {icon} | {title} | {desc} |
| {icon} | {title} | {desc} |
| {icon} | {title} | {desc} |

---

## How It Works

### Section Title
> {title}

### Steps

**Step 1: {step_1_title}**
{step_1_desc}

**Step 2: {step_2_title}**
{step_2_desc}

**Step 3: {step_3_title}**
{step_3_desc}

---

## Testimonials

### Testimonial 1

> "{quote}"
>
> — {name}, {title} at {company}

### Testimonial 2
...

---

## FAQ

### {question_1}
{answer_1}

### {question_2}
{answer_2}

### {question_3}
{answer_3}

---

## Final CTA Section

### Headline
> {headline}

### Supporting Text
{supporting_text}

### CTA Button
> {cta_text}

### Guarantee/Risk Reversal
{guarantee_text}
```

### cro-checklist.md

```markdown
# {Page Name} CRO Checklist

## Pre-Launch

### Hero Section
- [ ] 헤드라인 3초 테스트 통과
- [ ] CTA 버튼 대비 색상
- [ ] Above the fold 완성
- [ ] 모바일 Hero 최적화

### Trust Elements
- [ ] 로고 배너 설치
- [ ] 구체적 숫자 표시
- [ ] 실제 고객 후기 (사진 포함)
- [ ] 보안/보장 배지

### Forms
- [ ] 필드 수 최소화 ({n}개)
- [ ] 버튼 텍스트 명확
- [ ] 에러 처리 테스트
- [ ] Thank You 페이지 설정

### Technical
- [ ] 페이지 로딩 3초 이하
- [ ] 모바일 반응형 테스트
- [ ] GA 설치 및 Goal 설정
- [ ] FB Pixel 설치
- [ ] Hotjar/FullStory 설치

### Copy
- [ ] 타겟 언어 사용
- [ ] 혜택 중심 표현
- [ ] CTA 명확
- [ ] Objection 처리

---

## Post-Launch Monitoring

### Week 1
- [ ] 전환율 확인
- [ ] 히트맵 분석
- [ ] 이탈 지점 파악
- [ ] 첫 A/B 테스트 시작

### Week 2-4
- [ ] A/B 테스트 결과 분석
- [ ] 우승 버전 적용
- [ ] 다음 테스트 계획

---

## A/B Test Queue

| 우선순위 | 요소 | 가설 | 상태 |
|---------|------|------|------|
| 1 | {element} | {hypothesis} | ⬜ |
| 2 | {element} | {hypothesis} | ⬜ |
| 3 | {element} | {hypothesis} | ⬜ |
```

## 다음 스킬 연결

- **A/B Testing Skill**: LP 테스트 설계
- **Analytics KPI Skill**: 전환 추적 설정
- **Ads Creative Skill**: LP로 연결되는 광고

---

*좋은 랜딩페이지는 "한 가지 목표, 한 가지 CTA"에 집중합니다.*
*선택지가 많으면 전환율이 떨어집니다.*
