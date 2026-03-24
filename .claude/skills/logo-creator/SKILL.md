---
name: logo-creator
description: AI 로고 생성 전용 스킬. 브랜드 디스커버리 → 배치 생성(20개) → HTML 프리뷰 → 반복 → Crop/배경제거/SVG 변환까지 End-to-End. Gemini + 로컬 오픈소스만 사용 (유료 API 0개). "로고 만들어줘", "logo", "brand mark", "favicon", "앱 아이콘" 요청에 반응.
---

# Logo Creator Skill

AI 이미지 생성을 활용한 전문 로고 제작 스킬.

## 범위 (Scope)

**이 스킬의 핵심 역할: 로고 전문 특화 (SPECIALIZED)**
- **브랜드 디스커버리** — 업종/스타일/컬러 요구사항 수집
- **배치 생성** — 20개 로고 동시 생성 (Gemini Flash/Pro)
- **HTML 프리뷰** — 갤러리 형태로 로고 비교/선택
- **반복 생성** — 사용자 피드백 기반 변형 생성
- **후처리** — Crop, 배경 제거 (rembg), SVG 벡터화 (potrace)
- **최종 에셋 전달** — PNG/투명 PNG/SVG 멀티 포맷

**이 스킬이 절대 처리하지 않는 것:**
- 배너/커버/헤더 디자인 → `banner-design`
- CIP (명함, 레터헤드 등) → `design`
- SVG 아이콘 생성 → `design`
- UI 컴포넌트 코드 → `ui-styling`
- 디자인 토큰/시스템 → `design-system`

## 위임 (Delegates to)

| 요청 내용 | 위임 대상 | 조건 |
|-----------|-----------|------|
| 로고 완성 후 CIP 제작 | `design` | 로고 → CIP 파이프라인 |
| 로고 스타일 리서치 | `design` 내 BM25 검색 | 스타일/컬러/산업 가이드 조회 |
| HTML 프리뷰 갤러리 디자인 | `ui-ux-pro-max` | 프리뷰 페이지 디자인 시 |

## 이 스킬을 사용하지 않는 경우

- 배너/소셜 커버를 만들 때 → `banner-design`
- CIP/명함/레터헤드를 만들 때 → `design`
- UI 아이콘을 만들 때 → `design` (아이콘 빌트인)
- UI 컴포넌트를 코딩할 때 → `ui-styling`
- 브랜드 전체 패키지를 만들 때 → `design` (오케스트레이션) → 이 스킬은 로고 부분만 담당

## Prerequisites

**필수 환경변수:**
- `GEMINI_API_KEY` - [Google AI Studio](https://aistudio.google.com/apikey)에서 발급

**필수 Python 패키지:**
```bash
pip install google-genai pillow numpy
```

**선택 패키지 (후처리용):**
```bash
pip install rembg                 # 배경 제거 (로컬, 무료)
brew install potrace              # SVG 벡터화 (로컬, 무료)
```

## 파일 출력 위치

모든 생성 파일은 프로젝트 루트의 `.skill-output/logo-creator/` 에 저장:

```
.skill-output/logo-creator/<yyyy-mm-dd-브랜드명>/
  logo-01.png ~ logo-20.png       # 배치 생성 결과
  logo-05-v1.png ~ logo-05-v5.png  # 반복 변형
  logo-05-cropped.png              # 여백 제거
  logo-05-nobg.png                 # 배경 투명화
  logo-05.svg                      # 벡터 변환
  preview.html                     # 프리뷰 갤러리
```

## Workflow

### Step 1: Discovery & Requirements

로고 생성 전 반드시 사용자에게 확인:

1. **브랜드/프로젝트명** — 로고의 대상
2. **업종/산업** — tech, healthcare, food, fashion 등 (55개 산업 DB 보유)
3. **스타일 선호** — 20가지 스타일 중 선택 (또는 "알아서"):
   - minimalist, modern, geometric, gradient, abstract
   - lettermark, negative-space, lineart, 3d, vintage
   - emblem, mascot, hand-drawn, luxury, flat
   - pixel-art, monoline, wordmark, circular, organic
4. **컬러 선호** — 모노크롬, 특정 브랜드 컬러, AI 추천 (55개 팔레트 DB)
5. **비율** — 1:1 (기본), 16:9, 4:3 등
6. **레퍼런스** — 참고할 기존 로고나 스타일

**사용자 확인 후 다음 단계로!**

### Step 2: Design Brief (자동)

BM25 검색 엔진으로 최적 스타일/컬러/산업 가이드 자동 추천:

```bash
python3 <design_skill>/scripts/logo/search.py "<query>" --design-brief -p "<brand>"
```

결과를 바탕으로 프롬프트를 강화한다.

### Step 3: Batch Generate (20개)

```bash
python3 <skill_dir>/scripts/batch.py \
  --brand "BrandName" \
  --prompt "description of the brand" \
  --industry tech \
  --count 20 \
  --output-dir .skill-output/logo-creator/<yyyy-mm-dd-brand>/
  # --pro  # 고품질 (Gemini Pro) 사용 시
```

**모델 선택:**
- `gemini-2.5-flash-image` (기본) — 빠른 생성, 대량 변형
- `gemini-3-pro-image-preview` (`--pro`) — 고품질, 정교한 디테일

**프롬프트 팁:**
- 스타일 키워드: "pixel art", "minimalist", "8-bit", "flat design"
- 컬러 지정: "black on white", "monochrome", "blue gradient"
- 맥락 추가: "tech startup", "food brand", "gaming company"
- 형태 지정: "icon", "emblem", "mascot", "lettermark"

### Step 4: HTML Preview & 선택

배치 생성 완료 시 자동으로 preview.html 생성:

```bash
open .skill-output/logo-creator/<yyyy-mm-dd-brand>/preview.html
```

**프리뷰 기능:**
- 다크/화이트/체커보드 배경 전환
- 클릭으로 확대, 더블클릭으로 즐겨찾기
- 키보드: 좌우 화살표(탐색), F(즐겨찾기), Escape(닫기)
- 검색 필터
- 즐겨찾기 목록 하단 표시

사용자에게 물어본다:
- "어떤 로고가 마음에 드세요? (예: #5, #12, #18)"
- "어떤 점이 좋은가요?"
- "수정하고 싶은 부분이 있나요?"

### Step 5: Iterate (반복 생성)

선호 로고를 기반으로 추가 변형 생성:

```bash
python3 <skill_dir>/scripts/batch.py \
  --brand "BrandName" \
  --prompt "원래 프롬프트 + 사용자 피드백 반영" \
  --count 10 \
  --prefix "logo-05-v" \
  --output-dir .skill-output/logo-creator/<yyyy-mm-dd-brand>/
```

- 사용자가 만족할 때까지 반복
- 매 반복마다 preview.html 업데이트

### Step 6: Finalize (후처리)

사용자가 최종 로고를 선택하면:

**6a. Crop (여백 제거 + 1:1 센터링):**
```bash
python3 <skill_dir>/scripts/crop.py logo-05.png logo-05-cropped.png
# --padding 10  # 패딩 조절
# --threshold 240  # 흰색 감도 조절
```

**6b. Remove Background (배경 투명화):**
```bash
python3 <skill_dir>/scripts/remove_bg.py logo-05-cropped.png logo-05-nobg.png
```

**6c. Vectorize (SVG 변환):**
```bash
python3 <skill_dir>/scripts/vectorize.py logo-05-nobg.png logo-05.svg
# --threshold 128  # 이진화 임계값 조절
```

### Step 7: Deliver

최종 에셋 전달:

```
## Final Logo Assets

| 파일 | 설명 | 용도 |
|------|------|------|
| logo.png | 원본 | 소스 파일 |
| logo-cropped.png | 여백 제거 1:1 | 앱 아이콘, 파비콘 |
| logo-nobg.png | 투명 배경 | 웹, 인쇄 |
| logo.svg | 벡터 (무한 확대) | 인쇄, 대형 |

모든 파일: .skill-output/logo-creator/<yyyy-mm-dd-brand>/
```

사용자가 원하는 위치로 최종 로고 복사.

## Quick Reference

### 스타일 (20종)

| 스타일 | 설명 | 적합한 용도 |
|--------|------|-------------|
| minimalist | 심플, 기하학적, 여백 | 테크, SaaS, 전문직 |
| modern | 그라데이션, 세련된 | 스타트업, 앱 |
| geometric | 정밀한 기하학 패턴 | 테크, 건축 |
| gradient | 컬러 트랜지션 | 디지털, 앱 |
| abstract | 비구상, 상징적 | 컨설팅, 테크 |
| lettermark | 이니셜/모노그램 | 개인 브랜드, 럭셔리 |
| negative-space | 네거티브 스페이스 활용 | 크리에이티브 |
| lineart | 단일 선, 연속 | 미니멀, 아트 |
| 3d | 입체감, 아이소메트릭 | 게임, 테크 |
| vintage | 레트로, 뱃지 스타일 | 카페, 수제 브랜드 |
| emblem | 문장, 실드 형태 | 스포츠, 전통 |
| mascot | 캐릭터, 마스코트 | 푸드, 게임, 키즈 |
| hand-drawn | 손그림, 스케치 | 아티산, 크리에이티브 |
| luxury | 고급, 골드 악센트 | 패션, 주얼리 |
| flat | 플랫 디자인, 단색 | 앱, 웹 |
| pixel-art | 8비트, 레트로 게임 | 게임, 인디 |
| monoline | 단일 선 두께 | 모던, 미니멀 |
| wordmark | 브랜드명 타이포 | 미디어, 패션 |
| circular | 원형 구도 | 스탬프, 뱃지 |
| organic | 자연스러운 곡선 | 에코, 헬스 |

### Aspect Ratios

| 비율 | 용도 |
|------|------|
| 1:1 | 파비콘, 앱 아이콘, 소셜 아바타 (기본) |
| 16:9 | 웹사이트 헤더, 프레젠테이션 |
| 4:3 | 전통적 포맷 |
| 9:16 | 모바일, 세로 배너 |
| 3:4 | 포트레이트 |

### 의존성 요약

| 도구 | 용도 | 설치 | 비용 |
|------|------|------|------|
| Gemini API | 이미지 생성 | `GEMINI_API_KEY` | 무료 티어 |
| rembg | 배경 제거 | `pip install rembg` | 무료 |
| potrace | SVG 변환 | `brew install potrace` | 무료 |
| Pillow | 이미지 처리 | `pip install pillow` | 무료 |
