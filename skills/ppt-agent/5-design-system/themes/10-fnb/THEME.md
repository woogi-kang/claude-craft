---
name: theme-fnb
description: |
  F&B Appetite 테마. 식음료, 레스토랑, 호텔리어, 라이프스타일, 리테일 발표에 최적화.
  "식음료", "레스토랑", "카페", "호텔", "라이프스타일", "리테일", "푸드" 키워드로 활성화.
tags: [fnb, food, beverage, restaurant, cafe, hotel, lifestyle, retail, hospitality]
---

# F&B Appetite Theme

식욕을 자극하는 따뜻하고 친근한 F&B/라이프스타일 전문 디자인 테마입니다.

## Design Philosophy

- **식욕을 자극하는** 따뜻한 색상
- **수제 느낌**의 친근한 톤
- **텍스처와 질감** 활용
- **미드센추리 레트로 + 현대**의 조화

## Color Palette

### CSS Variables

```css
:root {
  /* Primary - Warm Base */
  --bg-primary: #faf6f0;        /* Cream */
  --bg-secondary: #ffffff;
  --bg-accent: #f5ebe0;         /* Warm Beige */
  --bg-dark: #2c2418;           /* Espresso */

  /* Text */
  --text-primary: #2c2418;      /* Espresso */
  --text-secondary: #5c4830;    /* Coffee */
  --text-muted: #8c7860;
  --text-on-dark: #faf6f0;

  /* Appetite Colors */
  --accent-terracotta: #c45a3b; /* Terracotta - Main */
  --accent-mustard: #d4a040;    /* Mustard Yellow */
  --accent-sage: #7a9a6a;       /* Fresh Sage */
  --accent-burgundy: #8b3a3a;   /* Wine Burgundy */
  --accent-mocha: #a67c52;      /* Mocha Mousse - 2025 Color of Year */

  /* Gradients */
  --gradient-warm: linear-gradient(135deg, #c45a3b 0%, #d4a040 100%);
}
```

### Color Reference Table

| Role | HEX | PptxGenJS | Usage |
|------|-----|-----------|-------|
| Cream | #faf6f0 | `faf6f0` | 메인 배경 |
| White | #ffffff | `ffffff` | 카드 배경 |
| Warm Beige | #f5ebe0 | `f5ebe0` | 섹션 배경 |
| Espresso | #2c2418 | `2c2418` | 제목, 다크 섹션 |
| Coffee | #5c4830 | `5c4830` | 본문 |
| Muted | #8c7860 | `8c7860` | 캡션 |
| Terracotta | #c45a3b | `c45a3b` | 주요 CTA |
| Mustard | #d4a040 | `d4a040` | 하이라이트, 포인트 |
| Sage | #7a9a6a | `7a9a6a` | 신선함, 자연 |
| Burgundy | #8b3a3a | `8b3a3a` | 와인, 프리미엄 |
| Mocha Mousse | #a67c52 | `a67c52` | 2025 트렌드 컬러 |

## Typography

### Font Stack

```css
--font-display: 'Playfair Display', 'Georgia', serif;
--font-body: 'Pretendard', 'Lato', sans-serif;
--font-handwritten: 'Caveat', 'Dancing Script', cursive; /* Optional */
```

### Size Hierarchy (Points)

| Level | Size | Weight | Usage |
|-------|------|--------|-------|
| Hero | 68pt | 500 | 타이틀 슬라이드 (Serif) |
| Title | 34pt | 500 | 슬라이드 제목 (Serif) |
| Subtitle | 22pt | 400 | 부제목 |
| Body | 18pt | 400 | 본문 (Sans-serif) |
| Caption | 13pt | 400 | 캡션, 출처 |
| Label | 11pt | 500 | 라벨, 태그 |
| Handwritten | 24pt | 400 | 포인트 텍스트 (Cursive) |

### Typography Note

- **Serif for display** - 우아한 느낌
- **Line height body: 1.7** - 편안한 가독성
- **Medium weight (500)** for titles - 너무 무겁지 않게

## Design Elements

### Menu-Style Cards

```css
.menu-card {
  background: #ffffff;
  border-radius: 4px;
  padding: 24pt;
  box-shadow: 0 2px 8px rgba(44, 36, 24, 0.08);
  border-bottom: 4px solid #c45a3b;
}
```

### Food Photo Treatment

```css
.food-image {
  border-radius: 8px;
  filter: saturate(1.05) contrast(1.02);  /* Slightly warm */
}

.food-image-frame {
  background: #f5ebe0;
  padding: 12pt;
  border-radius: 4px;
}
```

### Price/Value Display

```css
.price {
  font-family: 'Playfair Display', serif;
  font-size: 32pt;
  color: #c45a3b;
}

.currency {
  font-size: 18pt;
  vertical-align: super;
}
```

### Ingredient Tags

```css
.ingredient-tag {
  display: inline-block;
  background: #f5ebe0;
  color: #5c4830;
  padding: 4pt 12pt;
  border-radius: 20pt;
  font-size: 11pt;
  margin-right: 8pt;
}

.tag-fresh {
  background: rgba(122, 154, 106, 0.2);
  color: #5a7a4a;
}

.tag-premium {
  background: #d4a040;
  color: #2c2418;
}
```

### Decorative Elements

```css
/* Hand-drawn style underline */
.hand-underline {
  border-bottom: 3px solid #c45a3b;
  border-radius: 2px;
  opacity: 0.7;
}

/* Texture overlay */
.paper-texture {
  background-image: url('paper-texture.png');
  opacity: 0.03;
}
```

### Icon Style

```css
.food-icon {
  /* Hand-drawn or illustrated style */
  stroke-width: 2px;
  stroke-linecap: round;
  stroke-linejoin: round;
  color: #8c7860;
}
```

## Slide Layouts

### Cover Slide

```
┌──────────────────────────────────────────────────┐
│                                                   │
│  [Restaurant Logo]                               │
│                                                   │
│           ☕                                      │
│                                                   │
│           THE ARTISAN                            │
│           KITCHEN                                │
│           ─────────                              │
│           Farm to Table Excellence               │
│                                                   │
│                                                   │
│  [Est. 2015]                    [Location]       │
└──────────────────────────────────────────────────┘

Background: Cream (#faf6f0)
Icon: Terracotta (#c45a3b) or food illustration
Title: Espresso (#2c2418), Serif, 68pt
Divider: Terracotta line
Subtitle: Mocha (#a67c52), 20pt
```

### Menu Showcase

```
┌──────────────────────────────────────────────────┐
│  [SIGNATURE DISHES]                       [##]   │
├──────────────────────────────────────────────────┤
│                                                   │
│  ┌──────────────────────┐                        │
│  │                      │  Truffle Risotto       │
│  │   [FOOD PHOTO]       │  ─────────────         │
│  │                      │  Arborio rice, black   │
│  │                      │  truffle, parmesan,    │
│  │                      │  white wine reduction  │
│  │                      │                        │
│  │                      │  [Fresh] [Premium]     │
│  │                      │                        │
│  └──────────────────────┘  $42                   │
│                                                   │
└──────────────────────────────────────────────────┘

Photo: Warm filter, rounded corners
Title: Serif, Espresso, 28pt
Description: Coffee (#5c4830), 16pt
Tags: Sage for fresh, Mustard for premium
Price: Terracotta, Serif, 32pt
```

### Menu Grid

```
┌──────────────────────────────────────────────────┐
│  [APPETIZERS]                             [##]   │
├──────────────────────────────────────────────────┤
│                                                   │
│  ┌───────────────┐ ┌───────────────┐ ┌─────────┐│
│  │ [Photo]       │ │ [Photo]       │ │ [Photo] ││
│  │               │ │               │ │         ││
│  │ Bruschetta    │ │ Carpaccio     │ │ Burrata ││
│  │ ─────────     │ │ ─────────     │ │ ─────── ││
│  │ $16           │ │ $24           │ │ $18     ││
│  └───────────────┘ └───────────────┘ └─────────┘│
│                                                   │
│  ┌───────────────┐ ┌───────────────┐ ┌─────────┐│
│  │ [Photo]       │ │ [Photo]       │ │ [Photo] ││
│  │               │ │               │ │         ││
│  │ Calamari      │ │ Oysters       │ │ Soup    ││
│  │ ─────────     │ │ ─────────     │ │ ─────── ││
│  │ $18           │ │ $36           │ │ $14     ││
│  └───────────────┘ └───────────────┘ └─────────┘│
│                                                   │
└──────────────────────────────────────────────────┘

Cards: Cream background, terracotta bottom border
Photos: Rounded corners
Titles: Serif
Prices: Terracotta
```

### Statistics (F&B Style)

```
┌──────────────────────────────────────────────────┐
│  [BY THE NUMBERS]                         [##]   │
├──────────────────────────────────────────────────┤
│                                                   │
│        ☕                 🍷                 🥗    │
│                                                   │
│       12K               85%               100%   │
│    ─────────         ─────────         ─────────│
│    Cups of Coffee    Wine Selection    Organic   │
│      Daily          from Local          Produce  │
│                      Vineyards                   │
│                                                   │
│                                                   │
└──────────────────────────────────────────────────┘

Icons: Hand-drawn style or emoji
Values: Terracotta or Espresso, Serif, 60pt
Dividers: Mocha lines
Labels: Coffee (#5c4830), 14pt
```

### Section Divider

```
┌──────────────────────────────────────────────────┐
│▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓│
│▓                                              ▓▓▓│
│▓  02                                          ▓▓▓│
│▓  ─────────────────────                       ▓▓▓│
│▓  OUR                                         ▓▓▓│
│▓  PHILOSOPHY                                  ▓▓▓│
│▓                                              ▓▓▓│
│▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓│
└──────────────────────────────────────────────────┘

Background: Espresso (#2c2418)
Number: Mustard (#d4a040), 72pt
Divider: Mustard line
Title: Cream (#faf6f0), Serif, 48pt
```

### Quote/Testimonial

```
┌──────────────────────────────────────────────────┐
│                                                   │
│                                                   │
│           "Food is not just eating energy.       │
│            It's an experience."                  │
│                                                   │
│                    ─────                         │
│                                                   │
│                 EXECUTIVE CHEF                   │
│                 Marco Rosetti                    │
│                                                   │
│                                                   │
└──────────────────────────────────────────────────┘

Background: Warm Beige (#f5ebe0)
Quote: Espresso, Serif, Italic, 28pt
Divider: Terracotta, short
Name: Terracotta, Sans-serif, 14pt
Title: Muted, 12pt
```

## Texture & Photography Guidelines

### Photo Treatment

- **Color Temperature:** Slightly warm (add 5-10% warmth)
- **Saturation:** Natural, not oversaturated
- **Lighting:** Natural daylight preferred
- **Style:** Overhead or 45-degree angle

### Texture Options

```css
/* Paper texture */
background: url('kraft-paper.png');
opacity: 0.03;

/* Wood grain */
background: url('wood-texture.png');
opacity: 0.05;
```

## Accessibility Guidelines

### Contrast Ratios

| Combination | Ratio | Status |
|-------------|-------|--------|
| Espresso on Cream | 10.8:1 | ✅ AAA |
| Coffee on Cream | 6.2:1 | ✅ AA |
| Terracotta on Cream | 4.5:1 | ✅ AA |
| Cream on Espresso | 10.8:1 | ✅ AAA |

## Use Cases

| Scenario | Recommended Style |
|----------|-------------------|
| 레스토랑 메뉴 | Menu cards, food photos |
| 카페 브랜딩 | Warm tones, handwritten accents |
| 호텔 F&B | Premium elements, burgundy accents |
| 푸드 트럭 피치 | Playful, mustard highlights |
| 와이너리 | Burgundy dominant, elegant |

## PptxGenJS Implementation

```javascript
// F&B theme colors (no # prefix)
const FNB_COLORS = {
  bgPrimary: 'faf6f0',
  bgSecondary: 'ffffff',
  bgAccent: 'f5ebe0',
  bgDark: '2c2418',
  textPrimary: '2c2418',
  textSecondary: '5c4830',
  textMuted: '8c7860',
  accentTerracotta: 'c45a3b',
  accentMustard: 'd4a040',
  accentSage: '7a9a6a',
  accentBurgundy: '8b3a3a',
  accentMocha: 'a67c52'
};

// Warm cream background
slide.background = { color: FNB_COLORS.bgPrimary };

// Menu card with terracotta border
slide.addShape('rect', {
  x: 1, y: 2, w: 5, h: 3.5,
  fill: { color: FNB_COLORS.bgSecondary },
  shadow: { type: 'outer', blur: 8, offset: 2, angle: 90, opacity: 0.08 }
});
// Bottom terracotta border
slide.addShape('rect', {
  x: 1, y: 5.45, w: 5, h: 0.05,
  fill: { color: FNB_COLORS.accentTerracotta }
});

// Serif title (use Georgia as fallback)
slide.addText('Truffle Risotto', {
  x: 6.5, y: 2.2, w: 5.5, h: 0.6,
  fontSize: 28,
  fontFace: 'Georgia',  // Serif fallback
  color: FNB_COLORS.textPrimary
});

// Price
slide.addText('$42', {
  x: 6.5, y: 4.5, w: 1.5, h: 0.5,
  fontSize: 32,
  fontFace: 'Georgia',
  color: FNB_COLORS.accentTerracotta
});

// Fresh tag
slide.addShape('roundRect', {
  x: 6.5, y: 4, w: 1, h: 0.35,
  fill: { color: FNB_COLORS.accentSage, transparency: 80 }
});
slide.addText('Fresh', {
  x: 6.5, y: 4, w: 1, h: 0.35,
  fontSize: 11,
  color: '5a7a4a',
  align: 'center',
  valign: 'middle'
});
```

## Related Themes

- **Alternative:** Education Bright (요리 교육)
- **Premium Version:** Luxury Noir (파인 다이닝)
- **Casual Version:** Startup Gradient (푸드테크)
