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

## 다음 스킬 연결

- **A/B Testing Skill**: 광고 테스트 설계
- **Analytics KPI Skill**: 광고 성과 측정
- **Landing Page Skill**: 광고와 LP 연결

---

*좋은 광고는 "보여주는 것"이 아니라 "멈추게 하는 것"입니다.*
*스크롤을 멈추게 만드세요.*
