---
name: theme-real-estate
description: |
  Real Estate Trust 테마. 부동산, 투자, 자산관리, 건설, 개발 발표에 최적화.
  "부동산", "투자", "자산", "건설", "개발", "프로젝트" 키워드로 활성화.
tags: [real-estate, investment, property, construction, development, asset]
---

# Real Estate Trust Theme

신뢰와 안정성을 강조하는 부동산/투자 전문 디자인 테마입니다.

## Design Philosophy

- **신뢰와 안정성** 강조
- **네이비 + 골드**의 클래식 조합
- **깔끔한 데이터 시각화**
- **프로페셔널한** 톤

## Color Palette

### CSS Variables

```css
:root {
  /* Primary - Clean Professional */
  --bg-primary: #ffffff;
  --bg-secondary: #f5f7fa;
  --bg-accent: #eef2f7;
  --bg-dark: #0d1b2a;           /* Navy Dark */

  /* Text */
  --text-primary: #0d1b2a;
  --text-secondary: #415a77;
  --text-muted: #778da9;
  --text-on-dark: #ffffff;

  /* Accent Colors */
  --accent-navy: #1b4965;       /* Corporate Navy */
  --accent-blue: #62b6cb;       /* Sky Blue */
  --accent-gold: #c9a962;       /* Trust Gold */
  --accent-burgundy: #7a3b3f;   /* Luxury Accent */

  /* Status Colors */
  --status-success: #48a868;
  --status-warning: #e8a858;
  --status-alert: #c45a5a;
}
```

### Color Reference Table

| Role | HEX | PptxGenJS | Usage |
|------|-----|-----------|-------|
| White | #ffffff | `ffffff` | 메인 배경 |
| Light Gray | #f5f7fa | `f5f7fa` | 섹션 배경 |
| Accent BG | #eef2f7 | `eef2f7` | 하이라이트 영역 |
| Navy Dark | #0d1b2a | `0d1b2a` | 헤더, 다크 섹션 |
| Primary Text | #0d1b2a | `0d1b2a` | 제목 |
| Secondary Text | #415a77 | `415a77` | 본문 |
| Muted Text | #778da9 | `778da9` | 캡션 |
| Corporate Navy | #1b4965 | `1b4965` | 주요 강조 |
| Sky Blue | #62b6cb | `62b6cb` | 차트, 아이콘 |
| Trust Gold | #c9a962 | `c9a962` | 프리미엄 표시 |
| Burgundy | #7a3b3f | `7a3b3f` | 하이엔드 포인트 |

## Typography

### Font Stack

```css
--font-display: 'Pretendard', 'Georgia', serif;
--font-body: 'Pretendard', 'Inter', sans-serif;
```

### Size Hierarchy (Points)

| Level | Size | Weight | Usage |
|-------|------|--------|-------|
| Hero | 64pt | 600 | 타이틀 슬라이드 |
| Title | 32pt | 600 | 슬라이드 제목 |
| Subtitle | 22pt | 500 | 부제목 |
| Body | 17pt | 400 | 본문 |
| Caption | 13pt | 400 | 캡션, 출처 |
| Label | 11pt | 500 | 라벨, 태그 |

### Typography Note

- **Balanced weight** - 전문적이면서 친근
- **Slightly larger body** (17pt) - 가독성

## Design Elements

### Property Cards

```css
.property-card {
  background: #ffffff;
  border-radius: 8px;
  box-shadow: 0 2px 12px rgba(13, 27, 42, 0.08);
  overflow: hidden;
}

.property-card .header {
  background: #0d1b2a;
  color: #ffffff;
  padding: 16pt;
}

.property-card .body {
  padding: 20pt;
}
```

### Data Tables

```css
.data-table {
  width: 100%;
  border-collapse: collapse;
}

.data-table th {
  background: #0d1b2a;
  color: #ffffff;
  padding: 12pt 16pt;
  text-align: left;
  font-size: 12pt;
  font-weight: 600;
}

.data-table td {
  padding: 12pt 16pt;
  border-bottom: 1px solid #eef2f7;
  font-size: 14pt;
}

.data-table tr:nth-child(even) {
  background: #f5f7fa;
}
```

### Investment Metrics

```css
.metric-card {
  background: #f5f7fa;
  border-radius: 8px;
  padding: 24pt;
  border-left: 4px solid #1b4965;
}

.metric-value {
  font-size: 48pt;
  font-weight: 700;
  color: #1b4965;
}

.metric-label {
  font-size: 13pt;
  color: #778da9;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}
```

### Gold Accent Elements

```css
.premium-badge {
  display: inline-block;
  background: #c9a962;
  color: #0d1b2a;
  padding: 4pt 12pt;
  font-size: 10pt;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.1em;
}

.gold-border-card {
  border: 1px solid #c9a962;
  padding: 20pt;
}
```

### Location/Map Style

```css
.map-container {
  background: #eef2f7;
  border: 1px solid #c0d0e0;
  border-radius: 8px;
}

.location-marker {
  width: 20pt;
  height: 20pt;
  background: #1b4965;
  border-radius: 50%;
  border: 3px solid #c9a962;
}
```

## Slide Layouts

### Cover Slide

```
┌──────────────────────────────────────────────────┐
│▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓│
│▓                                              ▓▓▓│
│▓  [COMPANY LOGO]                              ▓▓▓│
│▓                                              ▓▓▓│
│▓           PRIME TOWER                        ▓▓▓│
│▓           DEVELOPMENT                        ▓▓▓│
│▓           ──────────                         ▓▓▓│
│▓           Investment Opportunity             ▓▓▓│
│▓                                              ▓▓▓│
│▓  [Property Image/Render]                     ▓▓▓│
│▓                                              ▓▓▓│
│▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓│
└──────────────────────────────────────────────────┘

Background: Navy Dark (#0d1b2a)
Title: White, 64pt
Subtitle: Gold (#c9a962), 18pt
Divider: Gold line
```

### Investment Summary

```
┌──────────────────────────────────────────────────┐
│  [INVESTMENT OVERVIEW]                    [##]   │
├──────────────────────────────────────────────────┤
│                                                   │
│  Key Investment Metrics                          │
│                                                   │
│  ┌────────────┐  ┌────────────┐  ┌────────────┐ │
│  │   8.5%     │  │   $125M    │  │   2027     │ │
│  │ ────────── │  │ ────────── │  │ ────────── │ │
│  │ Target IRR │  │Total Value │  │ Completion │ │
│  └────────────┘  └────────────┘  └────────────┘ │
│                                                   │
│  ┌────────────────────────────────────────────┐  │
│  │  Investment Structure                      │  │
│  │  ├── Equity:      60%    ████████████░░░░ │  │
│  │  ├── Debt:        35%    ██████████░░░░░░ │  │
│  │  └── Mezzanine:    5%    ██░░░░░░░░░░░░░░ │  │
│  └────────────────────────────────────────────┘  │
│                                                   │
└──────────────────────────────────────────────────┘

Metric Values: Corporate Navy (#1b4965), 48pt
Labels: Muted Text (#778da9), 13pt
Cards: White with navy left border
Progress: Navy (#1b4965) fill
```

### Property Overview

```
┌──────────────────────────────────────────────────┐
│  [PROPERTY DETAILS]                       [##]   │
├──────────────────────────────────────────────────┤
│                                                   │
│  ┌──────────────────────┐  PRIME TOWER          │
│  │                      │  ────────────          │
│  │                      │                        │
│  │   [Property Photo]   │  Location: Gangnam    │
│  │                      │  Type: Mixed-Use      │
│  │                      │  GFA: 125,000 sqm     │
│  │                      │  Floors: 45           │
│  │                      │                        │
│  │                      │  ┌────────────────┐   │
│  │                      │  │ 🏆 PREMIUM    │   │
│  └──────────────────────┘  └────────────────┘   │
│                                                   │
└──────────────────────────────────────────────────┘

Photo: White border, subtle shadow
Title: Primary Text (#0d1b2a), 28pt
Details: Secondary Text (#415a77), 16pt
Premium Badge: Gold background
```

### Financial Projections

```
┌──────────────────────────────────────────────────┐
│  [FINANCIAL PROJECTIONS]                  [##]   │
├──────────────────────────────────────────────────┤
│                                                   │
│  ┌────────────────────────────────────────────┐  │
│  │         Year      Revenue     NOI          │  │
│  │  ┼──────────────────────────────────────── │  │
│  │         2024      $8.2M      $5.8M         │  │
│  │         2025      $10.5M     $7.4M         │  │
│  │         2026      $12.8M     $9.0M         │  │
│  │         2027      $15.2M     $10.6M        │  │
│  └────────────────────────────────────────────┘  │
│                                                   │
│  Revenue Growth                                  │
│  2024 ████████░░░░░░░░░░░░░░░░░░░░░░  $8.2M    │
│  2025 ████████████░░░░░░░░░░░░░░░░░░  $10.5M   │
│  2026 ████████████████░░░░░░░░░░░░░░  $12.8M   │
│  2027 ████████████████████░░░░░░░░░░  $15.2M   │
│                                                   │
└──────────────────────────────────────────────────┘

Table Header: Navy Dark background
Table Data: Alternating row colors
Progress Bars: Navy → Sky Blue gradient
Values: Corporate Navy, bold
```

### Section Divider

```
┌──────────────────────────────────────────────────┐
│▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓│
│▓                                              ▓▓▓│
│▓  03                                          ▓▓▓│
│▓  ─────────────────────                       ▓▓▓│
│▓  FINANCIAL                                   ▓▓▓│
│▓  ANALYSIS                                    ▓▓▓│
│▓                                              ▓▓▓│
│▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓│
└──────────────────────────────────────────────────┘

Background: Navy Dark (#0d1b2a)
Number: Gold (#c9a962), 72pt
Divider: Gold line
Title: White, 48pt
```

### Comparable Analysis

```
┌──────────────────────────────────────────────────┐
│  [MARKET COMPARABLES]                     [##]   │
├──────────────────────────────────────────────────┤
│                                                   │
│  ┌─────────┬──────────┬────────┬────────┬──────┐│
│  │Property │ Location │ Size   │Price/SF│ Cap  ││
│  ├─────────┼──────────┼────────┼────────┼──────┤│
│  │Tower A  │Gangnam   │85K sqm │$450    │ 5.2% ││
│  │Tower B  │Yeouido   │92K sqm │$420    │ 5.5% ││
│  │Tower C  │CBD       │78K sqm │$480    │ 4.8% ││
│  │Ours     │Gangnam   │125K sqm│$425    │ 5.0% ││
│  └─────────┴──────────┴────────┴────────┴──────┘│
│                                                   │
│  ★ Our project offers competitive positioning    │
│                                                   │
└──────────────────────────────────────────────────┘

Header: Navy Dark background, white text
Highlight Row: Light gold background for "Ours"
Callout: Gold star icon
```

## Chart Color Scheme

```
60/30/10 Rule:
- 60%: Corporate Navy (#1b4965)
- 30%: Sky Blue (#62b6cb)
- 10%: Trust Gold (#c9a962)
```

## Accessibility Guidelines

### Contrast Ratios

| Combination | Ratio | Status |
|-------------|-------|--------|
| Navy on White | 14.8:1 | ✅ AAA |
| Secondary on White | 6.5:1 | ✅ AA |
| White on Navy | 14.8:1 | ✅ AAA |
| Gold on Navy | 5.8:1 | ✅ AA |

## Use Cases

| Scenario | Recommended Style |
|----------|-------------------|
| 투자 제안서 | Metric cards, financial tables |
| 개발 프로젝트 | Property showcase, timeline |
| 자산 보고서 | Data tables, charts |
| 임대 제안 | Location maps, comparables |
| 펀드 소개 | Investment summary |

## PptxGenJS Implementation

```javascript
// Real Estate theme colors (no # prefix)
const REALESTATE_COLORS = {
  bgPrimary: 'ffffff',
  bgSecondary: 'f5f7fa',
  bgAccent: 'eef2f7',
  bgDark: '0d1b2a',
  textPrimary: '0d1b2a',
  textSecondary: '415a77',
  textMuted: '778da9',
  accentNavy: '1b4965',
  accentBlue: '62b6cb',
  accentGold: 'c9a962',
  accentBurgundy: '7a3b3f'
};

// Clean white background
slide.background = { color: REALESTATE_COLORS.bgPrimary };

// Navy header bar
slide.addShape('rect', {
  x: 0, y: 0, w: 13.33, h: 1,
  fill: { color: REALESTATE_COLORS.bgDark }
});

// Metric card with navy border
slide.addShape('rect', {
  x: 1, y: 2, w: 3.5, h: 2,
  fill: { color: REALESTATE_COLORS.bgSecondary },
  line: { color: REALESTATE_COLORS.accentNavy, width: 0 }
});
// Left border effect
slide.addShape('rect', {
  x: 1, y: 2, w: 0.05, h: 2,
  fill: { color: REALESTATE_COLORS.accentNavy }
});

// Metric value
slide.addText('8.5%', {
  x: 1.2, y: 2.3, w: 3.1, h: 1,
  fontSize: 48,
  fontFace: 'Pretendard',
  color: REALESTATE_COLORS.accentNavy,
  bold: true
});

// Gold premium badge
slide.addShape('rect', {
  x: 8, y: 4, w: 2, h: 0.4,
  fill: { color: REALESTATE_COLORS.accentGold }
});
slide.addText('PREMIUM', {
  x: 8, y: 4, w: 2, h: 0.4,
  fontSize: 10,
  fontFace: 'Pretendard',
  color: REALESTATE_COLORS.bgDark,
  bold: true,
  align: 'center',
  valign: 'middle'
});
```

## Related Themes

- **Alternative:** Corporate Blue (기업 투자)
- **Luxury Version:** Luxury Noir (프리미엄 부동산)
- **ESG Version:** Sustainability Earth (친환경 개발)
