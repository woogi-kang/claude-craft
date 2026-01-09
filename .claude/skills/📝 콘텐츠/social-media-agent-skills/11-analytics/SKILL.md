---
name: social-analytics
description: |
  소셜미디어 콘텐츠 성과를 분석하고 인사이트를 도출합니다.

  활성화 조건:
  - "성과 분석해줘"
  - "인사이트 리포트"
  - "A/B 테스트 결과"
  - "KPI 확인"
  - "콘텐츠 성과 비교"
---

# 11. Analytics: 성과 분석

## 핵심 KPI

### 플랫폼별 주요 지표

```yaml
key_metrics:
  instagram:
    reach:
      - "도달 (Reach)"
      - "노출 (Impressions)"
      - "프로필 방문"
    engagement:
      - "좋아요"
      - "댓글"
      - "저장"
      - "공유"
      - "참여율 (Engagement Rate)"
    growth:
      - "팔로워 증가"
      - "팔로워 증가율"
    content:
      - "릴스 조회수"
      - "릴스 시청 완료율"
      - "스토리 탈출률"

  linkedin:
    reach:
      - "노출 (Impressions)"
      - "고유 뷰"
    engagement:
      - "반응 (Reactions)"
      - "댓글"
      - "공유/리포스트"
      - "참여율"
    growth:
      - "팔로워 증가"
      - "연결 요청"
    content:
      - "클릭률 (CTR)"
      - "체류 시간 (Dwell Time)"

  x:
    reach:
      - "노출 (Impressions)"
      - "도달"
    engagement:
      - "좋아요"
      - "리트윗"
      - "인용 트윗"
      - "답글"
      - "참여율"
    growth:
      - "팔로워 증가"
    content:
      - "링크 클릭"
      - "프로필 방문"
      - "미디어 조회"

  threads:
    engagement:
      - "좋아요"
      - "답글"
      - "리포스트"
      - "인용"
    growth:
      - "팔로워 증가"
    note: "상세 분석 도구 제한적"
```

## 참여율 계산

```yaml
engagement_rate_formulas:
  instagram:
    by_followers: |
      (좋아요 + 댓글 + 저장 + 공유) / 팔로워 수 × 100

    by_reach: |
      (좋아요 + 댓글 + 저장 + 공유) / 도달 × 100

    benchmark:
      excellent: ">6%"
      good: "3-6%"
      average: "1-3%"
      low: "<1%"

  linkedin:
    formula: |
      (반응 + 댓글 + 공유) / 노출 × 100

    benchmark:
      excellent: ">5%"
      good: "2-5%"
      average: "1-2%"
      low: "<1%"

  x:
    formula: |
      (좋아요 + RT + 답글 + 인용) / 노출 × 100

    benchmark:
      excellent: ">2%"
      good: "0.5-2%"
      average: "0.2-0.5%"
      low: "<0.2%"
```

## A/B 테스트 분석

### 테스트 설계

```yaml
ab_test_design:
  variables:
    caption:
      - "훅 (첫 문장)"
      - "CTA 문구"
      - "길이"
      - "이모지 사용"

    visual:
      - "이미지 vs 영상"
      - "색상 톤"
      - "텍스트 오버레이"
      - "얼굴 포함 여부"

    timing:
      - "발행 시간"
      - "발행 요일"

    format:
      - "캐러셀 vs 단일"
      - "릴스 vs 피드"

  test_rules:
    - "한 번에 하나의 변수만 테스트"
    - "충분한 샘플 사이즈 확보"
    - "최소 7일 이상 데이터 수집"
    - "동일 조건 유지 (시간, 타겟 등)"
```

### 테스트 결과 분석

```yaml
ab_test_analysis:
  template:
    test_name: "[테스트명]"
    variable: "[테스트 변수]"
    period: "2025-01-01 ~ 2025-01-07"

    variant_a:
      description: "[변형 A 설명]"
      metrics:
        reach: 10000
        engagement: 500
        engagement_rate: "5.0%"

    variant_b:
      description: "[변형 B 설명]"
      metrics:
        reach: 10200
        engagement: 620
        engagement_rate: "6.1%"

    winner: "Variant B"
    improvement: "+22%"
    confidence: "95%"

    insight: |
      질문형 훅이 진술형보다 22% 높은 참여율을 보였습니다.
      향후 콘텐츠에 질문형 훅을 기본으로 적용 권장합니다.

    next_test: |
      질문 유형별 A/B 테스트 (예/아니오 vs 선택형)
```

## 콘텐츠 성과 분석

### 고성과 콘텐츠 패턴

```yaml
top_performing_analysis:
  method: |
    1. 상위 10% 콘텐츠 식별
    2. 공통 패턴 추출
    3. 재현 가능한 요소 정리

  patterns_to_analyze:
    content:
      - "주제/토픽"
      - "콘텐츠 유형 (교육/스토리/프로모션)"
      - "훅 스타일"
      - "CTA 유형"

    format:
      - "포맷 (캐러셀/릴스/단일)"
      - "길이"
      - "비주얼 스타일"

    timing:
      - "발행 요일"
      - "발행 시간"

    engagement:
      - "첫 1시간 참여 패턴"
      - "댓글 대응 속도"

  output_template:
    period: "2025년 1월"
    top_posts:
      - rank: 1
        id: "IG-2025-0104-001"
        type: "carousel"
        topic: "마케팅 팁"
        engagement_rate: "8.2%"
        success_factors:
          - "질문형 훅"
          - "실용적 팁"
          - "저장 유도 CTA"

    patterns_identified:
      - "캐러셀이 단일 이미지 대비 평균 +40%"
      - "화요일 19:00 발행이 최고 성과"
      - "질문형 훅이 진술형 대비 +25%"
```

### 저성과 콘텐츠 분석

```yaml
low_performing_analysis:
  purpose: "실패에서 배우기"

  questions:
    - "왜 도달이 낮았는가?"
    - "왜 참여가 낮았는가?"
    - "타이밍 문제인가?"
    - "콘텐츠 자체 문제인가?"

  common_issues:
    reach:
      - "알고리즘 변화"
      - "발행 시간 부적절"
      - "해시태그 문제"
      - "외부 링크 포함"

    engagement:
      - "관심 없는 주제"
      - "약한 훅"
      - "CTA 없음"
      - "비주얼 퀄리티 낮음"

    conversion:
      - "CTA 불명확"
      - "랜딩 페이지 문제"
      - "오디언스 미스매치"
```

## 리포트 템플릿

### 주간 리포트

```yaml
weekly_report:
  period: "2025-01-01 ~ 2025-01-07"

  executive_summary: |
    이번 주 총 12개 콘텐츠 발행, 평균 참여율 4.2%로
    전주 대비 +15% 상승했습니다.

    최고 성과: 화요일 캐러셀 (참여율 8.2%)
    개선 필요: 금요일 릴스 (참여율 1.8%)

  metrics_overview:
    total_posts: 12
    total_reach: 45000
    total_engagement: 1890
    avg_engagement_rate: "4.2%"
    follower_change: "+120"

  platform_breakdown:
    instagram:
      posts: 5
      reach: 25000
      engagement_rate: "4.5%"
      top_post: "[링크]"

    linkedin:
      posts: 3
      impressions: 12000
      engagement_rate: "3.8%"
      top_post: "[링크]"

    x:
      posts: 4
      impressions: 8000
      engagement_rate: "2.1%"
      top_post: "[링크]"

  top_3_posts:
    - id: "[ID]"
      platform: "instagram"
      type: "carousel"
      engagement_rate: "8.2%"
      success_factor: "질문형 훅"

  insights:
    - "캐러셀이 릴스보다 +2% 높은 참여율"
    - "화요일 19:00이 최적 발행 시간"
    - "마케팅 팁 주제가 가장 인기"

  next_week_recommendations:
    - "캐러셀 비중 확대 (40% → 50%)"
    - "릴스 훅 강화 필요"
    - "금요일 콘텐츠 주제 변경 고려"
```

### 월간 리포트

```yaml
monthly_report:
  period: "2025년 1월"

  kpi_summary:
    followers:
      start: 10000
      end: 10500
      growth: "+5%"
    avg_engagement_rate: "4.0%"
    total_reach: 180000
    total_engagement: 7200

  goal_progress:
    - goal: "팔로워 10% 증가"
      progress: "50%"
      status: "on_track"

    - goal: "참여율 5% 달성"
      progress: "80%"
      status: "at_risk"

  content_performance:
    by_type:
      carousel: "5.2% 평균"
      reels: "4.8% 평균"
      single: "2.5% 평균"

    by_topic:
      tips: "5.5% 평균"
      story: "4.2% 평균"
      promo: "2.0% 평균"

    by_day:
      best: "화요일 (5.1%)"
      worst: "일요일 (2.3%)"

  competitor_benchmark:
    our_engagement: "4.0%"
    industry_avg: "3.2%"
    status: "Above average"

  recommendations:
    short_term:
      - "릴스 훅 3초 규칙 적용"
      - "일요일 발행 중단"
    long_term:
      - "영상 콘텐츠 역량 강화"
      - "커뮤니티 참여 프로그램 도입"
```

## 분석 도구

```yaml
analytics_tools:
  native:
    instagram: "Instagram Insights"
    linkedin: "LinkedIn Analytics"
    x: "X Analytics"
    threads: "제한적 (좋아요/답글 수만)"

  third_party:
    - name: "Sprout Social"
      features: ["통합 대시보드", "리포트 자동화", "경쟁사 분석"]

    - name: "Hootsuite Analytics"
      features: ["멀티 플랫폼", "커스텀 리포트"]

    - name: "Iconosquare"
      features: ["인스타 특화", "상세 분석"]

    - name: "Socialinsider"
      features: ["경쟁사 벤치마킹", "히스토리 분석"]

  free:
    - "각 플랫폼 네이티브 인사이트"
    - "Google Sheets (수동 트래킹)"
    - "Notion 데이터베이스"
```

## 데이터 트래킹 템플릿

```yaml
tracking_spreadsheet:
  columns:
    - "날짜"
    - "플랫폼"
    - "콘텐츠 ID"
    - "유형 (캐러셀/릴스/단일)"
    - "주제"
    - "훅 유형"
    - "발행 시간"
    - "도달"
    - "노출"
    - "좋아요"
    - "댓글"
    - "저장"
    - "공유"
    - "참여율"
    - "메모"

  review_cycle:
    daily: "주요 지표 체크"
    weekly: "주간 리포트 작성"
    monthly: "월간 분석 및 전략 조정"
    quarterly: "분기 전략 리뷰"
```

## 다음 단계

분석 완료 후:
1. → `0-strategy`: 전략 업데이트
2. → `4-content`: 인사이트 기반 콘텐츠 기획
3. → `8-schedule`: 최적 발행 일정 조정
