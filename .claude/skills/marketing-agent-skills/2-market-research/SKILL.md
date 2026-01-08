---
name: mkt-market-research
description: |
  3C 프레임워크 기반 시장/경쟁사/고객 분석.
  전략 수립의 기초가 되는 리서치를 수행합니다.
triggers:
  - "시장 조사"
  - "경쟁사 분석"
  - "3C 분석"
  - "시장 리서치"
input:
  - context/{project}-context.md
  - 경쟁사 이름 (선택)
output:
  - research/{project}-3c-analysis.md
---

# Market Research Skill

3C 프레임워크 기반의 체계적인 시장 분석을 수행합니다.

## 3C 프레임워크

```
┌─────────────────────────────────────────────────────────────┐
│                        3C Analysis                           │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│         ┌──────────────┐                                    │
│         │   Customer   │                                    │
│         │    (고객)     │                                    │
│         └──────┬───────┘                                    │
│                │                                             │
│     ┌──────────┴──────────┐                                 │
│     │                     │                                  │
│     ▼                     ▼                                  │
│ ┌──────────┐       ┌──────────┐                             │
│ │ Company  │◀─────▶│Competitor│                             │
│ │  (자사)   │       │ (경쟁사) │                             │
│ └──────────┘       └──────────┘                             │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

## 분석 항목

### 1. Customer (고객) 분석

```yaml
market_size:
  tam: ""                     # Total Addressable Market
  sam: ""                     # Serviceable Available Market
  som: ""                     # Serviceable Obtainable Market

customer_segments:
  - segment_name: ""
    size: ""
    characteristics: []
    needs: []
    behavior: []

trends:
  - trend: ""
    impact: ""                # high/medium/low
    timeline: ""

pain_points:
  primary: []                 # 핵심 문제
  secondary: []               # 부가 문제

buying_behavior:
  decision_factors: []        # 구매 결정 요인
  information_sources: []     # 정보 수집 채널
  purchase_journey: ""        # 구매 여정
```

### 2. Competitor (경쟁사) 분석

```yaml
direct_competitors:
  - name: ""
    positioning: ""
    strengths: []
    weaknesses: []
    pricing: ""
    target: ""
    channels: []
    messaging: ""

indirect_competitors:
  - name: ""
    category: ""
    threat_level: ""          # high/medium/low

competitive_landscape:
  market_leader: ""
  challengers: []
  niche_players: []

competitive_advantages:
  our_strengths: []
  our_weaknesses: []
  opportunities: []
  threats: []
```

### 3. Company (자사) 분석

```yaml
current_position:
  market_share: ""
  brand_awareness: ""
  customer_perception: ""

resources:
  strengths: []
  constraints: []
  unique_assets: []

capabilities:
  core_competencies: []
  gaps: []
```

## 워크플로우

```
1. 컨텍스트 문서 확인
      │
      ▼
2. Customer 분석
   ├─ 시장 규모 추정
   ├─ 세그먼트 파악
   └─ 트렌드 분석
      │
      ▼
3. Competitor 분석
   ├─ 직접 경쟁사 분석
   ├─ 간접 경쟁사 파악
   └─ 경쟁 우위 도출
      │
      ▼
4. Company 분석
   ├─ 현재 위치 파악
   └─ 강점/약점 정리
      │
      ▼
5. 인사이트 도출
      │
      ▼
6. 3C 분석 리포트 생성
   → workspace/work-marketing/research/{project}-3c-analysis.md
```

## 리서치 방법

### 공개 정보 활용

```
경쟁사 웹사이트
├─ 가격 페이지
├─ 기능 비교
├─ 고객 후기
└─ 블로그/콘텐츠

리뷰 사이트
├─ G2, Capterra (SaaS)
├─ 앱스토어 리뷰
└─ 네이버/구글 리뷰

업계 리포트
├─ 시장 규모
├─ 성장률
└─ 트렌드
```

### 웹 검색 쿼리 예시

```
시장 규모: "{industry} market size 2024"
경쟁사: "{competitor} vs alternatives"
트렌드: "{industry} trends 2024"
고객 리뷰: "{competitor} reviews"
```

## 출력 템플릿

```markdown
# {Project Name} 3C Analysis

## Executive Summary

{한 문단 요약: 핵심 인사이트 3가지}

---

## 1. Customer Analysis (고객 분석)

### 1.1 시장 규모

| 구분 | 규모 | 비고 |
|------|------|------|
| TAM (전체 시장) | {tam} | {note} |
| SAM (접근 가능) | {sam} | {note} |
| SOM (획득 가능) | {som} | {note} |

### 1.2 고객 세그먼트

#### 세그먼트 A: {name}
- **규모**: {size}
- **특성**: {characteristics}
- **니즈**: {needs}
- **행동**: {behavior}

#### 세그먼트 B: {name}
...

### 1.3 시장 트렌드

| 트렌드 | 영향도 | 시기 | 기회/위협 |
|--------|--------|------|----------|
| {trend_1} | High | 2024-2025 | 기회 |
| {trend_2} | Medium | 진행 중 | 위협 |

### 1.4 Pain Points

**핵심 문제**
1. {pain_point_1}
2. {pain_point_2}

**부가 문제**
1. {secondary_1}

### 1.5 구매 행동

- **결정 요인**: {factors}
- **정보 채널**: {channels}
- **구매 여정**: {journey}

---

## 2. Competitor Analysis (경쟁사 분석)

### 2.1 경쟁 구도

```
┌─────────────────────────────────────┐
│           Market Leader             │
│            {leader}                 │
├─────────────────────────────────────┤
│          Challengers                │
│     {challenger_1}, {challenger_2}  │
├─────────────────────────────────────┤
│         Niche Players               │
│     {niche_1}, {niche_2}            │
└─────────────────────────────────────┘
```

### 2.2 직접 경쟁사 상세

#### {Competitor 1}

| 항목 | 내용 |
|------|------|
| 포지셔닝 | {positioning} |
| 타겟 | {target} |
| 가격 | {pricing} |
| 핵심 메시지 | {messaging} |

**강점**
- {strength_1}
- {strength_2}

**약점**
- {weakness_1}
- {weakness_2}

**채널**
- {channel_1}
- {channel_2}

#### {Competitor 2}
...

### 2.3 경쟁 비교표

| 항목 | 우리 | 경쟁사 A | 경쟁사 B |
|------|------|---------|---------|
| 가격 | {price} | {price_a} | {price_b} |
| 핵심 기능 | {feature} | {feature_a} | {feature_b} |
| 타겟 | {target} | {target_a} | {target_b} |
| 강점 | {strength} | {strength_a} | {strength_b} |

### 2.4 SWOT 분석

```
┌──────────────────┬──────────────────┐
│    Strengths     │   Weaknesses     │
│    (강점)         │    (약점)         │
├──────────────────┼──────────────────┤
│ • {s1}           │ • {w1}           │
│ • {s2}           │ • {w2}           │
├──────────────────┼──────────────────┤
│   Opportunities  │     Threats      │
│    (기회)         │    (위협)         │
├──────────────────┼──────────────────┤
│ • {o1}           │ • {t1}           │
│ • {o2}           │ • {t2}           │
└──────────────────┴──────────────────┘
```

---

## 3. Company Analysis (자사 분석)

### 3.1 현재 위치

- **시장 점유율**: {market_share}
- **브랜드 인지도**: {awareness}
- **고객 인식**: {perception}

### 3.2 핵심 역량

1. {competency_1}
2. {competency_2}

### 3.3 리소스 제약

1. {constraint_1}
2. {constraint_2}

---

## 4. Key Insights & Implications

### 핵심 인사이트

1. **{insight_1_title}**
   {insight_1_detail}
   → 시사점: {implication_1}

2. **{insight_2_title}**
   {insight_2_detail}
   → 시사점: {implication_2}

3. **{insight_3_title}**
   {insight_3_detail}
   → 시사점: {implication_3}

### 전략 방향 제안

| 영역 | 제안 | 우선순위 |
|------|------|---------|
| 포지셔닝 | {suggestion_1} | High |
| 타겟팅 | {suggestion_2} | High |
| 채널 | {suggestion_3} | Medium |
| 메시징 | {suggestion_4} | Medium |

---

## 5. 다음 단계

1. [ ] Persona Skill로 타겟 고객 상세화
2. [ ] Positioning Skill로 차별화 전략 수립
3. [ ] Strategy Skill로 마케팅 전략 수립

---

*리서치 날짜: {date}*
*데이터 출처: {sources}*
```

## 퀄리티 vs 한계

### 강한 영역
- 공개 정보 기반 경쟁사 분석
- 프레임워크 기반 구조화
- 시사점 도출

### 한계
- 실시간/정확한 시장 규모 데이터
- 비공개 경쟁사 정보
- 실제 고객 인터뷰 데이터

### 보완 방법
- 사용자가 보유한 시장 데이터 제공
- 업계 리포트 URL 공유
- 고객 피드백/리뷰 공유

## 다음 스킬 연결

- **Persona Skill**: 고객 세그먼트를 상세 페르소나로 발전
- **Positioning Skill**: 경쟁 분석 기반 포지셔닝
- **Strategy Skill**: 인사이트 기반 전략 수립

---

*3C 분석은 전략의 기초입니다. 정확한 리서치가 좋은 전략을 만듭니다.*
