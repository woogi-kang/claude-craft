# Figma → Flutter Converter Agent

> **Version**: 1.0.0 | **Type**: Modular | **Target**: Flutter 3.24+ / Dart 3.5+

---

## Overview

Figma 디자인을 Flutter 위젯으로 변환하는 모듈형 에이전트입니다.
8개의 독립적인 Phase로 구성되어 단계별 실행이 가능합니다.

---

## Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                    Figma → Flutter Pipeline                     │
├─────────────────────────────────────────────────────────────────┤
│  Phase 0: Project Scan    → Flutter 프로젝트 구조 분석          │
│  Phase 1: Design Scan     → Figma 디자인 분석 (MCP)             │
│  Phase 2: Token Extract   → ThemeData 토큰 추출                 │
│  Phase 3: Widget Mapping  → Figma → Flutter 위젯 매핑           │
│  Phase 4: Code Generate   → Dart 코드 생성                      │
│  Phase 5: Asset Process   → 이미지/아이콘 처리                  │
│  Phase 6: Pixel-Perfect   → 1:1 검증                            │
│  Phase 7: Responsive      → 반응형 검증                         │
└─────────────────────────────────────────────────────────────────┘
```

---

## Phase Files

| Phase | File | Description |
|-------|------|-------------|
| 0 | `phases/phase-0-project-scan.md` | Flutter 프로젝트 분석 |
| 1 | `phases/phase-1-design-scan.md` | Figma 디자인 분석 |
| 2 | `phases/phase-2-token-extract.md` | ThemeData 토큰 추출 |
| 3 | `phases/phase-3-widget-mapping.md` | 위젯 매핑 |
| 4 | `phases/phase-4-code-generate.md` | 코드 생성 |
| 5 | `phases/phase-5-asset-process.md` | 에셋 처리 |
| 6 | `phases/phase-6-pixel-perfect.md` | Pixel-Perfect 검증 |
| 7 | `phases/phase-7-responsive.md` | 반응형 검증 |

---

## Usage

### Full Conversion

```
@figma-to-flutter [FIGMA_URL]
```

### Phase-by-Phase

```
@figma-to-flutter phase:0
@figma-to-flutter phase:1 [FIGMA_URL]
@figma-to-flutter phase:2
@figma-to-flutter phase:3
@figma-to-flutter phase:4
@figma-to-flutter phase:5
@figma-to-flutter phase:6
@figma-to-flutter phase:7
```

---

## Figma MCP Tools

| Tool | Purpose | Rate Limit Impact |
|------|---------|-------------------|
| `get_metadata` | 파일 구조 조회 (필수 첫 호출) | Low |
| `get_design_context` | 노드 상세 정보 | High |
| `get_variable_defs` | 변수 정의 조회 | Medium |
| `get_screenshot` | 스크린샷 생성 | High |
| `get_code_connect_map` | 코드 연결 조회 | Low |
| `add_code_connect_map` | 코드 연결 추가 | Low |
| `create_design_system_rules` | 디자인 시스템 규칙 | Low |

### Rate Limit Optimization

```dart
// MUST: Always call get_metadata first (80% token savings)
final metadata = await getMetadata(fileKey: fileKey, nodeId: nodeId);

// Then selectively call get_design_context for specific nodes
for (final node in relevantNodes) {
  final context = await getDesignContext(fileKey: fileKey, nodeId: node.id);
}
```

---

## Output Structure

```
lib/
├── core/
│   ├── theme/
│   │   ├── app_theme.dart          # ThemeData 정의
│   │   ├── app_colors.dart         # 색상 팔레트
│   │   ├── app_typography.dart     # 텍스트 스타일
│   │   └── app_spacing.dart        # 간격 상수
│   └── widgets/
│       └── index.dart              # 위젯 exports
│
├── features/
│   └── [feature]/
│       ├── presentation/
│       │   ├── widgets/            # Feature 위젯
│       │   └── pages/              # Feature 페이지
│       └── domain/
│
├── shared/
│   └── widgets/                    # 공통 위젯
│
└── main.dart

assets/
├── images/                         # 이미지 에셋
├── icons/                          # SVG 아이콘
└── fonts/                          # 커스텀 폰트
```

---

## Quality Gates

### Pixel-Perfect Threshold

- Desktop: 98%+
- Tablet: 95%+
- Mobile: 95%+

### Code Quality

- Dart Analysis: No errors
- Flutter Lint: All rules pass
- Widget Tests: Coverage 80%+

---

## Version Info

- Agent Version: 1.0.0
- Figma MCP API: 2025.1
- Flutter Target: 3.24+
- Dart Target: 3.5+
- Riverpod: 3.x (optional)
