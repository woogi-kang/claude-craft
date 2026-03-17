---
name: social-content-tiktok
description: |
  TikTok에 최적화된 콘텐츠를 작성합니다.

  활성화 조건:
  - "틱톡 콘텐츠 만들어줘"
  - "틱톡 스크립트 써줘"
  - "TikTok 영상 기획해줘"
  - "틱톡 트렌드 참여"
  - "숏폼 콘텐츠 만들어줘"
---

# TikTok 콘텐츠 작성 가이드

## 플랫폼 특성

```yaml
tiktok_profile:
  audience: "Gen Z + Millennial, 글로벌 / 한국"
  algorithm: "콘텐츠 기반 추천 (팔로워 수 무관)"
  core_value: "진정성, 엔터테인먼트, 교육"
  discovery: "For You Page (FYP) 알고리즘이 핵심"
  culture: "완벽한 퀄리티보다 진짜 콘텐츠가 승리"
```

## 알고리즘 우선순위

```yaml
algorithm_priorities:
  primary_signals:
    watch_time: |
      가장 중요한 지표
      - 시청 완료율 (Completion Rate) — 핵심 중의 핵심
      - 반복 시청 (Replay) — 강력한 긍정 시그널
      - 평균 시청 시간 — 길수록 유리
    shares: |
      두 번째로 중요
      - DM 공유가 가장 강력한 시그널
      - "친구 태그" 댓글도 공유와 유사 효과
    comments: |
      대화 유발
      - 댓글 수 + 댓글 길이 모두 중요
      - 제작자의 댓글 응답도 시그널
    likes: |
      기본 참여
      - 가장 쉬운 참여이므로 가중치는 상대적으로 낮음

  secondary_signals:
    - "프로필 방문 (영상 보고 프로필 클릭)"
    - "팔로우 전환 (영상 → 팔로우)"
    - "사운드 사용 (해당 사운드로 새 영상 생성)"
    - "듀엣/스티치 생성"

  algorithm_tips:
    - "처음 200-500 뷰에서의 반응이 확산 여부를 결정"
    - "새 계정도 FYP에 노출 가능 (팔로워 0에서도)"
    - "일관된 닛치/주제가 알고리즘 학습에 도움"
    - "영상 설명 + 해시태그로 콘텐츠 카테고리 시그널"
```

## 콘텐츠 유형

### 1. 트렌드 참여 (Trend Participation)

```yaml
trend_content:
  description: "현재 트렌딩 사운드/포맷을 활용한 콘텐츠"
  timing: "트렌드 초기에 참여할수록 유리 (24-72시간 이내)"

  types:
    sound_trends: |
      - 트렌딩 사운드에 맞춰 자기 버전 제작
      - TikTok Creative Center에서 트렌딩 사운드 확인
      - 사운드에 맞는 립싱크 또는 상황 연출

    format_trends: |
      - "POV:", "Tell me without telling me"
      - "Day in my life as a [직업]"
      - 특정 편집 스타일 (빠른 컷, 줌인/아웃)

    challenge_trends: |
      - 해시태그 챌린지 참여
      - 브랜드/업계 관련 챌린지 생성

  best_practices:
    - "트렌드를 자기 닛치에 맞게 변형"
    - "무리하게 관계없는 트렌드 참여 금지"
    - "트렌드 + 자기 전문성 = 최고 조합"

  example_kr: |
    [트렌딩 사운드 사용]
    "개발자가 이 사운드를 들으면..."
    → 코딩하다 에러 만났을 때 리액션

  example_en: |
    [Trending sound]
    "When the marketing team says 'let's go viral'..."
    → Reaction to unrealistic expectations
```

### 2. 듀엣 & 스티치 (Duets & Stitches)

```yaml
duet_stitch:
  duet:
    description: "다른 영상과 나란히 배치하여 리액션/추가 콘텐츠"
    use_cases:
      - "전문가 의견 추가"
      - "리액션/반응"
      - "비교/대조"
      - "사실 확인/보충 설명"
    example_en: |
      [Duet with a viral marketing tip]
      "OK but here's what they're NOT telling you..."

  stitch:
    description: "다른 영상의 일부를 가져와 이어서 촬영"
    use_cases:
      - "다른 영상의 질문에 답하기"
      - "반론/추가 설명"
      - "경험 공유"
    example_kr: |
      [스티치: "여러분은 어떤 툴 쓰세요?"]
      "저는 이 3가지 무료 툴로 월 1000만원 절약했어요..."
```

### 3. 튜토리얼 & 교육 (Tutorials & Education)

```yaml
tutorial_content:
  description: "실용적 팁, 방법론, 노하우 공유"
  format: "단계별 설명 + 화면 녹화 또는 시연"
  duration: "60초-3분 (복잡한 주제는 시리즈로)"

  structures:
    quick_tip:
      duration: "15-30초"
      pattern: "한 가지 팁을 빠르게"
      hook_en: "This one trick will save you hours..."
      hook_kr: "이 한 가지만 알면 시간을 아낄 수 있어요..."

    step_by_step:
      duration: "60초-3분"
      pattern: "3-5 단계로 설명"
      hook_en: "Here's how to [결과] in 3 steps:"
      hook_kr: "[결과]를 위한 3단계:"

    myth_busting:
      duration: "30-60초"
      pattern: "잘못된 상식 → 올바른 정보"
      hook_en: "Stop doing this! Here's why..."
      hook_kr: "이거 하지 마세요! 이유는..."

  example_en: |
    Hook: "3 free tools that replaced my $200/month subscription"
    Step 1: "Instead of Notion AI, use..."
    Step 2: "Instead of Canva Pro, use..."
    Step 3: "Instead of Buffer, use..."
    CTA: "Follow for more free alternatives"

  example_kr: |
    Hook: "월 20만원짜리 구독을 대체한 무료 도구 3개"
    Step 1: "Notion AI 대신..."
    Step 2: "Canva Pro 대신..."
    Step 3: "Buffer 대신..."
    CTA: "팔로우하면 더 많은 무료 대안을 알려드릴게요"
```

### 4. 비하인드 씬 (Behind the Scenes)

```yaml
behind_scenes:
  description: "과정, 일상, 작업 모습을 보여주는 콘텐츠"
  appeal: "진정성 + 호기심 충족"

  types:
    day_in_life: "하루 일과 (타임랩스 + 나레이션)"
    making_of: "제품/콘텐츠 제작 과정"
    office_tour: "작업 공간 소개"
    packing_order: "주문 포장 과정 (이커머스)"
    startup_journey: "창업 여정 기록 (Building in Public)"

  example_en: |
    "Day in my life as a solo founder 🎬"
    05:30 - Morning routine
    07:00 - Check analytics
    08:00 - Build new feature
    [Timelapse of coding]
    12:00 - User feedback review
    "Follow to see how I build a SaaS from scratch"

  example_kr: |
    "1인 창업자의 하루 📱"
    6시 - 기상 루틴
    7시 - 어제 데이터 확인
    8시 - 새 기능 개발
    [코딩 타임랩스]
    12시 - 사용자 피드백 확인
    "팔로우하면 창업 과정을 함께 볼 수 있어요"
```

### 5. 스토리텔링 (Storytelling)

```yaml
storytelling:
  description: "개인 경험, 사례, 교훈을 이야기 형식으로"
  power: "감정 연결 → 공유 → 바이럴"

  structures:
    struggle_to_success: |
      "6개월 전 나는..." → "그래서 이걸 시도했고..." → "결과는..."
    lesson_learned: |
      "실수했던 이야기..." → "이 실수에서 배운 것..." → "여러분은 이렇게 하세요"
    customer_story: |
      "고객에게 이런 메시지를 받았는데..." → "감동적인 사연..." → "이래서 이 일을 합니다"
```

## 영상 규격 (Video Specs)

```yaml
video_specs:
  aspect_ratio: "9:16 (세로 필수)"
  resolution: "1080x1920"
  duration_formats:
    trend_participation: "15초 (빠른 트렌드 참여)"
    quick_tip: "30-60초 (짧은 팁)"
    tutorial: "1-3분 (상세 설명)"
    deep_dive: "3-10분 (깊은 콘텐츠)"
  recommendation: "15-60초가 가장 높은 완료율"
  file_format: "MP4, MOV"
  max_file_size: "287.6MB (모바일), 500MB (웹)"
```

## 캡션 작성 가이드

```yaml
caption_guide:
  length:
    optimal: "150자 이하 (모바일에서 '...더보기' 없이 표시)"
    maximum: "2,200자"
    note: "긴 캡션은 '교육' 콘텐츠에만 권장"

  structure:
    hook_line: "첫 줄에 시선을 잡는 문구 (300자 중 첫 40자가 핵심)"
    body: "영상 내용 보충 또는 추가 맥락"
    cta: "행동 유도 (팔로우, 저장, 댓글)"
    hashtags: "3-5개 해시태그"

  hook_examples_en:
    - "This changed everything for me..."
    - "Nobody talks about this but..."
    - "The biggest mistake I see is..."
    - "Here's what $0 marketing looks like:"
    - "I wish I knew this sooner 😤"
    - "Stop scrolling if you..."
    - "POV: You just discovered..."

  hook_examples_kr:
    - "이거 모르면 진짜 손해..."
    - "아무도 안 알려주는 비밀"
    - "가장 큰 실수가 이거예요"
    - "마케팅 예산 0원으로 이렇게 했습니다"
    - "이걸 더 일찍 알았으면 😤"
    - "스크롤 멈추세요, 이게 진짜 중요합니다"
    - "POV: 방금 이걸 발견했을 때"

  cta_examples:
    en:
      - "Follow for more tips like this"
      - "Save this for later 📌"
      - "Tag someone who needs this"
      - "Comment '✅' if you agree"
      - "What would you add? Drop it below 👇"
    kr:
      - "팔로우하면 이런 팁 더 볼 수 있어요"
      - "저장 필수 📌"
      - "필요한 친구를 태그하세요"
      - "동의하면 '✅' 댓글!"
      - "추가할 내용 있으면 댓글로 👇"
```

## 사운드/음악 전략

```yaml
sound_strategy:
  trending_sounds:
    where_to_find:
      - "TikTok Creative Center (ads.tiktok.com/business/creativecenter)"
      - "FYP에서 반복적으로 보이는 사운드 저장"
      - "릴스에서 뜬 사운드가 TikTok으로 넘어오기도"
    timing: "트렌딩 초기에 사용할수록 알고리즘 부스트"
    caution: "저작권 확인 필수 (상업적 사용 시)"

  original_audio:
    use_cases:
      - "내레이션/보이스오버 (교육 콘텐츠)"
      - "말하기 영상 (얼굴 보이며 설명)"
      - "ASMR/제품 사운드"
    benefit: "다른 크리에이터가 사운드를 사용하면 추가 노출"

  music_tips:
    - "영상 분위기에 맞는 배경 음악 선택"
    - "TikTok 라이브러리에서 상업적 사용 가능한 음악 확인"
    - "음소거 시청 고려 → 자막 필수"
    - "사운드 볼륨: 내레이션 > 배경음악"

  korean_sounds:
    - "K-pop 트렌딩 사운드 (한국 타겟 시 효과적)"
    - "한국 밈 사운드/효과음"
    - "한국어 ASMR/나레이션"
```

## 발행 빈도 & 타이밍

```yaml
posting_frequency:
  growth_phase:
    recommended: "1-3회/일"
    minimum: "1회/일"
    note: "일관성이 빈도보다 중요"

  maintenance_phase:
    recommended: "3-5회/주"
    minimum: "3회/주"

  consistency_rule: |
    - 매일 같은 시간대에 발행
    - 갑작스런 중단보다 낮은 빈도가 나음
    - 품질 유지 가능한 최대 빈도 선택

  optimal_times:
    kr_audience:
      weekday: "12:00-13:00, 18:00-21:00 KST"
      weekend: "10:00-12:00, 19:00-22:00 KST"
    global_audience:
      weekday: "09:00-11:00, 19:00-21:00 EST"
      note: "TikTok은 알고리즘 기반이므로 시간 영향이 상대적으로 적음"
```

## 첫 3초 훅 패턴 (The 3-Second Hook)

```yaml
hook_patterns:
  importance: "첫 3초에서 시청 여부 결정 — 가장 중요한 부분"

  visual_hooks:
    movement: "빠른 줌인, 손 동작, 물건 등장"
    text_overlay: "큰 텍스트로 핵심 질문/주장"
    unexpected: "예상 밖의 첫 장면"
    face: "표정 리액션 (놀람, 충격)"

  verbal_hooks:
    question:
      en: "Did you know that...?"
      kr: "이거 알고 있었어요?"
    challenge:
      en: "I bet you didn't know this..."
      kr: "이거 모르는 사람이 많더라고요..."
    promise:
      en: "After this video, you'll never..."
      kr: "이 영상 보고 나면..."
    controversy:
      en: "Everyone is doing this wrong..."
      kr: "다들 이거 잘못하고 있어요..."
    story:
      en: "So this crazy thing happened..."
      kr: "방금 말도 안 되는 일이..."
    secret:
      en: "Here's what nobody tells you about..."
      kr: "아무도 안 알려주는 비밀인데..."

  hook_formula: |
    [강한 텍스트 오버레이] + [눈을 끄는 비주얼] + [호기심 유발 내레이션]
    = 처음 3초에 "계속 봐야 하는 이유" 제공
```

## 한국 vs 글로벌 오디언스 팁

```yaml
audience_tips:
  korean_audience:
    tone: "친근한 반말체 또는 존댓말 (~해요)"
    content_preferences:
      - "K-culture 관련 콘텐츠"
      - "한국 시장 특화 팁"
      - "한국어 트렌딩 사운드"
      - "한국 밈/유머"
    hashtags: ["#틱톡", "#추천", "#일상", "#꿀팁"]
    peak_times: "KST 기준 점심/저녁"

  global_english_audience:
    tone: "Casual, authentic, conversational"
    content_preferences:
      - "Universal topics (productivity, money, lifestyle)"
      - "English trending sounds"
      - "Relatable humor (cross-cultural)"
      - "Visual-heavy (less text dependency)"
    hashtags: ["#fyp", "#viral", "#tips", "#learnontiktok"]
    peak_times: "EST 기준 오전/저녁"

  bilingual_strategy:
    approach: |
      - 별도 계정 운영이 가장 효과적 (알고리즘이 오디언스 학습)
      - 단일 계정이면 한 언어를 주력으로 선택
      - 영어 자막 추가로 한국어 콘텐츠의 글로벌 도달 확대
      - 비언어적 콘텐츠 (댄스, 시각적 콘텐츠)는 양쪽 모두에 효과적
```

## 출력 형식

```yaml
tiktok_content_output:
  content_id: "TT-2025-0104-001"

  video_concept:
    type: "tutorial | trend | behind_scenes | duet | stitch | story"
    duration: "30초"
    hook: "[첫 3초 설명]"
    body: "[본문 콘텐츠 설명]"
    cta: "[마무리 CTA]"

  script:
    visual: |
      [각 장면의 비주얼 설명]
    narration: |
      [보이스오버/말하기 스크립트]
    text_overlay: |
      [화면에 표시할 텍스트]

  sound: "[트렌딩 사운드 이름 또는 오리지널]"

  caption: |
    [캡션 텍스트]
    #해시태그1 #해시태그2

  posting_time: "2025-01-04 19:00 KST"

  checklist:
    - [ ] 첫 3초 훅 확인
    - [ ] 세로 비율 (9:16) 확인
    - [ ] 자막/텍스트 오버레이 추가
    - [ ] 사운드/음악 설정
    - [ ] 캡션 + 해시태그 작성
    - [ ] Safe zone 내 텍스트 배치 확인
```

## 다음 단계

TikTok 콘텐츠 작성 완료 후:
1. → `5-visual`: 영상 비주얼 기획
2. → `6-hashtag`: 해시태그 최적화
3. → `8-schedule`: 발행 스케줄링
4. → `11-analytics`: 성과 분석 (시청 완료율 중점)
