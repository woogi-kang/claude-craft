---
name: social-schedule
description: |
  소셜미디어 콘텐츠 발행을 스케줄링합니다.

  활성화 조건:
  - "발행 스케줄 잡아줘"
  - "콘텐츠 캘린더 만들어줘"
  - "최적 발행 시간 알려줘"
  - "스케줄링해줘"
---

# 8. Schedule: 발행 스케줄링

## 플랫폼별 최적 발행 시간

### 한국 기준 (KST)

```yaml
best_times:
  instagram:
    weekday:
      morning: "07:00-09:00 (출근길)"
      lunch: "12:00-13:00"
      evening: "19:00-21:00 (퇴근 후)"
    weekend:
      morning: "10:00-11:00"
      evening: "20:00-22:00"
    best_days: ["화", "수", "목"]
    avoid: "심야 (00:00-06:00)"

  linkedin:
    weekday:
      morning: "07:30-08:30 (출근 전)"
      lunch: "12:00-13:00"
      afternoon: "17:00-18:00 (퇴근 전)"
    weekend: "피하기 권장"
    best_days: ["화", "수", "목"]
    avoid: "금요일 오후, 주말"

  x:
    weekday:
      morning: "09:00-10:00"
      lunch: "12:00-13:00"
      evening: "17:00-18:00"
    weekend:
      morning: "09:00-11:00"
    best_days: ["화", "수", "목"]
    note: "실시간 이슈는 즉시 발행"

  threads:
    weekday:
      lunch: "12:00-14:00"
      evening: "20:00-22:00"
    weekend:
      morning: "10:00-12:00"
      evening: "19:00-21:00"
    note: "캐주얼 플랫폼, 시간 덜 민감"
```

### 글로벌 타겟 시

```yaml
global_timing:
  strategy: "주요 타겟 시간대 기준"

  us_audience:
    est: "09:00-11:00, 14:00-16:00 EST"
    pst: "06:00-08:00, 11:00-13:00 PST"

  overlap_zones:
    korea_us: "22:00-24:00 KST = 09:00-11:00 EST"
    korea_europe: "16:00-18:00 KST = 08:00-10:00 CET"
```

## 발행 빈도 가이드

```yaml
posting_frequency:
  instagram:
    feed:
      optimal: "3-4회/주"
      maximum: "1회/일"
      note: "품질 > 양"
    story:
      optimal: "3-7회/일"
      note: "가볍게, 자주"
    reels:
      optimal: "3-5회/주"
      note: "알고리즘 부스트"

  linkedin:
    optimal: "2-3회/주"
    maximum: "1회/일"
    note: "주말 피하기"

  x:
    optimal: "1-3회/일"
    maximum: "5회/일"
    note: "스레드는 1개로 카운트"

  threads:
    optimal: "1-2회/일"
    note: "대화 참여가 더 중요"

  warning: |
    팔로워 10K 미만 계정이 하루 1회 이상 발행 시
    참여율 50% 하락 가능 (HubSpot 연구)
```

## 콘텐츠 캘린더

### 주간 캘린더 템플릿

```yaml
weekly_calendar:
  monday:
    instagram: "교육 캐러셀"
    linkedin: "인사이트 포스트"
    x: null
    threads: "월요일 질문"

  tuesday:
    instagram: "릴스"
    linkedin: null
    x: "업계 뉴스 코멘트"
    threads: null

  wednesday:
    instagram: "스토리 Q&A"
    linkedin: "케이스 스터디"
    x: "팁 스레드"
    threads: "대화 참여"

  thursday:
    instagram: "피드 포스트"
    linkedin: null
    x: null
    threads: "경험 공유"

  friday:
    instagram: "비하인드 릴스"
    linkedin: "주간 회고"
    x: "주말 질문"
    threads: "불금 포스트"

  saturday:
    instagram: "스토리만"
    linkedin: null
    x: null
    threads: "캐주얼 포스트"

  sunday:
    instagram: "스토리만"
    linkedin: null
    x: null
    threads: null
```

### 월간 테마 플래닝

```yaml
monthly_themes:
  structure:
    week_1: "교육/인사이트 중심"
    week_2: "커뮤니티/참여 중심"
    week_3: "브랜드 스토리 중심"
    week_4: "프로모션/CTA 중심"

  seasonal_events:
    january:
      - "새해 목표"
      - "신년 트렌드"
    february:
      - "설날"
      - "발렌타인"
    # ... (월별 이벤트)

  industry_events:
    - "주요 컨퍼런스"
    - "제품 출시"
    - "기념일"
```

## 배칭 (Batching) 전략

```yaml
content_batching:
  concept: "한 번에 여러 콘텐츠를 제작하여 효율성 극대화"

  schedule:
    weekly_batching:
      day: "금요일 또는 월요일"
      duration: "2-3시간"
      output: "다음 주 콘텐츠 전체"

    monthly_batching:
      day: "월말 하루"
      duration: "풀데이"
      output: "다음 달 핵심 콘텐츠"

  workflow:
    1_planning: |
      - 주제/아이디어 확정
      - 캘린더에 배치
      - 필요 리소스 확인

    2_creation: |
      - 캡션 일괄 작성
      - 비주얼 일괄 제작
      - 해시태그 준비

    3_scheduling: |
      - 스케줄링 도구에 업로드
      - 발행 시간 설정
      - 최종 확인

  benefits:
    - "300% 생산성 증가"
    - "일관된 품질 유지"
    - "시간 절약"
    - "스트레스 감소"
```

## 스케줄링 도구

```yaml
scheduling_tools:
  all_in_one:
    - name: "Hootsuite"
      platforms: "전체"
      features: ["예약", "분석", "팀 협업"]
      price: "$99+/월"

    - name: "Buffer"
      platforms: "전체"
      features: ["예약", "분석", "AI 제안"]
      price: "$6+/월"

    - name: "Later"
      platforms: "전체 (인스타 특화)"
      features: ["비주얼 플래너", "링크인바이오"]
      price: "$25+/월"

  platform_specific:
    instagram:
      - "Meta Business Suite (무료)"
      - "Later"
    linkedin:
      - "LinkedIn 네이티브 예약"
    x:
      - "TweetDeck (무료)"
      - "X Pro"

  free_options:
    - "Meta Business Suite (IG, FB)"
    - "TweetDeck (X)"
    - "LinkedIn 네이티브 예약"
```

## 캘린더 관리 팁

```yaml
calendar_tips:
  color_coding:
    red: "프로모션/세일"
    blue: "교육 콘텐츠"
    green: "커뮤니티/참여"
    yellow: "브랜드 스토리"
    gray: "큐레이션/리포스트"

  buffer_content:
    purpose: "빈 슬롯 채우기용 상시 콘텐츠"
    types:
      - "인용문"
      - "팁 리마인더"
      - "과거 인기 콘텐츠 리포스트"

  flexibility:
    - "20% 슬롯은 실시간 대응용으로 비워두기"
    - "트렌딩 토픽 대응 여유"
    - "긴급 공지 대응"

  review_cycle:
    weekly: "다음 주 콘텐츠 최종 확인"
    monthly: "다음 달 큰 그림 계획"
    quarterly: "전략 점검 및 조정"
```

## 발행 체크리스트

```yaml
pre_publish_checklist:
  content:
    - [ ] 최종 캡션 확인
    - [ ] 오타/문법 재확인
    - [ ] 링크 작동 테스트
    - [ ] 태그/멘션 확인

  visual:
    - [ ] 이미지/영상 업로드 확인
    - [ ] 미리보기 확인
    - [ ] 모바일 화면 테스트

  metadata:
    - [ ] 해시태그 첨부
    - [ ] 위치 태그 (필요시)
    - [ ] Alt 텍스트 (접근성)

  timing:
    - [ ] 발행 시간 재확인
    - [ ] 시간대 확인 (글로벌 타겟시)
    - [ ] 민감한 이슈 없는지 뉴스 체크

post_publish:
  - [ ] 실제 발행 확인
  - [ ] 링크 다시 테스트
  - [ ] 첫 댓글 추가 (해시태그/추가 정보)
  - [ ] 스토리 공유 (인스타그램)
```

## 출력 형식

```yaml
schedule_output:
  week_of: "2025-01-06"

  scheduled_posts:
    - id: "IG-2025-0106-001"
      platform: "instagram"
      type: "carousel"
      publish_time: "2025-01-06 19:00 KST"
      status: "scheduled"
      content_preview: "[첫 줄]..."

    - id: "LI-2025-0107-001"
      platform: "linkedin"
      type: "text_post"
      publish_time: "2025-01-07 08:00 KST"
      status: "scheduled"
      content_preview: "[첫 줄]..."

  calendar_view: |
    월: IG 캐러셀 (19:00)
    화: LI 포스트 (08:00), X 스레드 (09:00)
    수: IG 릴스 (12:00)
    목: TH 포스트 (20:00)
    금: IG 피드 (19:00), LI 회고 (17:00)

  notes:
    - "수요일 IG 릴스는 트렌딩 오디오 반영 필요"
    - "금요일 LI 회고는 주간 성과 데이터 업데이트"
```

## 다음 단계

스케줄링 완료 후:
1. → 발행
2. → `10-engagement`: 커뮤니티 관리
3. → `11-analytics`: 성과 분석
