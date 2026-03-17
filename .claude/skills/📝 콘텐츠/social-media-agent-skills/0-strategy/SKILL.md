---
name: social-strategy
description: |
  소셜미디어 콘텐츠 전략을 수립합니다.

  활성화 조건:
  - "소셜미디어 전략 세워줘"
  - "콘텐츠 전략 수립해줘"
  - "브랜드 보이스 정의해줘"
  - "타겟 오디언스 분석해줘"
  - "콘텐츠 필러 만들어줘"
---

# 0. Strategy: 콘텐츠 전략 수립

## 핵심 기능

### 1. brand_voice_analysis: 브랜드 보이스 정의

브랜드의 톤앤매너와 커뮤니케이션 스타일을 정의합니다.

```yaml
brand_voice:
  personality:
    - 형용사 3-5개 (예: 친근한, 전문적인, 유머러스한)
  tone_spectrum:
    formal: 1-10  # 1=매우 캐주얼, 10=매우 격식
    serious: 1-10  # 1=유머러스, 10=진지함
    enthusiastic: 1-10  # 1=차분함, 10=열정적
  language_style:
    - 사용할 표현 (예: "~해요" vs "~합니다")
    - 피할 표현 (예: 업계 전문용어, 비속어)
  emoji_usage:
    level: none | minimal | moderate | heavy
    preferred: ["🚀", "💡", "✨"]
    avoided: ["🔥", "💯"]
```

### 2. audience_persona: 타겟 오디언스 페르소나

```yaml
persona:
  name: "마케터 민지"
  demographics:
    age_range: "28-35"
    occupation: "스타트업 마케팅 담당자"
    location: "서울/수도권"
  psychographics:
    goals:
      - "최신 마케팅 트렌드 파악"
      - "실무에 바로 적용 가능한 팁"
    pain_points:
      - "시간 부족"
      - "정보 과부하"
    content_preferences:
      - "짧고 핵심적인 인사이트"
      - "실제 사례 중심"
  platform_behavior:
    instagram: "점심시간, 퇴근 후 브라우징"
    linkedin: "출근길, 업무 중 체크"
    x: "실시간 트렌드 확인"
    threads: "가벼운 소통"
```

### 3. content_pillar: 콘텐츠 주제 카테고리

콘텐츠의 일관성과 다양성을 위한 주제 카테고리를 정의합니다.

```yaml
content_pillars:
  - name: "교육/인사이트"
    percentage: 40%
    examples:
      - "업계 트렌드 분석"
      - "How-to 가이드"
      - "팁 & 트릭"

  - name: "브랜드 스토리"
    percentage: 25%
    examples:
      - "비하인드 씬"
      - "팀 소개"
      - "마일스톤 공유"

  - name: "커뮤니티 참여"
    percentage: 20%
    examples:
      - "Q&A"
      - "투표/설문"
      - "UGC 리포스트"

  - name: "프로모션"
    percentage: 15%
    examples:
      - "제품/서비스 소개"
      - "이벤트 안내"
      - "CTA"
```

### 4. platform_selection: 플랫폼 전략

목적과 리소스에 따른 플랫폼 우선순위를 결정합니다.

| 목적 | 1순위 | 2순위 | 3순위 |
|------|-------|-------|-------|
| 브랜드 인지도 | Instagram | X | Threads |
| B2B 리드 생성 | LinkedIn | X | - |
| 커뮤니티 구축 | Threads | Instagram | X |
| 바이럴/트렌드 | X | Threads | Instagram |
| 비주얼 스토리텔링 | Instagram | LinkedIn | - |

```yaml
platform_priority:
  primary: "instagram"
  secondary: "linkedin"
  experimental: "threads"

resource_allocation:
  instagram: 40%
  linkedin: 35%
  x: 15%
  threads: 10%
```

## 전략 문서 템플릿

```markdown
# [브랜드명] 소셜미디어 전략

## 1. 목표 (Objectives)
- 주요 KPI: [팔로워 증가율 / 참여율 / 전환율]
- 목표 수치: [구체적 숫자]
- 기간: [분기/반기/연간]

## 2. 브랜드 보이스
- 핵심 키워드: [3-5개]
- 톤앤매너: [설명]
- DO: [할 것]
- DON'T: [하지 말 것]

## 3. 타겟 오디언스
- 주요 페르소나: [이름/특성]
- 니즈: [리스트]
- 선호 콘텐츠: [유형]

## 4. 콘텐츠 필러
| 필러 | 비율 | 예시 |
|------|------|------|
| ... | ...% | ... |

## 5. 플랫폼별 전략
### Instagram
- 콘텐츠 유형: [피드/릴스/스토리 비율]
- 발행 빈도: [주 N회]
- 핵심 목표: [...]

### LinkedIn
- 콘텐츠 유형: [...]
- 발행 빈도: [...]
- 핵심 목표: [...]

## 6. 콘텐츠 캘린더 개요
- 월간 테마: [...]
- 정기 시리즈: [...]
- 시즌 캠페인: [...]
```

## 경쟁사 분석 프레임워크

```yaml
competitor_analysis:
  competitor_name: "경쟁사 A"
  platforms:
    instagram:
      followers: 50000
      posting_frequency: "주 5회"
      content_types: ["캐러셀", "릴스"]
      engagement_rate: "3.2%"
      top_performing:
        - "교육 콘텐츠"
        - "비하인드 씬"
      gaps:
        - "커뮤니티 참여 부족"
        - "스토리 미활용"
```

## 🌏 글로벌 확장 (Global Expansion)

### 글로벌 플랫폼 전략

| 목적 | 1순위 | 2순위 | 3순위 |
|------|-------|-------|-------|
| 글로벌 바이럴 | TikTok | YouTube Shorts | Instagram Reels |
| 글로벌 커뮤니티 | Reddit | Discord | TikTok |
| 비주얼 디스커버리 | Pinterest | Instagram | TikTok |
| 영상 SEO | YouTube | TikTok | - |
| B2B 글로벌 | LinkedIn | X | Reddit |

```yaml
global_platform_priority:
  tiktok:
    strength: "알고리즘 기반 콘텐츠 디스커버리, 팔로워 0에서도 바이럴 가능"
    audience: "Gen Z + Millennial 글로벌"
    content: "숏폼 비디오 (15s-10min)"
    posting: "1-3회/일"

  reddit:
    strength: "깊은 커뮤니티 참여, 닛치 타겟팅"
    audience: "테크, 비즈니스, 취미 커뮤니티"
    content: "텍스트 포스트, AMA, 가이드"
    caution: "노골적 프로모션 = 다운보트"

  pinterest:
    strength: "영감 기반 검색, 긴 콘텐츠 수명 (2-6개월)"
    audience: "라이프스타일, DIY, 비주얼 중심"
    content: "핀 이미지 (2:3), 아이디어 핀"
    posting: "3-10핀/일"

  youtube:
    strength: "세계 2위 검색엔진, 장기 트래픽"
    audience: "전 연령대, 글로벌"
    content: "Long-form + Shorts"
    posting: "1-2회/주 (Long), 3-5회/주 (Shorts)"
```

### 멀티마켓 타겟팅 가이드

```yaml
multi_market_targeting:
  korean_domestic:
    description: "한국 시장 집중"
    platforms: [Instagram, 네이버블로그, KakaoTalk, X]
    language: "한국어"
    tone: "친근한 반말체 또는 존댓말"
    hashtags: "한국어 해시태그 위주"
    timezone: "KST"

  english_global:
    description: "영어권 글로벌 시장"
    platforms: [TikTok, Instagram, X, Reddit, YouTube, Pinterest]
    language: "English"
    tone: "Conversational, authentic"
    hashtags: "영어 해시태그 위주"
    timezone: "UTC 기준, EST/PST 최적화"

  dual_market:
    description: "한국 + 글로벌 동시 운영"
    strategy: |
      - 별도 계정 운영 권장 (혼합 시 팔로워 혼란)
      - 핵심 콘텐츠는 양쪽 언어로 제작
      - 플랫폼별 주력 시장 지정
        예: Instagram KR = 한국, TikTok = 글로벌
      - 문화적 맥락에 맞게 적응 (단순 번역 X)
    content_ratio:
      korean_only: "30% (한국 고유 시즌/트렌드)"
      english_only: "30% (글로벌 트렌드)"
      bilingual: "40% (양쪽 공통 주제)"
```

### 글로벌 오디언스 페르소나 예시

```yaml
global_persona:
  name: "Alex the Indie Maker"
  demographics:
    age_range: "25-35"
    occupation: "Indie developer / Startup founder"
    location: "US, EU, Global remote"
  psychographics:
    goals:
      - "Learn growth tactics for side projects"
      - "Find practical, no-BS marketing tips"
    pain_points:
      - "Limited budget"
      - "Information overload"
    content_preferences:
      - "Short, actionable tips"
      - "Real case studies with numbers"
  platform_behavior:
    tiktok: "Scroll during breaks, discover new tools"
    reddit: "Deep dive research, community Q&A"
    x: "Industry news, hot takes"
    youtube: "Tutorials, reviews"
```

### 글로벌 전략 문서 추가 섹션

```markdown
### TikTok
- 콘텐츠 유형: [트렌드 참여/튜토리얼/비하인드 비율]
- 발행 빈도: [일 N회]
- 핵심 목표: [...]

### Reddit
- 주요 서브레딧: [리스트]
- 콘텐츠 유형: [가치 제공 포스트/AMA/가이드]
- 핵심 목표: [커뮤니티 신뢰/트래픽]

### Pinterest
- 보드 구성: [카테고리별]
- 핀 빈도: [일 N회]
- 핵심 목표: [검색 트래픽/영감]

### YouTube
- 콘텐츠 유형: [Long-form/Shorts 비율]
- 발행 빈도: [주 N회]
- 핵심 목표: [SEO/구독자]
```

## 다음 단계

전략 수립 완료 후:
1. → `1-research`: 트렌드 및 소재 리서치
2. → `4-content`: 플랫폼별 콘텐츠 작성
3. → `8-schedule`: 콘텐츠 캘린더 수립
