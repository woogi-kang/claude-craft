---
title: "당신의 AI 코딩이 실패하는 구조적 이유"
subtitle: "Vibe Coding의 함정에서 Context Engineering으로 탈출하기"
slug: context-engineering-ai-assisted-flutter-development
tags: ["context-engineering", "vibe-coding", "clean-architecture", "ai-agents", "flutter", "dart"]
seo_description: "Vibe Coding이 대규모 Flutter 프로젝트에서 실패하는 진짜 이유. MVC, MVVM, MVP가 AI 코딩에서 왜 비효율적인지, Feature-based Architecture로 어떻게 해결하는지 실전 가이드."
canonical_url: ""
cover_image: ""
---

# 당신의 AI 코딩이 실패하는 구조적 이유

AI 코딩으로 시작한 프로젝트, 왜 항상 비슷한 시점에 무너질까?

20개 화면까지는 마법처럼 잘 돌아간다. 30개쯤 되면 뭔가 이상해지기 시작하고. 50개를 넘어가면? 그때부터 AI가 내 코드를 이해 못하기 시작한다.

나도 똑같이 당했다. Claude한테 TODO 앱 만들어달라고 했을 때, 2분 만에 완성된 결과물 보고 "이거 진짜 개발자 필요 없겠는데?"라고 생각했다. 다크모드, 실시간 동기화, 반응형 UI까지.

그로부터 2개월 뒤, 50개 화면짜리 앱 앞에서 2일째 밤을 새고 있었다.

**AI가 만든 코드가 AI도 이해 못하는 스파게티가 돼버린 거다.**

Andrej Karpathy가 2025년 2월에 이걸 "Vibe Coding"이라고 불렀다. 원하는 걸 말하면 AI가 만들어주고, 핫 리로드 누르면서 분위기 타는 거다. 문제는, 이 방식이 특정 규모를 넘어서면 구조적으로 실패할 수밖에 없다는 거다.

## 바이브 코딩 숙취, 나만 겪은 게 아니었다

2025년 들어서 "Vibe Coding Hangover"라는 말이 돌기 시작했다. 숙취. 딱 맞는 표현이다.

숫자로 보면 더 무섭다:
- Veracode 2025 보고서에 따르면, AI 도구로 생성된 코드 샘플 분석 결과 약 **45%에서 보안 취약점**이 발견됐다
- 5만 라인 이상 시스템에서 **41% 더 많은 디버깅 시간** 소요
- 설문한 CTO 18명 중 **16명이 AI 코드로 인한 프로덕션 사고** 경험

한 Flutter 개발자가 공유한 이야기가 남의 일 같지 않았다:

> "AI가 만든 Provider 로직이 에뮬레이터에선 완벽했어요. 근데 실제 유저 100명이 동시에 접속하니까 상태 동기화 버그에 메모리 누수까지. dispose 처리를 제대로 안 한 거였는데, 디버깅하는 데 3일 걸렸습니다."

나도 겪어봤다. AI가 짠 위젯이 에뮬레이터에선 잘 돌다가 실기기에서 터지는 거. 그때마다 "이거 내가 처음부터 짰으면 더 빨랐겠다" 싶었다.

## 진짜 문제가 뭔지 깨닫기까지

AI가 멍청해서 그런 게 아니다. 오히려 무섭게 똑똑하다. 문제는 **AI가 내 코드베이스 전체를 한 번에 볼 수 없다**는 거다.

지금 가장 좋은 LLM도 컨텍스트 윈도우가 128K~200K 토큰이다. 많아 보이지? 계산해보면 얘기가 달라진다.

```
프로젝트 규모별 토큰 수:
├── MVP (20개 화면): ~30,000 토큰 --- 여유 있음
├── 중간 규모 (50개 화면): ~150,000 토큰 --- 빠듯함
├── 대형 (100개 이상): ~400,000 토큰 --- 불가능
```

AI한테 "주문 화면 수정해줘"라고 하면, 정리 안 된 프로젝트에선 이런 일이 벌어진다:

```
정리 안 된 프로젝트:
├── AI가 스캔한 파일: 52개
├── 실제로 관련 있는 파일: 11개 (21%)
├── 낭비된 토큰: ~40,000
└── 결과: AI가 헷갈려서 엉뚱한 파일 수정

정리된 프로젝트:
├── AI가 스캔한 파일: 11개
├── 실제로 관련 있는 파일: 11개 (100%)
├── 사용된 토큰: ~6,500
└── 결과: 정확한 수정
```

FlowHunt 연구에서 이런 문장이 나왔는데, 머리를 한 대 맞은 기분이었다:

> **"300개의 집중된 토큰이 113,000개의 흩어진 토큰보다 낫다."**

이게 핵심이다. Context Engineering의 본질.

## 내가 써봤던 아키텍처들, 왜 다 AI랑 안 맞았나

여기서 문제가 생겼다. "그러면 코드 정리 잘하면 되는 거 아니야?"

맞는 말이다. 근데 어떻게 정리해야 AI가 효율적으로 일할 수 있을까?

나도 지금까지 여러 아키텍처 패턴을 써봤다. MVC로 시작해서 MVVM이 좋다길래 바꿔봤고, MVP도 해봤고, Clean Architecture가 답이라길래 그것도 적용했다. 다 나름의 장점은 있었다.

근데 AI 에이전트 코딩 시대에 와서 보니까, 이 전통적인 패턴들이 **토큰 효율성** 측면에서는 전부 문제가 있더라.

### MVC: Massive Controller의 비극

Flutter에서 MVC 비슷하게 구조 잡으면 대충 이렇게 된다:

```
lib/
├── models/
│   ├── user.dart
│   ├── order.dart
│   └── payment.dart
├── views/
│   ├── user_view.dart
│   ├── order_view.dart
│   └── payment_view.dart
└── controllers/
    ├── user_controller.dart
    ├── order_controller.dart    # 점점 비대해짐
    └── payment_controller.dart
```

처음엔 깔끔하다. 근데 프로젝트가 커지면 Controller가 괴물이 된다. "Massive Controller" 문제. 주문 로직, 재고 확인, 결제 연동, 알림 처리... 전부 `order_controller.dart` 한 파일에 들어간다.

AI한테 "주문 취소 기능 추가해줘"라고 하면?

(참고: 아래 토큰 수치는 평균적인 중간 규모 Flutter 프로젝트 기준, 파일당 약 300-600토큰(코드 + 주석)을 가정한 추정치다. 실제 프로젝트마다 다를 수 있지만 상대적 비율은 유사하다.)

```
MVC에서 "주문 취소" 구현:
├── order_controller.dart (1,500 토큰) - 모든 주문 로직이 여기
├── order.dart (500 토큰)
├── user.dart (400 토큰) - 왜 로드됨? 사용자 정보 참조하니까
├── payment.dart (600 토큰) - 왜? 환불 로직이 필요하니까
├── order_view.dart (800 토큰)
└── 총: ~3,800 토큰 (실제 필요한 건 ~2,000)
```

Controller 하나 수정하는데 Model이랑 View까지 다 끌려온다. AI 입장에서 "주문 취소"만 고치고 싶은데 결제, 유저, UI 코드까지 전부 읽어야 한다.

### MVVM: ViewModel 의존성 지옥

"MVVM이 테스트하기 좋다더라." 맞는 말이다. 그래서 바꿔봤다.

```
lib/
├── models/
│   ├── user_model.dart
│   ├── order_model.dart
│   └── payment_model.dart
├── views/
│   └── order_screen.dart
├── viewmodels/
│   ├── user_viewmodel.dart
│   ├── order_viewmodel.dart    # UserViewModel 의존
│   └── payment_viewmodel.dart  # OrderViewModel 의존
└── bindings/
    └── order_binding.dart
```

문제는 ViewModel들이 서로 의존한다는 거다. `OrderViewModel`이 `UserViewModel`을 참조하고, `PaymentViewModel`이 `OrderViewModel`을 참조하고...

```dart
// order_viewmodel.dart
class OrderViewModel extends ChangeNotifier {
  final UserViewModel userViewModel;  // 의존
  final PaymentService paymentService; // 의존

  OrderViewModel({
    required this.userViewModel,
    required this.paymentService,
  });

  Future<void> cancelOrder(String orderId) async {
    final user = userViewModel.currentUser;  // User 데이터 필요
    // ...
  }
}
```

AI한테 "주문 취소 로직 수정해줘"라고 하면:

```
MVVM에서 "주문 취소" 수정:
├── order_viewmodel.dart (1,200 토큰)
├── user_viewmodel.dart (900 토큰) - 의존 관계라 로드됨
├── payment_service.dart (700 토큰) - 의존 관계라 로드됨
├── order_model.dart (400 토큰)
├── user_model.dart (350 토큰) - 왜? UserViewModel이 참조하니까
├── order_binding.dart (300 토큰)
└── 총: ~3,850 토큰
```

바인딩 로직이 분산되어 있어서 AI가 전체 흐름을 파악하기 어렵다. 하나의 ViewModel만 수정하고 싶은데 연쇄적으로 다른 ViewModel까지 끌려온다.

### MVP: Presenter-View 결합의 함정

"MVP가 테스트 용이성이 제일 좋다더라." 그래서 해봤다.

```
lib/
├── models/
│   └── order.dart
├── views/
│   ├── order_view.dart
│   └── order_view_interface.dart  # View 인터페이스
├── presenters/
│   └── order_presenter.dart       # View 인터페이스에 강결합
```

```dart
// order_view_interface.dart
abstract class OrderViewInterface {
  void showLoading();
  void hideLoading();
  void showOrders(List<Order> orders);
  void showError(String message);
  void showCancelSuccess();
  void showCancelError(String reason);
  // ... 계속 늘어남
}

// order_presenter.dart
class OrderPresenter {
  final OrderViewInterface view;  // View 인터페이스에 강하게 결합

  void cancelOrder(String orderId) async {
    view.showLoading();
    try {
      await repository.cancel(orderId);
      view.showCancelSuccess();
    } catch (e) {
      view.showCancelError(e.toString());
    }
  }
}
```

Presenter가 View 인터페이스에 강하게 결합되어 있다. AI가 Presenter 로직 수정할 때 View 인터페이스까지 같이 봐야 한다. "새 에러 케이스 추가해줘"라고 하면 인터페이스 메서드도 추가해야 하고, 구현체도 수정해야 한다.

```
MVP에서 "주문 취소 에러 처리 개선":
├── order_presenter.dart (1,000 토큰)
├── order_view_interface.dart (600 토큰) - 반드시 같이 봐야 함
├── order_view.dart (800 토큰) - 인터페이스 구현체
├── order.dart (400 토큰)
└── 총: ~2,800 토큰
```

테스트 용이성은 좋다. 근데 AI 컨텍스트 효율성은 낮다.

### 레이어 기반 Clean Architecture: 수평 분리의 한계

Clean Architecture 원칙 자체는 훌륭하다. 의존성 역전, 관심사 분리, 테스트 용이성. 다 맞는 말이다. 나도 그래서 도입했다.

근데 문제는 **레이어로만 나누어 구현했을 때** 생긴다.

```
lib/
├── domain/           # 비즈니스 로직
│   ├── entities/
│   │   ├── user.dart
│   │   ├── order.dart
│   │   └── payment.dart
│   ├── repositories/
│   │   └── order_repository.dart
│   └── usecases/
│       ├── get_orders.dart
│       ├── cancel_order.dart
│       └── process_payment.dart
├── data/             # 데이터 구현
│   ├── models/
│   │   ├── user_dto.dart
│   │   ├── order_dto.dart
│   │   └── payment_dto.dart
│   ├── repositories/
│   │   └── order_repository_impl.dart
│   └── datasources/
│       └── order_remote_datasource.dart
└── presentation/     # UI
    ├── pages/
    │   ├── user_page.dart
    │   ├── order_page.dart
    │   └── payment_page.dart
    ├── widgets/
    └── providers/
        └── order_provider.dart
```

레이어는 깔끔하게 분리됐다. 근데 **기능별 격리가 안 된다.**

`domain/entities/`에 user, order, payment가 전부 섞여 있다. AI한테 "주문" 작업 시키면:

```
레이어 기반에서 "주문 취소":
├── domain/entities/order.dart (400 토큰)
├── domain/entities/user.dart (350 토큰) - 같은 폴더니까 로드됨
├── domain/entities/payment.dart (300 토큰) - 같은 폴더니까
├── domain/usecases/cancel_order.dart (500 토큰)
├── domain/usecases/get_orders.dart (400 토큰) - 같은 폴더
├── domain/usecases/process_payment.dart (450 토큰) - 같은 폴더
├── data/repositories/order_repository_impl.dart (600 토큰)
├── data/models/order_dto.dart (300 토큰)
├── presentation/providers/order_provider.dart (500 토큰)
├── presentation/pages/order_page.dart (800 토큰)
└── 총: ~4,600 토큰 (실제 필요: ~2,400)
```

수평 레이어 분리는 됐지만, **수직 기능 분리가 안 됐다.** AI가 `domain/entities/` 폴더 스캔하면 주문이랑 관계없는 user, payment 엔티티까지 전부 로드한다.

결론부터 말하면, Clean Architecture와 Feature-based 구조는 **대립 관계가 아니라 조합 관계**다. Clean Architecture의 레이어 원칙(domain/data/presentation)을 유지하면서, 각 Feature 안에서 이 레이어를 적용하면 된다. 뒤에서 다룰 Feature-based Clean Architecture가 바로 이 조합이다.

## 공통된 문제: 물리적 경계의 부재

네 가지 아키텍처를 다 써봤는데, AI 코딩 관점에서 공통된 문제가 있었다:

**1. 기능 경계가 논리적이지, 물리적이지 않다**

MVC의 Controller, MVVM의 ViewModel, MVP의 Presenter, Clean Architecture의 UseCase... 전부 "레이어"로 나눈다. 근데 AI는 레이어가 아니라 **폴더와 파일**을 본다.

**2. 관련 없는 코드가 같은 폴더에 있다**

`entities/`에 user도 있고 order도 있고 payment도 있다. AI 입장에서 "주문" 작업인데 전부 스캔해야 한다.

**3. 의존성이 기능을 넘나든다**

OrderViewModel이 UserViewModel을 참조하고, CancelOrderUseCase가 PaymentService를 호출하고... 하나 수정하려면 연관된 걸 전부 로드해야 한다.

```
토큰 효율성 비교:

MVC         → 3,800 토큰 (효율 53%)
MVVM        → 3,850 토큰 (효율 52%)
MVP         → 2,800 토큰 (효율 71%)
Clean Arch  → 4,600 토큰 (효율 52%)

이상적 수치 → ~2,000 토큰 (효율 100%)
```

이쯤 되니까 깨달았다. **아키텍처의 목적이 달라져야 한다.** 예전엔 "테스트 용이성", "관심사 분리"가 중요했다. AI 시대엔 **"컨텍스트 효율성"**이 추가됐다.

## Feature-based Architecture: AI가 무시할 수 없는 경계

해결책은 깨닫고 나면 단순하다: **AI가 무시할 수 없는 물리적 경계를 만들어주자.**

Feature-based Clean Architecture는 수직(레이어)과 수평(기능) 분리를 결합한다.

```
lib/
├── features/
│   ├── auth/
│   │   ├── domain/
│   │   │   ├── entities/
│   │   │   │   └── user.dart
│   │   │   ├── repositories/
│   │   │   │   └── auth_repository.dart
│   │   │   └── usecases/
│   │   │       └── login_usecase.dart
│   │   ├── data/
│   │   │   ├── models/
│   │   │   │   └── user_dto.dart
│   │   │   ├── repositories/
│   │   │   │   └── auth_repository_impl.dart
│   │   │   └── datasources/
│   │   │       └── auth_remote_datasource.dart
│   │   ├── presentation/
│   │   │   ├── pages/
│   │   │   │   └── login_page.dart
│   │   │   ├── widgets/
│   │   │   │   └── login_form.dart
│   │   │   └── providers/
│   │   │       └── auth_provider.dart
│   │   └── auth_api.dart              # Public API
│   │
│   ├── order/
│   │   ├── domain/
│   │   │   ├── entities/
│   │   │   │   └── order.dart
│   │   │   └── usecases/
│   │   │       ├── get_orders_usecase.dart
│   │   │       └── cancel_order_usecase.dart
│   │   ├── data/
│   │   ├── presentation/
│   │   └── order_api.dart             # Public API
│   │
│   └── payment/
│       ├── domain/
│       ├── data/
│       ├── presentation/
│       └── payment_api.dart           # Public API
│
└── core/
    ├── network/
    │   └── dio_client.dart
    ├── error/
    │   └── failures.dart
    └── utils/
        └── either.dart
```

핵심은 **각 Feature가 자체 domain/data/presentation을 갖는다**는 거다.

### Public API: Feature의 유일한 출입구

```dart
// lib/features/auth/auth_api.dart
// 다른 Feature가 auth를 사용할 때 이 파일만 import

// Entities (외부 노출 가능한 것만)
export 'domain/entities/user.dart' show User;

// Providers (상태 접근)
export 'presentation/providers/auth_provider.dart' show authProvider;

// 편의 함수 (내부 구현 숨김)
String? getCurrentUserId() {
  // 구현은 숨기고 인터페이스만 노출
  return _authService.currentUser?.id;
}

bool isAuthenticated() {
  return _authService.isLoggedIn;
}
```

```dart
// lib/features/order/presentation/pages/order_page.dart
import 'package:myapp/features/auth/auth_api.dart';  // Public API만 import
// import 'package:myapp/features/auth/domain/entities/user.dart';  // 직접 접근 금지!

class OrderPage extends ConsumerWidget {
  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final authState = ref.watch(authProvider);

    if (!isAuthenticated()) {
      return LoginPromptWidget();
    }

    // ...
  }
}
```

### 토큰 효율성 비교

이제 같은 "주문 취소" 작업을 해보자:

```
Feature-based에서 "주문 취소":
├── features/order/domain/entities/order.dart (400 토큰)
├── features/order/domain/usecases/cancel_order_usecase.dart (500 토큰)
├── features/order/data/repositories/order_repository_impl.dart (600 토큰)
├── features/order/presentation/providers/order_provider.dart (500 토큰)
└── 총: ~2,000 토큰 (효율 100%)

vs 레이어 기반: ~4,600 토큰 (효율 43%)
```

**2.3배 효율적이다.** AI가 볼 필요 없는 user, payment 관련 코드가 물리적으로 분리되어 있으니까 아예 로드가 안 된다.

### 병렬 작업의 끝판왕: Git Worktree

Feature-based 구조의 또 다른 장점이 있다. **AI 에이전트 여러 개를 동시에 돌릴 수 있다.**

기존 구조에서 AI 에이전트 두 개를 동시에 돌리면? 같은 파일 건드릴 확률이 높다. 충돌 지옥.

근데 Feature가 물리적으로 분리되어 있으면?

Git Worktree가 뭔지 모르는 사람을 위해 간단히 설명하면, 하나의 Git 저장소에서 여러 브랜치를 **동시에 다른 폴더로 체크아웃**할 수 있게 해주는 기능이다. 보통은 브랜치 전환하려면 현재 작업을 커밋하거나 stash해야 하는데, worktree를 쓰면 그냥 다른 폴더로 가면 된다.

```bash
# 메인 브랜치에서 worktree 생성
git worktree add ../myapp-order feature/order-cancel
git worktree add ../myapp-payment feature/payment-refund
```

```
myapp/                    # 메인 (auth 작업 중)
myapp-order/             # AI Agent 1: 주문 취소 기능
myapp-payment/           # AI Agent 2: 환불 기능
```

각 worktree에서 다른 AI 에이전트가 작업해도 **서로 다른 Feature 폴더**를 건드리니까 충돌이 안 난다.

실제로 이렇게 쓴다:
- Agent 1: `lib/features/order/` 전담
- Agent 2: `lib/features/payment/` 전담
- Agent 3: `lib/features/notification/` 전담

머지할 때도 깔끔하다. 각 Feature가 독립적이니까 conflict가 거의 없다.

Vibe Coding에선 상상도 못할 일이다. 구조 없이 AI 여러 개 돌리면? 같은 `utils.dart` 파일을 세 에이전트가 동시에 수정하는 참사가 벌어진다.

### Flutter 상태관리와의 통합

Riverpod을 쓴다면:

```dart
// lib/features/order/presentation/providers/order_provider.dart
import 'package:riverpod_annotation/riverpod_annotation.dart';
import '../../domain/usecases/cancel_order_usecase.dart';

part 'order_provider.g.dart';

@riverpod
class OrderNotifier extends _$OrderNotifier {
  @override
  AsyncValue<List<Order>> build() {
    return const AsyncValue.loading();
  }

  Future<void> cancelOrder(String orderId) async {
    state = const AsyncValue.loading();

    final useCase = ref.read(cancelOrderUseCaseProvider);
    final result = await useCase.execute(orderId);

    result.fold(
      (failure) => state = AsyncValue.error(failure, StackTrace.current),
      (success) => _refreshOrders(),
    );
  }
}
```

Provider를 쓴다면:

```dart
// lib/features/order/presentation/providers/order_provider.dart
class OrderProvider extends ChangeNotifier {
  final CancelOrderUseCase _cancelOrderUseCase;

  List<Order> _orders = [];
  bool _isLoading = false;

  List<Order> get orders => _orders;
  bool get isLoading => _isLoading;

  Future<void> cancelOrder(String orderId) async {
    _isLoading = true;
    notifyListeners();

    final result = await _cancelOrderUseCase.execute(orderId);

    result.fold(
      (failure) => _handleError(failure),
      (success) => _refreshOrders(),
    );

    _isLoading = false;
    notifyListeners();
  }
}
```

BLoC을 쓴다면:

```dart
// lib/features/order/presentation/bloc/order_bloc.dart
class OrderBloc extends Bloc<OrderEvent, OrderState> {
  final CancelOrderUseCase cancelOrderUseCase;

  OrderBloc({required this.cancelOrderUseCase}) : super(OrderInitial()) {
    on<CancelOrderRequested>(_onCancelOrder);
  }

  Future<void> _onCancelOrder(
    CancelOrderRequested event,
    Emitter<OrderState> emit,
  ) async {
    emit(OrderLoading());

    final result = await cancelOrderUseCase.execute(event.orderId);

    result.fold(
      (failure) => emit(OrderError(failure.message)),
      (success) => emit(OrderCancelled(event.orderId)),
    );
  }
}
```

어떤 상태관리를 쓰든, **feature 폴더 안에 격리된다.** AI가 order 작업할 때 auth나 payment의 BLoC/Provider를 건드릴 이유가 없다.

### 어떤 상태관리를 선택할까?

| 상태관리 | 적합한 경우 | AI 컨텍스트 효율성 |
|---------|------------|-------------------|
| Riverpod | 코드 생성으로 보일러플레이트 최소화, 타입 안전성 중시 | 높음 (코드 생성 파일 분리) |
| Provider | 간단한 앱, 러닝커브 낮음 | 중간 |
| BLoC | 복잡한 상태 흐름, 이벤트 기반 로직 | 높음 (Event/State 분리) |

### 공유 상태는 어떻게?

Feature가 완전히 독립적일 순 없다. 인증 상태 같은 건 전역으로 필요하다.

```dart
// lib/features/order/presentation/pages/order_page.dart
import 'package:myapp/features/auth/auth_api.dart';

class OrderPage extends ConsumerWidget {
  @override
  Widget build(BuildContext context, WidgetRef ref) {
    // auth Feature의 public API를 통해 상태 접근
    final authState = ref.watch(authProvider);
    final currentUser = authState.user;

    if (currentUser == null) {
      return const LoginPromptWidget();
    }

    // 주문 목록은 이 Feature 내부 Provider 사용
    final orders = ref.watch(orderListProvider(currentUser.id));
    // ...
  }
}
```

핵심: 다른 Feature의 상태는 `*_api.dart`를 통해서만 접근. 내부 구현에 직접 의존하지 않는다.

### Flutter 위젯 트리와 컨텍스트 경계

Flutter의 위젯 트리 특성상 컨텍스트 경계가 더 명확해진다:

```dart
// lib/features/order/presentation/pages/order_detail_page.dart
class OrderDetailPage extends StatelessWidget {
  final String orderId;

  const OrderDetailPage({required this.orderId});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: Text('주문 상세')),
      body: Column(
        children: [
          // 이 Feature 내부 위젯만 사용
          OrderInfoCard(orderId: orderId),
          OrderItemList(orderId: orderId),
          OrderActionButtons(orderId: orderId),
        ],
      ),
    );
  }
}

// lib/features/order/presentation/widgets/order_action_buttons.dart
class OrderActionButtons extends ConsumerWidget {
  final String orderId;

  const OrderActionButtons({required this.orderId});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    return Row(
      children: [
        ElevatedButton(
          onPressed: () => ref.read(orderProvider.notifier).cancelOrder(orderId),
          child: Text('주문 취소'),
        ),
      ],
    );
  }
}
```

위젯도 feature 폴더 안에 있으니까, AI가 "주문 취소 버튼 디자인 수정해줘"라고 하면 `features/order/presentation/widgets/`만 보면 된다.

## 기능 간 통신: 이벤트 버스 패턴

기능이 격리되면 서로 어떻게 대화할까?

**절대 다른 기능의 내부를 import하지 말 것.**

```dart
// 하지 마
import 'package:myapp/features/auth/domain/entities/user.dart';
import 'package:myapp/features/auth/data/datasources/auth_local_datasource.dart';

// 이렇게
import 'package:myapp/features/auth/auth_api.dart';
```

**이벤트 버스로 느슨한 결합:**

```dart
// lib/core/events/event_bus.dart
class EventBus {
  static final EventBus _instance = EventBus._internal();
  factory EventBus() => _instance;
  EventBus._internal();

  final _controller = StreamController<AppEvent>.broadcast();

  Stream<T> on<T extends AppEvent>() {
    return _controller.stream.where((event) => event is T).cast<T>();
  }

  void emit(AppEvent event) {
    _controller.add(event);
  }

  void dispose() {
    _controller.close();
  }
}

// lib/core/events/app_events.dart
abstract class AppEvent {}

class PaymentCompletedEvent extends AppEvent {
  final String paymentId;
  final String orderId;
  final int amount;

  PaymentCompletedEvent({
    required this.paymentId,
    required this.orderId,
    required this.amount,
  });
}

class OrderCancelledEvent extends AppEvent {
  final String orderId;
  final String reason;

  OrderCancelledEvent({
    required this.orderId,
    required this.reason,
  });
}
```

```dart
// lib/features/payment/domain/usecases/complete_payment_usecase.dart
class CompletePaymentUseCase {
  final PaymentRepository repository;
  final EventBus eventBus;

  CompletePaymentUseCase({
    required this.repository,
    required this.eventBus,
  });

  Future<Either<Failure, Payment>> execute(String paymentId) async {
    final result = await repository.completePayment(paymentId);

    result.fold(
      (failure) => null,
      (payment) {
        // 결제 완료 이벤트 발행
        eventBus.emit(PaymentCompletedEvent(
          paymentId: payment.id,
          orderId: payment.orderId,
          amount: payment.amount,
        ));
      },
    );

    return result;
  }
}
```

```dart
// lib/features/notification/presentation/providers/notification_provider.dart
class NotificationProvider extends ChangeNotifier {
  late final StreamSubscription _paymentSubscription;
  late final StreamSubscription _orderSubscription;

  NotificationProvider(EventBus eventBus) {
    _paymentSubscription = eventBus.on<PaymentCompletedEvent>().listen((event) {
      _showNotification('결제 완료: ${event.amount}원');
    });

    _orderSubscription = eventBus.on<OrderCancelledEvent>().listen((event) {
      _showNotification('주문 취소됨: ${event.reason}');
    });
  }

  void _showNotification(String message) {
    // 알림 표시 로직
  }

  @override
  void dispose() {
    _paymentSubscription.cancel();
    _orderSubscription.cancel();
    super.dispose();
  }
}
```

payment Feature는 notification Feature를 모른다. 그냥 이벤트만 발행한다. notification Feature는 관심 있는 이벤트를 구독해서 처리한다.

AI가 payment 작업할 때 notification 코드를 건드릴 이유가 없어진다.

### 이벤트 버스의 트레이드오프

물론 이벤트 버스도 만능은 아니다.

**단점:**
- 이벤트 흐름 추적이 어려움 (누가 발행하고 누가 구독하는지 코드만 보면 안 보임)
- 타입 안전성 약화 (런타임 에러 가능성)
- 암묵적 의존성 (컴파일 타임에 의존성 파악 어려움)

**대안:**
- 이벤트 로깅 미들웨어 추가
- 개발 모드에서 이벤트 플로우 시각화
- 복잡도가 높아지면 Riverpod의 `ref.listen`이나 BLoC의 명시적 의존성 주입 고려

결국 트레이드오프다. AI 컨텍스트 효율성 vs 디버깅 용이성. 프로젝트 규모와 팀 상황에 맞게 선택하면 된다.

**언제 무엇을 쓸까?**

| 상황 | 권장 방식 |
|------|----------|
| 1:N 통신, 느슨한 결합 필요 | 이벤트 버스 |
| 1:1 관계 명확, 흐름 추적 중요 | Public API 직접 호출 |
| 복잡한 상태 의존성 | Riverpod `ref.listen` 또는 BLoC 의존성 주입 |

## 내 AI 프롬프트가 달라졌다

요즘 내 프롬프트는 이렇게 생겼다:

```
Feature-based Clean Architecture Flutter 프로젝트에서 작업 중.

**Feature:** order (주문 처리)
**범위:** 모든 변경은 `lib/features/order/` 안에서만

**작업:** 사용자가 주문 취소하면 재고 복구 이벤트 발행하기

**관련 파일:**
- lib/features/order/domain/usecases/cancel_order_usecase.dart (수정)
- lib/features/order/domain/entities/order.dart (참조)
- lib/core/events/app_events.dart (OrderCancelledEvent 추가)

**규칙:**
- 다른 Feature 내부 직접 import 금지
- 다른 Feature 데이터 필요하면 해당 Feature의 *_api.dart 사용
- 새 Provider는 lib/features/order/presentation/providers/에
- Either<Failure, T> 패턴으로 에러 처리
- 재고 복구는 이벤트로 inventory Feature에 알림

cancel_order_usecase.dart 업데이트해줘.
```

명확한 경계. 구체적인 파일. 명시적인 규칙.

AI가 범위 밖으로 나가려고 하면 내가 바로 알 수 있다. "왜 payment 폴더 건드렸어?" 물어볼 수 있게 됐다.

## 개발자 역할이 바뀌었다

Addy Osmani가 정확히 짚었다:

> "Vibe Coding과 AI-Assisted Engineering은 다르다."

| Vibe Coding | AI-Assisted Engineering |
|-------------|------------------------|
| "돌아가면 배포" | "유지보수 가능해야 함" |
| 구조 없이 생성 | 명확한 아키텍처 안에서 생성 |
| 소규모에서만 작동 | 무한히 확장 가능 |
| AI가 모든 걸 결정 | AI가 경계 안에서 작업 |

내 역할이 바뀌었다. "이 위젯 어떻게 만들지"에서 **"이 위젯 어디에 둘지"**로.

```
[Vibe Coding]
개발자 → AI한테 요청 → 코드 받음 → 핫 리로드하고 기도

[AI-Assisted Engineering]
개발자 → 경계 설정 → AI가 생성 → 경계 검증 → 배포
    (Feature +    (실행)    (가드레일)
        레이어)
```

아키텍처가 생산성의 핵심 레버가 됐다. 좋은 구조가 있으면 AI는 기가 막히게 일한다. 구조가 없으면 AI는 제멋대로 한다.

## Context Engineering: AI 시대의 새 역량

이걸 깨닫고 나니까 Context Engineering이라는 개념이 얼마나 중요한지 느껴졌다.

AI에게 무엇을 보여주고 무엇을 숨길지 설계하는 능력. 이게 AI 지원 개발에서 진짜 중요한 스킬이 됐다.

**Context Engineering 체크리스트:**

1. **범위 제한** - AI가 볼 파일을 명시적으로 제한
2. **패턴 강제** - 아키텍처로 코딩 스타일 통일
3. **경계 검증** - 변경이 범위를 벗어났는지 확인
4. **점진적 공개** - 필요한 정보만 단계적으로 제공

## 결론: 구조가 자유를 만든다

Vibe Coding이 실패하는 건 AI가 Flutter를 못해서가 아니다. **우리가 명확한 경계를 안 줬기 때문이다.**

전통적인 아키텍처(MVC, MVVM, MVP, 레이어 기반 Clean Architecture)는 각자의 목적이 있었다. 테스트 용이성, 관심사 분리, 의존성 역전. 다 좋은 거다.

근데 AI 에이전트 시대에는 **토큰 효율성**이라는 새로운 기준이 생겼다. 물리적 경계가 없으면 AI는 관련 없는 코드까지 전부 읽어야 한다.

Feature-based Architecture가 주는 것:

1. **컨텍스트 격리** - AI가 필요한 것만 본다
2. **예측 가능한 변경** - 수정이 Feature 경계 안에 머문다
3. **교차 오염 방지** - 물리적 분리가 "과잉 친절"을 막는다
4. **지속 가능한 확장** - 20개 화면이든 200개 화면이든 작동한다
5. **병렬 AI 작업** - Git Worktree로 에이전트 여러 개를 동시에 돌릴 수 있다

---

**300개의 집중된 토큰이 113,000개의 흩어진 토큰을 이긴다.**

이게 구조화된 컨텍스트의 힘이다.

Vibe Coding의 마법이 사라질 필요 없다. **올바른 구조 안에서는 지속 가능해진다.**

제약이 자유를 만든다는 말, 코드에도 적용된다.

---

**References**

- [Vibe Coding - Wikipedia](https://en.wikipedia.org/wiki/Vibe_coding)
- [Vibe Coding is not AI-Assisted Engineering - Addy Osmani](https://medium.com/@addyosmani/vibe-coding-is-not-the-same-as-ai-assisted-engineering-3f81088d5b98)
- [The Rise of Vibe Coding in 2025 - Emil](https://ecoemil.medium.com/the-rise-of-vibe-coding-in-2025-a-revolution-or-a-reckoning-4c2f7053ceef)
- [Context Engineering - FlowHunt](https://www.flowhunt.io/blog/context-engineering/)
- [The Clean Architecture - Robert C. Martin](https://blog.cleancoder.com/uncle-bob/2012/08/13/the-clean-architecture.html)
- [AI Code Generation Security Study - Veracode 2025](https://www.veracode.com/resources/state-software-security)

--- woogi
