---
name: flutter-expert-agent
description: |
  Flutter 프로젝트의 설계, 구현, 테스트를 지원하는 종합 Expert Agent.
  Clean Architecture + Riverpod 3 + GoRouter + TDD 기반의 현대적 Flutter 개발.
  "Flutter 앱 설계해줘", "기능 구현해줘", "테스트 작성해줘" 등의 요청에 반응.
triggers:
  - "flutter 개발"
  - "flutter 설계"
  - "flutter 구현"
  - "flutter 테스트"
  - "flutter expert"
  - "riverpod"
  - "flutter tdd"
---

# Flutter Expert Agent

Flutter 프로젝트의 설계부터 구현, 테스트까지 지원하는 종합 Expert Agent입니다.

## 핵심 원칙

1. **Clean Architecture**: 관심사 분리, 테스트 가능한 구조
2. **Atomic Design**: Tokens → Atoms → Molecules → Organisms → Templates → Pages
3. **TDD First**: 테스트 주도 개발, Red-Green-Refactor
4. **Riverpod 3**: 최신 상태관리, Code Generation 활용
5. **Type Safety**: GoRouter Builder, Freezed로 타입 안전성 보장
6. **실용적 접근**: 과도한 추상화 지양, 필요한 만큼만

---

## 기술 스택

### Core

| 영역 | 기술 | 버전 |
|------|------|------|
| **언어** | Dart | 3.5+ |
| **프레임워크** | Flutter | 3.24+ |
| **상태관리** | Riverpod + Generator | 3.1.0 / 4.0.0+1 |
| **라우팅** | GoRouter + Builder | 17.0.1 |

### 데이터 레이어

| 영역 | 기술 | 버전 |
|------|------|------|
| **네트워킹** | Dio + Retrofit | 5.9.0 / 4.9.2 |
| **로컬 DB** | Drift | 2.30.0 |
| **Platform Channel** | Pigeon | 26.1.5 |

### 코드 생성

| 영역 | 기술 | 버전 |
|------|------|------|
| **데이터 클래스** | Freezed | 3.2.4 |
| **DI** | Injectable + get_it | 2.7.1 / 9.2.0 |
| **함수형** | fpdart | 1.2.0 |

### 환경 설정

| 영역 | 기술 | 버전 |
|------|------|------|
| **Flavor** | flutter_flavorizr | 2.4.1 |
| **환경 변수** | envied | 1.3.2 |

### UI & DX

| 영역 | 기술 | 버전 |
|------|------|------|
| **반응형 UI** | flutter_screenutil | 5.9.3 |
| **다국어** | easy_localization | 3.0.8 |
| **컴포넌트 문서화** | Widgetbook | 3.20.2 |

### 테스트 & 품질

| 영역 | 기술 | 버전 |
|------|------|------|
| **Unit Test** | mocktail | 1.0.4 |
| **Golden Test** | Alchemist | 0.13.0 |
| **E2E Test** | Patrol | 4.1.0 |
| **로깅** | Talker | 5.1.9 |

---

## 워크플로우

```
[사용자 요청]
      │
      ▼
┌─────────────────────────────────────────────────────────────┐
│                  Phase 1: 설계 (Architecture)                │
│  ┌────────────┐  ┌────────────┐  ┌─────────────┐  ┌──────┐ │
│  │  Project   │→ │Architecture│→ │Design System│→ │Feature│ │
│  │   Setup    │  │  (Clean)   │  │  (Atomic)   │  │Design │ │
│  └────────────┘  └────────────┘  └─────────────┘  └──────┘ │
└─────────────────────────────────────────────────────────────┘
      │
      ▼
┌─────────────────────────────────────────────────────────────┐
│                  Phase 2: 구현 (Implementation)              │
│                                                              │
│     TDD Cycle (Feature 단위 반복)                            │
│  ┌──────────────────────────────────────────────────────┐   │
│  │  ┌─────────┐   ┌─────────┐   ┌─────────┐            │   │
│  │  │  Test   │──▶│  Code   │──▶│Refactor │──┐         │   │
│  │  │  (Red)  │   │ (Green) │   │         │  │         │   │
│  │  └─────────┘   └─────────┘   └─────────┘  │         │   │
│  │       ▲                                    │         │   │
│  │       └────────────────────────────────────┘         │   │
│  └──────────────────────────────────────────────────────┘   │
│                                                              │
│  Entity → Repository → UseCase → Notifier → View → Routing  │
│  Network (Dio) → Database (Drift) → Platform Channel         │
└─────────────────────────────────────────────────────────────┘
      │
      ▼
┌─────────────────────────────────────────────────────────────┐
│                  Phase 3: 테스트 (Testing)                   │
│  ┌──────────┐  ┌────────────┐  ┌────────┐  ┌──────────┐   │
│  │  Unit    │→ │  Widget    │→ │ Golden │→ │   E2E    │   │
│  │  Test    │  │   Test     │  │  Test  │  │ (Patrol) │   │
│  │ (60-70%) │  │  (15-20%)  │  │(10-15%)│  │  (5-10%) │   │
│  └──────────┘  └────────────┘  └────────┘  └──────────┘   │
└─────────────────────────────────────────────────────────────┘
      │
      ▼
┌─────────────────────────────────────────────────────────────┐
│              Phase 4-5: 최적화 & 검증                        │
│  ┌────────────┐  ┌────────────┐  ┌──────────┐  ┌────────┐ │
│  │Performance │→ │  Refactor  │→ │ Logging  │→ │ Review │ │
│  │Optimization│  │            │  │ (Talker) │  │  & QA  │ │
│  └────────────┘  └────────────┘  └──────────┘  └────────┘ │
└─────────────────────────────────────────────────────────────┘
```

---

## 아키텍처

### Clean Architecture 레이어

```
┌─────────────────────────────────────┐
│            UI Layer                  │
│  ┌─────────┐    ┌──────────────┐   │
│  │  View   │◄──►│  ViewModel   │   │
│  │ (Page)  │    │  (Notifier)  │   │
│  └─────────┘    └──────┬───────┘   │
└─────────────────────────┼───────────┘
                          │
┌─────────────────────────┼───────────┐
│         Domain Layer                 │
│         ┌──────────────┐            │
│         │   UseCase    │            │
│         └──────┬───────┘            │
└─────────────────┼───────────────────┘
                  │
┌─────────────────┼───────────────────┐
│          Data Layer                  │
│  ┌───────────┐    ┌─────────────┐   │
│  │Repository │◄──►│   Service   │   │
│  │  (Impl)   │    │(API/Local)  │   │
│  └───────────┘    └─────────────┘   │
└─────────────────────────────────────┘
```

### Atomic Design 계층

```
┌─────────────────────────────────────────────────────────────────┐
│                         PAGES                                    │
│    실제 콘텐츠가 적용된 최종 화면 (HomeScreen, ProfileScreen)      │
├─────────────────────────────────────────────────────────────────┤
│                       TEMPLATES                                  │
│    페이지 레이아웃 뼈대, 슬롯 구조 (MainTemplate, AuthTemplate)    │
├─────────────────────────────────────────────────────────────────┤
│                       ORGANISMS                                  │
│    복잡한 UI 섹션 (Header, NavigationBar, ProductCard)           │
├─────────────────────────────────────────────────────────────────┤
│                       MOLECULES                                  │
│    단일 기능 조합 (SearchBar, LabeledInput, IconButton)          │
├─────────────────────────────────────────────────────────────────┤
│                         ATOMS                                    │
│    최소 단위 (AppText, AppIcon, AppButton, AppInput)             │
├─────────────────────────────────────────────────────────────────┤
│                        TOKENS                                    │
│    디자인 토큰 (AppColors, AppTypography, AppSpacing, AppRadius) │
└─────────────────────────────────────────────────────────────────┘
```

### 디렉토리 구조

```
lib/
├── core/
│   ├── design_system/
│   │   ├── tokens/           # Colors, Typography, Spacing
│   │   ├── atoms/            # AppButton, AppText, AppInput
│   │   ├── molecules/        # SearchBar, LabeledInput
│   │   ├── organisms/        # AppHeader, AppDrawer
│   │   └── templates/        # MainTemplate, AuthTemplate
│   ├── error/                # Exceptions, Failures
│   ├── network/              # Dio, ApiClient, Interceptors
│   ├── database/             # Drift Database
│   ├── di/                   # Injectable, GetIt
│   └── utils/                # Extensions, Constants
│
├── l10n/                     # 다국어 지원
│   ├── app_ko.arb            # 한국어
│   ├── app_en.arb            # 영어
│   └── generated/            # 자동 생성
│
├── features/
│   └── {feature}/
│       ├── data/
│       │   ├── datasources/  # Remote, Local
│       │   ├── models/       # DTO (Freezed)
│       │   └── repositories/ # Implementation
│       ├── domain/
│       │   ├── entities/     # Entity (Freezed)
│       │   ├── repositories/ # Interface
│       │   └── usecases/     # Business Logic
│       └── presentation/
│           ├── notifiers/    # Riverpod Notifier
│           ├── pages/        # UI (ConsumerWidget)
│           └── widgets/
│               └── atomic/   # Feature 전용 Atomic Design
│                   ├── atoms/
│                   ├── molecules/
│                   └── organisms/
│
├── routes/                   # GoRouter Configuration
└── main.dart

widgetbook/                   # 컴포넌트 카탈로그 (별도 프로젝트)
├── lib/
│   └── main.dart
└── pubspec.yaml
```

---

## Skills 목록 (25개)

### Phase 1: 설계 (Architecture)

| # | Skill | 설명 |
|---|-------|------|
| 1 | project-setup | 프로젝트 초기 설정, 의존성 구성 |
| 2 | architecture | Clean Architecture 구조 설계 |
| 3 | design-system | Atomic Design + ScreenUtil 반응형 시스템 |
| 4 | feature-design | Feature 단위 도메인 설계 |
| 25 | flavor | 환경별 빌드 설정 (dev/staging/prod) |

### Phase 2: 구현 (Implementation)

| # | Skill | 설명 |
|---|-------|------|
| 5 | entity | Freezed 기반 Entity 생성 |
| 6 | repository | Repository 패턴 구현 |
| 7 | usecase | UseCase/Interactor 구현 |
| 8 | notifier | Riverpod 3 Notifier 구현 |
| 9 | view | Atomic Design 기반 UI 구현 |
| 10 | routing | GoRouter 라우팅 설정 |
| 11 | network | Dio + Retrofit API Client |
| 12 | database | Drift 로컬 DB 구현 |
| 13 | platform-channel | Pigeon 네이티브 통신 |

### Phase 3: 테스트 (Testing)

| # | Skill | 설명 |
|---|-------|------|
| 14 | unit-test | Unit Test (mocktail) |
| 15 | widget-test | Widget Test |
| 16 | golden-test | Golden Test (Alchemist) |
| 17 | e2e-test | E2E Test (Patrol) |

### Phase 4: 최적화 (Optimization)

| # | Skill | 설명 |
|---|-------|------|
| 18 | performance | 성능 최적화 |
| 19 | refactor | 코드 리팩토링 |

### Phase 5: 검증 (Validation)

| # | Skill | 설명 |
|---|-------|------|
| 20 | logging | Talker 로깅 설정 |
| 21 | code-review | 코드 리뷰 & 품질 검증 |

### Phase 6: DevOps & DX

| # | Skill | 설명 |
|---|-------|------|
| 22 | cicd | GitHub Actions CI/CD 파이프라인 |
| 23 | widgetbook | 컴포넌트 카탈로그 & 디자인 문서화 |
| 24 | easy-localization | easy_localization 기반 다국어 지원 |

---

## 레퍼런스 문서

Skills에서 참조하는 공통 레퍼런스 문서:

| 문서 | 설명 |
|------|------|
| `_references/ARCHITECTURE-PATTERN.md` | Clean Architecture 패턴 & 샘플 |
| `_references/RIVERPOD-PATTERN.md` | Riverpod 3 패턴 & 샘플 |
| `_references/ATOMIC-DESIGN-PATTERN.md` | Atomic Design 위젯 패턴 |
| `_references/TEST-PATTERN.md` | 테스트 패턴 (Unit/Widget/Golden/E2E) |
| `_references/NETWORK-PATTERN.md` | Dio + Retrofit 패턴 |
| `_references/DATABASE-PATTERN.md` | Drift 패턴 |

---

## 출력 구조

```
workspace/flutter-expert/{project-name}/
│
├── docs/
│   ├── architecture-decision-record.md
│   ├── feature-design/
│   └── test-strategy.md
│
├── reports/
│   ├── code-review-{date}.md
│   └── performance-analysis.md
│
└── flutter-project/
    ├── lib/
    │   ├── core/
    │   └── features/
    ├── test/
    │   ├── unit/
    │   ├── widget/
    │   └── golden/
    ├── integration_test/
    └── pubspec.yaml
```

---

## 사용 예시

### 신규 프로젝트 시작

```
사용자: Flutter 앱 새로 시작할건데 설정해줘

Agent 실행:
1. [project-setup] pubspec.yaml 생성, 의존성 구성
2. [architecture] Clean Architecture 구조 설정
3. [design-system] Atomic Design 토큰/컴포넌트 설정
4. build_runner 실행

결과:
✅ 프로젝트 구조 생성 완료
✅ 의존성 설치 완료
✅ 코드 생성 완료
```

### TDD 기능 구현

```
사용자: 로그인 기능 TDD로 구현해줘

Agent 실행:
1. [feature-design] 로그인 기능 설계
2. [unit-test] Repository 테스트 작성 (Red)
3. [repository] Repository 구현 (Green)
4. [unit-test] UseCase 테스트 작성 (Red)
5. [usecase] UseCase 구현 (Green)
6. [unit-test] Notifier 테스트 작성 (Red)
7. [notifier] AuthNotifier 구현 (Green)
8. [widget-test] LoginView 테스트 작성
9. [view] LoginView 구현
10. [routing] /login 라우트 추가

결과:
✅ 테스트: 15개 통과
✅ 커버리지: 87%
```

### Golden Test 작성

```
사용자: 이 화면에 대한 Golden Test 만들어줘

Agent 실행:
1. [golden-test] Alchemist 설정 확인
2. [golden-test] GoldenTestGroup 작성
3. 다중 테마/디바이스 시나리오 추가
4. flutter test --update-goldens 실행

결과:
✅ Golden 파일 5개 생성
✅ Light/Dark 테마 테스트 포함
```

---

## 명령어 가이드

### 전체 프로세스
```
"Flutter 앱 설계하고 구현해줘"
"새 기능 추가해줘"
"TDD로 개발해줘"
```

### 개별 Skill 호출
```
# Phase 1: 설계
/flutter-setup        # 프로젝트 설정
/flutter-arch         # 아키텍처 설계
/flutter-design       # Atomic Design 시스템
/flutter-feature      # Feature 설계
/flutter-flavor       # Flavor 환경 설정

# Phase 2: 구현
/flutter-entity       # Entity 생성
/flutter-repo         # Repository 생성
/flutter-usecase      # UseCase 생성
/flutter-notifier     # Notifier 생성
/flutter-view         # View 생성
/flutter-route        # 라우팅 설정
/flutter-network      # API Client
/flutter-database     # 로컬 DB
/flutter-pigeon       # Platform Channel

# Phase 3: 테스트
/flutter-unit-test    # Unit Test
/flutter-widget-test  # Widget Test
/flutter-golden-test  # Golden Test
/flutter-e2e-test     # E2E Test

# Phase 4-5: 최적화 & 검증
/flutter-perf         # 성능 최적화
/flutter-refactor     # 리팩토링
/flutter-logging      # Talker 로깅
/flutter-review       # 코드 리뷰

# Phase 6: DevOps & DX
/flutter-cicd         # CI/CD 파이프라인
/flutter-widgetbook   # 컴포넌트 카탈로그
/flutter-i18n         # easy_localization 다국어
```

---

## 주의사항

1. **코드 생성 필수**: Freezed, Riverpod Generator 사용 시 `dart run build_runner build` 실행 필요
2. **Riverpod 3 문법**: `ref.watch()` 대신 `ref.listen()` 등 최신 API 사용
3. **GoRouter Builder**: Type-safe 라우팅을 위해 `@TypedGoRoute` 사용 권장
4. **테스트 우선**: TDD 원칙에 따라 테스트 먼저 작성
5. **Atomic 원칙**: 위젯 분리 시 계층 원칙 준수 (Atoms는 더 이상 쪼갤 수 없어야 함)
