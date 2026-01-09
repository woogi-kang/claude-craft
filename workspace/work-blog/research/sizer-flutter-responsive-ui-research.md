# Research: Flutter sizer 패키지 - 반응형 UI 개발

**Date:** 2026-01-08
**Author:** woogi
**Series:** flutter_packages_weekly
**Status:** Ready for Draft

---

## Topic Analysis

```yaml
topic_analysis:
  main_topic: "Flutter sizer 패키지를 활용한 반응형 UI 개발"
  sub_topics:
    - "sizer 패키지란 무엇인가"
    - "설치 및 기본 설정"
    - "핵심 기능 (h, w, sp, dp 확장)"
    - "디바이스 감지 (orientation, screenType)"
    - "실전 코드 예제"
    - "flutter_screenutil과의 비교"
    - "장단점 및 사용 시 주의사항"
  target_audience: "intermediate"
  key_questions:
    - "sizer 패키지는 어떤 문제를 해결하는가?"
    - "어떻게 사용하는가?"
    - "다른 반응형 패키지와 비교했을 때 장단점은?"
    - "실제 프로젝트에서 어떻게 활용할 수 있는가?"
```

## SEO Keywords

```yaml
seo_keywords:
  primary: "Flutter sizer 패키지"
  secondary:
    - "Flutter 반응형 UI"
    - "Flutter responsive design"
    - "sizer vs screenutil"
    - "Flutter 다양한 화면 크기 대응"
  long_tail:
    - "Flutter sizer 패키지 사용법"
    - "Flutter 태블릿 모바일 반응형"
    - "Flutter 화면 비율 적용"
  search_intent: "tutorial"
  suggested_title_keywords: ["Flutter", "sizer", "반응형 UI", "가이드", "2026"]
```

---

## Web Research

### W001: pub.dev 공식 페이지
- **URL:** https://pub.dev/packages/sizer
- **Type:** documentation
- **Key Points:**
  - 현재 버전: 3.1.3
  - 주간 다운로드: 160,000+
  - 1.8k likes, 150 pub points
  - MIT 라이선스
  - Publisher: technoprashant.me (verified)
  - 지원 플랫폼: Android, iOS, Linux, macOS, Web, Windows
- **Credibility:** high

### W002: GitHub Repository
- **URL:** https://github.com/TechnoPrashant/Sizer
- **Type:** source code
- **Key Points:**
  - 오픈소스, 활발한 유지보수
  - Issue tracking 및 커뮤니티 지원
- **Credibility:** high

### W003: Medium Tutorial (Cagdas Pektas)
- **URL:** https://medium.com/@cagdaspektas3405/flutter-responsive-ui-with-sizer-4d95235b2d3e
- **Type:** tutorial
- **Key Points:**
  - 실전 사용 예제 제공
  - 간단한 API 설명
- **Credibility:** medium

### W004: Sizer vs ScreenUtil 비교
- **URL:** https://medium.com/easy-flutter/sizer-vs-screenutil-what-you-should-prefer-for-responsive-layouts-in-flutter-3d32dc648e40
- **Type:** comparison
- **Key Points:**
  - Sizer: 더 간단한 API, 초보자 친화적
  - ScreenUtil: 더 많은 기능, 더 큰 커뮤니티
  - 둘 다 유사한 기본 기능 제공
- **Credibility:** medium

### W005: Flutter 공식 문서 - Adaptive and Responsive Design
- **URL:** https://docs.flutter.dev/ui/adaptive-responsive
- **Type:** official documentation
- **Key Points:**
  - MediaQuery, LayoutBuilder 권장
  - 하드코딩된 사이즈 피하기
  - Flexible, Expanded 위젯 활용
  - SafeArea 사용 권장
- **Credibility:** high

---

## Package Details

### 핵심 기능

#### 1. 반응형 사이징 Extensions
```dart
// 화면 높이의 퍼센트
Container(height: 30.h)  // 화면 높이의 30%

// 화면 너비의 퍼센트
Container(width: 50.w)   // 화면 너비의 50%

// SafeArea 고려한 사이징
Container(height: 30.sh) // SafeArea 제외 높이의 30%
Container(width: 50.sw)  // SafeArea 제외 너비의 50%

// 폰트 사이징
Text('Hello', style: TextStyle(fontSize: 16.sp))  // 화면 비율 기반
Text('Hello', style: TextStyle(fontSize: 16.dp))  // pixel density 기반
```

#### 2. 물리적 단위 변환
- cm, mm, inches, picas, points, pixels 지원

#### 3. 디바이스 감지
```dart
// 방향 감지
Device.orientation == Orientation.portrait

// 디바이스 타입 감지
Device.screenType == ScreenType.mobile
Device.screenType == ScreenType.tablet
Device.screenType == ScreenType.desktop

// 기타 정보
Device.aspectRatio
Device.pixelRatio
Device.boxConstraints
```

### 설정 옵션
```dart
Sizer(
  builder: (context, orientation, screenType) {
    return MaterialApp(home: HomePage());
  },
)
```

- `maxMobileWidth`: 모바일/태블릿 구분 기준 (기본값: 599px)
- `maxTabletWidth`: 태블릿/데스크톱 구분 기준

---

## Key Insights

### Pain Points 해결
1. **하드코딩 사이즈 문제**: 다양한 디바이스에서 일관된 UI 제공
2. **복잡한 MediaQuery 사용**: 간단한 Extension으로 대체
3. **방향 전환 대응**: 자동으로 orientation 변화 감지
4. **디바이스별 레이아웃**: screenType으로 조건부 렌더링

### 장점
- **간단한 API**: `.h`, `.w`, `.sp` 직관적 사용
- **낮은 학습 곡선**: 초보자도 쉽게 적용 가능
- **멀티 플랫폼 지원**: Mobile, Web, Desktop 모두 지원
- **SafeArea 자동 처리**: `.sh`, `.sw` 확장 제공
- **의존성 없음**: Flutter 프레임워크 외 추가 의존성 없음

### 단점
- **IDE 자동 import 미지원**: Extension method 특성상 수동 import 필요
- **물리적 화면 크기 미접근**: pixel ratio 기반 dp 계산
- **기준 디자인 사이즈 설정 없음**: screenutil과 달리 디자이너 시안 기준 설정 불가

### flutter_screenutil vs sizer 비교

| 항목 | sizer | flutter_screenutil |
|------|-------|-------------------|
| **API 복잡도** | 단순 | 다양한 옵션 |
| **학습 곡선** | 낮음 | 중간 |
| **기준 디자인 사이즈** | 미지원 | 지원 |
| **커뮤니티** | 중간 | 큼 |
| **추가 기능** | 기본적 | 고급 스케일링 |
| **추천 대상** | 빠른 프로토타입, 소규모 프로젝트 | 대규모 프로젝트, 디자인 시스템 |

### Best Practices
1. 프로젝트 초기에 반응형 전략 결정
2. 일관된 Extension 사용 (.h, .w, .sp)
3. breakpoint 기준 명확히 정의
4. 극단적인 화면 비율 테스트 필수

---

## Suggested Outline

```markdown
# Flutter sizer 패키지로 반응형 UI 쉽게 구현하기

## Hook
"다양한 화면 크기에 대응하는 Flutter 앱을 만들고 싶은데,
MediaQuery 코드가 너무 복잡하다고 느꼈던 적 있으신가요?"

## Sections
1. **들어가며** - 반응형 UI의 필요성
2. **sizer 패키지 소개** - 무엇이고 왜 쓰는가
3. **설치 및 설정** - 프로젝트 적용 방법
4. **핵심 기능 가이드** - h, w, sp, dp 사용법
5. **디바이스 감지** - orientation, screenType 활용
6. **실전 예제** - 반응형 카드 UI 만들기
7. **다른 패키지와 비교** - screenutil과의 차이
8. **마무리** - 언제 사용하면 좋을까

## Estimated Length
~2000-2500 words (한국어)

## Code Examples Needed
- [x] 기본 설정 코드
- [x] h, w, sp 사용 예제
- [x] 조건부 레이아웃 예제
- [x] 실전 반응형 카드 UI
```

---

## Sources

- [pub.dev - sizer](https://pub.dev/packages/sizer)
- [GitHub - TechnoPrashant/Sizer](https://github.com/TechnoPrashant/Sizer)
- [Flutter Gems - sizer](https://fluttergems.dev/packages/sizer/)
- [Medium - Flutter Responsive UI With Sizer](https://medium.com/@cagdaspektas3405/flutter-responsive-ui-with-sizer-4d95235b2d3e)
- [Medium - Sizer vs ScreenUtil](https://medium.com/easy-flutter/sizer-vs-screenutil-what-you-should-prefer-for-responsive-layouts-in-flutter-3d32dc648e40)
- [Flutter Docs - Adaptive and Responsive Design](https://docs.flutter.dev/ui/adaptive-responsive)
- [Flutter Docs - Best Practices for Adaptive Design](https://docs.flutter.dev/ui/adaptive-responsive/best-practices)
