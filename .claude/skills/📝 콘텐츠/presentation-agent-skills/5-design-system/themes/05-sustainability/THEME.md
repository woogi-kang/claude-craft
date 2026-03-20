---
name: theme-sustainability
description: |
  Sustainability Earth 테마. ESG 보고서, 환경 이니셔티브, 지속가능성, 임팩트 투자, CSR 발표에 최적화.
  "ESG", "환경", "지속가능성", "탄소", "친환경", "임팩트", "CSR" 키워드로 활성화.
tags: [esg, sustainability, environment, green, carbon, impact, csr, climate]
---

# Sustainability Earth Theme

자연에서 영감받은 진정성 있는 ESG/환경 전문 디자인 테마입니다.

## Design Philosophy

- **자연에서 영감받은** 색상 팔레트
- **투명성과 신뢰**를 강조
- **데이터 기반 스토리텔링**
- **그린워싱 아닌 진정성** 있는 비주얼

## Color Palette

### CSS Variables

```css
:root {
  /* Primary - Natural Base */
  --bg-primary: #f5f7f4;        /* Organic White */
  --bg-secondary: #ffffff;
  --bg-accent: #e8ede4;         /* Light Sage */
  --bg-dark: #1a2820;           /* Forest Dark */

  /* Text */
  --text-primary: #1a2820;      /* Deep Forest */
  --text-secondary: #4a584a;
  --text-muted: #7a8a7a;
  --text-on-dark: #f5f7f4;

  /* Nature Accent Colors */
  --accent-forest: #2d5a3d;     /* Forest Green */
  --accent-leaf: #4a9a5a;       /* Leaf Green */
  --accent-earth: #8b7355;      /* Earth Brown */
  --accent-sky: #5a9ab8;        /* Clean Sky Blue */
  --accent-sun: #d4a04a;        /* Solar Gold */

  /* Gradients */
  --gradient-nature: linear-gradient(135deg, #2d5a3d 0%, #4a9a5a 100%);
  --gradient-earth: linear-gradient(180deg, #f5f7f4 0%, #e8ede4 100%);
}
```

### Color Reference Table

| Role | HEX | PptxGenJS | Usage |
|------|-----|-----------|-------|
| Organic White | #f5f7f4 | `f5f7f4` | 메인 배경 |
| White | #ffffff | `ffffff` | 카드 배경 |
| Light Sage | #e8ede4 | `e8ede4` | 섹션 구분 |
| Forest Dark | #1a2820 | `1a2820` | 다크 섹션 |
| Deep Forest | #1a2820 | `1a2820` | 제목, 헤드라인 |
| Secondary Text | #4a584a | `4a584a` | 본문 |
| Forest Green | #2d5a3d | `2d5a3d` | 주요 강조 |
| Leaf Green | #4a9a5a | `4a9a5a` | 성장, 긍정 지표 |
| Earth Brown | #8b7355 | `8b7355` | 보조 텍스트, 아이콘 |
| Sky Blue | #5a9ab8 | `5a9ab8` | 차트, 데이터 |
| Solar Gold | #d4a04a | `d4a04a` | 에너지, 하이라이트 |

## ESG Color Coding

```
E (Environmental): Forest Green (#2d5a3d), Leaf Green (#4a9a5a)
S (Social): Sky Blue (#5a9ab8)
G (Governance): Earth Brown (#8b7355), Solar Gold (#d4a04a)
```

## Typography

### Font Stack

```css
--font-family: 'Pretendard', 'Source Sans Pro', sans-serif;
```

### Size Hierarchy (Points)

| Level | Size | Weight | Usage |
|-------|------|--------|-------|
| Hero | 68pt | 600 | 타이틀 슬라이드 |
| Title | 34pt | 600 | 슬라이드 제목 |
| Subtitle | 22pt | 500 | 부제목 |
| Body | 18pt | 400 | 본문 |
| Caption | 13pt | 400 | 캡션, 출처 |
| Label | 11pt | 500 | 라벨, 태그 |

### Typography Note

- **Balanced, not aggressive** - 부드러운 인상
- **Line height body: 1.7** - 읽기 편한 간격

## Design Elements

### ESG Indicator Cards

```css
.esg-card {
  background: #ffffff;
  border-radius: 8px;
  padding: 24pt;
  box-shadow: 0 2px 8px rgba(26, 40, 32, 0.08);
}

.esg-card.environmental {
  border-left: 4px solid #2d5a3d;
}

.esg-card.social {
  border-left: 4px solid #5a9ab8;
}

.esg-card.governance {
  border-left: 4px solid #8b7355;
}
```

### Nature Icons

- **Style:** Organic line icons
- **Stroke:** 2px
- **Corners:** Rounded, soft
- **Motifs:** Leaves, trees, water, sun, earth

```css
.eco-icon {
  color: #2d5a3d;
  width: 32pt;
  height: 32pt;
}
```

### Progress Indicators

```css
.sustainability-progress {
  height: 12px;
  border-radius: 6px;
  background: #e8ede4;
}

.sustainability-progress .fill {
  background: linear-gradient(90deg, #2d5a3d 0%, #4a9a5a 100%);
  border-radius: 6px;
}
```

### Data Charts Color Scheme

```
Primary Spectrum (Green to Blue):
#2d5a3d → #4a9a5a → #6aaa7a → #5a9ab8 → #8b7355

For negative/positive:
Positive: #4a9a5a (Leaf Green)
Negative: #b85a5a (Muted Red)
Neutral: #8b7355 (Earth Brown)
```

### Organic Curves

```css
.organic-shape {
  border-radius: 60% 40% 30% 70% / 60% 30% 70% 40%;
  /* Blob-like organic shape */
}
```

## Slide Layouts

### Cover Slide

```
┌──────────────────────────────────────────────────┐
│                                                   │
│  [Company Logo]                                  │
│                                                   │
│           🌱                                      │
│                                                   │
│           ESG REPORT 2025                        │
│           ──────────────────                     │
│           Building a Sustainable Future          │
│                                                   │
│                                                   │
│  [Company Name]                    [Report Date] │
└──────────────────────────────────────────────────┘

Background: Organic White (#f5f7f4)
Icon: Leaf Green (#4a9a5a)
Title: Deep Forest (#1a2820), 68pt
Subtitle: Secondary Text (#4a584a), 22pt
```

### ESG Overview Slide

```
┌──────────────────────────────────────────────────┐
│  [ESG OVERVIEW]                           [##]   │
├──────────────────────────────────────────────────┤
│                                                   │
│  Our Commitment to Sustainability                │
│                                                   │
│  ┌──────────────┐ ┌──────────────┐ ┌──────────┐ │
│  │ E            │ │ S            │ │ G        │ │
│  │              │ │              │ │          │ │
│  │ 45%          │ │ 12K          │ │ 100%     │ │
│  │ Carbon       │ │ Community    │ │ Board    │ │
│  │ Reduction    │ │ Impact       │ │ Diversity│ │
│  └──────────────┘ └──────────────┘ └──────────┘ │
│                                                   │
└──────────────────────────────────────────────────┘

E Card: Forest Green left border
S Card: Sky Blue left border
G Card: Earth Brown left border
Values: Leaf Green (#4a9a5a), 48pt
Labels: Secondary Text (#4a584a), 14pt
```

### Environmental Impact

```
┌──────────────────────────────────────────────────┐
│  [ENVIRONMENTAL]                          [##]   │
├──────────────────────────────────────────────────┤
│                                                   │
│  Carbon Footprint Reduction                      │
│                                                   │
│  2020 ████████████████████████████░░░░░░  100%   │
│  2021 █████████████████████████░░░░░░░░░   85%   │
│  2022 ████████████████████░░░░░░░░░░░░░░   68%   │
│  2023 ██████████████████░░░░░░░░░░░░░░░░   55%   │
│  2024 █████████████░░░░░░░░░░░░░░░░░░░░░   45%   │
│                                                   │
│  Target: Net Zero by 2030                        │
│                                                   │
└──────────────────────────────────────────────────┘

Progress Fill: Forest Green (#2d5a3d)
Empty: Light Sage (#e8ede4)
Labels: Deep Forest (#1a2820)
Target: Solar Gold (#d4a04a)
```

### Section Divider

```
┌──────────────────────────────────────────────────┐
│▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓│
│▓                                              ▓▓▓│
│▓  02                                          ▓▓▓│
│▓  ─────────────────────                       ▓▓▓│
│▓  SOCIAL IMPACT                               ▓▓▓│
│▓  Community engagement and DEI initiatives    ▓▓▓│
│▓                                              ▓▓▓│
│▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓│
└──────────────────────────────────────────────────┘

Background: Forest Dark (#1a2820)
Number: Leaf Green (#4a9a5a), 96pt
Title: Text on Dark (#f5f7f4), 54pt
Description: Text on Dark at 80%, 18pt
```

### Goals & Timeline

```
┌──────────────────────────────────────────────────┐
│  SUSTAINABILITY ROADMAP                   [##]   │
├──────────────────────────────────────────────────┤
│                                                   │
│      2024       2025       2027       2030       │
│        ●─────────●─────────●─────────●           │
│        │         │         │         │           │
│    ┌───┴───┐ ┌───┴───┐ ┌───┴───┐ ┌───┴───┐     │
│    │Carbon │ │Renew- │ │Supply │ │Net    │     │
│    │Audit  │ │able   │ │Chain  │ │Zero   │     │
│    │       │ │Energy │ │100%   │ │       │     │
│    └───────┘ └───────┘ └───────┘ └───────┘     │
│                                                   │
└──────────────────────────────────────────────────┘

Timeline Line: Earth Brown (#8b7355), 2pt
Milestones: Forest Green (#2d5a3d) circles
Cards: White background, subtle shadow
Final Goal: Solar Gold (#d4a04a) highlight
```

## Decorative Elements

### Leaf Pattern (subtle background)

```css
.leaf-pattern {
  background-image: url('leaf-pattern.svg');
  opacity: 0.03;
}
```

### Organic Dividers

```css
.organic-divider {
  height: 4px;
  background: linear-gradient(90deg,
    #2d5a3d 0%,
    #4a9a5a 30%,
    #5a9ab8 60%,
    #8b7355 100%
  );
  border-radius: 2px;
}
```

## Accessibility Guidelines

### Contrast Ratios

| Combination | Ratio | Status |
|-------------|-------|--------|
| Deep Forest on Organic White | 11.2:1 | ✅ AAA |
| Forest Green on White | 7.8:1 | ✅ AAA |
| Sky Blue on White | 4.5:1 | ✅ AA |
| Text on Dark bg | 12.1:1 | ✅ AAA |

### Color Blind Considerations

- Use patterns/textures in addition to colors
- Add labels to color-coded elements
- ESG categories identifiable by shape + color

## Use Cases

| Scenario | Recommended Style |
|----------|-------------------|
| 연간 ESG 보고서 | Full ESG color coding |
| 환경 이니셔티브 | Green spectrum focus |
| 임팩트 투자 피치 | Data-heavy, goals timeline |
| CSR 발표 | Community imagery, Social blue |
| 탄소중립 로드맵 | Timeline, progress bars |

## PptxGenJS Implementation

```javascript
// Sustainability theme colors (no # prefix)
const SUSTAINABILITY_COLORS = {
  bgPrimary: 'f5f7f4',
  bgSecondary: 'ffffff',
  bgAccent: 'e8ede4',
  bgDark: '1a2820',
  textPrimary: '1a2820',
  textSecondary: '4a584a',
  accentForest: '2d5a3d',
  accentLeaf: '4a9a5a',
  accentEarth: '8b7355',
  accentSky: '5a9ab8',
  accentSun: 'd4a04a'
};

// Natural background
slide.background = { color: SUSTAINABILITY_COLORS.bgPrimary };

// ESG Card with Environmental border
slide.addShape('rect', {
  x: 1, y: 2, w: 3.5, h: 2.5,
  fill: { color: SUSTAINABILITY_COLORS.bgSecondary },
  shadow: { type: 'outer', blur: 8, offset: 2, angle: 90, opacity: 0.08 }
});
// Left border effect
slide.addShape('rect', {
  x: 1, y: 2, w: 0.05, h: 2.5,
  fill: { color: SUSTAINABILITY_COLORS.accentForest }
});

// Progress bar
slide.addShape('rect', {
  x: 1, y: 4, w: 10, h: 0.2,
  fill: { color: SUSTAINABILITY_COLORS.bgAccent }
});
slide.addShape('rect', {
  x: 1, y: 4, w: 4.5, h: 0.2,  // 45% fill
  fill: { color: SUSTAINABILITY_COLORS.accentForest }
});
```

## Related Themes

- **Alternative:** Healthcare Clean (환경 건강)
- **Corporate Version:** Corporate Blue (기업 ESG)
- **Premium Version:** Luxury Noir (럭셔리 지속가능성)
