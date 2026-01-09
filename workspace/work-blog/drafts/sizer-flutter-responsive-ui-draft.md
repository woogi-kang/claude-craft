---
title: "Flutter sizer 패키지로 반응형 UI 쉽게 구현하기"
subtitle: "다양한 화면 크기에 대응하는 Flutter 앱 만들기"
series: "flutter_packages_weekly"
tags: ["flutter", "responsive-design", "sizer", "ui", "mobile-development"]
cover_image: ""
canonical_url: ""
draft: true
tone: "mixed"
language: "ko"
word_count: 2300
seo:
  primary_keyword: "Flutter sizer 패키지"
  secondary_keywords: ["Flutter 반응형 UI", "Flutter responsive", "sizer vs screenutil"]
  meta_description: "Flutter sizer 패키지를 사용해 다양한 화면 크기에 대응하는 반응형 UI를 쉽게 구현하는 방법을 코드 예제와 함께 알아봅니다."
  slug: "flutter-sizer-responsive-ui-guide"
---

# Flutter sizer 패키지로 반응형 UI 쉽게 구현하기

안녕하세요, woogi입니다! 오늘은 Flutter에서 반응형 UI를 쉽게 구현할 수 있게 도와주는 **sizer** 패키지에 대해 이야기해볼까 합니다.

다양한 화면 크기에 대응하는 Flutter 앱을 만들고 싶은데, MediaQuery 코드가 너무 복잡하다고 느끼신 적 있으신가요? 저도 처음에는 `MediaQuery.of(context).size.width * 0.5` 이런 코드를 반복해서 작성하다가 "이게 맞나?" 싶었거든요.

sizer 패키지를 사용하면 단순히 `50.w`라고 쓰는 것만으로 화면 너비의 50%를 지정할 수 있습니다. 이번 글에서는 sizer 패키지의 설치부터 실전 활용까지 차근차근 알아보겠습니다.

---

## 목차

- [sizer 패키지란?](#sizer-패키지란)
- [설치 및 기본 설정](#설치-및-기본-설정)
- [핵심 기능 가이드](#핵심-기능-가이드)
- [디바이스 감지 기능](#디바이스-감지-기능)
- [실전 예제: 반응형 카드 UI](#실전-예제-반응형-카드-ui)
- [flutter_screenutil과 비교](#flutter_screenutil과-비교)
- [마무리](#마무리)

---

## sizer 패키지란?

[sizer](https://pub.dev/packages/sizer)는 Flutter에서 반응형 UI를 쉽게 구현할 수 있도록 도와주는 패키지입니다. 2024년 기준 주간 다운로드 160,000회 이상을 기록하며, 많은 Flutter 개발자들이 사용하고 있습니다.

### 주요 특징

- **간단한 API**: `.h`, `.w`, `.sp` 같은 직관적인 Extension 제공
- **멀티 플랫폼 지원**: Android, iOS, Web, Desktop 모두 지원
- **디바이스 감지**: 모바일/태블릿/데스크톱, 세로/가로 모드 자동 감지
- **SafeArea 지원**: 노치나 시스템 UI 영역을 고려한 사이징
- **의존성 없음**: Flutter 프레임워크 외 추가 의존성 없음

```
현재 버전: 3.1.3
라이선스: MIT
Publisher: technoprashant.me (verified)
```

---

## 설치 및 기본 설정

### 1. 패키지 설치

`pubspec.yaml`에 sizer를 추가합니다:

```yaml
dependencies:
  flutter:
    sdk: flutter
  sizer: ^3.1.3
```

터미널에서 패키지를 설치합니다:

```bash
flutter pub get
```

### 2. 앱에 Sizer 적용하기

`main.dart`에서 `MaterialApp`을 `Sizer` 위젯으로 감싸줍니다:

```dart
import 'package:flutter/material.dart';
import 'package:sizer/sizer.dart';

void main() {
  runApp(const MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  @override
  Widget build(BuildContext context) {
    return Sizer(
      builder: (context, orientation, screenType) {
        return MaterialApp(
          title: 'Sizer Demo',
          theme: ThemeData(
            primarySwatch: Colors.blue,
          ),
          home: const HomePage(),
        );
      },
    );
  }
}
```

`Sizer` 위젯의 `builder` 콜백에서는 세 가지 유용한 정보를 받을 수 있습니다:

- `context`: BuildContext
- `orientation`: 현재 화면 방향 (portrait/landscape)
- `screenType`: 디바이스 타입 (mobile/tablet/desktop)

### 3. Import 추가

sizer의 Extension을 사용하려면 각 파일에서 import를 추가해야 합니다:

```dart
import 'package:sizer/sizer.dart';
```

> **Tip**: IDE의 자동 import가 Extension method에는 작동하지 않을 수 있어서, 수동으로 import 해주셔야 합니다.

---

## 핵심 기능 가이드

sizer의 핵심은 숫자 타입에 추가되는 **Extension methods**입니다. 이를 통해 화면 비율 기반의 사이징을 매우 간단하게 할 수 있습니다.

### 화면 비율 기반 사이징

#### `.h` - 화면 높이의 퍼센트

```dart
Container(
  height: 30.h,  // 화면 높이의 30%
)
```

#### `.w` - 화면 너비의 퍼센트

```dart
Container(
  width: 50.w,   // 화면 너비의 50%
)
```

#### 실제 사용 예시

```dart
Container(
  width: 80.w,       // 화면 너비의 80%
  height: 25.h,      // 화면 높이의 25%
  padding: EdgeInsets.symmetric(
    horizontal: 5.w,  // 좌우 패딩: 화면 너비의 5%
    vertical: 2.h,    // 상하 패딩: 화면 높이의 2%
  ),
  decoration: BoxDecoration(
    color: Colors.blue,
    borderRadius: BorderRadius.circular(2.w),
  ),
  child: Text('반응형 컨테이너'),
)
```

### SafeArea를 고려한 사이징

노치나 상태바 영역을 제외한 "안전 영역" 기준으로 사이징하고 싶다면 `.sh`와 `.sw`를 사용합니다:

```dart
Container(
  height: 30.sh,  // SafeArea 제외 높이의 30%
  width: 50.sw,   // SafeArea 제외 너비의 50%
)
```

### 폰트 사이징

#### `.sp` - 화면 비율 기반 폰트 크기

```dart
Text(
  'Hello Flutter!',
  style: TextStyle(fontSize: 16.sp),
)
```

#### `.dp` - 픽셀 밀도 기반 폰트 크기

```dart
Text(
  'Hello Flutter!',
  style: TextStyle(fontSize: 16.dp),
)
```

**`.sp` vs `.dp`의 차이점:**

- `.sp`: 화면 비율과 aspect ratio를 함께 고려
- `.dp`: 디바이스의 pixel ratio만 고려

일반적으로 본문 텍스트에는 `.sp`를, 고정 크기가 필요한 아이콘이나 라벨에는 `.dp`를 사용하는 것을 권장합니다.

### 사이징 Extension 정리

| Extension | 설명 | 예시 |
|-----------|------|------|
| `.h` | 화면 높이의 % | `30.h` = 높이의 30% |
| `.w` | 화면 너비의 % | `50.w` = 너비의 50% |
| `.sh` | SafeArea 높이의 % | `30.sh` |
| `.sw` | SafeArea 너비의 % | `50.sw` |
| `.sp` | 화면 비율 기반 폰트 | `16.sp` |
| `.dp` | 픽셀 밀도 기반 폰트 | `16.dp` |

---

## 디바이스 감지 기능

sizer는 단순한 사이징 외에도 디바이스 정보를 감지하는 기능을 제공합니다.

### 화면 방향 감지

```dart
if (Device.orientation == Orientation.portrait) {
  // 세로 모드 UI
  return PortraitLayout();
} else {
  // 가로 모드 UI
  return LandscapeLayout();
}
```

### 디바이스 타입 감지

```dart
if (Device.screenType == ScreenType.mobile) {
  return MobileLayout();
} else if (Device.screenType == ScreenType.tablet) {
  return TabletLayout();
} else {
  return DesktopLayout();
}
```

### 기타 디바이스 정보

```dart
// 화면 비율
double ratio = Device.aspectRatio;

// 픽셀 밀도
double pixelRatio = Device.pixelRatio;

// BoxConstraints
BoxConstraints constraints = Device.boxConstraints;
```

### 디바이스 타입 기준 커스터마이징

기본적으로 sizer는 화면 너비 599px을 기준으로 모바일/태블릿을 구분합니다. 이 기준을 변경하려면 `Sizer` 위젯의 파라미터를 사용합니다:

```dart
Sizer(
  builder: (context, orientation, screenType) {
    return MaterialApp(
      home: HomePage(),
    );
  },
  // maxMobileWidth: 599,  // 기본값
  // maxTabletWidth: 900,  // 데스크톱 구분 기준 추가
)
```

---

## 실전 예제: 반응형 카드 UI

실제 프로젝트에서 sizer를 어떻게 활용하는지 예제를 통해 살펴보겠습니다.

### 반응형 프로필 카드

```dart
import 'package:flutter/material.dart';
import 'package:sizer/sizer.dart';

class ProfileCard extends StatelessWidget {
  final String name;
  final String role;
  final String avatarUrl;

  const ProfileCard({
    super.key,
    required this.name,
    required this.role,
    required this.avatarUrl,
  });

  @override
  Widget build(BuildContext context) {
    return Container(
      width: Device.screenType == ScreenType.mobile ? 90.w : 45.w,
      padding: EdgeInsets.all(4.w),
      decoration: BoxDecoration(
        color: Colors.white,
        borderRadius: BorderRadius.circular(3.w),
        boxShadow: [
          BoxShadow(
            color: Colors.black.withOpacity(0.1),
            blurRadius: 2.w,
            offset: Offset(0, 1.h),
          ),
        ],
      ),
      child: Device.orientation == Orientation.portrait
          ? _buildVerticalLayout()
          : _buildHorizontalLayout(),
    );
  }

  Widget _buildVerticalLayout() {
    return Column(
      mainAxisSize: MainAxisSize.min,
      children: [
        CircleAvatar(
          radius: 15.w,
          backgroundImage: NetworkImage(avatarUrl),
        ),
        SizedBox(height: 2.h),
        Text(
          name,
          style: TextStyle(
            fontSize: 18.sp,
            fontWeight: FontWeight.bold,
          ),
        ),
        SizedBox(height: 0.5.h),
        Text(
          role,
          style: TextStyle(
            fontSize: 14.sp,
            color: Colors.grey[600],
          ),
        ),
      ],
    );
  }

  Widget _buildHorizontalLayout() {
    return Row(
      children: [
        CircleAvatar(
          radius: 10.w,
          backgroundImage: NetworkImage(avatarUrl),
        ),
        SizedBox(width: 4.w),
        Expanded(
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            mainAxisSize: MainAxisSize.min,
            children: [
              Text(
                name,
                style: TextStyle(
                  fontSize: 16.sp,
                  fontWeight: FontWeight.bold,
                ),
              ),
              Text(
                role,
                style: TextStyle(
                  fontSize: 12.sp,
                  color: Colors.grey[600],
                ),
              ),
            ],
          ),
        ),
      ],
    );
  }
}
```

### 사용 예시

```dart
class HomePage extends StatelessWidget {
  const HomePage({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text(
          'Sizer Demo',
          style: TextStyle(fontSize: 18.sp),
        ),
      ),
      body: Center(
        child: SingleChildScrollView(
          padding: EdgeInsets.all(4.w),
          child: Column(
            children: [
              ProfileCard(
                name: 'woogi',
                role: 'Flutter Developer',
                avatarUrl: 'https://example.com/avatar.png',
              ),
              SizedBox(height: 3.h),
              Text(
                'Device: ${Device.screenType}',
                style: TextStyle(fontSize: 14.sp),
              ),
              Text(
                'Orientation: ${Device.orientation}',
                style: TextStyle(fontSize: 14.sp),
              ),
            ],
          ),
        ),
      ),
    );
  }
}
```

이 예제에서 주목할 점:

1. **카드 너비**: 모바일에서는 90%, 태블릿/데스크톱에서는 45%
2. **레이아웃 전환**: 세로 모드에서는 수직 레이아웃, 가로 모드에서는 수평 레이아웃
3. **일관된 간격**: 모든 padding과 margin이 화면 비율 기반

---

## flutter_screenutil과 비교

Flutter의 반응형 UI 패키지 중 가장 많이 비교되는 것이 `sizer`와 `flutter_screenutil`입니다.

### 비교표

| 항목 | sizer | flutter_screenutil |
|------|-------|-------------------|
| **API 복잡도** | 단순함 | 다양한 옵션 |
| **학습 곡선** | 낮음 | 중간 |
| **기준 디자인 사이즈 설정** | 미지원 | 지원 |
| **커뮤니티 크기** | 중간 | 큼 |
| **주간 다운로드** | ~160K | ~250K |
| **추가 기능** | 기본적 | 고급 스케일링 |

### flutter_screenutil의 디자인 사이즈 설정

flutter_screenutil의 가장 큰 차별점은 **디자이너의 시안 기준 사이즈를 설정**할 수 있다는 점입니다:

```dart
// flutter_screenutil 설정
ScreenUtilInit(
  designSize: const Size(375, 812),  // 디자이너 시안 기준
  builder: (context, child) {
    return MaterialApp(home: HomePage());
  },
);
```

이렇게 하면 Figma나 Sketch에서 작업한 디자인 시안의 수치를 그대로 사용할 수 있습니다.

### 어떤 패키지를 선택해야 할까?

**sizer를 추천하는 경우:**
- 빠른 프로토타이핑이 필요할 때
- 소규모 프로젝트나 개인 프로젝트
- 간단한 API를 선호할 때
- Flutter를 처음 배우는 개발자

**flutter_screenutil을 추천하는 경우:**
- 디자이너와 협업하는 프로젝트
- 디자인 시스템이 잘 정의된 프로젝트
- 대규모 팀 프로젝트
- 더 세밀한 커스터마이징이 필요할 때

---

## 마무리

오늘은 Flutter에서 반응형 UI를 쉽게 구현할 수 있는 sizer 패키지에 대해 알아봤습니다.

### 핵심 정리

1. **설치**: `pubspec.yaml`에 `sizer: ^3.1.3` 추가
2. **설정**: `MaterialApp`을 `Sizer` 위젯으로 감싸기
3. **사용**: `.h`, `.w`, `.sp` Extension으로 반응형 사이징
4. **디바이스 감지**: `Device.orientation`, `Device.screenType` 활용

### 주의사항

- IDE 자동 import가 안 될 수 있으니 수동으로 `import 'package:sizer/sizer.dart';` 추가
- 너무 과도한 퍼센트 사용은 오히려 레이아웃을 복잡하게 만들 수 있음
- 극단적인 화면 비율(폴더블 기기 등)에서는 별도 테스트 필요

sizer는 "간단하게 반응형 UI를 구현하고 싶다"는 니즈에 딱 맞는 패키지입니다. 물론 더 복잡한 요구사항이 있다면 flutter_screenutil이나 responsive_framework 같은 패키지도 고려해보세요.

여러분의 다음 Flutter 프로젝트에서 sizer를 한번 사용해보시길 추천드립니다!

---

읽어주셔서 감사합니다! 도움이 되셨다면 댓글로 알려주세요. 질문이 있으시면 언제든 환영합니다.

-- woogi

---

**참고 자료:**
- [pub.dev - sizer](https://pub.dev/packages/sizer)
- [GitHub - TechnoPrashant/Sizer](https://github.com/TechnoPrashant/Sizer)
- [Flutter 공식 문서 - Adaptive and Responsive Design](https://docs.flutter.dev/ui/adaptive-responsive)
- [Medium - Sizer vs ScreenUtil 비교](https://medium.com/easy-flutter/sizer-vs-screenutil-what-you-should-prefer-for-responsive-layouts-in-flutter-3d32dc648e40)

---
*Draft generated: 2026-01-08*
*Ready for review: /blog-review*
