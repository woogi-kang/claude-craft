---
name: theme-creative
description: |
  Creative Neon 테마. 크리에이티브 에이전시, 디자인 스튜디오, 포트폴리오, 아트 프로젝트 발표에 최적화.
  "크리에이티브", "에이전시", "디자인", "포트폴리오", "아트" 키워드로 활성화.
tags: [creative, agency, design, portfolio, art, studio, experimental]
---

# Creative Neon Theme

대담하고 파격적인 크리에이티브 전문 디자인 테마입니다.

## Design Philosophy

- **대담하고 파격적인** 컬러 사용
- **그리드 브레이킹** 레이아웃
- **개성과 창의성** 표현
- **멀티 네온 컬러** 믹스

## Color Palette

### CSS Variables

```css
:root {
  /* Primary - Dark Canvas */
  --bg-primary: #0f0f0f;
  --bg-secondary: #1a1a1a;
  --bg-card: #252525;

  /* Neon Accent Colors */
  --neon-magenta: #ff00ff;      /* Electric Magenta */
  --neon-cyan: #00ffff;         /* Cyber Cyan */
  --neon-lime: #c8ff00;         /* Acid Lime */
  --neon-orange: #ff6600;       /* Hot Orange */
  --neon-blue: #0066ff;         /* Electric Blue */
  --neon-pink: #ff0080;         /* Hot Pink */

  /* Muted versions (for backgrounds) */
  --muted-magenta: rgba(255, 0, 255, 0.15);
  --muted-cyan: rgba(0, 255, 255, 0.15);
  --muted-lime: rgba(200, 255, 0, 0.15);

  /* Text */
  --text-primary: #ffffff;
  --text-secondary: #b0b0b0;
}
```

### Color Reference Table

| Role | HEX | PptxGenJS | Usage |
|------|-----|-----------|-------|
| Dark Canvas | #0f0f0f | `0f0f0f` | 메인 배경 |
| Dark Secondary | #1a1a1a | `1a1a1a` | 보조 배경 |
| Card | #252525 | `252525` | 콘텐츠 카드 |
| White | #ffffff | `ffffff` | 주요 텍스트 |
| Light Gray | #b0b0b0 | `b0b0b0` | 보조 텍스트 |
| Electric Magenta | #ff00ff | `ff00ff` | 주요 강조 |
| Cyber Cyan | #00ffff | `00ffff` | 링크, 하이라이트 |
| Acid Lime | #c8ff00 | `c8ff00` | 경고, 액션 |
| Hot Orange | #ff6600 | `ff6600` | CTA |
| Electric Blue | #0066ff | `0066ff` | 보조 강조 |
| Hot Pink | #ff0080 | `ff0080` | 포인트 |

## Typography

### Font Stack

```css
--font-display: 'Space Grotesk', 'Archivo Black', sans-serif;
--font-body: 'Pretendard', 'Inter', sans-serif;
```

### Size Hierarchy (Points)

| Level | Size | Weight | Letter Spacing | Line Height | Usage |
|-------|------|--------|----------------|-------------|-------|
| Hero | 120pt | 900 | -0.05em | 0.9 | 대형 헤드라인 |
| Title | 48pt | 800 | -0.03em | 1.0 | 슬라이드 제목 |
| Subtitle | 24pt | 600 | -0.01em | 1.2 | 부제목 |
| Body | 18pt | 400 | 0 | 1.6 | 본문 |
| Caption | 13pt | 400 | 0.02em | 1.4 | 캡션 |
| Label | 11pt | 700 | 0.1em | 1.0 | 라벨 |

### Typography Note

- **Extra Black (900)** for Hero - 최대 임팩트
- **Tight line height (0.9)** - 밀도 있는 헤드라인
- **Negative letter spacing** - 타이트한 느낌

## Design Elements

### Neon Glow

```css
.neon-glow {
  text-shadow:
    0 0 5px currentColor,
    0 0 10px currentColor,
    0 0 20px currentColor,
    0 0 40px currentColor;
}

.neon-box-glow {
  box-shadow:
    0 0 10px currentColor,
    0 0 20px currentColor,
    inset 0 0 10px rgba(255, 255, 255, 0.1);
}
```

### Neon Borders

```css
.neon-border {
  border: 3px solid #ff00ff;
  box-shadow: 0 0 20px rgba(255, 0, 255, 0.5);
}

.neon-border-cyan {
  border: 3px solid #00ffff;
  box-shadow: 0 0 20px rgba(0, 255, 255, 0.5);
}
```

### Glitch Effect (for web/animation)

```css
.glitch {
  position: relative;
}

.glitch::before,
.glitch::after {
  content: attr(data-text);
  position: absolute;
  top: 0;
  left: 0;
}

.glitch::before {
  color: #00ffff;
  clip: rect(0, 900px, 0, 0);
  animation: glitch-1 2s infinite;
}

.glitch::after {
  color: #ff00ff;
  clip: rect(0, 900px, 0, 0);
  animation: glitch-2 2s infinite;
}
```

### Asymmetric Layouts

```css
.offset-left {
  transform: translateX(-20pt);
}

.offset-right {
  transform: translateX(20pt);
}

.rotate-slight {
  transform: rotate(-3deg);
}
```

### Overlapping Elements

```css
.overlap-layer {
  position: relative;
  z-index: 1;
  margin-top: -30pt;
}
```

## Slide Layouts

### Cover Slide (Maximum Impact)

```
┌──────────────────────────────────────────────────┐
│▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓│
│▓                                              ▓▓▓│
│▓      WE                                      ▓▓▓│
│▓      CREATE                                  ▓▓▓│
│▓      THE                                     ▓▓▓│
│▓      IMPOSSIBLE                              ▓▓▓│
│▓                                              ▓▓▓│
│▓      ────────                                ▓▓▓│
│▓      CREATIVE AGENCY                         ▓▓▓│
│▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓│
└──────────────────────────────────────────────────┘

Background: Dark Canvas (#0f0f0f)
"WE": Magenta (#ff00ff) with glow, 120pt
"CREATE": White, 120pt
"THE": White, 120pt
"IMPOSSIBLE": Cyan (#00ffff) with glow, 120pt
Subtitle: Lime (#c8ff00), 14pt, uppercase, spaced
```

### Portfolio Grid

```
┌──────────────────────────────────────────────────┐
│  SELECTED WORKS                           [##]   │
├──────────────────────────────────────────────────┤
│                                                   │
│  ┌─────────────────┐  ┌─────────────────────────┐│
│  │                 │  │                         ││
│  │   [PROJECT 1]   │  │      [PROJECT 2]        ││
│  │    ░░░░░░░░░    │  │       ░░░░░░░░░░        ││
│  │                 │  │                         ││
│  │   BRAND X       │  │      CAMPAIGN Y         ││
│  └─────────────────┘  └─────────────────────────┘│
│                                                   │
│  ┌──────────────────────────┐  ┌────────────────┐│
│  │                          │  │                ││
│  │       [PROJECT 3]        │  │  [PROJECT 4]   ││
│  │        ░░░░░░░░░         │  │   ░░░░░░░░     ││
│  │                          │  │                ││
│  │       DIGITAL Z          │  │   APP W        ││
│  └──────────────────────────┘  └────────────────┘│
│                                                   │
└──────────────────────────────────────────────────┘

Title: White, 48pt
Cards: Different neon borders (Magenta, Cyan, Lime, Orange)
Labels: Respective neon colors, 14pt
```

### Services Slide (Neon List)

```
┌──────────────────────────────────────────────────┐
│  WHAT WE DO                               [##]   │
├──────────────────────────────────────────────────┤
│                                                   │
│  ┌──────────────────────────────────────────┐    │
│  │ 01  BRANDING          ░░░░░░░░░░░░░░░░░ │    │
│  │ ───────────────────────────────────────── │    │
│  │ 02  DIGITAL DESIGN    ░░░░░░░░░░░░░░░░░ │    │
│  │ ───────────────────────────────────────── │    │
│  │ 03  MOTION GRAPHICS   ░░░░░░░░░░░░░░░░░ │    │
│  │ ───────────────────────────────────────── │    │
│  │ 04  DEVELOPMENT       ░░░░░░░░░░░░░░░░░ │    │
│  │ ───────────────────────────────────────── │    │
│  │ 05  STRATEGY          ░░░░░░░░░░░░░░░░░ │    │
│  └──────────────────────────────────────────┘    │
│                                                   │
└──────────────────────────────────────────────────┘

Numbers: Rotating neon colors (Magenta, Cyan, Lime, Orange, Pink)
Titles: White, 24pt, Bold
Dividers: Gradient lines (dark → neon → dark)
```

### Stats Slide (Neon Impact)

```
┌──────────────────────────────────────────────────┐
│                                                   │
│                                                   │
│         127                    95%               │
│     ─────────               ─────────            │
│     PROJECTS                RETENTION            │
│                                                   │
│           15                    42               │
│       ─────────             ─────────            │
│         AWARDS              TEAM SIZE            │
│                                                   │
│                                                   │
└──────────────────────────────────────────────────┘

Values: Different neon colors, 96pt, glow effect
Labels: White, 14pt, uppercase
```

### Section Divider

```
┌──────────────────────────────────────────────────┐
│▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓│
│▓                                              ▓▓▓│
│▓                                              ▓▓▓│
│▓             02                               ▓▓▓│
│▓             ══════                           ▓▓▓│
│▓             PROCESS                          ▓▓▓│
│▓                                              ▓▓▓│
│▓                                              ▓▓▓│
│▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓│
└──────────────────────────────────────────────────┘

Background: Dark Canvas
Number: Cyan (#00ffff), 96pt, glow
Divider: Neon double line
Title: White, 72pt
```

## Color Rotation System

For variety across slides:

```javascript
const NEON_ROTATION = [
  'ff00ff',  // Magenta
  '00ffff',  // Cyan
  'c8ff00',  // Lime
  'ff6600',  // Orange
  'ff0080',  // Pink
  '0066ff'   // Blue
];

function getAccentColor(index) {
  return NEON_ROTATION[index % NEON_ROTATION.length];
}
```

## Accessibility Guidelines

### Contrast Ratios (Dark Mode)

| Combination | Ratio | Status |
|-------------|-------|--------|
| White on Dark | 19.4:1 | ✅ AAA |
| Cyan on Dark | 15.1:1 | ✅ AAA |
| Lime on Dark | 17.8:1 | ✅ AAA |
| Magenta on Dark | 6.4:1 | ✅ AA |

### Neon Readability

- Use neon colors for headlines, not body text
- White body text on dark backgrounds
- Glow effects enhance readability, not reduce it

## Use Cases

| Scenario | Recommended Style |
|----------|-------------------|
| 에이전시 피치 | Maximum neon impact |
| 포트폴리오 | Grid with color-coded projects |
| 브랜드 제안 | Restrained neon accents |
| 아트 프로젝트 | Experimental layouts |
| 크리에이티브 리뷰 | Clean with neon highlights |

## PptxGenJS Implementation

```javascript
// Creative Neon colors (no # prefix)
const CREATIVE_COLORS = {
  bgPrimary: '0f0f0f',
  bgSecondary: '1a1a1a',
  bgCard: '252525',
  textPrimary: 'ffffff',
  textSecondary: 'b0b0b0',
  neonMagenta: 'ff00ff',
  neonCyan: '00ffff',
  neonLime: 'c8ff00',
  neonOrange: 'ff6600',
  neonBlue: '0066ff',
  neonPink: 'ff0080'
};

// Dark canvas background
slide.background = { color: CREATIVE_COLORS.bgPrimary };

// Neon headline with glow
slide.addText('CREATE', {
  x: 0.7, y: 2, w: 11.93, h: 2,
  fontSize: 120,
  fontFace: 'Pretendard',
  color: CREATIVE_COLORS.neonMagenta,
  bold: true,
  shadow: { type: 'outer', blur: 40, color: CREATIVE_COLORS.neonMagenta, offset: 0, opacity: 0.8 }
});

// Neon border card
slide.addShape('rect', {
  x: 1, y: 2, w: 5, h: 3,
  fill: { type: 'none' },
  line: { color: CREATIVE_COLORS.neonCyan, width: 3 },
  shadow: { type: 'outer', blur: 20, color: CREATIVE_COLORS.neonCyan, offset: 0, opacity: 0.5 }
});

// Service item with neon number
slide.addText('01', {
  x: 1, y: 2, w: 0.8, h: 0.6,
  fontSize: 24,
  fontFace: 'Pretendard',
  color: CREATIVE_COLORS.neonMagenta,
  bold: true
});
slide.addText('BRANDING', {
  x: 2, y: 2, w: 8, h: 0.6,
  fontSize: 24,
  fontFace: 'Pretendard',
  color: CREATIVE_COLORS.textPrimary,
  bold: true
});
```

## Related Themes

- **Alternative:** Startup Gradient (스타트업 크리에이티브)
- **Professional Version:** Modern Dark (기업 크리에이티브)
- **Futuristic Version:** AI Futuristic (테크 아트)
