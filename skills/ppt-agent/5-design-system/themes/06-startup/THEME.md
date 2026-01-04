---
name: theme-startup
description: |
  Startup Gradient 테마. 피치덱, 시드/시리즈 펀딩, 스타트업 소개, 데모데이 발표에 최적화.
  "스타트업", "피치", "투자", "펀딩", "시리즈", "VC", "데모데이" 키워드로 활성화.
tags: [startup, pitch, funding, series, vc, investor, demo-day, seed]
---

# Startup Gradient Theme

에너지와 성장 잠재력을 표현하는 스타트업 피치 전문 디자인 테마입니다.

## Design Philosophy

- **에너지와 성장 잠재력** 표현
- **그라데이션**으로 역동성 강조
- **깔끔하지만 Bold**한 타이포그래피
- **핵심 메트릭** 강조

## Color Palette

### CSS Variables

```css
:root {
  /* Primary - Clean Base */
  --bg-primary: #fafafa;
  --bg-secondary: #ffffff;
  --bg-dark: #18181b;

  /* Text */
  --text-primary: #18181b;
  --text-secondary: #52525b;
  --text-muted: #a1a1aa;
  --text-on-dark: #ffffff;

  /* Gradient Accents */
  --accent-start: #f97316;      /* Coral Orange */
  --accent-mid: #ec4899;        /* Pink */
  --accent-end: #8b5cf6;        /* Violet */
  --accent-success: #22c55e;

  /* Gradients */
  --gradient-primary: linear-gradient(135deg, #f97316 0%, #ec4899 50%, #8b5cf6 100%);
  --gradient-subtle: linear-gradient(135deg, rgba(249,115,22,0.1) 0%, rgba(139,92,246,0.1) 100%);
  --gradient-button: linear-gradient(90deg, #f97316 0%, #ec4899 100%);
}
```

### Color Reference Table

| Role | HEX | PptxGenJS | Usage |
|------|-----|-----------|-------|
| Light BG | #fafafa | `fafafa` | 라이트 모드 배경 |
| White | #ffffff | `ffffff` | 카드 배경 |
| Dark BG | #18181b | `18181b` | 다크 섹션, 표지 |
| Primary Text | #18181b | `18181b` | 제목 |
| Secondary Text | #52525b | `52525b` | 본문 |
| Muted | #a1a1aa | `a1a1aa` | 캡션 |
| Coral Orange | #f97316 | `f97316` | 그라데이션 시작 |
| Pink | #ec4899 | `ec4899` | 그라데이션 중간 |
| Violet | #8b5cf6 | `8b5cf6` | 그라데이션 끝 |
| Success Green | #22c55e | `22c55e` | 성장률, 긍정 지표 |

## Typography

### Font Stack

```css
--font-family: 'Pretendard', 'Inter', sans-serif;
```

### Size Hierarchy (Points)

| Level | Size | Weight | Letter Spacing | Usage |
|-------|------|--------|----------------|-------|
| Hero | 88pt | 800 | -0.03em | 타이틀 슬라이드 |
| Metric | 72pt | 700 | -0.02em | 대형 수치 |
| Title | 40pt | 700 | -0.02em | 슬라이드 제목 |
| Subtitle | 24pt | 600 | -0.01em | 부제목 |
| Body | 18pt | 400 | 0 | 본문 |
| Caption | 13pt | 400 | 0.02em | 캡션 |
| Label | 11pt | 600 | 0.05em | 라벨 |

### Typography Note

- **Extra Bold (800)** for Hero - 강한 임팩트
- **Negative letter spacing** - 타이트하고 현대적인 느낌

## Design Elements

### Gradient Cards

```css
.gradient-card {
  background: #ffffff;
  border-radius: 16px;
  padding: 32pt;
  position: relative;
  overflow: hidden;
}

.gradient-card::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 4px;
  background: var(--gradient-primary);
}
```

### Metric Display

```css
.metric-value {
  font-size: 72pt;
  font-weight: 700;
  background: var(--gradient-primary);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}

.metric-label {
  font-size: 14pt;
  color: #52525b;
  text-transform: uppercase;
  letter-spacing: 0.1em;
}

.metric-change {
  font-size: 14pt;
  color: #22c55e;
  font-weight: 600;
}
```

### CTA Buttons

```css
.cta-button {
  background: var(--gradient-button);
  color: #ffffff;
  padding: 12pt 32pt;
  border-radius: 24pt;
  font-size: 14pt;
  font-weight: 600;
}
```

### Progress/Growth Indicator

```css
.growth-bar {
  height: 8px;
  background: #e4e4e7;
  border-radius: 4px;
  overflow: hidden;
}

.growth-bar .fill {
  background: var(--gradient-primary);
  border-radius: 4px;
}
```

### Testimonial/Quote Card

```css
.quote-card {
  background: linear-gradient(135deg, rgba(249,115,22,0.05) 0%, rgba(139,92,246,0.05) 100%);
  border: 1px solid rgba(139,92,246,0.2);
  border-radius: 12px;
  padding: 24pt;
}
```

## Slide Layouts

### Cover Slide (Dark)

```
┌──────────────────────────────────────────────────┐
│▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓│
│▓                                              ▓▓▓│
│▓  [Logo]                                      ▓▓▓│
│▓                                              ▓▓▓│
│▓           TRANSFORMING                       ▓▓▓│
│▓           THE FUTURE OF                      ▓▓▓│
│▓           [INDUSTRY]                         ▓▓▓│
│▓                                              ▓▓▓│
│▓           Series A Pitch Deck                ▓▓▓│
│▓                                              ▓▓▓│
│▓  [Date]                        [Contact]     ▓▓▓│
│▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓│
└──────────────────────────────────────────────────┘

Background: Dark (#18181b)
Title: White, 88pt, Extra Bold
Tagline: Gradient text or Muted (#a1a1aa), 24pt
```

### Traction / Metrics Slide

```
┌──────────────────────────────────────────────────┐
│  [TRACTION]                               [##]   │
├──────────────────────────────────────────────────┤
│                                                   │
│  ┌─────────────────────────────────────────────┐ │
│  │     $5.2M         420%          50K         │ │
│  │   ─────────     ─────────    ─────────      │ │
│  │      ARR        YoY Growth     MAU          │ │
│  │                                             │ │
│  │    ▲ +85%       ▲ +150%      ▲ +200%       │ │
│  └─────────────────────────────────────────────┘ │
│                                                   │
│  Revenue Growth                                  │
│  ████████████████████████████████░░░░░░░░░░ 78% │
│                                                   │
└──────────────────────────────────────────────────┘

Metric Values: Gradient text, 64pt
Labels: Secondary Text (#52525b), 14pt
Growth Indicators: Success Green (#22c55e)
Progress Bar: Gradient fill
```

### Problem / Solution

```
┌──────────────────────────────────────────────────┐
│  THE PROBLEM                              [##]   │
├──────────────────────────────────────────────────┤
│                                                   │
│  [Pain Point Icon - Coral]                       │
│                                                   │
│  "Current solutions are slow,                    │
│   expensive, and frustrating."                   │
│                                                   │
│  ┌─────────────────────────────────────────────┐ │
│  │  85%        $2.5B         3 days            │ │
│  │  of users   wasted        average           │ │
│  │  frustrated annually      wait time         │ │
│  └─────────────────────────────────────────────┘ │
│                                                   │
└──────────────────────────────────────────────────┘

Pain Icon: Coral Orange (#f97316)
Quote: Primary Text (#18181b), 32pt, Italic
Stats: Coral Orange for emphasis
```

### Market Opportunity

```
┌──────────────────────────────────────────────────┐
│  MARKET OPPORTUNITY                       [##]   │
├──────────────────────────────────────────────────┤
│                                                   │
│  ┌───────────────────────────────────────────┐   │
│  │           $85B                            │   │
│  │         TAM 2030                          │   │
│  │                                           │   │
│  │      ┌─────────────────────┐              │   │
│  │      │      $12B           │              │   │
│  │      │      SAM            │              │   │
│  │      │   ┌─────────┐       │              │   │
│  │      │   │  $2.5B  │       │              │   │
│  │      │   │  SOM    │       │              │   │
│  │      │   └─────────┘       │              │   │
│  │      └─────────────────────┘              │   │
│  └───────────────────────────────────────────┘   │
│                                                   │
└──────────────────────────────────────────────────┘

TAM Circle: Light gradient background
SAM Circle: Gradient border
SOM Circle: Solid gradient fill
Values: Gradient text, bold
```

### Section Divider

```
┌──────────────────────────────────────────────────┐
│░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░│
│░░                                            ░░░░│
│░░  02                                        ░░░░│
│░░  ─────────────────────                     ░░░░│
│░░  OUR SOLUTION                              ░░░░│
│░░                                            ░░░░│
│░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░│
└──────────────────────────────────────────────────┘

Background: Full gradient (Orange → Pink → Violet)
Number: White, 96pt
Title: White, 54pt
```

### The Ask / Funding

```
┌──────────────────────────────────────────────────┐
│  THE ASK                                  [##]   │
├──────────────────────────────────────────────────┤
│                                                   │
│           Raising $10M Series A                  │
│           ──────────────────────                 │
│                                                   │
│  ┌────────────┐ ┌────────────┐ ┌────────────┐   │
│  │    40%     │ │    35%     │ │    25%     │   │
│  │  ───────── │ │  ───────── │ │  ───────── │   │
│  │  Product   │ │  Sales &   │ │  Operations│   │
│  │  Dev       │ │  Marketing │ │            │   │
│  └────────────┘ └────────────┘ └────────────┘   │
│                                                   │
│  Use of Funds                                    │
│  ████████████████ ████████████████ ██████████   │
│       40%              35%            25%        │
│                                                   │
└──────────────────────────────────────────────────┘

Headline: Primary Text, 48pt
Percentage: Gradient text, 48pt
Cards: White with gradient top border
Progress: Gradient segments
```

## Gradient Implementation

### Solid Color Fallback for PPTX

Since PPTX doesn't support CSS gradients natively:

```javascript
// Option 1: Use the dominant color
const DOMINANT_COLOR = 'ec4899';  // Pink (middle of gradient)

// Option 2: Use gradient as image background
// Pre-render gradient as PNG
```

### Gradient Text Alternative

```javascript
// Use accent color for "gradient text" effect
const ACCENT_COLOR = 'ec4899';  // Pink

slide.addText('$5.2M', {
  fontSize: 72,
  color: ACCENT_COLOR,
  bold: true
});
```

## Accessibility Guidelines

### Contrast Ratios

| Combination | Ratio | Status |
|-------------|-------|--------|
| Dark Text on Light BG | 15.8:1 | ✅ AAA |
| White on Dark BG | 15.8:1 | ✅ AAA |
| White on Orange | 3.1:1 | ⚠️ Large text only |
| White on Pink | 4.5:1 | ✅ AA |
| White on Violet | 5.8:1 | ✅ AA |

### Gradient Accessibility

- Always use white text on gradient backgrounds
- Ensure minimum 4.5:1 contrast at darkest gradient point

## Use Cases

| Scenario | Recommended Style |
|----------|-------------------|
| Seed 피치 | Clean, metric-focused |
| Series A | Full gradient, professional |
| 데모데이 | High impact, bold numbers |
| 투자자 미팅 | Balanced, data-driven |
| 제품 발표 | Visual, demo-focused |

## PptxGenJS Implementation

```javascript
// Startup theme colors (no # prefix)
const STARTUP_COLORS = {
  bgPrimary: 'fafafa',
  bgSecondary: 'ffffff',
  bgDark: '18181b',
  textPrimary: '18181b',
  textSecondary: '52525b',
  textMuted: 'a1a1aa',
  accentStart: 'f97316',
  accentMid: 'ec4899',
  accentEnd: '8b5cf6',
  accentSuccess: '22c55e'
};

// Dark cover slide
slide.background = { color: STARTUP_COLORS.bgDark };

// Metric card with top gradient border effect
slide.addShape('rect', {
  x: 1, y: 2, w: 3.5, h: 2.5,
  fill: { color: STARTUP_COLORS.bgSecondary },
  shadow: { type: 'outer', blur: 12, offset: 4, angle: 90, opacity: 0.1 }
});
// Top border (use solid color as gradient fallback)
slide.addShape('rect', {
  x: 1, y: 2, w: 3.5, h: 0.05,
  fill: { color: STARTUP_COLORS.accentMid }
});

// Metric value (use accent color)
slide.addText('$5.2M', {
  x: 1, y: 2.3, w: 3.5, h: 1,
  fontSize: 64,
  fontFace: 'Pretendard',
  color: STARTUP_COLORS.accentMid,
  bold: true,
  align: 'center'
});

// Growth indicator
slide.addText('▲ +85%', {
  x: 1, y: 3.5, w: 3.5, h: 0.4,
  fontSize: 14,
  color: STARTUP_COLORS.accentSuccess,
  bold: true,
  align: 'center'
});
```

## Related Themes

- **Alternative:** Fintech Bold (금융 스타트업)
- **Corporate Version:** Corporate Blue (후기 단계 스타트업)
- **Creative Version:** Creative Neon (크리에이티브 스타트업)
