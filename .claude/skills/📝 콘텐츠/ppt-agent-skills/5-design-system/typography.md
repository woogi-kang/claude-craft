# Typography System

PPT Design System의 타이포그래피 시스템입니다.

## 기본 폰트

**Primary:** Pretendard (한글) / Inter (영문)

```html
<link rel="stylesheet" href="https://cdn.jsdelivr.net/gh/orioncactus/pretendard/dist/web/static/pretendard.css">
```

## 폰트 크기 계층

| 레벨 | 크기 | 굵기 | 자간 | 행간 | 용도 |
|------|------|------|------|------|------|
| **Hero** | 72-96pt | 700 | -0.02em | 1.1 | 타이틀 슬라이드 |
| **Section Title** | 48-60pt | 700 | -0.02em | 1.2 | 섹션 구분 |
| **Slide Title** | 32-40pt | 600 | -0.01em | 1.3 | 슬라이드 제목 |
| **Subtitle** | 20-24pt | 500 | 0 | 1.4 | 부제목 |
| **Body** | 16-20pt | 400 | 0 | 1.6 | 본문 |
| **Caption** | 12-14pt | 400 | 0.02em | 1.5 | 캡션/출처 |
| **Label** | 10-12pt | 500 | 0.05em | 1.4 | 라벨/태그 |

## 타이포그래피 CSS

```css
:root {
  /* Font Sizes */
  --font-hero: 84pt;
  --font-section: 54pt;
  --font-title: 36pt;
  --font-subtitle: 22pt;
  --font-body: 18pt;
  --font-caption: 13pt;
  --font-label: 11pt;

  /* Font Weights */
  --weight-bold: 700;
  --weight-semibold: 600;
  --weight-medium: 500;
  --weight-regular: 400;

  /* Line Heights */
  --lh-tight: 1.1;
  --lh-heading: 1.3;
  --lh-body: 1.6;
}

/* Title Style */
.slide-title {
  font-size: var(--font-title);
  font-weight: var(--weight-semibold);
  letter-spacing: -0.01em;
  line-height: var(--lh-heading);
}

/* Body Style */
.slide-body {
  font-size: var(--font-body);
  font-weight: var(--weight-regular);
  line-height: var(--lh-body);
}
```
