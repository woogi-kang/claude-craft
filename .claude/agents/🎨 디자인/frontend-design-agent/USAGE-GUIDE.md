# Frontend Design Agent 사용 가이드

독창적이고 프로덕션 수준의 프론트엔드 디자인을 생성하는 Agent 사용법입니다.

---

## 전략 비교표

| 전략 | 특징 | 폰트 스타일 | 적용 분야 | 템플릿 |
|------|------|------------|----------|--------|
| **Modern** | 세련된, 미니멀, 기능 중심 | Sans-serif, Mono | SaaS, AI, 개발자 도구 | Liquid Glass, Barely-There, Tech Documentation |
| **Minimal** | 여백, 타이포그래피 중심 | Serif, Elegant | 미디어, 갤러리, 웰니스 | Editorial Magazine, Brutalist Raw, Organic Natural |
| **Bold** | 대담한, 실험적, 눈에 띄는 | Display, Decorative | 브랜드, 포트폴리오, 게임 | Soft Maximalism, Anti-Design, Retro-Futuristic |

---

## 전략 선택 가이드

### Modern 전략 선택 시
- B2B SaaS 제품
- AI/ML 플랫폼
- 개발자 도구 / API 문서
- 테크 스타트업 앱

### Minimal 전략 선택 시
- 매거진 / 블로그
- 아트 갤러리 / 포트폴리오
- 웰니스 / 라이프스타일
- 럭셔리 브랜드

### Bold 전략 선택 시
- 브랜드 캠페인 사이트
- 크리에이티브 에이전시
- 게임 / 엔터테인먼트
- 스타트업 랜딩페이지

---

## 전체 명령어

### 자연어 요청
```
"UI 디자인해줘"
"랜딩페이지 만들어줘"
"대시보드 디자인 해줘"
"SaaS 앱 디자인"
"모바일 앱 UI 만들어줘"
```

### Phase 1: Discovery (탐색)
| 명령어 | 설명 |
|--------|------|
| `/fd-context` | 프로젝트 컨텍스트 파악 |
| `/fd-inspiration` | 레퍼런스 수집 |
| `/fd-direction` | 미적 방향 결정 |

### Phase 2: Foundation (기반)
| 명령어 | 설명 |
|--------|------|
| `/fd-typography` | 타이포그래피 시스템 |
| `/fd-color` | 색상 팔레트 |
| `/fd-spacing` | 스페이싱 시스템 |
| `/fd-motion` | 애니메이션 시스템 |

### Phase 3: Components (컴포넌트)
| 명령어 | 설명 |
|--------|------|
| `/fd-primitives` | 기본 컴포넌트 |
| `/fd-patterns` | 복합 패턴 |
| `/fd-effects` | 배경 효과 |
| `/fd-interactions` | 마이크로인터랙션 |

### Phase 4: Pages (페이지)
| 명령어 | 설명 |
|--------|------|
| `/fd-landing` | 랜딩 페이지 |
| `/fd-dashboard` | 대시보드 |
| `/fd-content` | 콘텐츠 페이지 |
| `/fd-mobile` | 모바일 최적화 |

### Phase 5: Polish (완성)
| 명령어 | 설명 |
|--------|------|
| `/fd-a11y` | 접근성 검증 |
| `/fd-responsive` | 반응형 검증 |
| `/fd-perf` | 성능 최적화 |

---

## 사용 예시

### 예시 1: B2B SaaS 대시보드
```
입력: "B2B SaaS 대시보드 디자인해줘"

Agent 처리:
1. [context] → B2B, 데이터 중심, 생산성 도구
2. [direction] → Modern 전략 → "Barely-There Minimal"
3. [typography] → Geist + JetBrains Mono
4. [color] → Neutral base + Blue accent
5. [dashboard] → 데이터 테이블, 차트, 필터
```

### 예시 2: 크리에이티브 포트폴리오
```
입력: "디자이너 포트폴리오 만들어줘"

Agent 처리:
1. [context] → 개인 브랜딩, 창의성 강조
2. [direction] → Bold 전략 → "Anti-Design Chaos"
3. [typography] → Basement Grotesque
4. [effects] → 노이즈 텍스처, 커스텀 커서
5. [landing] → 비정형 그리드, 오버랩 레이아웃
```

### 예시 3: 웰니스 앱 랜딩
```
입력: "명상 앱 랜딩페이지 만들어줘"

Agent 처리:
1. [context] → 웰니스, 평화로움, 자연
2. [direction] → Minimal 전략 → "Organic Natural"
3. [typography] → Cormorant + Lora
4. [color] → Earth tones, Soft greens
5. [landing] → 부드러운 곡선, 여백 활용
```

---

## 12개 Aesthetic Template 요약

| # | 템플릿 | 전략 | 특징 | 적용 분야 |
|---|--------|------|------|----------|
| 1 | Barely-There Minimal | Modern | 극도의 절제, 여백 | SaaS, AI |
| 2 | Liquid Glass | Modern | Apple 스타일, 블러 | 앱 |
| 3 | Tech Documentation | Modern | 매뉴얼 스타일 | 개발자 도구 |
| 4 | Editorial Magazine | Minimal | 타이포 중심 | 미디어 |
| 5 | Organic Natural | Minimal | 자연, 부드러운 곡선 | 웰니스 |
| 6 | Brutalist Raw | Minimal | 거친, 원시적 | 갤러리 |
| 7 | Luxury Refined | Minimal | 고급, 세련된 | 럭셔리 |
| 8 | Soft Maximalism | Bold | 대담하지만 통제된 | 브랜드 |
| 9 | Anti-Design Chaos | Bold | 규칙 파괴, 비정형 | 포트폴리오 |
| 10 | Retro-Futuristic | Bold | 90s + 사이버 | 게임 |
| 11 | Playful Rounded | Bold | 친근한, 둥근 | 교육 |
| 12 | Grade-School Bold | Bold | 기본 색상, 명확한 | 스타트업 |

---

## 디자인 다양성 보장

### Template Rotation
- 12개 템플릿 중 이전에 사용하지 않은 것 우선 선택
- 같은 프로젝트 유형이라도 다른 미적 방향 제안

### Color Palette Shuffle
- 같은 템플릿이라도 accent color를 매번 다르게
- Primary hue를 +/-30도 범위에서 변형
- Dark/Light mode 기본값 번갈아 제안

### Layout Variation
- Centered Text
- Split Layout (Left Text + Right Image)
- Split Layout (Left Image + Right Text)
- Full-Bleed Background
- Asymmetric Grid
- Bento Style

---

## 참조 문서

| 문서 | 위치 |
|------|------|
| Modern 전략 상세 | `references/strategies/strategy-modern.md` |
| Minimal 전략 상세 | `references/strategies/strategy-minimal.md` |
| Bold 전략 상세 | `references/strategies/strategy-bold.md` |
| 디자인 원칙 | `references/shared/design-principles.md` |
| 기술 스택 | `references/shared/tech-stack.md` |
