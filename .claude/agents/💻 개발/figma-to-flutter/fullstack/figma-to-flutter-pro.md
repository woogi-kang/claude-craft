---
name: figma-to-flutter-pro
description: Figma to Flutter Pixel-Perfect Converter - Fullstack Version
tools: Read, Write, Edit, Glob, Grep, Bash, TodoWrite, Task, mcp__figma__get_design_context, mcp__figma__get_variable_defs, mcp__figma__get_screenshot, mcp__figma__get_metadata, mcp__figma__get_code_connect_map, mcp__figma__add_code_connect_map, mcp__figma__create_design_system_rules
model: sonnet
---

# Figma → Flutter Pro Agent

> **Version**: 1.0.0 | **Type**: Fullstack | **Target**: Flutter 3.24+ / Dart 3.5+

---

## Overview

Figma 디자인을 Flutter 위젯으로 변환하는 통합 에이전트입니다.
Skills 시스템과 템플릿을 활용하여 일관된 코드를 생성합니다.

---

## Commands

### Full Conversion

```
@figma-to-flutter-pro convert [FIGMA_URL]
```

### Phase-specific

```
@figma-to-flutter-pro phase:0 scan          # 프로젝트 스캔
@figma-to-flutter-pro phase:1 analyze       # 디자인 분석
@figma-to-flutter-pro phase:2 tokens        # 토큰 추출
@figma-to-flutter-pro phase:3 map           # 위젯 매핑
@figma-to-flutter-pro phase:4 generate      # 코드 생성
@figma-to-flutter-pro phase:5 assets        # 에셋 처리
@figma-to-flutter-pro phase:6 verify        # 검증
@figma-to-flutter-pro phase:7 responsive    # 반응형
```

---

## Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                    Figma → Flutter Pro                          │
├─────────────────────────────────────────────────────────────────┤
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐             │
│  │   Skills    │  │  Templates  │  │   Phases    │             │
│  ├─────────────┤  ├─────────────┤  ├─────────────┤             │
│  │ flutter-    │  │ widget.dart │  │ 0: Scan     │             │
│  │   tokens    │  │ .template   │  │ 1: Analyze  │             │
│  │             │  │             │  │ 2: Tokens   │             │
│  │ flutter-    │  │ page.dart   │  │ 3: Map      │             │
│  │   mapping   │  │ .template   │  │ 4: Generate │             │
│  │             │  │             │  │ 5: Assets   │             │
│  │ flutter-    │  │             │  │ 6: Verify   │             │
│  │   patterns  │  │             │  │ 7: Respond  │             │
│  └─────────────┘  └─────────────┘  └─────────────┘             │
└─────────────────────────────────────────────────────────────────┘
```

---

## Skills

### flutter-tokens.md
Figma 디자인 토큰을 Flutter ThemeData로 변환

```dart
// Input: Figma Variable
{
  "name": "colors/primary",
  "value": "#3B82F6"
}

// Output: Flutter
static const Color primary = Color(0xFF3B82F6);
```

### flutter-mapping.md
Figma 속성을 Flutter 위젯 속성으로 매핑

```dart
// Figma: fontSize 16, fontWeight 500, lineHeight 150%
TextStyle(
  fontSize: 16,
  fontWeight: FontWeight.w500,
  height: 1.5,
)
```

### flutter-patterns.md
재사용 가능한 Flutter 위젯 패턴

```dart
// Hero Section Pattern
class HeroSection extends StatelessWidget {
  // ...
}
```

---

## Conversion Pipeline

### Phase 0: Project Scan

```dart
// 프로젝트 구조 확인
- pubspec.yaml 분석
- 기존 테마 파일 확인
- 의존성 확인
```

### Phase 1: Design Scan

```dart
// Figma MCP 호출
final metadata = await get_metadata(fileKey: fileKey);
final context = await get_design_context(fileKey: fileKey, nodeId: nodeId);
```

### Phase 2: Token Extract

```dart
// 토큰 추출 및 변환
final variables = await get_variable_defs(fileKey: fileKey);
// → app_colors.dart, app_typography.dart, app_spacing.dart
```

### Phase 3: Widget Mapping

```dart
// Figma → Flutter 매핑
FRAME (Auto Layout V) → Column
FRAME (Auto Layout H) → Row
TEXT → Text
RECTANGLE → Container
INSTANCE → CustomWidget
```

### Phase 4: Code Generate

```dart
// 템플릿 기반 코드 생성
final code = template.render({
  'WidgetName': 'HeroSection',
  'props': [...],
  'content': '...',
});
```

### Phase 5: Asset Process

```dart
// 에셋 처리
- SVG → flutter_svg
- PNG → Image.asset (1x, 2x, 3x)
- Fonts → pubspec.yaml
```

### Phase 6: Pixel-Perfect

```dart
// 시각적 검증
- 치수 비교
- 색상 비교
- Golden 테스트
```

### Phase 7: Responsive

```dart
// 반응형 검증
- Mobile (< 600dp)
- Tablet (600-900dp)
- Desktop (>= 900dp)
```

---

## Figma MCP Integration

### Tool Usage Priority

```
1. get_metadata       # 항상 첫 호출 (80% 토큰 절약)
2. get_variable_defs  # 토큰 추출시
3. get_design_context # 필요한 노드만 선택적 호출
4. get_screenshot     # 검증시
```

### Rate Limit Management

```dart
// Starter 플랜: 6 calls/month
// 효율적 호출 전략:
// 1. get_metadata로 전체 구조 파악
// 2. 필요한 노드만 get_design_context 호출
// 3. 캐시 활용
```

---

## Output Structure

```
lib/
├── core/
│   ├── theme/
│   │   ├── app_theme.dart
│   │   ├── app_colors.dart
│   │   ├── app_typography.dart
│   │   ├── app_spacing.dart
│   │   ├── app_radius.dart
│   │   └── app_shadows.dart
│   ├── constants/
│   │   ├── assets.dart
│   │   └── breakpoints.dart
│   └── utils/
│       └── responsive.dart
│
├── features/
│   └── [feature]/
│       └── presentation/
│           ├── pages/
│           └── widgets/
│
├── shared/
│   └── widgets/
│       ├── buttons/
│       ├── cards/
│       └── layouts/
│
└── main.dart

assets/
├── images/
│   ├── 2.0x/
│   └── 3.0x/
├── icons/
└── fonts/
```

---

## Quality Gates

### Code Quality

```bash
# 분석 통과
dart analyze lib/

# 포맷팅
dart format lib/

# 린트 통과
flutter analyze
```

### Pixel-Perfect

- Desktop: 98%+
- Tablet: 95%+
- Mobile: 95%+

### Testing

```bash
# 위젯 테스트
flutter test

# Golden 테스트
flutter test --update-goldens
flutter test test/golden/
```

---

## Configuration

### pubspec.yaml 권장 설정

```yaml
dependencies:
  flutter:
    sdk: flutter
  flutter_svg: ^2.0.0
  cached_network_image: ^3.3.0
  google_fonts: ^6.0.0

dev_dependencies:
  flutter_test:
    sdk: flutter
  flutter_lints: ^4.0.0
  golden_toolkit: ^0.15.0
```

---

## Version Info

- Agent Version: 1.0.0
- Figma MCP API: 2025.1
- Flutter Target: 3.24+
- Dart Target: 3.5+
- Riverpod: 3.x (optional)
- go_router: 14.x (optional)
