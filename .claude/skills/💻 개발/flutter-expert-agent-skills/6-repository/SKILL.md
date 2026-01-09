# Repository Skill

Repository 패턴을 구현합니다 (Interface + Implementation).

## Triggers

- "repository 생성", "데이터 레이어"

---

## Input

| 항목 | 필수 | 설명 |
|------|------|------|
| `entityName` | ✅ | Entity 이름 |
| `featurePath` | ✅ | Feature 경로 |
| `methods` | ❌ | Repository 메서드 목록 |

---

## Output Template

### Repository Interface (Domain Layer)

```dart
// features/{feature}/domain/repositories/{entity}_repository.dart
import 'package:fpdart/fpdart.dart';

abstract class {Entity}Repository {
  /// {Entity} 단일 조회
  Future<Either<Failure, {Entity}Entity>> get{Entity}(String id);

  /// {Entity} 목록 조회
  Future<Either<Failure, List<{Entity}Entity>>> get{Entity}List({
    int? page,
    int? limit,
  });

  /// {Entity} 생성
  Future<Either<Failure, {Entity}Entity>> create{Entity}(
    {Entity}Entity entity,
  );

  /// {Entity} 수정
  Future<Either<Failure, {Entity}Entity>> update{Entity}(
    {Entity}Entity entity,
  );

  /// {Entity} 삭제
  Future<Either<Failure, Unit>> delete{Entity}(String id);

  /// {Entity} 검색
  Future<Either<Failure, List<{Entity}Entity>>> search{Entity}(
    String query,
  );
}
```

### Repository Implementation (Data Layer)

```dart
// features/{feature}/data/repositories/{entity}_repository_impl.dart
import 'package:fpdart/fpdart.dart';
import 'package:injectable/injectable.dart';

@Injectable(as: {Entity}Repository)
class {Entity}RepositoryImpl implements {Entity}Repository {
  final {Entity}RemoteDataSource _remoteDataSource;
  final {Entity}LocalDataSource _localDataSource;
  final NetworkInfo _networkInfo;

  {Entity}RepositoryImpl(
    this._remoteDataSource,
    this._localDataSource,
    this._networkInfo,
  );

  @override
  Future<Either<Failure, {Entity}Entity>> get{Entity}(String id) async {
    if (await _networkInfo.isConnected) {
      try {
        final model = await _remoteDataSource.get{Entity}(id);
        await _localDataSource.cache{Entity}(model);
        return Right(model.toEntity());
      } on ServerException catch (e) {
        return Left(ServerFailure(e.message, statusCode: e.statusCode));
      }
    } else {
      try {
        final cached = await _localDataSource.getCached{Entity}(id);
        if (cached != null) {
          return Right(cached.toEntity());
        }
        return const Left(CacheFailure('캐시된 데이터가 없습니다'));
      } on CacheException catch (e) {
        return Left(CacheFailure(e.message));
      }
    }
  }

  @override
  Future<Either<Failure, List<{Entity}Entity>>> get{Entity}List({
    int? page,
    int? limit,
  }) async {
    try {
      final models = await _remoteDataSource.get{Entity}List(
        page: page,
        limit: limit,
      );
      return Right(models.map((m) => m.toEntity()).toList());
    } on ServerException catch (e) {
      return Left(ServerFailure(e.message, statusCode: e.statusCode));
    }
  }

  @override
  Future<Either<Failure, {Entity}Entity>> create{Entity}(
    {Entity}Entity entity,
  ) async {
    try {
      final model = {Entity}Model.fromEntity(entity);
      final created = await _remoteDataSource.create{Entity}(model);
      return Right(created.toEntity());
    } on ServerException catch (e) {
      return Left(ServerFailure(e.message, statusCode: e.statusCode));
    }
  }

  @override
  Future<Either<Failure, {Entity}Entity>> update{Entity}(
    {Entity}Entity entity,
  ) async {
    try {
      final model = {Entity}Model.fromEntity(entity);
      final updated = await _remoteDataSource.update{Entity}(model);
      await _localDataSource.cache{Entity}(updated);
      return Right(updated.toEntity());
    } on ServerException catch (e) {
      return Left(ServerFailure(e.message, statusCode: e.statusCode));
    }
  }

  @override
  Future<Either<Failure, Unit>> delete{Entity}(String id) async {
    try {
      await _remoteDataSource.delete{Entity}(id);
      return const Right(unit);
    } on ServerException catch (e) {
      return Left(ServerFailure(e.message, statusCode: e.statusCode));
    }
  }
}
```

---

## Either 패턴

```dart
// 성공/실패를 명시적으로 처리
final result = await repository.getUser(id);

result.fold(
  (failure) => showError(failure.displayMessage),
  (user) => showUser(user),
);

// 또는
result.match(
  (failure) => showError(failure),
  (user) => showUser(user),
);
```

## References

- `_references/ARCHITECTURE-PATTERN.md`
