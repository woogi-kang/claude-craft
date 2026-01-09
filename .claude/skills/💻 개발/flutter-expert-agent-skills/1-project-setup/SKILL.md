# Project Setup Skill

Flutter 프로젝트 초기 설정 및 의존성 구성을 수행합니다.

## Triggers

- "프로젝트 생성", "프로젝트 설정", "flutter init", "flutter create"

---

## Input

| 항목 | 필수 | 설명 |
|------|------|------|
| `projectName` | ✅ | 프로젝트 이름 (snake_case) |
| `packageName` | ✅ | 패키지 이름 (com.example.app) |

---

## Output

### pubspec.yaml

```yaml
name: {project_name}
description: A Flutter application with Clean Architecture.
version: 1.0.0+1

environment:
  sdk: '>=3.5.0 <4.0.0'
  flutter: '>=3.24.0'

dependencies:
  flutter:
    sdk: flutter

  # 상태관리
  flutter_riverpod: ^3.1.0
  riverpod_annotation: ^4.0.0

  # 라우팅
  go_router: ^17.0.1

  # 네트워킹
  dio: ^5.9.0
  retrofit: ^4.9.2

  # 로컬 DB
  drift: ^2.30.0
  sqlite3_flutter_libs: ^0.5.0
  path_provider: ^2.1.0
  path: ^1.9.0

  # 로깅
  talker: ^5.1.9
  talker_flutter: ^5.1.9
  talker_dio_logger: ^5.1.9
  talker_riverpod_logger: ^5.1.9

  # 코드 생성 (annotations)
  freezed_annotation: ^3.0.0
  json_annotation: ^4.9.0

  # DI
  injectable: ^2.7.1
  get_it: ^9.2.0

  # 유틸리티
  fpdart: ^1.2.0
  connectivity_plus: ^6.0.0
  flutter_secure_storage: ^9.2.0

  # 반응형 UI
  flutter_screenutil: ^5.9.3

  # 다국어
  easy_localization: ^3.0.8
  flutter_localizations:
    sdk: flutter

dev_dependencies:
  flutter_test:
    sdk: flutter
  flutter_lints: ^5.0.0
  build_runner: ^2.4.0
  freezed: ^3.2.4
  json_serializable: ^6.11.3
  riverpod_generator: ^4.0.0+1
  go_router_builder: ^4.1.3
  injectable_generator: ^2.12.0
  retrofit_generator: ^10.2.1
  drift_dev: ^2.30.0
  pigeon: ^26.1.5
  mocktail: ^1.0.4
  patrol: ^4.1.0
  alchemist: ^0.13.0
```

### 디렉토리 구조

```
lib/
├── core/
│   ├── design_system/
│   │   ├── tokens/
│   │   ├── atoms/
│   │   ├── molecules/
│   │   ├── organisms/
│   │   └── templates/
│   ├── error/
│   ├── network/
│   ├── database/
│   ├── di/
│   └── utils/
├── features/
├── routes/
└── main.dart

test/
├── unit/
├── widget/
├── golden/
└── helpers/

integration_test/
```

### 실행 명령어

```bash
flutter create --org {org} {project_name}
cd {project_name}
flutter pub get
dart run build_runner build --delete-conflicting-outputs
```

## References

- `_references/ARCHITECTURE-PATTERN.md`
