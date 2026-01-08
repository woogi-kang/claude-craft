---
name: social-content-threads
description: |
  Threads에 최적화된 콘텐츠를 작성합니다.

  활성화 조건:
  - "스레드 콘텐츠 만들어줘"
  - "Threads 포스트 써줘"
  - "쓰레드 기획해줘"
---

# Threads 콘텐츠 작성 가이드

## 플랫폼 특성

```yaml
threads_profile:
  audience: "캐주얼한 대화, Instagram 연동 사용자"
  content_lifespan: "6-24시간"
  algorithm_priority:
    - 참여율 (답글, 리포스트, 인용)
    - Instagram 연동 관계
    - 주제 관심사
    - 대화 참여도
  best_times:
    weekday: "12:00-14:00, 20:00-22:00"
    weekend: "10:00-12:00, 19:00-21:00"
  audience_mindset: "가벼운 소통, 일상 공유, 실시간 반응"

  key_difference:
    vs_x: "더 캐주얼, 덜 뉴스 중심, 커뮤니티 느낌"
    vs_instagram: "텍스트 중심, 완성도보다 진정성"
```

## 콘텐츠 유형별 가이드

### 1. 단일 포스트

```yaml
single_post:
  specs:
    max_length: 500자
    media: "이미지, 영상, GIF 첨부 가능"
    links: "지원 (미리보기 표시)"

  best_practices:
    - 대화하듯 자연스럽게
    - 완벽하지 않아도 OK
    - 생각/의견 바로 공유
    - 일상적인 톤

  structure:
    casual: |
      [생각/관찰]

      [부연 설명]

      [질문 또는 여운]
```

### 2. 스레드 (연결 포스트)

```yaml
thread:
  specs:
    posts: "2-7개 권장"
    flow: "자연스러운 대화 흐름"

  structure:
    post_1: |
      훅 또는 주제 제시
      - 호기심 유발
      - "계속 읽고 싶게"

    post_2_n: |
      이야기 전개
      - 각 포스트가 자연스럽게 연결
      - 대화하듯 풀어가기

    last_post: |
      마무리
      - 결론 또는 질문
      - 답글 유도

  vs_x_thread:
    threads: "대화체, 생각의 흐름 그대로"
    x: "정보 전달, 구조화된 형식"
```

### 3. 답글/대화

```yaml
reply:
  importance: "Threads의 핵심 = 대화"

  best_practices:
    - 적극적으로 답글 달기
    - 다른 사람 포스트에 참여
    - 대화를 이어가기
    - 커뮤니티 느낌 만들기

  engagement_types:
    agreement: "ㅋㅋㅋ 진짜 공감"
    add_on: "여기에 덧붙이자면..."
    question: "근데 이건 어떻게 생각해요?"
    experience: "저도 비슷한 경험이..."
```

## 글쓰기 공식

### 톤앤매너

```yaml
threads_tone:
  voice:
    - 친구한테 말하듯
    - 캐주얼하고 편안한
    - 진정성 있는
    - 유머러스한 (자연스럽게)

  language:
    - 반말/존댓말 혼용 OK
    - 구어체 적극 활용
    - 줄임말/신조어 OK
    - 이모지 자유롭게

  examples:
    formal: "오늘 중요한 인사이트를 공유드립니다."
    threads: "아 오늘 깨달은 건데 진짜 신기함"
```

### 구조별 템플릿

**1. 생각 공유형**
```
갑자기 든 생각인데

[생각/관찰]

근데 생각해보면 [부연]

나만 그런가?
```

**2. 일상 관찰형**
```
[상황 설명]

근데 웃긴 게 [관찰]

ㅋㅋㅋㅋ [반응]
```

**3. 의견 표현형**
```
솔직히 말하면

[의견]

왜냐면 [이유]

다들 어떻게 생각함?
```

**4. 질문형**
```
궁금한 게 있는데

[질문]

나는 [본인 생각/경험]인데

다들은?
```

**5. 공유형**
```
이거 봤어?

[링크 또는 설명]

[내 반응/생각]

대박 아님?
```

**6. 스레드형 (연결)**
```
[포스트 1]
오늘 있었던 일 얘기해도 됨?

[포스트 2]
그래서 뭐였냐면...
[상황 설명]

[포스트 3]
근데 반전이 있음
[전개]

[포스트 4]
결론: [마무리]
어떻게 생각해?
```

## 언어 스타일 가이드

```yaml
language_style:
  casual_expressions:
    instead_of: "그러나" → "근데"
    instead_of: "왜냐하면" → "왜냐면"
    instead_of: "그렇습니다" → "그럼"
    instead_of: "동의합니다" → "인정"
    instead_of: "재미있습니다" → "웃김 ㅋㅋ"

  sentence_endings:
    - "~인 듯"
    - "~임"
    - "~인데"
    - "~아님?"
    - "~거 아니야?"

  filler_words:
    - "아"
    - "근데"
    - "진짜"
    - "솔직히"
    - "갑자기"

  reactions:
    - "ㅋㅋㅋ"
    - "ㅠㅠ"
    - "헐"
    - "대박"
    - "인정"
```

## 이모지 가이드

```yaml
emoji_usage:
  frequency: "자유롭게, 과하지 않게"

  common:
    - "ㅋㅋㅋ" (웃음 - 이모지보다 자주 사용)
    - "😂" (크게 웃을 때)
    - "🤔" (생각/의문)
    - "👀" (관심/주목)
    - "💀" (웃겨 죽겠을 때)
    - "🙏" (부탁/감사)

  avoid:
    - 비즈니스 이모지 (📊📈💼)
    - 과도한 장식
    - 매 문장 이모지
```

## 해시태그 전략

```yaml
hashtag_strategy:
  count: "0-3개"
  placement: "포스트 끝 또는 사용 안 함"

  approach:
    - X보다 해시태그 덜 중요
    - 트렌딩 주제 참여 시 활용
    - 캠페인/이벤트 시 사용
    - 일반 포스트는 없어도 OK

  examples:
    trending: "#요즘핫한거"
    event: "#쓰레드출시1주년"
```

## 참여 전략

```yaml
engagement_strategy:
  active_participation:
    - 다른 사람 포스트에 답글
    - 흥미로운 포스트 리포스트
    - 대화에 적극 참여
    - 인용으로 의견 추가

  community_building:
    - 같은 관심사 사람들과 소통
    - 정기적으로 답글 체크
    - 팔로워 포스트에 반응
    - 질문에 성실히 답변

  timing:
    - 발행 후 30분-1시간 집중 응답
    - 답글에 빠르게 반응
    - 대화 이어가기
```

## Threads vs 다른 플랫폼

| 요소 | Threads | X | Instagram |
|------|---------|---|-----------|
| 톤 | 매우 캐주얼 | 캐주얼~전문적 | 세련됨 |
| 길이 | 500자 | 280자 | 2200자 |
| 비주얼 | 선택적 | 선택적 | 필수 |
| 해시태그 | 최소 | 1-2개 | 10-30개 |
| 목적 | 대화/소통 | 정보/의견 | 브랜딩/시각 |
| 완성도 | 낮아도 OK | 중간 | 높음 |

## CTA 모음

```yaml
threads_ctas:
  question:
    - "다들 어떻게 생각함?"
    - "나만 그런가?"
    - "이거 공감되는 사람?"
    - "비슷한 경험 있어?"

  engagement:
    - "알려줘"
    - "같이 얘기해요"
    - "답글 고고"

  share:
    - "공유해도 됨?"
    - "퍼가~"

  reaction:
    - "어때?"
    - "괜찮음?"
```

## 출력 형식

```yaml
threads_output:
  post_id: "TH-2025-0104-001"
  type: "single"

  content: |
    [포스트 내용]

  media: null  # 또는 이미지/영상 설명

  hashtags: []  # 또는 ["#태그"]

  posting_recommendation:
    best_time: "2025-01-05 20:00 KST"
    cross_post: "Instagram 스토리에 공유 권장"

  engagement_plan:
    - "답글 적극 응답"
    - "관련 주제 포스트에 참여"
```

## 크로스 포스팅 가이드

```yaml
cross_posting:
  from_instagram:
    - 스토리 → Threads (비하인드 씬)
    - 릴스 → Threads (반응 요청)
    - 피드 → Threads (가벼운 버전)

  to_instagram:
    - Threads 인기 포스트 → 스토리 공유
    - 대화 하이라이트 → 피드 콘텐츠화

  adaptation:
    - 같은 내용이라도 톤 조정
    - Threads는 더 캐주얼하게
    - 완성도 낮춰도 OK
```

## 다음 단계

콘텐츠 작성 완료 후:
1. → `2-validation`: 콘텐츠 검증 (간단히)
2. → `8-schedule`: 발행 스케줄링
3. → `10-engagement`: 답글/대화 관리
