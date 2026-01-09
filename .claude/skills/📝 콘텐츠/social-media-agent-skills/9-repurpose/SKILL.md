---
name: social-repurpose
description: |
  하나의 콘텐츠를 여러 플랫폼에 맞게 변환합니다.

  활성화 조건:
  - "크로스포스팅해줘"
  - "다른 플랫폼용으로 변환해줘"
  - "콘텐츠 리퍼포징해줘"
  - "재활용해줘"
---

# 9. Repurpose: 크로스플랫폼 변환

## 개요

하나의 소재로 여러 플랫폼에 최적화된 콘텐츠를 생성하여 효율성을 극대화합니다.

## 변환 매트릭스

### 원본 → 타겟 플랫폼

```yaml
repurpose_matrix:
  from_blog_article:
    to_linkedin:
      format: "텍스트 포스트 (요약)"
      adaptation: "핵심 인사이트 3-5개 추출"
      length: "1000-1500자"

    to_instagram:
      format: "캐러셀"
      adaptation: "포인트별 슬라이드화"
      slides: "7-10장"

    to_x:
      format: "스레드"
      adaptation: "핵심 포인트 압축"
      tweets: "5-10개"

    to_threads:
      format: "짧은 포스트"
      adaptation: "한 가지 핵심만"
      length: "200-300자"

  from_linkedin_post:
    to_instagram:
      format: "텍스트 이미지 또는 캐러셀"
      adaptation: "시각화 + 감성적 톤"

    to_x:
      format: "단일 트윗 또는 짧은 스레드"
      adaptation: "핵심 한 문장 + 부연"

    to_threads:
      format: "캐주얼 버전"
      adaptation: "대화체로 변환"

  from_instagram_carousel:
    to_linkedin:
      format: "PDF 캐러셀 또는 텍스트"
      adaptation: "전문적 톤으로 변환"

    to_x:
      format: "스레드"
      adaptation: "슬라이드 → 트윗 변환"

    to_threads:
      format: "요약 포스트"
      adaptation: "핵심만 캐주얼하게"

  from_video_reel:
    to_linkedin:
      format: "텍스트 포스트 + 비디오"
      adaptation: "전문적 설명 추가"

    to_x:
      format: "비디오 트윗 또는 GIF"
      adaptation: "짧게 편집 (30초 이하)"

    to_threads:
      format: "비디오 + 캐주얼 캡션"
      adaptation: "반응 요청"
```

## 톤 변환 가이드

```yaml
tone_adaptation:
  instagram:
    from_linkedin: |
      - 격식체 → 친근한 대화체
      - 데이터 → 스토리텔링
      - 전문용어 → 쉬운 표현
      - 이모지 추가

    example:
      before: "본 연구에 따르면 고객 유지율이 5% 증가하면 수익이 25-95% 증가합니다."
      after: |
        알고 있었나요? 💡

        기존 고객을 5% 더 유지하면
        수익이 최대 95%까지 늘어난대요!

        새 고객 찾는 것보다
        기존 고객 관리가 왜 중요한지
        이제 아시겠죠? 🙌

  linkedin:
    from_instagram: |
      - 친근체 → 전문적 어조
      - 감성 → 인사이트/데이터
      - 이모지 최소화
      - 비즈니스 맥락 추가

    example:
      before: |
        오늘 깨달은 거 🤯

        고객한테 계속 연락하는 게
        진짜 중요하더라고요

        여러분도 그런 경험 있어요?
      after: |
        고객 유지의 진정한 가치를 재발견했습니다.

        Bain & Company 연구에 따르면,
        고객 유지율 5% 증가는 수익 25-95% 증가로 이어집니다.

        신규 고객 획득 비용이 기존 고객 유지 비용의
        5-25배라는 점을 고려하면,

        우리의 마케팅 리소스 배분을 재고해볼 필요가 있습니다.

        여러분의 회사는 어떤 전략을 취하고 계신가요?

  x:
    from_linkedin: |
      - 긴 문장 → 짧게
      - 부연 설명 제거
      - 임팩트 있는 핵심만
      - 위트 추가 (가능시)

    example:
      before: "[긴 LinkedIn 포스트]"
      after: |
        고객 유지율 5% ↑ = 수익 25-95% ↑

        신규 고객 획득보다 기존 고객 유지가
        5-25배 효율적입니다.

        근데 왜 다들 신규 고객한테만 집중할까요?

  threads:
    from_any: |
      - 가장 캐주얼하게
      - 생각하듯 말하듯
      - 완벽하지 않아도 OK
      - 대화 유도

    example:
      before: "[어떤 포맷이든]"
      after: |
        갑자기 든 생각인데

        기존 고객 5%만 더 잡으면
        수익이 거의 2배가 될 수 있다는 거
        왜 아무도 안 알려줬지?

        신규 고객 찾느라 정신없었는데
        진짜 중요한 건 따로 있었음
```

## 길이 변환 가이드

```yaml
length_adaptation:
  long_to_short:
    strategy: |
      1. 핵심 메시지 1개 추출
      2. 불필요한 맥락 제거
      3. 예시는 가장 강력한 것만
      4. CTA 유지

    example:
      original: "1500자 LinkedIn 포스트"
      x_version: |
        1/ 10년간 100개 스타트업을 봤습니다.

        성공한 곳들의 공통점:
        → 고객 유지에 집착
        → 신규 획득보다 기존 고객 우선

        이 한 가지가 성패를 갈랐습니다.

  short_to_long:
    strategy: |
      1. 핵심 메시지 유지
      2. 배경/맥락 추가
      3. 예시/데이터 보강
      4. 실행 방안 추가

    example:
      original: "280자 트윗"
      linkedin_version: "[확장된 버전]"
```

## 비주얼 변환 가이드

```yaml
visual_adaptation:
  instagram_carousel_to_linkedin:
    format: "PDF 업로드"
    changes:
      - "컬러 톤 조정 (더 차분하게)"
      - "이모지 제거/최소화"
      - "전문적 폰트"
      - "데이터/출처 강조"

  linkedin_text_to_instagram:
    format: "텍스트 이미지 또는 캐러셀"
    changes:
      - "핵심 포인트 시각화"
      - "컬러풀하게"
      - "이모지 추가"
      - "인용문 스타일"

  video_repurposing:
    long_to_short:
      - "핵심 부분만 클립"
      - "세로 비율로 크롭"
      - "자막 추가"
      - "빠른 편집"

    platform_specific:
      instagram_reel: "9:16, 15-30초, 트렌딩 오디오"
      linkedin_video: "1:1 또는 16:9, 30-60초"
      x_video: "16:9, 2분 20초 이하"
```

## 리퍼포징 워크플로우

```yaml
repurpose_workflow:
  step_1_create_pillar:
    description: "기둥 콘텐츠 제작"
    format: "블로그 글, 긴 영상, 웨비나 등"
    purpose: "재활용의 원천"

  step_2_extract_core:
    description: "핵심 메시지 추출"
    output:
      - "메인 인사이트 3-5개"
      - "인용 가능한 문장"
      - "핵심 데이터/통계"

  step_3_adapt_format:
    description: "플랫폼별 포맷 변환"
    output:
      - "Instagram 캐러셀"
      - "LinkedIn 텍스트"
      - "X 스레드"
      - "Threads 포스트"

  step_4_adjust_tone:
    description: "톤앤매너 조정"
    check:
      - "플랫폼 특성 반영?"
      - "오디언스 기대 충족?"
      - "브랜드 보이스 유지?"

  step_5_schedule:
    description: "발행 스케줄링"
    tip: "같은 날 여러 플랫폼 발행 OK (다른 오디언스)"
```

## 리퍼포징 아이디어

```yaml
repurpose_ideas:
  from_one_blog_post:
    - "LinkedIn 인사이트 포스트"
    - "Instagram 캐러셀 (핵심 팁)"
    - "X 스레드 (요약)"
    - "Threads 토론 시작"
    - "Instagram 릴스 (핵심 1개)"
    - "인용문 이미지 3-5개"
    - "인포그래픽 1개"
    total: "10+ 콘텐츠"

  from_one_video:
    - "짧은 클립 5-10개"
    - "오디오 → 팟캐스트 에피소드"
    - "트랜스크립트 → 블로그"
    - "핵심 인용 → 이미지"
    - "비하인드 → 스토리"

  from_customer_testimonial:
    - "인용문 이미지"
    - "케이스 스터디 포스트"
    - "비디오 클립"
    - "캐러셀 스토리"
```

## 크로스포스팅 주의사항

```yaml
cross_posting_tips:
  do:
    - "각 플랫폼에 맞게 최적화"
    - "발행 시간 다르게"
    - "핵심 메시지는 유지하되 표현 변경"
    - "플랫폼별 해시태그 전략"

  dont:
    - "복붙 그대로 발행 (lazy cross-posting)"
    - "Instagram 캡션 그대로 LinkedIn에"
    - "LinkedIn 톤 그대로 Threads에"
    - "같은 시간에 모든 플랫폼 발행"

  platform_linking:
    instagram_to_threads: "자동 공유 기능 활용 가능"
    caution: "자동 공유도 최적화 권장"
```

## 출력 형식

```yaml
repurpose_output:
  original_content:
    id: "BLOG-2025-0104-001"
    type: "blog_article"
    title: "[원본 제목]"
    core_message: "[핵심 메시지]"

  repurposed:
    - platform: "instagram"
      format: "carousel"
      content: "[Instagram용 캡션]"
      slides: 8
      hashtags: ["#해시태그"]

    - platform: "linkedin"
      format: "text_post"
      content: "[LinkedIn용 텍스트]"

    - platform: "x"
      format: "thread"
      tweets: ["[트윗 1]", "[트윗 2]", "..."]

    - platform: "threads"
      format: "single_post"
      content: "[Threads용 텍스트]"

  schedule:
    instagram: "2025-01-05 19:00"
    linkedin: "2025-01-06 08:00"
    x: "2025-01-06 09:00"
    threads: "2025-01-06 20:00"
```

## 다음 단계

리퍼포징 완료 후:
1. → `2-validation`: 각 버전 검증
2. → `8-schedule`: 발행 스케줄링
3. → `11-analytics`: 플랫폼별 성과 비교
