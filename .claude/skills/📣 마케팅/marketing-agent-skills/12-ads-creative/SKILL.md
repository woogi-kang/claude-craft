---
name: mkt-ads-creative
description: |
  광고 플랫폼별 크리에이티브 제작.
  Google, Meta, LinkedIn 광고 카피와 규격을 제공합니다.
triggers:
  - "광고 카피"
  - "Google Ads"
  - "Facebook 광고"
  - "LinkedIn 광고"
input:
  - context/{project}-context.md
  - copy/*.md
  - personas/*.md
output:
  - ads/google-ads.md
  - ads/meta-ads.md
  - ads/linkedin-ads.md
---

# Ads Creative Skill

플랫폼별 광고 크리에이티브를 제작합니다.

## 플랫폼별 규격

### Google Ads

```yaml
google_ads:
  search:
    headlines:
      count: 15
      max_length: 30자
    descriptions:
      count: 4
      max_length: 90자
    display_url:
      path1: 15자
      path2: 15자

  responsive_display:
    headlines:
      short: 25자
      long: 90자
    descriptions: 90자
    images:
      landscape: "1200x628"
      square: "1200x1200"
      logo: "1200x1200"

  youtube:
    bumper:
      duration: "6초"
    skippable:
      duration: "15-60초"
    non_skippable:
      duration: "15초"
```

### Meta Ads (Facebook/Instagram)

```yaml
meta_ads:
  feed:
    primary_text: 125자 (권장), 최대 무제한
    headline: 27자 (권장)
    description: 27자 (권장)
    image:
      ratio: "1:1 또는 4:5"
      size: "1080x1080 또는 1080x1350"
    video:
      ratio: "1:1, 4:5, 16:9"
      duration: "15초 권장"

  stories:
    text: "최소화"
    ratio: "9:16"
    size: "1080x1920"
    duration: "15초"

  reels:
    ratio: "9:16"
    duration: "15-30초"
```

### LinkedIn Ads

```yaml
linkedin_ads:
  single_image:
    intro_text: 150자 (권장)
    headline: 70자
    description: 100자
    image: "1200x627"

  carousel:
    intro_text: 150자
    cards: 2-10장
    card_headline: 45자
    image: "1080x1080"

  video:
    intro_text: 150자
    headline: 70자
    duration: "15초-3분"
    ratio: "16:9, 1:1, 9:16"

  text_ad:
    headline: 25자
    description: 75자
```

## 광고 카피 프레임워크

### Hook → Value → CTA

```
Hook: 주의를 끄는 첫 문장
Value: 핵심 혜택/제안
CTA: 행동 유도
```

### Problem → Solution → Proof

```
Problem: 고객의 문제 언급
Solution: 우리 제품이 해결
Proof: 증거 (숫자, 후기)
```

## 워크플로우

```
1. 플랫폼 & 캠페인 목표 확인
      │
      ▼
2. 타겟 오디언스 확인
      │
      ▼
3. 규격에 맞는 카피 작성
      │
      ▼
4. 변형 버전 생성 (A/B 테스트용)
      │
      ▼
5. 플랫폼별 문서 저장
   → workspace/work-marketing/ads/*.md
```

## 출력 템플릿

### google-ads.md

```markdown
# {Project Name} Google Ads

## Campaign Info

| 항목 | 내용 |
|------|------|
| 캠페인 목표 | {goal} |
| 타겟 키워드 | {keywords} |
| 랜딩페이지 | {landing_url} |
| 일 예산 | {budget} |

---

## Search Ads (반응형 검색 광고)

### Ad Group 1: {theme}

**Keywords**: {keyword_list}

#### Headlines (30자 이하)

| # | Headline | 글자 수 | 유형 |
|---|----------|--------|------|
| 1 | {headline_1} | {count} | 브랜드 |
| 2 | {headline_2} | {count} | 혜택 |
| 3 | {headline_3} | {count} | 기능 |
| 4 | {headline_4} | {count} | CTA |
| 5 | {headline_5} | {count} | 숫자 |
| 6 | {headline_6} | {count} | 질문 |
| 7 | {headline_7} | {count} | 긴급 |
| 8 | {headline_8} | {count} | 가격 |
| ... | ... | ... | ... |

#### Descriptions (90자 이하)

| # | Description | 글자 수 |
|---|-------------|--------|
| 1 | {desc_1} | {count} |
| 2 | {desc_2} | {count} |
| 3 | {desc_3} | {count} |
| 4 | {desc_4} | {count} |

#### Display Path

```
{domain}.com/{path1}/{path2}
```

#### Preview

```
{headline_1} | {headline_2} | {headline_3}
{display_url}
{description_1}
```

---

### Ad Group 2: {theme}

(동일 형식)

---

## Performance Max / Display

### Responsive Display Ad

#### Short Headlines (25자)

1. {short_headline_1}
2. {short_headline_2}
3. {short_headline_3}

#### Long Headlines (90자)

1. {long_headline_1}
2. {long_headline_2}

#### Descriptions (90자)

1. {description_1}
2. {description_2}

#### Image Requirements

| 유형 | 규격 | 용도 |
|------|------|------|
| Landscape | 1200x628 | 메인 |
| Square | 1200x1200 | 피드 |
| Logo | 1200x1200 | 브랜딩 |

---

## Keyword Strategy

### Primary Keywords

| 키워드 | 검색량 | 경쟁 | 입찰가 |
|--------|--------|------|--------|
| {keyword_1} | {volume} | {competition} | {bid} |
| {keyword_2} | {volume} | {competition} | {bid} |

### Negative Keywords

- {negative_1}
- {negative_2}
- {negative_3}
```

### meta-ads.md

```markdown
# {Project Name} Meta Ads

## Campaign Info

| 항목 | 내용 |
|------|------|
| 캠페인 목표 | {goal} |
| 타겟 | {target} |
| 랜딩페이지 | {landing_url} |
| 일 예산 | {budget} |
| 플랫폼 | Facebook / Instagram |

---

## Feed Ads

### Ad Set 1: {theme}

#### Version A

**Primary Text** (125자 권장)
```
{primary_text}
```

**Headline** (27자)
```
{headline}
```

**Description** (27자)
```
{description}
```

**CTA Button**: {cta_button}

**Image/Video Spec**:
- 비율: 1:1 (1080x1080)
- 형식: {image/video}

---

#### Version B (A/B Test)

**Primary Text**
```
{primary_text_b}
```

**Headline**
```
{headline_b}
```

---

### Ad Set 2: {theme}

(동일 형식)

---

## Stories/Reels Ads

### Story Ad 1

**Text Overlay** (최소화)
```
{text_overlay}
```

**CTA**: {cta}

**Spec**:
- 비율: 9:16 (1080x1920)
- 길이: 15초

---

## Carousel Ads

### Carousel 1: {theme}

**Primary Text**
```
{intro_text}
```

| 카드 | 이미지 | 헤드라인 | 설명 | 링크 |
|------|--------|---------|------|------|
| 1 | {desc} | {headline} | {desc} | {url} |
| 2 | {desc} | {headline} | {desc} | {url} |
| 3 | {desc} | {headline} | {desc} | {url} |

---

## Audience Targeting

### Core Audience

| 항목 | 설정 |
|------|------|
| 연령 | {age_range} |
| 성별 | {gender} |
| 위치 | {location} |
| 관심사 | {interests} |
| 행동 | {behaviors} |

### Custom Audiences

- [ ] 웹사이트 방문자
- [ ] 이메일 리스트
- [ ] 앱 사용자
- [ ] 참여 사용자

### Lookalike Audiences

- [ ] 구매자 유사
- [ ] 가입자 유사
```

### linkedin-ads.md

```markdown
# {Project Name} LinkedIn Ads

## Campaign Info

| 항목 | 내용 |
|------|------|
| 캠페인 목표 | {goal} |
| 타겟 | {target} |
| 랜딩페이지 | {landing_url} |
| 일 예산 | {budget} |

---

## Sponsored Content

### Single Image Ad 1

**Intro Text** (150자 권장)
```
{intro_text}
```

**Headline** (70자)
```
{headline}
```

**Description** (100자)
```
{description}
```

**CTA Button**: {cta_button}

**Image**: 1200x627

---

### Single Image Ad 2 (A/B)

(동일 형식)

---

## Carousel Ads

### Carousel 1

**Intro Text**
```
{intro_text}
```

| 카드 | 헤드라인 (45자) | 이미지 |
|------|----------------|--------|
| 1 | {headline_1} | 1080x1080 |
| 2 | {headline_2} | 1080x1080 |
| 3 | {headline_3} | 1080x1080 |

---

## Video Ads

### Video Ad 1

**Intro Text**
```
{intro_text}
```

**Headline** (70자)
```
{headline}
```

**Video Spec**:
- 비율: 16:9 또는 1:1
- 길이: 15-30초 권장
- 자막: 필수

---

## Text Ads

### Text Ad 1

**Headline** (25자)
```
{headline}
```

**Description** (75자)
```
{description}
```

---

## Targeting

### Professional Targeting

| 항목 | 설정 |
|------|------|
| 직책 | {job_titles} |
| 직군 | {job_functions} |
| 산업 | {industries} |
| 회사 규모 | {company_size} |
| 경력 | {seniority} |

### Account-Based Marketing (ABM)

| 회사 | 규모 | 산업 |
|------|------|------|
| {company_1} | {size} | {industry} |
| {company_2} | {size} | {industry} |
```

## 광고 카피 팁

### 플랫폼별 톤

```yaml
google_search:
  tone: "직접적, 키워드 포함"
  focus: "검색 의도 매칭"

meta:
  tone: "대화적, 감성적"
  focus: "스토리텔링, 비주얼"

linkedin:
  tone: "전문적, 신뢰"
  focus: "비즈니스 가치, B2B"
```

### 모바일 우선

```
✅ 짧은 문장
✅ 큰 CTA 버튼
✅ 세로 비디오 (9:16)
✅ 첫 3초에 핵심
```

<!-- Merged from coreyhaines31/marketingskills -->

## TikTok Ads 규격

```yaml
tiktok_ads:
  ad_text:
    recommended: 80자
    max: 100자
    note: "비디오 위에 표시"

  display_name:
    max: 40자
    note: "브랜드 이름"

  video_specs:
    aspect_ratio: ["9:16", "1:1", "16:9"]
    resolution_min: "540x960 (9:16)"
    duration: "5-60초 (권장 15-30초)"
    file_size_max: "500MB"
    format: ["mp4", "mov", "mpeg"]

  format_types:
    in_feed: "For You 페이지에 표시되는 네이티브 광고"
    top_view: "앱 오픈 시 첫 번째 광고"
    branded_hashtag: "해시태그 챌린지 캠페인"
    branded_effect: "브랜드 AR 필터/스티커"

  best_practices:
    - "네이티브 느낌의 콘텐츠가 폴리시된 광고보다 효과적"
    - "처음 3초에 훅 필수"
    - "세로(9:16) 형식 우선"
    - "트렌드 사운드 활용"
    - "자막 필수 (85%가 무음으로 시청)"
```

---

## Twitter/X Ads 규격

```yaml
twitter_x_ads:
  tweet_text:
    max: 280자
    note: "광고 카피 본문"

  card_headline:
    max: 70자
    note: "카드 헤드라인"

  card_description:
    max: 200자
    note: "카드 설명"

  image_specs:
    single_image:
      ratio: "1.91:1"
      size: "1200x628"
    carousel:
      ratio: "1:1"
      size: "800x800"

  video_specs:
    duration: "최대 2분 20초 (권장 15초)"
    file_size_max: "1GB"
    ratio: ["16:9", "1:1"]

  ad_formats:
    promoted_ads: "일반 트윗 형태의 프로모션"
    follower_ads: "팔로워 확보 광고"
    amplify: "프리미엄 비디오 콘텐츠 내 광고"
    takeover:
      timeline: "타임라인 최상단"
      trend: "트렌딩 탭"
```

---

## Campaign Architecture (캠페인 구조)

광고 계정의 체계적 구조화는 효율적인 운영과 최적화의 기반입니다.

### 계정 구조

```
Account
├── Campaign 1: [목표] - [오디언스/제품]
│   ├── Ad Set 1: [타겟팅 변형]
│   │   ├── Ad 1: [크리에이티브 A]
│   │   ├── Ad 2: [크리에이티브 B]
│   │   └── Ad 3: [크리에이티브 C]
│   └── Ad Set 2: [타겟팅 변형]
└── Campaign 2...
```

### 네이밍 컨벤션

```
[Platform]_[Objective]_[Audience]_[Offer]_[Date]

예시:
META_Conv_Lookalike-Customers_FreeTrial_2024Q1
GOOG_Search_Brand_Demo_Ongoing
LI_LeadGen_CMOs-SaaS_Whitepaper_Mar24
TIKTOK_Traffic_GenZ_AppInstall_2024Q2
```

### 캠페인 유형별 설정

```yaml
campaign_types:
  awareness:
    objective: "도달, 브랜드 인지"
    bidding: "CPM 타겟"
    primary_kpi: "CPM, Reach, Video View Rate"

  consideration:
    objective: "트래픽, 참여, 리드"
    bidding: "CPC 또는 CPL 타겟"
    primary_kpi: "CTR, CPC, Time on Site"

  conversion:
    objective: "전환, 구매, 가입"
    bidding: "CPA 또는 ROAS 타겟"
    primary_kpi: "CPA, ROAS, Conversion Rate"
```

---

## Budget Optimization & Scaling Framework

### 스케일링 판단 기준

```yaml
scaling_criteria:
  when_to_increase:
    - "CPA가 타겟 이하로 안정적 (최소 3-5일)"
    - "50건 이상의 전환 데이터 확보"
    - "학습 기간 완료 (알고리즘이 안정화)"

  how_to_increase:
    incremental: "20-30%씩 점진적 증가"
    wait_period: "증가 후 3-5일 대기 (알고리즘 재학습)"
    never: "한 번에 2배 이상 증가하지 않음"
```

### Diminishing Returns (수확 체감)

```
Budget Increase vs Performance
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
       Performance
    ●
   ●│
  ● │        ← Sweet Spot
 ●  │    ●
●   │        ●
    │              ●     ← Diminishing Returns
    │                    ●
    └──────────────────────── Budget
```

```yaml
diminishing_returns_signals:
  - "CPA가 타겟 대비 20%+ 증가"
  - "CTR 하락"
  - "빈도(Frequency)가 3+ 초과"
  - "동일 오디언스 내 도달 포화"

mitigation:
  - "새 오디언스 세그먼트 탐색"
  - "새 크리에이티브로 교체"
  - "새 플랫폼 테스트"
  - "예산을 다른 고성과 캠페인으로 재배분"
```

### 테스팅 vs 스케일링 예산 배분

```yaml
budget_allocation:
  testing_phase:                  # 첫 2-4주
    proven_campaigns: "70%"
    testing_new: "30%"

  scaling_phase:                  # 데이터 확보 후
    top_performers: "80%"
    testing: "20%"
```

---

## Attribution Modeling (기여도 모델)

어떤 터치포인트가 전환에 기여했는지 파악하는 프레임워크입니다.

### 모델 유형

| 모델 | 설명 | 적합한 경우 |
|------|------|-----------|
| **Last-Click** | 마지막 클릭에 100% 기여 | 단순한 퍼널, 빠른 의사결정 |
| **First-Click** | 첫 클릭에 100% 기여 | 인지도 캠페인 평가 |
| **Linear** | 모든 터치포인트에 균등 배분 | 여러 채널이 균등하게 기여할 때 |
| **Time-Decay** | 전환에 가까울수록 더 높은 기여 | 긴 세일즈 사이클 |
| **Data-Driven** | 실제 데이터 기반 기여도 산정 | 충분한 전환 데이터 (300건+) |

### 실무 가이드

```yaml
attribution_best_practices:
  - "플랫폼 자체 기여도는 과대 측정됨 — 항상 GA4와 교차 확인"
  - "UTM 파라미터를 일관성 있게 사용"
  - "Blended CAC (전체 CAC) 확인이 플랫폼별 CPA보다 중요"
  - "전환 윈도우 설정 통일 (7일 클릭 + 1일 뷰 등)"
  - "점진적 A/B (지역별 on/off)로 진짜 영향 측정"
```

---

## Performance Iteration Workflow (성과 기반 반복)

기존 광고 성과 데이터를 기반으로 체계적으로 크리에이티브를 개선합니다.

### 반복 루프

```
Pull Performance Data
        │
        ▼
Analyze Winners (CTR, Conv Rate, ROAS 기준)
        │
        ├─ 승리 테마 파악 (어떤 주제/앵글이 효과적?)
        ├─ 승리 구조 파악 (질문? 명령? 숫자?)
        └─ 패배 패턴 파악 (어떤 앵글이 무효?)
        │
        ▼
Generate Variations
        │
        ├─ 승리 테마 강화 (새로운 표현으로)
        ├─ 승리 앵글을 새 변형으로 확장
        ├─ 1-2개 미탐색 앵글 테스트
        └─ 패배 패턴 회피
        │
        ▼
Validate Against Specs → Upload → Repeat
```

### Iteration Log 템플릿

```markdown
## Iteration Log
- Round: {number}
- Date: {date}
- Top performers: {list with metrics}
- Winning patterns: {summary}
- New variations: {count} headlines, {count} descriptions
- New angles being tested: {list}
- Angles retired: {list}
```

### 주의사항

```yaml
iteration_rules:
  - "한 번에 하나의 변수만 테스트"
  - "1,000+ 노출 전에 크리에이티브 판단하지 않기"
  - "직감보다 데이터 기반 결정"
  - "승리 크리에이티브도 2-4주마다 새로 고침 (광고 피로)"
```

<!-- End of merged content from coreyhaines31/marketingskills -->

---

## 다음 스킬 연결

- **A/B Testing Skill**: 광고 테스트 설계
- **Analytics KPI Skill**: 광고 성과 측정
- **Landing Page Skill**: 광고와 LP 연결

---

*좋은 광고는 "보여주는 것"이 아니라 "멈추게 하는 것"입니다.*
*스크롤을 멈추게 만드세요.*
