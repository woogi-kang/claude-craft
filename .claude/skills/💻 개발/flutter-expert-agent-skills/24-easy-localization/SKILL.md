# l10n (Localization) Skill

easy_localization 패키지를 사용한 다국어 지원(국제화)을 구성합니다.

## Triggers

- "l10n", "다국어", "국제화", "localization", "번역", "easy_localization"

---

## Input

| 항목 | 필수 | 설명 |
|------|------|------|
| `supportedLocales` | ✅ | 지원 언어 목록 (ko, en, ja 등) |
| `defaultLocale` | ❌ | 기본 언어 (기본: ko) |

---

## 설정

### pubspec.yaml

```yaml
dependencies:
  easy_localization: ^3.0.8
  flutter_localizations:
    sdk: flutter

dev_dependencies:
  # 코드 생성 (선택)
  easy_localization_generator: ^2.0.0
```

### assets 선언

```yaml
flutter:
  assets:
    - assets/translations/
```

### iOS 설정 (ios/Runner/Info.plist)

```xml
<key>CFBundleLocalizations</key>
<array>
  <string>ko</string>
  <string>en</string>
  <string>ja</string>
</array>
```

---

## 디렉토리 구조

```
assets/
└── translations/
    ├── ko.json          # 한국어
    ├── en.json          # 영어
    └── ja.json          # 일본어

lib/
├── l10n/
│   └── locale_keys.g.dart   # 자동 생성 (선택)
└── main.dart
```

---

## Output Templates

### 1. 번역 파일 (JSON)

```json
// assets/translations/ko.json
{
  "app": {
    "title": "앱 이름",
    "version": "버전 {version}"
  },

  "common": {
    "confirm": "확인",
    "cancel": "취소",
    "save": "저장",
    "delete": "삭제",
    "edit": "수정",
    "next": "다음",
    "previous": "이전",
    "loading": "로딩 중...",
    "refresh": "새로고침"
  },

  "auth": {
    "login": "로그인",
    "logout": "로그아웃",
    "register": "회원가입",
    "email": "이메일",
    "password": "비밀번호",
    "forgot_password": "비밀번호 찾기"
  },

  "welcome": {
    "greeting": "환영합니다, {name}님!",
    "message": "{name}님, {count}개의 새 알림이 있습니다"
  },

  "items": {
    "zero": "아이템이 없습니다",
    "one": "1개 아이템",
    "other": "{} 개 아이템"
  },

  "price": {
    "zero": "무료",
    "one": "{}원",
    "other": "{}원"
  },

  "gender": {
    "male": "그가 로그인했습니다",
    "female": "그녀가 로그인했습니다",
    "other": "사용자가 로그인했습니다"
  },

  "error": {
    "required": "필수 입력 항목입니다",
    "invalid_email": "올바른 이메일 형식이 아닙니다",
    "min_length": "최소 {min}자 이상 입력하세요",
    "max_length": "최대 {max}자까지 입력 가능합니다",
    "network": "네트워크 오류가 발생했습니다",
    "unknown": "알 수 없는 오류가 발생했습니다"
  },

  "nav": {
    "home": "홈",
    "profile": "프로필",
    "settings": "설정",
    "notifications": "알림"
  },

  "linked": {
    "app_name": "MyApp",
    "welcome": "@:linked.app_name에 오신 것을 환영합니다!"
  }
}
```

```json
// assets/translations/en.json
{
  "app": {
    "title": "App Name",
    "version": "Version {version}"
  },

  "common": {
    "confirm": "Confirm",
    "cancel": "Cancel",
    "save": "Save",
    "delete": "Delete",
    "edit": "Edit",
    "next": "Next",
    "previous": "Previous",
    "loading": "Loading...",
    "refresh": "Refresh"
  },

  "auth": {
    "login": "Login",
    "logout": "Logout",
    "register": "Sign Up",
    "email": "Email",
    "password": "Password",
    "forgot_password": "Forgot Password?"
  },

  "welcome": {
    "greeting": "Welcome, {name}!",
    "message": "{name}, you have {count} new notifications"
  },

  "items": {
    "zero": "No items",
    "one": "1 item",
    "other": "{} items"
  },

  "price": {
    "zero": "Free",
    "one": "${} dollar",
    "other": "${} dollars"
  },

  "gender": {
    "male": "He logged in",
    "female": "She logged in",
    "other": "User logged in"
  },

  "error": {
    "required": "This field is required",
    "invalid_email": "Invalid email format",
    "min_length": "Minimum {min} characters required",
    "max_length": "Maximum {max} characters allowed",
    "network": "Network error occurred",
    "unknown": "An unknown error occurred"
  },

  "nav": {
    "home": "Home",
    "profile": "Profile",
    "settings": "Settings",
    "notifications": "Notifications"
  },

  "linked": {
    "app_name": "MyApp",
    "welcome": "Welcome to @:linked.app_name!"
  }
}
```

```json
// assets/translations/ja.json
{
  "app": {
    "title": "アプリ名",
    "version": "バージョン {version}"
  },

  "common": {
    "confirm": "確認",
    "cancel": "キャンセル",
    "save": "保存",
    "delete": "削除",
    "edit": "編集",
    "next": "次へ",
    "previous": "前へ",
    "loading": "読み込み中...",
    "refresh": "更新"
  },

  "auth": {
    "login": "ログイン",
    "logout": "ログアウト",
    "register": "新規登録",
    "email": "メールアドレス",
    "password": "パスワード",
    "forgot_password": "パスワードをお忘れですか？"
  },

  "welcome": {
    "greeting": "ようこそ、{name}さん！",
    "message": "{name}さん、{count}件の新しい通知があります"
  },

  "items": {
    "zero": "アイテムがありません",
    "one": "1個のアイテム",
    "other": "{}個のアイテム"
  },

  "error": {
    "required": "必須項目です",
    "invalid_email": "メールアドレスの形式が正しくありません",
    "min_length": "{min}文字以上入力してください",
    "max_length": "{max}文字以内で入力してください",
    "network": "ネットワークエラーが発生しました",
    "unknown": "不明なエラーが発生しました"
  },

  "nav": {
    "home": "ホーム",
    "profile": "プロフィール",
    "settings": "設定",
    "notifications": "通知"
  }
}
```

### 2. Main 설정

```dart
// lib/main.dart
import 'package:flutter/material.dart';
import 'package:easy_localization/easy_localization.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';

void main() async {
  WidgetsFlutterBinding.ensureInitialized();
  await EasyLocalization.ensureInitialized();

  runApp(
    EasyLocalization(
      supportedLocales: const [
        Locale('ko'),
        Locale('en'),
        Locale('ja'),
      ],
      path: 'assets/translations',
      fallbackLocale: const Locale('ko'),
      // 기본값은 디바이스 언어. 시작 언어를 고정하려면:
      // startLocale: const Locale('ko'),
      child: const ProviderScope(
        child: MyApp(),
      ),
    ),
  );
}

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      // easy_localization 연동
      localizationsDelegates: context.localizationDelegates,
      supportedLocales: context.supportedLocales,
      locale: context.locale,

      title: 'app.title'.tr(),
      theme: ThemeData(
        colorScheme: ColorScheme.fromSeed(seedColor: Colors.indigo),
        useMaterial3: true,
      ),
      home: const HomePage(),
    );
  }
}
```

### 3. 사용 예시

```dart
import 'package:easy_localization/easy_localization.dart';

class HomePage extends StatelessWidget {
  const HomePage({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('app.title'.tr()),
      ),
      body: Column(
        children: [
          // 기본 번역
          Text('common.confirm'.tr()),
          Text('auth.login'.tr()),

          // Named Arguments (중괄호)
          Text('welcome.greeting'.tr(namedArgs: {'name': '홍길동'})),
          // Output: 환영합니다, 홍길동님!

          // 여러 Named Arguments
          Text('welcome.message'.tr(namedArgs: {
            'name': '홍길동',
            'count': '5',
          })),
          // Output: 홍길동님, 5개의 새 알림이 있습니다

          // Positional Arguments (중괄호 없이 {})
          Text('error.min_length'.tr(namedArgs: {'min': '8'})),
          // Output: 최소 8자 이상 입력하세요

          // 복수형 (plural)
          Text('items'.plural(0)),   // 아이템이 없습니다
          Text('items'.plural(1)),   // 1개 아이템
          Text('items'.plural(5)),   // 5개 아이템

          // 복수형 + 숫자 포맷
          Text('price'.plural(
            1000000,
            format: NumberFormat.compact(locale: context.locale.toString()),
          )),

          // 성별 (gender)
          Text('gender'.tr(gender: 'male')),   // 그가 로그인했습니다
          Text('gender'.tr(gender: 'female')), // 그녀가 로그인했습니다

          // Linked Translation (@:)
          Text('linked.welcome'.tr()),
          // Output: MyApp에 오신 것을 환영합니다!

          // 현재 로케일 표시
          Text('현재 언어: ${context.locale.languageCode}'),
        ],
      ),
    );
  }
}
```

### 4. 언어 변경

```dart
// 언어 변경
context.setLocale(const Locale('en'));
context.setLocale(const Locale('ja'));
context.setLocale(const Locale('ko'));

// 디바이스 언어로 리셋
context.resetLocale();

// 현재 로케일 가져오기
final currentLocale = context.locale;

// 디바이스 로케일 가져오기
final deviceLocale = context.deviceLocale;

// 지원 로케일 목록
final supportedLocales = context.supportedLocales;

// 저장된 로케일 삭제
context.deleteSaveLocale();
```

### 5. 언어 선택 UI (Riverpod 통합)

```dart
// lib/features/settings/presentation/pages/language_settings_page.dart
import 'package:easy_localization/easy_localization.dart';
import 'package:flutter/material.dart';

class LanguageSettingsPage extends StatelessWidget {
  const LanguageSettingsPage({super.key});

  static const _localeOptions = [
    _LocaleOption(locale: Locale('ko'), name: '한국어', flag: '🇰🇷'),
    _LocaleOption(locale: Locale('en'), name: 'English', flag: '🇺🇸'),
    _LocaleOption(locale: Locale('ja'), name: '日本語', flag: '🇯🇵'),
  ];

  @override
  Widget build(BuildContext context) {
    final currentLocale = context.locale;

    return Scaffold(
      appBar: AppBar(
        title: Text('nav.settings'.tr()),
      ),
      body: ListView.builder(
        itemCount: _localeOptions.length,
        itemBuilder: (context, index) {
          final option = _localeOptions[index];
          final isSelected = option.locale == currentLocale;

          return ListTile(
            leading: Text(option.flag, style: const TextStyle(fontSize: 24)),
            title: Text(option.name),
            trailing: isSelected
                ? const Icon(Icons.check, color: Colors.green)
                : null,
            onTap: () async {
              await context.setLocale(option.locale);
            },
          );
        },
      ),
    );
  }
}

class _LocaleOption {
  final Locale locale;
  final String name;
  final String flag;

  const _LocaleOption({
    required this.locale,
    required this.name,
    required this.flag,
  });
}
```

### 6. Extension으로 간편하게

```dart
// lib/core/extensions/l10n_extension.dart
import 'package:easy_localization/easy_localization.dart';

/// 자주 사용하는 번역 키를 Extension으로 제공
extension CommonL10n on String {
  // 에러 메시지
  String get errorRequired => 'error.required'.tr();
  String get errorNetwork => 'error.network'.tr();
  String errorMinLength(int min) => 'error.min_length'.tr(namedArgs: {'min': '$min'});
  String errorMaxLength(int max) => 'error.max_length'.tr(namedArgs: {'max': '$max'});
}

/// 네비게이션 번역
extension NavL10n on BuildContext {
  String get navHome => 'nav.home'.tr();
  String get navProfile => 'nav.profile'.tr();
  String get navSettings => 'nav.settings'.tr();
}
```

---

## 코드 생성 (Type-safe Keys)

### 생성 명령어

```bash
# locale_keys.g.dart 생성
flutter pub run easy_localization:generate -S assets/translations -f keys -O lib/l10n -o locale_keys.g.dart

# 누락된 키 감사
flutter pub run easy_localization:audit
```

### 생성된 파일 사용

```dart
// lib/l10n/locale_keys.g.dart (자동 생성)
abstract class LocaleKeys {
  static const app_title = 'app.title';
  static const common_confirm = 'common.confirm';
  static const welcome_greeting = 'welcome.greeting';
  // ...
}

// 사용
import 'package:your_app/l10n/locale_keys.g.dart';

Text(LocaleKeys.app_title.tr())
Text(LocaleKeys.welcome_greeting.tr(namedArgs: {'name': '홍길동'}))
```

---

## API 요약

### String Extension

| 메서드 | 설명 | 예시 |
|--------|------|------|
| `.tr()` | 기본 번역 | `'key'.tr()` |
| `.tr(args: [])` | 위치 인자 | `'key'.tr(args: ['value'])` |
| `.tr(namedArgs: {})` | 이름 인자 | `'key'.tr(namedArgs: {'name': 'value'})` |
| `.tr(gender: '')` | 성별 번역 | `'key'.tr(gender: 'male')` |
| `.plural(n)` | 복수형 | `'key'.plural(5)` |

### BuildContext Extension

| 메서드 | 설명 |
|--------|------|
| `context.locale` | 현재 로케일 |
| `context.setLocale(locale)` | 로케일 변경 |
| `context.resetLocale()` | 디바이스 언어로 리셋 |
| `context.deviceLocale` | 디바이스 로케일 |
| `context.supportedLocales` | 지원 로케일 목록 |
| `context.fallbackLocale` | 폴백 로케일 |
| `context.deleteSaveLocale()` | 저장된 로케일 삭제 |
| `context.localizationDelegates` | MaterialApp에 전달할 delegates |

---

## JSON 키 네이밍 컨벤션

| 접두사 | 용도 | 예시 |
|--------|------|------|
| `app.` | 앱 전역 | `app.title`, `app.version` |
| `common.` | 공통 버튼/액션 | `common.confirm`, `common.cancel` |
| `auth.` | 인증 관련 | `auth.login`, `auth.password` |
| `nav.` | 네비게이션 | `nav.home`, `nav.profile` |
| `error.` | 에러 메시지 | `error.required`, `error.network` |
| `{feature}.` | Feature 전용 | `product.add_to_cart` |

---

## Linked Translation (참조)

```json
{
  "brand": {
    "name": "MyApp",
    "slogan": "최고의 앱"
  },
  "intro": {
    "welcome": "@:brand.name에 오신 것을 환영합니다!",
    "tagline": "@:brand.name - @:brand.slogan"
  }
}
```

### Modifier

| Modifier | 설명 | 예시 |
|----------|------|------|
| `@.upper:` | 대문자 | `@.upper:brand.name` → MYAPP |
| `@.lower:` | 소문자 | `@.lower:brand.name` → myapp |
| `@.capitalize:` | 첫 글자만 대문자 | `@.capitalize:brand.name` → Myapp |

---

## EasyLocalization 위젯 옵션

```dart
EasyLocalization(
  // 필수
  supportedLocales: [Locale('ko'), Locale('en')],
  path: 'assets/translations',
  child: MyApp(),

  // 선택
  fallbackLocale: Locale('ko'),           // 폴백 언어
  startLocale: Locale('ko'),              // 시작 언어 강제 지정
  saveLocale: true,                       // 선택한 언어 저장 (기본: true)
  useFallbackTranslations: true,          // 누락 키 시 폴백 사용
  useOnlyLangCode: true,                  // 언어 코드만 사용 (ko vs ko_KR)
  assetLoader: JsonAssetLoader(),         // 커스텀 로더
)
```

## References

- [pub.dev/packages/easy_localization](https://pub.dev/packages/easy_localization)
- [GitHub: aissat/easy_localization](https://github.com/aissat/easy_localization)
