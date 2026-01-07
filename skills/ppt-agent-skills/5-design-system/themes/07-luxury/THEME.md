---
name: theme-luxury
description: |
  Luxury Noir 테마. 럭셔리 브랜드, 하이엔드 서비스, 프리미엄 제품, VIP 프레젠테이션에 최적화.
  "럭셔리", "프리미엄", "하이엔드", "VIP", "명품", "고급" 키워드로 활성화.
tags: [luxury, premium, high-end, vip, exclusive, fashion, beauty]
---

# Luxury Noir Theme

"Quiet Luxury" - 절제된 우아함을 표현하는 프리미엄 디자인 테마입니다.

## Design Philosophy

- **"Quiet Luxury"** - 절제된 우아함
- **블랙 & 골드**의 클래식 조합
- **공간의 여백**을 적극 활용
- **세리프와 산세리프**의 조화

## Color Palette

### CSS Variables (Dark Mode - Primary)

```css
:root {
  /* Primary - Dark Base */
  --bg-primary: #0a0a0a;        /* Noir Black */
  --bg-secondary: #141414;
  --bg-card: #1a1a1a;
  --bg-elevated: #242424;

  /* Text */
  --text-primary: #ffffff;
  --text-secondary: #a0a0a0;
  --text-muted: #606060;

  /* Luxury Accents */
  --accent-gold: #c9a962;       /* Champagne Gold */
  --accent-gold-light: #e8d4a8;
  --accent-platinum: #e0e0e0;
  --accent-rose: #b76e79;       /* Rose Gold hint */

  /* Gradients */
  --gradient-gold: linear-gradient(135deg, #c9a962 0%, #e8d4a8 100%);
  --gradient-dark: linear-gradient(180deg, #141414 0%, #0a0a0a 100%);
}
```

### CSS Variables (Light Mode - Alternative)

```css
:root.light {
  --bg-primary: #f8f6f3;        /* Ivory */
  --bg-secondary: #ffffff;
  --text-primary: #1a1a1a;
  --text-secondary: #606060;
}
```

### Color Reference Table

| Role | HEX | PptxGenJS | Usage |
|------|-----|-----------|-------|
| Noir Black | #0a0a0a | `0a0a0a` | 메인 배경 (다크) |
| Dark Secondary | #141414 | `141414` | 보조 배경 |
| Card | #1a1a1a | `1a1a1a` | 콘텐츠 영역 |
| Elevated | #242424 | `242424` | 호버, 강조 |
| Ivory | #f8f6f3 | `f8f6f3` | 라이트 모드 배경 |
| White | #ffffff | `ffffff` | 주요 텍스트 (다크) |
| Light Gray | #a0a0a0 | `a0a0a0` | 보조 텍스트 |
| Champagne Gold | #c9a962 | `c9a962` | 강조, 로고, 장식 |
| Gold Light | #e8d4a8 | `e8d4a8` | 하이라이트 |
| Platinum | #e0e0e0 | `e0e0e0` | 보조 강조 |
| Rose Gold | #b76e79 | `b76e79` | 부드러운 포인트 |

## Typography

### Font Stack

```css
--font-display: 'Cormorant Garamond', 'Playfair Display', 'Times New Roman', serif;
--font-body: 'Pretendard', 'Inter', sans-serif;
```

### Size Hierarchy (Points)

| Level | Size | Weight | Letter Spacing | Usage |
|-------|------|--------|----------------|-------|
| Hero | 72pt | 300 | 0.05em | 타이틀 (라이트 웨이트!) |
| Title | 32pt | 400 | 0.02em | 슬라이드 제목 |
| Subtitle | 20pt | 400 | 0.03em | 부제목 |
| Body | 16pt | 400 | 0 | 본문 (산세리프) |
| Caption | 12pt | 400 | 0.04em | 캡션 |
| Label | 10pt | 500 | 0.1em | 라벨 (대문자) |

### Typography Note

- **Light weight (300)** for Hero - 우아한 느낌
- **Positive letter spacing** - 여유로운 인상
- **제목: 세리프 / 본문: 산세리프** 조합

## Design Elements

### Gold Accents

```css
.gold-text {
  color: #c9a962;
}

.gold-border {
  border: 1px solid #c9a962;
}

.gold-line {
  height: 1px;
  background: linear-gradient(90deg,
    transparent 0%,
    #c9a962 20%,
    #c9a962 80%,
    transparent 100%
  );
}
```

### Minimal Cards

```css
.luxury-card {
  background: #1a1a1a;
  border: 1px solid #242424;
  padding: 48pt;
}

/* No border-radius - sharp, modern luxury */
```

### Image Treatments

```css
.image-frame {
  border: 1px solid #c9a962;
  padding: 8pt;
}

.image-full-bleed {
  /* No padding, edge-to-edge */
  object-fit: cover;
  width: 100%;
  height: 100%;
}
```

### Divider Lines

```css
.divider {
  width: 60pt;
  height: 1px;
  background: #c9a962;
  margin: 32pt auto;
}

.divider-long {
  width: 100%;
  height: 1px;
  background: #242424;
}
```

### Label/Tag Style

```css
.luxury-label {
  font-size: 10pt;
  font-weight: 500;
  letter-spacing: 0.1em;
  text-transform: uppercase;
  color: #c9a962;
}
```

## Slide Layouts

### Cover Slide (Dark)

```
┌──────────────────────────────────────────────────┐
│▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓│
│▓                                              ▓▓▓│
│▓                                              ▓▓▓│
│▓                                              ▓▓▓│
│▓           MAISON LUMIÈRE                     ▓▓▓│
│▓           ─────────                          ▓▓▓│
│▓           COLLECTION PRINTEMPS 2025          ▓▓▓│
│▓                                              ▓▓▓│
│▓                                              ▓▓▓│
│▓                                              ▓▓▓│
│▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓│
└──────────────────────────────────────────────────┘

Background: Noir Black (#0a0a0a)
Title: White, Serif, 72pt, Light weight, spaced
Divider: Gold line (60pt wide)
Subtitle: Gold (#c9a962), 14pt, uppercase, spaced
```

### Product Showcase

```
┌──────────────────────────────────────────────────┐
│                                                   │
│  ┌──────────────────────┐                        │
│  │                      │        THE HERITAGE    │
│  │                      │        COLLECTION      │
│  │                      │        ─────────       │
│  │    [PRODUCT IMAGE]   │                        │
│  │                      │        Crafted with    │
│  │                      │        precision and   │
│  │                      │        timeless        │
│  │                      │        elegance.       │
│  │                      │                        │
│  └──────────────────────┘        [EXPLORE →]     │
│                                                   │
└──────────────────────────────────────────────────┘

Image: Full height, left aligned, gold frame
Title: White, Serif, 32pt
Body: Light Gray (#a0a0a0), Sans-serif, 16pt
CTA: Gold text with arrow
```

### Statistics (Minimal)

```
┌──────────────────────────────────────────────────┐
│                                                   │
│                                                   │
│       150           30            95%            │
│       ───           ───           ───            │
│      YEARS        COUNTRIES     SATISFACTION     │
│                                                   │
│                                                   │
└──────────────────────────────────────────────────┘

Numbers: White, Serif, 60pt, Light weight
Dividers: Gold lines (30pt wide)
Labels: Gold, 10pt, uppercase, wide spacing
```

### Section Divider

```
┌──────────────────────────────────────────────────┐
│▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓│
│▓                                              ▓▓▓│
│▓                                              ▓▓▓│
│▓           II                                 ▓▓▓│
│▓           ─────                              ▓▓▓│
│▓           SAVOIR-FAIRE                       ▓▓▓│
│▓                                              ▓▓▓│
│▓                                              ▓▓▓│
│▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓│
└──────────────────────────────────────────────────┘

Background: Noir Black
Number: Gold (#c9a962), Serif, Roman numerals, 48pt
Divider: Gold line
Title: White, Serif, 40pt, spaced
```

### Quote

```
┌──────────────────────────────────────────────────┐
│                                                   │
│                                                   │
│           "Excellence is not a destination       │
│            but a continuous journey."            │
│                                                   │
│                    ─────                         │
│                                                   │
│                 FOUNDER NAME                     │
│                 Creative Director                │
│                                                   │
│                                                   │
└──────────────────────────────────────────────────┘

Quote: White, Serif, Italic, 28pt
Divider: Gold, centered
Name: Gold, 12pt, uppercase
Title: Light Gray, 11pt
```

## Light Mode Variant

For presentations in bright environments:

```
Background: Ivory (#f8f6f3)
Text Primary: Almost Black (#1a1a1a)
Text Secondary: Gray (#606060)
Accents: Same gold palette
```

## Spacing & Whitespace

```css
/* Generous margins - key to luxury feel */
--margin-slide: 60pt;        /* Edge padding */
--margin-section: 48pt;      /* Between sections */
--margin-element: 24pt;      /* Between elements */

/* Line heights - airy */
--line-height-display: 1.4;
--line-height-body: 1.8;
```

## Accessibility Guidelines

### Contrast Ratios (Dark Mode)

| Combination | Ratio | Status |
|-------------|-------|--------|
| White on Noir | 21:1 | ✅ AAA |
| Gold on Noir | 8.4:1 | ✅ AAA |
| Light Gray on Noir | 9.5:1 | ✅ AAA |

### Contrast Ratios (Light Mode)

| Combination | Ratio | Status |
|-------------|-------|--------|
| Black on Ivory | 18.2:1 | ✅ AAA |
| Gold on Ivory | 3.2:1 | ⚠️ Large text only |

## Use Cases

| Scenario | Recommended Style |
|----------|-------------------|
| 패션/뷰티 브랜드 | Dark mode, serif titles |
| 주얼리/시계 | Gold accents, product focus |
| 럭셔리 호텔 | Light mode option |
| 프리미엄 서비스 | Minimal stats |
| VIP 이벤트 | Full dark, gold details |

## PptxGenJS Implementation

```javascript
// Luxury theme colors (no # prefix)
const LUXURY_COLORS = {
  bgPrimary: '0a0a0a',
  bgSecondary: '141414',
  bgCard: '1a1a1a',
  bgIvory: 'f8f6f3',
  textPrimary: 'ffffff',
  textSecondary: 'a0a0a0',
  accentGold: 'c9a962',
  accentGoldLight: 'e8d4a8',
  accentPlatinum: 'e0e0e0',
  accentRose: 'b76e79'
};

// Dark elegant slide
slide.background = { color: LUXURY_COLORS.bgPrimary };

// Serif title (use Georgia as fallback for Cormorant)
slide.addText('MAISON LUMIÈRE', {
  x: 0.7, y: 3, w: 11.93, h: 1.2,
  fontSize: 72,
  fontFace: 'Georgia',  // Serif fallback
  color: LUXURY_COLORS.textPrimary,
  align: 'center',
  charSpacing: 5  // Wide spacing
});

// Gold divider line
slide.addShape('rect', {
  x: 5.5, y: 4.2, w: 1.5, h: 0.02,
  fill: { color: LUXURY_COLORS.accentGold }
});

// Uppercase label
slide.addText('COLLECTION PRINTEMPS 2025', {
  x: 0.7, y: 4.5, w: 11.93, h: 0.4,
  fontSize: 11,
  fontFace: 'Pretendard',
  color: LUXURY_COLORS.accentGold,
  align: 'center',
  charSpacing: 8  // Very wide spacing
});

// Gold frame for image
slide.addShape('rect', {
  x: 1, y: 1.5, w: 4, h: 4,
  line: { color: LUXURY_COLORS.accentGold, width: 1 },
  fill: { color: LUXURY_COLORS.bgCard }
});
```

## Related Themes

- **Alternative:** Real Estate Trust (럭셔리 부동산)
- **Colorful Version:** F&B Appetite (럭셔리 다이닝)
- **Modern Version:** Fintech Bold (럭셔리 테크)
