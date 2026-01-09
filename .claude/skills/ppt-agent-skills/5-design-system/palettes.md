# Color Palettes

PPT Design System의 5가지 컬러 팔레트입니다.

## 1. Executive Minimal (이그제큐티브 미니멀)

**용도:** 임원 보고, 투자자 피치, 프리미엄 발표

```css
:root {
  --bg-primary: #f5f5f0;      /* Warm White */
  --bg-secondary: #ffffff;
  --text-primary: #1a1a1a;     /* Almost Black */
  --text-secondary: #666666;
  --accent: #2d2d2d;
  --border: #e0e0e0;
}
```

| 역할 | HEX | 용도 |
|------|-----|------|
| Background | #f5f5f0 | 메인 배경 |
| Card | #ffffff | 카드, 섹션 |
| Text Primary | #1a1a1a | 제목, 강조 |
| Text Secondary | #666666 | 본문 |
| Accent | #2d2d2d | 버튼, 강조 |
| Border | #e0e0e0 | 구분선 |

## 2. Sage Professional (세이지 프로페셔널)

**용도:** 컨설팅, 헬스케어, 환경/ESG

```css
:root {
  --bg-primary: #f8faf8;
  --bg-secondary: #ffffff;
  --text-primary: #1a1a1a;
  --text-secondary: #4a5548;
  --accent: #b8c4b8;           /* Sage Green */
  --accent-dark: #7a8a78;
  --border: #dce3dc;
}
```

| 역할 | HEX | 용도 |
|------|-----|------|
| Background | #f8faf8 | 메인 배경 |
| Accent | #b8c4b8 | 강조, 아이콘 |
| Accent Dark | #7a8a78 | 호버, CTA |
| Text | #4a5548 | 본문 텍스트 |

## 3. Modern Dark (모던 다크)

**용도:** 테크 세미나, 스타트업, 개발자 발표

```css
:root {
  --bg-primary: #0f0f0f;       /* Pure Dark */
  --bg-secondary: #1a1a1a;
  --bg-card: #252525;
  --text-primary: #ffffff;
  --text-secondary: #a0a0a0;
  --accent: #667eea;           /* Primary Blue */
  --accent-secondary: #764ba2;  /* Purple */
  --gradient: linear-gradient(135deg, #667eea, #764ba2);
}
```

| 역할 | HEX | 용도 |
|------|-----|------|
| Background | #0f0f0f | 메인 배경 |
| Card | #252525 | 카드, 코드블록 |
| Text Primary | #ffffff | 제목 |
| Text Secondary | #a0a0a0 | 본문 |
| Accent | #667eea | 링크, 강조 |
| Gradient | #667eea→#764ba2 | 배경, CTA |

## 4. Corporate Blue (코퍼레이트 블루)

**용도:** 기업 발표, 금융, 공공기관

```css
:root {
  --bg-primary: #ffffff;
  --bg-secondary: #f0f4f8;
  --text-primary: #0d1b2a;     /* Navy */
  --text-secondary: #415a77;
  --accent: #1b4965;           /* Corporate Blue */
  --accent-light: #5fa8d3;
  --border: #cad2d8;
}
```

| 역할 | HEX | 용도 |
|------|-----|------|
| Background | #ffffff | 메인 배경 |
| Secondary BG | #f0f4f8 | 섹션 구분 |
| Navy | #0d1b2a | 제목 |
| Corporate Blue | #1b4965 | 강조 |
| Light Blue | #5fa8d3 | 차트, 아이콘 |

## 5. Warm Neutral (웜 뉴트럴)

**용도:** 마케팅, 라이프스타일, 브랜드 발표

```css
:root {
  --bg-primary: #faf8f5;       /* Cream */
  --bg-secondary: #ffffff;
  --text-primary: #2d2a26;
  --text-secondary: #6b635a;
  --accent: #c45a3b;           /* Terracotta */
  --accent-light: #e8a090;
  --border: #e5e0d8;
}
```

| 역할 | HEX | 용도 |
|------|-----|------|
| Background | #faf8f5 | 메인 배경 |
| Text Primary | #2d2a26 | 제목 |
| Terracotta | #c45a3b | CTA, 강조 |
| Accent Light | #e8a090 | 하이라이트 |

## 팔레트 선택 가이드

| 발표 상황 | 추천 팔레트 | 이유 |
|----------|------------|------|
| 투자자 피치 | Executive Minimal | 신뢰감, 집중도 |
| 기술 세미나 | Modern Dark | 몰입감, 트렌디 |
| 기업 보고서 | Corporate Blue | 전문성, 안정감 |
| ESG/지속가능성 | Sage Professional | 자연, 신뢰 |
| 마케팅 제안 | Warm Neutral | 친근함, 감성 |
