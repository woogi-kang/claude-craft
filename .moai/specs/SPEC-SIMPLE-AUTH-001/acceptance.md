# SPEC-SIMPLE-AUTH-001: 인수 조건

## 메타데이터

| 항목 | 내용 |
|------|------|
| **SPEC ID** | SPEC-SIMPLE-AUTH-001 |
| **제목** | 간소화된 인증 - Firebase Anonymous Login |
| **생성일** | 2026-01-20 |
| **관련 문서** | [spec.md](spec.md), [plan.md](plan.md) |

---

## 1. 인증 테스트 시나리오

### TC-AUTH-001: 최초 실행 시 자동 익명 로그인

```gherkin
Feature: 자동 익명 로그인
  사용자가 앱을 처음 실행하면 자동으로 익명 로그인이 되어야 한다

  Scenario: 최초 사용자의 익명 로그인
    Given 앱이 처음 설치되었다
    And Firebase Auth에 기존 세션이 없다
    When 앱을 실행한다
    Then Firebase Anonymous Authentication으로 자동 로그인된다
    And 고유한 anonymousUid가 생성된다
    And 이름 입력 화면으로 이동한다

  Scenario: 로그인 실패 시 재시도
    Given 앱이 처음 설치되었다
    And 네트워크 연결이 불안정하다
    When 앱을 실행한다
    And 익명 로그인이 실패한다
    Then 에러 메시지가 표시된다
    And 재시도 버튼이 제공된다
```

### TC-AUTH-002: 이름 입력 및 저장

```gherkin
Feature: 이름 입력
  최초 사용자는 이름을 입력하고 저장해야 한다

  Scenario: 유효한 이름 입력
    Given 익명 로그인이 완료되었다
    And 이름 입력 화면이 표시되었다
    When 이름 입력 필드에 "우기"를 입력한다
    And 저장 버튼을 탭한다
    Then Firestore users/{anonymousUid}/name 필드에 "우기"가 저장된다
    And 홈 화면으로 이동한다

  Scenario: 빈 이름 입력 방지
    Given 익명 로그인이 완료되었다
    And 이름 입력 화면이 표시되었다
    When 이름 입력 필드를 비워둔다
    And 저장 버튼을 탭한다
    Then "이름을 입력해주세요" 에러 메시지가 표시된다
    And 화면이 이동하지 않는다

  Scenario: 이름 최대 길이 제한
    Given 익명 로그인이 완료되었다
    When 20자 초과의 이름을 입력한다
    Then 20자까지만 입력된다
    Or 에러 메시지가 표시된다
```

### TC-AUTH-003: 세션 자동 복원

```gherkin
Feature: 세션 복원
  기존 사용자는 자동으로 세션이 복원되어야 한다

  Scenario: 기존 사용자의 자동 로그인
    Given 이전에 앱에 로그인한 적이 있다
    And Firestore에 사용자 이름이 저장되어 있다
    When 앱을 다시 실행한다
    Then Firebase SDK가 자동으로 세션을 복원한다
    And 이름 입력 화면을 건너뛴다
    And 홈 화면으로 바로 이동한다

  Scenario: 앱 삭제 후 재설치
    Given 이전에 앱에 로그인한 적이 있다
    When 앱을 삭제하고 재설치한다
    And 앱을 실행한다
    Then 새로운 anonymousUid가 생성된다
    And 이름 입력 화면이 표시된다
```

---

## 2. FCM 토큰 관리 테스트 시나리오

### TC-FCM-001: 토큰 저장

```gherkin
Feature: FCM 토큰 저장
  FCM 토큰은 올바른 위치에 저장되어야 한다

  Scenario: 앱 시작 시 토큰 저장
    Given 사용자가 익명 로그인되어 있다
    And FCM 토큰이 발급된다
    When 앱이 시작된다
    Then FCM 토큰이 users/{anonymousUid}/fcmTokens 배열에 저장된다

  Scenario: 토큰 저장 위치 검증
    Given FCM 토큰 "abc123"이 발급되었다
    When 토큰 저장이 완료된다
    Then Firestore 경로 "users/{uid}/fcmTokens"에서 "abc123"을 찾을 수 있다
```

### TC-FCM-002: 토큰 누적 저장

```gherkin
Feature: FCM 토큰 누적
  새 토큰은 기존 토큰을 교체하지 않고 누적되어야 한다

  Scenario: 두 번째 기기에서 토큰 추가
    Given 사용자의 fcmTokens에 "token1"이 저장되어 있다
    When 두 번째 기기에서 앱을 실행한다
    And 새 토큰 "token2"가 발급된다
    Then fcmTokens 배열은 ["token1", "token2"]가 된다
    And "token1"이 삭제되지 않는다

  Scenario: 중복 토큰 방지
    Given 사용자의 fcmTokens에 "token1"이 저장되어 있다
    When 같은 기기에서 앱을 재실행한다
    And 동일한 "token1" 토큰이 다시 저장 시도된다
    Then fcmTokens 배열은 ["token1"]로 유지된다
    And 중복 토큰이 추가되지 않는다
```

### TC-FCM-003: 앱 시작 시 토큰 갱신

```gherkin
Feature: 토큰 갱신
  앱 시작 시 항상 FCM 토큰을 갱신해야 한다

  Scenario: 정상적인 토큰 갱신
    Given 사용자가 로그인되어 있다
    When 앱이 시작된다
    Then FirebaseMessaging.getToken()이 호출된다
    And 획득한 토큰이 Firestore에 저장된다

  Scenario: 토큰 획득 실패 처리
    Given 사용자가 로그인되어 있다
    And FCM 서비스가 일시적으로 불가능하다
    When 앱이 시작된다
    Then 토큰 획득 실패가 로깅된다
    And 앱은 정상적으로 동작한다
    And 다음 앱 시작 시 재시도된다
```

---

## 3. 푸시 알림 테스트 시나리오

### TC-PUSH-001: 전체 토큰 조회

```gherkin
Feature: 푸시 알림 토큰 조회
  푸시 발송 시 모든 사용자의 모든 토큰을 조회해야 한다

  Scenario: 두 사용자의 모든 토큰 조회
    Given 사용자1의 fcmTokens가 ["token1", "token2"]이다
    And 사용자2의 fcmTokens가 ["token3"]이다
    When 푸시 알림 트리거가 발생한다
    Then Cloud Functions가 모든 users 문서를 조회한다
    And 총 3개의 토큰 ["token1", "token2", "token3"]이 수집된다
```

### TC-PUSH-002: 전체 기기 발송

```gherkin
Feature: 푸시 알림 발송
  조회된 모든 토큰에 푸시 알림을 발송해야 한다

  Scenario: 새 할 일 생성 시 푸시 발송
    Given 3개의 FCM 토큰이 등록되어 있다
    When 새 할 일 "장보기"가 생성된다
    Then Cloud Functions onCreate 트리거가 실행된다
    And 3개의 토큰 모두에 푸시 알림이 발송된다
    And 알림 제목은 "새 할 일"이다
    And 알림 내용은 "장보기"이다

  Scenario: 무효 토큰 처리
    Given 토큰 "invalidToken"이 등록되어 있다
    When 푸시 알림을 발송한다
    And 해당 토큰이 무효하다는 응답을 받는다
    Then 무효 토큰은 로깅된다
    And 나머지 유효 토큰은 정상 발송된다
```

---

## 4. 할 일 할당 테스트 시나리오

### TC-TODO-001: 사용자 할당

```gherkin
Feature: 할 일 사용자 할당
  할 일을 특정 사용자에게 할당할 수 있어야 한다

  Scenario: 할 일 생성 시 사용자 할당
    Given 사용자 "우기"(uid1)와 "민지"(uid2)가 있다
    When 새 할 일 "장보기"를 생성한다
    And "민지"를 할당 대상으로 선택한다
    Then 할 일의 assignedTo 필드가 uid2로 저장된다
    And 할 일의 createdBy 필드가 현재 사용자 uid로 저장된다

  Scenario: 할당 없이 할 일 생성
    Given 사용자 "우기"(uid1)가 로그인되어 있다
    When 새 할 일 "청소하기"를 생성한다
    And 할당 대상을 선택하지 않는다
    Then 할 일의 assignedTo 필드는 null이다
```

### TC-TODO-002: 할당자 이름 표시

```gherkin
Feature: 할당자 이름 표시
  할당된 사용자의 이름이 표시되어야 한다

  Scenario: 할당된 할 일 목록 표시
    Given 할 일 "장보기"가 "민지"(uid2)에게 할당되어 있다
    When 할 일 목록을 조회한다
    Then "장보기" 항목에 "민지에게 할당됨"이 표시된다

  Scenario: 미할당 할 일 표시
    Given 할 일 "청소하기"가 아무에게도 할당되지 않았다
    When 할 일 목록을 조회한다
    Then "청소하기" 항목에 할당 정보가 표시되지 않는다

  Scenario: 사용자 이름 캐싱
    Given 사용자 목록이 이미 로드되어 있다
    When 할 일 목록을 조회한다
    Then 추가 Firestore 쿼리 없이 이름이 표시된다
```

### TC-TODO-003: 전체 수정 권한

```gherkin
Feature: 할 일 전체 수정 권한
  모든 사용자가 모든 할 일을 수정할 수 있어야 한다

  Scenario: 다른 사용자의 할 일 수정
    Given "우기"가 "장보기" 할 일을 생성했다
    When "민지"가 로그인한다
    And "장보기" 할 일을 "마트 장보기"로 수정한다
    Then 수정이 성공한다
    And 할 일 제목이 "마트 장보기"로 변경된다

  Scenario: 다른 사용자의 할 일 완료 처리
    Given "우기"가 "장보기" 할 일을 생성했다
    When "민지"가 해당 할 일을 완료 처리한다
    Then 완료 처리가 성공한다
    And completed 필드가 true로 변경된다
```

---

## 5. 커플 매칭 비활성화 테스트 시나리오

### TC-COUPLE-001: 코드 보존 확인

```gherkin
Feature: 커플 매칭 코드 보존
  커플 매칭 관련 코드가 삭제되지 않아야 한다

  Scenario: 커플 매칭 서비스 클래스 존재 확인
    Given 프로젝트 소스 코드를 검사한다
    Then CoupleMatchingService 클래스가 존재한다
    And 커플 코드 생성 로직이 존재한다
    And 커플 연결 로직이 존재한다

  Scenario: 커플 매칭 UI 코드 존재 확인
    Given 프로젝트 소스 코드를 검사한다
    Then 커플 매칭 관련 화면 코드가 존재한다
    And 초대 코드 입력 위젯이 존재한다
```

### TC-COUPLE-002: 기능 비활성화 확인

```gherkin
Feature: 커플 매칭 비활성화
  현재 버전에서 커플 매칭 기능이 비활성화되어야 한다

  Scenario: 커플 매칭 화면 진입 방지
    Given 앱이 정상적으로 실행된다
    When 홈 화면에 도달한다
    Then 커플 매칭 화면으로 이동하는 UI가 표시되지 않는다
    Or 비활성화된 상태로 표시된다

  Scenario: 우회 플래그 확인
    Given 앱 설정을 확인한다
    Then ENABLE_COUPLE_MATCHING 플래그가 false이다
    Or 커플 매칭 진입점에 조건문이 있다
```

---

## 6. Quality Gate (품질 관문)

### 6.1 기능 완료 기준

| 항목 | 기준 | 상태 |
|------|------|------|
| 자동 익명 로그인 | 앱 실행 시 100% 성공 | [ ] |
| 이름 저장 | Firestore에 정확히 저장됨 | [ ] |
| 세션 복원 | 기존 사용자 자동 로그인 | [ ] |
| FCM 토큰 저장 | arrayUnion으로 누적 저장 | [ ] |
| 푸시 알림 발송 | 모든 토큰에 발송 성공 | [ ] |
| 할 일 할당 | 사용자 이름 정확히 표시 | [ ] |
| 커플 매칭 비활성화 | 코드 보존, 기능 비활성 | [ ] |

### 6.2 비기능 요구사항 기준

| 항목 | 기준 | 상태 |
|------|------|------|
| 앱 시작 시간 | 3초 이내 홈 화면 도달 | [ ] |
| 토큰 저장 시간 | 1초 이내 완료 | [ ] |
| 에러 처리 | 모든 실패 케이스 처리됨 | [ ] |
| 보안 | Firestore Rules 적용됨 | [ ] |

### 6.3 Definition of Done

- [ ] 모든 테스트 시나리오 통과
- [ ] Firestore Security Rules 적용 및 검증
- [ ] 에러 핸들링 및 로깅 구현
- [ ] 코드 리뷰 완료
- [ ] 다중 기기 테스트 완료

---

## Related Documents

- [Requirements Specification](spec.md)
- [Implementation Plan](plan.md)
