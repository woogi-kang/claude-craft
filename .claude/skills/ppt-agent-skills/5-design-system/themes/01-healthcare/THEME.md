---
name: theme-healthcare
description: |
  Healthcare Clean 테마. 병원, 제약, 바이오테크, 헬스케어 스타트업, 의료기기 발표에 최적화.
  "의료", "헬스케어", "병원", "바이오", "제약" 키워드로 활성화.
tags: [healthcare, medical, biotech, pharma, hospital]
---

# Healthcare Clean Theme

신뢰와 안정감을 주는 의료/헬스케어 전문 디자인 테마입니다.

## Design Philosophy

- **신뢰와 안정감**을 주는 블루 계열 기반
- **치유와 자연**을 상징하는 세이지 그린 포인트
- **접근성 최우선** (WCAG AAA 준수)
- **깨끗하고 미니멀**한 레이아웃

## Color Palette

### CSS Variables

```css
:root {
  /* Primary */
  --bg-primary: #f8fafb;        /* Medical White */
  --bg-secondary: #ffffff;
  --bg-accent: #e8f4f8;         /* Light Cyan Tint */

  /* Text */
  --text-primary: #1a2a3a;      /* Medical Navy */
  --text-secondary: #5a6a7a;
  --text-muted: #8a9aaa;

  /* Accent Colors */
  --accent-primary: #2a7fba;    /* Trust Blue */
  --accent-secondary: #7ab8a8;  /* Healing Sage */
  --accent-success: #48b088;    /* Medical Green */
  --accent-warning: #e8a858;    /* Caution Amber */

  /* Borders & Dividers */
  --border-light: #e0e8f0;
  --border-medium: #c0d0e0;
}
```

### Color Reference Table

| Role | HEX | RGB | PptxGenJS | Usage |
|------|-----|-----|-----------|-------|
| Background | #f8fafb | 248,250,251 | `f8fafb` | 슬라이드 배경 |
| Card | #ffffff | 255,255,255 | `ffffff` | 카드, 콘텐츠 블록 |
| Accent BG | #e8f4f8 | 232,244,248 | `e8f4f8` | 강조 섹션 |
| Primary Text | #1a2a3a | 26,42,58 | `1a2a3a` | 제목, 헤드라인 |
| Secondary Text | #5a6a7a | 90,106,122 | `5a6a7a` | 본문 |
| Trust Blue | #2a7fba | 42,127,186 | `2a7fba` | CTA, 링크, 아이콘 |
| Healing Sage | #7ab8a8 | 122,184,168 | `7ab8a8` | 보조 강조 |
| Medical Green | #48b088 | 72,176,136 | `48b088` | 성공, 긍정 지표 |
| Caution Amber | #e8a858 | 232,168,88 | `e8a858` | 경고, 주의 |

## Typography

### Font Stack

```css
--font-family: 'Pretendard', 'Inter', 'Helvetica Neue', sans-serif;
```

### Size Hierarchy (Points)

| Level | Size | Weight | Letter Spacing | Usage |
|-------|------|--------|----------------|-------|
| Hero | 72pt | 600 | -0.02em | 타이틀 슬라이드 |
| Title | 36pt | 600 | -0.01em | 슬라이드 제목 |
| Subtitle | 22pt | 500 | 0 | 부제목 |
| Body | 18pt | 400 | 0 | 본문 |
| Caption | 13pt | 400 | 0.02em | 캡션, 출처 |
| Label | 11pt | 500 | 0.05em | 라벨, 태그 |

### Typography Note

- Title weight: **600** (700 아님 - 부드러운 인상 유지)
- Line height body: **1.6**

## Design Elements

### Charts & Data Visualization

```
Chart Color Scale (Blue → Sage):
#2a7fba → #4a9fba → #7ab8a8 → #8ac8b8 → #b8d8c8
```

파이/바 차트에 블루-그린 그라데이션 스펙트럼 사용

### Icons

- **Style:** Line icons
- **Stroke:** 2px
- **Corners:** Rounded
- **Color:** Trust Blue (#2a7fba) or Medical Navy (#1a2a3a)

### Images

```css
.image {
  border-radius: 8px;  /* 부드러운 모서리 */
}

/* 또는 더 둥글게 */
.image-soft {
  border-radius: 12px;
}
```

### Data Cards

```css
.data-card {
  background: #ffffff;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);
  padding: 24pt;
}
```

### Badges

```css
.badge {
  background: #e8f4f8;
  color: #2a7fba;
  padding: 6pt 14pt;
  border-radius: 4pt;
  font-size: 11pt;
  font-weight: 500;
}
```

## Slide Layouts

### Cover Slide

```
┌──────────────────────────────────────────────────┐
│  [Logo - top left]                               │
│                                                   │
│                                                   │
│           [Hospital/Company Name]                │
│           ─────────────────────                  │
│           [Presentation Title]                   │
│           [Subtitle - Date]                      │
│                                                   │
│                                                   │
│  [Presenter]                    [Contact Info]   │
└──────────────────────────────────────────────────┘

Background: Medical White (#f8fafb)
Title: Medical Navy (#1a2a3a), 72pt
Subtitle: Secondary Text (#5a6a7a), 22pt
```

### Data/Statistics Slide

```
┌──────────────────────────────────────────────────┐
│  [Section Badge: Trust Blue]              [##]   │
├──────────────────────────────────────────────────┤
│                                                   │
│  KEY HEALTH METRICS                              │
│                                                   │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐       │
│  │   95%    │  │   2.3x   │  │   $1.2M  │       │
│  │ ──────── │  │ ──────── │  │ ──────── │       │
│  │ Recovery │  │ Efficacy │  │ Savings  │       │
│  └──────────┘  └──────────┘  └──────────┘       │
│                                                   │
└──────────────────────────────────────────────────┘

Metric Value: Trust Blue (#2a7fba), 60pt
Metric Label: Secondary Text (#5a6a7a), 14pt
Card Background: White (#ffffff)
```

### Section Divider

```
┌──────────────────────────────────────────────────┐
│░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░│
│░░                                            ░░░░│
│░░  01                                        ░░░░│
│░░  CLINICAL RESULTS                          ░░░░│
│░░  Evidence-based outcomes and analysis      ░░░░│
│░░                                            ░░░░│
│░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░│
└──────────────────────────────────────────────────┘

Background: Trust Blue (#2a7fba)
Number: White (#ffffff), 96pt
Title: White (#ffffff), 48pt
Description: White (#ffffff) at 80% opacity, 18pt
```

## Accessibility Guidelines

### Contrast Ratios

| Combination | Ratio | Status |
|-------------|-------|--------|
| Navy on White | 12.6:1 | ✅ AAA |
| Trust Blue on White | 4.6:1 | ✅ AA |
| Secondary Text on White | 5.2:1 | ✅ AA |
| White on Trust Blue | 4.6:1 | ✅ AA |

### Minimum Font Sizes

- Body text: 18pt minimum
- Captions: 13pt minimum
- Never use lighter than 400 weight for body text

## Use Cases

| Scenario | Recommended Emphasis |
|----------|---------------------|
| 환자 교육 자료 | Healing Sage 강조 |
| 투자자 피치 | Trust Blue + 데이터 카드 |
| 의료진 프레젠테이션 | 미니멀, Medical Navy 제목 |
| 제약 마케팅 | Trust Blue CTA |
| 바이오테크 데모 | 차트 강조, 그린 스펙트럼 |

## PptxGenJS Implementation

```javascript
// Healthcare theme colors (no # prefix)
const HEALTHCARE_COLORS = {
  bgPrimary: 'f8fafb',
  bgSecondary: 'ffffff',
  bgAccent: 'e8f4f8',
  textPrimary: '1a2a3a',
  textSecondary: '5a6a7a',
  accentPrimary: '2a7fba',
  accentSecondary: '7ab8a8',
  accentSuccess: '48b088',
  border: 'e0e8f0'
};

// Apply to slide
slide.background = { color: HEALTHCARE_COLORS.bgPrimary };

// Title text
slide.addText('Health Report', {
  x: 0.7, y: 0.5, w: 11.93, h: 1,
  fontSize: 36,
  fontFace: 'Pretendard',
  color: HEALTHCARE_COLORS.textPrimary,
  bold: true
});

// Data card
slide.addShape('rect', {
  x: 1, y: 2, w: 3, h: 2.5,
  fill: { color: HEALTHCARE_COLORS.bgSecondary },
  shadow: { type: 'outer', blur: 8, offset: 2, angle: 90, opacity: 0.06 }
});
```

## Related Themes

- **Alternative:** Sustainability Earth (자연/치유 강조 시)
- **Formal Version:** Corporate Blue (기업 의료 발표)
