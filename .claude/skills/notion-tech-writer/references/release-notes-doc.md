# Release Notes Template

## Structure

```markdown
# Release Notes - v[X.Y.Z]

| 속성 | 값 |
|------|-----|
| 🏷️ 태그 | Release, Changelog |
| 📅 릴리즈 일자 | YYYY-MM-DD |
| 🔖 버전 | vX.Y.Z |
| 📦 빌드 | #1234 |
| 🎯 플랫폼 | iOS / Android / Web / All |

## Highlights

> 이번 릴리즈의 핵심 변경사항 1-2문장 요약

💡 주요 변경: [가장 중요한 변경사항]

## What's New

### ✨ New Features

#### [기능명 1]

[기능 설명 1-2문장]

[Image: 기능 스크린샷 또는 GIF]

**사용 방법**:
1. 단계 1
2. 단계 2

#### [기능명 2]

[기능 설명]

### 🔧 Improvements

| 영역 | 개선 내용 |
|------|----------|
| 성능 | API 응답 속도 30% 개선 |
| UX | 로딩 인디케이터 추가 |
| 접근성 | 스크린 리더 지원 개선 |

### 🐛 Bug Fixes

| 이슈 | 증상 | 해결 |
|------|------|------|
| #123 | 로그인 후 화면 깜빡임 | 상태 초기화 로직 수정 |
| #124 | 다크모드에서 텍스트 안보임 | 색상 컨트라스트 조정 |
| #125 | 간헐적 크래시 | 메모리 누수 수정 |

▶️ 전체 버그 수정 목록
   - Fix: 이슈 설명 (#issue)
   - Fix: 이슈 설명 (#issue)
   - ...

### ⚠️ Breaking Changes

🚨 **API 변경**

```diff
- GET /api/v1/users
+ GET /api/v2/users
```

**마이그레이션 방법**:
1. API 버전 업데이트
2. 응답 형식 변경 대응

⚠️ **Deprecated**

| 항목 | 대체 | 제거 예정 |
|------|------|----------|
| `oldMethod()` | `newMethod()` | v3.0.0 |

### 🗑️ Removed

- `legacyFeature`: v2.0.0에서 deprecated, 이번 버전에서 제거

## Technical Details

### Dependencies Updated

| 패키지 | 이전 | 이후 |
|--------|------|------|
| flutter | 3.19.0 | 3.22.0 |
| bloc | 8.1.0 | 8.2.0 |

### Database Changes

```sql
-- Migration: 20250101_add_column
ALTER TABLE users ADD COLUMN avatar_url TEXT;
```

### Configuration Changes

```yaml
# 변경된 설정
feature_flags:
  new_feature: true  # ← 신규
```

## Compatibility

| 플랫폼 | 최소 버전 | 권장 버전 |
|--------|----------|----------|
| iOS | 14.0 | 17.0+ |
| Android | API 24 | API 34+ |
| Web | Chrome 90+ | Latest |

## Known Issues

| 이슈 | 상태 | 우회 방법 |
|------|------|----------|
| 특정 기기에서 느림 | 조사중 | 앱 재시작 |

## Upgrade Guide

### From v[Previous] to v[Current]

1. 의존성 업데이트
   ```bash
   flutter pub upgrade
   ```
2. 마이그레이션 실행
   ```bash
   flutter pub run build_runner build
   ```
3. Breaking changes 대응

✅ 업그레이드 확인: 앱 정상 실행 및 기존 기능 동작 확인

## Contributors

- @name1 - Feature A
- @name2 - Bug fixes
- @name3 - Documentation

## Links

- [Full Changelog](link)
- [Download](link)
- [Documentation](link)

---
📝 **유지보수 노트**
- 매 릴리즈 시 작성
- Hotfix 시 패치 버전 추가
```

## Version Naming Convention

```
vX.Y.Z
│ │ └── Patch: 버그 수정
│ └──── Minor: 하위 호환 기능 추가
└────── Major: Breaking changes
```

## Key Elements

1. **Highlights**: 핵심 변경사항 1줄 요약
2. **What's New**: 카테고리별 정리 (Feature/Improvement/Fix)
3. **Breaking Changes**: 빨간 콜아웃, diff 형식
4. **Upgrade Guide**: 업그레이드 단계별 안내
5. **Known Issues**: 알려진 문제와 우회 방법
6. **Compatibility**: 플랫폼별 요구사항 테이블
