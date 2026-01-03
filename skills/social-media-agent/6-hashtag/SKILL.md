---
name: social-hashtag
description: |
  플랫폼별 해시태그 전략을 최적화합니다.

  활성화 조건:
  - "해시태그 추천해줘"
  - "해시태그 전략 세워줘"
  - "태그 최적화해줘"
---

# 6. Hashtag: 해시태그 최적화

## 플랫폼별 해시태그 전략

### Instagram

```yaml
instagram_hashtags:
  count:
    recommended: "20-30개"
    minimum: "10개"
    maximum: "30개"

  mix_strategy:
    large: |
      30%
      - 100만+ 게시물
      - 노출 기회, 경쟁 치열
      - 예: #마케팅, #일상

    medium: |
      40%
      - 10만-100만 게시물
      - 균형 잡힌 도달
      - 예: #마케팅팁, #스타트업일상

    niche: |
      30%
      - 1만-10만 게시물
      - 타겟 정확, 상위 노출 가능
      - 예: #콘텐츠마케터, #SaaS스타트업

  placement:
    option_1: "캡션 하단 (줄바꿈 5개 후)"
    option_2: "첫 댓글"
    recommendation: "첫 댓글 권장 (캡션 깔끔)"

  banned_hashtags:
    check: "정기적으로 확인 필요"
    risk: "섀도우밴 가능성"
    tool: "IQ Hashtags, Display Purposes"
```

### LinkedIn

```yaml
linkedin_hashtags:
  count:
    recommended: "3-5개"
    maximum: "5개"

  strategy:
    - 업계/전문 해시태그
    - 팔로워가 많은 해시태그
    - 브랜드/캠페인 해시태그

  placement: "포스트 끝 또는 본문에 자연스럽게"

  examples:
    industry: "#마케팅 #스타트업 #테크"
    professional: "#리더십 #커리어 #생산성"
    content: "#팁 #인사이트 #케이스스터디"
```

### X (Twitter)

```yaml
x_hashtags:
  count:
    recommended: "1-2개"
    maximum: "3개"

  strategy:
    - 트렌딩 해시태그 활용
    - 대화 참여용
    - 브랜드/캠페인 태그

  placement: "본문에 자연스럽게 또는 끝에"

  tips:
    - 과도한 해시태그 = 스팸으로 인식
    - 트렌딩 활용 시 관련성 확보
    - 브랜드 해시태그 일관성
```

### Threads

```yaml
threads_hashtags:
  count:
    recommended: "0-3개"
    style: "최소한으로"

  strategy:
    - 필수 아님
    - 트렌딩 참여 시에만
    - 캠페인/이벤트용

  note: "Threads는 대화 중심, 해시태그 덜 중요"
```

## 해시태그 리서치 방법

### 1. 경쟁사/인플루언서 분석

```yaml
competitor_analysis:
  steps:
    1: "업계 상위 계정 10개 선정"
    2: "최근 인기 포스트의 해시태그 수집"
    3: "공통 해시태그 추출"
    4: "성과 좋은 조합 파악"

  template:
    account: "@competitor"
    post: "[포스트 링크]"
    engagement: "5.2%"
    hashtags: ["#해시태그1", "#해시태그2"]
```

### 2. 검색량 확인

```yaml
search_volume:
  tools:
    - Instagram 검색 (게시물 수 확인)
    - Hashtagify
    - RiteTag
    - All Hashtag

  evaluation:
    too_large: "100만+ → 경쟁 과다"
    sweet_spot: "10만-100만 → 균형"
    niche: "1만-10만 → 타겟팅"
    too_small: "1만 미만 → 노출 제한"
```

### 3. 관련 해시태그 확장

```yaml
expansion:
  method: |
    핵심 해시태그에서 관련 태그 탐색

  example:
    core: "#콘텐츠마케팅"
    related:
      - "#콘텐츠전략"
      - "#디지털마케팅"
      - "#SNS마케팅"
      - "#브랜드마케팅"
      - "#마케팅팁"
      - "#콘텐츠크리에이터"
```

## 해시태그 카테고리

```yaml
hashtag_categories:
  industry:
    description: "업계/산업 관련"
    examples: ["#마케팅", "#테크", "#패션", "#F&B"]

  niche:
    description: "세부 주제/전문 분야"
    examples: ["#그로스해킹", "#UX디자인", "#핀테크"]

  community:
    description: "커뮤니티/문화"
    examples: ["#마케터일상", "#개발자일기", "#디자이너의하루"]

  location:
    description: "지역 기반"
    examples: ["#서울맛집", "#강남카페", "#부산여행"]

  branded:
    description: "브랜드/캠페인"
    examples: ["#브랜드명", "#캠페인명", "#이벤트명"]

  trending:
    description: "트렌딩/시즌"
    examples: ["#2025트렌드", "#월요일", "#불금"]

  engagement:
    description: "참여 유도"
    examples: ["#오늘의기록", "#일상공유", "#소통해요"]
```

## 해시태그 세트 관리

```yaml
hashtag_sets:
  purpose: "콘텐츠 유형별 해시태그 세트 사전 준비"

  example_sets:
    educational:
      name: "교육/팁 콘텐츠"
      hashtags:
        - "#마케팅팁"
        - "#비즈니스인사이트"
        - "#자기계발"
        # ... 30개 준비

    promotional:
      name: "프로모션/제품"
      hashtags:
        - "#신제품"
        - "#이벤트"
        - "#할인"
        # ...

    behind_scenes:
      name: "비하인드/일상"
      hashtags:
        - "#회사일상"
        - "#팀문화"
        - "#오피스라이프"
        # ...

  rotation:
    - 매번 같은 세트 사용 금지
    - 세트 내에서 10-20% 변경
    - 정기적으로 성과 분석 후 업데이트
```

## 금지/위험 해시태그

```yaml
banned_hashtags:
  types:
    permanently_banned: |
      - 스팸/성인 콘텐츠 관련
      - 불법 활동 관련
      - 혐오 표현 관련

    temporarily_banned: |
      - 남용으로 일시 제한
      - 정치적 민감 시기
      - 사회 이슈 관련

  risks:
    shadow_ban: "콘텐츠 노출 제한"
    reduced_reach: "도달률 감소"
    account_flag: "계정 경고"

  prevention:
    - 정기적 체크 (월 1회)
    - 자동 체크 도구 활용
    - 의심스러운 태그 회피
```

## 해시태그 성과 분석

```yaml
performance_analysis:
  metrics:
    reach: "해시태그 통한 도달"
    impressions: "해시태그 노출"
    top_posts: "상위 게시물 진입 여부"

  instagram_insights:
    location: "인사이트 > 콘텐츠 > 게시물 > 도달"
    data: "해시태그에서 온 노출 수"

  optimization:
    - 낮은 성과 태그 교체
    - 높은 성과 태그 유지
    - A/B 테스트로 최적 조합 발견
```

## 출력 형식

```yaml
hashtag_output:
  content_id: "IG-2025-0104-001"
  platform: "instagram"

  recommended_hashtags:
    large:
      - "#마케팅" (500만)
      - "#인스타그램" (1억)
    medium:
      - "#콘텐츠마케팅" (50만)
      - "#마케팅팁" (30만)
    niche:
      - "#그로스해커" (5만)
      - "#마케터일상" (8만)

  total_count: 25

  placement: "첫 댓글"

  rotation_note: "다음 포스트에서 30% 변경 권장"

  banned_check:
    status: "pass"
    checked_date: "2025-01-04"
```

## 다음 단계

해시태그 최적화 후:
1. → `2-validation`: 금지 태그 최종 확인
2. → `7-approval`: 승인
3. → `8-schedule`: 발행
