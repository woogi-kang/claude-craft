# Placeholder 사용 가이드

## 개요

HTML 슬라이드에서 `class="placeholder"` 를 가진 요소는 이미지/차트가 들어갈 영역을 나타냅니다.
html2pptx.js가 이 영역의 위치와 크기를 추출하여 별도로 반환합니다.

## 사용법

### HTML에서 Placeholder 정의

```html
<!-- 기본 placeholder -->
<div id="hero-image" class="placeholder"
     style="position: absolute; left: 550px; top: 150px; width: 360px; height: 250px;
            background: #e5e5e0; border-radius: 12px;">
</div>

<!-- 원형 placeholder -->
<div id="section-image" class="placeholder"
     style="position: absolute; left: 700px; top: 220px; width: 200px; height: 200px;
            background: #333333; border-radius: 100px;">
</div>
```

### 필수 속성
- `id`: 고유 식별자 (예: "hero-image", "chart-area")
- `class="placeholder"`: placeholder로 인식되기 위한 필수 클래스
- `position: absolute`: 정확한 위치 지정
- `left`, `top`, `width`, `height`: 픽셀 단위 크기

### 빌드 결과

html2pptx()가 반환하는 placeholders 배열:

```javascript
const { slide, placeholders } = await html2pptx('slide.html', pptx);

// placeholders 예시:
[
  { id: "hero-image", x: 5.73, y: 1.56, w: 3.75, h: 2.60 },
  { id: "section-image", x: 7.29, y: 2.29, w: 2.08, h: 2.08 }
]
// 모든 값은 inches 단위
```

### 이미지 추가 방법

```javascript
// placeholder 위치에 이미지 추가
const placeholder = placeholders.find(p => p.id === 'hero-image');
slide.addImage({
  path: './images/hero.png',
  x: placeholder.x,
  y: placeholder.y,
  w: placeholder.w,
  h: placeholder.h
});
```

---

## 이미지 생성 프롬프트

### 1. Hero Image (표지 슬라이드)

**용도**: Claude Code 2.0 표지의 메인 비주얼

**크기**: 360x250px (3.75" x 2.60")

**프롬프트**:
```
Create a minimalist tech illustration for a presentation about "Claude Code" - an AI coding assistant.

Style:
- Clean, modern, flat design
- Executive minimal aesthetic
- Color palette: #1a1a1a (black), #f5f5f0 (cream), #666666 (gray)
- No gradients, solid colors only

Content:
- Abstract representation of a terminal/CLI interface
- Geometric shapes suggesting code structure
- Subtle AI/neural network pattern in background
- No text or logos

Dimensions: 360x250 pixels
Background: Transparent or #e5e5e0
```

### 2. Section Divider Image (섹션 구분)

**용도**: 섹션 전환 슬라이드의 장식 요소

**크기**: 200x200px (원형)

**프롬프트**:
```
Create a circular minimalist icon for a presentation section divider.

Style:
- Geometric, abstract
- Monochromatic: white (#ffffff) on dark background or vice versa
- Clean lines, no gradients

Content for "Advanced Features" section:
- Interconnected nodes/dots suggesting automation
- Gear or settings iconography
- Abstract representation of parallel processing

Dimensions: 200x200 pixels (circular)
Background: Transparent
```

### 3. Feature Illustration (기능 설명)

**용도**: Extended Thinking, MCP 등 기능 설명 슬라이드

**크기**: 300x200px

**프롬프트**:
```
Create a simple diagram/illustration for [FEATURE_NAME].

Style:
- Flat, isometric optional
- 2-3 colors max from palette: #1a1a1a, #f5f5f0, #888888, #4ade80
- Clean lines, no shadows

Content suggestions:
- Extended Thinking: Brain with thought bubbles/arrows
- MCP: Connecting lines between boxes (tools/databases)
- Background Agents: Multiple parallel process lanes

Dimensions: 300x200 pixels
Background: Transparent or #f5f5f0
```

---

## 현재 슬라이드의 Placeholder 목록

| Slide | ID | 크기 (px) | 용도 | 권장 이미지 |
|-------|-----|-----------|------|-------------|
| 1 | hero-image | 360x250 | 표지 메인 비주얼 | Terminal/Code illustration |
| 9 | section-image | 200x200 | 섹션 장식 | Abstract circular icon |

---

## 추가 Placeholder 예시

필요시 슬라이드에 추가할 수 있는 placeholder 패턴:

```html
<!-- 차트 영역 -->
<div id="chart-area" class="placeholder"
     style="position: absolute; left: 506px; top: 150px; width: 390px; height: 280px;
            background: #f5f5f0; border-radius: 12px;">
</div>

<!-- 스크린샷 영역 -->
<div id="screenshot" class="placeholder"
     style="position: absolute; left: 64px; top: 200px; width: 400px; height: 250px;
            background: #e5e5e0; border-radius: 8px;">
</div>

<!-- 아이콘 영역 -->
<div id="feature-icon" class="placeholder"
     style="position: absolute; left: 64px; top: 100px; width: 80px; height: 80px;
            background: #1a1a1a; border-radius: 12px;">
</div>
```

---

## 이미지 최적화 권장사항

1. **포맷**: PNG (투명 배경 필요시) 또는 JPG
2. **해상도**: Placeholder 크기의 2배 (Retina 대응)
3. **파일 크기**: 500KB 이하 권장
4. **압축**: 품질 85% 이상 유지
