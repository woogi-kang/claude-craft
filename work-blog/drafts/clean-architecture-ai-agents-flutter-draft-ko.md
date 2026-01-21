---
title: "왜 AI가 작은 Flutter 앱은 잘 짜다가 앱이 커지면 망가질까"
slug: vibe-coding-trap-clean-architecture-flutter-ko
tags: ["vibe-coding", "clean-architecture", "flutter", "dart", "ai-agents", "context-engineering", "feature-based"]
seo_description: "AI가 생성한 Flutter 코드를 디버깅하느라 몇 주를 보냈다. 작은 앱에서는 완벽하게 돌아가던 코드가. Vibe Coding이 왜 규모가 커지면 무너지는지, Feature 기반 Clean Architecture가 어떻게 이걸 해결하는지 정리해봤다."
---

# 왜 AI가 작은 Flutter 앱은 잘 짜다가 앱이 커지면 망가질까

처음 Claude로 Flutter 앱을 만들던 날이 아직도 기억난다.

"Firebase 연동되는 간단한 TODO 앱 만들어줘." 2분 후, 돌아가는 앱이 나왔다. Material Design. 다크 모드. 실시간 동기화. 전부 다.

그때 생각했다. "잠깐, 이러면 Flutter 개발자 필요 없는 거 아냐?"

Andrej Karpathy가 2025년 2월에 이걸 "Vibe Coding"이라고 불렀다. 원하는 걸 설명하면 AI가 만들고, 핫 리로드 하고, 그냥 분위기 타면 된다. 모든 위젯을 이해할 필요 없다. 그냥... 돌아간다.

**그러다 앱이 50개 화면을 넘기면서 전부 무너졌다.**

## 숙취는 진짜다

나만 그런 게 아니었다. 2025년에 사람들이 이걸 "Vibe Coding Hangover"라고 부르기 시작했다.

숫자가 잔인하다:
- AI 생성 코드의 45%가 보안 취약점을 가지고 있다 (Veracode, 2025)
- 5만 줄 넘는 시스템에서 디버깅 시간 41% 증가
- 설문 응답 CTO 18명 중 16명이 AI 코드로 프로덕션 장애를 경험

한 Flutter 개발자의 이야기가 남의 일 같지 않았다:

> "AI가 생성한 Provider 코드가 테스트에서는 완벽하게 돌아갔어요. 근데 실제 사용자 100명이 동시 접속하니까 앱이 ANR로 멈췄습니다. AI가 StreamBuilder 안에 또 StreamBuilder를 넣었는데, 각각이 독립적으로 Firebase를 구독하고 있었거든요. 디버깅에 3일 걸렸어요."

나도 겪어봤다. AI가 만든 위젯이 맞아 보이고, 에뮬레이터에서 잘 돌아가다가, 실제 기기에서 터지는 거.

## 결국 이해한 것

문제는 AI가 멍청해서가 아니다. AI는 사실 무섭게 똑똑하다. 문제는 **AI가 코드베이스 전체를 한 번에 볼 수 없다**는 거다.

지금 가장 좋은 LLM들도 128K-200K 토큰 컨텍스트 윈도우를 가지고 있다. 많아 보이지만 계산해보면:

```
Flutter 프로젝트 크기 vs 토큰:
├── MVP (20개 화면): ~30,000 토큰 ✅ 여유
├── 중간 앱 (50개 화면): ~150,000 토큰 ⚠️ 빡빡함
├── 큰 앱 (100개 이상): ~400,000 토큰 ❌ 불가능
```

엉망인 코드베이스에서 "주문 화면 고쳐줘"라고 하면 이런 일이 벌어진다:

```
구조 없는 Flutter 프로젝트:
├── AI가 스캔해야 하는 파일: 52개
├── 실제로 관련 있는 것: 11개 (21%)
├── 낭비된 토큰: ~40,000
└── 결과: AI가 헷갈려서 엉뚱한 위젯 수정

구조 있는 Flutter 프로젝트:
├── AI가 스캔해야 하는 파일: 11개
├── 실제로 관련 있는 것: 11개 (100%)
├── 사용된 토큰: ~6,500
└── 결과: 정확한 수정
```

FlowHunt 연구가 내가 의심하던 걸 증명했다:

> "집중된 300 토큰이 흩어진 113,000 토큰을 이긴다."

이게 뼈 때렸다.

## 분명히 겪어봤을 짜증들

구조 없는 Flutter 프로젝트에서 AI랑 작업하면 아마 이런 경험 있을 거다:

**컨텍스트 치매.** 어제 우리 Riverpod StateNotifier 인증 플로우를 한 시간 동안 설명했다. 오늘 "소셜 로그인 추가해줘"라고 했더니 AI가 완전 새로운 GetX 기반 인증 모듈을 만들었다. 어제 얘기한 거 다 무시하고.

**도움인 척 하는 월권.** 버튼 색깔 바꿔달라고 했다. AI가 "도움이 될 것 같아서" PaymentRepository의 API 호출이랑 응답 모델까지 리팩토링했다. 테스트 전부 깨짐.

**패턴 맹인.** 우리 코드베이스 전체가 에러 처리에 `Either<Failure, T>`를 쓴다. AI는 자기 마음대로 `try-catch` 블록이랑 nullable 타입을 여기저기 뿌렸다.

**범위 인플레이션.** "이 위젯 하나만 최적화해줘." AI가 모든 상위 위젯의 props를 수정했다. 한 줄 고치는 건데 PR이 300줄.

AI가 고장난 게 아니다. **우리가 AI한테 명확한 경계를 안 주고 있는 거다.**

## 왜 일반 Clean Architecture로는 부족한가

"그냥 Clean Architecture 쓰면 되지 않아?"

나도 처음엔 그렇게 생각했다:

```
lib/
├── domain/          # 순수 비즈니스 로직
│   ├── entities/
│   ├── repositories/  # 추상 인터페이스
│   └── usecases/
├── data/            # domain 인터페이스 구현
│   ├── repositories/
│   ├── datasources/
│   └── models/
└── presentation/    # UI, 상태 관리
    ├── screens/
    ├── widgets/
    └── providers/
```

도움이 됐다. 근데 프로젝트가 커지니까 새로운 문제가 생겼다.

**문제 1: 응집도가 무너진다.**

'orders', 'users', 'payments', 'shipping' 추가하면 갑자기:

```
lib/
├── domain/
│   ├── entities/
│   │   ├── user.dart
│   │   ├── order.dart
│   │   ├── payment.dart
│   │   └── ... (20개 이상)
│   └── usecases/
│       ├── create_user_usecase.dart
│       ├── create_order_usecase.dart
│       └── ... (30개 이상)
```

AI한테 "주문" 물어보면 다른 것도 다 뒤져야 한다.

**문제 2: 교차 오염.**

`Order`랑 `User`가 같은 폴더에 있으면 AI가 주문 최적화하다가 슬쩍 User 엔티티에 `lastOrderId` 필드를 추가한다. 한두 번 본 게 아니다.

```dart
// AI가 주문 조회 "개선"하면서
class User {
  final String id;
  final String email;
  final String name;
  final String? lastOrderId;  // 👈 주문 작업하다가 User 건드림

  const User({
    required this.id,
    required this.email,
    required this.name,
    this.lastOrderId,
  });
}
```

**문제 3: "core" 폴더가 공동묘지가 된다.**

```dart
core/
├── either.dart
├── failure.dart
├── validators/        # 다 여기서 검증
├── formatters/        # 여러 feature가 여기 덤프
├── helpers/           # "일단 여기 넣자" 무덤
├── widgets/           # 이 공통 위젯들 주인이 누구지?
└── mixins/            # 모든 곳에서 쓰고 아무도 안 관리함
```

AI는 이걸 전부 관련 컨텍스트로 취급한다. 뭘 하든.

## 실제로 작동하는 것: Feature 기반 아키텍처

보면 단순하다: **AI가 무시할 수 없는 물리적 경계를 줘라.**

Feature 기반 아키텍처는 수직 레이어와 수평 feature 분리를 결합한다:

```
lib/
├── features/                      # 👈 전부 여기, 격리됨
│   ├── auth/
│   │   ├── domain/
│   │   │   ├── entities/
│   │   │   │   └── user.dart      # auth의 User만
│   │   │   ├── repositories/
│   │   │   │   └── auth_repository.dart
│   │   │   └── usecases/
│   │   ├── data/
│   │   │   ├── models/
│   │   │   ├── datasources/
│   │   │   └── repositories/
│   │   ├── presentation/
│   │   │   ├── providers/
│   │   │   ├── screens/
│   │   │   └── widgets/
│   │   └── auth_api.dart          # 공개 인터페이스
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
└── core/                          # 👈 진짜 공통만
    ├── either.dart
    └── failure.dart
```

컨텍스트 효율성 차이:

```
레이어 기반 "주문 고쳐줘":
├── domain/entities/* (전체 엔티티)     ~8,000 토큰
├── domain/usecases/* (전체)            ~12,000 토큰
├── presentation/screens/* (전체)       ~20,000 토큰
└── 총 컨텍스트                         ~40,000 토큰 ❌

Feature 기반 "주문 고쳐줘":
├── features/order/domain/*             ~2,500 토큰
├── features/order/presentation/*       ~4,000 토큰
└── 총 컨텍스트                         ~6,500 토큰 ✅
```

**6배 더 효율적.** 작은 개선이 아니다.

## Feature끼리 대화하게 만들기

Feature가 격리되어 있어도 통신은 해야 한다. 이게 작동한다.

**규칙: 다른 feature 내부를 절대 import하지 마라.**

```dart
// ❌ 하지 마
import 'package:app/features/auth/domain/usecases/get_user_usecase.dart';

// ✅ 이렇게 해
import 'package:app/features/auth/auth_api.dart';
```

**해결책 1: Public API (Facade)**

```dart
// lib/features/auth/auth_api.dart - 다른 feature가 import할 수 있는 유일한 파일

// 다른 feature가 쓸 수 있는 타입
export 'domain/entities/user.dart' show User;
export 'domain/entities/auth_status.dart' show AuthStatus;

// 다른 feature가 접근할 수 있는 Provider
export 'presentation/providers/auth_provider.dart' show AuthProvider, authProvider;

// 다른 feature가 호출할 수 있는 함수
String? getCurrentUserId() {
  // 구현은 숨김
}

bool isAuthenticated() {
  // 구현은 숨김
}
```

**해결책 2: 이벤트 기반 통신**

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
        // Notification feature가 이걸 구독
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

## 요즘 AI한테 프롬프트 주는 법

요즘 내 프롬프트는 이렇게 생겼다:

```
당신은 feature 기반 clean architecture 프로젝트에서 작업하는 Flutter 전문가입니다.

**Feature:** order (주문 처리)
**범위:** 모든 변경은 `lib/features/order/` 안에서만

**태스크:** 사용자가 주문 취소할 때 재고 복원 추가.

**관련 파일:**
- lib/features/order/domain/usecases/cancel_order_usecase.dart (이거 수정)
- lib/features/order/domain/repositories/inventory_repository.dart (이 인터페이스 사용)
- lib/features/order/domain/entities/order.dart (참조)

**규칙:**
- 다른 feature 내부에서 import 금지
- 다른 feature 데이터 필요하면? 그 feature의 *_api.dart 사용
- 새 repository는 lib/features/order/domain/repositories/에
- 모든 결과에 Either<Failure, T> 사용

cancel_order_usecase.dart를 업데이트하세요.
```

명확한 경계. 특정 파일. 명시적 규칙.

## 나한테 달라진 것

Addy Osmani가 정확히 짚었다:

> "Vibe Coding은 AI-Assisted Engineering이랑 다르다."

| Vibe Coding | AI-Assisted Engineering |
|-------------|------------------------|
| "돌아가면 배포해" | "유지보수 가능해야 해" |
| 구조 없이 생성만 | 명확한 아키텍처 안에서 생성 |
| 작은 규모에서만 작동 | 무한 확장 가능 |
| AI가 다 관리 | AI가 경계 안에서 작업 |

내 역할이 "이 위젯 어떻게 만들지"에서 "이 위젯 어디에 둬야 하지"로 바뀌었다.

```
[Vibe Coding]
개발자 → AI한테 물어봄 → 위젯 받음 → 🤞 핫 리로드하고 기도

[AI-Assisted Engineering]
개발자 → 경계 설정 → AI 생성 → 경계 검증 → 배포
          (Feature +    (실행)     (가드레일)
           레이어)
```

## 결론

Vibe Coding이 실패하는 건 AI가 Flutter 못 해서가 아니다. **우리가 명확한 경계를 안 주면 AI가 그걸 볼 수 없어서** 실패하는 거다.

Feature 기반 Clean Architecture가 주는 것:

1. **컨텍스트 격리** - AI가 필요한 것만 본다
2. **예측 가능한 변경** - 수정이 feature 경계 안에 머문다
3. **교차 오염 없음** - 물리적 분리가 "도움주려는" 월권을 막는다
4. **지속 가능한 확장** - 20개 화면에서도, 200개 화면에서도 작동

---

집중된 300 토큰이 흩어진 113,000개를 이긴다.

이게 구조화된 컨텍스트의 힘이다.

Vibe Coding의 마법이 사라질 필요 없다. **올바른 구조 안에서, 지속 가능해진다.**

---

**참고자료**

- [Vibe Coding - Wikipedia](https://en.wikipedia.org/wiki/Vibe_coding)
- [Vibe Coding is not AI-Assisted Engineering - Addy Osmani](https://medium.com/@addyosmani/vibe-coding-is-not-the-same-as-ai-assisted-engineering-3f81088d5b98)
- [The Rise of Vibe Coding in 2025 - Emil](https://ecoemil.medium.com/the-rise-of-vibe-coding-in-2025-a-revolution-or-a-reckoning-4c2f7053ceef)
- [How AI Vibe Coding Is Destroying Junior Developers' Careers - Final Round AI](https://www.finalroundai.com/blog/ai-vibe-coding-destroying-junior-developers-careers)
- [The Clean Architecture - Robert C. Martin](https://blog.cleancoder.com/uncle-bob/2012/08/13/the-clean-architecture.html)
- [Context Engineering - FlowHunt](https://www.flowhunt.io/blog/context-engineering/)

— woogi
