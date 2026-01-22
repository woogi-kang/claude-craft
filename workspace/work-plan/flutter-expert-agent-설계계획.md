# Flutter Expert Agent 설계 계획서

## 조사 결과 요약

### 1. Riverpod 3.+ 최신 기능 (2025년 9월 릴리즈)

**핵심 신규 기능:**

| 기능 | 설명 |
|------|------|
| **Offline Persistence** | Provider를 로컬 DB에 캐싱하여 앱 재시작 시 복원 |
| **Mutations (Experimental)** | 폼 제출 등 사이드이펙트에 대한 UI 반응 (Idle/Pending/Error/Success) |
| **Automatic Retry** | 실패한 Provider 자동 재시도 (200ms → 6.4s 지수 백오프) |
| **Generic Type Parameters** | `@riverpod T multiply<T extends num>(...)` 제네릭 지원 |
| **Unified Ref** | `Ref<T>`, `FutureProviderRef` 등 통일 → 단일 `Ref` |
| **Pause/Resume** | 리스너 수동 일시정지/재개, TickerMode 기반 자동 일시정지 |
| **ref.mounted** | 비동기 작업 후 Provider 활성 상태 확인 |

**테스팅 유틸:**
- `ProviderContainer.test()` - 테스트 후 자동 dispose
- `NotifierProvider.overrideWithBuild()` - build 로직만 mock
- `WidgetTester.container` - 위젯 테스트에서 컨테이너 접근

**권장 버전:**
```yaml
flutter_riverpod: ^3.1.0
riverpod_annotation: ^4.0.0
riverpod_generator: ^4.0.0+1
```

---

### 2. Clean Architecture (Flutter 공식 + 커뮤니티)

**Flutter 공식 가이드 (MVVM 패턴):**

```
┌─────────────────────────────────────┐
│            UI Layer                  │
│  ┌─────────┐    ┌──────────────┐   │
│  │  View   │◄──►│  ViewModel   │   │
│  │(Widget) │    │(Notifier/Cubit)│  │
│  └─────────┘    └──────┬───────┘   │
└─────────────────────────┼───────────┘
                          │
┌─────────────────────────┼───────────┐
│     Domain Layer (Optional)         │
│         ┌──────────────┐            │
│         │   UseCase    │            │
│         │ (Interactor) │            │
│         └──────┬───────┘            │
└─────────────────┼───────────────────┘
                  │
┌─────────────────┼───────────────────┐
│          Data Layer                  │
│  ┌───────────┐    ┌─────────────┐   │
│  │Repository │◄──►│   Service   │   │
│  │(Interface)│    │(API/Local)  │   │
│  └───────────┘    └─────────────┘   │
└─────────────────────────────────────┘
```

**모듈 구조 (Feature-based):**
```
/lib
├── core/                    # 공통 (errors, utils, constants)
│   ├── error/
│   ├── network/
│   └── utils/
├── features/
│   └── auth/
│       ├── data/           # Repository 구현, DataSource
│       ├── domain/         # Entity, UseCase, Repository 인터페이스
│       └── presentation/   # View, ViewModel(Notifier)
└── main.dart
```

---

### 3. GoRouter 최신 기능

**핵심 기능:**

| 기능 | 설명 |
|------|------|
| **StatefulShellRoute** | 탭 네비게이션 상태 보존 (IndexedStack) |
| **Navigation Guard** | `redirect` 콜백으로 인증 라우팅 |
| **Type-Safe Routes** | `go_router_builder`로 타입 안전 라우팅 |
| **Deep Linking** | 웹/앱 딥링크 자동 지원 |
| **Nested Navigation** | ShellRoute로 중첩 네비게이션 |

**Type-Safe Route 예시:**
```dart
@TypedGoRoute<HomeRoute>(path: '/')
class HomeRoute extends GoRouteData {
  const HomeRoute();
}

@TypedGoRoute<UserRoute>(path: '/user/:id')
class UserRoute extends GoRouteData {
  final int id;
  const UserRoute({required this.id});
}

// 사용
const HomeRoute().go(context);
UserRoute(id: 123).push(context);
```

---

### 4. TDD / 테스트 전략

**Testing Pyramid:**

```
                    ╱╲
                   ╱  ╲      E2E (Patrol)
                  ╱────╲     5-10%
                 ╱      ╲
                ╱────────╲   Golden Tests
               ╱          ╲  10-15%
              ╱────────────╲
             ╱   Widget    ╲ 15-20%
            ╱────────────────╲
           ╱      Unit       ╲ 60-70%
          ╱────────────────────╲
```

**테스트 유형별 도구:**

| 유형 | 패키지 | 용도 |
|------|--------|------|
| **Unit** | `flutter_test`, `mocktail` | 비즈니스 로직 격리 테스트 |
| **Widget** | `flutter_test` | 위젯 렌더링/상호작용 테스트 |
| **Golden** | `alchemist`, `golden_toolkit` | 시각적 회귀 테스트 |
| **E2E** | `patrol` | 네이티브 UI 상호작용 테스트 |

**Patrol 4.0 특징:**
- 네이티브 권한 다이얼로그 처리
- 푸시 알림 상호작용
- WebView OAuth 테스트
- Hot Restart로 빠른 테스트 개발
- 웹 테스트 지원 (신규)
- Firebase Test Lab, BrowserStack 연동

**Riverpod 테스트 패턴:**
```dart
test('AsyncNotifier test', () async {
  final container = ProviderContainer.test(
    overrides: [
      someServiceProvider.overrideWithValue(mockService),
    ],
  );

  await container.read(myAsyncNotifierProvider.future);
  expect(container.read(myAsyncNotifierProvider).value, expectedValue);
});
```

---

### 5. Dart MCP (Model Context Protocol)

**사용 가능한 MCP 서버:**

| 서버 | 기능 |
|------|------|
| **Dart** | Flutter 명령 실행, 패키지 추가, 포맷터, 분석기, 스크린샷, Hot Restart |
| **Git** | 브랜치 관리, 커밋, diff, 상태 확인 |
| **GitHub** | 이슈/PR 관리, 브랜치 생성 |
| **Figma (Framelink)** | 디자인 읽기, UI 구현 생성 |
| **iOS Simulator** | 시뮬레이터 생성, 스크린샷, GPS 모킹 |
| **Fetch** | URL에서 문서/API 스키마 가져오기 |

**Dart MCP 서버 (실험적):**
- Dart 팀에서 개발 중
- pub.dev에서 사용 가능
- Flutter 워크스페이스 내 명령 실행 지원

---

### 6. 네트워크 통신 (Dio + Retrofit)

**Dio + Retrofit 조합의 장점:**
- **Type-Safe API Client**: 어노테이션 기반으로 컴파일 타임 에러 감지
- **Interceptors**: 토큰 주입, 로깅, 에러 핸들링 중앙 관리
- **Code Generation**: 보일러플레이트 자동 생성

**권장 버전:**
```yaml
dependencies:
  dio: ^5.9.0
  retrofit: ^4.9.2

dev_dependencies:
  retrofit_generator: ^10.0.1
```

**Retrofit 사용 예시:**
```dart
@RestApi(baseUrl: 'https://api.example.com')
abstract class ApiClient {
  factory ApiClient(Dio dio, {String baseUrl}) = _ApiClient;

  @GET('/users/{id}')
  Future<User> getUser(@Path('id') String id);

  @POST('/users')
  Future<User> createUser(@Body() CreateUserRequest request);

  @GET('/users')
  Future<List<User>> getUsers(@Query('page') int page);
}
```

**Dio Interceptor 패턴:**
```dart
class AuthInterceptor extends Interceptor {
  @override
  void onRequest(RequestOptions options, RequestInterceptorHandler handler) {
    final token = getIt<TokenStorage>().accessToken;
    if (token != null) {
      options.headers['Authorization'] = 'Bearer $token';
    }
    handler.next(options);
  }
}
```

---

### 7. 로컬 스토리지 (Drift 선택)

**Drift vs Hive 비교:**

| 항목 | Drift | Hive |
|------|-------|------|
| **타입** | SQL (SQLite ORM) | NoSQL (Key-Value) |
| **타입 안전성** | 컴파일 타임 체크 | 기본적 |
| **복잡한 쿼리** | Full SQL 지원 | 제한적 |
| **관계형 데이터** | 완벽 지원 | 미지원 |
| **마이그레이션** | 스키마 마이그레이션 지원 | 제한적 |
| **대용량 데이터** | 우수 | 메모리 캐싱으로 빠르지만 한계 |
| **유지보수** | 활발 | **⚠️ Deprecated 예정** |

**결론: Drift 선택**
- Hive는 deprecated 예정이며, 대안인 Isar도 유지보수 중단 상태
- Drift는 타입 안전성, SQL 지원, 활발한 유지보수로 권장

**권장 버전:**
```yaml
dependencies:
  drift: ^2.30.0
  sqlite3_flutter_libs: ^0.5.0
  path_provider: ^2.1.0
  path: ^1.9.0

dev_dependencies:
  drift_dev: ^2.30.0
```

**Drift 사용 예시:**
```dart
// 테이블 정의
class Users extends Table {
  IntColumn get id => integer().autoIncrement()();
  TextColumn get name => text().withLength(min: 1, max: 50)();
  TextColumn get email => text().nullable()();
  DateTimeColumn get createdAt => dateTime().withDefault(currentDateAndTime)();
}

// Database 클래스
@DriftDatabase(tables: [Users])
class AppDatabase extends _$AppDatabase {
  AppDatabase() : super(_openConnection());

  @override
  int get schemaVersion => 1;

  // 쿼리 메서드
  Future<List<User>> getAllUsers() => select(users).get();
  Stream<List<User>> watchAllUsers() => select(users).watch();
  Future<int> insertUser(UsersCompanion user) => into(users).insert(user);
}
```

---

### 8. Platform Channel (Pigeon)

**Pigeon 장점:**
- **Type-Safe**: Flutter ↔ Native 간 타입 안전 통신
- **Code Generation**: 보일러플레이트 자동 생성
- **Multi-Platform**: iOS (Swift/ObjC), Android (Kotlin/Java), Windows, Linux 지원

**권장 버전:**
```yaml
dev_dependencies:
  pigeon: ^26.1.5
```

**Pigeon 사용 예시:**

```dart
// pigeons/messages.dart
import 'package:pigeon/pigeon.dart';

class DeviceInfo {
  String? model;
  String? osVersion;
  int? batteryLevel;
}

@HostApi()
abstract class DeviceApi {
  DeviceInfo getDeviceInfo();
  void openSettings();
}

@FlutterApi()
abstract class FlutterNotificationApi {
  void onBatteryLevelChanged(int level);
}
```

**코드 생성:**
```bash
dart run pigeon \
  --input pigeons/messages.dart \
  --dart_out lib/src/generated/messages.g.dart \
  --kotlin_out android/app/src/main/kotlin/Messages.g.kt \
  --swift_out ios/Runner/Messages.g.swift
```

---

### 9. Logger (Talker)

**Talker 생태계:**

| 패키지 | 용도 |
|--------|------|
| **talker** | Core 로깅 |
| **talker_flutter** | Flutter UI 로그 뷰어 |
| **talker_dio_logger** | Dio HTTP 요청/응답 로깅 |
| **talker_riverpod_logger** | Riverpod 상태 변화 로깅 |

**권장 버전:**
```yaml
dependencies:
  talker: ^5.1.9
  talker_flutter: ^5.1.9
  talker_dio_logger: ^5.1.9
  talker_riverpod_logger: ^5.1.9
```

**Talker 설정 예시:**
```dart
// 전역 Talker 인스턴스
final talker = TalkerFlutter.init(
  settings: TalkerSettings(
    maxHistoryItems: 1000,
    useConsoleLogs: true,
  ),
);

// Dio에 Talker 로거 연결
final dio = Dio()
  ..interceptors.add(
    TalkerDioLogger(
      talker: talker,
      settings: TalkerDioLoggerSettings(
        printRequestHeaders: true,
        printResponseHeaders: true,
        printResponseMessage: true,
      ),
    ),
  );

// Riverpod에 Talker 로거 연결
final container = ProviderContainer(
  observers: [
    TalkerRiverpodObserver(talker: talker),
  ],
);

// 앱에서 로그 뷰어 열기
TalkerScreen(talker: talker);
```

---

### 10. 추가 권장 도구

**코드 생성:**

| 패키지 | 용도 |
|--------|------|
| **freezed** | Immutable 데이터 클래스, 유니온, JSON 직렬화 |
| **riverpod_generator** | Provider 코드 생성 |
| **go_router_builder** | 타입 안전 라우트 생성 |
| **injectable** | DI 코드 생성 (get_it 기반) |
| **retrofit_generator** | API Client 코드 생성 |
| **drift_dev** | Database 코드 생성 |

**freezed 예시:**
```dart
@freezed
class User with _$User {
  const factory User({
    required String id,
    required String name,
    String? email,
  }) = _User;

  factory User.fromJson(Map<String, dynamic> json) => _$UserFromJson(json);
}
```

---

### 11. Atomic Design 패턴 (위젯 구조)

**Brad Frost의 Atomic Design**은 UI를 계층적이고 모듈화된 방식으로 구축하는 방법론입니다.
화학의 원자-분자-유기체 개념을 차용하여 컴포넌트를 체계적으로 조직합니다.

#### 5단계 계층 구조

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
│    최소 단위 (Text, Icon, Container, Button)                     │
├─────────────────────────────────────────────────────────────────┤
│                        TOKENS                                    │
│    디자인 토큰 (Colors, Typography, Spacing, Radius)             │
└─────────────────────────────────────────────────────────────────┘
```

#### 각 계층 상세

| 계층 | 정의 | Flutter 예시 | 상태 |
|------|------|-------------|------|
| **Tokens** | 디자인 시스템의 원시값 (색상, 타이포, 간격) | `AppColors`, `AppTypography`, `AppSpacing` | - |
| **Atoms** | 더 이상 분해할 수 없는 기본 위젯 | `AppText`, `AppIcon`, `AppButton`, `AppInput` | StatelessWidget |
| **Molecules** | Atoms 조합, 단일 책임 | `SearchBar`, `LabeledTextField`, `AvatarWithName` | Stateless/Stateful |
| **Organisms** | Molecules + Atoms 조합, 복합 기능 | `AppHeader`, `ProductCard`, `LoginForm`, `BottomNav` | Stateful |
| **Templates** | 페이지 레이아웃 구조 (슬롯) | `MainTemplate`, `AuthTemplate`, `DashboardTemplate` | StatelessWidget |
| **Pages** | 템플릿 + 실제 데이터 | `HomePage`, `ProfilePage`, `SettingsPage` | ConsumerWidget |

#### 폴더 구조

```
lib/
├── core/
│   ├── design_system/
│   │   ├── tokens/
│   │   │   ├── colors.dart           # AppColors
│   │   │   ├── typography.dart       # AppTypography
│   │   │   ├── spacing.dart          # AppSpacing
│   │   │   ├── radius.dart           # AppRadius
│   │   │   ├── shadows.dart          # AppShadows
│   │   │   └── index.dart            # barrel export
│   │   │
│   │   ├── atoms/
│   │   │   ├── app_text.dart
│   │   │   ├── app_icon.dart
│   │   │   ├── app_button.dart
│   │   │   ├── app_input.dart
│   │   │   ├── app_image.dart
│   │   │   ├── app_spacer.dart
│   │   │   ├── app_divider.dart
│   │   │   └── index.dart
│   │   │
│   │   ├── molecules/
│   │   │   ├── search_bar.dart
│   │   │   ├── labeled_input.dart
│   │   │   ├── icon_text_button.dart
│   │   │   ├── avatar_with_name.dart
│   │   │   ├── rating_stars.dart
│   │   │   └── index.dart
│   │   │
│   │   ├── organisms/
│   │   │   ├── app_header.dart
│   │   │   ├── app_bottom_nav.dart
│   │   │   ├── app_drawer.dart
│   │   │   ├── product_card.dart
│   │   │   ├── login_form.dart
│   │   │   ├── comment_section.dart
│   │   │   └── index.dart
│   │   │
│   │   └── templates/
│   │       ├── main_template.dart
│   │       ├── auth_template.dart
│   │       ├── dashboard_template.dart
│   │       └── index.dart
│   │
│   └── theme/
│       ├── app_theme.dart            # ThemeData 통합
│       ├── light_theme.dart
│       └── dark_theme.dart
│
└── features/
    └── home/
        └── presentation/
            └── pages/
                └── home_page.dart    # Template + 실제 데이터
```

#### Tokens (디자인 토큰) 예시

```dart
// tokens/colors.dart
abstract class AppColors {
  // Primary
  static const Color primary = Color(0xFF6366F1);
  static const Color primaryLight = Color(0xFF818CF8);
  static const Color primaryDark = Color(0xFF4F46E5);

  // Neutral
  static const Color background = Color(0xFFFAFAFA);
  static const Color surface = Color(0xFFFFFFFF);
  static const Color textPrimary = Color(0xFF1F2937);
  static const Color textSecondary = Color(0xFF6B7280);

  // Semantic
  static const Color success = Color(0xFF10B981);
  static const Color warning = Color(0xFFF59E0B);
  static const Color error = Color(0xFFEF4444);
  static const Color info = Color(0xFF3B82F6);
}

// tokens/spacing.dart
abstract class AppSpacing {
  static const double xs = 4.0;
  static const double sm = 8.0;
  static const double md = 16.0;
  static const double lg = 24.0;
  static const double xl = 32.0;
  static const double xxl = 48.0;
}

// tokens/typography.dart
abstract class AppTypography {
  static const String fontFamily = 'Pretendard';

  static const TextStyle displayLarge = TextStyle(
    fontFamily: fontFamily,
    fontSize: 57,
    fontWeight: FontWeight.w400,
    letterSpacing: -0.25,
  );

  static const TextStyle headlineLarge = TextStyle(
    fontFamily: fontFamily,
    fontSize: 32,
    fontWeight: FontWeight.w600,
  );

  static const TextStyle titleLarge = TextStyle(
    fontFamily: fontFamily,
    fontSize: 22,
    fontWeight: FontWeight.w500,
  );

  static const TextStyle bodyLarge = TextStyle(
    fontFamily: fontFamily,
    fontSize: 16,
    fontWeight: FontWeight.w400,
  );

  static const TextStyle labelLarge = TextStyle(
    fontFamily: fontFamily,
    fontSize: 14,
    fontWeight: FontWeight.w500,
  );
}

// tokens/radius.dart
abstract class AppRadius {
  static const double none = 0;
  static const double sm = 4.0;
  static const double md = 8.0;
  static const double lg = 12.0;
  static const double xl = 16.0;
  static const double full = 9999.0;
}
```

#### Atoms 예시

```dart
// atoms/app_button.dart
enum AppButtonVariant { primary, secondary, outline, ghost }
enum AppButtonSize { sm, md, lg }

class AppButton extends StatelessWidget {
  const AppButton({
    super.key,
    required this.label,
    required this.onPressed,
    this.variant = AppButtonVariant.primary,
    this.size = AppButtonSize.md,
    this.icon,
    this.isLoading = false,
    this.isDisabled = false,
  });

  final String label;
  final VoidCallback? onPressed;
  final AppButtonVariant variant;
  final AppButtonSize size;
  final IconData? icon;
  final bool isLoading;
  final bool isDisabled;

  @override
  Widget build(BuildContext context) {
    return SizedBox(
      height: _getHeight(),
      child: ElevatedButton(
        onPressed: isDisabled || isLoading ? null : onPressed,
        style: _getButtonStyle(),
        child: isLoading
            ? SizedBox(
                width: 20,
                height: 20,
                child: CircularProgressIndicator(strokeWidth: 2),
              )
            : Row(
                mainAxisSize: MainAxisSize.min,
                children: [
                  if (icon != null) ...[
                    Icon(icon, size: _getIconSize()),
                    SizedBox(width: AppSpacing.sm),
                  ],
                  Text(label, style: _getTextStyle()),
                ],
              ),
      ),
    );
  }

  double _getHeight() => switch (size) {
    AppButtonSize.sm => 32,
    AppButtonSize.md => 40,
    AppButtonSize.lg => 48,
  };

  double _getIconSize() => switch (size) {
    AppButtonSize.sm => 16,
    AppButtonSize.md => 20,
    AppButtonSize.lg => 24,
  };

  // ... _getButtonStyle(), _getTextStyle() 구현
}

// atoms/app_text.dart
enum AppTextVariant { display, headline, title, body, label, caption }

class AppText extends StatelessWidget {
  const AppText(
    this.text, {
    super.key,
    this.variant = AppTextVariant.body,
    this.color,
    this.maxLines,
    this.overflow,
    this.textAlign,
  });

  final String text;
  final AppTextVariant variant;
  final Color? color;
  final int? maxLines;
  final TextOverflow? overflow;
  final TextAlign? textAlign;

  @override
  Widget build(BuildContext context) {
    return Text(
      text,
      style: _getTextStyle().copyWith(color: color),
      maxLines: maxLines,
      overflow: overflow,
      textAlign: textAlign,
    );
  }

  TextStyle _getTextStyle() => switch (variant) {
    AppTextVariant.display => AppTypography.displayLarge,
    AppTextVariant.headline => AppTypography.headlineLarge,
    AppTextVariant.title => AppTypography.titleLarge,
    AppTextVariant.body => AppTypography.bodyLarge,
    AppTextVariant.label => AppTypography.labelLarge,
    AppTextVariant.caption => AppTypography.bodySmall,
  };
}
```

#### Molecules 예시

```dart
// molecules/search_bar.dart
class SearchBar extends StatelessWidget {
  const SearchBar({
    super.key,
    required this.controller,
    this.hintText = '검색어를 입력하세요',
    this.onChanged,
    this.onSubmitted,
    this.onClear,
  });

  final TextEditingController controller;
  final String hintText;
  final ValueChanged<String>? onChanged;
  final ValueChanged<String>? onSubmitted;
  final VoidCallback? onClear;

  @override
  Widget build(BuildContext context) {
    return Row(
      children: [
        // Atom: Icon
        AppIcon(Icons.search, color: AppColors.textSecondary),
        SizedBox(width: AppSpacing.sm),
        // Atom: Input
        Expanded(
          child: AppInput(
            controller: controller,
            hintText: hintText,
            onChanged: onChanged,
            onSubmitted: onSubmitted,
          ),
        ),
        // Atom: IconButton (clear)
        if (controller.text.isNotEmpty)
          AppIconButton(
            icon: Icons.close,
            onPressed: onClear,
            size: AppButtonSize.sm,
          ),
      ],
    );
  }
}

// molecules/labeled_input.dart
class LabeledInput extends StatelessWidget {
  const LabeledInput({
    super.key,
    required this.label,
    required this.controller,
    this.hintText,
    this.errorText,
    this.isRequired = false,
    this.obscureText = false,
  });

  final String label;
  final TextEditingController controller;
  final String? hintText;
  final String? errorText;
  final bool isRequired;
  final bool obscureText;

  @override
  Widget build(BuildContext context) {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        // Atoms: Label + Required indicator
        Row(
          children: [
            AppText(label, variant: AppTextVariant.label),
            if (isRequired)
              AppText(' *', variant: AppTextVariant.label, color: AppColors.error),
          ],
        ),
        SizedBox(height: AppSpacing.xs),
        // Atom: Input
        AppInput(
          controller: controller,
          hintText: hintText,
          obscureText: obscureText,
          hasError: errorText != null,
        ),
        // Atom: Error text
        if (errorText != null) ...[
          SizedBox(height: AppSpacing.xs),
          AppText(errorText!, variant: AppTextVariant.caption, color: AppColors.error),
        ],
      ],
    );
  }
}
```

#### Organisms 예시

```dart
// organisms/login_form.dart
class LoginForm extends StatefulWidget {
  const LoginForm({
    super.key,
    required this.onSubmit,
    this.isLoading = false,
  });

  final void Function(String email, String password) onSubmit;
  final bool isLoading;

  @override
  State<LoginForm> createState() => _LoginFormState();
}

class _LoginFormState extends State<LoginForm> {
  final _emailController = TextEditingController();
  final _passwordController = TextEditingController();
  String? _emailError;
  String? _passwordError;

  @override
  Widget build(BuildContext context) {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.stretch,
      children: [
        // Molecule: LabeledInput (Email)
        LabeledInput(
          label: '이메일',
          controller: _emailController,
          hintText: 'example@email.com',
          errorText: _emailError,
          isRequired: true,
        ),
        SizedBox(height: AppSpacing.md),

        // Molecule: LabeledInput (Password)
        LabeledInput(
          label: '비밀번호',
          controller: _passwordController,
          hintText: '비밀번호를 입력하세요',
          errorText: _passwordError,
          isRequired: true,
          obscureText: true,
        ),
        SizedBox(height: AppSpacing.lg),

        // Atom: Button
        AppButton(
          label: '로그인',
          onPressed: _handleSubmit,
          isLoading: widget.isLoading,
        ),
        SizedBox(height: AppSpacing.md),

        // Molecule: TextButton (Forgot Password)
        Center(
          child: AppTextButton(
            label: '비밀번호를 잊으셨나요?',
            onPressed: () {},
          ),
        ),
      ],
    );
  }

  void _handleSubmit() {
    // Validation logic
    widget.onSubmit(_emailController.text, _passwordController.text);
  }
}

// organisms/app_header.dart
class AppHeader extends StatelessWidget {
  const AppHeader({
    super.key,
    required this.title,
    this.showBackButton = false,
    this.actions = const [],
    this.onBack,
  });

  final String title;
  final bool showBackButton;
  final List<Widget> actions;
  final VoidCallback? onBack;

  @override
  Widget build(BuildContext context) {
    return Container(
      padding: EdgeInsets.symmetric(
        horizontal: AppSpacing.md,
        vertical: AppSpacing.sm,
      ),
      decoration: BoxDecoration(
        color: AppColors.surface,
        boxShadow: [AppShadows.sm],
      ),
      child: Row(
        children: [
          // Atom: Back Button
          if (showBackButton)
            AppIconButton(
              icon: Icons.arrow_back,
              onPressed: onBack ?? () => Navigator.pop(context),
            ),

          // Atom: Title
          Expanded(
            child: AppText(
              title,
              variant: AppTextVariant.title,
              textAlign: showBackButton ? TextAlign.center : TextAlign.start,
            ),
          ),

          // Actions
          ...actions,
        ],
      ),
    );
  }
}
```

#### Templates 예시

```dart
// templates/main_template.dart
class MainTemplate extends StatelessWidget {
  const MainTemplate({
    super.key,
    required this.body,
    this.title,
    this.showHeader = true,
    this.showBottomNav = true,
    this.floatingActionButton,
    this.headerActions = const [],
  });

  final Widget body;
  final String? title;
  final bool showHeader;
  final bool showBottomNav;
  final Widget? floatingActionButton;
  final List<Widget> headerActions;

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: SafeArea(
        child: Column(
          children: [
            // Organism: Header
            if (showHeader && title != null)
              AppHeader(
                title: title!,
                actions: headerActions,
              ),

            // Body Slot
            Expanded(child: body),
          ],
        ),
      ),

      // Organism: Bottom Navigation
      bottomNavigationBar: showBottomNav ? const AppBottomNav() : null,

      floatingActionButton: floatingActionButton,
    );
  }
}

// templates/auth_template.dart
class AuthTemplate extends StatelessWidget {
  const AuthTemplate({
    super.key,
    required this.child,
    this.title,
    this.subtitle,
  });

  final Widget child;
  final String? title;
  final String? subtitle;

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: SafeArea(
        child: SingleChildScrollView(
          padding: EdgeInsets.all(AppSpacing.lg),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.stretch,
            children: [
              SizedBox(height: AppSpacing.xxl),

              // Atom: Logo
              Center(child: AppLogo(size: 80)),
              SizedBox(height: AppSpacing.xl),

              // Atoms: Title & Subtitle
              if (title != null) ...[
                AppText(title!, variant: AppTextVariant.headline, textAlign: TextAlign.center),
                SizedBox(height: AppSpacing.sm),
              ],
              if (subtitle != null) ...[
                AppText(subtitle!, variant: AppTextVariant.body, color: AppColors.textSecondary, textAlign: TextAlign.center),
                SizedBox(height: AppSpacing.xl),
              ],

              // Content Slot
              child,
            ],
          ),
        ),
      ),
    );
  }
}
```

#### Pages 예시 (with Riverpod)

```dart
// features/auth/presentation/pages/login_page.dart
class LoginPage extends ConsumerWidget {
  const LoginPage({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final authState = ref.watch(authNotifierProvider);

    return AuthTemplate(
      title: '로그인',
      subtitle: '계정에 로그인하세요',
      child: LoginForm(
        onSubmit: (email, password) {
          ref.read(authNotifierProvider.notifier).login(email, password);
        },
        isLoading: authState.isLoading,
      ),
    );
  }
}
```

#### Atomic Design 적용 가이드라인

**분류 기준:**

| 질문 | Yes → | No → |
|------|-------|------|
| 더 쪼갤 수 있나? | 상위 계층 | Atom |
| 단일 책임인가? | Molecule | Organism |
| 레이아웃 구조인가? | Template | Organism |
| 실제 데이터가 있나? | Page | Template |

**네이밍 규칙:**
- Atoms: `App` 접두사 (`AppButton`, `AppText`, `AppInput`)
- Molecules: 기능 설명 (`SearchBar`, `LabeledInput`)
- Organisms: 컴포넌트명 (`LoginForm`, `ProductCard`)
- Templates: `Template` 접미사 (`MainTemplate`, `AuthTemplate`)
- Pages: `Page` 접미사 (`HomePage`, `LoginPage`)

**Atomic Design 장점:**
- **재사용성**: 컴포넌트를 조합하여 새 화면 빠르게 구축
- **일관성**: 디자인 토큰으로 통일된 UI
- **테스트 용이**: 작은 단위로 분리되어 단위 테스트 쉬움
- **유지보수**: 변경 시 영향 범위 최소화
- **협업**: 디자이너-개발자 간 공통 언어

---

## Flutter Expert Agent 설계

### Agent 개요

```yaml
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
  - "riverpod"
  - "flutter expert"
```

### 핵심 원칙

1. **Clean Architecture**: 관심사 분리, 테스트 가능한 구조
2. **Atomic Design**: Tokens → Atoms → Molecules → Organisms → Templates → Pages
3. **TDD First**: 테스트 주도 개발, Red-Green-Refactor
4. **Riverpod 3**: 최신 상태관리, Code Generation 활용
5. **Type Safety**: GoRouter Builder, Freezed로 타입 안전성 보장
6. **실용적 접근**: 과도한 추상화 지양, 필요한 만큼만

---

### Skills 구조 (21개)

```
.claude/skills/💻 개발/flutter-expert-agent-skills/
│
├── Phase 1: 설계 (Architecture)
│   ├── 1-project-setup/         # 프로젝트 초기 설정
│   ├── 2-architecture/          # Clean Architecture 설계
│   ├── 3-design-system/         # Atomic Design + Design Tokens
│   └── 4-feature-design/        # Feature 단위 설계
│
├── Phase 2: 구현 (Implementation)
│   ├── 5-entity/                # Domain Entity (freezed)
│   ├── 6-repository/            # Repository 패턴 구현
│   ├── 7-usecase/               # UseCase/Interactor
│   ├── 8-notifier/              # Riverpod Notifier 구현
│   ├── 9-view/                  # UI Widget (Atomic 계층별)
│   ├── 10-routing/              # GoRouter 설정
│   ├── 11-network/              # Dio + Retrofit API Client
│   ├── 12-database/             # Drift 로컬 DB
│   └── 13-platform-channel/     # Pigeon 네이티브 통신
│
├── Phase 3: 테스트 (Testing)
│   ├── 14-unit-test/            # Unit Test (mocktail)
│   ├── 15-widget-test/          # Widget Test
│   ├── 16-golden-test/          # Golden Test (alchemist)
│   └── 17-e2e-test/             # E2E Test (patrol)
│
├── Phase 4: 최적화 (Optimization)
│   ├── 18-performance/          # 성능 최적화
│   └── 19-refactor/             # 리팩토링
│
└── Phase 5: 검증 (Validation)
    ├── 20-logging/              # Talker 로깅 설정
    └── 21-code-review/          # 코드 리뷰 & 품질 검증
```

---

### 워크플로우

```
[사용자 요청]
      │
      ▼
┌─────────────────────────────────────────────────────────────┐
│                  Phase 1: 설계 (Architecture)                │
│  ┌────────────┐  ┌────────────┐  ┌────────────────┐        │
│  │  Project   │→ │Architecture│→ │Feature Design  │        │
│  │   Setup    │  │  (Clean)   │  │(Domain 모델링) │        │
│  └────────────┘  └────────────┘  └────────────────┘        │
└─────────────────────────────────────────────────────────────┘
      │
      ▼
┌─────────────────────────────────────────────────────────────┐
│                  Phase 2: 구현 (Implementation)              │
│                                                              │
│     TDD Cycle (Feature 단위 반복)                            │
│  ┌──────────────────────────────────────────────────────┐   │
│  │                                                       │   │
│  │  ┌─────────┐   ┌─────────┐   ┌─────────┐            │   │
│  │  │  Test   │──▶│  Code   │──▶│Refactor │──┐         │   │
│  │  │  (Red)  │   │ (Green) │   │         │  │         │   │
│  │  └─────────┘   └─────────┘   └─────────┘  │         │   │
│  │       ▲                                    │         │   │
│  │       └────────────────────────────────────┘         │   │
│  └──────────────────────────────────────────────────────┘   │
│                                                              │
│  구현 순서:                                                   │
│  Entity → Repository → UseCase → Notifier → View → Routing  │
│                                                              │
└─────────────────────────────────────────────────────────────┘
      │
      ▼
┌─────────────────────────────────────────────────────────────┐
│                  Phase 3: 테스트 (Testing)                   │
│  ┌──────────┐  ┌────────────┐  ┌────────┐  ┌──────────┐   │
│  │  Unit    │→ │  Widget    │→ │ Golden │→ │   E2E    │   │
│  │  Test    │  │   Test     │  │  Test  │  │ (Patrol) │   │
│  └──────────┘  └────────────┘  └────────┘  └──────────┘   │
└─────────────────────────────────────────────────────────────┘
      │
      ▼
┌─────────────────────────────────────────────────────────────┐
│                  Phase 4 & 5: 최적화 & 검증                   │
│  ┌────────────┐  ┌────────────┐  ┌────────────┐            │
│  │Performance │→ │  Refactor  │→ │Code Review │            │
│  │Optimization│  │            │  │  & QA      │            │
│  └────────────┘  └────────────┘  └────────────┘            │
└─────────────────────────────────────────────────────────────┘
```

---

### Skill 상세 정의

#### Phase 1: 설계

##### 1-project-setup
```yaml
name: project-setup
description: Flutter 프로젝트 초기 설정 및 의존성 구성
triggers:
  - "프로젝트 생성"
  - "flutter init"
  - "프로젝트 설정"

output:
  - pubspec.yaml (의존성 구성)
  - analysis_options.yaml (린트 규칙)
  - 디렉토리 구조 생성
  - .vscode/settings.json

dependencies:
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

  # 로거
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

  # 유틸
  fpdart: ^1.2.0      # Functional programming

dev_dependencies:
  # 코드 생성
  build_runner: ^2.4.0
  freezed: ^3.2.4
  json_serializable: ^6.10.0
  riverpod_generator: ^4.0.0+1
  go_router_builder: ^2.7.0
  injectable_generator: ^2.7.0
  retrofit_generator: ^10.0.1
  drift_dev: ^2.30.0

  # Platform Channel
  pigeon: ^26.1.5

  # 테스팅
  mocktail: ^1.0.4
  patrol: ^4.1.0
  alchemist: ^0.13.0
```

##### 2-architecture
```yaml
name: architecture
description: Clean Architecture 기반 프로젝트 구조 설계
triggers:
  - "아키텍처 설계"
  - "구조 설계"
  - "clean architecture"

output:
  - architecture-decision-record.md (ADR)
  - 디렉토리 구조 생성
  - 공통 모듈 설정 (core/)

structure:
  lib/
    core/
      error/
        exceptions.dart
        failures.dart
      network/
        api_client.dart
        network_info.dart
      utils/
        extensions.dart
        constants.dart
      di/
        injection.dart
    features/
      # feature별 data/domain/presentation
    main.dart
```

##### 3-design-system
```yaml
name: design-system
description: Atomic Design 기반 디자인 시스템 및 토큰 설정
triggers:
  - "디자인 시스템"
  - "atomic design"
  - "design tokens"
  - "위젯 구조"

components:
  tokens:
    - colors.dart         # AppColors
    - typography.dart     # AppTypography
    - spacing.dart        # AppSpacing
    - radius.dart         # AppRadius
    - shadows.dart        # AppShadows

  atoms:
    - app_text.dart       # 텍스트 위젯
    - app_button.dart     # 버튼 위젯
    - app_input.dart      # 입력 위젯
    - app_icon.dart       # 아이콘 위젯
    - app_image.dart      # 이미지 위젯
    - app_spacer.dart     # 간격 위젯
    - app_divider.dart    # 구분선 위젯

  molecules:
    - search_bar.dart     # 검색바 (Icon + Input + Button)
    - labeled_input.dart  # 라벨 입력 (Label + Input + Error)
    - avatar_with_name.dart

  organisms:
    - app_header.dart     # 앱 헤더
    - app_bottom_nav.dart # 하단 네비게이션
    - login_form.dart     # 로그인 폼
    - product_card.dart   # 상품 카드

  templates:
    - main_template.dart  # 메인 레이아웃
    - auth_template.dart  # 인증 레이아웃

hierarchy:
  - Tokens: 디자인 원시값 (static const)
  - Atoms: 최소 단위, StatelessWidget
  - Molecules: Atoms 조합, 단일 책임
  - Organisms: 복합 기능, Stateful 가능
  - Templates: 레이아웃 뼈대, 슬롯 구조
  - Pages: 템플릿 + 실제 데이터 (ConsumerWidget)

naming:
  atoms: "App" 접두사 (AppButton, AppText)
  molecules: 기능 설명 (SearchBar, LabeledInput)
  organisms: 컴포넌트명 (LoginForm, ProductCard)
  templates: "Template" 접미사 (MainTemplate)
  pages: "Page" 접미사 (HomePage)
```

##### 4-feature-design
```yaml
name: feature-design
description: 개별 Feature 도메인 모델링 및 설계
triggers:
  - "기능 설계"
  - "feature 설계"
  - "도메인 설계"

output:
  - feature-design.md (설계 문서)
  - Entity 목록
  - UseCase 목록
  - Repository 인터페이스
  - UI 흐름도
```

#### Phase 2: 구현

##### 5-entity
```yaml
name: entity
description: Freezed 기반 Domain Entity 생성
triggers:
  - "entity 생성"
  - "모델 생성"
  - "데이터 클래스"

template: |
  @freezed
  class {EntityName} with _${EntityName} {
    const factory {EntityName}({
      required String id,
      // ... properties
    }) = _{EntityName};

    factory {EntityName}.fromJson(Map<String, dynamic> json) =>
      _${EntityName}FromJson(json);
  }
```

##### 6-repository
```yaml
name: repository
description: Repository 패턴 구현 (Interface + Implementation)
triggers:
  - "repository 생성"
  - "데이터 레이어"

pattern:
  domain: Repository 인터페이스 (abstract class)
  data: Repository 구현체 (DataSource 의존)
```

##### 7-usecase
```yaml
name: usecase
description: UseCase/Interactor 구현
triggers:
  - "usecase 생성"
  - "비즈니스 로직"

pattern:
  - 단일 책임 (하나의 비즈니스 액션)
  - Either<Failure, Success> 반환
  - Repository 의존
```

##### 8-notifier
```yaml
name: notifier
description: Riverpod 3 Notifier 구현
triggers:
  - "notifier 생성"
  - "상태관리"
  - "riverpod"

patterns:
  - Notifier (동기)
  - AsyncNotifier (비동기)
  - StreamNotifier (스트림)
  - FamilyNotifier (파라미터)

features:
  - @riverpod 코드 생성 활용
  - Mutations 패턴 (폼 제출 등)
  - Offline Persistence (필요시)
```

##### 9-view
```yaml
name: view
description: Flutter Widget/View 구현
triggers:
  - "화면 구현"
  - "UI 구현"
  - "widget"

patterns:
  - ConsumerWidget (Riverpod 연동)
  - HookConsumerWidget (hooks 사용시)
  - 상태별 UI (Loading, Error, Data)
```

##### 10-routing
```yaml
name: routing
description: GoRouter 라우팅 설정
triggers:
  - "라우팅 설정"
  - "go_router"
  - "네비게이션"

patterns:
  - Type-safe routes (go_router_builder)
  - StatefulShellRoute (탭 네비게이션)
  - Navigation guards (redirect)
  - Deep linking
```

##### 11-network
```yaml
name: network
description: Dio + Retrofit 기반 네트워크 레이어 구현
triggers:
  - "API 클라이언트"
  - "네트워크 설정"
  - "retrofit"
  - "dio"

components:
  - ApiClient (Retrofit interface)
  - Dio 설정 (BaseOptions, Interceptors)
  - AuthInterceptor (토큰 주입)
  - ErrorInterceptor (에러 핸들링)
  - TalkerDioLogger 연동

patterns:
  - @RestApi 어노테이션
  - @GET, @POST, @PUT, @DELETE
  - @Path, @Query, @Body
  - Request/Response 모델 (Freezed)
```

##### 12-database
```yaml
name: database
description: Drift 로컬 데이터베이스 구현
triggers:
  - "로컬 DB"
  - "drift"
  - "sqlite"
  - "오프라인 저장"

components:
  - Table 정의 (extends Table)
  - Database 클래스 (@DriftDatabase)
  - DAO (Data Access Object)
  - Migration 전략

patterns:
  - Stream 기반 반응형 쿼리 (watch)
  - Transaction 처리
  - 복잡한 JOIN 쿼리
  - 스키마 마이그레이션
```

##### 13-platform-channel
```yaml
name: platform-channel
description: Pigeon 기반 네이티브 플랫폼 통신
triggers:
  - "platform channel"
  - "pigeon"
  - "네이티브 연동"
  - "iOS/Android 연동"

components:
  - Pigeon 인터페이스 정의
  - @HostApi (Flutter → Native)
  - @FlutterApi (Native → Flutter)
  - 코드 생성 스크립트

output:
  - pigeons/*.dart (인터페이스 정의)
  - lib/src/generated/*.g.dart (Dart)
  - android/.../Messages.g.kt (Kotlin)
  - ios/.../Messages.g.swift (Swift)
```

#### Phase 3: 테스트

##### 14-unit-test
```yaml
name: unit-test
description: Unit Test 작성 (Repository, UseCase, Notifier)
triggers:
  - "unit test"
  - "단위 테스트"

tools:
  - flutter_test
  - mocktail

patterns:
  - AAA (Arrange, Act, Assert)
  - Given-When-Then
  - ProviderContainer.test() 활용
```

##### 15-widget-test
```yaml
name: widget-test
description: Widget Test 작성
triggers:
  - "widget test"
  - "위젯 테스트"

tools:
  - flutter_test
  - ProviderScope overrides

patterns:
  - pumpWidget + pumpAndSettle
  - find.byType / find.byKey
  - tester.tap / tester.enterText
```

##### 16-golden-test
```yaml
name: golden-test
description: Golden Test (시각적 회귀 테스트) 작성
triggers:
  - "golden test"
  - "스냅샷 테스트"
  - "visual regression"

tools:
  - alchemist
  - golden_toolkit

patterns:
  - GoldenTestGroup / GoldenTestScenario
  - 다중 테마/디바이스 테스트
  - CI 환경 일관성 (폰트 로딩)
```

##### 17-e2e-test
```yaml
name: e2e-test
description: E2E 통합 테스트 (Patrol)
triggers:
  - "e2e test"
  - "통합 테스트"
  - "patrol"

tools:
  - patrol

features:
  - 네이티브 권한 처리
  - WebView 상호작용
  - 푸시 알림 테스트
  - Hot Restart 개발 모드
```

#### Phase 4: 최적화

##### 18-performance
```yaml
name: performance
description: 성능 최적화 분석 및 적용
triggers:
  - "성능 최적화"
  - "performance"

areas:
  - Widget 리빌드 최적화 (select, Consumer)
  - 이미지 최적화
  - 리스트 최적화 (ListView.builder, cacheExtent)
  - 메모리 프로파일링
```

##### 19-refactor
```yaml
name: refactor
description: 코드 리팩토링
triggers:
  - "리팩토링"
  - "refactor"

patterns:
  - DRY (Don't Repeat Yourself)
  - 함수/클래스 추출
  - 의존성 정리
  - 네이밍 개선
```

#### Phase 5: 검증

##### 20-logging
```yaml
name: logging
description: Talker 로깅 시스템 설정
triggers:
  - "로깅 설정"
  - "talker"
  - "디버깅"

components:
  - Talker 인스턴스 설정
  - TalkerDioLogger (HTTP 로깅)
  - TalkerRiverpodObserver (상태 로깅)
  - TalkerScreen (UI 로그 뷰어)

features:
  - 로그 히스토리 관리
  - 로그 필터링
  - 로그 공유 (share_plus)
  - Crashlytics 연동 (선택)
```

##### 21-code-review
```yaml
name: code-review
description: 코드 리뷰 및 품질 검증
triggers:
  - "코드 리뷰"
  - "품질 검증"
  - "QA"

checklist:
  - Clean Architecture 준수
  - 테스트 커버리지
  - 린트 규칙 준수
  - 성능 이슈
  - 보안 취약점
```

---

### 기술 스택 요약

| 영역 | 기술 | 버전 |
|------|------|------|
| **언어** | Dart | 3.5+ |
| **프레임워크** | Flutter | 3.24+ |
| **상태관리** | Riverpod + Generator | 3.1.0 / 4.0.0+1 |
| **라우팅** | GoRouter + Builder | 17.0.1 |
| **네트워킹** | Dio + Retrofit | 5.9.0 / 4.9.2 |
| **로컬 DB** | Drift | 2.30.0 |
| **Platform Channel** | Pigeon | 26.1.5 |
| **로거** | Talker (Dio/Riverpod) | 5.1.9 |
| **데이터 클래스** | Freezed | 3.2.4 |
| **DI** | Injectable + get_it | 2.7.1 / 9.2.0 |
| **테스트 (Unit)** | mocktail | 1.0.4 |
| **테스트 (Golden)** | Alchemist | 0.13.0 |
| **테스트 (E2E)** | Patrol | 4.1.0 |
| **함수형** | fpdart | 1.2.0 |
| **MCP** | Dart MCP Server | 실험적 |

---

### 출력물 구조

```
workspace/flutter-expert/{project-name}/
│
├── docs/
│   ├── architecture-decision-record.md   # ADR
│   ├── feature-design/                   # 기능별 설계 문서
│   └── test-strategy.md                  # 테스트 전략
│
├── reports/
│   ├── code-review-{date}.md            # 코드 리뷰 리포트
│   └── performance-analysis.md           # 성능 분석 리포트
│
└── flutter-project/                      # 생성된 Flutter 프로젝트
    ├── lib/
    │   ├── core/
    │   └── features/
    ├── test/
    │   ├── unit/
    │   ├── widget/
    │   └── golden/
    ├── integration_test/                 # Patrol E2E
    └── pubspec.yaml
```

---

### 명령어 가이드

#### 전체 프로세스
```
"Flutter 앱 설계하고 구현해줘"
"새 기능 추가해줘"
"TDD로 개발해줘"
```

#### 개별 Skill 호출
```
# Phase 1: 설계
/flutter-setup        # 프로젝트 설정
/flutter-arch         # 아키텍처 설계
/flutter-design       # Atomic Design 시스템
/flutter-feature      # Feature 설계

# Phase 2: 구현
/flutter-entity       # Entity 생성
/flutter-repo         # Repository 생성
/flutter-usecase      # UseCase 생성
/flutter-notifier     # Notifier 생성
/flutter-view         # View 생성 (Atomic 계층별)
/flutter-route        # 라우팅 설정
/flutter-network      # API Client (Dio+Retrofit)
/flutter-database     # 로컬 DB (Drift)
/flutter-pigeon       # Platform Channel

# Phase 3: 테스트
/flutter-unit-test    # Unit Test
/flutter-widget-test  # Widget Test
/flutter-golden-test  # Golden Test
/flutter-e2e-test     # E2E Test (Patrol)

# Phase 4-5: 최적화 & 검증
/flutter-perf         # 성능 최적화
/flutter-refactor     # 리팩토링
/flutter-logging      # Talker 로깅
/flutter-review       # 코드 리뷰
```

---

### 사용 시나리오

#### 시나리오 1: 신규 프로젝트 시작

```
사용자: Flutter 앱 새로 시작할건데 설정해줘

Agent 실행:
1. [project-setup] pubspec.yaml 생성, 의존성 구성
2. [architecture] Clean Architecture 구조 설정
3. build_runner 실행

결과:
✅ 프로젝트 구조 생성 완료
✅ 의존성 설치 완료
✅ 코드 생성 완료
```

#### 시나리오 2: 기능 구현 (TDD)

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

#### 시나리오 3: 테스트 작성

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

### 다음 단계

1. **Agent 파일 생성**: `.claude/agents/💻 개발/flutter-expert-agent.md`
2. **Skills 구현**: 16개 스킬 SKILL.md 파일 생성
3. **레퍼런스 문서 작성**: WIDGET-PATTERN.md, TEST-PATTERN.md 등
4. **테스트 및 검증**: 실제 프로젝트에서 워크플로우 테스트

---

## 참고 자료

### Riverpod 3.0
- [What's New in Riverpod 3.0](https://riverpod.dev/docs/whats_new)
- [Riverpod Generator](https://pub.dev/packages/riverpod_generator)
- [Riverpod 3 New Features](https://www.dhiwise.com/post/riverpod-3-new-features-for-flutter-developers)

### Clean Architecture
- [Flutter App Architecture Guide](https://docs.flutter.dev/app-architecture/guide)
- [Clean Architecture Example](https://github.com/guilherme-v/flutter-clean-architecture-example)
- [Mastering Flutter Clean Architecture 2025](https://medium.com/@notesapp555/mastering-flutter-clean-architecture-in-2025-a-beginner-to-pro-guide-for-scalable-app-development-d87a3995408e)

### Atomic Design
- [Atomic Design Methodology (Brad Frost)](https://atomicdesign.bradfrost.com/chapter-2/)
- [Flutter Atomic Design GitHub](https://github.com/aramidefemi/flutter-atomic-design)
- [Building a Design System with Atomic Design in Flutter](https://medium.com/@hlfdev/building-a-design-system-with-atomic-design-in-flutter-a7a16e28739b)
- [Bancolombia Tech: Atomic Design in Flutter](https://medium.com/bancolombia-tech/building-a-design-system-using-atomic-design-methodology-in-flutter-327142bf30c2)
- [Flutter Design System (Widgetbook)](https://www.widgetbook.io/blog/building-and-maintaining-high-quality-flutter-uis-with-a-design-system)
- [Flutter Theme Extensions for Design Tokens](https://vibe-studio.ai/insights/creating-reusable-design-system-tokens-in-flutter-with-theme-extensions)

### 네트워킹
- [Dio Package](https://pub.dev/packages/dio)
- [Retrofit Package](https://pub.dev/packages/retrofit)
- [Mastering HTTP Calls in Flutter 2025](https://medium.com/@pv.jassim/mastering-http-calls-in-flutter-2025-edition-http-vs-dio-vs-retrofit-1962ec46be43)
- [Flutter Retrofit Tutorial: Clean Architecture](https://medium.com/@prathamesh.dev004/flutter-retrofit-tutorial-clean-architecture-based-api-integration-d4539a30b82e)

### 로컬 데이터베이스
- [Drift Package](https://pub.dev/packages/drift)
- [Drift Documentation](https://drift.simonbinder.eu/)
- [Flutter Databases Comparison 2025](https://quashbugs.com/blog/hive-vs-drift-vs-floor-vs-isar-2025)

### Platform Channel
- [Pigeon Package](https://pub.dev/packages/pigeon)
- [Flutter Platform Channels](https://docs.flutter.dev/platform-integration/platform-channels)
- [Type-Safe Platform Channels with Pigeon 2025](https://the-expert-developer.medium.com/%EF%B8%8F-type-safe-platform-channels-in-flutter-2025-with-pigeon-build-native-power-without-the-15f9db2d7d96)

### 로깅
- [Talker Flutter Package](https://pub.dev/packages/talker_flutter)
- [Talker Dio Logger](https://pub.dev/packages/talker_dio_logger)
- [Talker Riverpod Logger](https://pub.dev/packages/talker_riverpod_logger)

### Testing
- [Patrol Framework](https://patrol.leancode.co/)
- [Alchemist Golden Testing](https://pub.dev/packages/alchemist)
- [Mocktail](https://pub.dev/packages/mocktail)

### MCP
- [7 MCP Servers for Flutter](https://www.verygood.ventures/blog/7-mcp-servers-every-dart-and-flutter-developer-should-know)
- [MCP Flutter GitHub](https://gist.github.com/lukemmtt/62c0889f7a959546702a973239382b12)

### 코드 생성
- [Freezed Package](https://pub.dev/packages/freezed)
- [Injectable Package](https://pub.dev/packages/injectable)
- [Go Router Builder](https://pub.dev/packages/go_router_builder)
