# PPT 디자인 시스템 스펙 v3.0

## 기본 규격

### 슬라이드 크기
```
Width:  13.333 inches (960px at 72dpi)
Height: 7.5 inches (540px at 72dpi)
Ratio:  16:9
```

### 단위 변환
```
1 inch = 72 points = 914400 EMU
python-pptx: Inches() 사용
```

## 그리드 시스템

### 여백 (Margin)
```
Top:    0.5 inch
Bottom: 0.5 inch
Left:   0.7 inch
Right:  0.7 inch

Content Width:  13.333 - 1.4 = 11.933 inches
Content Height: 7.5 - 1.0 = 6.5 inches
```

### 수직 영역 분할
```
┌─────────────────────────────────────────────────┐
│  HEADER ZONE      (0.5" - 1.2")    Height: 0.7" │
├─────────────────────────────────────────────────┤
│                                                  │
│  CONTENT ZONE     (1.2" - 6.3")    Height: 5.1" │
│                                                  │
├─────────────────────────────────────────────────┤
│  FOOTER ZONE      (6.3" - 7.0")    Height: 0.7" │
└─────────────────────────────────────────────────┘
```

## 타이포그래피

### 폰트 스택
```
Primary: Arial (시스템 호환성)
Korean: Malgun Gothic / Apple SD Gothic Neo
Mono: Consolas / Courier New
```

### 크기 스케일 (Points)
```
Level 1 - Hero:      44pt (타이틀 슬라이드)
Level 2 - Section:   36pt (섹션 구분)
Level 3 - Title:     28pt (슬라이드 제목)
Level 4 - Subtitle:  20pt (부제목)
Level 5 - Body:      16pt (본문)
Level 6 - Caption:   12pt (캡션/출처)
Level 7 - Label:     10pt (라벨/태그)
```

### Line Height
```
Titles:  1.2 (tight)
Body:    1.5 (comfortable)
Lists:   1.4 (readable)
```

## 컬러 팔레트: Modern Dark

### Primary Colors
```
bg-primary:     #0d1117  (메인 배경)
bg-secondary:   #161b22  (보조 배경)
bg-card:        #21262d  (카드)
bg-accent:      #238636  (강조 배경 - 녹색)
```

### Text Colors
```
text-primary:   #f0f6fc  (주요 텍스트 - 거의 흰색)
text-secondary: #8b949e  (보조 텍스트 - 회색)
text-muted:     #6e7681  (약한 텍스트)
```

### Accent Colors
```
accent-blue:    #58a6ff  (링크, 강조)
accent-green:   #3fb950  (성공, 포인트)
accent-purple:  #a371f7  (보조 강조)
accent-yellow:  #d29922  (경고)
accent-red:     #f85149  (에러)
```

## 슬라이드 템플릿 레이아웃

### 1. Cover Slide (표지)
```
┌──────────────────────────────────────────────────────────┐
│                                                           │
│                                                           │
│                                                           │
│              [HERO TITLE - 44pt, Bold, Center]            │
│              ─────────────────────────────────            │
│              [Subtitle - 20pt, Center]                    │
│                                                           │
│                                                           │
│                                                           │
│  [Presenter - 12pt]                        [Date - 12pt]  │
└──────────────────────────────────────────────────────────┘

Positions (inches):
- Title: x=0.7, y=2.8, w=11.933, h=1.0
- Subtitle: x=0.7, y=4.0, w=11.933, h=0.5
- Presenter: x=0.7, y=6.5, w=4.0, h=0.4
- Date: x=8.633, y=6.5, w=4.0, h=0.4 (right-aligned)
```

### 2. Section Divider (섹션 구분)
```
┌──────────────────────────────────────────────────────────┐
│                                                           │
│                                                           │
│    [Number - 72pt]                                        │
│                                                           │
│    [Section Title - 36pt, Bold]                           │
│    [Description - 16pt]                                   │
│                                                           │
│                                                           │
│                                                           │
└──────────────────────────────────────────────────────────┘

Positions (inches):
- Number: x=0.7, y=2.2, w=2.0, h=1.0
- Title: x=0.7, y=3.4, w=11.933, h=0.8
- Description: x=0.7, y=4.4, w=11.933, h=0.5
- Background: 전체 accent-blue (#58a6ff)
```

### 3. Content Slide (기본)
```
┌──────────────────────────────────────────────────────────┐
│  [Badge]                                         [##/25]  │
├──────────────────────────────────────────────────────────┤
│                                                           │
│  [Headline - 28pt, Bold]                                  │
│                                                           │
│  • Bullet point 1                                         │
│  • Bullet point 2                                         │
│  • Bullet point 3                                         │
│  • Bullet point 4                                         │
│                                                           │
│                                                           │
├──────────────────────────────────────────────────────────┤
│  [Source/Footer]                                          │
└──────────────────────────────────────────────────────────┘

Positions (inches):
- Badge: x=0.7, y=0.5, w=1.5, h=0.35
- Page: x=11.5, y=0.5, w=1.1, h=0.35
- Headline: x=0.7, y=1.2, w=11.933, h=0.6
- Bullets: x=0.7, y=2.0, w=11.933, h=4.0
- Footer: x=0.7, y=6.5, w=11.933, h=0.35
```

### 4. Two Column (2단)
```
┌──────────────────────────────────────────────────────────┐
│  [Badge]                                         [##/25]  │
├──────────────────────────────────────────────────────────┤
│                                                           │
│  [Headline - 28pt, Bold]                                  │
│                                                           │
│  ┌─────────────────────┐  ┌─────────────────────────────┐ │
│  │                     │  │                             │ │
│  │   • Point 1         │  │    [Visual / Diagram]       │ │
│  │   • Point 2         │  │                             │ │
│  │   • Point 3         │  │                             │ │
│  │                     │  │                             │ │
│  └─────────────────────┘  └─────────────────────────────┘ │
│                                                           │
└──────────────────────────────────────────────────────────┘

Positions (inches):
- Left Column: x=0.7, y=2.0, w=5.2, h=4.0
- Right Column: x=6.2, y=2.0, w=6.433, h=4.0
- Gap between columns: 0.3 inch
```

### 5. Statistics (통계)
```
┌──────────────────────────────────────────────────────────┐
│  [Badge]                                         [##/25]  │
├──────────────────────────────────────────────────────────┤
│                                                           │
│  [Headline - 28pt, Bold]                                  │
│                                                           │
│  ┌──────────┐     ┌──────────┐     ┌──────────┐          │
│  │          │     │          │     │          │          │
│  │   85%    │     │   2.5x   │     │  $1.2M   │          │
│  │ ──────── │     │ ──────── │     │ ──────── │          │
│  │  Label   │     │  Label   │     │  Label   │          │
│  │          │     │          │     │          │          │
│  └──────────┘     └──────────┘     └──────────┘          │
│                                                           │
└──────────────────────────────────────────────────────────┘

Card Layout (3 cards):
- Card Width: 3.4 inches
- Card Height: 2.8 inches
- Gap: 0.5 inch
- Total: 3.4*3 + 0.5*2 = 11.2 inches
- Start X: (13.333 - 11.2) / 2 = 1.07 inches

Card Positions:
- Card 1: x=1.07, y=2.2
- Card 2: x=4.97, y=2.2
- Card 3: x=8.87, y=2.2

Inside Card:
- Value: y=card_y+0.5, h=1.2, font=36pt, accent-green
- Label: y=card_y+2.0, h=0.5, font=14pt, text-secondary
```

### 6. Comparison (비교)
```
┌──────────────────────────────────────────────────────────┐
│  [Badge]                                         [##/25]  │
├──────────────────────────────────────────────────────────┤
│                                                           │
│  [Headline - 28pt, Bold]                                  │
│                                                           │
│  ┌─────────────────────────┐ ┌─────────────────────────┐  │
│  │ ▓▓▓▓ BEFORE ▓▓▓▓▓▓▓▓▓▓ │ │ ████ AFTER █████████████│  │
│  │                         │ │                         │  │
│  │ • Item 1                │ │ • Item 1                │  │
│  │ • Item 2                │ │ • Item 2                │  │
│  │ • Item 3                │ │ • Item 3                │  │
│  │                         │ │                         │  │
│  └─────────────────────────┘ └─────────────────────────┘  │
│                                                           │
└──────────────────────────────────────────────────────────┘

Positions (inches):
- Left Box: x=0.7, y=2.0, w=5.766, h=4.0
- Right Box: x=6.766, y=2.0, w=5.766, h=4.0
- Gap: 0.3 inch
- Header Height: 0.45 inch (BEFORE/AFTER labels)
```

### 7. Code Block
```
┌──────────────────────────────────────────────────────────┐
│  [Badge]                                         [##/25]  │
├──────────────────────────────────────────────────────────┤
│                                                           │
│  [Headline - 28pt, Bold]                                  │
│                                                           │
│  ┌────────────────────────────────────────────────────┐   │
│  │ ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░ │   │
│  │ ░ code line 1                                   ░ │   │
│  │ ░ code line 2                                   ░ │   │
│  │ ░ code line 3                                   ░ │   │
│  │ ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░ │   │
│  └────────────────────────────────────────────────────┘   │
│                                                           │
└──────────────────────────────────────────────────────────┘

Code Block:
- Box: x=0.7, y=2.0, w=11.933, h=3.5
- Background: bg-card (#21262d)
- Padding: 0.3 inch all sides
- Font: Consolas/Courier New, 14pt
- Text Color: accent-green (#3fb950)
```

### 8. Quote
```
┌──────────────────────────────────────────────────────────┐
│                                                           │
│                                                           │
│            ❝                                              │
│            [Quote Text - 24pt, Italic]                    │
│            ❞                                              │
│                                                           │
│                        — [Author]                         │
│                          [Title]                          │
│                                                           │
│                                                           │
└──────────────────────────────────────────────────────────┘

Positions (inches):
- Quote Mark Open: x=1.5, y=2.0
- Quote Text: x=2.0, y=2.5, w=9.333, h=2.0, center-aligned
- Attribution: x=2.0, y=5.0, w=9.333, h=0.8, center-aligned
- Background: bg-secondary (#161b22)
```

### 9. Closing
```
┌──────────────────────────────────────────────────────────┐
│                                                           │
│                                                           │
│                                                           │
│              [Thank You - 44pt, Bold, Center]             │
│                                                           │
│              [Subtitle - 20pt, Center]                    │
│                                                           │
│              [Contact - 14pt, Center]                     │
│                                                           │
│                                                           │
└──────────────────────────────────────────────────────────┘

Positions (inches):
- Title: x=0.7, y=2.5, w=11.933, h=1.0
- Subtitle: x=0.7, y=3.8, w=11.933, h=0.5
- Contact: x=0.7, y=5.0, w=11.933, h=0.5
- Background: accent-blue (#58a6ff)
```

## 컴포넌트 상세

### Badge (섹션 표시)
```
Size: w=1.5", h=0.35"
Background: accent-blue (#58a6ff)
Text: 10pt, Bold, White, Center
Border Radius: 4pt (if possible)
Position: x=0.7, y=0.5
```

### Page Number
```
Size: w=1.1", h=0.35"
Text: "##/25" format, 12pt, text-secondary
Alignment: Right
Position: x=11.533, y=0.5
```

### Bullet Points
```
Marker: "•" (bullet) or "1." (numbered)
Indent: 0.3 inch from left
Space After: 0.25 inch (18pt)
Font: 16pt, text-primary
```

### Cards (통계용)
```
Size: w=3.4", h=2.8"
Background: bg-card (#21262d)
Border: None
Padding: 0.3" all sides
```

## 정렬 규칙

### 수평 정렬
```
Left:   x = 0.7"
Center: x = (13.333 - element_width) / 2
Right:  x = 13.333 - 0.7 - element_width
```

### 수직 정렬
```
Top:    Content Zone 시작 (y = 1.2")
Middle: y = (7.5 - element_height) / 2
Bottom: y = 7.5 - 0.5 - element_height
```

## 검증 체크리스트

```
□ 모든 요소가 Content Zone 내에 위치
□ 텍스트가 잘리지 않음
□ 적절한 여백 유지 (최소 0.3")
□ 폰트 크기 일관성
□ 색상 대비 충분 (4.5:1 이상)
□ 정렬 일관성 (좌측정렬 기본)
```
