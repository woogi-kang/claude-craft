# Layout System & Slide Templates

PPT Design System의 레이아웃 시스템과 10가지 슬라이드 템플릿입니다.

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

---

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
