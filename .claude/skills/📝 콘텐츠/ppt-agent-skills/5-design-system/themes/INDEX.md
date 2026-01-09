---
name: theme-index
description: |
  10가지 토픽별 전문 디자인 테마 인덱스. 주제에 맞는 테마를 자동 선택.
---

# Theme Index

프레젠테이션 주제에 따라 최적의 디자인 테마를 자동으로 선택합니다.

## Quick Reference

| # | Theme | File | Keywords |
|---|-------|------|----------|
| 01 | Healthcare Clean | [01-healthcare/THEME.md](./01-healthcare/THEME.md) | 의료, 헬스케어, 병원, 바이오, 제약 |
| 02 | Education Bright | [02-education/THEME.md](./02-education/THEME.md) | 교육, 학교, 대학, 트레이닝, 워크샵 |
| 03 | Fintech Bold | [03-fintech/THEME.md](./03-fintech/THEME.md) | 핀테크, 금융, 페이먼트, 크립토, 뱅킹 |
| 04 | AI Futuristic | [04-ai-tech/THEME.md](./04-ai-tech/THEME.md) | AI, ML, 머신러닝, 클라우드, 개발자 |
| 05 | Sustainability Earth | [05-sustainability/THEME.md](./05-sustainability/THEME.md) | ESG, 환경, 지속가능성, 탄소, 친환경 |
| 06 | Startup Gradient | [06-startup/THEME.md](./06-startup/THEME.md) | 스타트업, 피치, 투자, 펀딩, VC |
| 07 | Luxury Noir | [07-luxury/THEME.md](./07-luxury/THEME.md) | 럭셔리, 프리미엄, 하이엔드, VIP, 명품 |
| 08 | Creative Neon | [08-creative/THEME.md](./08-creative/THEME.md) | 크리에이티브, 에이전시, 디자인, 포트폴리오 |
| 09 | Real Estate Trust | [09-real-estate/THEME.md](./09-real-estate/THEME.md) | 부동산, 투자, 자산, 건설, 개발 |
| 10 | F&B Appetite | [10-fnb/THEME.md](./10-fnb/THEME.md) | 식음료, 레스토랑, 카페, 호텔, 라이프스타일 |

## Theme Selection Logic

### By Industry Keywords

```javascript
const THEME_KEYWORDS = {
  '01-healthcare': ['의료', '헬스케어', '병원', '바이오', '제약', 'medical', 'healthcare', 'hospital', 'bio', 'pharma'],
  '02-education': ['교육', '학교', '대학', '트레이닝', '워크샵', 'education', 'school', 'university', 'training', 'workshop'],
  '03-fintech': ['핀테크', '금융', '페이먼트', '크립토', '뱅킹', 'fintech', 'finance', 'payment', 'crypto', 'banking'],
  '04-ai-tech': ['AI', 'ML', '머신러닝', '딥러닝', '클라우드', '개발자', 'tech', 'developer', 'cloud'],
  '05-sustainability': ['ESG', '환경', '지속가능성', '탄소', '친환경', 'sustainability', 'green', 'carbon', 'climate'],
  '06-startup': ['스타트업', '피치', '투자', '펀딩', 'VC', 'startup', 'pitch', 'funding', 'investor'],
  '07-luxury': ['럭셔리', '프리미엄', '하이엔드', 'VIP', '명품', 'luxury', 'premium', 'high-end', 'exclusive'],
  '08-creative': ['크리에이티브', '에이전시', '디자인', '포트폴리오', 'creative', 'agency', 'design', 'portfolio'],
  '09-real-estate': ['부동산', '투자', '자산', '건설', '개발', 'real estate', 'property', 'investment', 'construction'],
  '10-fnb': ['식음료', '레스토랑', '카페', '호텔', '라이프스타일', 'food', 'beverage', 'restaurant', 'cafe', 'hotel']
};
```

### By Audience

| Audience | Primary Theme | Alternative |
|----------|---------------|-------------|
| 투자자/VC | Startup Gradient | Fintech Bold |
| 기업 임원 | Real Estate Trust | Healthcare Clean |
| 개발자/엔지니어 | AI Futuristic | Fintech Bold |
| 일반 소비자 | Education Bright | F&B Appetite |
| 하이엔드 고객 | Luxury Noir | Real Estate Trust |
| 크리에이터 | Creative Neon | Startup Gradient |

### By Mood

| Mood | Primary Theme | Alternative |
|------|---------------|-------------|
| 신뢰/안정 | Healthcare Clean | Real Estate Trust |
| 혁신/미래 | AI Futuristic | Fintech Bold |
| 성장/에너지 | Startup Gradient | Education Bright |
| 우아/프리미엄 | Luxury Noir | F&B Appetite |
| 친환경/자연 | Sustainability Earth | Healthcare Clean |
| 대담/창의 | Creative Neon | Startup Gradient |

## Color Mode Summary

| Theme | Mode | Primary BG | Accent |
|-------|------|------------|--------|
| Healthcare | Light | #f8fafb | Blue/Sage |
| Education | Light | #fafcfc | Teal/Orange |
| Fintech | Dark | #0c0c14 | Purple/Neon |
| AI Tech | Dark | #0a0a0f | Blue/Cyan |
| Sustainability | Light | #f5f7f4 | Green/Earth |
| Startup | Mixed | #fafafa / #18181b | Gradient |
| Luxury | Dark | #0a0a0a | Gold |
| Creative | Dark | #0f0f0f | Multi-Neon |
| Real Estate | Light | #ffffff | Navy/Gold |
| F&B | Light | #faf6f0 | Terracotta/Mustard |

## Usage in PPT Generation

```javascript
// 1. Analyze topic keywords
const topic = "AI 스타트업 피치덱";
const detectedTheme = detectTheme(topic);
// Result: '04-ai-tech' or '06-startup'

// 2. Load theme configuration
const themeConfig = await loadTheme(detectedTheme);

// 3. Apply to slides
applyTheme(slides, themeConfig);
```

## Fallback Theme

기본 테마가 명확하지 않은 경우:
- **Business/Corporate → Real Estate Trust**
- **Tech/Innovation → AI Futuristic**
- **Consumer/Lifestyle → F&B Appetite**
