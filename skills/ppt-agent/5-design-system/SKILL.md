---
name: ppt-design-system
description: |
  전문 프레젠테이션 디자인 시스템. 정밀한 타이포그래피, 10가지 토픽별 테마, 10가지 슬라이드 템플릿 제공.
  "디자인 적용", "템플릿", "스타일 시스템" 요청 시 활성화.
---

# PPT Design System Skill

전문적인 프레젠테이션 디자인을 위한 정밀 시스템입니다.
**"Less is More"** 철학을 기반으로 불필요한 요소를 제거하고 콘텐츠에 집중합니다.

## Topic-Based Themes (10가지)

각 주제에 맞는 전문 테마가 별도 파일로 분리되어 있습니다:

| Theme | File | Use Case |
|-------|------|----------|
| Healthcare Clean | [themes/01-healthcare/](./themes/01-healthcare/THEME.md) | 의료, 바이오, 헬스케어 |
| Education Bright | [themes/02-education/](./themes/02-education/THEME.md) | 교육, 트레이닝, 워크샵 |
| Fintech Bold | [themes/03-fintech/](./themes/03-fintech/THEME.md) | 핀테크, 금융, 크립토 |
| AI Futuristic | [themes/04-ai-tech/](./themes/04-ai-tech/THEME.md) | AI/ML, 테크, 개발자 |
| Sustainability Earth | [themes/05-sustainability/](./themes/05-sustainability/THEME.md) | ESG, 환경, 지속가능성 |
| Startup Gradient | [themes/06-startup/](./themes/06-startup/THEME.md) | 피치덱, 스타트업, VC |
| Luxury Noir | [themes/07-luxury/](./themes/07-luxury/THEME.md) | 럭셔리, 프리미엄, VIP |
| Creative Neon | [themes/08-creative/](./themes/08-creative/THEME.md) | 에이전시, 디자인, 포트폴리오 |
| Real Estate Trust | [themes/09-real-estate/](./themes/09-real-estate/THEME.md) | 부동산, 투자, 자산 |
| F&B Appetite | [themes/10-fnb/](./themes/10-fnb/THEME.md) | 식음료, 레스토랑, 호텔 |

> **Theme Selection:** [themes/INDEX.md](./themes/INDEX.md) - 테마 선택 가이드 및 키워드 매핑

## 슬라이드 규격

### 표준 크기 (포인트 단위)

| 비율 | 너비 | 높이 | 용도 |
|------|------|------|------|
| **16:9** | 720pt | 405pt | 표준 (권장) |
| 16:10 | 720pt | 450pt | 맥북/태블릿 |
| 4:3 | 720pt | 540pt | 레거시 프로젝터 |

### 단위 변환

```
1 inch = 72pt = 96px = 914400 EMU
PT_PER_PX = 0.75
PX_PER_IN = 96
```

## 타이포그래피 시스템

### 기본 폰트

**Primary:** Pretendard (한글) / Inter (영문)

```html
<link rel="stylesheet" href="https://cdn.jsdelivr.net/gh/orioncactus/pretendard/dist/web/static/pretendard.css">
```

### 폰트 크기 계층

| 레벨 | 크기 | 굵기 | 자간 | 행간 | 용도 |
|------|------|------|------|------|------|
| **Hero** | 72-96pt | 700 | -0.02em | 1.1 | 타이틀 슬라이드 |
| **Section Title** | 48-60pt | 700 | -0.02em | 1.2 | 섹션 구분 |
| **Slide Title** | 32-40pt | 600 | -0.01em | 1.3 | 슬라이드 제목 |
| **Subtitle** | 20-24pt | 500 | 0 | 1.4 | 부제목 |
| **Body** | 16-20pt | 400 | 0 | 1.6 | 본문 |
| **Caption** | 12-14pt | 400 | 0.02em | 1.5 | 캡션/출처 |
| **Label** | 10-12pt | 500 | 0.05em | 1.4 | 라벨/태그 |

### 타이포그래피 CSS

```css
:root {
  /* Font Sizes */
  --font-hero: 84pt;
  --font-section: 54pt;
  --font-title: 36pt;
  --font-subtitle: 22pt;
  --font-body: 18pt;
  --font-caption: 13pt;
  --font-label: 11pt;

  /* Font Weights */
  --weight-bold: 700;
  --weight-semibold: 600;
  --weight-medium: 500;
  --weight-regular: 400;

  /* Line Heights */
  --lh-tight: 1.1;
  --lh-heading: 1.3;
  --lh-body: 1.6;
}

/* Title Style */
.slide-title {
  font-size: var(--font-title);
  font-weight: var(--weight-semibold);
  letter-spacing: -0.01em;
  line-height: var(--lh-heading);
}

/* Body Style */
.slide-body {
  font-size: var(--font-body);
  font-weight: var(--weight-regular);
  line-height: var(--lh-body);
}
```

## 5가지 컬러 팔레트

### 1. Executive Minimal (이그제큐티브 미니멀)

**용도:** 임원 보고, 투자자 피치, 프리미엄 발표

```css
:root {
  --bg-primary: #f5f5f0;      /* Warm White */
  --bg-secondary: #ffffff;
  --text-primary: #1a1a1a;     /* Almost Black */
  --text-secondary: #666666;
  --accent: #2d2d2d;
  --border: #e0e0e0;
}
```

| 역할 | HEX | 용도 |
|------|-----|------|
| Background | #f5f5f0 | 메인 배경 |
| Card | #ffffff | 카드, 섹션 |
| Text Primary | #1a1a1a | 제목, 강조 |
| Text Secondary | #666666 | 본문 |
| Accent | #2d2d2d | 버튼, 강조 |
| Border | #e0e0e0 | 구분선 |

### 2. Sage Professional (세이지 프로페셔널)

**용도:** 컨설팅, 헬스케어, 환경/ESG

```css
:root {
  --bg-primary: #f8faf8;
  --bg-secondary: #ffffff;
  --text-primary: #1a1a1a;
  --text-secondary: #4a5548;
  --accent: #b8c4b8;           /* Sage Green */
  --accent-dark: #7a8a78;
  --border: #dce3dc;
}
```

| 역할 | HEX | 용도 |
|------|-----|------|
| Background | #f8faf8 | 메인 배경 |
| Accent | #b8c4b8 | 강조, 아이콘 |
| Accent Dark | #7a8a78 | 호버, CTA |
| Text | #4a5548 | 본문 텍스트 |

### 3. Modern Dark (모던 다크)

**용도:** 테크 세미나, 스타트업, 개발자 발표

```css
:root {
  --bg-primary: #0f0f0f;       /* Pure Dark */
  --bg-secondary: #1a1a1a;
  --bg-card: #252525;
  --text-primary: #ffffff;
  --text-secondary: #a0a0a0;
  --accent: #667eea;           /* Primary Blue */
  --accent-secondary: #764ba2;  /* Purple */
  --gradient: linear-gradient(135deg, #667eea, #764ba2);
}
```

| 역할 | HEX | 용도 |
|------|-----|------|
| Background | #0f0f0f | 메인 배경 |
| Card | #252525 | 카드, 코드블록 |
| Text Primary | #ffffff | 제목 |
| Text Secondary | #a0a0a0 | 본문 |
| Accent | #667eea | 링크, 강조 |
| Gradient | #667eea→#764ba2 | 배경, CTA |

### 4. Corporate Blue (코퍼레이트 블루)

**용도:** 기업 발표, 금융, 공공기관

```css
:root {
  --bg-primary: #ffffff;
  --bg-secondary: #f0f4f8;
  --text-primary: #0d1b2a;     /* Navy */
  --text-secondary: #415a77;
  --accent: #1b4965;           /* Corporate Blue */
  --accent-light: #5fa8d3;
  --border: #cad2d8;
}
```

| 역할 | HEX | 용도 |
|------|-----|------|
| Background | #ffffff | 메인 배경 |
| Secondary BG | #f0f4f8 | 섹션 구분 |
| Navy | #0d1b2a | 제목 |
| Corporate Blue | #1b4965 | 강조 |
| Light Blue | #5fa8d3 | 차트, 아이콘 |

### 5. Warm Neutral (웜 뉴트럴)

**용도:** 마케팅, 라이프스타일, 브랜드 발표

```css
:root {
  --bg-primary: #faf8f5;       /* Cream */
  --bg-secondary: #ffffff;
  --text-primary: #2d2a26;
  --text-secondary: #6b635a;
  --accent: #c45a3b;           /* Terracotta */
  --accent-light: #e8a090;
  --border: #e5e0d8;
}
```

| 역할 | HEX | 용도 |
|------|-----|------|
| Background | #faf8f5 | 메인 배경 |
| Text Primary | #2d2a26 | 제목 |
| Terracotta | #c45a3b | CTA, 강조 |
| Accent Light | #e8a090 | 하이라이트 |

## 레이아웃 시스템

### 여백 (Padding)

```css
:root {
  --pad-slide: 48pt;      /* 슬라이드 외곽 */
  --pad-section: 32pt;    /* 섹션 간격 */
  --pad-element: 16pt;    /* 요소 간격 */
  --pad-inner: 8pt;       /* 내부 간격 */
}
```

### 그리드 시스템

```css
/* 2-Column Equal */
.grid-2 {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 32pt;
}

/* 3-Column Equal */
.grid-3 {
  display: grid;
  grid-template-columns: 1fr 1fr 1fr;
  gap: 24pt;
}

/* Asymmetric (Golden Ratio) */
.grid-golden {
  display: grid;
  grid-template-columns: 1fr 1.618fr;
  gap: 32pt;
}

/* Content + Visual */
.grid-content-visual {
  display: grid;
  grid-template-columns: 2fr 3fr;
  gap: 32pt;
}
```

### 레이아웃 영역 구성

```
┌──────────────────────────────────────────────────┐
│                   HEADER (48pt)                   │
│  [Section Badge]              [Page Number]       │
├──────────────────────────────────────────────────┤
│                                                   │
│                                                   │
│                 MAIN CONTENT                      │
│                  (309pt)                          │
│                                                   │
│                                                   │
├──────────────────────────────────────────────────┤
│                   FOOTER (48pt)                   │
│  [Source/Notes]                    [Logo]         │
└──────────────────────────────────────────────────┘

Content Area: 720pt - 96pt (양쪽 padding) = 624pt 너비
              405pt - 96pt (상하 padding) = 309pt 높이
```

## 10가지 슬라이드 템플릿

### 1. Cover Slide (표지)

```
┌──────────────────────────────────────────────────┐
│                                                   │
│  [Logo]                                           │
│                                                   │
│                                                   │
│           [HERO TITLE]                            │
│           [Subtitle - Date]                       │
│                                                   │
│                                                   │
│  [Presenter Name]              [Contact Info]     │
└──────────────────────────────────────────────────┘
```

**요소 스펙:**
- Hero Title: 72-84pt, Bold, 중앙 정렬
- Subtitle: 20-24pt, Regular
- Presenter: 14pt, 좌하단
- Logo: 우상단 또는 좌상단

### 2. Contents (목차)

```
┌──────────────────────────────────────────────────┐
│  CONTENTS                                         │
├──────────────────────────────────────────────────┤
│                                                   │
│  01  Introduction ........................... 03  │
│  02  Problem Statement ...................... 05  │
│  03  Solution ............................... 08  │
│  04  Implementation ......................... 12  │
│  05  Conclusion ............................. 18  │
│                                                   │
└──────────────────────────────────────────────────┘
```

**요소 스펙:**
- Section Number: 24pt, Bold, Accent Color
- Section Title: 20pt, Regular
- Page Number: 16pt, Text Secondary
- 행 간격: 48pt

### 3. Section Divider (섹션 구분)

```
┌──────────────────────────────────────────────────┐
│░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░│
│░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░│
│░░                                            ░░░░│
│░░  01                                        ░░░░│
│░░  SECTION TITLE                             ░░░░│
│░░  Brief description of this section         ░░░░│
│░░                                            ░░░░│
│░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░│
└──────────────────────────────────────────────────┘
```

**요소 스펙:**
- Background: 풀스크린 이미지 또는 Accent Color
- Section Number: 96pt, Bold, White/Contrast
- Title: 48-60pt
- Description: 18pt, 1-2줄

### 4. Content Slide (콘텐츠)

```
┌──────────────────────────────────────────────────┐
│  [Section] ─────────────────────────────── [03]  │
├──────────────────────────────────────────────────┤
│                                                   │
│  SLIDE HEADLINE                                   │
│                                                   │
│  ┌─────────────────┐  ┌─────────────────────────┐ │
│  │                 │  │                         │ │
│  │   • Point 1     │  │      [Visual]          │ │
│  │   • Point 2     │  │                         │ │
│  │   • Point 3     │  │                         │ │
│  │                 │  │                         │ │
│  └─────────────────┘  └─────────────────────────┘ │
├──────────────────────────────────────────────────┤
│  [Source/Note]                          [Logo]    │
└──────────────────────────────────────────────────┘
```

**요소 스펙:**
- Header: Section Badge + Page Number
- Headline: 32-36pt, Bold
- Content: 2-column (1fr 1.5fr)
- Bullets: 16-18pt, 1.6 line-height
- Footer: 12pt caption

### 5. Statistics (통계/수치)

```
┌──────────────────────────────────────────────────┐
│  KEY METRICS                                      │
├──────────────────────────────────────────────────┤
│                                                   │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐        │
│  │          │  │          │  │          │        │
│  │   85%    │  │   2.5x   │  │   $1.2M  │        │
│  │          │  │          │  │          │        │
│  │ Accuracy │  │  Speed   │  │ Revenue  │        │
│  │          │  │          │  │          │        │
│  └──────────┘  └──────────┘  └──────────┘        │
│                                                   │
└──────────────────────────────────────────────────┘
```

**요소 스펙:**
- Metric Value: 60-72pt, Bold, Accent Color
- Metric Label: 16pt, Text Secondary
- Card: 배경색 차별화, 8pt radius
- 3-column grid, equal spacing

### 6. Split Layout (분할)

```
┌──────────────────────────────────────────────────┐
│                                                   │
│  ┌───────────────────┐  ┌───────────────────────┐│
│  │                   │  │                       ││
│  │                   │  │  HEADLINE             ││
│  │    [IMAGE]        │  │                       ││
│  │                   │  │  Description text     ││
│  │                   │  │  goes here with       ││
│  │                   │  │  supporting details.  ││
│  │                   │  │                       ││
│  │                   │  │  [CTA Button]         ││
│  └───────────────────┘  └───────────────────────┘│
│                                                   │
└──────────────────────────────────────────────────┘
```

**요소 스펙:**
- Layout: 50/50 또는 40/60
- Image: 전체 높이, object-fit: cover
- Text Area: 48pt padding
- CTA: 버튼 스타일, Accent Color

### 7. Team Slide (팀 소개)

```
┌──────────────────────────────────────────────────┐
│  OUR TEAM                                         │
├──────────────────────────────────────────────────┤
│                                                   │
│  ┌────────┐  ┌────────┐  ┌────────┐  ┌────────┐  │
│  │ [Photo]│  │ [Photo]│  │ [Photo]│  │ [Photo]│  │
│  │        │  │        │  │        │  │        │  │
│  │  Name  │  │  Name  │  │  Name  │  │  Name  │  │
│  │  Role  │  │  Role  │  │  Role  │  │  Role  │  │
│  └────────┘  └────────┘  └────────┘  └────────┘  │
│                                                   │
└──────────────────────────────────────────────────┘
```

**요소 스펙:**
- Photo: 정사각형 또는 원형, 120pt
- Name: 16pt, Bold
- Role: 14pt, Text Secondary
- 4-column grid

### 8. Quote Slide (인용)

```
┌──────────────────────────────────────────────────┐
│                                                   │
│                                                   │
│           ❝                                       │
│           The only way to do great work           │
│           is to love what you do.                 │
│           ❞                                       │
│                                                   │
│                     — Steve Jobs                  │
│                       CEO, Apple                  │
│                                                   │
│                                                   │
└──────────────────────────────────────────────────┘
```

**요소 스펙:**
- Quote Mark: 72pt, Accent Color, 상단
- Quote Text: 32-40pt, Italic 또는 Regular
- Attribution: 18pt, Text Secondary
- 중앙 정렬, 좌우 padding 증가 (80pt)

### 9. Timeline (타임라인)

```
┌──────────────────────────────────────────────────┐
│  ROADMAP                                          │
├──────────────────────────────────────────────────┤
│                                                   │
│      Q1        Q2        Q3        Q4            │
│       ●─────────●─────────●─────────●            │
│       │         │         │         │            │
│    ┌──┴──┐   ┌──┴──┐   ┌──┴──┐   ┌──┴──┐        │
│    │Plan │   │Build│   │Test │   │Launch│        │
│    │     │   │     │   │     │   │     │        │
│    └─────┘   └─────┘   └─────┘   └─────┘        │
│                                                   │
└──────────────────────────────────────────────────┘
```

**요소 스펙:**
- Timeline Line: 2pt, Accent Color
- Milestone Dot: 12pt 원, filled
- Label: 14pt, Bold
- Description Card: 16pt, 카드 스타일

### 10. Closing Slide (마무리)

```
┌──────────────────────────────────────────────────┐
│░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░│
│░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░│
│░░                                            ░░░░│
│░░            [Logo]                          ░░░░│
│░░                                            ░░░░│
│░░          Thank You                         ░░░░│
│░░                                            ░░░░│
│░░       email@company.com                    ░░░░│
│░░       www.company.com                      ░░░░│
│░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░│
└──────────────────────────────────────────────────┘
```

**요소 스펙:**
- Background: Dark 또는 Brand Color
- Thank You: 48-60pt, Bold, White
- Contact: 16pt, 중앙 정렬
- Logo: 상단 중앙

## 컴포넌트 라이브러리

### Badge (뱃지)

```css
.badge {
  display: inline-block;
  padding: 6pt 14pt;
  font-size: 11pt;
  font-weight: 500;
  letter-spacing: 0.05em;
  text-transform: uppercase;
  border: 1pt solid currentColor;
  border-radius: 4pt;
}
```

### Card (카드)

```css
.card {
  background: var(--bg-secondary);
  padding: 24pt;
  border-radius: 12pt;
  box-shadow: 0 2pt 8pt rgba(0, 0, 0, 0.08);
}
```

### Icon Button (아이콘 버튼)

```css
.icon-button {
  width: 32pt;
  height: 32pt;
  border: 1pt solid var(--border);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
}
```

### Divider (구분선)

```css
.divider {
  height: 1pt;
  background: var(--border);
  margin: 24pt 0;
}
```

## 디자인 적용 워크플로우

```
1. 발표 유형 분석
        │
        ▼
2. 팔레트 선택
   ├── Executive Minimal (임원/투자)
   ├── Sage Professional (컨설팅/ESG)
   ├── Modern Dark (테크/스타트업)
   ├── Corporate Blue (기업/금융)
   └── Warm Neutral (마케팅/브랜드)
        │
        ▼
3. 템플릿 매핑
   ├── 표지 → Cover Slide
   ├── 목차 → Contents
   ├── 섹션 시작 → Section Divider
   ├── 일반 내용 → Content Slide
   ├── 핵심 수치 → Statistics
   ├── 비교/사례 → Split Layout
   ├── 팀 소개 → Team Slide
   ├── 인용/강조 → Quote Slide
   ├── 로드맵 → Timeline
   └── 마무리 → Closing Slide
        │
        ▼
4. 타이포그래피 적용
        │
        ▼
5. 접근성 검증
   ├── 대비율 체크 (4.5:1 이상)
   ├── 최소 폰트 크기 (12pt)
   └── 색맹 친화적 팔레트
        │
        ▼
6. Export Skill로 전달
```

## PptxGenJS 변환 규칙

### 색상 코드

```javascript
// HEX에서 '#' 제거 필수
const color = "667eea";  // ✅ 올바름
const color = "#667eea"; // ❌ 오류 발생
```

### 폰트 매핑

```javascript
const FONT_MAP = {
  'Pretendard': 'Pretendard',  // 로컬 설치 필요
  'Inter': 'Arial',            // 폴백
  'Poppins': 'Arial',          // 폴백
};
```

### 그라데이션 처리

```javascript
// CSS 그라데이션은 이미지로 변환 필요
// PptxGenJS는 CSS gradient 미지원

// 방법 1: 단일 색상으로 대체
// 방법 2: 배경 이미지로 렌더링
```

## 주의사항

1. **폰트 임베딩**: Pretendard는 로컬 설치 또는 이미지 변환 필요
2. **그라데이션**: CSS gradient는 이미지로 사전 렌더링
3. **색상 코드**: HEX에서 '#' 제거
4. **단위 변환**: pt ↔ px ↔ inch 정확히 계산
5. **텍스트 태그**: 시맨틱 HTML 사용 (p, h1-h6, ul, li)
6. **이미지 경로**: 절대 경로 사용

## 팔레트 선택 가이드

| 발표 상황 | 추천 팔레트 | 이유 |
|----------|------------|------|
| 투자자 피치 | Executive Minimal | 신뢰감, 집중도 |
| 기술 세미나 | Modern Dark | 몰입감, 트렌디 |
| 기업 보고서 | Corporate Blue | 전문성, 안정감 |
| ESG/지속가능성 | Sage Professional | 자연, 신뢰 |
| 마케팅 제안 | Warm Neutral | 친근함, 감성 |
