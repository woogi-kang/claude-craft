# SPEC-SIMPLE-AUTH-001: 구현 계획

## 메타데이터

| 항목 | 내용 |
|------|------|
| **SPEC ID** | SPEC-SIMPLE-AUTH-001 |
| **제목** | 간소화된 인증 - Firebase Anonymous Login |
| **생성일** | 2026-01-20 |
| **관련 문서** | [spec.md](spec.md), [acceptance.md](acceptance.md) |

---

## 1. 마일스톤 (우선순위 기반)

### Primary Goal (1차 목표): 인증 시스템 구현

**범위**: Firebase Anonymous Auth 통합 및 사용자 관리

| 태스크 | 설명 | 관련 요구사항 |
|--------|------|---------------|
| AUTH-1.1 | AuthService 클래스 생성 및 signInAnonymously() 구현 | REQ-AUTH-001 |
| AUTH-1.2 | 앱 시작 시 인증 상태 확인 로직 구현 | REQ-AUTH-003 |
| AUTH-1.3 | 이름 입력 화면 UI 구현 | REQ-AUTH-002 |
| AUTH-1.4 | Firestore users 컬렉션 스키마 정의 및 생성 로직 | REQ-AUTH-002 |

**완료 기준**:
- 앱 실행 시 자동으로 익명 로그인됨
- 최초 사용자는 이름 입력 후 Firestore에 저장됨
- 기존 사용자는 자동으로 홈 화면으로 이동됨

### Secondary Goal (2차 목표): FCM 토큰 관리

**범위**: FCM 토큰 저장 및 갱신 로직

| 태스크 | 설명 | 관련 요구사항 |
|--------|------|---------------|
| FCM-2.1 | FcmService 클래스 생성 | REQ-FCM-001 |
| FCM-2.2 | FCM 토큰 획득 로직 구현 | REQ-FCM-003 |
| FCM-2.3 | arrayUnion을 사용한 토큰 누적 저장 구현 | REQ-FCM-002 |
| FCM-2.4 | 앱 시작 시 자동 토큰 갱신 통합 | REQ-FCM-003 |

**완료 기준**:
- 앱 시작 시 FCM 토큰이 Firestore에 저장됨
- 동일 토큰은 중복 저장되지 않음
- 다중 기기 토큰이 배열로 누적됨

### Tertiary Goal (3차 목표): 푸시 알림 시스템

**범위**: Cloud Functions 기반 푸시 알림 발송

| 태스크 | 설명 | 관련 요구사항 |
|--------|------|---------------|
| PUSH-3.1 | Cloud Functions 프로젝트 설정 | REQ-PUSH-001 |
| PUSH-3.2 | 할 일 생성 트리거 함수 구현 | REQ-PUSH-001 |
| PUSH-3.3 | 전체 사용자 토큰 조회 로직 | REQ-PUSH-001 |
| PUSH-3.4 | sendEachForMulticast를 사용한 일괄 발송 | REQ-PUSH-002 |

**완료 기준**:
- 새 할 일 생성 시 모든 기기에 푸시 알림 발송됨
- 무효 토큰 처리 로직 포함

### Quaternary Goal (4차 목표): 할 일 할당 기능

**범위**: 사용자별 할 일 할당 및 표시

| 태스크 | 설명 | 관련 요구사항 |
|--------|------|---------------|
| TODO-4.1 | todos 컬렉션 스키마에 assignedTo 필드 추가 | REQ-TODO-001 |
| TODO-4.2 | 할 일 생성/수정 시 사용자 선택 UI | REQ-TODO-001 |
| TODO-4.3 | 할당된 사용자 이름 조회 및 표시 | REQ-TODO-002 |
| TODO-4.4 | 사용자 목록 캐싱 최적화 | REQ-TODO-002 |

**완료 기준**:
- 할 일에 사용자 할당 가능
- "{이름}에게 할당됨" 형식으로 표시됨

### Optional Goal (선택 목표): 커플 매칭 비활성화

**범위**: 기존 커플 매칭 코드 보존 및 우회

| 태스크 | 설명 | 관련 요구사항 |
|--------|------|---------------|
| COUPLE-5.1 | 커플 매칭 진입점 식별 | REQ-COUPLE-001 |
| COUPLE-5.2 | Feature flag 또는 조건문으로 우회 처리 | REQ-COUPLE-002 |
| COUPLE-5.3 | 코드 보존 확인 및 문서화 | REQ-COUPLE-003 |

**완료 기준**:
- 커플 매칭 코드가 삭제되지 않음
- 현재 버전에서 커플 매칭 기능이 비활성화됨
- 향후 활성화 방법이 문서화됨

---

## 2. 기술적 접근 방식

### 2.1 인증 아키텍처

```
┌─────────────────────────────────────────────────────────┐
│                    Flutter App                          │
├─────────────────────────────────────────────────────────┤
│  ┌──────────────┐    ┌──────────────┐    ┌───────────┐ │
│  │ AuthService  │───▶│ Firebase     │───▶│ Firestore │ │
│  │              │    │ Auth SDK     │    │ users/    │ │
│  └──────────────┘    └──────────────┘    └───────────┘ │
│         │                                               │
│         ▼                                               │
│  ┌──────────────┐                                       │
│  │ AuthState    │ (Provider/Riverpod)                  │
│  │ - user       │                                       │
│  │ - isNewUser  │                                       │
│  └──────────────┘                                       │
└─────────────────────────────────────────────────────────┘
```

### 2.2 FCM 토큰 흐름

```
[앱 시작]
    │
    ▼
[FirebaseMessaging.getToken()]
    │
    ▼
[토큰 획득 성공?]
    │
    ├─ 예 ──▶ [Firestore arrayUnion 저장]
    │              │
    │              ▼
    │         [저장 완료]
    │
    └─ 아니오 ──▶ [에러 로깅, 재시도 스케줄링]
```

### 2.3 푸시 알림 아키텍처

```
┌─────────────────┐      ┌──────────────────┐
│   Firestore     │      │  Cloud Functions │
│   todos/        │─────▶│  onCreate 트리거 │
└─────────────────┘      └────────┬─────────┘
                                  │
                                  ▼
                         ┌──────────────────┐
                         │ 모든 users/      │
                         │ fcmTokens 조회   │
                         └────────┬─────────┘
                                  │
                                  ▼
                         ┌──────────────────┐
                         │ FCM 일괄 발송    │
                         │ sendEachFor      │
                         │ Multicast        │
                         └──────────────────┘
```

---

## 3. 아키텍처 설계 방향

### 3.1 디렉토리 구조 (Flutter)

```
lib/
├── main.dart
├── firebase_options.dart
├── services/
│   ├── auth_service.dart          # 인증 관련 로직
│   ├── fcm_service.dart           # FCM 토큰 관리
│   ├── user_service.dart          # 사용자 CRUD
│   └── todo_service.dart          # 할 일 CRUD
├── providers/
│   ├── auth_provider.dart         # 인증 상태 관리
│   ├── user_provider.dart         # 사용자 목록 캐싱
│   └── todo_provider.dart         # 할 일 상태 관리
├── screens/
│   ├── splash_screen.dart         # 인증 상태 확인
│   ├── name_input_screen.dart     # 이름 입력 화면
│   ├── home_screen.dart           # 메인 화면
│   └── todo_detail_screen.dart    # 할 일 상세
├── widgets/
│   ├── user_selector.dart         # 사용자 선택 위젯
│   └── assigned_user_chip.dart    # 할당된 사용자 표시
└── models/
    ├── app_user.dart              # 사용자 모델
    └── todo.dart                  # 할 일 모델
```

### 3.2 Cloud Functions 구조

```
functions/
├── src/
│   ├── index.ts                   # 함수 진입점
│   ├── triggers/
│   │   └── todoCreated.ts         # 할 일 생성 트리거
│   └── utils/
│       └── fcmUtils.ts            # FCM 유틸리티
├── package.json
└── tsconfig.json
```

### 3.3 상태 관리 전략

**권장 패턴**: Riverpod (또는 Provider)

```dart
// auth_provider.dart 예시
final authStateProvider = StreamProvider<User?>((ref) {
  return FirebaseAuth.instance.authStateChanges();
});

final currentUserProvider = FutureProvider<AppUser?>((ref) async {
  final authState = ref.watch(authStateProvider);
  return authState.when(
    data: (user) => user != null
      ? UserService().getUser(user.uid)
      : null,
    loading: () => null,
    error: (_, __) => null,
  );
});
```

---

## 4. 리스크 및 대응 방안

### 4.1 기술적 리스크

| 리스크 | 영향도 | 대응 방안 |
|--------|--------|-----------|
| Anonymous 세션 만료 | 높음 | 앱 시작 시 항상 signInAnonymously() 호출, 기존 세션 있으면 재사용됨 |
| FCM 토큰 무효화 | 중간 | Cloud Functions에서 무효 토큰 자동 제거 로직 구현 |
| 다중 기기 토큰 누적 | 낮음 | 주기적으로 오래된 토큰 정리 배치 작업 고려 |

### 4.2 비즈니스 리스크

| 리스크 | 영향도 | 대응 방안 |
|--------|--------|-----------|
| 사용자 데이터 유실 (앱 삭제) | 높음 | Anonymous Auth 특성상 불가피, 향후 계정 연동 기능 고려 |
| 무단 접근 | 중간 | Firestore Security Rules로 인증 필수화 |

---

## 5. 의존성

### 5.1 Flutter 패키지

```yaml
dependencies:
  firebase_core: ^3.9.0
  firebase_auth: ^5.5.0
  firebase_messaging: ^15.2.0
  cloud_firestore: ^5.6.0
  flutter_riverpod: ^2.6.0  # 또는 provider
```

### 5.2 Cloud Functions 패키지

```json
{
  "dependencies": {
    "firebase-admin": "^12.0.0",
    "firebase-functions": "^6.0.0"
  }
}
```

---

## 6. 검증 방법

### 6.1 단위 테스트

- AuthService: Mock Firebase Auth로 signInAnonymously 테스트
- FcmService: Mock Firestore로 토큰 저장 테스트
- TodoService: 할당 로직 테스트

### 6.2 통합 테스트

- 앱 최초 실행 → 이름 입력 → 홈 화면 플로우
- FCM 토큰 저장 및 푸시 알림 수신
- 할 일 생성 및 할당 플로우

### 6.3 E2E 테스트

- 실제 Firebase 프로젝트에서 전체 플로우 테스트
- 다중 기기 시나리오 검증

---

## Related Documents

- [Requirements Specification](spec.md)
- [Acceptance Criteria](acceptance.md)
