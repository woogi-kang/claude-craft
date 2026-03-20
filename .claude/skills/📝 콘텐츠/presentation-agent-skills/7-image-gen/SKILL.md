---
name: ppt-image-gen
description: |
  PPT 슬라이드용 AI 이미지 생성 Skill. Gemini CLI(Nano Banana)를 활용하여
  프레젠테이션에 최적화된 비주얼 이미지를 자동 생성합니다.
  모든 슬라이드에 대해 테마와 일관된 스타일의 이미지를 생성하고 저장합니다.
triggers:
  - "이미지 생성"
  - "비주얼 만들어"
  - "일러스트 필요"
  - "배경 이미지"
  - "아이콘 생성"
---

# PPT Image Gen Skill

Gemini CLI의 Nano Banana 확장을 활용한 PPT 슬라이드용 AI 이미지 생성 Skill입니다.
모든 슬라이드에 테마와 일관된 스타일의 전문적인 비주얼을 자동으로 생성합니다.

> **필수 요건:**
> - Gemini CLI 설치 (`/opt/homebrew/bin/gemini`)
> - Nano Banana 확장 설치
> - `NANOBANANA_GEMINI_API_KEY` 또는 `GEMINI_API_KEY` 환경 변수 설정

## 핵심 원칙

> **"Describe the scene, don't just list keywords."**
> — Google Developers Blog

Gemini는 키워드 나열보다 **자연스러운 설명 문장**에서 더 좋은 결과를 생성합니다.

## 이미지 유형 분류

| 유형 | 설명 | 용도 | 권장 사이즈 |
|------|------|------|------------|
| **background** | 전체 슬라이드 배경 | Cover, Section Divider | 1920x1080 |
| **concept** | 개념 시각화 일러스트 | Problem, Solution 슬라이드 | 800x600 |
| **icon** | 아이콘 스타일 요소 | 불릿 포인트, 프로세스 | 256x256 |
| **isometric** | 3D 아이소메트릭 | 기술, 프로세스 설명 | 600x600 |
| **abstract** | 추상적 비주얼 | 배경, 장식 요소 | 1200x800 |
| **product** | 제품/서비스 목업 | 소개, 데모 슬라이드 | 800x600 |

## 프롬프트 구조 (6-Part Framework)

> 출처: [Google Developers Blog](https://developers.googleblog.com/en/how-to-prompt-gemini-2-5-flash-image-generation-for-the-best-results/)

```
┌─────────────────────────────────────────────────────────────┐
│ 1. SUBJECT        │ 핵심 주제/객체 (무엇이 이미지에 있어야 하는가)   │
├─────────────────────────────────────────────────────────────┤
│ 2. COMPOSITION    │ 구도, 배경, 피사계 심도, 종횡비              │
├─────────────────────────────────────────────────────────────┤
│ 3. LIGHTING       │ 시간대, 조명 스타일, 렌즈 정보              │
├─────────────────────────────────────────────────────────────┤
│ 4. STYLE          │ 시각적 스타일, 아트 무브먼트, 컬러 팔레트      │
├─────────────────────────────────────────────────────────────┤
│ 5. CONSTRAINTS    │ 제외할 요소 (자연어로 명시)                  │
├─────────────────────────────────────────────────────────────┤
│ 6. OUTPUT SPEC    │ 해상도, 종횡비, 품질 설정                   │
└─────────────────────────────────────────────────────────────┘
```

## PPT 스타일별 프롬프트 템플릿

### 1. Flat Illustration (플랫 일러스트)

**특징:** 단순한 기하학적 형태, 솔리드 컬러, 미니멀한 디테일
**적합한 테마:** Education, Healthcare, Startup

```
Template:
"Flat vector illustration of [subject],
[color_palette] color scheme,
simple geometric shapes, clean lines,
minimalist style, no gradients,
white background, no text, no shadows,
centered composition, professional business style"

Example:
"Flat vector illustration of diverse team collaborating around a digital dashboard,
blue and cyan color scheme with orange accents,
simple geometric shapes, clean lines,
minimalist corporate memphis style, no gradients,
white background, no text, no shadows,
centered composition, professional business style"
```

### 2. Isometric 3D (아이소메트릭)

**특징:** 30도 각도의 3D 뷰, 기술적이고 모던한 느낌
**적합한 테마:** AI/Tech, Fintech, Real Estate

```
Template:
"Isometric 3D illustration of [subject],
[color_palette] with soft shadows,
clean geometric shapes, modern tech aesthetic,
white or light gray background,
no text, centered, high detail,
professional business technology style"

Example:
"Isometric 3D illustration of cloud computing infrastructure
with servers, data flow connections, and security shields,
deep blue and cyan with purple accents and soft shadows,
clean geometric shapes, modern tech aesthetic,
white background, no text, centered, high detail,
professional business technology style"
```

### 3. Corporate Memphis (코퍼레이트 멤피스)

**특징:** 밝은 색상, 단순화된 인물, 과장된 비율
**적합한 테마:** Startup, Creative, Education

```
Template:
"Corporate memphis style illustration of [subject],
[color_palette] vibrant colors,
simplified human figures with exaggerated proportions,
flat design, geometric background elements,
white background, no text,
modern corporate illustration style"

Example:
"Corporate memphis style illustration of remote workers
having a video conference with floating UI elements,
blue, orange, and pink vibrant colors,
simplified human figures with exaggerated proportions,
flat design, geometric background elements,
white background, no text,
modern corporate illustration style"
```

### 4. Minimalist Abstract (미니멀 추상)

**특징:** 단순한 형태, 여백 활용, 텍스트 오버레이에 적합
**적합한 테마:** Luxury, Executive, Consulting

```
Template:
"Minimalist abstract design for [purpose],
[color_palette] with [accent_color] accent,
clean geometric shapes, ample negative space,
soft gradients, no text,
[subject] positioned [position],
professional elegant aesthetic,
16:9 aspect ratio"

Example:
"Minimalist abstract design for presentation background,
warm beige and cream with terracotta accent,
clean geometric shapes, ample negative space,
soft gradients, no text,
subtle flowing curves positioned bottom-right,
professional elegant aesthetic,
16:9 aspect ratio"
```

### 5. Tech/Data Visualization (테크/데이터)

**특징:** 다크 테마, 네온 컬러, 데이터 플로우 느낌
**적합한 테마:** AI/Tech, Fintech, Developer

```
Template:
"Futuristic data visualization background,
dark [bg_color] background with [accent_colors] glow effects,
abstract neural network nodes, flowing data streams,
circuit patterns, subtle grid overlay,
no text, no faces,
cinematic lighting, high contrast,
16:9 aspect ratio, 4K quality"

Example:
"Futuristic data visualization background,
dark navy (#0a0a0f) background with cyan and purple glow effects,
abstract neural network nodes, flowing data streams,
circuit patterns, subtle grid overlay,
no text, no faces,
cinematic lighting, high contrast,
16:9 aspect ratio, 4K quality"
```

### 6. Nature/Sustainability (자연/지속가능성)

**특징:** 자연 요소, 그린 톤, 친환경적 느낌
**적합한 테마:** Sustainability, Healthcare, F&B

```
Template:
"Eco-friendly illustration of [subject],
earthy green and natural tones with [accent_color],
organic flowing shapes, leaf patterns,
soft watercolor texture, minimalist style,
light background, no text,
sustainable business aesthetic"

Example:
"Eco-friendly illustration of sustainable city concept
with green buildings, solar panels, and wind turbines,
earthy green and sage tones with warm wood accents,
organic flowing shapes, integrated nature elements,
soft watercolor texture, minimalist style,
light cream background, no text,
sustainable business aesthetic"
```

## 테마-스타일 자동 매핑

| PPT Theme | Primary Style | Secondary Style | 컬러 키워드 |
|-----------|---------------|-----------------|-------------|
| Healthcare | Flat Illustration | Minimalist | sage, teal, clean white |
| Education | Corporate Memphis | Flat | bright blue, orange, yellow |
| Fintech | Isometric 3D | Tech/Data | navy, gold, dark blue |
| AI/Tech | Tech/Data | Isometric | dark, cyan, purple, neon |
| Sustainability | Nature | Minimalist | green, earth tones, natural |
| Startup | Corporate Memphis | Isometric | gradient, purple, energetic |
| Luxury | Minimalist Abstract | - | black, gold, cream |
| Creative | Corporate Memphis | Abstract | neon, pink, vibrant |
| Real Estate | Isometric 3D | Minimalist | navy, gold, trustworthy |
| F&B | Nature | Flat | warm, appetizing, natural |

## 슬라이드 유형별 이미지 생성 가이드

### Cover Slide (표지)
```yaml
image_type: background
style: minimalist_abstract OR theme_specific
requirements:
  - 텍스트 오버레이 공간 확보 (중앙 또는 좌측)
  - 브랜드 컬러 반영
  - 16:9 비율
prompt_modifier: "ample negative space for text overlay, professional"
```

### Section Divider (섹션 구분)
```yaml
image_type: background
style: abstract OR theme_accent
requirements:
  - 강렬한 시각적 임팩트
  - 섹션 번호/제목 공간
  - 테마 컬러 강조
prompt_modifier: "dramatic, bold colors, space for large text"
```

### Content Slide (콘텐츠)
```yaml
image_type: concept OR icon
style: flat_illustration OR isometric
requirements:
  - 콘텐츠 보조 역할
  - 복잡하지 않은 구성
  - 우측 또는 좌측 배치
prompt_modifier: "supporting visual, clean composition"
```

### Statistics (통계)
```yaml
image_type: abstract OR icon
style: minimalist
requirements:
  - 숫자가 주인공
  - 배경 보조 역할만
  - 깔끔한 기하학적 요소
prompt_modifier: "subtle background element, geometric"
```

### Process/Timeline (프로세스)
```yaml
image_type: isometric OR icon_set
style: isometric_3d OR flat
requirements:
  - 단계별 일관된 스타일
  - 각 단계 식별 가능
  - 연결성 시각화
prompt_modifier: "step-by-step visual, consistent style across elements"
```

## 사전 설정

### 1. Gemini CLI 인증 (필수)

Gemini CLI에 Google 계정으로 로그인합니다:

```bash
# 첫 실행 시 자동으로 로그인 프롬프트 표시
gemini

# "Login with Google" 선택 후 브라우저에서 인증
# Pro/Advanced 구독 계정으로 로그인 시 더 높은 할당량 제공
```

### 2. Nano Banana 확장 설치 (이미지 생성용)

```bash
# Nano Banana 확장 설치
gemini extensions install https://github.com/gemini-cli-extensions/nanobanana

# 설치 확인
gemini extensions list
```

### 3. API 키 설정

> **중요**: Gemini CLI의 이미지 생성 기능(`/image`, `/icon` 등)은 Google 계정 로그인과 별도로
> API 키가 필요합니다. Pro 구독자도 이미지 생성에는 API 키 설정이 필요합니다.

```bash
# 방법 1: 환경 변수 설정 (권장)
export GEMINI_API_KEY="your-api-key-here"

# 방법 2: Nano Banana 전용 키 (대안)
export NANOBANANA_GEMINI_API_KEY="your-api-key-here"

# 방법 3: .zshrc에 영구 설정
echo 'export GEMINI_API_KEY="your-api-key-here"' >> ~/.zshrc
source ~/.zshrc
```

> **API 키 발급**: [Google AI Studio](https://aistudio.google.com/apikey)에서 무료로 발급받을 수 있습니다.
> Pro 구독자는 동일한 API 키로 더 높은 할당량(RPM)과 우선 접근 권한을 받습니다.

### 4. 설치 확인

```bash
# Gemini CLI 버전 확인
gemini --version

# 확장 목록 확인
gemini --list-extensions

# 이미지 생성 테스트
gemini -y "/image test blue circle on white background"
```

## Gemini CLI 사용법

### 이미지 생성 명령어

Nano Banana 확장 설치 후 사용 가능한 네이티브 명령어:

| 명령어 | 용도 | PPT 활용 |
|--------|------|----------|
| `/image [prompt]` | 사실적/예술적 이미지 | 배경, 개념 일러스트 |
| `/icon [prompt]` | 앱 아이콘, UI 요소 | 불릿 아이콘, 프로세스 요소 |
| `/diagram [prompt]` | 플로우차트, 아키텍처 | 프로세스, 시스템 구조 |
| `/pattern [prompt]` | 심리스 텍스처 | 배경 패턴 |
| `/edit [file] [prompt]` | 이미지 수정 | 기존 이미지 보정 |

### 기본 명령어

```bash
# 일반 이미지 생성
gemini -y "/image [prompt]"

# 아이콘 생성
gemini -y "/icon [prompt]"

# 다이어그램 생성
gemini -y "/diagram [prompt]"

# 패턴 생성
gemini -y "/pattern [prompt]"
```

> **자동 승인 옵션**:
> - `-y` 또는 `--yolo`: 모든 도구 자동 승인
> - `--approval-mode yolo`: 동일 기능 (둘 중 하나만 사용)

### 이미지 저장

```bash
# 이미지 생성 시 현재 디렉토리에 자동 저장
# 파일명: generated_image_[timestamp].png 또는 nanobanana_[timestamp].png

# 특정 디렉토리에서 실행하여 저장 위치 지정
cd output/project-name/images && gemini -y "/image [prompt]"
```

### PPT용 프롬프트 예시

```bash
# 배경 이미지 생성
gemini -y "/image Minimalist abstract background,
deep navy blue gradient with subtle gold geometric accents,
clean professional aesthetic, ample negative space for text,
no text, no watermarks, 16:9 aspect ratio, high resolution"

# 개념 일러스트 생성
gemini -y "/image Isometric 3D illustration of
team collaboration with connected digital workspace elements,
blue and cyan color scheme with soft shadows,
modern tech aesthetic, white background, no text,
professional business style"

# 아이콘 세트 생성
gemini -y "/icon minimalist check mark icon,
corporate blue color, rounded corners,
flat design style, transparent background"

# 프로세스 다이어그램
gemini -y "/diagram simple 3-step workflow diagram,
left to right flow, modern flat design,
blue and gray color scheme, no text labels"
```

### 배치 생성 스크립트

```bash
#!/bin/bash
# generate-ppt-images.sh

PROJECT_DIR="output/[project-name]"
IMAGES_DIR="$PROJECT_DIR/images"

mkdir -p "$IMAGES_DIR"
cd "$IMAGES_DIR"

# API 키 확인
if [ -z "$GEMINI_API_KEY" ] && [ -z "$NANOBANANA_GEMINI_API_KEY" ]; then
    echo "Error: GEMINI_API_KEY 환경 변수 설정 필요"
    echo "발급: https://aistudio.google.com/apikey"
    exit 1
fi

# 슬라이드별 이미지 생성
echo "Generating cover image..."
gemini -y "/image [cover_prompt]"
mv generated_image_*.png slide-01-cover.png 2>/dev/null || \
mv nanobanana_*.png slide-01-cover.png 2>/dev/null

echo "Generating concept illustration..."
gemini -y "/image [concept_prompt]"
mv generated_image_*.png slide-03-concept.png 2>/dev/null || \
mv nanobanana_*.png slide-03-concept.png 2>/dev/null

echo "Generating icons..."
gemini -y "/icon [icon_prompt]"
mv generated_icon_*.png icon-01.png 2>/dev/null

# 다이어그램
echo "Generating process diagram..."
gemini -y "/diagram [diagram_prompt]"
mv generated_diagram_*.png slide-05-process.png 2>/dev/null

echo "Done! Images saved to $IMAGES_DIR"
```

## 문제 해결

### 일반적인 오류

| 오류 메시지 | 원인 | 해결 방법 |
|------------|------|----------|
| `No valid API key found` | API 키 미설정 | `NANOBANANA_GEMINI_API_KEY` 환경 변수 설정 |
| `Cannot use both -y and --approval-mode` | 플래그 충돌 | `-y` 제거, `--approval-mode yolo`만 사용 |
| `Extension not found` | Nano Banana 미설치 | `gemini extensions install ...` 실행 |
| `thinking is not supported` | 잘못된 모델 | Nano Banana 확장 사용 확인 |

### API 키 확인

```bash
# 환경 변수 확인
echo $NANOBANANA_GEMINI_API_KEY
echo $GEMINI_API_KEY

# 키가 설정되어 있지 않다면 설정
export NANOBANANA_GEMINI_API_KEY="your-api-key"
```

## 이미지 품질 체크리스트

### 생성 전 확인
- [ ] 슬라이드 유형에 맞는 이미지 타입 선택
- [ ] 테마 컬러 팔레트 반영
- [ ] 적절한 사이즈/비율 설정
- [ ] 프롬프트에 "no text" 포함

### 생성 후 검증
- [ ] 텍스트가 포함되어 있지 않은가?
- [ ] 테마 컬러와 일관성 있는가?
- [ ] 슬라이드 맥락에 적합한가?
- [ ] 해상도가 충분한가? (최소 1920x1080 배경)
- [ ] 스타일이 다른 슬라이드와 일관적인가?

## 네거티브 프롬프트 (Semantic Exclusions)

PPT 이미지 생성 시 반드시 제외할 요소:

```
Standard Exclusions:
- "no text, no letters, no words, no typography"
- "no watermarks, no signatures"
- "no borders, no frames"
- "no realistic human faces" (법적 이슈 방지)
- "no copyrighted logos or brands"
- "no cluttered backgrounds"
```

### 스타일별 추가 제외

| 스타일 | 제외 요소 |
|--------|----------|
| Flat | no gradients, no shadows, no 3D effects |
| Isometric | no perspective distortion, no realistic textures |
| Minimalist | no complex patterns, no busy backgrounds |
| Tech/Data | no cartoon elements, no hand-drawn style |

## 대체 텍스트 (Alt Text) 자동 생성

접근성을 위한 alt text 생성 템플릿:

```
Template:
"[image_type]: [brief_description] in [style] style, featuring [key_elements], using [color_description] color scheme"

Example:
"Concept illustration: Team collaboration in flat vector style, featuring four people around a digital screen, using blue and orange color scheme"
```

## 폴백 옵션

이미지 생성 실패 시 대안:

1. **재시도**: 프롬프트 단순화 후 재생성
2. **스타일 변경**: 복잡한 스타일 → 단순 스타일
3. **아이콘 대체**: Lucide/Phosphor 아이콘으로 대체
4. **컬러 블록**: 테마 컬러의 단순 그라데이션 배경
5. **Unsplash**: 무료 스톡 이미지 검색 제안

```yaml
fallback_priority:
  1: retry_simplified_prompt
  2: switch_to_simpler_style
  3: use_icon_library
  4: color_gradient_background
  5: suggest_stock_image
```

## 이미지 저장 규칙

### 파일 구조

```
output/[project-name]/
├── images/
│   ├── slide-01-cover.png
│   ├── slide-02-contents.png
│   ├── slide-03-section-problem.png
│   ├── slide-05-concept-solution.png
│   ├── icons/
│   │   ├── icon-check.png
│   │   ├── icon-chart.png
│   │   └── icon-team.png
│   └── backgrounds/
│       ├── bg-gradient-dark.png
│       └── bg-abstract-light.png
├── slides/
└── ...
```

### 파일 명명 규칙

```
[slide-number]-[type]-[description].png

Examples:
- slide-01-cover-main.png
- slide-05-concept-automation.png
- slide-08-bg-section-results.png
- icon-process-step1.png
```

## 스타일 일관성 유지

### 세션 스타일 시드

동일 PPT 내 모든 이미지의 일관성을 위한 공통 프롬프트 요소:

```yaml
session_style:
  color_palette: "[테마에서 추출]"
  style_keywords: "[flat/isometric/minimalist]"
  common_modifiers: "clean, professional, modern, no text"
  quality_spec: "high resolution, sharp details"
```

### 프롬프트 공통 Suffix

```
", consistent with previous images in this presentation,
[theme_color_palette], professional business aesthetic,
no text, no watermarks, high quality"
```

## 워크플로우 통합

```
┌─────────────────────────────────────────────────────────────┐
│                     PPT Agent Workflow                       │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  Content Skill                                               │
│       │                                                      │
│       ▼                                                      │
│  Design System Skill                                         │
│       │ ─── 테마 정보 전달 ───┐                              │
│       │                        │                             │
│       ▼                        ▼                             │
│  Visual Skill            Image Gen Skill                     │
│  (차트/다이어그램)         (AI 이미지 생성)                    │
│       │                        │                             │
│       └────────┬───────────────┘                             │
│                │                                             │
│                ▼                                             │
│           Review Skill                                       │
│           (이미지 품질 검토 포함)                              │
│                │                                             │
│                ▼                                             │
│         Export Skills                                        │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

## 입력/출력 명세

### 입력

```yaml
input:
  slide_info:
    number: 5
    type: "solution"
    title: "3단계 자동화로 오류율 90% 감소"
    key_concepts: ["자동화", "AI", "효율성"]

  theme:
    name: "ai-tech"
    colors:
      primary: "#667eea"
      secondary: "#00d9ff"
      background: "#0a0a0f"
    style: "tech_futuristic"

  image_request:
    type: "concept"
    position: "right"
    size: "half-slide"
```

### 출력

```yaml
output:
  image:
    path: "output/project/images/slide-05-concept-automation.png"
    dimensions: "800x600"
    format: "PNG"

  prompt_used: "[생성에 사용된 전체 프롬프트]"

  alt_text: "Concept illustration: Three-step automation process
             in isometric 3D style, featuring connected workflow
             nodes with AI elements, using blue and cyan color scheme"

  metadata:
    generated_at: "2025-01-06T10:30:00Z"
    model: "gemini-3-flash"  # or "gemini-3-pro" for higher quality
    style: "isometric_3d"
    retry_count: 0
```

## 참고 자료

### 프롬프트 엔지니어링 가이드
- [Google Developers Blog - Gemini 2.5 Flash Image Generation](https://developers.googleblog.com/en/how-to-prompt-gemini-2-5-flash-image-generation-for-the-best-results/)
- [AI SuperHub - 50+ Nano Banana Prompts](https://www.aisuperhub.io/blog/prompt-engineering-for-gemini-25-flash-image-nano-banana-50plus-image-prompts-included)

### 스타일 레퍼런스
- [Flat Illustration Series Template](https://docsbot.ai/prompts/creative/flat-illustration-series)
- [Midjourney Isometric Prompts](https://openart.ai/blog/post/midjourney-prompts-for-isometric)

### 비즈니스 프레젠테이션 비주얼
- [Superside AI Prompts for Presentations](https://www.superside.com/blog/ai-prompts-presentations)
- [SlidesAI Presentation Prompts](https://www.slidesai.io/blog/prompts-to-make-presentations-with-ai)

## 주의사항

1. **저작권**: 브랜드 로고, 유명인 초상 등 저작권 이슈 요소 배제
2. **일관성**: 동일 PPT 내 스타일 통일 유지
3. **맥락 적합성**: 슬라이드 내용과 이미지의 관련성 확인
4. **파일 크기**: 고해상도 유지하되 파일 크기 최적화
5. **대체 텍스트**: 모든 이미지에 접근성용 alt text 필수
6. **텍스트 제외**: PPT 이미지에는 텍스트 포함하지 않음 (슬라이드에서 별도 추가)
