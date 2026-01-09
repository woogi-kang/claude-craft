---
name: validate
description: |
  변환된 Next.js 프로젝트의 타입, 린트, 빌드를 검증합니다.
  오류 발생 시 수정 방안을 제시합니다.
triggers:
  - "검증"
  - "validate"
  - "빌드 테스트"
---

# Validation Skill

변환된 Next.js 프로젝트의 품질을 검증합니다.

## 입력

- 변환된 Next.js 프로젝트 경로

## 출력

- 검증 결과 리포트
- 오류 수정 (필요시)

---

## 검증 단계

### Step 1: TypeScript 타입 체크

```bash
npm run typecheck
# 또는
npx tsc --noEmit
```

#### 일반적인 타입 에러 및 해결

| 에러 | 원인 | 해결 |
|------|------|------|
| `Property 'x' does not exist` | Flutter 모델 미변환 | types/ 폴더에 타입 정의 |
| `Cannot find module '@/...'` | 경로 별칭 미설정 | tsconfig.json paths 확인 |
| `Type 'null' is not assignable` | Null 안전성 | Optional 또는 기본값 |
| `Parameter 'x' implicitly has 'any' type` | 타입 누락 | 명시적 타입 추가 |

### Step 2: ESLint 검사

```bash
npm run lint
```

#### 일반적인 린트 에러 및 해결

| 에러 | 해결 |
|------|------|
| `'use client' must be the first statement` | 파일 최상단으로 이동 |
| `React Hook useEffect has a missing dependency` | deps 배열 수정 또는 // eslint-disable |
| `'x' is defined but never used` | 사용하거나 `_` prefix 추가 |
| `Unexpected any` | 구체적인 타입으로 변경 |

### Step 3: 빌드 테스트

```bash
npm run build
```

#### 일반적인 빌드 에러 및 해결

| 에러 | 원인 | 해결 |
|------|------|------|
| `Module not found` | 패키지 미설치 | npm install 실행 |
| `Dynamic server usage` | Server Component에서 동적 함수 사용 | `'use client'` 추가 또는 구조 변경 |
| `Image is missing required "alt" property` | alt 속성 누락 | alt 추가 |
| `Hydration failed` | SSR/CSR 불일치 | suppressHydrationWarning 또는 구조 수정 |

### Step 4: 런타임 검증

```bash
npm run dev
```

#### 검증 체크리스트

- [ ] 페이지 로딩 정상
- [ ] 네비게이션 동작
- [ ] API 호출 성공
- [ ] 상태 업데이트 정상
- [ ] 반응형 레이아웃
- [ ] 콘솔 에러 없음

---

## 자동 수정 가능한 항목

### 1. Import 정리

```bash
# ESLint auto-fix
npm run lint -- --fix

# 또는 Prettier
npm run format
```

### 2. 누락된 타입 생성

```typescript
// 감지된 미정의 타입을 자동 생성
// src/types/index.ts에 추가

// Flutter 모델 기반
interface User {
  id: string
  email: string
  name: string
  createdAt: string
}
```

### 3. 'use client' 자동 추가

```typescript
// useState, useEffect 등 훅 사용 시 자동 감지
// 파일 최상단에 'use client' 추가
```

---

## 검증 결과 리포트

### validation-report.md

```markdown
# Validation Report: {project-name}

## 요약

| 항목 | 상태 | 오류 수 |
|------|------|---------|
| TypeScript | ✅ Pass | 0 |
| ESLint | ⚠️ Warnings | 3 |
| Build | ✅ Pass | 0 |
| Runtime | ✅ Pass | 0 |

## TypeScript 검사

```
✓ 타입 체크 통과
  - 검사된 파일: 45개
  - 에러: 0개
  - 경고: 0개
```

## ESLint 검사

```
⚠️ 경고 발견

src/components/ProductCard.tsx
  Line 15: 'category' is defined but never used  @typescript-eslint/no-unused-vars

src/app/page.tsx
  Line 8: React Hook useEffect has a missing dependency: 'fetchData'  react-hooks/exhaustive-deps
```

### 권장 수정

1. **ProductCard.tsx:15** - `category` 파라미터 제거 또는 사용
2. **page.tsx:8** - useEffect deps에 fetchData 추가

## 빌드 검사

```
✓ 빌드 성공

Route (app)                Size     First Load JS
┌ ○ /                     5.2 kB        89.5 kB
├ ○ /login               3.1 kB        87.4 kB
├ ○ /product/[id]        4.8 kB        89.1 kB
└ ○ /profile             2.9 kB        87.2 kB

○  (Static)   prerendered as static content
●  (Dynamic)  server-rendered on demand
```

## 런타임 검사

```
✓ 개발 서버 정상 실행
✓ 페이지 로딩 정상
✓ 콘솔 에러 없음
```

## 다음 단계

- [ ] ESLint 경고 수정
- [ ] 8-review Skill로 최종 품질 검토
```

---

## 오류 유형별 자동 수정

### 타입 에러 자동 수정

```typescript
// 에러: Property 'user' does not exist on type 'AuthState'

// 자동 수정: types/auth.types.ts 생성 또는 수정
export interface AuthState {
  user: User | null
  isLoading: boolean
  error: string | null
}
```

### 빌드 에러 자동 수정

```typescript
// 에러: You're importing a component that needs useState.
//       It only works in a Client Component.

// 자동 수정: 파일 상단에 추가
'use client'

import { useState } from 'react'
// ...
```

### Import 에러 자동 수정

```typescript
// 에러: Module not found: Can't resolve '@/components/ui/button'

// 자동 수정: shadcn/ui 컴포넌트 설치
// npx shadcn@latest add button
```

---

## 성능 체크리스트

### 번들 크기 검사

```bash
# 번들 분석
npm run build
npx @next/bundle-analyzer
```

권장 기준:
- First Load JS < 100KB
- 개별 페이지 < 50KB

### 이미지 최적화 검사

- [ ] 모든 이미지가 `next/image` 사용
- [ ] 적절한 width/height 설정
- [ ] priority 속성 (LCP 이미지)

### 코드 스플리팅 검사

- [ ] 동적 import 사용 (`next/dynamic`)
- [ ] 큰 라이브러리 lazy loading
- [ ] Route별 코드 분리

---

## 검증 자동화 스크립트

```json
// package.json scripts
{
  "scripts": {
    "validate": "npm run typecheck && npm run lint && npm run build",
    "validate:fix": "npm run lint -- --fix && npm run format && npm run validate"
  }
}
```
