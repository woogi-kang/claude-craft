# Notifier Skill

Riverpod 3 Notifier를 구현합니다.

## Triggers

- "notifier 생성", "상태관리", "riverpod"

---

## Input

| 항목 | 필수 | 설명 |
|------|------|------|
| `notifierName` | ✅ | Notifier 이름 |
| `featurePath` | ✅ | Feature 경로 |
| `stateType` | ✅ | 상태 타입 (Entity, List, Custom) |

---

## Output Template

### AsyncNotifier (비동기 상태)

```dart
// features/{feature}/presentation/notifiers/{entity}_notifier.dart
import 'package:riverpod_annotation/riverpod_annotation.dart';

part '{entity}_notifier.g.dart';

@riverpod
class {Entity}Notifier extends _${Entity}Notifier {
  @override
  FutureOr<{Entity}Entity?> build() {
    return null;
  }

  Future<void> load{Entity}(String id) async {
    state = const AsyncLoading();

    final useCase = ref.read(get{Entity}UseCaseProvider);
    final result = await useCase(id);

    state = result.fold(
      (failure) => AsyncError(failure, StackTrace.current),
      (entity) => AsyncData(entity),
    );
  }

  Future<void> update{Entity}(Update{Entity}Params params) async {
    state = const AsyncLoading();

    final useCase = ref.read(update{Entity}UseCaseProvider);
    final result = await useCase(params);

    state = result.fold(
      (failure) => AsyncError(failure, StackTrace.current),
      (entity) => AsyncData(entity),
    );
  }
}
```

### AsyncNotifier (목록)

```dart
@riverpod
class {Entity}ListNotifier extends _${Entity}ListNotifier {
  @override
  FutureOr<List<{Entity}Entity>> build() async {
    return _fetch{Entity}List();
  }

  Future<List<{Entity}Entity>> _fetch{Entity}List() async {
    final useCase = ref.read(get{Entity}ListUseCaseProvider);
    final result = await useCase();

    return result.fold(
      (failure) => throw failure,
      (entities) => entities,
    );
  }

  Future<void> refresh() async {
    ref.invalidateSelf();
  }

  Future<void> delete{Entity}(String id) async {
    final useCase = ref.read(delete{Entity}UseCaseProvider);
    final result = await useCase(id);

    result.fold(
      (failure) => throw failure,
      (_) {
        // 목록에서 제거
        state = AsyncData(
          state.valueOrNull?.where((e) => e.id != id).toList() ?? [],
        );
      },
    );
  }
}
```

### Family Notifier (파라미터)

```dart
@riverpod
class {Entity}DetailNotifier extends _${Entity}DetailNotifier {
  @override
  FutureOr<{Entity}Entity?> build(String {entity}Id) async {
    return _fetch{Entity}({entity}Id);
  }

  Future<{Entity}Entity?> _fetch{Entity}(String id) async {
    final useCase = ref.read(get{Entity}UseCaseProvider);
    final result = await useCase(id);

    return result.fold(
      (failure) => throw failure,
      (entity) => entity,
    );
  }

  Future<void> refresh() async {
    ref.invalidateSelf();
  }
}
```

### Notifier (동기 상태)

```dart
@riverpod
class {Entity}FormNotifier extends _${Entity}FormNotifier {
  @override
  {Entity}FormState build() {
    return const {Entity}FormState();
  }

  void updateName(String name) {
    state = state.copyWith(name: name);
  }

  void updateDescription(String description) {
    state = state.copyWith(description: description);
  }

  bool validate() {
    final errors = <String, String>{};

    if (state.name.isEmpty) {
      errors['name'] = '이름을 입력해주세요';
    }

    state = state.copyWith(errors: errors);
    return errors.isEmpty;
  }

  Future<void> submit() async {
    if (!validate()) return;

    state = state.copyWith(isSubmitting: true);

    final useCase = ref.read(create{Entity}UseCaseProvider);
    final result = await useCase(Create{Entity}Params(
      name: state.name,
      description: state.description,
    ));

    result.fold(
      (failure) {
        state = state.copyWith(
          isSubmitting: false,
          submitError: failure.displayMessage,
        );
      },
      (entity) {
        state = state.copyWith(
          isSubmitting: false,
          isSubmitted: true,
        );
      },
    );
  }
}

@freezed
class {Entity}FormState with _${Entity}FormState {
  const factory {Entity}FormState({
    @Default('') String name,
    @Default('') String description,
    @Default({}) Map<String, String> errors,
    @Default(false) bool isSubmitting,
    @Default(false) bool isSubmitted,
    String? submitError,
  }) = _{Entity}FormState;
}
```

---

## Provider 정의 (자동 생성)

```dart
// {entity}_notifier.g.dart (자동 생성됨)
final {entity}NotifierProvider = AsyncNotifierProvider<{Entity}Notifier, {Entity}Entity?>(
  {Entity}Notifier.new,
);

final {entity}DetailNotifierProvider = AsyncNotifierProvider.family<{Entity}DetailNotifier, {Entity}Entity?, String>(
  {Entity}DetailNotifier.new,
);
```

## References

- `_references/RIVERPOD-PATTERN.md`
