---
name: notion-tech-writer
description: 기술 문서 작성 전문 Skill. API 문서, 아키텍처 문서, 트러블슈팅 가이드, 기술 스펙, 릴리즈 노트, 환경 설정 가이드, 코드 컨벤션 등 개발팀을 위한 기술 문서 작성 시 활성화.
version: 1.0.0
user-invocable: true
triggers:
  keywords:
    - API 문서
    - 아키텍처 문서
    - 트러블슈팅
    - 기술 스펙
    - TSD
    - 릴리즈 노트
    - 환경 설정 가이드
    - 코드 컨벤션
    - tech doc
    - technical documentation
dependencies:
  - notion-core
updated: 2026-01-29
---

# Notion Tech Writer

개발팀을 위한 기술 문서 작성 전문 Skill.

notion-core의 포맷팅 규칙을 상속하여 적용.

## Workflow

```
Step 1: 문서 유형 파악
        ↓
Step 2: 구조 제안 (ToC + 블록 전략)
        ↓
Step 3: 사용자 확인
        ↓
Step 4: 본문 작성
        ↓
Step 5: 유지보수 조건 명시
```

## Document Type Selection

| 요청 키워드 | 문서 유형 | 템플릿 참조 |
|------------|----------|------------|
| API, 엔드포인트, REST | API 문서 | `references/api-doc.md` |
| 아키텍처, 시스템 구조 | 아키텍처 문서 | `references/architecture-doc.md` |
| 에러, 문제해결, 트러블슈팅 | 트러블슈팅 | `references/troubleshooting-doc.md` |
| 기술 스펙, TSD, 기능 명세 | 기술 스펙 | `references/tech-spec-doc.md` |
| 릴리즈, 버전, 변경사항 | 릴리즈 노트 | `references/release-notes-doc.md` |
| 환경설정, 셋업, 설치 | 환경 설정 가이드 | `references/setup-guide-doc.md` |
| 코딩 스타일, 컨벤션 | 코드 컨벤션 | `references/code-convention-doc.md` |

## Pre-Writing Checklist

문서 작성 전 확인:

1. **주제**: 무엇을 문서화하는가?
2. **독자**: 누가 읽는가? (신입 개발자 / 시니어 / 외부 개발자)
3. **목적**: 읽은 후 무엇을 할 수 있어야 하는가?
4. **범위**: 어디까지 다루는가?

불명확하면 역질문으로 확인.

## Structure Proposal Format

본문 작성 전 제안 형식:

```markdown
## 구조 제안

**문서 유형**: [선택된 유형]
**예상 독자**: [타겟 독자]

### 목차 (ToC)
1. 섹션 1
2. 섹션 2
   - 2.1 하위 섹션
3. 섹션 3

### Notion 블록 전략
- 콜아웃: [어디에 사용할지]
- 토글: [어디에 사용할지]
- 테이블: [어디에 사용할지]
- 다이어그램: [필요 위치]

이 구조로 진행할까요?
```

## Common Patterns

### 코드 예시 패턴

```markdown
### 사용 예시

**기본 사용법**
```dart
// 파일: lib/example.dart
final result = await api.call();
```

▶️ 고급 옵션 보기
   [토글 내용: 추가 파라미터, 에러 핸들링 등]
```

### 에러/해결 패턴

```markdown
### 🚨 `ErrorName` 에러

**증상**
- 증상 1
- 증상 2

**원인**
원인 설명

**해결**
1. 단계 1
2. 단계 2

💡 이 에러는 [상황]에서 주로 발생합니다.
```

### API 엔드포인트 패턴

```markdown
### `POST /api/v1/resource`

**설명**: 리소스 생성

**Headers**
| 이름 | 필수 | 설명 |
|------|------|------|
| Authorization | ✅ | Bearer 토큰 |

**Request Body**
```json
{
  "field": "value"
}
```

**Response**
```json
{
  "id": "123",
  "created_at": "2025-01-01T00:00:00Z"
}
```

⚠️ rate limit: 100 req/min
```

## Quality Checklist

작성 완료 후 확인:

- [ ] 메타데이터 테이블 포함?
- [ ] H1은 1개만?
- [ ] 코드 블록에 언어 지정?
- [ ] 30줄 초과 코드는 토글 처리?
- [ ] 콜아웃 적절히 사용?
- [ ] 다이어그램 필요 위치 표시?
- [ ] 유지보수 조건 명시?
- [ ] 다음 행동(Action)이 명확?

## Maintenance Triggers

| 문서 유형 | 업데이트 트리거 |
|----------|----------------|
| API 문서 | API 버전 변경, 엔드포인트 추가/삭제 |
| 아키텍처 | 주요 컴포넌트 변경, 기술 스택 변경 |
| 트러블슈팅 | 새로운 에러 패턴 발견 |
| 기술 스펙 | 요구사항 변경, 구현 완료 |
| 릴리즈 노트 | 매 릴리즈 |
| 환경 설정 | 의존성 버전 변경, 도구 변경 |
| 코드 컨벤션 | 팀 합의 변경 |
