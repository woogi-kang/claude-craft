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

## 다음 단계

전략 수립 완료 후:
1. → `1-research`: 트렌드 및 소재 리서치
2. → `4-content`: 플랫폼별 콘텐츠 작성
3. → `8-schedule`: 콘텐츠 캘린더 수립
