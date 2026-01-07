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

## 컴포넌트 라이브러리 (확장)

> Research 데이터를 효과적으로 시각화하기 위한 HTML 컴포넌트 모음

### 기본 컴포넌트

#### Badge (뱃지)

```html
<span class="badge badge--primary">RESEARCH</span>
<span class="badge badge--success">VERIFIED</span>
<span class="badge badge--warning">PENDING</span>
```

```css
.badge {
  display: inline-block;
  padding: 6pt 14pt;
  font-size: 11pt;
  font-weight: 500;
  letter-spacing: 0.05em;
  text-transform: uppercase;
  border-radius: 4pt;
}
.badge--primary { background: var(--accent); color: white; }
.badge--success { background: #22c55e; color: white; }
.badge--warning { background: #f59e0b; color: white; }
.badge--outline { background: transparent; border: 1pt solid currentColor; }
```

#### Card (카드)

```html
<div class="card">
  <div class="card__header">
    <span class="card__icon">📊</span>
    <h3 class="card__title">제목</h3>
  </div>
  <div class="card__body">내용</div>
  <div class="card__footer">
    <span class="card__source">출처: Gartner 2024</span>
  </div>
</div>
```

```css
.card {
  background: var(--bg-secondary);
  padding: 24pt;
  border-radius: 12pt;
  box-shadow: 0 2pt 8pt rgba(0, 0, 0, 0.08);
}
.card__header { display: flex; align-items: center; gap: 12pt; margin-bottom: 16pt; }
.card__icon { font-size: 24pt; }
.card__title { font-size: 18pt; font-weight: 600; margin: 0; }
.card__body { font-size: 16pt; line-height: 1.6; }
.card__footer { margin-top: 16pt; padding-top: 12pt; border-top: 1pt solid var(--border); }
.card__source { font-size: 12pt; color: var(--text-secondary); }
```

#### Divider (구분선)

```css
.divider { height: 1pt; background: var(--border); margin: 24pt 0; }
.divider--vertical { width: 1pt; height: 100%; margin: 0 24pt; }
.divider--dashed { background: none; border-top: 2pt dashed var(--border); }
```

---

### 데이터 시각화 컴포넌트

#### Metric Box (핵심 지표)

```html
<div class="metric-box">
  <div class="metric-box__value">$2M</div>
  <div class="metric-box__label">연간 손실</div>
  <div class="metric-box__delta metric-box__delta--negative">
    <span class="delta-icon">↓</span> 15% 감소
  </div>
  <div class="metric-box__source">(내부 감사 2024)</div>
</div>
```

```css
.metric-box {
  background: var(--bg-secondary);
  padding: 32pt;
  border-radius: 16pt;
  text-align: center;
  min-width: 180pt;
}
.metric-box__value {
  font-size: 60pt;
  font-weight: 700;
  color: var(--accent);
  line-height: 1;
  margin-bottom: 8pt;
}
.metric-box__label {
  font-size: 16pt;
  color: var(--text-secondary);
  margin-bottom: 12pt;
}
.metric-box__delta {
  font-size: 14pt;
  font-weight: 500;
  padding: 4pt 12pt;
  border-radius: 20pt;
  display: inline-block;
}
.metric-box__delta--positive { background: #dcfce7; color: #166534; }
.metric-box__delta--negative { background: #fee2e2; color: #991b1b; }
.metric-box__source {
  font-size: 11pt;
  color: var(--text-secondary);
  margin-top: 12pt;
}
```

#### Metric Row (가로 지표 배열)

```html
<div class="metric-row">
  <div class="metric-row__item">
    <span class="metric-row__value">85%</span>
    <span class="metric-row__label">정확도</span>
  </div>
  <div class="metric-row__divider"></div>
  <div class="metric-row__item">
    <span class="metric-row__value">2.5x</span>
    <span class="metric-row__label">속도</span>
  </div>
  <div class="metric-row__divider"></div>
  <div class="metric-row__item">
    <span class="metric-row__value">$1.2M</span>
    <span class="metric-row__label">절감</span>
  </div>
</div>
```

```css
.metric-row {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 48pt;
  padding: 32pt;
}
.metric-row__item { text-align: center; }
.metric-row__value { display: block; font-size: 48pt; font-weight: 700; color: var(--accent); }
.metric-row__label { display: block; font-size: 14pt; color: var(--text-secondary); margin-top: 8pt; }
.metric-row__divider { width: 1pt; height: 60pt; background: var(--border); }
```

#### Comparison Table (비교 테이블)

```html
<div class="comparison-table">
  <div class="comparison-table__header">
    <div class="comparison-table__cell"></div>
    <div class="comparison-table__cell comparison-table__cell--highlight">Our Solution</div>
    <div class="comparison-table__cell">Competitor A</div>
    <div class="comparison-table__cell">Competitor B</div>
  </div>
  <div class="comparison-table__row">
    <div class="comparison-table__cell comparison-table__cell--label">가격</div>
    <div class="comparison-table__cell comparison-table__cell--highlight">$99/월</div>
    <div class="comparison-table__cell">$149/월</div>
    <div class="comparison-table__cell">$199/월</div>
  </div>
  <div class="comparison-table__row">
    <div class="comparison-table__cell comparison-table__cell--label">속도</div>
    <div class="comparison-table__cell comparison-table__cell--highlight">
      <span class="check-icon">✓</span> 2x 빠름
    </div>
    <div class="comparison-table__cell">기본</div>
    <div class="comparison-table__cell">기본</div>
  </div>
</div>
```

```css
.comparison-table {
  width: 100%;
  border-collapse: collapse;
}
.comparison-table__header {
  display: grid;
  grid-template-columns: 1fr repeat(3, 1fr);
  background: var(--bg-secondary);
  font-weight: 600;
}
.comparison-table__row {
  display: grid;
  grid-template-columns: 1fr repeat(3, 1fr);
  border-bottom: 1pt solid var(--border);
}
.comparison-table__cell {
  padding: 16pt;
  text-align: center;
  font-size: 14pt;
}
.comparison-table__cell--label {
  text-align: left;
  font-weight: 500;
  background: var(--bg-secondary);
}
.comparison-table__cell--highlight {
  background: rgba(var(--accent-rgb), 0.1);
  color: var(--accent);
  font-weight: 600;
}
.check-icon { color: #22c55e; margin-right: 4pt; }
```

#### Progress Bar (진행률)

```html
<div class="progress">
  <div class="progress__label">
    <span>프로젝트 진행률</span>
    <span>75%</span>
  </div>
  <div class="progress__bar">
    <div class="progress__fill" style="width: 75%"></div>
  </div>
</div>
```

```css
.progress { margin: 16pt 0; }
.progress__label {
  display: flex;
  justify-content: space-between;
  font-size: 14pt;
  margin-bottom: 8pt;
}
.progress__bar {
  height: 12pt;
  background: var(--bg-secondary);
  border-radius: 6pt;
  overflow: hidden;
}
.progress__fill {
  height: 100%;
  background: var(--accent);
  border-radius: 6pt;
  transition: width 0.3s ease;
}
```

---

### Quote & Citation 컴포넌트

#### Quote Block (인용문)

```html
<blockquote class="quote-block">
  <div class="quote-block__mark">"</div>
  <p class="quote-block__text">
    The only way to do great work is to love what you do.
  </p>
  <footer class="quote-block__attribution">
    <cite class="quote-block__author">Steve Jobs</cite>
    <span class="quote-block__role">CEO, Apple</span>
  </footer>
</blockquote>
```

```css
.quote-block {
  position: relative;
  padding: 48pt 64pt;
  text-align: center;
}
.quote-block__mark {
  font-size: 120pt;
  color: var(--accent);
  opacity: 0.2;
  position: absolute;
  top: 0;
  left: 32pt;
  line-height: 1;
}
.quote-block__text {
  font-size: 32pt;
  font-style: italic;
  line-height: 1.4;
  margin: 0 0 24pt;
}
.quote-block__attribution { font-size: 16pt; }
.quote-block__author { font-weight: 600; display: block; }
.quote-block__role { color: var(--text-secondary); }
```

#### Citation Footnote (출처 각주)

```html
<div class="citation-footnote">
  <sup class="citation-footnote__number">1</sup>
  <span class="citation-footnote__text">Gartner AI Market Report, November 2024</span>
</div>
```

```css
.citation-footnote {
  font-size: 11pt;
  color: var(--text-secondary);
  display: flex;
  align-items: baseline;
  gap: 4pt;
}
.citation-footnote__number {
  font-size: 9pt;
  color: var(--accent);
}
```

#### Source Badge (출처 뱃지)

```html
<span class="source-badge">
  <span class="source-badge__icon">📊</span>
  <span class="source-badge__text">Gartner 2024</span>
</span>
```

```css
.source-badge {
  display: inline-flex;
  align-items: center;
  gap: 6pt;
  padding: 4pt 10pt;
  background: var(--bg-secondary);
  border-radius: 12pt;
  font-size: 11pt;
  color: var(--text-secondary);
}
```

---

### 리스트 & 불릿 컴포넌트

#### Icon List (아이콘 리스트)

```html
<ul class="icon-list">
  <li class="icon-list__item">
    <span class="icon-list__icon">✓</span>
    <span class="icon-list__text">첫 번째 포인트</span>
    <span class="icon-list__source">(McKinsey, 2024)</span>
  </li>
  <li class="icon-list__item">
    <span class="icon-list__icon">✓</span>
    <span class="icon-list__text">두 번째 포인트</span>
  </li>
</ul>
```

```css
.icon-list {
  list-style: none;
  padding: 0;
  margin: 0;
}
.icon-list__item {
  display: flex;
  align-items: flex-start;
  gap: 12pt;
  padding: 12pt 0;
  font-size: 18pt;
  line-height: 1.5;
}
.icon-list__icon {
  flex-shrink: 0;
  width: 24pt;
  height: 24pt;
  display: flex;
  align-items: center;
  justify-content: center;
  background: var(--accent);
  color: white;
  border-radius: 50%;
  font-size: 14pt;
}
.icon-list__text { flex: 1; }
.icon-list__source {
  font-size: 12pt;
  color: var(--text-secondary);
  white-space: nowrap;
}
```

#### Numbered List (번호 리스트)

```html
<ol class="numbered-list">
  <li class="numbered-list__item">
    <span class="numbered-list__number">01</span>
    <div class="numbered-list__content">
      <h4 class="numbered-list__title">첫 번째 단계</h4>
      <p class="numbered-list__desc">상세 설명이 여기에 들어갑니다.</p>
    </div>
  </li>
</ol>
```

```css
.numbered-list {
  list-style: none;
  padding: 0;
  counter-reset: item;
}
.numbered-list__item {
  display: flex;
  align-items: flex-start;
  gap: 24pt;
  padding: 24pt 0;
  border-bottom: 1pt solid var(--border);
}
.numbered-list__number {
  font-size: 36pt;
  font-weight: 700;
  color: var(--accent);
  opacity: 0.5;
  min-width: 60pt;
}
.numbered-list__title {
  font-size: 20pt;
  font-weight: 600;
  margin: 0 0 8pt;
}
.numbered-list__desc {
  font-size: 16pt;
  color: var(--text-secondary);
  margin: 0;
}
```

---

### 타임라인 & 프로세스 컴포넌트

#### Timeline Horizontal (가로 타임라인)

```html
<div class="timeline-h">
  <div class="timeline-h__item timeline-h__item--active">
    <div class="timeline-h__dot"></div>
    <div class="timeline-h__label">Q1 2024</div>
    <div class="timeline-h__title">계획</div>
  </div>
  <div class="timeline-h__line"></div>
  <div class="timeline-h__item">
    <div class="timeline-h__dot"></div>
    <div class="timeline-h__label">Q2 2024</div>
    <div class="timeline-h__title">개발</div>
  </div>
  <div class="timeline-h__line"></div>
  <div class="timeline-h__item">
    <div class="timeline-h__dot"></div>
    <div class="timeline-h__label">Q3 2024</div>
    <div class="timeline-h__title">출시</div>
  </div>
</div>
```

```css
.timeline-h {
  display: flex;
  align-items: flex-start;
  justify-content: center;
  padding: 32pt 0;
}
.timeline-h__item {
  display: flex;
  flex-direction: column;
  align-items: center;
  min-width: 120pt;
}
.timeline-h__dot {
  width: 16pt;
  height: 16pt;
  background: var(--border);
  border-radius: 50%;
  margin-bottom: 12pt;
}
.timeline-h__item--active .timeline-h__dot {
  background: var(--accent);
  box-shadow: 0 0 0 4pt rgba(var(--accent-rgb), 0.2);
}
.timeline-h__line {
  flex: 1;
  height: 2pt;
  background: var(--border);
  margin-top: 7pt;
  min-width: 60pt;
}
.timeline-h__label {
  font-size: 12pt;
  color: var(--text-secondary);
}
.timeline-h__title {
  font-size: 16pt;
  font-weight: 600;
  margin-top: 4pt;
}
```

#### Process Flow (프로세스 플로우)

```html
<div class="process-flow">
  <div class="process-flow__step">
    <div class="process-flow__icon">1</div>
    <div class="process-flow__content">
      <h4>데이터 수집</h4>
      <p>다양한 소스에서 데이터 수집</p>
    </div>
  </div>
  <div class="process-flow__arrow">→</div>
  <div class="process-flow__step">
    <div class="process-flow__icon">2</div>
    <div class="process-flow__content">
      <h4>분석</h4>
      <p>AI 기반 데이터 분석</p>
    </div>
  </div>
  <div class="process-flow__arrow">→</div>
  <div class="process-flow__step">
    <div class="process-flow__icon">3</div>
    <div class="process-flow__content">
      <h4>인사이트</h4>
      <p>액션 가능한 인사이트 도출</p>
    </div>
  </div>
</div>
```

```css
.process-flow {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 16pt;
}
.process-flow__step {
  display: flex;
  align-items: center;
  gap: 16pt;
  background: var(--bg-secondary);
  padding: 20pt 24pt;
  border-radius: 12pt;
}
.process-flow__icon {
  width: 40pt;
  height: 40pt;
  background: var(--accent);
  color: white;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 700;
  font-size: 18pt;
}
.process-flow__content h4 {
  font-size: 16pt;
  margin: 0 0 4pt;
}
.process-flow__content p {
  font-size: 12pt;
  color: var(--text-secondary);
  margin: 0;
}
.process-flow__arrow {
  font-size: 24pt;
  color: var(--accent);
}
```

---

### 팀 & 프로필 컴포넌트

#### Team Card (팀 카드)

```html
<div class="team-card">
  <div class="team-card__avatar">
    <img src="avatar.jpg" alt="Name">
  </div>
  <h4 class="team-card__name">홍길동</h4>
  <p class="team-card__role">CEO & Founder</p>
  <p class="team-card__bio">10년 경력의 테크 리더</p>
  <div class="team-card__links">
    <a href="#">LinkedIn</a>
    <a href="#">Twitter</a>
  </div>
</div>
```

```css
.team-card {
  text-align: center;
  padding: 24pt;
}
.team-card__avatar {
  width: 100pt;
  height: 100pt;
  border-radius: 50%;
  overflow: hidden;
  margin: 0 auto 16pt;
  background: var(--bg-secondary);
}
.team-card__avatar img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}
.team-card__name {
  font-size: 18pt;
  font-weight: 600;
  margin: 0 0 4pt;
}
.team-card__role {
  font-size: 14pt;
  color: var(--accent);
  margin: 0 0 8pt;
}
.team-card__bio {
  font-size: 12pt;
  color: var(--text-secondary);
  margin: 0;
}
.team-card__links {
  margin-top: 12pt;
  display: flex;
  justify-content: center;
  gap: 12pt;
}
.team-card__links a {
  font-size: 12pt;
  color: var(--accent);
}
```

#### Case Study Card (사례 연구 카드) ⭐ NEW

고객 성공 사례를 요약 카드 형태로 표현합니다.

```html
<div class="case-card">
  <div class="case-card__header">
    <img class="case-card__logo" src="company-logo.png" alt="삼성전자">
    <div class="case-card__company">
      <span class="case-card__name">삼성전자</span>
      <span class="case-card__industry">전자/IT</span>
    </div>
  </div>
  <div class="case-card__body">
    <h4 class="case-card__headline">생산성 40% 향상</h4>
    <p class="case-card__summary">수작업 오류 문제를 AI 자동화로 해결</p>
  </div>
  <div class="case-card__metrics">
    <div class="case-card__metric">
      <span class="case-card__metric-value case-card__metric-value--up">+40%</span>
      <span class="case-card__metric-label">생산성</span>
    </div>
    <div class="case-card__metric">
      <span class="case-card__metric-value case-card__metric-value--down">-90%</span>
      <span class="case-card__metric-label">오류율</span>
    </div>
  </div>
  <div class="case-card__testimonial">
    <p class="case-card__quote">"AutoFlow 도입 후 팀 생산성이 40% 향상되었습니다."</p>
    <span class="case-card__author">— 김철수, IT팀장</span>
  </div>
</div>
```

```css
.case-card {
  background: var(--bg-secondary);
  border-radius: 16pt;
  padding: 24pt;
  border-left: 4pt solid var(--accent);
}
.case-card__header {
  display: flex;
  align-items: center;
  gap: 16pt;
  margin-bottom: 20pt;
}
.case-card__logo {
  width: 48pt;
  height: 48pt;
  object-fit: contain;
  border-radius: 8pt;
  background: white;
  padding: 4pt;
}
.case-card__name {
  display: block;
  font-size: 16pt;
  font-weight: 600;
}
.case-card__industry {
  display: block;
  font-size: 12pt;
  color: var(--text-secondary);
}
.case-card__headline {
  font-size: 24pt;
  font-weight: 700;
  color: var(--accent);
  margin: 0 0 8pt;
}
.case-card__summary {
  font-size: 14pt;
  color: var(--text-secondary);
  margin: 0;
}
.case-card__metrics {
  display: flex;
  gap: 24pt;
  margin-top: 20pt;
  padding-top: 16pt;
  border-top: 1pt solid var(--border);
}
.case-card__metric {
  text-align: center;
}
.case-card__metric-value {
  display: block;
  font-size: 28pt;
  font-weight: 700;
}
.case-card__metric-value--up {
  color: #22c55e;
}
.case-card__metric-value--down {
  color: #22c55e; /* 오류 감소는 긍정적이므로 녹색 */
}
.case-card__metric-label {
  display: block;
  font-size: 12pt;
  color: var(--text-secondary);
  margin-top: 4pt;
}
.case-card__testimonial {
  margin-top: 16pt;
  padding-top: 16pt;
  border-top: 1pt solid var(--border);
}
.case-card__quote {
  font-size: 14pt;
  font-style: italic;
  color: var(--text-primary);
  margin: 0 0 8pt;
}
.case-card__author {
  font-size: 12pt;
  color: var(--text-secondary);
}
```

#### Case Study Grid (사례 그리드)

여러 고객 사례를 그리드로 배치합니다.

```html
<div class="case-grid">
  <div class="case-card case-card--compact">
    <img class="case-card__logo" src="samsung.png" alt="삼성전자">
    <h4 class="case-card__headline">생산성 40%↑</h4>
    <span class="case-card__industry">전자/IT</span>
  </div>
  <div class="case-card case-card--compact">
    <img class="case-card__logo" src="hyundai.png" alt="현대자동차">
    <h4 class="case-card__headline">오류 90%↓</h4>
    <span class="case-card__industry">자동차</span>
  </div>
  <div class="case-card case-card--compact">
    <img class="case-card__logo" src="kakao.png" alt="카카오">
    <h4 class="case-card__headline">비용 50%↓</h4>
    <span class="case-card__industry">IT서비스</span>
  </div>
</div>
```

```css
.case-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 24pt;
}
.case-card--compact {
  text-align: center;
  border-left: none;
  border-top: 4pt solid var(--accent);
}
.case-card--compact .case-card__logo {
  width: 64pt;
  height: 64pt;
  margin: 0 auto 12pt;
}
.case-card--compact .case-card__headline {
  font-size: 20pt;
  margin-bottom: 4pt;
}
```

---

### CTA & 버튼 컴포넌트

#### Button Group (버튼 그룹)

```html
<div class="button-group">
  <button class="btn btn--primary">시작하기</button>
  <button class="btn btn--secondary">자세히 보기</button>
</div>
```

```css
.button-group {
  display: flex;
  gap: 16pt;
  justify-content: center;
}
.btn {
  padding: 14pt 32pt;
  font-size: 16pt;
  font-weight: 600;
  border-radius: 8pt;
  border: none;
  cursor: pointer;
  transition: all 0.2s;
}
.btn--primary {
  background: var(--accent);
  color: white;
}
.btn--secondary {
  background: transparent;
  border: 2pt solid var(--accent);
  color: var(--accent);
}
.btn--large {
  padding: 18pt 48pt;
  font-size: 18pt;
}
```

#### CTA Box (CTA 박스)

```html
<div class="cta-box">
  <h3 class="cta-box__title">지금 시작하세요</h3>
  <p class="cta-box__desc">30일 무료 체험으로 시작해보세요</p>
  <button class="btn btn--primary btn--large">무료 체험 시작</button>
  <p class="cta-box__note">신용카드 불필요</p>
</div>
```

```css
.cta-box {
  text-align: center;
  padding: 48pt;
  background: var(--bg-secondary);
  border-radius: 16pt;
}
.cta-box__title {
  font-size: 32pt;
  font-weight: 700;
  margin: 0 0 12pt;
}
.cta-box__desc {
  font-size: 18pt;
  color: var(--text-secondary);
  margin: 0 0 24pt;
}
.cta-box__note {
  font-size: 12pt;
  color: var(--text-secondary);
  margin: 16pt 0 0;
}
```

---

### 레이아웃 헬퍼

#### Grid System (그리드 시스템)

```css
/* 균등 분할 그리드 */
.grid-2 { display: grid; grid-template-columns: repeat(2, 1fr); gap: 32pt; }
.grid-3 { display: grid; grid-template-columns: repeat(3, 1fr); gap: 24pt; }
.grid-4 { display: grid; grid-template-columns: repeat(4, 1fr); gap: 20pt; }

/* 비대칭 그리드 */
.grid-1-2 { display: grid; grid-template-columns: 1fr 2fr; gap: 32pt; }
.grid-2-1 { display: grid; grid-template-columns: 2fr 1fr; gap: 32pt; }
.grid-golden { display: grid; grid-template-columns: 1fr 1.618fr; gap: 32pt; }

/* 콘텐츠+비주얼 */
.grid-content-visual { display: grid; grid-template-columns: 2fr 3fr; gap: 32pt; align-items: center; }
.grid-visual-content { display: grid; grid-template-columns: 3fr 2fr; gap: 32pt; align-items: center; }
```

#### Flexbox Helpers

```css
.flex { display: flex; }
.flex-col { flex-direction: column; }
.flex-center { justify-content: center; align-items: center; }
.flex-between { justify-content: space-between; }
.flex-wrap { flex-wrap: wrap; }
.gap-sm { gap: 12pt; }
.gap-md { gap: 24pt; }
.gap-lg { gap: 48pt; }
```

#### Spacing Utilities

```css
.mt-0 { margin-top: 0; }
.mt-sm { margin-top: 12pt; }
.mt-md { margin-top: 24pt; }
.mt-lg { margin-top: 48pt; }
.mb-0 { margin-bottom: 0; }
.mb-sm { margin-bottom: 12pt; }
.mb-md { margin-bottom: 24pt; }
.mb-lg { margin-bottom: 48pt; }
.p-0 { padding: 0; }
.p-sm { padding: 12pt; }
.p-md { padding: 24pt; }
.p-lg { padding: 48pt; }
```

---

### 컴포넌트-데이터 타입 매핑 (확장)

| data_type | 1순위 컴포넌트 | 2순위 컴포넌트 | 선택 기준 |
|-----------|--------------|--------------|----------|
| `statistic` | metric-box | metric-row | 단일 지표 vs 복수 지표 |
| `quote` | quote-block | case-card (testimonial) | 독립 인용 vs 사례 내 인용 |
| `case_study` | case-card | process-flow | outcome 중심 vs 과정 중심 |
| `comparison` | comparison-table | metric-row | 다항목 비교 vs 핵심 수치 비교 |
| `trend` | timeline-h | line-chart | 마일스톤 중심 vs 연속 데이터 |
| `roadmap` | timeline-h | numbered-list | 시각적 강조 vs 텍스트 중심 |
| `team` | team-card (grid-4) | icon-list | 상세 프로필 vs 간단 목록 |
| `cta` | cta-box | button-group | 강조 CTA vs 옵션 제시 |

**Visual Type 자동 선택 로직:**

```
data_type 확인
    │
    ├─ statistic
    │     ├─ 단일 값 → metric-box
    │     └─ 복수 값 (2-4개) → metric-row
    │
    ├─ case_study
    │     ├─ steps 배열 존재 → process-flow
    │     ├─ outcome_metrics 존재 → case-card
    │     └─ testimonial만 존재 → quote-block + source-badge
    │
    ├─ trend
    │     ├─ milestones 배열 존재 → timeline-h
    │     └─ 연속 데이터 → line-chart
    │
    └─ comparison
          ├─ 3개 이상 항목 → comparison-table
          └─ 2개 항목 → metric-row (before/after)
```

---

### 컴포넌트 조합 예시

#### 문제 정의 슬라이드

```html
<section class="slide slide--problem">
  <header class="slide__header">
    <span class="badge badge--outline">PROBLEM</span>
    <span class="slide__number">05</span>
  </header>

  <h1 class="slide__title">수작업 오류로 연간 $2M 손실</h1>

  <div class="grid-content-visual">
    <div class="slide__content">
      <ul class="icon-list">
        <li class="icon-list__item">
          <span class="icon-list__icon">!</span>
          <span class="icon-list__text">수작업 데이터 입력 오류율 15%</span>
          <span class="icon-list__source">(운영팀 조사)</span>
        </li>
        <li class="icon-list__item">
          <span class="icon-list__icon">!</span>
          <span class="icon-list__text">직원 40% 업무시간 수동 작업에 소비</span>
          <span class="icon-list__source">(직원 설문)</span>
        </li>
      </ul>
    </div>
    <div class="slide__visual">
      <div class="metric-box">
        <div class="metric-box__value">$2M</div>
        <div class="metric-box__label">연간 손실</div>
        <div class="metric-box__source">(내부 감사 2024)</div>
      </div>
    </div>
  </div>

  <footer class="slide__footer">
    <div class="citation-footnote">
      <sup>1</sup> 내부 감사 보고서 2024, n=500 거래 분석
    </div>
  </footer>
</section>
```

#### 솔루션 슬라이드

```html
<section class="slide slide--solution">
  <header class="slide__header">
    <span class="badge badge--primary">SOLUTION</span>
  </header>

  <h1 class="slide__title">3단계 자동화로 오류율 90% 감소</h1>

  <div class="process-flow mt-lg">
    <div class="process-flow__step">
      <div class="process-flow__icon">1</div>
      <div class="process-flow__content">
        <h4>데이터 수집 자동화</h4>
        <p>API 연동으로 수동 입력 제거</p>
      </div>
    </div>
    <div class="process-flow__arrow">→</div>
    <div class="process-flow__step">
      <div class="process-flow__icon">2</div>
      <div class="process-flow__content">
        <h4>AI 검증</h4>
        <p>실시간 오류 탐지 및 수정</p>
      </div>
    </div>
    <div class="process-flow__arrow">→</div>
    <div class="process-flow__step">
      <div class="process-flow__icon">3</div>
      <div class="process-flow__content">
        <h4>대시보드</h4>
        <p>실시간 모니터링 및 알림</p>
      </div>
    </div>
  </div>

  <div class="metric-row mt-lg">
    <div class="metric-row__item">
      <span class="metric-row__value">90%</span>
      <span class="metric-row__label">오류 감소</span>
    </div>
    <div class="metric-row__divider"></div>
    <div class="metric-row__item">
      <span class="metric-row__value">3개월</span>
      <span class="metric-row__label">ROI 달성</span>
    </div>
    <div class="metric-row__divider"></div>
    <div class="metric-row__item">
      <span class="metric-row__value">$1.8M</span>
      <span class="metric-row__label">연간 절감</span>
    </div>
  </div>
</section>
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
