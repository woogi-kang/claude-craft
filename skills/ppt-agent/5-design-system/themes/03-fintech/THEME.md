---
name: theme-fintech
description: |
  Fintech Bold 테마. 핀테크, 페이먼트, 크립토, 인슈어테크, 뱅킹 혁신 발표에 최적화.
  "핀테크", "금융", "페이먼트", "크립토", "뱅킹", "인슈어테크" 키워드로 활성화.
tags: [fintech, payment, crypto, insurtech, banking, finance, blockchain]
---

# Fintech Bold Theme

혁신과 미래지향적 이미지의 핀테크 전문 디자인 테마입니다.

## Design Philosophy

- **혁신과 미래지향적** 이미지
- **전통 금융의 신뢰감** + **테크의 역동성**
- **퍼플 계열**로 프리미엄하면서 현대적인 느낌
- **대비가 강한 Bold** 타이포그래피

## Color Palette

### CSS Variables

```css
:root {
  /* Primary - Dark Mode Base */
  --bg-primary: #0c0c14;        /* Deep Space */
  --bg-secondary: #16162a;
  --bg-card: #1e1e38;
  --bg-elevated: #28284a;

  /* Text */
  --text-primary: #ffffff;
  --text-secondary: #a0a0c0;
  --text-muted: #6060a0;

  /* Accent Colors */
  --accent-primary: #8b5cf6;    /* Fintech Purple */
  --accent-secondary: #06ffa5;  /* Neon Green */
  --accent-tertiary: #00d4ff;   /* Cyan */
  --accent-warning: #fbbf24;    /* Gold */

  /* Gradient */
  --gradient-hero: linear-gradient(135deg, #8b5cf6 0%, #06ffa5 100%);
  --gradient-card: linear-gradient(180deg, #1e1e38 0%, #16162a 100%);
}
```

### Color Reference Table

| Role | HEX | PptxGenJS | Usage |
|------|-----|-----------|-------|
| Deep Space | #0c0c14 | `0c0c14` | 메인 배경 |
| Dark Secondary | #16162a | `16162a` | 보조 배경 |
| Card BG | #1e1e38 | `1e1e38` | 카드, 데이터 블록 |
| Elevated | #28284a | `28284a` | 호버, 강조 카드 |
| White | #ffffff | `ffffff` | 주요 텍스트 |
| Light Purple | #a0a0c0 | `a0a0c0` | 보조 텍스트 |
| Fintech Purple | #8b5cf6 | `8b5cf6` | 주요 CTA, 강조 |
| Neon Green | #06ffa5 | `06ffa5` | 성공, 상승, 긍정 수치 |
| Cyan | #00d4ff | `00d4ff` | 보조 강조, 차트 |
| Gold | #fbbf24 | `fbbf24` | 경고, 프리미엄 표시 |

## Typography

### Font Stack

```css
--font-family: 'Pretendard', 'Inter', 'SF Pro Display', sans-serif;
```

### Size Hierarchy (Points)

| Level | Size | Weight | Letter Spacing | Usage |
|-------|------|--------|----------------|-------|
| Hero | 84pt | 800 | -0.03em | 타이틀 슬라이드 |
| Metric | 96pt | 700 | -0.03em | 대형 수치 표시 |
| Title | 42pt | 700 | -0.02em | 슬라이드 제목 |
| Subtitle | 24pt | 600 | -0.01em | 부제목 |
| Body | 18pt | 400 | 0 | 본문 |
| Caption | 13pt | 400 | 0.02em | 캡션 |
| Label | 11pt | 500 | 0.05em | 라벨 |

### Typography Note

- **Extra Bold (800)** for Hero - 강한 임팩트
- **Negative letter spacing** - 타이트한 느낌

## Design Elements

### Glassmorphism Cards

```css
.glass-card {
  background: rgba(30, 30, 56, 0.6);
  backdrop-filter: blur(20px);
  border: 1px solid rgba(139, 92, 246, 0.3);
  border-radius: 16px;
  padding: 24pt;
}
```

### Neon Glow Effect

```css
.neon-text {
  color: #8b5cf6;
  text-shadow: 0 0 10px rgba(139, 92, 246, 0.5),
               0 0 20px rgba(139, 92, 246, 0.3),
               0 0 40px rgba(139, 92, 246, 0.2);
}

.neon-border {
  box-shadow: 0 0 20px rgba(139, 92, 246, 0.3),
              inset 0 0 20px rgba(139, 92, 246, 0.05);
}
```

### Metric Display

```css
.metric-value {
  font-size: 96pt;
  font-weight: 700;
  color: #06ffa5;  /* Neon Green for positive */
  letter-spacing: -0.03em;
}

.metric-value.negative {
  color: #f43f5e;  /* Red for negative */
}

.metric-label {
  font-size: 14pt;
  color: #a0a0c0;
  text-transform: uppercase;
  letter-spacing: 0.1em;
}
```

### Chart Colors

```
Primary Spectrum:
#8b5cf6 (Purple) → #00d4ff (Cyan) → #06ffa5 (Green)

Status Colors:
Positive: #06ffa5
Negative: #f43f5e
Neutral: #a0a0c0
Warning: #fbbf24
```

## Slide Layouts

### Cover Slide

```
┌──────────────────────────────────────────────────┐
│▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓│
│▓                                              ▓▓▓│
│▓  [Logo]                                      ▓▓▓│
│▓                                              ▓▓▓│
│▓           REVOLUTIONIZING                    ▓▓▓│
│▓           DIGITAL PAYMENTS                   ▓▓▓│
│▓           ──────────────────                 ▓▓▓│
│▓           Series A Pitch Deck                ▓▓▓│
│▓                                              ▓▓▓│
│▓  [Date]                        [Contact]     ▓▓▓│
│▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓│
└──────────────────────────────────────────────────┘

Background: Purple → Green gradient (subtle)
Title: White, 84pt, Extra Bold
Subtitle: Light Purple (#a0a0c0), 24pt
```

### Key Metrics Slide

```
┌──────────────────────────────────────────────────┐
│  [TRACTION]                               [##]   │
├──────────────────────────────────────────────────┤
│                                                   │
│  ┌─────────────────────────────────────────────┐ │
│  │     $2.5B          320%         99.9%       │ │
│  │   ─────────      ─────────    ─────────     │ │
│  │     TPV           YoY Growth   Uptime       │ │
│  │                                             │ │
│  │    ▲ +45%         ▲ +120%     ● Live        │ │
│  └─────────────────────────────────────────────┘ │
│                                                   │
│  ┌────────────┐  ┌────────────┐  ┌────────────┐ │
│  │   1.2M     │  │    45+     │  │   $12M     │ │
│  │ ────────── │  │ ────────── │  │ ────────── │ │
│  │   Users    │  │  Partners  │  │  Revenue   │ │
│  └────────────┘  └────────────┘  └────────────┘ │
│                                                   │
└──────────────────────────────────────────────────┘

Hero Metrics: Neon Green (#06ffa5), 72pt
Card Background: #1e1e38
Labels: Light Purple (#a0a0c0), 14pt
```

### Transaction Flow Diagram

```
┌──────────────────────────────────────────────────┐
│  HOW IT WORKS                             [##]   │
├──────────────────────────────────────────────────┤
│                                                   │
│  ┌────────┐      ┌────────┐      ┌────────┐     │
│  │ ░░░░░░ │  ──► │ ░░░░░░ │  ──► │ ░░░░░░ │     │
│  │  User  │      │ Process │      │  Bank  │     │
│  └────────┘      └────────┘      └────────┘     │
│       │               │               │          │
│       ▼               ▼               ▼          │
│   Initiate       Validate        Complete        │
│   Payment        & Route         Transfer        │
│                                                   │
│   < 0.1 sec      < 0.5 sec       < 1.0 sec      │
│                                                   │
└──────────────────────────────────────────────────┘

Nodes: Glass cards with purple border
Arrows: Cyan (#00d4ff)
Labels: White, 16pt
Timing: Neon Green, 14pt
```

### Section Divider

```
┌──────────────────────────────────────────────────┐
│▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓│
│▓                                              ▓▓▓│
│▓  03                                          ▓▓▓│
│▓  ─────────────────────                       ▓▓▓│
│▓  SECURITY &                                  ▓▓▓│
│▓  COMPLIANCE                                  ▓▓▓│
│▓                                              ▓▓▓│
│▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓│
└──────────────────────────────────────────────────┘

Background: Deep Space (#0c0c14)
Number: Fintech Purple (#8b5cf6), 96pt, glow effect
Title: White, 54pt
```

## Special Effects

### Gradient Text (CSS)

```css
.gradient-text {
  background: linear-gradient(135deg, #8b5cf6 0%, #06ffa5 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}
```

### Animated Border (for web)

```css
.animated-border {
  position: relative;
  background: #1e1e38;
  border-radius: 16px;
}

.animated-border::before {
  content: '';
  position: absolute;
  inset: -2px;
  background: linear-gradient(135deg, #8b5cf6, #06ffa5, #00d4ff, #8b5cf6);
  border-radius: 18px;
  z-index: -1;
  background-size: 300% 300%;
  animation: gradient-spin 3s linear infinite;
}
```

## Accessibility Guidelines

### Contrast Ratios (Dark Mode)

| Combination | Ratio | Status |
|-------------|-------|--------|
| White on Deep Space | 19.5:1 | ✅ AAA |
| Purple on Deep Space | 5.8:1 | ✅ AA |
| Neon Green on Deep Space | 12.4:1 | ✅ AAA |
| Light Purple on Deep Space | 7.2:1 | ✅ AAA |

### Minimum Font Sizes

- Body text: 18pt
- Captions: 13pt
- Metric values: 48pt minimum for readability

## Use Cases

| Scenario | Recommended Style |
|----------|-------------------|
| 투자자 피치 | Hero metrics, glass cards |
| 제품 데모 | Flow diagrams, neon accents |
| 분기 리포트 | Data cards, chart focus |
| 파트너십 제안 | Corporate + bold metrics |
| 크립토/Web3 | Maximum neon, gradient text |

## PptxGenJS Implementation

```javascript
// Fintech theme colors (no # prefix)
const FINTECH_COLORS = {
  bgPrimary: '0c0c14',
  bgSecondary: '16162a',
  bgCard: '1e1e38',
  textPrimary: 'ffffff',
  textSecondary: 'a0a0c0',
  accentPrimary: '8b5cf6',
  accentSecondary: '06ffa5',
  accentTertiary: '00d4ff',
  accentWarning: 'fbbf24'
};

// Dark slide background
slide.background = { color: FINTECH_COLORS.bgPrimary };

// Metric card
slide.addShape('rect', {
  x: 1, y: 2, w: 3.5, h: 2.5,
  fill: { color: FINTECH_COLORS.bgCard },
  line: { color: FINTECH_COLORS.accentPrimary, width: 1, transparency: 70 },
  shadow: { type: 'outer', blur: 40, color: FINTECH_COLORS.accentPrimary, offset: 0, opacity: 0.15 }
});

// Neon metric value
slide.addText('$2.5B', {
  x: 1, y: 2.2, w: 3.5, h: 1.5,
  fontSize: 72,
  fontFace: 'Pretendard',
  color: FINTECH_COLORS.accentSecondary,
  bold: true,
  align: 'center'
});
```

## Related Themes

- **Alternative:** AI Futuristic (더 테크 포커스)
- **Corporate Version:** Corporate Blue (전통 금융 발표)
- **Bold Version:** Startup Gradient (스타트업 피치)
