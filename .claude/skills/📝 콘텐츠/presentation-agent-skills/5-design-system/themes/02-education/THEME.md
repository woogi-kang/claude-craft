---
name: theme-education
description: |
  Education Bright 테마. 교육기관, E-러닝, EdTech, 워크샵, 트레이닝 발표에 최적화.
  "교육", "학교", "대학", "트레이닝", "워크샵", "e-러닝" 키워드로 활성화.
tags: [education, school, university, training, workshop, e-learning, edtech]
---

# Education Bright Theme

활기차고 접근하기 쉬운 교육 전문 디자인 테마입니다.

## Design Philosophy

- **활기차고 접근하기 쉬운** 느낌
- **집중력**을 높이는 틸 + **주의**를 끄는 오렌지 액센트
- **정보 계층**이 명확한 구조
- **친근하면서도 신뢰감** 있는 톤

## Color Palette

### CSS Variables

```css
:root {
  /* Primary */
  --bg-primary: #fafcfc;
  --bg-secondary: #ffffff;
  --bg-accent: #e8f6f4;         /* Soft Teal Tint */

  /* Text */
  --text-primary: #1a2e35;
  --text-secondary: #4a5e65;
  --text-muted: #7a8e95;

  /* Accent Colors */
  --accent-primary: #00a89d;    /* Learning Teal */
  --accent-secondary: #ff7f50;  /* Engagement Orange */
  --accent-tertiary: #6366f1;   /* Interactive Indigo */
  --accent-success: #10b981;    /* Achievement Green */

  /* Borders */
  --border-light: #e0eaec;
}
```

### Color Reference Table

| Role | HEX | PptxGenJS | Usage |
|------|-----|-----------|-------|
| Background | #fafcfc | `fafcfc` | 메인 배경 |
| Card | #ffffff | `ffffff` | 콘텐츠 카드 |
| Accent BG | #e8f6f4 | `e8f6f4` | 강조 섹션 |
| Primary Text | #1a2e35 | `1a2e35` | 제목, 헤드라인 |
| Secondary Text | #4a5e65 | `4a5e65` | 본문 |
| Learning Teal | #00a89d | `00a89d` | 주요 강조, 제목 |
| Engagement Orange | #ff7f50 | `ff7f50` | CTA, 중요 포인트 |
| Interactive Indigo | #6366f1 | `6366f1` | 링크, 인터랙션 |
| Achievement Green | #10b981 | `10b981` | 완료, 성공 표시 |

## Typography

### Font Stack

```css
--font-family: 'Pretendard', 'Nunito Sans', sans-serif;
```

### Size Hierarchy (Points)

| Level | Size | Weight | Usage |
|-------|------|--------|-------|
| Hero | 76pt | 700 | 타이틀 슬라이드 |
| Title | 38pt | 600 | 슬라이드 제목 |
| Subtitle | 24pt | 500 | 부제목 |
| Body | 20pt | 400 | 본문 (가독성 높임) |
| Caption | 14pt | 400 | 캡션, 출처 |
| Label | 12pt | 500 | 라벨, 태그 |

### Typography Note

- **Body 크기 증가**: 가독성을 위해 20pt 사용
- **Line height**: 1.7 (읽기 편한 간격)

## Design Elements

### Progress Bars

```css
.progress-bar {
  height: 8px;
  border-radius: 4px;
  background: linear-gradient(90deg, #00a89d 0%, #ff7f50 100%);
}
```

틸 → 오렌지 그라데이션으로 진행 상태 표시

### Step Indicators

```css
.step-indicator {
  width: 48pt;
  height: 48pt;
  border-radius: 50%;
  background: #00a89d;
  color: #ffffff;
  font-size: 24pt;
  font-weight: 700;
  display: flex;
  align-items: center;
  justify-content: center;
}
```

### Callout Boxes

```css
.callout {
  background: #e8f6f4;
  border-left: 4px solid #00a89d;
  padding: 16pt 20pt;
  border-radius: 0 8px 8px 0;
}

.callout-important {
  background: #fff5f0;
  border-left: 4px solid #ff7f50;
}
```

### Quiz/Interactive Elements

```css
.interactive-element {
  border: 2px solid #6366f1;
  background: rgba(99, 102, 241, 0.05);
  border-radius: 8px;
  padding: 16pt;
}

.interactive-element:hover {
  background: rgba(99, 102, 241, 0.1);
}
```

### Achievement Badges

```css
.achievement {
  background: #10b981;
  color: #ffffff;
  padding: 8pt 16pt;
  border-radius: 20pt;
  font-size: 12pt;
  font-weight: 600;
}
```

## Slide Layouts

### Cover Slide

```
┌──────────────────────────────────────────────────┐
│  [Institution Logo]                              │
│                                                   │
│                                                   │
│           [Course/Workshop Title]                │
│           ─────────────────────                  │
│           [Subtitle / Module Name]               │
│                                                   │
│                                                   │
│  [Instructor Name]               [Date/Duration] │
└──────────────────────────────────────────────────┘

Background: Soft Teal (#e8f6f4)
Title: Primary Text (#1a2e35), 76pt
Subtitle: Learning Teal (#00a89d), 24pt
```

### Learning Objectives Slide

```
┌──────────────────────────────────────────────────┐
│  [LEARNING]                               [##]   │
├──────────────────────────────────────────────────┤
│                                                   │
│  What You'll Learn Today                         │
│                                                   │
│  ┌─────┐  Understand core concepts              │
│  │  1  │  of responsive design                  │
│  └─────┘                                         │
│                                                   │
│  ┌─────┐  Apply best practices                  │
│  │  2  │  in real-world projects               │
│  └─────┘                                         │
│                                                   │
│  ┌─────┐  Build confidence through              │
│  │  3  │  hands-on exercises                   │
│  └─────┘                                         │
│                                                   │
└──────────────────────────────────────────────────┘

Step Number: Teal circle with white number
Title: Primary Text (#1a2e35), 38pt
Content: Secondary Text (#4a5e65), 20pt
```

### Progress Tracker

```
┌──────────────────────────────────────────────────┐
│  YOUR PROGRESS                            [##]   │
├──────────────────────────────────────────────────┤
│                                                   │
│      Module 1    Module 2    Module 3    Module 4│
│         ●───────────●───────────◐───────────○    │
│       Done       Done      Current    Upcoming   │
│                                                   │
│  ┌────────────────────────────────────────────┐  │
│  │ ████████████████████████░░░░░░░░░░░░░░░░░░│  │
│  │                    65% Complete            │  │
│  └────────────────────────────────────────────┘  │
│                                                   │
└──────────────────────────────────────────────────┘

Progress Fill: Teal → Orange gradient
Completed: Achievement Green (#10b981)
Current: Learning Teal (#00a89d)
Upcoming: Muted (#7a8e95)
```

### Section Divider

```
┌──────────────────────────────────────────────────┐
│░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░│
│░░                                            ░░░░│
│░░  SECTION 02                                ░░░░│
│░░  ────────────────────────────              ░░░░│
│░░  Hands-On Practice                         ░░░░│
│░░                                            ░░░░│
│░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░│
└──────────────────────────────────────────────────┘

Background: Learning Teal (#00a89d)
Section Label: White, 14pt
Title: White, 54pt
```

## Interactive Elements

### Quiz Option Cards

```
┌────────────────────────────┐
│  A                         │
│                            │
│  Option text here          │
│                            │
└────────────────────────────┘

Default: White bg, Indigo border
Selected: Indigo bg (10% opacity)
Correct: Green border + checkmark
```

### Tip Boxes

```css
.tip-box {
  background: #fff5f0;
  border: 1px solid #ff7f50;
  border-radius: 8px;
  padding: 16pt;
}

.tip-icon {
  color: #ff7f50;
  font-size: 20pt;
}
```

## Accessibility Guidelines

### Contrast Ratios

| Combination | Ratio | Status |
|-------------|-------|--------|
| Primary Text on White | 13.1:1 | ✅ AAA |
| Teal on White | 4.8:1 | ✅ AA |
| Orange on White | 3.1:1 | ⚠️ Large text only |
| White on Teal | 4.8:1 | ✅ AA |

### Minimum Font Sizes

- Body text: 20pt (accessibility enhanced)
- Captions: 14pt minimum
- Interactive elements: 16pt minimum

## Use Cases

| Scenario | Recommended Style |
|----------|-------------------|
| University 강의 | Teal 강조, 단계별 구성 |
| Corporate 트레이닝 | Progress bars, Achievement badges |
| E-러닝 모듈 | Interactive elements, Quiz cards |
| Workshop | Step indicators, Callout boxes |
| 학생 발표 | 활기찬 컬러, 큰 텍스트 |

## PptxGenJS Implementation

```javascript
// Education theme colors (no # prefix)
const EDUCATION_COLORS = {
  bgPrimary: 'fafcfc',
  bgSecondary: 'ffffff',
  bgAccent: 'e8f6f4',
  textPrimary: '1a2e35',
  textSecondary: '4a5e65',
  accentPrimary: '00a89d',
  accentSecondary: 'ff7f50',
  accentTertiary: '6366f1',
  accentSuccess: '10b981',
  border: 'e0eaec'
};

// Step indicator
slide.addShape('ellipse', {
  x: 0.7, y: 2, w: 0.5, h: 0.5,
  fill: { color: EDUCATION_COLORS.accentPrimary }
});
slide.addText('1', {
  x: 0.7, y: 2, w: 0.5, h: 0.5,
  fontSize: 24,
  color: 'ffffff',
  bold: true,
  align: 'center',
  valign: 'middle'
});

// Callout box
slide.addShape('rect', {
  x: 1.3, y: 2, w: 10, h: 0.8,
  fill: { color: EDUCATION_COLORS.bgAccent }
});
```

## Related Themes

- **Alternative:** Healthcare Clean (의료 교육)
- **Corporate Version:** Corporate Blue (기업 트레이닝)
- **Fun Version:** Creative Neon (크리에이티브 워크샵)
