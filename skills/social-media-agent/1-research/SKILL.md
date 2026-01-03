---
name: social-research
description: |
  소셜미디어 콘텐츠를 위한 트렌드와 소재를 리서치합니다.

  활성화 조건:
  - "트렌드 조사해줘"
  - "소재 리서치해줘"
  - "경쟁사 분석해줘"
  - "바이럴 콘텐츠 분석"
  - "인기 주제 찾아줘"
---

# 1. Research: 트렌드 & 소재 리서치

## 핵심 기능

### 1. trend_monitoring: 실시간 트렌드 분석

```yaml
trend_sources:
  global:
    - Google Trends (검색 트렌드)
    - X Trending Topics
    - TikTok Discover
    - Reddit r/popular

  korea:
    - 네이버 실시간 검색어
    - 다음 실시간 이슈
    - 트위터 코리아 트렌드
    - 디시인사이드 실시간 베스트

  industry:
    - 업계 뉴스 피드
    - 전문 블로그/미디어
    - 컨퍼런스/이벤트 발표
    - 경쟁사 동향

trend_categories:
  - seasonal: "계절/시즌 트렌드"
  - cultural: "문화/사회 트렌드"
  - industry: "산업별 트렌드"
  - platform: "플랫폼 고유 트렌드"
  - viral: "바이럴/밈 트렌드"
```

### 2. competitor_watch: 경쟁사 콘텐츠 분석

```yaml
competitor_analysis:
  content_audit:
    - 발행 빈도
    - 콘텐츠 유형 (비율)
    - 인기 콘텐츠 패턴
    - 참여율 벤치마크
    - 해시태그 전략
    - 발행 시간대

  performance_metrics:
    instagram:
      - 좋아요 평균
      - 댓글 평균
      - 저장 추정치
      - 릴스 vs 피드 성과

    linkedin:
      - 반응(리액션) 평균
      - 댓글 깊이
      - 공유 수

    x:
      - 리트윗 평균
      - 인용 트윗 비율
      - 답글 수

    threads:
      - 답글 수
      - 리포스트 수

  template:
    competitor: "[경쟁사명]"
    platform: "instagram"
    followers: 50000
    posting_frequency: "주 5회"
    top_content:
      - type: "carousel"
        topic: "업계 팁"
        engagement: 5.2%
      - type: "reel"
        topic: "비하인드씬"
        engagement: 8.1%
    content_mix:
      educational: 40%
      promotional: 20%
      entertainment: 25%
      community: 15%
    gaps:
      - "스토리 활용 부족"
      - "UGC 리포스트 없음"
```

### 3. viral_pattern: 바이럴 콘텐츠 패턴 분석

```yaml
viral_analysis:
  elements_to_identify:
    hook: "첫 문장/장면의 특징"
    emotion: "유발하는 감정"
    format: "콘텐츠 형식"
    timing: "발행 타이밍"
    cta: "참여 유도 방식"

  common_patterns:
    controversy: |
      - 기존 통념 반박
      - 논쟁 유발 의견
      - "인기 없는 의견" 프레이밍

    relatability: |
      - 공감 가능한 경험
      - "나도 그래" 반응
      - 보편적 고민/상황

    utility: |
      - 바로 적용 가능한 팁
      - 저장할 가치
      - 공유하고 싶은 정보

    surprise: |
      - 예상 밖의 결과
      - 반전 스토리
      - 충격적인 통계

    humor: |
      - 상황 코미디
      - 자기비하 유머
      - 밈 활용
```

### 4. topic_clustering: 주제 확장

```yaml
topic_expansion:
  method: |
    핵심 주제에서 관련 주제로 확장

  example:
    core_topic: "재택근무"
    expanded_topics:
      - "홈오피스 셋업"
      - "재택근무 생산성"
      - "비동기 커뮤니케이션"
      - "원격 팀 빌딩"
      - "워라밸"
      - "디지털 노마드"
      - "하이브리드 근무"

  content_angles:
    how_to: "[주제] 하는 방법"
    mistakes: "[주제]에서 하는 실수"
    myths: "[주제]에 대한 오해"
    trends: "[주제] 최신 트렌드"
    tools: "[주제]를 위한 도구"
    case_study: "[주제] 성공 사례"
    comparison: "A vs B 비교"
    predictions: "[주제]의 미래"
```

### 5. content_calendar_ideas: 콘텐츠 아이디어 생성

```yaml
idea_generation:
  frameworks:
    5W1H: |
      - What: 무엇인가?
      - Why: 왜 중요한가?
      - How: 어떻게 하는가?
      - When: 언제 해야 하는가?
      - Where: 어디서 적용되는가?
      - Who: 누구를 위한 것인가?

    pain_point: |
      - 오디언스의 문제 식별
      - 해결책 제시
      - 실패 사례에서 교훈

    question_based: |
      - FAQ 수집
      - 댓글/DM 질문 분석
      - 검색 자동완성 활용

  seasonal_hooks:
    monthly:
      1월: "새해 목표, 신년 계획"
      2월: "설날, 발렌타인"
      3월: "봄 시작, 새 학기"
      4월: "벚꽃, 새로운 시작"
      5월: "어버이날, 가정의 달"
      6월: "여름 준비, 상반기 회고"
      7월: "휴가 시즌, 여름"
      8월: "휴가, 광복절"
      9월: "추석, 가을 시작"
      10월: "할로윈, 독서의 달"
      11월: "빼빼로데이, 수능"
      12월: "연말 정산, 송년, 크리스마스"

    recurring:
      monday: "월요병, 주간 목표"
      friday: "불금, 주간 회고"
      weekend: "휴식, 취미"
```

## 리서치 워크플로우

```
1. 트렌드 스캔
   └─ 플랫폼별 트렌딩 확인
   └─ 뉴스/업계 동향 파악

2. 경쟁사 모니터링
   └─ 최근 인기 콘텐츠 분석
   └─ 새로운 시도 파악

3. 오디언스 리스닝
   └─ 댓글/DM 질문 수집
   └─ 커뮤니티 대화 모니터링

4. 아이디어 브레인스토밍
   └─ 주제 확장
   └─ 각도 다양화

5. 아이디어 검증
   └─ 검색량 확인
   └─ 경쟁 콘텐츠 분석

6. 우선순위 결정
   └─ 적시성 (시즌/트렌드)
   └─ 전략 적합성
   └─ 제작 난이도
```

## 리서치 결과 템플릿

```yaml
research_output:
  date: "2025-01-04"
  topic: "[리서치 주제]"

  trends:
    - trend: "[트렌드 1]"
      source: "Google Trends"
      relevance: "high"
      content_angle: "[콘텐츠 각도]"

  competitor_insights:
    - competitor: "[경쟁사]"
      finding: "[발견 사항]"
      opportunity: "[기회]"

  content_ideas:
    - idea: "[아이디어 1]"
      platform: "instagram"
      format: "carousel"
      priority: "high"
      timing: "이번 주"

    - idea: "[아이디어 2]"
      platform: "linkedin"
      format: "text_post"
      priority: "medium"
      timing: "다음 주"

  sources:
    - url: "[출처 URL]"
      title: "[출처 제목]"
      credibility: "high"
```

## 도구 추천

```yaml
research_tools:
  trend_monitoring:
    - Google Trends (무료)
    - Exploding Topics (유료)
    - SparkToro (유료)

  social_listening:
    - Brandwatch (유료)
    - Mention (유료)
    - 네이버 데이터랩 (무료)

  competitor_analysis:
    - Social Blade (무료/유료)
    - Rival IQ (유료)
    - Socialinsider (유료)

  content_inspiration:
    - BuzzSumo (유료)
    - Feedly (무료/유료)
    - Pinterest Trends (무료)
```

## 다음 단계

리서치 완료 후:
1. → `4-content`: 플랫폼별 콘텐츠 작성
2. → `0-strategy`: 전략 업데이트 (필요시)
3. → `8-schedule`: 콘텐츠 캘린더 반영
