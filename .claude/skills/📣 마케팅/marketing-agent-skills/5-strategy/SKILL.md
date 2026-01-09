---
name: mkt-strategy
description: |
  마케팅 전략 수립 (PESO 미디어 믹스, North Star Metric).
  전체 마케팅 방향과 로드맵을 정의합니다.
triggers:
  - "마케팅 전략"
  - "전략 수립"
  - "PESO"
  - "마케팅 로드맵"
input:
  - context/{project}-context.md
  - strategy/positioning.md
  - personas/*.md
output:
  - strategy/marketing-strategy.md
---

# Strategy Skill

PESO 미디어 믹스와 North Star Metric 기반의 마케팅 전략을 수립합니다.

## PESO 프레임워크

```
┌─────────────────────────────────────────────────────────────┐
│                      PESO Model                              │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│   ┌──────────┐   ┌──────────┐   ┌──────────┐   ┌──────────┐│
│   │  Paid    │   │  Earned  │   │  Shared  │   │  Owned   ││
│   │  Media   │   │  Media   │   │  Media   │   │  Media   ││
│   └──────────┘   └──────────┘   └──────────┘   └──────────┘│
│                                                              │
│   광고, 스폰서     PR, 언론       소셜, 바이럴    웹사이트,    │
│                                                 블로그,      │
│                                                 뉴스레터     │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

### PESO 상세

```yaml
paid:                         # 유료 미디어
  channels:
    - search_ads              # 검색 광고
    - display_ads             # 디스플레이
    - social_ads              # 소셜 광고
    - sponsored_content       # 스폰서 콘텐츠
    - influencer_paid         # 인플루언서 (유료)
  characteristics:
    - immediate_results
    - scalable
    - measurable
    - requires_budget

earned:                       # 획득 미디어
  channels:
    - press_coverage          # 언론 보도
    - reviews                 # 리뷰
    - word_of_mouth          # 입소문
    - organic_mentions        # 자연 언급
  characteristics:
    - high_credibility
    - free
    - unpredictable
    - hard_to_scale

shared:                       # 공유 미디어
  channels:
    - social_media            # 소셜 미디어
    - user_generated_content  # UGC
    - community               # 커뮤니티
    - viral_content           # 바이럴
  characteristics:
    - engagement_focused
    - community_building
    - amplification

owned:                        # 소유 미디어
  channels:
    - website                 # 웹사이트
    - blog                    # 블로그
    - email_list              # 이메일
    - app                     # 앱
  characteristics:
    - full_control
    - long_term_asset
    - requires_content
```

## North Star Metric (NSM)

```
┌─────────────────────────────────────────────────────────────┐
│                    North Star Metric                         │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│   "고객에게 전달하는 핵심 가치를 반영하는 단 하나의 지표"       │
│                                                              │
│   예시:                                                      │
│   • Airbnb: "예약된 숙박 일수"                               │
│   • Spotify: "청취 시간"                                     │
│   • Slack: "일일 활성 사용자의 메시지 수"                     │
│   • Facebook: "일일 활성 사용자"                             │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

### NSM 선정 기준

```yaml
criteria:
  - reflects_value: true      # 고객 가치 반영
  - measurable: true          # 측정 가능
  - actionable: true          # 행동 유도
  - leading_indicator: true   # 선행 지표
  - team_aligned: true        # 팀 정렬 가능
```

## 워크플로우

```
1. 기존 문서 확인
   ├─ 컨텍스트
   ├─ 포지셔닝
   └─ 페르소나
      │
      ▼
2. 목표 설정
   ├─ North Star Metric 정의
   └─ SMART Goals 수립
      │
      ▼
3. PESO 믹스 설계
   ├─ 채널별 역할 정의
   └─ 예산 배분
      │
      ▼
4. 전략 프레임워크
   ├─ 핵심 전략 3가지
   └─ 실행 로드맵
      │
      ▼
5. 문서 저장
   → workspace/work-marketing/strategy/marketing-strategy.md
```

## 출력 템플릿

```markdown
# {Project Name} Marketing Strategy

## Executive Summary

{전략 한 문단 요약}

---

## 1. Strategic Foundation

### Vision
{마케팅 비전}

### Mission
{마케팅 미션}

### North Star Metric

| 항목 | 내용 |
|------|------|
| NSM | {north_star_metric} |
| 현재 | {current_value} |
| 목표 | {target_value} |
| 기간 | {timeline} |

**선정 이유**: {rationale}

---

## 2. Goals & Objectives

### Primary Goal
{primary_goal}

### SMART Objectives

| 목표 | Specific | Measurable | Achievable | Relevant | Time-bound |
|------|----------|------------|------------|----------|------------|
| {obj_1} | {s} | {m} | {a} | {r} | {t} |
| {obj_2} | {s} | {m} | {a} | {r} | {t} |
| {obj_3} | {s} | {m} | {a} | {r} | {t} |

### KPI Dashboard

| KPI | 현재 | 목표 | 측정 방법 |
|-----|------|------|----------|
| {kpi_1} | {current} | {target} | {method} |
| {kpi_2} | {current} | {target} | {method} |
| {kpi_3} | {current} | {target} | {method} |

---

## 3. Target Audience

### Primary Target
{primary_target_summary}
→ 상세: [Persona 1 링크]

### Secondary Target
{secondary_target_summary}
→ 상세: [Persona 2 링크]

---

## 4. Positioning Recap

> "{positioning_statement}"

### Key Messages

1. **Primary**: {primary_message}
2. **Supporting**: {supporting_message_1}
3. **Supporting**: {supporting_message_2}

---

## 5. PESO Media Mix

### 채널 전략

```
┌──────────────────────────────────────────────────────────┐
│                    PESO Allocation                        │
├──────────────────────────────────────────────────────────┤
│                                                           │
│   Paid (40%)        Earned (10%)                         │
│   ████████          ██                                   │
│                                                           │
│   Shared (20%)      Owned (30%)                          │
│   ████              ██████                               │
│                                                           │
└──────────────────────────────────────────────────────────┘
```

### Paid Media

| 채널 | 목적 | 예산 비중 | 예상 결과 |
|------|------|----------|----------|
| {channel_1} | {purpose} | {%} | {result} |
| {channel_2} | {purpose} | {%} | {result} |

**핵심 전략**: {paid_strategy}

### Earned Media

| 채널 | 목적 | 활동 | 예상 결과 |
|------|------|------|----------|
| {channel_1} | {purpose} | {activity} | {result} |

**핵심 전략**: {earned_strategy}

### Shared Media

| 채널 | 목적 | 콘텐츠 유형 | 빈도 |
|------|------|------------|------|
| {channel_1} | {purpose} | {content} | {frequency} |
| {channel_2} | {purpose} | {content} | {frequency} |

**핵심 전략**: {shared_strategy}

### Owned Media

| 채널 | 목적 | 콘텐츠 유형 | 빈도 |
|------|------|------------|------|
| {channel_1} | {purpose} | {content} | {frequency} |
| {channel_2} | {purpose} | {content} | {frequency} |

**핵심 전략**: {owned_strategy}

---

## 6. Core Strategies (핵심 전략 3가지)

### Strategy 1: {name}

**목표**: {goal}

**접근법**: {approach}

**핵심 활동**:
1. {activity_1}
2. {activity_2}
3. {activity_3}

**성공 지표**: {metrics}

### Strategy 2: {name}

**목표**: {goal}

**접근법**: {approach}

**핵심 활동**:
1. {activity_1}
2. {activity_2}
3. {activity_3}

**성공 지표**: {metrics}

### Strategy 3: {name}

**목표**: {goal}

**접근법**: {approach}

**핵심 활동**:
1. {activity_1}
2. {activity_2}
3. {activity_3}

**성공 지표**: {metrics}

---

## 7. Budget Allocation

### 전체 예산

| 항목 | 금액 | 비중 |
|------|------|------|
| 총 예산 | {total} | 100% |
| Paid | {paid} | {%} |
| Content | {content} | {%} |
| Tools | {tools} | {%} |
| Other | {other} | {%} |

### 채널별 예산

| 채널 | 월 예산 | 분기 예산 | 예상 ROI |
|------|--------|----------|---------|
| {channel_1} | {monthly} | {quarterly} | {roi} |
| {channel_2} | {monthly} | {quarterly} | {roi} |

---

## 8. Roadmap

### Phase 1: Foundation ({month_1}-{month_2})

**목표**: {phase_1_goal}

| 주차 | 활동 | 담당 | 산출물 |
|------|------|------|--------|
| W1-2 | {activity} | {owner} | {deliverable} |
| W3-4 | {activity} | {owner} | {deliverable} |

### Phase 2: Growth ({month_3}-{month_4})

**목표**: {phase_2_goal}

| 주차 | 활동 | 담당 | 산출물 |
|------|------|------|--------|
| W1-2 | {activity} | {owner} | {deliverable} |
| W3-4 | {activity} | {owner} | {deliverable} |

### Phase 3: Optimization ({month_5}-{month_6})

**목표**: {phase_3_goal}

| 주차 | 활동 | 담당 | 산출물 |
|------|------|------|--------|
| W1-2 | {activity} | {owner} | {deliverable} |
| W3-4 | {activity} | {owner} | {deliverable} |

---

## 9. Risk & Mitigation

| 리스크 | 영향도 | 발생 확률 | 대응 방안 |
|--------|--------|----------|----------|
| {risk_1} | High | Medium | {mitigation} |
| {risk_2} | Medium | High | {mitigation} |
| {risk_3} | Low | High | {mitigation} |

---

## 10. Success Criteria

### 단기 (1-3개월)
- [ ] {criteria_1}
- [ ] {criteria_2}
- [ ] {criteria_3}

### 중기 (3-6개월)
- [ ] {criteria_1}
- [ ] {criteria_2}

### 장기 (6-12개월)
- [ ] {criteria_1}
- [ ] {criteria_2}

---

## 11. 다음 단계

1. [ ] Campaign Skill로 캠페인 상세 기획
2. [ ] Funnel Skill로 퍼널 설계
3. [ ] Content 스킬들로 실행물 제작

---

*Strategy Version: 1.0*
*Created: {date}*
*Review Date: {review_date}*
```

## 전략 예시

### B2B SaaS 예시

```markdown
## North Star Metric
"주간 활성 API 호출 수"
→ 고객이 우리 제품에서 가치를 얻고 있다는 직접적 증거

## PESO Mix
- Paid (30%): Google Ads (개발자 키워드), LinkedIn
- Earned (10%): Product Hunt, 개발자 미디어
- Shared (30%): Twitter, GitHub, 개발자 커뮤니티
- Owned (30%): 블로그 (기술 콘텐츠), 뉴스레터

## Core Strategies
1. Developer Evangelism - 개발자 커뮤니티 신뢰 구축
2. Content-Led Growth - 기술 블로그로 SEO 확보
3. Product-Led Growth - 무료 티어로 바이럴
```

## AI 시대 전략 강화 (2025)

### 2025 핵심 트렌드

```yaml
key_insights:
  숏폼이_왕이다:
    stat: "78%의 사람들이 숏폼 비디오로 새 제품을 알게 됨"
    implication: "숏폼 80% + 이미지/텍스트 20%"

  바이럴_equals_참여:
    principle: "팔리는 콘텐츠 ❌ → 공감이 전염되는 콘텐츠 ✅"
    implication: "소비자가 공동 창작자가 되어야 확산"

  커뮤니티가_핵:
    principle: "신뢰 + 공감 + 커뮤니티 = 2025 확산의 3축"
    implication: "초기 100명의 열성 팬이 1만 명보다 가치있음"

  AI_도구가_게임_체인저:
    stat: "79% 크리에이터가 AI로 더 많은 콘텐츠 생산"
    implication: "예산 0원도 AI 도구로 프로급 콘텐츠 가능"
```

### 숏폼 우선 전략 (PESO 재정의)

```yaml
peso_2025:
  Paid:
    전통: "검색광고, 디스플레이"
    AI강화: "틱톡/릴스 프로모션, 마이크로 인플루언서"

  Earned:
    전통: "PR, 언론"
    AI강화: "바이럴 챌린지 참여, UGC 확산"

  Shared:
    전통: "소셜 미디어"
    AI강화:
      - "숏폼 비디오 80%"
      - "참여형 챌린지"
      - "밈화 유도"
      - "커뮤니티 팬덤"

  Owned:
    전통: "웹사이트, 블로그"
    AI강화:
      - "Discord/카톡 커뮤니티"
      - "Building in Public"
      - "앰배서더 프로그램"
```

### 콘텐츠 비중 가이드

```
2025 콘텐츠 믹스
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
숏폼 비디오    ████████████████████████  80%
(TikTok, Reels, Shorts)

이미지/텍스트  █████                      20%
(피드, 카드뉴스, 블로그)
```

### 플랫폼 우선순위

```yaml
platform_priority:
  바이럴_잠재력:
    1: "TikTok (알고리즘 노출 기회 최고)"
    2: "Instagram Reels"
    3: "YouTube Shorts"

  타겟별_선택:
    2030_국내: [TikTok, Instagram]
    B2B: [LinkedIn, Twitter]
    개발자: [Twitter, GitHub, Discord]
    10대: [TikTok]
```

### AI 도구 추천

```yaml
ai_tools:
  무료_필수:
    영상_편집: "CapCut"
    그래픽: "Canva AI"
    스크립트: "ChatGPT"
    랜딩페이지: "Carrd, Tally"
    이메일: "Mailchimp (무료 티어)"
    분석: "Google Analytics 4"

  유료_추천:
    영상: "Descript, Runway"
    그래픽: "Midjourney, DALL-E"
    아바타: "HeyGen, Synthesia"
    카피: "Jasper, Copy.ai"
    자동화: "Zapier, Make"
```

### 전략 체크리스트 (AI 시대)

```markdown
□ 숏폼 비디오가 콘텐츠 믹스의 80%인가?
□ 참여형 챌린지/밈 요소가 있는가?
□ 커뮤니티 빌딩 계획이 있는가?
□ AI 도구 활용 계획이 구체적인가?
□ Building in Public 전략이 있는가?
□ 마이크로 인플루언서 활용 계획이 있는가?
□ 무예산으로도 실행 가능한 전략이 있는가?
```

---

## 다음 스킬 연결

- **Campaign Skill**: 전략을 구체적 캠페인으로 (챌린지 포함)
- **Funnel Skill**: AARRR 퍼널 상세 설계
- **Copywriting Skill**: 숏폼 스크립트 제작
- **Analytics KPI Skill**: KPI 측정 체계 구축

---

*좋은 전략은 "무엇을 하지 않을 것인가"를 명확히 합니다.*
*모든 것을 다 할 수는 없습니다. 선택과 집중이 핵심입니다.*
*2025년엔 "어떻게 참여하게 만들 것인가?"가 선택의 기준입니다.*
