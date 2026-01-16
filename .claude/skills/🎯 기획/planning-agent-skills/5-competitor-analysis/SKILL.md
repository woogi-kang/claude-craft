---
name: plan-competitor-analysis
description: |
  직접/간접 경쟁사를 분석하는 스킬.
  포지셔닝 맵, Feature Matrix를 작성합니다.
triggers:
  - "경쟁사 분석"
  - "경쟁 분석"
  - "포지셔닝"
  - "벤치마킹"
input:
  - 경쟁사 이름/URL
  - 서비스 카테고리
output:
  - 02-research/competitor-analysis.md
---

# Competitor Analysis Skill

직접/간접 경쟁사를 체계적으로 분석하여 차별화 전략을 도출합니다.

## 핵심 프레임워크

### 경쟁사 유형 분류

```
┌─────────────────────────────────────────────────────────────────┐
│                      경쟁 구도                                   │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│   직접 경쟁사 (Direct)                                           │
│   └─ 같은 고객, 같은 문제, 같은 솔루션 유형                        │
│   └─ 예: Notion vs Coda                                         │
│                                                                  │
│   간접 경쟁사 (Indirect)                                         │
│   └─ 같은 고객, 같은 문제, 다른 솔루션                             │
│   └─ 예: Notion vs Google Docs + Trello                         │
│                                                                  │
│   대체재 (Substitutes)                                           │
│   └─ 같은 Job, 완전히 다른 방식                                   │
│   └─ 예: Notion vs 포스트잇 + 화이트보드                          │
│                                                                  │
│   잠재적 경쟁사 (Potential)                                       │
│   └─ 인접 시장에서 진입 가능성                                    │
│   └─ 예: Microsoft, Google                                       │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### Positioning Map (2x2 Matrix)

```
                       High Price
                           │
                           │
          Premium          │        Enterprise
          ┌────────────────┼────────────────┐
          │                │                │
          │     ★ 우리     │      ○ A사     │
Low ──────│────────────────┼────────────────│────── High
Feature   │                │                │     Feature
          │     ○ B사      │      ○ C사     │
          │                │                │
          └────────────────┼────────────────┘
          Budget           │        Value
                           │
                       Low Price
```

## 수집/분석 항목

### 1. 경쟁사 기본 정보

```yaml
competitor:
  name: ""
  type: ""                    # direct/indirect/substitute
  website: ""
  founded: ""
  funding: ""                 # 투자 유치 금액
  employees: ""               # 직원 수
  headquarters: ""            # 본사 위치
```

### 2. 제품/서비스 분석

```yaml
product:
  description: ""             # 서비스 설명
  target_customer: ""         # 타겟 고객
  main_features: []           # 주요 기능
  pricing:
    model: ""                 # 가격 모델 (구독, 일회성 등)
    plans: []                 # 가격 플랜
    free_tier: false          # 무료 플랜 여부
  technology: []              # 사용 기술
```

### 3. 시장 포지션

```yaml
position:
  market_share: ""            # 시장 점유율 (추정)
  positioning: ""             # 포지셔닝 메시지
  target_segment: ""          # 타겟 세그먼트
  unique_value: ""            # 고유 가치
```

### 4. 강점/약점 분석

```yaml
strengths:
  - area: ""
    detail: ""
    impact: ""                # high/medium/low

weaknesses:
  - area: ""
    detail: ""
    opportunity: ""           # 우리의 기회
```

### 5. 마케팅/영업 전략

```yaml
go_to_market:
  channels: []                # 마케팅 채널
  messaging: ""               # 핵심 메시지
  content_strategy: ""        # 콘텐츠 전략
  sales_model: ""             # 영업 모델 (셀프서브, 세일즈 등)
```

## 워크플로우

```
1. 경쟁사 식별
      │
      ├─ 직접 경쟁사 3-5개
      ├─ 간접 경쟁사 2-3개
      └─ 대체재 1-2개
      │
      ▼
2. 기본 정보 수집
      │
      ▼
3. Feature Matrix 작성
      │
      ▼
4. 가격 비교 분석
      │
      ▼
5. 포지셔닝 맵 작성
      │
      ▼
6. SWOT 분석
      │
      ▼
7. 차별화 전략 도출
      │
      ▼
8. 최종 문서 저장
   → workspace/work-plan/{project}/02-research/competitor-analysis.md
```

## 출력 템플릿

```markdown
# {Project Name} - 경쟁사 분석

## Executive Summary

### 경쟁 구도 요약

| 유형 | 경쟁사 | 위협 수준 |
|------|--------|----------|
| 직접 | {competitor_1}, {competitor_2} | 🔴 High |
| 간접 | {competitor_3}, {competitor_4} | 🟡 Medium |
| 대체재 | {substitute} | 🟢 Low |

### 핵심 인사이트
> {key_insight}

### 차별화 기회
> {differentiation_opportunity}

---

## 1. 경쟁사 Overview

### 1.1 {Competitor 1 Name}

| 항목 | 내용 |
|------|------|
| 유형 | 직접 경쟁 |
| 설립 | {founded} |
| 투자 | {funding} |
| 규모 | {employees}명 |
| 웹사이트 | {website} |

**서비스 설명**
{description}

**타겟 고객**
{target_customer}

**핵심 가치 제안**
> "{value_proposition}"

**강점**
- {strength_1}
- {strength_2}

**약점**
- {weakness_1}
- {weakness_2}

---

### 1.2 {Competitor 2 Name}

(동일 구조 반복)

---

## 2. Feature Matrix

### 핵심 기능 비교

| 기능 | 우리 | {Comp1} | {Comp2} | {Comp3} |
|------|------|---------|---------|---------|
| {feature_1} | ✅ | ✅ | ❌ | ✅ |
| {feature_2} | ✅ | ✅ | ✅ | ❌ |
| {feature_3} | ✅ | ❌ | ✅ | ✅ |
| {feature_4} | ✅ | ✅ | ✅ | ✅ |
| {feature_5} | 🔜 | ✅ | ❌ | ❌ |

**범례**: ✅ 있음 | ❌ 없음 | 🔜 예정 | ⭐ 강점

### 차별화 기능

우리만 있는 기능:
1. **{unique_feature_1}**: {description}
2. **{unique_feature_2}**: {description}

경쟁사에만 있는 기능:
1. **{missing_feature_1}**: {who_has_it} - {priority}
2. **{missing_feature_2}**: {who_has_it} - {priority}

---

## 3. 가격 비교

### 가격 모델 비교

| 서비스 | 무료 | 기본 | 프로 | 엔터프라이즈 |
|--------|------|------|------|-------------|
| 우리 (예정) | {our_free} | {our_basic} | {our_pro} | {our_ent} |
| {Comp1} | {c1_free} | {c1_basic} | {c1_pro} | {c1_ent} |
| {Comp2} | {c2_free} | {c2_basic} | {c2_pro} | {c2_ent} |

### 가격 포지셔닝

```
Premium (고가)
│
├── {Competitor_A}: ${price}/월
│
├── ★ 우리 (목표): ${price}/월
│
├── {Competitor_B}: ${price}/월
│
Budget (저가)
└── {Competitor_C}: ${price}/월
```

### 가격 전략 권장

{pricing_recommendation}

---

## 4. Positioning Map

### 기능 vs 가격

```
                       High Price
                           │
                           │
          ┌────────────────┼────────────────┐
          │                │                │
          │    {Comp_A}    │   {Comp_B}     │
Simple ───│────────────────┼────────────────│─── Complex
Feature   │                │                │   Feature
          │    ★ 우리      │   {Comp_C}     │
          │   (목표)       │                │
          └────────────────┼────────────────┘
                           │
                       Low Price
```

### 우리의 포지션

**현재 빈틈 (White Space)**
{white_space_description}

**목표 포지션**
{target_position}

---

## 5. SWOT 분석 (경쟁 관점)

### 경쟁 우위 SWOT

| 강점 (S) | 약점 (W) |
|----------|----------|
| {strength_1} | {weakness_1} |
| {strength_2} | {weakness_2} |
| {strength_3} | {weakness_3} |

| 기회 (O) | 위협 (T) |
|----------|----------|
| {opportunity_1} | {threat_1} |
| {opportunity_2} | {threat_2} |
| {opportunity_3} | {threat_3} |

### 전략 도출

**SO 전략** (강점으로 기회 활용)
- {so_strategy}

**WO 전략** (약점 보완하여 기회 활용)
- {wo_strategy}

**ST 전략** (강점으로 위협 대응)
- {st_strategy}

**WT 전략** (약점 보완하고 위협 회피)
- {wt_strategy}

---

## 6. 경쟁사별 대응 전략

### {Competitor 1}

| 그들의 강점 | 우리의 대응 |
|------------|------------|
| {their_strength_1} | {our_response_1} |
| {their_strength_2} | {our_response_2} |

**핵심 메시지 (vs {Comp1})**
> "{comparison_message}"

### {Competitor 2}

(동일 구조)

---

## 7. 차별화 전략

### 차별화 축

| 축 | 경쟁사 | 우리 | 차별화 |
|---|--------|------|--------|
| 가격 | {comp_price} | {our_price} | {diff} |
| 타겟 | {comp_target} | {our_target} | {diff} |
| 기능 | {comp_feature} | {our_feature} | {diff} |
| 경험 | {comp_ux} | {our_ux} | {diff} |
| 지원 | {comp_support} | {our_support} | {diff} |

### 핵심 차별화 메시지

**Tagline**
> "{differentiation_tagline}"

**주요 차별점 3가지**

1. **{diff_point_1}**
   - 경쟁사: {competitor_approach}
   - 우리: {our_approach}
   - 가치: {value_to_customer}

2. **{diff_point_2}**
   - 경쟁사: {competitor_approach}
   - 우리: {our_approach}
   - 가치: {value_to_customer}

3. **{diff_point_3}**
   - 경쟁사: {competitor_approach}
   - 우리: {our_approach}
   - 가치: {value_to_customer}

---

## 8. 경쟁 모니터링 계획

### 모니터링 항목

| 항목 | 빈도 | 담당 |
|------|------|------|
| 가격 변경 | 월 1회 | - |
| 신규 기능 | 월 2회 | - |
| 마케팅 캠페인 | 주 1회 | - |
| 고객 리뷰 | 주 1회 | - |
| 채용 공고 | 월 1회 | - |

### 모니터링 도구

- Google Alerts: {competitor_names}
- ProductHunt: 신규 런칭
- G2/Capterra: 리뷰 추적
- LinkedIn: 채용/조직 동향

---

## 9. 결론

### 경쟁 환경 평가

| 요소 | 평가 | 근거 |
|------|------|------|
| 경쟁 강도 | {intensity_level} | {reason} |
| 진입 장벽 | {barrier_level} | {reason} |
| 차별화 기회 | {opportunity_level} | {reason} |
| 종합 | {overall} | {summary} |

### 핵심 Action Items

1. **즉시**: {action_immediate}
2. **단기 (1-3개월)**: {action_short}
3. **중기 (3-6개월)**: {action_medium}

---

*다음 단계: User Research → Lean Canvas*
```

## 분석 팁

### 경쟁사 정보 수집처

| 정보 | 소스 |
|------|------|
| 기본 정보 | Crunchbase, LinkedIn |
| 가격 | 공식 웹사이트 |
| 기능 | 제품 페이지, 도움말 |
| 리뷰 | G2, Capterra, App Store |
| 트래픽 | SimilarWeb, Alexa |
| 기술 스택 | BuiltWith, Wappalyzer |
| 채용 | 채용 공고 (방향성 파악) |

### 좋은 경쟁 분석 특징

```
✅ 객관적 - 경쟁사 과소평가 금지
✅ 구체적 - 막연한 "더 좋다" 금지
✅ 실행 가능 - 차별화 전략 도출
✅ 업데이트 가능 - 지속적 모니터링
```

## 퀄리티 체크리스트

```
□ 직접/간접 경쟁사가 구분되었는가?
□ Feature Matrix가 완성되었는가?
□ 가격 비교가 정확한가?
□ 포지셔닝 맵이 그려졌는가?
□ 차별화 포인트가 명확한가?
□ 대응 전략이 구체적인가?
□ 모니터링 계획이 있는가?
```

## 🎯 인터랙티브 가이드

### 작성 전 확인 질문

**Q1. 직접 경쟁사를 알고 있나요?**
- 알고 있음 → 경쟁사 목록 확인
- 모름 → "어떤 키워드로 고객이 검색할까요?"

**Q2. 경쟁사 제품을 직접 사용해봤나요?**
- 사용해봄 → 장단점 공유 요청
- 안 해봄 → "무료 버전이라도 체험해보시겠어요?"

**Q3. 우리만의 차별점이 명확한가요?**
- 명확함 → 차별점 검증
- 불명확 → "경쟁사가 못하는 것은 무엇인가요?"

### 의사결정 포인트

| 시점 | 확인 내용 | 사용자 프롬프트 |
|------|----------|----------------|
| 경쟁사 식별 | 완전성 | "간접 경쟁사와 대체재도 고려했나요?" |
| 기능 비교 | 객관성 | "경쟁사의 강점을 인정하고 있나요?" |
| 포지셔닝 | 빈틈 | "시장에서 비어있는 영역은 어디인가요?" |
| 최종 확인 | 대응책 | "경쟁사 대응 전략이 현실적인가요?" |

---

## 다음 스킬 연결

Competitor Analysis 완료 후:

1. **사용자 검증** → User Research Skill
2. **비즈니스 모델** → Lean Canvas, Business Model Skill
3. **포지셔닝 적용** → Value Proposition 업데이트

---

*경쟁사를 알되 집착하지 말고, 고객에게 집중하세요.*
