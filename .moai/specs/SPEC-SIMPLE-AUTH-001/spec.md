# SPEC-SIMPLE-AUTH-001: 간소화된 인증 - Firebase Anonymous Login

## 메타데이터

| 항목 | 내용 |
|------|------|
| **SPEC ID** | SPEC-SIMPLE-AUTH-001 |
| **제목** | 간소화된 인증 - Firebase Anonymous Login |
| **생성일** | 2026-01-20 |
| **상태** | Planned |
| **우선순위** | High |
| **담당 에이전트** | expert-backend, expert-frontend |

---

## 1. Environment (환경)

### 1.1 기술 스택

| 구성요소 | 기술 |
|----------|------|
| **Frontend** | Flutter |
| **Backend** | Firebase (Firestore, Cloud Functions) |
| **Authentication** | Firebase Anonymous Auth |
| **Push Notification** | Firebase Cloud Messaging (FCM) |

### 1.2 시스템 컨텍스트

- **사용자**: 커플 앱 사용자 2명 (다중 기기 지원)
- **환경**: iOS/Android 모바일 앱
- **기존 상태**: 이메일/비밀번호 로그인 시스템 계획됨 (미구현)
- **목표 상태**: Firebase Anonymous Authentication으로 간소화

### 1.3 데이터 구조

```
Firestore:
├─ users/
│   ├─ {anonymousUid1}/
│   │   ├─ name: "우기"
│   │   └─ fcmTokens: ["token1", "token2"...]
│   │
│   └─ {anonymousUid2}/
│       ├─ name: "민지"
│       └─ fcmTokens: ["token3"...]
│
├─ todos/
│   └─ {todoId}/
│       ├─ title: "장보기"
│       ├─ assignedTo: {anonymousUid}
│       ├─ createdBy: {anonymousUid}
│       └─ completed: false
```

---

## 2. Assumptions (가정)

### 2.1 기술적 가정

- **A1**: Firebase Anonymous Auth는 기기별 고유 UID를 생성한다
- **A2**: Anonymous 세션은 앱 삭제 전까지 Firebase SDK에 의해 자동 복원된다
- **A3**: FCM 토큰은 앱 시작 시 항상 갱신 가능하다
- **A4**: Firestore는 배열 필드에 대한 arrayUnion 연산을 지원한다

### 2.2 비즈니스 가정

- **B1**: 사용자는 최대 2명이다 (커플)
- **B2**: 한 사용자가 여러 기기에서 앱을 사용할 수 있다
- **B3**: 커플 매칭 기능은 추후 친구들이 사용할 수 있도록 코드를 보존한다
- **B4**: 이름 입력은 최초 1회만 필요하다

### 2.3 보안 가정

- **S1**: Anonymous UID는 충분한 엔트로피를 가진다
- **S2**: Firestore Security Rules로 데이터 접근을 제어한다
- **S3**: FCM 토큰 노출은 푸시 알림 수신만 가능하게 한다

---

## 3. Requirements (요구사항) - EARS Format

### 3.1 인증 요구사항

#### REQ-AUTH-001: 자동 익명 로그인 (Ubiquitous)
> 시스템은 **항상** 앱 실행 시 Firebase Anonymous Authentication을 통해 자동으로 로그인해야 한다.

#### REQ-AUTH-002: 최초 실행 이름 입력 (Event-Driven)
> **WHEN** 사용자가 앱을 최초 실행하면 **THEN** 시스템은 이름 입력 화면을 표시하고 Firestore users/{anonymousUid}/name 필드에 저장해야 한다.

#### REQ-AUTH-003: 세션 자동 복원 (State-Driven)
> **IF** 이전에 로그인한 적이 있는 기기라면 **THEN** Firebase SDK가 세션을 자동 복원하고 이름 입력 화면을 건너뛰어야 한다.

#### REQ-AUTH-004: 이메일/비밀번호 관리 제외 (Unwanted)
> 시스템은 이메일/비밀번호 입력, 저장, 검증 기능을 **구현하지 않아야 한다**.

### 3.2 FCM 토큰 관리 요구사항

#### REQ-FCM-001: 토큰 저장 위치 (Ubiquitous)
> 시스템은 **항상** FCM 토큰을 users/{anonymousUid}/fcmTokens 배열 필드에 저장해야 한다.

#### REQ-FCM-002: 토큰 누적 저장 (Event-Driven)
> **WHEN** 새로운 FCM 토큰이 발급되면 **THEN** 기존 토큰을 교체하지 않고 arrayUnion을 사용하여 누적 저장해야 한다.

#### REQ-FCM-003: 앱 시작 시 토큰 갱신 (Event-Driven)
> **WHEN** 앱이 시작되면 **THEN** FCM 토큰을 획득하고 Firestore에 저장해야 한다.

#### REQ-FCM-004: 기기 식별 (Ubiquitous)
> 시스템은 **항상** FCM 토큰 자체를 기기 식별자로 사용해야 한다.

### 3.3 푸시 알림 요구사항

#### REQ-PUSH-001: 전체 토큰 조회 (Event-Driven)
> **WHEN** 푸시 알림 전송이 트리거되면 **THEN** Cloud Functions는 모든 사용자의 모든 fcmTokens를 조회해야 한다.

#### REQ-PUSH-002: 전체 기기 발송 (Event-Driven)
> **WHEN** 푸시 알림을 발송할 때 **THEN** 조회된 모든 FCM 토큰에 알림을 전송해야 한다.

### 3.4 할 일 할당 요구사항

#### REQ-TODO-001: 사용자 할당 (Event-Driven)
> **WHEN** 할 일을 생성하거나 수정할 때 **THEN** assignedTo 필드에 anonymousUid를 저장하여 특정 사용자에게 할당할 수 있어야 한다.

#### REQ-TODO-002: 할당자 이름 표시 (State-Driven)
> **IF** 할 일에 assignedTo가 설정되어 있다면 **THEN** 해당 사용자의 이름을 조회하여 "{이름}에게 할당됨" 형식으로 표시해야 한다.

#### REQ-TODO-003: 전체 수정 권한 (Ubiquitous)
> 시스템은 **항상** 모든 사용자가 모든 할 일을 수정할 수 있도록 해야 한다.

### 3.5 커플 매칭 기능 요구사항

#### REQ-COUPLE-001: 코드 보존 (Unwanted)
> 시스템은 기존 커플 매칭 관련 코드를 **삭제하지 않아야 한다**.

#### REQ-COUPLE-002: 기능 비활성화 (State-Driven)
> **IF** 현재 버전이라면 **THEN** 커플 매칭 기능을 우회(bypass)하여 비활성화해야 한다.

#### REQ-COUPLE-003: 향후 확장성 (Optional)
> **가능하면** 커플 매칭 로직을 추후 친구들이 사용할 수 있도록 모듈화하여 보존해야 한다.

---

## 4. Specifications (명세)

### 4.1 인증 흐름 명세

```
[앱 시작]
    │
    ▼
[Firebase Auth 상태 확인]
    │
    ├─ 기존 세션 있음 ──▶ [홈 화면으로 이동]
    │
    └─ 신규 사용자 ──▶ [signInAnonymously() 호출]
                            │
                            ▼
                      [이름 입력 화면]
                            │
                            ▼
                      [Firestore에 사용자 생성]
                            │
                            ▼
                      [홈 화면으로 이동]
```

### 4.2 FCM 토큰 관리 명세

```dart
// Flutter 코드 예시
Future<void> refreshFcmToken() async {
  final user = FirebaseAuth.instance.currentUser;
  if (user == null) return;

  final token = await FirebaseMessaging.instance.getToken();
  if (token == null) return;

  await FirebaseFirestore.instance
      .collection('users')
      .doc(user.uid)
      .update({
        'fcmTokens': FieldValue.arrayUnion([token]),
      });
}
```

### 4.3 Cloud Functions 푸시 알림 명세

```typescript
// Cloud Functions 코드 예시
export const sendPushToAll = functions.firestore
  .document('todos/{todoId}')
  .onCreate(async (snap, context) => {
    const usersSnapshot = await admin.firestore()
      .collection('users')
      .get();

    const allTokens: string[] = [];
    usersSnapshot.docs.forEach(doc => {
      const tokens = doc.data().fcmTokens || [];
      allTokens.push(...tokens);
    });

    if (allTokens.length === 0) return;

    await admin.messaging().sendEachForMulticast({
      tokens: allTokens,
      notification: {
        title: '새 할 일',
        body: snap.data().title,
      },
    });
  });
```

### 4.4 Firestore Security Rules 명세

```javascript
rules_version = '2';
service cloud.firestore {
  match /databases/{database}/documents {
    // 인증된 사용자만 접근 가능
    match /users/{userId} {
      allow read: if request.auth != null;
      allow write: if request.auth != null && request.auth.uid == userId;
    }

    // 모든 인증된 사용자가 할 일 읽기/쓰기 가능
    match /todos/{todoId} {
      allow read, write: if request.auth != null;
    }
  }
}
```

---

## 5. Constraints (제약사항)

### 5.1 기술적 제약

- Firebase Anonymous Auth의 세션 만료 정책을 따름
- FCM 토큰은 Firebase에서 주기적으로 갱신될 수 있음
- arrayUnion은 중복 토큰을 자동으로 무시함

### 5.2 비즈니스 제약

- 사용자 수는 2명으로 제한 (현재 버전)
- 커플 매칭 코드 삭제 금지

### 5.3 보안 제약

- 모든 Firestore 접근은 인증 필수
- 사용자는 자신의 문서만 수정 가능 (users 컬렉션)
- 할 일은 모든 인증된 사용자가 수정 가능

---

## 6. Traceability (추적성)

| 요구사항 ID | 구현 위치 | 테스트 시나리오 |
|-------------|-----------|-----------------|
| REQ-AUTH-001 | AuthService.signInAnonymously() | TC-AUTH-001 |
| REQ-AUTH-002 | NameInputScreen | TC-AUTH-002 |
| REQ-AUTH-003 | AuthService.checkSession() | TC-AUTH-003 |
| REQ-FCM-001 | FcmService.saveToken() | TC-FCM-001 |
| REQ-FCM-002 | FcmService.saveToken() | TC-FCM-002 |
| REQ-TODO-001 | TodoService.assignUser() | TC-TODO-001 |
| REQ-COUPLE-001 | CoupleMatchingService (disabled) | TC-COUPLE-001 |

---

## Related Documents

- [Implementation Plan](plan.md)
- [Acceptance Criteria](acceptance.md)
