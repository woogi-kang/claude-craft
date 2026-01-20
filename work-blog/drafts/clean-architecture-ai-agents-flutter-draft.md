---
title: "Vibe Coding의 달콤한 함정: 왜 규모가 커지면 AI가 망가질까 (Flutter Edition)"
slug: vibe-coding-trap-clean-architecture-flutter
tags: ["vibe-coding", "clean-architecture", "flutter", "dart", "ai-agents", "context-engineering", "feature-based"]
seo_description: "Flutter 프로젝트에서 Vibe Coding이 처음엔 마법처럼 느껴지지만 규모가 커지면 왜 AI가 무너지는지, 그리고 Feature-based Clean Architecture가 어떻게 이 문제를 해결하는지 살펴봅니다."
---

# Vibe Coding의 달콤한 함정: 왜 규모가 커지면 AI가 망가질까 (Flutter Edition)

## 들어가며: 마법 같았던 첫 경험

"이거 진짜 개발자 필요 없겠는데?"

첫 번째 Vibe Coding 경험을 떠올려보세요. Claude나 Cursor에게 "간단한 TODO Flutter 앱 만들어줘"라고 말했을 때, 몇 분 만에 Material Design이 적용된 깔끔한 앱이 눈앞에 펼쳐졌습니다. Firebase 연동? 문제없습니다. 상태관리? Riverpod으로 자동 설정됩니다. 심지어 다크모드까지.

Andrej Karpathy가 2025년 2월 "Vibe Coding"이라는 용어를 처음 소개했을 때, 많은 Flutter 개발자들이 고개를 끄덕였습니다. 프롬프트만 던지면 AI가 위젯 트리를 뚝딱 만들어내고, 우리는 핫 리로드 결과만 확인하면 되는 시대가 온 것입니다.

**하지만 당신의 Flutter 프로젝트가 50개 화면을 넘어가는 순간, 마법은 악몽으로 바뀌기 시작합니다.**

## Vibe Coding Hangover: 숫자가 말하는 불편한 진실

2025년, "Vibe Coding Hangover"라는 현상이 본격적으로 보고되기 시작했습니다.

### 충격적인 통계들

- **45%의 AI 생성 코드에 보안 취약점 존재** (Veracode, 2025)
- **50,000줄 이상 시스템에서 AI 코드 디버깅에 41% 더 많은 시간 소요** (UK Tech Firms 연구)
- **18명의 CTO 중 16명이 AI 생성 코드로 인한 프로덕션 재해 경험** (Final Round AI 설문)
- **63%의 개발자가 AI 코드 디버깅에 직접 작성보다 더 많은 시간 소요 경험** (2025 조사)

### Flutter 프로젝트의 실제 사례

한 시니어 Flutter 개발자의 증언:

> "AI가 생성한 Provider 코드가 테스트에서는 완벽하게 동작했습니다. 하지만 실제 사용자 100명이 동시 접속하는 순간, 앱이 ANR(Application Not Responding)에 빠졌습니다. AI가 생성한 `StreamBuilder` 안에 또 다른 `StreamBuilder`를 중첩하고, 각각이 독립적으로 Firebase를 구독하고 있었거든요. 디버깅에 3일이 걸렸습니다."

### 왜 이런 일이 발생하는가?

AI는 **완성(completion)**에 최적화되어 있지, **확장성(scalability)**이나 **응집성(cohesion)**에 최적화되어 있지 않습니다. 에뮬레이터에서 동작하는 코드와 실제 사용자 기기에서 버티는 코드는 다릅니다.

더 근본적인 문제: **AI는 전체 코드를 한 번에 볼 수 없습니다.**

## 진짜 문제: AI의 한계는 '능력'이 아니라 '시야'

### Context Window의 한계

현재 가장 발전한 LLM도 128K~200K 토큰의 Context Window를 가집니다. 충분해 보이지만:

```
Flutter 프로젝트 규모별 토큰 사용량:
├── MVP (20개 화면): ~30,000 tokens ✅ 충분
├── 중형 앱 (50개 화면): ~150,000 tokens ⚠️ 한계
├── 대형 앱 (100개+ 화면): ~400,000 tokens ❌ 불가능
```

### 산만한 컨텍스트의 비극

AI에게 "주문 화면 수정해줘"라고 요청했을 때, 코드베이스 구조에 따라 극적인 차이가 발생합니다:

```
비구조화된 Flutter 프로젝트:
├── AI가 탐색해야 할 파일: 52개
├── 관련 없는 파일: 43개 (83%)
├── 토큰 낭비: ~40,000 tokens
└── 결과: AI 혼란, 엉뚱한 위젯 수정

구조화된 Flutter 프로젝트:
├── AI가 탐색해야 할 파일: 11개
├── 모두 관련 파일: 100%
├── 사용 토큰: ~6,500 tokens
└── 결과: 정확한 수정
```

FlowHunt의 연구가 이를 증명합니다:

> "300 토큰의 집중된 컨텍스트가 113,000 토큰의 산만한 컨텍스트보다 더 나은 성능을 발휘한다."

## 매일 반복되는 좌절의 패턴

구조화되지 않은 Flutter 프로젝트에서 AI와 협업하면 다음 패턴을 반복적으로 경험하게 됩니다:

- **컨텍스트 소멸**: 어젯밤 완벽하게 설명해준 Riverpod StateNotifier 기반 인증 로직을 오늘 아침에는 완전히 잊은 듯, "소셜 로그인 추가해줘"라고 하자 어제 대화는 전부 무시하고 GetX 기반의 새로운 인증 모듈을 통째로 만들어냅니다.

- **지능적 오지랖**: "결제 버튼 색상만 바꿔줘"라는 간단한 요청에, AI는 관련 없어 보이는 `PaymentRepository`의 API 호출 로직을 '개선'하고 응답 모델 구조까지 바꿔서 전체 테스트를 깨뜨립니다.

- **패턴 무시**: 프로젝트 전체에 적용된 `Either<Failure, T>` 에러 핸들링 패턴을 무시하고, 자신만의 `try-catch`와 nullable 타입을 수놓습니다.

- **과잉 리팩토링**: "이 위젯 내부 로직만 개선해줘"라고 했는데, 그 위젯을 사용하는 모든 상위 위젯의 props까지 바꿔버려 300줄짜리 PR을 만들어냅니다.

**AI가 똑똑하지 않은 게 아닙니다. 우리의 코드베이스가 AI에게 명확한 경계를 제공하지 못하는 것입니다.**

## 왜 Layer-based Clean Architecture만으로는 부족한가

"Clean Architecture 적용하면 되지 않나요?"

처음에는 저도 그렇게 생각했습니다:

```
lib/
├── domain/          # 의존성 없음, 순수 비즈니스 규칙
│   ├── entities/
│   ├── repositories/  # 추상 인터페이스
│   └── usecases/
├── data/            # domain 인터페이스 구현
│   ├── repositories/
│   ├── datasources/
│   └── models/
└── presentation/    # UI, 상태관리
    ├── screens/
    ├── widgets/
    └── providers/
```

일관성이 생기기 시작했습니다. 하지만 프로젝트가 커지면서 **새로운 문제**가 나타났습니다.

### 문제 1: 응집도 저하

'주문', '사용자', '결제', '배송' 기능이 추가되면:

```
lib/
├── domain/
│   ├── entities/
│   │   ├── user.dart
│   │   ├── order.dart
│   │   ├── payment.dart
│   │   ├── shipping.dart
│   │   └── ... (20개 이상)
│   └── usecases/
│       ├── create_user_usecase.dart
│       ├── create_order_usecase.dart
│       ├── process_payment_usecase.dart
│       └── ... (30개 이상)
```

AI에게 "주문 관련 컨텍스트를 파악해"라고 하면, **관련 없는 수많은 파일을 함께 탐색**하게 됩니다.

### 문제 2: Cross-feature 오염

`domain/entities` 폴더에 `Order`와 `User` 엔티티가 함께 있으면, AI가 '주문' 기능을 수정하다가 **`User` 엔티티에 `lastOrderId` 속성을 추가**하는 것은 너무 쉬운 일입니다.

```dart
// AI가 "주문 조회 최적화"를 하다가 추가한 코드
class User {
  final String id;
  final String email;
  final String name;
  final String? lastOrderId;  // 👈 주문 기능 수정하다 사용자 엔티티를 건드림!

  const User({
    required this.id,
    required this.email,
    required this.name,
    this.lastOrderId,
  });
}
```

### 문제 3: core 디렉토리의 비극

```dart
// 6개월 후의 core 폴더
core/
├── either.dart
├── failure.dart
├── validators/        # 온갖 validation 로직
├── formatters/        # 여러 feature에서 가져다 씀
├── helpers/           # "일단 여기 두자"의 무덤
├── constants/         # 모든 상수의 집합소
├── widgets/           # 어느 feature 소속인지 모호한 위젯들
└── mixins/            # 여기저기서 쓰이는 mixin들
```

AI에게는 이 모든 것이 '관련 컨텍스트'로 인식됩니다.

## 해결책: Feature-based Clean Architecture

Vibe Coding이 규모에서 실패하는 이유는 명확합니다: **AI가 "이 기능에만 집중해"라는 물리적 경계를 볼 수 없기 때문입니다.**

Feature-based Clean Architecture는 **수직적 분리(레이어) + 수평적 분리(기능)**를 결합합니다:

```
lib/
├── features/                      # 👈 모든 기능은 여기에 격리
│   ├── auth/
│   │   ├── domain/
│   │   │   ├── entities/
│   │   │   │   └── user.dart      # auth feature의 User만
│   │   │   ├── repositories/
│   │   │   │   └── auth_repository.dart
│   │   │   └── usecases/
│   │   │       ├── login_usecase.dart
│   │   │       └── register_usecase.dart
│   │   ├── data/
│   │   │   ├── models/
│   │   │   │   └── user_model.dart
│   │   │   ├── datasources/
│   │   │   │   └── auth_remote_datasource.dart
│   │   │   └── repositories/
│   │   │       └── auth_repository_impl.dart
│   │   ├── presentation/
│   │   │   ├── providers/
│   │   │   │   └── auth_provider.dart
│   │   │   ├── screens/
│   │   │   │   └── login_screen.dart
│   │   │   └── widgets/
│   │   │       └── login_form.dart
│   │   └── auth_api.dart          # 외부 공개 인터페이스
│   │
│   ├── order/
│   │   ├── domain/
│   │   ├── data/
│   │   ├── presentation/
│   │   └── order_api.dart
│   │
│   └── payment/
│       └── ...
│
└── core/                          # 👈 정말 순수한 코드만
    ├── either.dart
    ├── failure.dart
    └── usecase.dart
```

### 컨텍스트 효율성 비교

```
Layer-based로 "주문 기능 수정" 요청 시:
├── domain/entities/* (모든 엔티티)     ~8,000 tokens
├── domain/usecases/* (모든 UC)         ~12,000 tokens
├── presentation/screens/* (모든 화면)  ~20,000 tokens
└── 총 컨텍스트                         ~40,000 tokens ❌

Feature-based로 "주문 기능 수정" 요청 시:
├── features/order/domain/*             ~2,500 tokens
├── features/order/presentation/*       ~4,000 tokens
└── 총 컨텍스트                         ~6,500 tokens ✅
```

**6배의 컨텍스트 효율성 차이!**

## Feature 간 통신 규칙

Feature들이 서로 격리되면, 올바른 통신 방법이 필요합니다.

### 원칙: Feature는 다른 Feature의 내부에 직접 의존하면 안 된다

```dart
// ❌ 잘못된 방법: 다른 feature의 내부 직접 import
import 'package:app/features/auth/domain/usecases/get_user_usecase.dart';

// ✅ 올바른 방법: 공개된 인터페이스 사용
import 'package:app/features/auth/auth_api.dart';
```

### 해결책 1: 공개 API (Facade)

```dart
// lib/features/auth/auth_api.dart - auth feature의 유일한 외부 공개 인터페이스

// 외부에서 사용 가능한 타입들
export 'domain/entities/user.dart' show User;
export 'domain/entities/auth_status.dart' show AuthStatus;

// 외부에서 사용 가능한 Provider
export 'presentation/providers/auth_provider.dart' show AuthProvider, authProvider;

// 외부에서 호출 가능한 함수
String? getCurrentUserId() {
  // 내부 구현은 숨김
}

bool isAuthenticated() {
  // 내부 구현은 숨김
}
```

### 해결책 2: 이벤트 기반 통신

```dart
// lib/features/payment/domain/usecases/complete_payment_usecase.dart
class CompletePaymentUseCase {
  final PaymentRepository repository;
  final EventBus eventBus;

  CompletePaymentUseCase({
    required this.repository,
    required this.eventBus,
  });

  Future<Either<Failure, Payment>> call(String paymentId) async {
    final result = await repository.completePayment(paymentId);

    return result.fold(
      (failure) => Left(failure),
      (payment) {
        // 이벤트 발행 - notification feature가 구독
        eventBus.fire(PaymentCompletedEvent(
          paymentId: payment.id,
          userId: payment.userId,
          amount: payment.amount,
        ));
        return Right(payment);
      },
    );
  }
}
```

## Vibe Coding에서 AI-Assisted Engineering으로

Addy Osmani가 정확히 지적했듯이:

> "Vibe coding is not the same as AI-Assisted Engineering."

| Vibe Coding | AI-Assisted Engineering |
|-------------|------------------------|
| "동작하면 됐지" | "유지보수 가능해야 함" |
| 구조 없이 생성 | 명확한 아키텍처 안에서 생성 |
| 소규모에서만 유효 | 규모에 관계없이 지속 가능 |
| AI에게 전체 맡김 | AI에게 명확한 경계 제공 |

Feature-based Clean Architecture는 **Vibe Coding을 AI-Assisted Engineering으로 업그레이드**합니다.

## 실전: AI Agent에게 효과적으로 컨텍스트 전달하기

### 개선된 프롬프트 (Feature Scope 포함)

```
너는 Flutter Feature-based Clean Architecture 전문가야.

**Feature:** order (주문 처리)
**Scope:** 모든 변경은 `lib/features/order/` 디렉토리 내에서만 이뤄져야 해.

**Objective:** 사용자가 주문을 취소할 때 재고를 다시 채우는 로직을 추가해줘.

**Context Files:**
- lib/features/order/domain/usecases/cancel_order_usecase.dart (핵심 수정 파일)
- lib/features/order/domain/repositories/inventory_repository.dart (사용해야 할 인터페이스)
- lib/features/order/domain/entities/order.dart (참조용)

**Constraints:**
- 다른 feature의 코드를 직접 import하지 마
- 다른 feature의 데이터가 필요하면 해당 feature의 *_api.dart 사용
- 새로운 Repository가 필요하면 lib/features/order/domain/repositories/에 정의
- Either<Failure, T> 패턴을 따라줘

이제 cancel_order_usecase.dart를 수정해줘.
```

### 의존성 규칙 강제하기

```yaml
# analysis_options.yaml
analyzer:
  plugins:
    - custom_lint

linter:
  rules:
    - always_declare_return_types
    - avoid_dynamic_calls
    - prefer_const_constructors
```

```yaml
# melos.yaml (모노레포 사용 시)
packages:
  - features/auth
  - features/order
  - features/payment
  - core

command:
  bootstrap:
    dependencies:
      # order는 auth의 api.dart만 의존 가능
      features/order:
        - features/auth  # auth_api.dart만 export됨
        - core
```

## 개발자의 역할 변화

**과거의 개발자 역할:**
> "**어떻게(How)** 코드를 작성할 것인가"

**AI 시대의 개발자 역할:**
> "**어디서(Where)** 코드가 작성되어야 하는가"

```
[Vibe Coding]
개발자 → AI에게 요청 → 위젯 받음 → 🤞 기도 후 핫 리로드

[AI-Assisted Engineering]
개발자 → 경계 설정 → AI 코드 생성 → 경계 검증 → 배포
         (Feature +    (실행)        (가드레일)
          레이어)
```

## 결론: Vibe Coding Hangover의 해독제

Vibe Coding이 규모에서 실패하는 이유는 AI의 능력 부족이 아닙니다. **AI가 집중할 수 있는 명확한 경계를 제공하지 못하기 때문입니다.**

Feature-based Clean Architecture는:

1. **완벽한 Context 격리**: Feature 단위 분리로 불필요한 컨텍스트 원천 차단
2. **예측 가능한 변경**: 의존성 규칙 + Feature 경계로 영향 범위 이중 제한
3. **Cross-feature 오염 방지**: 물리적 분리로 AI의 "지능적 오지랖" 차단
4. **확장 가능한 협업**: 프로젝트가 커져도 AI 효율성 유지

---

**300 토큰의 집중된 컨텍스트가 113,000 토큰을 이기는 이유.**

그것은 **구조화된 지식**의 힘입니다.

Vibe Coding의 마법은 사라지지 않습니다. **올바른 구조 안에서, 그 마법은 지속 가능해집니다.**

---

**참고 자료**

- [Vibe Coding - Wikipedia](https://en.wikipedia.org/wiki/Vibe_coding)
- [Vibe Coding is not AI-Assisted Engineering - Addy Osmani](https://medium.com/@addyosmani/vibe-coding-is-not-the-same-as-ai-assisted-engineering-3f81088d5b98)
- [The Rise of Vibe Coding in 2025 - Emil](https://ecoemil.medium.com/the-rise-of-vibe-coding-in-2025-a-revolution-or-a-reckoning-4c2f7053ceef)
- [How AI Vibe Coding Is Destroying Junior Developers' Careers - Final Round AI](https://www.finalroundai.com/blog/ai-vibe-coding-destroying-junior-developers-careers)
- [The Clean Architecture - Robert C. Martin](https://blog.cleancoder.com/uncle-bob/2012/08/13/the-clean-architecture.html)
- [Context Engineering - FlowHunt](https://www.flowhunt.io/blog/context-engineering/)
- [Vibe Coding, Architecture & AI Agents - vFunction](https://vfunction.com/blog/vibe-coding-architecture-ai-agents/)

— woogi
