# Code Convention Template

## Structure

```markdown
# [프로젝트명] Code Convention

| 속성 | 값 |
|------|-----|
| 🏷️ 태그 | Convention, Style Guide |
| 👤 담당자 | @tech-lead |
| 📅 상태 | 배포됨 |
| 📆 최종수정 | YYYY-MM-DD |
| 🔧 린터 설정 | `analysis_options.yaml` |

## Overview

이 문서는 [프로젝트명] 코드베이스의 일관성을 위한 코딩 컨벤션을 정의합니다.

💡 대부분의 규칙은 린터가 자동으로 검사합니다. 이 문서는 린터가 잡지 못하는 규칙과 팀 합의 사항을 다룹니다.

## Naming Conventions

### 파일명

| 유형 | 규칙 | 예시 |
|------|------|------|
| Dart 파일 | snake_case | `user_repository.dart` |
| 테스트 파일 | `*_test.dart` | `user_repository_test.dart` |
| BLoC | `*_bloc.dart` | `auth_bloc.dart` |
| 모델 | `*_model.dart` | `user_model.dart` |

### 클래스/변수

| 유형 | 규칙 | 예시 |
|------|------|------|
| 클래스 | PascalCase | `UserRepository` |
| 변수/함수 | camelCase | `getUserById` |
| 상수 | camelCase or SCREAMING_SNAKE | `maxRetryCount`, `API_KEY` |
| Private | `_` prefix | `_internalState` |
| Boolean | is/has/can prefix | `isLoading`, `hasError` |

### 예시

```dart
// ✅ Good
class UserRepository {
  final bool isAuthenticated;
  final int maxRetryCount;
  
  Future<User> getUserById(String userId) async { ... }
}

// ❌ Bad
class user_repository {
  final bool authenticated;  // is prefix 누락
  final int MAX_RETRY;       // 일관성 없음
  
  Future<User> get_user(String id) async { ... }  // snake_case
}
```

## Code Organization

### 파일 구조

```
lib/
├── core/                 # 공통 유틸, 상수, 확장
│   ├── constants/
│   ├── extensions/
│   └── utils/
├── data/                 # 데이터 레이어
│   ├── models/
│   ├── repositories/
│   └── sources/
├── domain/               # 도메인 레이어
│   ├── entities/
│   └── usecases/
├── presentation/         # UI 레이어
│   ├── blocs/
│   ├── pages/
│   └── widgets/
└── main.dart
```

### Import 순서

```dart
// 1. Dart SDK
import 'dart:async';
import 'dart:io';

// 2. Flutter SDK
import 'package:flutter/material.dart';
import 'package:flutter/services.dart';

// 3. 외부 패키지 (알파벳 순)
import 'package:bloc/bloc.dart';
import 'package:dio/dio.dart';

// 4. 프로젝트 내부 (알파벳 순)
import 'package:myapp/core/constants.dart';
import 'package:myapp/data/models/user.dart';
```

💡 VS Code에서 `Dart: Sort Imports` 명령어로 자동 정렬 가능

## Formatting Rules

### 줄 길이

- **최대**: 80자 (권장), 120자 (하드 리밋)
- **린터**: `analysis_options.yaml`에서 설정

### 들여쓰기

- **Spaces**: 2칸 (Dart 표준)
- **Tab 사용 금지**

### 중괄호

```dart
// ✅ Good - 한 줄이어도 중괄호 사용
if (condition) {
  doSomething();
}

// ❌ Bad
if (condition) doSomething();
```

### 콤마

```dart
// ✅ Good - Trailing comma 사용
Widget build(BuildContext context) {
  return Container(
    padding: EdgeInsets.all(16),
    child: Text('Hello'),  // ← trailing comma
  );
}
```

## Widget Guidelines

### 위젯 분리 기준

| 조건 | 액션 |
|------|------|
| 100줄 초과 | 분리 고려 |
| 재사용 가능 | 별도 파일로 분리 |
| 3단계 이상 중첩 | 메서드 추출 |

### 위젯 구조

```dart
class MyWidget extends StatelessWidget {
  // 1. 생성자
  const MyWidget({
    super.key,
    required this.title,
    this.onTap,
  });

  // 2. 필드 (final)
  final String title;
  final VoidCallback? onTap;

  // 3. build 메서드
  @override
  Widget build(BuildContext context) {
    return ...;
  }

  // 4. Private 헬퍼 메서드
  Widget _buildHeader() { ... }
}
```

### const 사용

```dart
// ✅ Good
const SizedBox(height: 16);
const EdgeInsets.all(8);

// ❌ Bad
SizedBox(height: 16);  // const 누락
```

⚠️ `const` 사용 가능한 곳에서 누락 시 린터 경고

## State Management

### BLoC 네이밍

| 유형 | 접미사 | 예시 |
|------|--------|------|
| BLoC | `Bloc` | `AuthBloc` |
| Event | `Event` | `AuthLoginRequested` |
| State | `State` | `AuthAuthenticated` |

### Event 네이밍

```dart
// ✅ Good - 과거분사 또는 명사
sealed class AuthEvent {
  const AuthEvent();
}

class AuthLoginRequested extends AuthEvent {
  const AuthLoginRequested(this.email, this.password);
  final String email;
  final String password;
}

class AuthLogoutRequested extends AuthEvent {
  const AuthLogoutRequested();
}

// ❌ Bad - 동사 원형
class Login extends AuthEvent { }  // 의미 불명확
```

### State 네이밍

```dart
// ✅ Good - 형용사 또는 현재 상태
sealed class AuthState {
  const AuthState();
}

class AuthInitial extends AuthState {}
class AuthLoading extends AuthState {}
class AuthAuthenticated extends AuthState {
  const AuthAuthenticated(this.user);
  final User user;
}
class AuthUnauthenticated extends AuthState {}
class AuthError extends AuthState {
  const AuthError(this.message);
  final String message;
}
```

## Error Handling

### try-catch 패턴

```dart
// ✅ Good
try {
  final result = await repository.fetchData();
  emit(DataLoaded(result));
} on NetworkException catch (e) {
  emit(DataError('네트워크 오류: ${e.message}'));
} on ServerException catch (e) {
  emit(DataError('서버 오류: ${e.code}'));
} catch (e, stackTrace) {
  logger.error('Unexpected error', e, stackTrace);
  emit(DataError('알 수 없는 오류'));
}

// ❌ Bad
try {
  ...
} catch (e) {
  print(e);  // 로깅 미흡
}
```

### Result 패턴 (선택)

```dart
sealed class Result<T> {
  const Result();
}

class Success<T> extends Result<T> {
  const Success(this.data);
  final T data;
}

class Failure<T> extends Result<T> {
  const Failure(this.error);
  final AppException error;
}
```

## Documentation

### 주석 규칙

```dart
/// 사용자 정보를 가져옵니다.
/// 
/// [userId]가 유효하지 않으면 [UserNotFoundException]을 던집니다.
/// 
/// Example:
/// ```dart
/// final user = await getUserById('123');
/// ```
Future<User> getUserById(String userId) async { ... }
```

| 상황 | 주석 필요 여부 |
|------|---------------|
| Public API | ✅ 필수 (doc comment) |
| 복잡한 비즈니스 로직 | ✅ 권장 |
| 자명한 코드 | ❌ 불필요 |
| TODO/FIXME | ✅ 이슈 번호와 함께 |

### TODO 형식

```dart
// TODO(#123): 캐싱 로직 추가 필요
// FIXME(#456): null 체크 누락
```

## Testing

### 테스트 구조

```dart
void main() {
  group('UserRepository', () {
    late UserRepository repository;
    late MockApiClient mockClient;

    setUp(() {
      mockClient = MockApiClient();
      repository = UserRepository(mockClient);
    });

    group('getUserById', () {
      test('should return user when API call succeeds', () async {
        // Arrange
        when(() => mockClient.get(any())).thenAnswer(
          (_) async => Response(data: userJson),
        );

        // Act
        final result = await repository.getUserById('123');

        // Assert
        expect(result, isA<User>());
        expect(result.id, equals('123'));
      });

      test('should throw when user not found', () async {
        // ...
      });
    });
  });
}
```

### 테스트 네이밍

```dart
// ✅ Good - should ... when ...
test('should return empty list when no users exist', () { });

// ❌ Bad
test('test1', () { });
test('getUserById', () { });
```

## Git Conventions

### Branch 네이밍

| 유형 | 형식 | 예시 |
|------|------|------|
| Feature | `feature/[issue]-[desc]` | `feature/123-user-auth` |
| Bugfix | `bugfix/[issue]-[desc]` | `bugfix/456-login-crash` |
| Hotfix | `hotfix/[desc]` | `hotfix/critical-fix` |

### Commit 메시지

```
type(scope): subject

body (optional)

footer (optional)
```

| Type | 용도 |
|------|------|
| `feat` | 새 기능 |
| `fix` | 버그 수정 |
| `docs` | 문서 변경 |
| `style` | 포맷팅 (코드 변경 없음) |
| `refactor` | 리팩토링 |
| `test` | 테스트 추가/수정 |
| `chore` | 빌드, 설정 변경 |

**예시**:
```
feat(auth): add social login support

- Add Google OAuth integration
- Add Apple Sign-In for iOS

Closes #123
```

---
📝 **유지보수 노트**
- 팀 합의 변경 시 업데이트
- 새로운 패턴 도입 시 추가
- 분기별 리뷰 권장
```

## Key Elements

1. **네이밍 테이블**: 일관된 규칙 참조
2. **Good/Bad 예시**: 코드 블록으로 비교
3. **린터 연계**: 자동화 가능한 부분 명시
4. **테스트 패턴**: AAA (Arrange-Act-Assert)
5. **Git 컨벤션**: 브랜치 + 커밋 메시지
