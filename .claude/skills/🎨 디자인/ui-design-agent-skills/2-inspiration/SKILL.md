---
name: fd-inspiration
description: |
  디자인 영감과 레퍼런스를 수집하는 스킬.
  Awwwards, Dribbble, SiteInspire 등에서 트렌드 분석 및 무드보드 생성을 지원합니다.
triggers:
  - "레퍼런스"
  - "인스피레이션"
  - "영감"
  - "무드보드"
  - "벤치마크"
  - "트렌드"
input:
  - 프로젝트 컨텍스트 (1-context 결과물)
  - 선호 스타일 힌트 (선택)
output:
  - workspace/work-design/{project}/inspiration/mood-board.md
  - workspace/work-design/{project}/inspiration/trend-analysis.md
  - workspace/work-design/{project}/inspiration/competitor-analysis.md
---

# Inspiration & Reference Skill

효과적인 디자인은 좋은 레퍼런스에서 시작됩니다.
이 스킬은 체계적인 레퍼런스 수집, 트렌드 분석, 무드보드 생성을 지원합니다.

## 왜 중요한가?

```
레퍼런스 없이 디자인
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
백지 상태 → 시행착오 반복 → 시간 낭비

레퍼런스 기반 디자인
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Curated References → 명확한 방향 → 효율적 실행
```

## Input

| 항목 | 필수 | 설명 |
|------|------|------|
| 프로젝트 컨텍스트 | Y | 1-context 스킬 결과물 |
| 산업군/유형 | Y | 컨텍스트에서 추출 |
| 선호 스타일 힌트 | N | 미니멀, 다크, 그라데이션 등 |
| 경쟁사 URL | N | 분석할 경쟁사 사이트 |

## 레퍼런스 소스

### 1. 최고 수준 디자인 (Award Sites)

| 소스 | URL | 특징 | 적합 용도 |
|------|-----|------|----------|
| **Awwwards** | awwwards.com | 최고 수준, 인터랙션 중심 | 에이전시, 포트폴리오, 브랜드 |
| **CSS Design Awards** | cssdesignawards.com | UX 중시, 다양한 카테고리 | SaaS, 랜딩페이지 |
| **FWA** | thefwa.com | 혁신적, 실험적 | 크리에이티브, 인터랙티브 |
| **Webby Awards** | webbyawards.com | 산업별 분류, 기능 중심 | 엔터프라이즈, 비영리 |

### 2. 디자인 커뮤니티

| 소스 | URL | 특징 | 적합 용도 |
|------|-----|------|----------|
| **Dribbble** | dribbble.com | UI 요소, 마이크로 인터랙션 | 컴포넌트, 아이콘, 일러스트 |
| **Behance** | behance.net | 프로젝트 전체 케이스 스터디 | 브랜딩, UX 프로세스 |
| **Figma Community** | figma.com/community | 실제 사용 가능한 파일 | 템플릿, 컴포넌트 키트 |

### 3. 갤러리/컬렉션

| 소스 | URL | 특징 | 적합 용도 |
|------|-----|------|----------|
| **SiteInspire** | siteinspire.com | 미니멀, 타이포 중심 | 콘텐츠 사이트, 포트폴리오 |
| **Godly** | godly.website | 최신 트렌드, 큐레이션 | 랜딩페이지, SaaS |
| **Lapa Ninja** | lapa.ninja | 랜딩페이지 전문 | 마케팅, 제품 페이지 |
| **Land-book** | land-book.com | 카테고리 분류 상세 | 산업별 레퍼런스 |
| **One Page Love** | onepagelove.com | 원페이지 전문 | 간단한 랜딩, 이벤트 |
| **Dark Mode Design** | darkmodedesign.com | 다크 테마 전문 | 다크 UI |
| **Minimal Gallery** | minimal.gallery | 미니멀 전문 | 미니멀 디자인 |

### 4. 산업별 갤러리

| 산업 | 소스 | URL |
|------|------|-----|
| SaaS | SaaS Landing Page | saaslandingpage.com |
| SaaS | SaaS Pages | saaspages.xyz |
| 이커머스 | ecomm.design | ecomm.design |
| 이커머스 | Page Flows | pageflows.com |
| 대시보드 | UI Garage | uigarage.net |
| 대시보드 | Collect UI | collectui.com |
| 모바일 | Mobbin | mobbin.com |
| 모바일 | Pttrns | pttrns.com |

### 5. 트렌드/리서치

| 소스 | URL | 특징 |
|------|-----|------|
| **Pinterest** | pinterest.com | 무드보드, 비주얼 영감 |
| **Muzli** | muz.li | 일일 디자인 뉴스 |
| **Codrops** | codrops.tympanus.com | 실험적 인터랙션 |
| **Screenlane** | screenlane.com | UX 패턴, 플로우 |

## 트렌드 분석 프레임워크

### 2024-2025 주요 트렌드

```yaml
visual_trends:
  bento_grid:
    description: "다양한 크기의 카드가 그리드로 배치"
    use_case: "대시보드, 피처 섹션, 포트폴리오"
    reference: "Apple 뉴스, Linear"

  glassmorphism_2.0:
    description: "반투명 + 블러 + 미묘한 그라데이션"
    use_case: "카드, 모달, 네비게이션"
    caution: "성능 주의, 접근성 고려"

  dark_mode_default:
    description: "다크 모드가 기본, 라이트가 대안"
    use_case: "테크, SaaS, 개발자 도구"
    reference: "Linear, Vercel, Raycast"

  3d_illustrations:
    description: "3D 캐릭터, 아이콘, 배경"
    use_case: "SaaS, 핀테크, 게임"
    tools: "Spline, Blender"

  variable_fonts:
    description: "가변 폰트로 다이내믹 타이포"
    use_case: "에디토리얼, 브랜딩"
    reference: "매거진, 에이전시"

  kinetic_typography:
    description: "움직이는 텍스트, 스크롤 기반"
    use_case: "에이전시, 포트폴리오"
    reference: "Locomotive, 크리에이티브 스튜디오"

  organic_shapes:
    description: "불규칙한 blob, 유기적 곡선"
    use_case: "웰니스, 뷰티, 라이프스타일"
    contrast: "기하학적 테크 디자인"

  gradients_mesh:
    description: "복잡한 메시 그라데이션"
    use_case: "배경, 히어로 섹션"
    tools: "Figma Mesh Gradient"

interaction_trends:
  scroll_storytelling:
    description: "스크롤 기반 애니메이션 스토리텔링"
    use_case: "제품 쇼케이스, 케이스 스터디"
    reference: "Apple 제품 페이지"

  micro_interactions:
    description: "버튼, 호버, 로딩 등 섬세한 피드백"
    use_case: "모든 인터랙티브 요소"
    library: "Framer Motion, Lottie"

  cursor_effects:
    description: "커서 따라다니는 효과, 커스텀 커서"
    use_case: "크리에이티브, 포트폴리오"
    caution: "사용성 저하 주의"

  horizontal_scroll:
    description: "가로 스크롤 섹션"
    use_case: "갤러리, 타임라인"
    caution: "UX 혼란 가능"
```

### 트렌드 분석 템플릿

```markdown
## Trend Analysis: {Trend Name}

### 설명
{trend_description}

### 발견된 사례
| 사이트 | URL | 적용 방식 |
|--------|-----|----------|
| {site1} | {url1} | {how_applied} |
| {site2} | {url2} | {how_applied} |

### 우리 프로젝트 적용 가능성
- **적합도**: 높음 / 중간 / 낮음
- **이유**: {reasoning}
- **적용 방안**: {how_to_apply}

### 주의사항
- {caution_1}
- {caution_2}
```

## 무드보드 생성 가이드

### 무드보드 구성 요소

```yaml
mood_board_elements:
  colors:
    count: 5-7
    description: "메인 팔레트 + 액센트"

  typography:
    count: 2-3
    description: "헤딩 + 본문 + 액센트 폰트"

  imagery:
    count: 5-10
    types:
      - "전체 레이아웃 스크린샷"
      - "컴포넌트 클로즈업"
      - "일러스트레이션/아이콘 스타일"
      - "포토그래피 톤"

  ui_elements:
    count: 5-10
    types:
      - "버튼 스타일"
      - "카드 디자인"
      - "네비게이션"
      - "폼 요소"
      - "아이콘"

  mood_keywords:
    count: 5-7
    description: "느낌을 표현하는 키워드"

  textures:
    count: 2-4
    description: "그라데이션, 노이즈, 패턴 등"
```

### 무드보드 수집 프로세스

```
1. 컨텍스트 기반 키워드 추출
   └── 산업, 톤, 타겟에서 검색어 도출
        │
        ▼
2. 소스별 검색 (병렬)
   ├── Awwwards: {industry} + {style}
   ├── Dribbble: {component} + {aesthetic}
   ├── SiteInspire: {type} + {mood}
   └── Pinterest: {mood_keywords}
        │
        ▼
3. 1차 수집 (20-30개)
        │
        ▼
4. 필터링 기준
   ├── 컨텍스트 적합성
   ├── 기술적 실현 가능성
   ├── 타겟 사용자 적합성
   └── 차별화 가능성
        │
        ▼
5. 큐레이션 (10-15개)
        │
        ▼
6. 무드보드 문서화
```

## 경쟁사 분석 템플릿

### 분석 항목

```yaml
competitor_analysis:
  overview:
    name: ""
    url: ""
    one_liner: ""
    industry: ""

  visual_design:
    color_palette:
      primary: ""
      secondary: ""
      accent: ""
      mood: ""

    typography:
      heading_font: ""
      body_font: ""
      style: ""  # 예: "모던 산세리프", "클래식 세리프"

    imagery:
      style: ""  # 사진, 일러스트, 3D
      tone: ""   # 밝음, 어두움, 비비드

    layout:
      style: ""  # 그리드, 자유형, 벤토
      whitespace: ""  # 많음, 보통, 적음

  ux_patterns:
    navigation: ""
    cta_style: ""
    form_design: ""
    micro_interactions: ""

  strengths:
    - ""
    - ""

  weaknesses:
    - ""
    - ""

  differentiation_opportunity:
    - ""
    - ""
```

## Workflow

```
1. 컨텍스트 로드
   └── workspace/work-design/{project}/context/project-context.md
        │
        ▼
2. 검색 키워드 도출
   ├── 산업: {industry}
   ├── 유형: {project_type}
   ├── 톤: {brand_tone}
   └── 스타일 힌트: {style_hints}
        │
        ▼
3. 레퍼런스 수집 (병렬)
   ├── Award Sites 검색
   ├── 갤러리 검색
   ├── 산업별 갤러리 검색
   └── 경쟁사 분석
        │
        ▼
4. 트렌드 분석
   └── 수집된 레퍼런스에서 패턴 추출
        │
        ▼
5. 무드보드 큐레이션
   └── 10-15개 핵심 레퍼런스 선정
        │
        ▼
6. 문서화 및 저장
   ├── mood-board.md
   ├── trend-analysis.md
   └── competitor-analysis.md
        │
        ▼
7. 사용자 피드백 수집
        │
        ▼
8. 필요시 보완 반복
```

## Output

### 출력 디렉토리 구조

```
workspace/work-design/{project}/
├── context/
│   └── project-context.md
└── inspiration/
    ├── mood-board.md           # 무드보드
    ├── trend-analysis.md       # 트렌드 분석
    └── competitor-analysis.md  # 경쟁사 분석
```

### 무드보드 출력 템플릿

```markdown
# {Project Name} Mood Board

> 생성일: {date}
> 컨텍스트: context/project-context.md 기반

## 핵심 키워드

| 키워드 | 설명 |
|--------|------|
| {keyword_1} | {why_relevant} |
| {keyword_2} | {why_relevant} |
| {keyword_3} | {why_relevant} |

## 컬러 팔레트 영감

| 컬러 | HEX | 레퍼런스 | 용도 |
|------|-----|----------|------|
| {color_name} | {hex} | {source} | Primary |
| {color_name} | {hex} | {source} | Secondary |
| {color_name} | {hex} | {source} | Accent |

## 타이포그래피 영감

| 역할 | 폰트 | 레퍼런스 | 느낌 |
|------|------|----------|------|
| Heading | {font} | {source} | {mood} |
| Body | {font} | {source} | {mood} |

## 레퍼런스 사이트

### 전체 레이아웃

| 순위 | 사이트 | URL | 참고 포인트 |
|------|--------|-----|-------------|
| 1 | {site} | {url} | {what_to_learn} |
| 2 | {site} | {url} | {what_to_learn} |
| 3 | {site} | {url} | {what_to_learn} |

### 컴포넌트/UI 요소

| 요소 | 레퍼런스 | URL | 설명 |
|------|----------|-----|------|
| Hero Section | {site} | {url} | {description} |
| Navigation | {site} | {url} | {description} |
| Cards | {site} | {url} | {description} |
| CTA Buttons | {site} | {url} | {description} |
| Footer | {site} | {url} | {description} |

### 인터랙션/모션

| 타입 | 레퍼런스 | URL | 적용 방안 |
|------|----------|-----|----------|
| {interaction_type} | {site} | {url} | {how_to_apply} |

## 이미지 스타일 가이드

### 포토그래피
- **톤**: {bright/dark/natural}
- **필터**: {filter_style}
- **구도**: {composition_style}

### 일러스트레이션
- **스타일**: {2d/3d/line/flat}
- **컬러**: {vibrant/muted/monochrome}
- **레퍼런스**: {source}

### 아이콘
- **스타일**: {line/solid/duo-tone}
- **굵기**: {thin/regular/bold}
- **레퍼런스**: {icon_set}

## 적용 우선순위

| 우선순위 | 요소 | 적용 레퍼런스 | 이유 |
|----------|------|---------------|------|
| 1 | {element} | {reference} | {rationale} |
| 2 | {element} | {reference} | {rationale} |
| 3 | {element} | {reference} | {rationale} |

## 피해야 할 것

| 항목 | 이유 |
|------|------|
| {avoid_1} | {why} |
| {avoid_2} | {why} |

---

*다음 단계: 3-direction (미적 방향 결정)*
```

### 트렌드 분석 출력 템플릿

```markdown
# {Project Name} Trend Analysis

> 분석일: {date}
> 산업군: {industry}

## 관련 트렌드 요약

| 트렌드 | 적합도 | 이유 |
|--------|--------|------|
| {trend_1} | 높음/중간/낮음 | {rationale} |
| {trend_2} | 높음/중간/낮음 | {rationale} |

## 상세 분석

### {Trend 1}

**설명**: {description}

**발견 사례**:
- {site_1} - {url}
- {site_2} - {url}

**적용 방안**: {how_to_apply}

**주의사항**: {cautions}

---

*각 트렌드 반복*
```

## 퀄리티 체크리스트

```
□ 최소 10개 레퍼런스 수집
□ 3개 이상 소스 사용 (Awwwards, Dribbble, 산업별)
□ 경쟁사 최소 2개 분석
□ 컬러 팔레트 영감 3개 이상
□ 타이포그래피 영감 2개 이상
□ 컴포넌트별 레퍼런스 5개 이상
□ 피해야 할 것 명시
□ 적용 우선순위 설정
```

## 다음 스킬 연결

인스피레이션 수집 완료 후:

| 다음 스킬 | 조건 |
|-----------|------|
| **3-direction** | 미적 방향 결정 필요 (권장) |
| **4-typography** | 폰트 결정이 시급한 경우 |
| **5-color** | 컬러가 가장 중요한 경우 |

---

*좋은 레퍼런스는 창작의 시작점입니다. Copy하지 말고 Learn하세요.*
