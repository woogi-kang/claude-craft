# Design 스킬 라우팅 매트릭스

6개 디자인 관련 스킬의 역할 분담과 라우팅 규칙을 정의한다.

## 스킬 역할 요약

| 스킬 | 역할 | 핵심 키워드 |
|------|------|-------------|
| `design` | **오케스트레이터** — 종합 디자인 요청을 적절한 스킬로 분배. 자체 구현은 CIP, 슬라이드, 아이콘, 소셜 포토만 담당 | CIP, 아이콘, 소셜 포토, 브랜드 패키지 |
| `ui-ux-pro-max` | **설계 단계** — 스타일/컬러/폰트/레이아웃 의사결정, UX 가이드라인, 디자인 시스템 추천 | 스타일 추천, 컬러 팔레트, UX 리뷰, 디자인 시스템 생성 |
| `ui-styling` | **구현 단계** — shadcn/ui 컴포넌트 + Tailwind CSS로 실제 코드 작성 | shadcn, Tailwind, 컴포넌트 코드, 다크모드 구현 |
| `design-system` | **시스템 단계** — 3-레이어 토큰 아키텍처, CSS 변수, 컴포넌트 스펙 정의 | 토큰, CSS 변수, 컴포넌트 스펙, 토큰 검증 |
| `logo-creator` | **전문 특화** — AI 로고 생성 End-to-End (디스커버리 → 배치 생성 → 후처리) | 로고, brand mark, favicon, 앱 아이콘 |
| `banner-design` | **전문 특화** — 배너 디자인 (소셜/광고/웹/인쇄) | 배너, 커버, 헤더, 광고 배너 |

## 라우팅 매트릭스

| 사용자 의도 | 1차 스킬 | 2차 스킬 (위임) | 사용하지 않음 |
|-------------|----------|-----------------|---------------|
| "랜딩 페이지 디자인해줘" | `ui-ux-pro-max` (설계) | `ui-styling` (구현) | `design`, `design-system`, `logo-creator`, `banner-design` |
| "이 페이지 UX 리뷰해줘" | `ui-ux-pro-max` | — | `ui-styling`, `design`, `design-system` |
| "대시보드 컬러/폰트 추천해줘" | `ui-ux-pro-max` | — | `ui-styling`, `design` |
| "버튼 컴포넌트 만들어줘" | `ui-styling` | — | `ui-ux-pro-max`, `design` |
| "shadcn Dialog 추가해줘" | `ui-styling` | — | `ui-ux-pro-max`, `design`, `design-system` |
| "다크모드 구현해줘" | `ui-styling` | `ui-ux-pro-max` (컬러 검증) | `design`, `design-system` |
| "디자인 토큰 만들어줘" | `design-system` | — | `ui-ux-pro-max`, `ui-styling` |
| "CSS 변수 시스템 구축해줘" | `design-system` | — | `ui-ux-pro-max`, `ui-styling` |
| "컴포넌트 스펙 정의해줘" | `design-system` | — | `ui-ux-pro-max`, `ui-styling` |
| "로고 만들어줘" | `logo-creator` | — | `design`, `ui-ux-pro-max`, `ui-styling` |
| "favicon 만들어줘" | `logo-creator` | — | `design`, `ui-ux-pro-max` |
| "배너 디자인해줘" | `banner-design` | `ui-ux-pro-max` (리서치) | `design`, `ui-styling` |
| "트위터 헤더 만들어줘" | `banner-design` | — | `design`, `ui-ux-pro-max` |
| "CIP 만들어줘" | `design` | `logo-creator` (로고 없으면) | `ui-ux-pro-max`, `ui-styling` |
| "명함/레터헤드 디자인" | `design` | — | `ui-ux-pro-max`, `ui-styling`, `banner-design` |
| "아이콘 생성해줘" | `design` | — | `ui-ux-pro-max`, `ui-styling`, `banner-design` |
| "소셜 포토 만들어줘" | `design` | `ui-ux-pro-max` (디자인 인텔리전스) | `ui-styling`, `banner-design` |
| "슬라이드/발표자료 만들어줘" | `slides` | `design-system` (토큰 적용) | `ui-ux-pro-max`, `ui-styling` |
| "브랜드 패키지 전체 만들어줘" | `design` (오케스트레이션) | `logo-creator` → `design` (CIP) → `banner-design` | `ui-styling` |
| "새 프로젝트 디자인 시스템 구축" | `ui-ux-pro-max` (추천) | `design-system` (토큰) → `ui-styling` (구현) | `design`, `logo-creator`, `banner-design` |
| "Tailwind 테마 설정해줘" | `ui-styling` | `design-system` (토큰 연동) | `design`, `ui-ux-pro-max` |
| "프레젠테이션 만들어줘" | `slides` | `design-system` (토큰) | `ui-ux-pro-max`, `ui-styling` |

## 의사결정 플로우차트

```
사용자 요청 분석
      │
      ├─ 로고/favicon/앱 아이콘? ──────────→ logo-creator
      │
      ├─ 배너/커버/헤더/광고 배너? ────────→ banner-design
      │
      ├─ CIP/명함/아이콘/소셜포토/슬라이드? → design (자체 처리)
      │
      ├─ 브랜드 패키지 전체? ──────────────→ design (오케스트레이션)
      │                                      ├→ logo-creator
      │                                      ├→ design (CIP)
      │                                      └→ banner-design
      │
      ├─ 토큰/CSS 변수/컴포넌트 스펙? ─────→ design-system
      │
      ├─ 스타일/컬러/폰트 추천? ───────────→ ui-ux-pro-max
      │  UX 리뷰/접근성 검토?
      │  디자인 의사결정?
      │
      └─ 컴포넌트 코드 구현? ──────────────→ ui-styling
         shadcn/Tailwind 작업?
         다크모드/반응형 구현?
```

## 핵심 경계 규칙

1. **`design`은 구현하지 않는다** — CIP, 슬라이드, 아이콘, 소셜 포토만 자체 처리. 나머지는 위임.
2. **`ui-ux-pro-max`는 코드를 작성하지 않는다** — 무엇을 만들지 결정. 코드는 `ui-styling`이 담당.
3. **`ui-styling`은 디자인 의사결정을 하지 않는다** — 주어진 스펙대로 구현. 스타일 선택은 `ui-ux-pro-max`에 위임.
4. **`design-system`은 UI 코드를 작성하지 않는다** — 토큰과 스펙만 정의. 실제 적용은 `ui-styling`이 담당.
5. **`logo-creator`와 `banner-design`은 독립적이다** — 다른 스킬의 영역을 침범하지 않는다.
6. **`logo-creator`는 로고만 만든다** — CIP, 배너, 아이콘은 절대 처리하지 않는다.
7. **`banner-design`은 배너만 만든다** — 로고, CIP, UI 컴포넌트는 절대 처리하지 않는다.
