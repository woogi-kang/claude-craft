---
name: ppt-design-system
description: |
  전문 프레젠테이션 디자인 시스템. 정밀한 타이포그래피, 10가지 토픽별 테마, 10가지 슬라이드 템플릿 제공.
  "디자인 적용", "템플릿", "스타일 시스템" 요청 시 활성화.
---

# PPT Design System Skill

전문적인 프레젠테이션 디자인을 위한 정밀 시스템입니다.
**"Less is More"** 철학을 기반으로 불필요한 요소를 제거하고 콘텐츠에 집중합니다.

## Topic-Based Themes (10가지)

각 주제에 맞는 전문 테마가 별도 파일로 분리되어 있습니다:

| Theme | File | Use Case |
|-------|------|----------|
| Healthcare Clean | [themes/01-healthcare/](./themes/01-healthcare/THEME.md) | 의료, 바이오, 헬스케어 |
| Education Bright | [themes/02-education/](./themes/02-education/THEME.md) | 교육, 트레이닝, 워크샵 |
| Fintech Bold | [themes/03-fintech/](./themes/03-fintech/THEME.md) | 핀테크, 금융, 크립토 |
| AI Futuristic | [themes/04-ai-tech/](./themes/04-ai-tech/THEME.md) | AI/ML, 테크, 개발자 |
| Sustainability Earth | [themes/05-sustainability/](./themes/05-sustainability/THEME.md) | ESG, 환경, 지속가능성 |
| Startup Gradient | [themes/06-startup/](./themes/06-startup/THEME.md) | 피치덱, 스타트업, VC |
| Luxury Noir | [themes/07-luxury/](./themes/07-luxury/THEME.md) | 럭셔리, 프리미엄, VIP |
| Creative Neon | [themes/08-creative/](./themes/08-creative/THEME.md) | 에이전시, 디자인, 포트폴리오 |
| Real Estate Trust | [themes/09-real-estate/](./themes/09-real-estate/THEME.md) | 부동산, 투자, 자산 |
| F&B Appetite | [themes/10-fnb/](./themes/10-fnb/THEME.md) | 식음료, 레스토랑, 호텔 |

> **Theme Selection:** [themes/INDEX.md](./themes/INDEX.md) - 테마 선택 가이드 및 키워드 매핑

## 슬라이드 규격

### 표준 크기 (포인트 단위)

| 비율 | 너비 | 높이 | 용도 |
|------|------|------|------|
| **16:9** | 720pt | 405pt | 표준 (권장) |
| 16:10 | 720pt | 450pt | 맥북/태블릿 |
| 4:3 | 720pt | 540pt | 레거시 프로젝터 |

### 단위 변환

```
1 inch = 72pt = 96px = 914400 EMU
PT_PER_PX = 0.75
PX_PER_IN = 96
```

---

## 상세 문서

디자인 시스템의 상세 내용은 아래 파일들로 분리되어 있습니다:

| 문서 | 설명 | 내용 |
|------|------|------|
| [typography.md](./typography.md) | 타이포그래피 시스템 | 폰트, 크기 계층, CSS 정의 |
| [palettes.md](./palettes.md) | 컬러 팔레트 | 5가지 팔레트 상세 및 선택 가이드 |
| [layout.md](./layout.md) | 레이아웃 & 템플릿 | 그리드 시스템 + 10가지 슬라이드 템플릿 |
| [components.md](./components.md) | 컴포넌트 라이브러리 | HTML 컴포넌트, 데이터 시각화, CTA |
| [THEMES.md](./THEMES.md) | 테마 선택 가이드 | 발표 유형별 테마 추천 |

---

## 디자인 적용 워크플로우

```
1. 발표 유형 분석
        │
        ▼
2. 팔레트 선택
   ├── Executive Minimal (임원/투자)
   ├── Sage Professional (컨설팅/ESG)
   ├── Modern Dark (테크/스타트업)
   ├── Corporate Blue (기업/금융)
   └── Warm Neutral (마케팅/브랜드)
        │
        ▼
3. 템플릿 매핑
   ├── 표지 → Cover Slide
   ├── 목차 → Contents
   ├── 섹션 시작 → Section Divider
   ├── 일반 내용 → Content Slide
   ├── 핵심 수치 → Statistics
   ├── 비교/사례 → Split Layout
   ├── 팀 소개 → Team Slide
   ├── 인용/강조 → Quote Slide
   ├── 로드맵 → Timeline
   └── 마무리 → Closing Slide
        │
        ▼
4. 타이포그래피 적용
        │
        ▼
5. 접근성 검증
   ├── 대비율 체크 (4.5:1 이상)
   ├── 최소 폰트 크기 (12pt)
   └── 색맹 친화적 팔레트
        │
        ▼
6. Export Skill로 전달
```

## PptxGenJS 변환 규칙

### 색상 코드

```javascript
// HEX에서 '#' 제거 필수
const color = "667eea";  // ✅ 올바름
const color = "#667eea"; // ❌ 오류 발생
```

### 폰트 매핑

```javascript
const FONT_MAP = {
  'Pretendard': 'Pretendard',  // 로컬 설치 필요
  'Inter': 'Arial',            // 폴백
  'Poppins': 'Arial',          // 폴백
};
```

### 그라데이션 처리

```javascript
// CSS 그라데이션은 이미지로 변환 필요
// PptxGenJS는 CSS gradient 미지원

// 방법 1: 단일 색상으로 대체
// 방법 2: 배경 이미지로 렌더링
```

## 주의사항

1. **폰트 임베딩**: Pretendard는 로컬 설치 또는 이미지 변환 필요
2. **그라데이션**: CSS gradient는 이미지로 사전 렌더링
3. **색상 코드**: HEX에서 '#' 제거
4. **단위 변환**: pt ↔ px ↔ inch 정확히 계산
5. **텍스트 태그**: 시맨틱 HTML 사용 (p, h1-h6, ul, li)
6. **이미지 경로**: 절대 경로 사용

## 팔레트 선택 가이드

| 발표 상황 | 추천 팔레트 | 이유 |
|----------|------------|------|
| 투자자 피치 | Executive Minimal | 신뢰감, 집중도 |
| 기술 세미나 | Modern Dark | 몰입감, 트렌디 |
| 기업 보고서 | Corporate Blue | 전문성, 안정감 |
| ESG/지속가능성 | Sage Professional | 자연, 신뢰 |
| 마케팅 제안 | Warm Neutral | 친근함, 감성 |
