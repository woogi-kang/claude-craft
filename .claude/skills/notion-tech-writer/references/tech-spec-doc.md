# Technical Specification Document Template

## Structure

```markdown
# [기능명] Technical Specification

| 속성 | 값 |
|------|-----|
| 🏷️ 태그 | TSD, Spec, [기능 카테고리] |
| 👤 담당자 | @name |
| 📅 상태 | Draft / Review / Approved / Implemented |
| 📆 최종수정 | YYYY-MM-DD |
| 🔗 관련 PRD | [PRD 링크] |
| 🎯 목표 릴리즈 | vX.X.X / YYYY-MM-DD |

## Summary

| 항목 | 내용 |
|------|------|
| 목적 | [1문장: 무엇을 왜 만드는가] |
| 범위 | [포함/제외 사항] |
| 예상 공수 | [X MD (Man-Days)] |
| 리스크 | [주요 기술적 리스크] |

## Background

### 문제 정의

[해결하려는 문제 2-3문장]

### 현재 상태

[As-Is 설명]

### 목표 상태

[To-Be 설명]

[Image: As-Is vs To-Be 비교 다이어그램]

## Requirements

### Functional Requirements

| ID | 요구사항 | 우선순위 | 비고 |
|----|----------|----------|------|
| FR-01 | [요구사항 설명] | Must | |
| FR-02 | [요구사항 설명] | Should | |
| FR-03 | [요구사항 설명] | Could | |

### Non-Functional Requirements

| ID | 요구사항 | 기준 | 측정 방법 |
|----|----------|------|----------|
| NFR-01 | 응답 시간 | < 200ms (p99) | APM 모니터링 |
| NFR-02 | 가용성 | 99.9% | Uptime 모니터링 |
| NFR-03 | 동시 사용자 | 1,000명 | 부하 테스트 |

## Technical Design

### Architecture Overview

[Image: 기능 아키텍처 다이어그램]

### Component Design

#### [컴포넌트 1]

**책임**: [역할 설명]

**인터페이스**:
```dart
// 파일: lib/feature/interface.dart
abstract class FeatureRepository {
  Future<Result> execute(Request request);
}
```

**구현 세부사항**:
- [세부사항 1]
- [세부사항 2]

### Data Model

```sql
-- 신규 테이블
CREATE TABLE feature_table (
  id UUID PRIMARY KEY,
  user_id UUID REFERENCES users(id),
  data JSONB NOT NULL,
  created_at TIMESTAMP DEFAULT NOW()
);

-- 인덱스
CREATE INDEX idx_feature_user ON feature_table(user_id);
```

⚠️ 기존 `users` 테이블에 마이그레이션 필요 없음

### API Design

#### `POST /api/v1/feature`

**Request**
```json
{
  "user_id": "uuid",
  "data": {}
}
```

**Response**
```json
{
  "id": "uuid",
  "status": "created"
}
```

▶️ 전체 API 스펙
   [상세 API 명세]

### State Management

[Image: 상태 다이어그램]

```dart
// 파일: lib/feature/bloc/feature_bloc.dart
class FeatureBloc extends Bloc<FeatureEvent, FeatureState> {
  // 상태 관리 로직
}
```

## Implementation Plan

### Phase 1: Foundation (Week 1-2)

| Task | 담당 | 예상 공수 | 의존성 |
|------|------|----------|--------|
| DB 스키마 생성 | @backend | 0.5d | - |
| API 엔드포인트 | @backend | 2d | DB 스키마 |
| Repository 구현 | @frontend | 1d | API |

### Phase 2: Core Feature (Week 3-4)

| Task | 담당 | 예상 공수 | 의존성 |
|------|------|----------|--------|
| BLoC 구현 | @frontend | 2d | Repository |
| UI 개발 | @frontend | 3d | BLoC |
| 통합 테스트 | @qa | 1d | UI |

### Milestones

- [ ] Week 2: API 완료 및 테스트
- [ ] Week 4: Feature 완료 및 QA
- [ ] Week 5: 릴리즈

## Testing Strategy

### Unit Tests

```dart
// 파일: test/feature_test.dart
test('should return success when valid input', () {
  // 테스트 케이스
});
```

### Integration Tests

| 시나리오 | 예상 결과 |
|----------|----------|
| 정상 플로우 | 성공 응답 |
| 잘못된 입력 | 400 에러 |
| 권한 없음 | 401 에러 |

### Performance Tests

- 목표: 1000 RPS, p99 < 200ms
- 도구: k6, Artillery

## Risks & Mitigations

| 리스크 | 영향 | 확률 | 대응 방안 |
|--------|------|------|----------|
| API 지연 | High | Medium | 캐싱 레이어 추가 |
| DB 부하 | High | Low | 인덱스 최적화, Read Replica |
| 외부 의존성 | Medium | Medium | Fallback 구현 |

## Alternatives Considered

### Option A: [대안 1]

**장점**: ...
**단점**: ...

### Option B: [대안 2] ← 선택

**장점**: ...
**단점**: ...

**선택 이유**: [왜 이 방안을 선택했는지]

## Open Questions

- [ ] Q1: [미결 사항] → 담당: @name, 기한: MM/DD
- [ ] Q2: [미결 사항] → 담당: @name, 기한: MM/DD

## References

- [관련 PRD 링크]
- [관련 디자인 링크]
- [참고 문서 링크]

---
📝 **유지보수 노트**
- 요구사항 변경 시 업데이트
- 구현 완료 후 상태를 "Implemented"로 변경
- 실제 구현과 차이 발생 시 문서 동기화
```

## Key Elements

1. **Summary 테이블**: 한눈에 파악 가능한 요약
2. **Requirements**: ID 부여, 우선순위 명시
3. **NFR**: 측정 가능한 기준값
4. **Implementation Plan**: 테이블로 Task 관리
5. **Risks**: 영향도/확률 매트릭스
6. **Alternatives**: 의사결정 근거 기록
7. **Open Questions**: 미결 사항 추적
