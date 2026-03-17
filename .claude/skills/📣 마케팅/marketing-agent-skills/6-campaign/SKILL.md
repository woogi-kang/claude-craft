---
name: mkt-campaign
description: |
  마케팅 캠페인 기획 (SMART Goals, 채널, 예산).
  구체적인 캠페인 계획을 수립합니다.
triggers:
  - "캠페인 기획"
  - "캠페인 설계"
  - "프로모션 기획"
  - "런칭 캠페인"
input:
  - context/{project}-context.md
  - strategy/marketing-strategy.md
output:
  - strategy/campaign-plan.md
---

# Campaign Skill

SMART Goals 기반의 마케팅 캠페인을 기획합니다.

## 캠페인 유형

```yaml
campaign_types:
  awareness:                  # 인지도
    - brand_launch
    - product_launch
    - rebranding

  acquisition:                # 획득
    - lead_generation
    - signup_drive
    - trial_campaign

  conversion:                 # 전환
    - sales_promotion
    - upsell_campaign
    - seasonal_sale

  retention:                  # 유지
    - loyalty_program
    - reengagement
    - referral_program

  advocacy:                   # 옹호
    - ugc_campaign
    - review_campaign
    - ambassador_program
```

## SMART Goals 프레임워크

```
┌─────────────────────────────────────────────────────────────┐
│                       SMART Goals                            │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│   S - Specific (구체적)                                      │
│       "가입자 늘리기" ❌                                     │
│       "무료 체험 가입자 100명 확보" ✅                        │
│                                                              │
│   M - Measurable (측정 가능)                                 │
│       측정 방법과 도구 명시                                   │
│                                                              │
│   A - Achievable (달성 가능)                                 │
│       현실적인 목표, 리소스 고려                              │
│                                                              │
│   R - Relevant (관련성)                                      │
│       비즈니스 목표와 연결                                    │
│                                                              │
│   T - Time-bound (기한)                                      │
│       명확한 시작일과 종료일                                  │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

## 캠페인 구성 요소

```yaml
campaign_elements:
  objective:
    primary_goal: ""
    secondary_goals: []
    success_metrics: []

  target:
    primary_audience: ""
    secondary_audience: ""
    exclusions: []

  message:
    key_message: ""
    supporting_points: []
    cta: ""

  channels:
    primary: []
    secondary: []
    budget_split: {}

  creative:
    formats: []
    assets_needed: []

  timeline:
    start_date: ""
    end_date: ""
    milestones: []

  budget:
    total: ""
    breakdown: {}
    contingency: ""
```

## 워크플로우

```
1. 기존 전략 문서 확인
      │
      ▼
2. 캠페인 목표 설정 (SMART)
      │
      ▼
3. 타겟 오디언스 정의
      │
      ▼
4. 메시지 & CTA 설계
      │
      ▼
5. 채널 & 예산 배분
      │
      ▼
6. 타임라인 수립
      │
      ▼
7. 성공 지표 정의
      │
      ▼
8. 캠페인 기획서 저장
   → workspace/work-marketing/strategy/campaign-plan.md
```

## 출력 템플릿

```markdown
# {Campaign Name} Campaign Plan

## Campaign Overview

| 항목 | 내용 |
|------|------|
| 캠페인명 | {name} |
| 유형 | {type} |
| 기간 | {start_date} - {end_date} |
| 총 예산 | {total_budget} |

### Campaign Summary
{한 문단 요약}

---

## 1. Objectives (목표)

### Primary Goal (SMART)

| SMART | 내용 |
|-------|------|
| Specific | {specific} |
| Measurable | {measurable} |
| Achievable | {achievable} |
| Relevant | {relevant} |
| Time-bound | {time_bound} |

**목표 문장**: "{goal_statement}"

### Secondary Goals
1. {secondary_1}
2. {secondary_2}

### Success Metrics

| 지표 | 목표 | 측정 방법 |
|------|------|----------|
| {metric_1} | {target} | {method} |
| {metric_2} | {target} | {method} |
| {metric_3} | {target} | {method} |

---

## 2. Target Audience (타겟)

### Primary Audience
{primary_description}
→ Persona: {persona_name}

### Secondary Audience
{secondary_description}

### Exclusions (제외 대상)
- {exclusion_1}
- {exclusion_2}

---

## 3. Messaging (메시지)

### Key Message
> "{key_message}"

### Supporting Messages
1. {supporting_1}
2. {supporting_2}
3. {supporting_3}

### Call-to-Action
**Primary CTA**: {primary_cta}
**Secondary CTA**: {secondary_cta}

### Message by Stage

| 퍼널 단계 | 메시지 | CTA |
|----------|--------|-----|
| 인지 | {awareness_msg} | {cta} |
| 고려 | {consideration_msg} | {cta} |
| 결정 | {decision_msg} | {cta} |

---

## 4. Channels & Tactics (채널)

### Channel Mix

```
Channel Allocation
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
{channel_1}  ████████████████  40%
{channel_2}  ████████          25%
{channel_3}  ██████            20%
{channel_4}  ████              15%
```

### Channel Details

#### {Channel 1}

| 항목 | 내용 |
|------|------|
| 목적 | {purpose} |
| 타겟팅 | {targeting} |
| 포맷 | {format} |
| 예산 | {budget} |
| 예상 결과 | {expected_result} |

**Tactics**:
1. {tactic_1}
2. {tactic_2}

#### {Channel 2}
...

---

## 5. Creative Requirements (크리에이티브)

### 필요 에셋

| 에셋 | 규격 | 수량 | 담당 | 마감 |
|------|------|------|------|------|
| {asset_1} | {spec} | {qty} | {owner} | {deadline} |
| {asset_2} | {spec} | {qty} | {owner} | {deadline} |

### Creative Guidelines
- 톤앤매너: {tone}
- 컬러: {colors}
- 이미지 스타일: {image_style}

---

## 6. Timeline (타임라인)

### Overview

```
{month_1}          {month_2}          {month_3}
    │                  │                  │
    ▼                  ▼                  ▼
┌────────┐        ┌────────┐        ┌────────┐
│ Phase 1│   →    │ Phase 2│   →    │ Phase 3│
│ 준비   │        │ 런칭   │        │ 최적화 │
└────────┘        └────────┘        └────────┘
```

### Detailed Timeline

| 주차 | 단계 | 활동 | 담당 | 산출물 |
|------|------|------|------|--------|
| W1 | 준비 | {activity} | {owner} | {deliverable} |
| W2 | 준비 | {activity} | {owner} | {deliverable} |
| W3 | 런칭 | {activity} | {owner} | {deliverable} |
| W4 | 최적화 | {activity} | {owner} | {deliverable} |

### Key Milestones

| 날짜 | 마일스톤 | 상태 |
|------|----------|------|
| {date_1} | {milestone_1} | ⬜ |
| {date_2} | {milestone_2} | ⬜ |
| {date_3} | {milestone_3} | ⬜ |

---

## 7. Budget (예산)

### Budget Summary

| 항목 | 금액 | 비중 |
|------|------|------|
| 총 예산 | {total} | 100% |
| 미디어 비용 | {media} | {%} |
| 크리에이티브 | {creative} | {%} |
| 툴/소프트웨어 | {tools} | {%} |
| 예비비 | {contingency} | 10% |

### Channel Budget Breakdown

| 채널 | 예산 | CPM/CPC 예상 | 예상 도달 |
|------|------|-------------|----------|
| {channel_1} | {budget} | {cost} | {reach} |
| {channel_2} | {budget} | {cost} | {reach} |

---

## 8. Measurement & Optimization (측정)

### KPIs

| 단계 | KPI | 목표 | 측정 도구 |
|------|-----|------|----------|
| 인지 | {kpi} | {target} | {tool} |
| 참여 | {kpi} | {target} | {tool} |
| 전환 | {kpi} | {target} | {tool} |

### Optimization Plan

**Weekly Review**:
- {review_item_1}
- {review_item_2}

**Optimization Triggers**:
- If {metric} < {threshold} → {action}
- If {metric} > {threshold} → {action}

### A/B Tests Planned

| 테스트 | 변수 | 가설 |
|--------|------|------|
| {test_1} | {variable} | {hypothesis} |
| {test_2} | {variable} | {hypothesis} |

---

## 9. Risks & Contingencies (리스크)

| 리스크 | 확률 | 영향 | 대응 방안 |
|--------|------|------|----------|
| {risk_1} | High | High | {mitigation} |
| {risk_2} | Medium | Medium | {mitigation} |

---

## 10. Team & Responsibilities (팀)

| 역할 | 담당 | 책임 |
|------|------|------|
| 캠페인 매니저 | {name} | 전체 관리 |
| 크리에이티브 | {name} | 에셋 제작 |
| 미디어 바잉 | {name} | 광고 집행 |
| 분석 | {name} | 성과 측정 |

---

## 11. Appendix

### Checklist

**런칭 전**
- [ ] 크리에이티브 에셋 완료
- [ ] 랜딩페이지 라이브
- [ ] 트래킹 설정 완료
- [ ] 광고 계정 세팅
- [ ] 팀 브리핑 완료

**런칭 후**
- [ ] 첫 날 성과 확인
- [ ] 주간 리뷰 미팅
- [ ] 최적화 적용
- [ ] 최종 리포트

---

*Campaign Version: 1.0*
*Created: {date}*
*Owner: {owner}*
```

## AI 시대 캠페인 강화 (2025)

### 참여형 챌린지 캠페인

```yaml
challenge_campaign:
  핵심_원칙: "팔리는 콘텐츠 ❌ → 공감이 전염되는 콘텐츠 ✅"

  챌린지_유형:
    자기_비하_유머:
      - "#사진정리포기챌린지"
      - "#실패인증챌린지"
      바이럴_포인트: "공감 + 숫자가 클수록 재미"

    졸업_이사_콘셉트:
      - "#비트윈졸업챌린지"
      - "#새앱이사챌린지"
      바이럴_포인트: "졸업 = 성장 느낌"

    Before_After:
      - "#AI가알아서챌린지"
      - "#변신챌린지"
      바이럴_포인트: "시각적 임팩트"

  챌린지_설계_체크리스트:
    - 참여 장벽이 낮은가? (30초 내 완료)
    - 자랑하고 싶은 결과물인가?
    - 친구 태그가 자연스러운가?
    - 트렌드 사운드 활용 가능한가?
```

### 커뮤니티 팬덤 빌딩

```yaml
community_strategy:
  Building_in_Public:
    description: "개발/마케팅 과정을 실시간 공유"
    채널: [Twitter, Threads, 인스타그램 스토리]
    효과:
      - 투명성 → 신뢰
      - 팔로워가 응원하게 됨
      - 런칭 시 자발적 홍보

  앰배서더_프로그램:
    조건: "사전예약 + 친구 3명 초대"
    혜택:
      - 평생 프리미엄 무료
      - 신기능 먼저 체험
      - 전용 배지/타이틀
    목표: "50명의 앰배서더 → 150명 추가 확보"

  커뮤니티_채널:
    Discord: "해외 타겟, 개발자 친화적"
    카카오_오픈채팅: "국내 타겟, 접근성 최고"
    운영_포인트:
      - 사전예약자 전용
      - 개발 과정 실시간 공유
      - 기능 투표 참여
      - 얼리어답터 특권
```

### 무예산/저예산 바이럴 전략

```yaml
zero_budget_tactics:
  숏폼_집중:
    비중: "숏폼 80% + 이미지 20%"
    우선순위:
      1: "TikTok (바이럴 잠재력 최고)"
      2: "Instagram Reels"
      3: "YouTube Shorts"

  AI_도구_활용:
    영상_편집: "CapCut (무료, 트렌드 템플릿)"
    그래픽: "Canva AI (무료, 배경 제거)"
    스크립트: "ChatGPT (훅 문구, 스크립트)"
    음악: "CapCut/TikTok (트렌드 사운드)"
    아바타: "HeyGen Free (AI 아바타)"
    랜딩페이지: "Carrd/Tally (무료)"

  마이크로_인플루언서:
    조건: "1K-10K 팔로워"
    방식: "제품 제공 대가 리뷰"
    기대효과: "진정성 높은 추천"
```

### AI 콘텐츠 대량 생산 파이프라인

```
┌─────────────────────────────────────────────────────────────┐
│               AI 콘텐츠 생산 파이프라인                       │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│   1. 아이디어 생성 (ChatGPT)                                 │
│      "바이럴 훅 10개 생성해줘"                                │
│                                                              │
│   2. 스크립트 작성 (ChatGPT)                                 │
│      "15초 틱톡 스크립트로 변환해줘"                          │
│                                                              │
│   3. 비주얼 제작 (Canva AI)                                  │
│      텍스트 오버레이, 썸네일 생성                             │
│                                                              │
│   4. 영상 편집 (CapCut)                                      │
│      자동 캡션, 트렌드 템플릿 적용                            │
│                                                              │
│   5. 최적화 (AI 분석)                                        │
│      성과 분석 → 다음 콘텐츠 개선                             │
│                                                              │
│   결과: 1시간에 5개 콘텐츠 생산 가능                          │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

---

<!-- Merged from coreyhaines31/marketingskills -->

## ORB Framework (Owned / Rented / Borrowed)

PESO 모델의 대안으로, 채널을 소유권 관점에서 분류합니다. 모든 것은 궁극적으로 Owned 채널로 귀결되어야 합니다.

```
┌─────────────────────────────────────────────────────────────┐
│                      ORB Framework                           │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│   ┌──────────────┐  ┌──────────────┐  ┌──────────────┐     │
│   │   Owned      │  │   Rented     │  │   Borrowed   │     │
│   │   Channels   │  │   Channels   │  │   Channels   │     │
│   └──────────────┘  └──────────────┘  └──────────────┘     │
│                                                              │
│   이메일 리스트       소셜 미디어         게스트 콘텐츠       │
│   블로그             앱 스토어           팟캐스트 인터뷰     │
│   팟캐스트           YouTube            콜라보레이션        │
│   커뮤니티           Reddit             컨퍼런스 발표       │
│   웹사이트           마켓플레이스        인플루언서 파트너십  │
│                                                              │
│   → 시간이 갈수록     → 알고리즘 변경     → 타인의 청중에     │
│     가치 증가          위험 있음           접근 가능          │
│   → 직접 관계         → 속도는 빠름       → 즉각적 신뢰      │
│   → 복리 효과         → 안정성 낮음       → 일회성 가능성     │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

### Owned 채널 선택 가이드

```yaml
owned_channel_selection:
  업계에_양질_콘텐츠_부족: "→ 블로그 시작"
  직접_업데이트_원하는_청중: "→ 이메일 집중"
  참여도가_중요: "→ 커뮤니티 구축 (Discord/카톡)"
```

### Rented → Owned 전환

```
Rented 채널 활동 → Owned 채널로 유도
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Twitter 스레드 → 뉴스레터 구독 유도
LinkedIn 포스트 → 게이티드 콘텐츠 or 이메일 구독
YouTube 영상 → 웹사이트 방문 유도
Reddit 활동 → 제품 사이트로 링크
```

---

## 5-Phase Launch Approach (5단계 런칭)

런칭은 하루의 이벤트가 아니라, 모멘텀을 쌓아가는 단계적 과정입니다.

```
┌────────────┐   ┌────────────┐   ┌────────────┐   ┌────────────┐   ┌────────────┐
│  Phase 1   │ → │  Phase 2   │ → │  Phase 3   │ → │  Phase 4   │ → │  Phase 5   │
│  Internal  │   │   Alpha    │   │    Beta    │   │ Early Access│   │ Full Launch│
│  Launch    │   │   Launch   │   │   Launch   │   │   Launch   │   │            │
└────────────┘   └────────────┘   └────────────┘   └────────────┘   └────────────┘
```

### Phase 1: Internal Launch

```yaml
internal_launch:
  목표: "핵심 기능을 친근한 사용자와 검증"
  actions:
    - "1:1로 얼리 사용자 모집하여 무료 테스트"
    - "사용성 갭과 누락 기능에 대한 피드백 수집"
    - "데모 가능한 수준의 프로토타입 확보 (프로덕션 레디 불필요)"
```

### Phase 2: Alpha Launch

```yaml
alpha_launch:
  목표: "최초 외부 검증 및 웨이트리스트 구축"
  actions:
    - "얼리 액세스 신청 폼이 있는 랜딩 페이지 생성"
    - "제품 존재를 알리는 발표"
    - "개별 초대로 사용자 테스트 시작"
    - "프로덕션에서 동작하는 MVP (진화 중이어도 OK)"
```

### Phase 3: Beta Launch

```yaml
beta_launch:
  목표: "버즈 생성 및 더 넓은 피드백으로 제품 개선"
  actions:
    - "얼리 액세스 리스트 처리 (일부 무료, 일부 유료)"
    - "해결하는 문제에 대한 티저 마케팅 시작"
    - "친구, 투자자, 인플루언서에게 테스트 & 공유 요청"
  consider:
    - "Coming soon 랜딩 페이지 또는 웨이트리스트"
    - "대시보드에 'Beta' 스티커"
    - "얼리 액세스 리스트에 이메일 초대"
```

### Phase 4: Early Access Launch

```yaml
early_access_launch:
  목표: "스케일 검증 및 풀 런칭 준비"
  actions:
    - "제품 상세 공개: 스크린샷, 기능 GIF, 데모"
    - "정량적 사용 데이터 + 정성적 피드백 수집"
    - "참여 사용자 대상 사용자 리서치 (크레딧 인센티브)"
    - "PMF 서베이로 메시징 정제 (선택)"
  expansion_options:
    option_a: "배치별 초대 (한 번에 5-10%)"
    option_b: "'Early Access' 프레이밍으로 전체 초대"
```

### Phase 5: Full Launch

```yaml
full_launch:
  목표: "최대 가시성 및 유료 사용자 전환"
  actions:
    - "셀프서브 가입 오픈"
    - "과금 시작 (아직 안 했다면)"
    - "모든 채널에서 GA(General Availability) 발표"
  launch_touchpoints:
    - "고객 이메일"
    - "인앱 팝업 및 프로덕트 투어"
    - "웹사이트 배너"
    - "대시보드 'New' 스티커"
    - "블로그 포스트"
    - "소셜 포스트"
    - "Product Hunt, BetaList, Hacker News 등"
```

---

## Product Hunt Launch Strategy

### 장단점

```yaml
product_hunt:
  pros:
    - "테크 얼리어답터 청중에 노출"
    - "신뢰도 상승 (Product of the Day 선정 시)"
    - "PR 커버리지 및 백링크 가능"
  cons:
    - "랭킹 경쟁 치열"
    - "트래픽 스파이크 단기적"
    - "상당한 사전 준비 필요"
```

### 런칭 전 준비

```yaml
pre_launch:
  - "영향력 있는 서포터, 콘텐츠 허브, 커뮤니티와 관계 구축"
  - "리스팅 최적화: 매력적 태그라인, 세련된 비주얼, 짧은 데모 영상"
  - "성공 런칭 사례 연구"
  - "관련 커뮤니티에서 먼저 가치 제공 (피칭 전에)"
  - "팀 전원 종일 참여 준비"
```

### 런칭 당일

```yaml
launch_day:
  - "종일 이벤트로 취급"
  - "모든 댓글에 실시간 응답"
  - "질문 답변 및 토론 유도"
  - "기존 청중에게 참여 독려"
  - "트래픽을 사이트로 유도하여 가입 전환"
```

### 런칭 후

```yaml
post_launch:
  - "참여한 모든 사람에게 팔로업"
  - "PH 트래픽을 Owned 관계로 전환 (이메일 구독)"
  - "포스트 런칭 콘텐츠로 모멘텀 지속"
```

---

## Post-Launch 모멘텀 전략

런칭 발표가 나간 후에도 끝이 아닙니다. 지속적인 모멘텀이 핵심입니다.

### 즉각적 액션

```yaml
immediate_post_launch:
  educate_new_users: "핵심 기능 & 사용 사례 소개 온보딩 이메일 시퀀스 셋업"
  reinforce_launch: "주간/격주/월간 라운드업 이메일에 발표 포함"
  differentiate: "비교 페이지 발행 (왜 우리가 명확한 선택인지)"
  update_web: "새 기능/제품에 대한 전용 섹션 웹사이트에 추가"
  offer_preview: "노코드 인터랙티브 데모 (Navattic 등) 생성"
```

### 업데이트별 마케팅 강도

| 업데이트 유형 | 마케팅 강도 | 채널 |
|-------------|-----------|------|
| **Major** (새 기능, 제품 오버홀) | 전체 캠페인 | 블로그, 이메일, 인앱, 소셜 |
| **Medium** (인테그레이션, UI 개선) | 타겟 발표 | 관련 세그먼트 이메일, 인앱 배너 |
| **Minor** (버그 픽스, 소소한 개선) | 체인지로그 | 릴리스 노트 |

### 핵심 원칙

```
• 릴리스를 분산하여 모멘텀 유지 (한꺼번에 X)
• 이전 발표에서 효과적이었던 전술 재사용
• 작은 체인지로그 업데이트도 "제품이 발전 중" 신호
• 기존 모멘텀에 올라타는 것이 새로 시작하는 것보다 쉬움
```

<!-- End of merged content from coreyhaines31/marketingskills -->

---

## 다음 스킬 연결

- **Funnel Skill**: 캠페인 퍼널 상세 설계
- **Copywriting Skill**: 캠페인 카피 제작 (숏폼 스크립트 포함)
- **Ads Creative Skill**: 광고 에셋 제작
- **A/B Testing Skill**: 테스트 설계

---

*좋은 캠페인은 명확한 목표에서 시작합니다.*
*"무엇을 달성하고 싶은가?"에 SMART하게 답할 수 있어야 합니다.*
*2025년엔 "어떻게 참여하게 만들 것인가?"도 함께 고민하세요.*
