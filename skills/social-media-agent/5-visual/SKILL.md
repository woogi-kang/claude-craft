---
name: social-visual
description: |
  소셜미디어 콘텐츠를 위한 이미지와 영상을 기획합니다.

  활성화 조건:
  - "이미지 기획해줘"
  - "비주얼 만들어줘"
  - "썸네일 디자인"
  - "영상 스토리보드"
  - "캐러셀 디자인"
---

# 5. Visual: 이미지/영상 기획

## 플랫폼별 이미지 사이즈

```yaml
image_specs:
  instagram:
    feed_square: "1080x1080 (1:1)"
    feed_portrait: "1080x1350 (4:5) - 권장"
    feed_landscape: "1080x566 (1.91:1)"
    story_reel: "1080x1920 (9:16)"
    carousel: "1080x1080 또는 1080x1350 (통일)"

  linkedin:
    feed_image: "1200x627 (1.91:1)"
    square: "1080x1080 (1:1)"
    carousel_pdf: "1080x1080 또는 1080x1350"
    cover_image: "1584x396"

  x:
    single_image: "1200x675 (16:9)"
    two_images: "700x800 each"
    header: "1500x500"

  threads:
    flexible: "Instagram과 동일"
    recommended: "1080x1080"
```

## 비주얼 유형별 가이드

### 1. 텍스트 기반 이미지

```yaml
text_image:
  use_cases:
    - 인용문/명언
    - 팁/인사이트
    - 통계/숫자
    - 질문/투표

  design_principles:
    - 텍스트 50% 이하 (Instagram 권장)
    - 폰트 크기: 모바일 가독성 확보
    - 대비: 배경과 텍스트 명확히 구분
    - 여백: 충분한 공간 확보

  layout_options:
    centered: "텍스트 중앙 배치"
    top_bottom: "상단 텍스트 + 하단 CTA"
    left_aligned: "왼쪽 정렬 + 우측 여백"

  font_pairing:
    heading: "Bold Sans-serif (Pretendard, Noto Sans)"
    body: "Regular Sans-serif"
    accent: "Serif 또는 Script (포인트)"
```

### 2. 캐러셀/슬라이드

```yaml
carousel_design:
  structure:
    cover: |
      - 강렬한 헤드라인
      - 시선을 끄는 비주얼
      - 스와이프 힌트 (화살표, "Swipe →")

    content_slides: |
      - 한 슬라이드 = 한 포인트
      - 일관된 레이아웃
      - 진행 표시 (번호, 프로그레스바)

    cta_slide: |
      - 핵심 요약
      - 저장/공유 유도
      - 팔로우 CTA

  design_system:
    colors: "브랜드 컬러 2-3개"
    fonts: "헤드라인 + 본문 2종"
    layout: "일관된 그리드"
    elements: "아이콘, 구분선, 도형"

  templates:
    listicle: "[N]가지 [주제]"
    how_to: "[주제] 하는 방법"
    comparison: "A vs B"
    timeline: "[기간] 동안의 변화"
    checklist: "[주제] 체크리스트"
```

### 3. 인포그래픽

```yaml
infographic:
  types:
    statistical: "데이터/통계 시각화"
    process: "단계별 프로세스"
    comparison: "비교 차트"
    timeline: "타임라인"
    hierarchical: "피라미드/계층"

  design_tips:
    - 데이터 하이라이트
    - 명확한 시각적 계층
    - 컬러로 구분
    - 아이콘 활용
    - 숫자 강조

  chart_selection:
    comparison: "막대 그래프"
    trend: "라인 그래프"
    proportion: "원형 차트 (2-3개만)"
    distribution: "히스토그램"
```

### 4. 영상/릴스 스토리보드

```yaml
video_storyboard:
  structure:
    hook: |
      0-3초
      - 강렬한 시작
      - 텍스트 오버레이
      - 빠른 컷

    body: |
      3-25초
      - 주요 콘텐츠
      - 2-3초 컷
      - 자막 필수

    cta: |
      마지막 5초
      - 행동 유도
      - 팔로우/저장 요청

  template:
    scene_1:
      duration: "3초"
      visual: "[설명]"
      text_overlay: "[텍스트]"
      audio: "[음악/보이스]"
      transition: "컷"

    scene_2:
      # ...

  audio_tips:
    - 트렌딩 오디오 활용
    - 저작권 확인 필수
    - 음소거 시청 고려 → 자막 필수
```

## AI 이미지 생성 프롬프트

### 프롬프트 구조

```yaml
ai_image_prompt:
  structure:
    subject: "주제/피사체"
    style: "아트 스타일"
    composition: "구도"
    lighting: "조명"
    mood: "분위기"
    details: "추가 디테일"

  example:
    prompt: |
      A modern minimalist workspace with a laptop,
      coffee cup, and plant on a white desk,
      soft natural lighting from window,
      clean and professional aesthetic,
      lifestyle photography style,
      4K, high quality

  style_keywords:
    minimalist: "clean, simple, white space"
    corporate: "professional, business, modern"
    creative: "colorful, artistic, dynamic"
    lifestyle: "natural, authentic, candid"
    tech: "futuristic, digital, sleek"
```

### 플랫폼별 프롬프트 가이드

```yaml
platform_prompts:
  instagram:
    style: "Instagram-worthy, aesthetic, lifestyle"
    mood: "aspirational, visually pleasing"
    avoid: "stock photo feel, overly corporate"

  linkedin:
    style: "professional, corporate, clean"
    mood: "trustworthy, competent"
    avoid: "too casual, meme-like"

  x:
    style: "eye-catching, shareable, bold"
    mood: "impactful, memorable"
    avoid: "complex, hard to read on mobile"

  threads:
    style: "casual, authentic, relatable"
    mood: "friendly, approachable"
    avoid: "overly polished, corporate"
```

## 디자인 도구 추천

```yaml
design_tools:
  beginner:
    - name: "Canva"
      best_for: "템플릿 기반 빠른 제작"
      price: "무료/Pro $12.99/월"

    - name: "Adobe Express"
      best_for: "소셜미디어 최적화"
      price: "무료/Premium $9.99/월"

  intermediate:
    - name: "Figma"
      best_for: "커스텀 디자인, 협업"
      price: "무료/Pro $12/월"

    - name: "Photoshop"
      best_for: "고급 이미지 편집"
      price: "$20.99/월"

  video:
    - name: "CapCut"
      best_for: "릴스/숏폼 편집"
      price: "무료"

    - name: "Premiere Pro"
      best_for: "전문 영상 편집"
      price: "$20.99/월"

  ai_generation:
    - name: "Midjourney"
      best_for: "아티스틱 이미지"
      price: "$10-30/월"

    - name: "DALL-E"
      best_for: "다양한 스타일"
      price: "크레딧 기반"
```

## 비주얼 체크리스트

```yaml
visual_checklist:
  technical:
    - [ ] 해상도 충분 (흐리지 않음)
    - [ ] 올바른 비율
    - [ ] 파일 크기 적정
    - [ ] 모바일 가독성

  brand:
    - [ ] 브랜드 컬러 사용
    - [ ] 폰트 일관성
    - [ ] 로고 배치 (필요시)
    - [ ] 전체 피드 조화

  accessibility:
    - [ ] 충분한 대비
    - [ ] 텍스트 읽기 쉬움
    - [ ] 색맹 고려
    - [ ] Alt 텍스트 준비

  content:
    - [ ] 메시지 명확
    - [ ] CTA 포함
    - [ ] 불필요한 요소 제거
```

## 출력 형식

```yaml
visual_output:
  content_id: "IG-2025-0104-001"

  visual_spec:
    type: "carousel"
    slides: 7
    ratio: "4:5"
    dimensions: "1080x1350"

  slide_details:
    - slide: 1
      description: "표지 - 헤드라인 중앙 배치"
      text: "마케터가 몰랐던 5가지 비밀"
      elements: ["그라데이션 배경", "볼드 타이틀"]

    - slide: 2
      description: "비밀 #1"
      text: "[내용]"
      elements: ["숫자 강조", "아이콘"]

  ai_prompts:
    background: "[AI 이미지 프롬프트]"

  design_notes:
    - "브랜드 컬러: #FF6B6B, #4ECDC4"
    - "폰트: Pretendard Bold/Regular"
```

## 다음 단계

비주얼 기획 완료 후:
1. → 디자인 도구로 제작
2. → `2-validation`: 브랜드 일관성 검증
3. → `7-approval`: 최종 승인
