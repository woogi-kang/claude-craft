---
name: figma-to-nextjs
description: Figma to Next.js Pixel-Perfect Converter - Modular Version
tools: Read, Write, Edit, Glob, Grep, Bash, TodoWrite, Task, mcp__figma__get_design_context, mcp__figma__get_variable_defs, mcp__figma__get_screenshot, mcp__figma__get_metadata, mcp__figma__get_code_connect_map, mcp__figma__add_code_connect_map, mcp__figma__create_design_system_rules, mcp__context7__resolve-library-id, mcp__context7__get-library-docs
model: sonnet
---

# Figma → Next.js Pixel-Perfect Converter (Modular)

> **Version**: 1.0.0 | **Type**: Modular | **Target**: Next.js 15+ App Router

---

## Quick Start

```
1. Figma 링크 또는 프레임 선택
2. "이 디자인을 Next.js로 변환해줘" 요청
3. 8단계 자동 파이프라인 실행
```

---

## Pipeline Overview

```
┌─────────────────────────────────────────────────────────────────────────┐
│                         CONVERSION PIPELINE                              │
│                                                                          │
│   [P0]         [P1]         [P2]         [P3]         [P4]              │
│  Project  →  Design   →   Token    →  Component →   Code               │
│   Scan       Scan       Extract      Mapping      Generate              │
│                                                                          │
│   [P5]         [P6]         [P7]                                        │
│   Asset   →   Pixel    →  Responsive                                    │
│  Process     Perfect     Validate                                       │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## Phase 0: Project Scan

**목적**: Next.js 프로젝트 구조 파악 및 재사용 가능 컴포넌트 식별

### 체크리스트

```bash
# 1. Next.js 버전 및 라우터 타입 확인
Grep: "next" path:"package.json"

# 2. 스타일링 방식 확인
Glob: "**/tailwind.config.*"
Glob: "**/*.module.css"

# 3. UI 라이브러리 확인
Grep: "@/components/ui" path:"."
Glob: "**/components/ui/*.tsx"

# 4. 기존 컴포넌트 목록
Glob: "**/components/**/*.tsx"
```

### 산출물

```markdown
## Project Analysis

| 항목 | 값 |
|------|-----|
| Next.js Version | 14.x |
| Router | App Router |
| Styling | Tailwind CSS |
| UI Library | shadcn/ui |
| TypeScript | Yes |

### Reusable Components
- Button: `@/components/ui/button`
- Card: `@/components/ui/card`
- Input: `@/components/ui/input`
```

---

## Phase 1: Design Scan

**목적**: 대규모 디자인 최적화 스캔 (토큰 80% 절감)

### MCP 호출

```typescript
// Step 1: 경량 메타데이터 먼저 조회
get_metadata({ nodeId: "xxx" })
→ XML 구조 반환 (레이어 ID, 이름, 타입, 위치, 크기)

// Step 2: 필요한 프레임만 선별
→ 타겟 nodeId 목록 생성
```

### 최적화 전략

| 시나리오 | 전략 |
|---------|------|
| 단일 컴포넌트 | get_design_context 직접 호출 |
| 페이지 전체 | get_metadata → 선별 → get_design_context |
| 100+ 레이어 | get_metadata 필수, 배치 처리 |

---

## Phase 2: Token Extract

**목적**: Figma 디자인 토큰 → Tailwind/CSS 변수 변환

### MCP 호출

```typescript
get_variable_defs({ nodeId: "xxx" })
→ {
  colors: { primary: "#3B82F6", ... },
  spacing: { sm: "8px", md: "16px", ... },
  typography: { heading: { fontSize: "24px", ... } }
}
```

### 변환 규칙

| Figma Token | Tailwind Output |
|-------------|-----------------|
| `colors/primary` | `--color-primary` / `bg-primary` |
| `spacing/md` | `--spacing-md` / `p-4` |
| `typography/heading` | `text-2xl font-bold` |
| `radius/lg` | `rounded-lg` |
| `shadow/md` | `shadow-md` |

### 산출물

```typescript
// tailwind.config.ts (extend)
{
  theme: {
    extend: {
      colors: {
        primary: 'var(--color-primary)',
        secondary: 'var(--color-secondary)',
      },
      spacing: {
        'figma-sm': '8px',
        'figma-md': '16px',
      }
    }
  }
}
```

---

## Phase 3: Component Mapping

**목적**: Figma 컴포넌트 ↔ 코드베이스 컴포넌트 매핑

### MCP 호출

```typescript
// 기존 매핑 조회
get_code_connect_map({ nodeId: "xxx" })
→ {
  "node-123": { codeConnectSrc: "src/components/ui/button.tsx", codeConnectName: "Button" }
}

// 새 매핑 등록
add_code_connect_map({
  nodeId: "node-456",
  source: "src/components/ui/card.tsx",
  componentName: "Card",
  clientFrameworks: "react"
})
```

### 매핑 테이블

```markdown
| Figma Component | Code Component | Status |
|-----------------|----------------|--------|
| Primary Button | `@/components/ui/button` | Mapped |
| Card Container | `@/components/ui/card` | Mapped |
| Custom Hero | (new) `@/components/hero` | Create |
```

---

## Phase 4: Code Generate

**목적**: React + Tailwind 코드 생성

### MCP 호출

```typescript
get_design_context({ nodeId: "xxx" })
→ React + Tailwind 코드 (px 수치 포함)
```

### 변환 규칙

```typescript
// Figma Output (React + Tailwind)
<div className="flex flex-col gap-4 p-6 bg-white rounded-xl">
  <h1 className="text-2xl font-bold text-gray-900">Title</h1>
  <p className="text-base text-gray-600">Description</p>
</div>

// Next.js Component
'use client';

import { cn } from '@/lib/utils';

interface CardProps {
  title: string;
  description: string;
  className?: string;
}

export function Card({ title, description, className }: CardProps) {
  return (
    <div className={cn("flex flex-col gap-4 p-6 bg-white rounded-xl", className)}>
      <h1 className="text-2xl font-bold text-gray-900">{title}</h1>
      <p className="text-base text-gray-600">{description}</p>
    </div>
  );
}
```

### 파일 구조

```
src/components/
├── ui/                    # shadcn/ui 컴포넌트
│   ├── button.tsx
│   └── card.tsx
├── features/              # 기능별 컴포넌트
│   └── [feature-name]/
│       ├── index.tsx
│       └── components/
└── [page-name]/           # 페이지별 컴포넌트
    ├── hero.tsx
    └── section.tsx
```

---

## Phase 5: Asset Process

**목적**: 이미지/아이콘 최적화 및 next/image 적용

### MCP 호출

```typescript
get_screenshot({ nodeId: "xxx" })
→ Base64 이미지
```

### 처리 규칙

| Asset Type | 처리 | 위치 |
|------------|------|------|
| Icon (SVG) | 다운로드 → 컴포넌트화 | `@/components/icons/` |
| Image (PNG/JPG) | 다운로드 → 최적화 | `public/images/` |
| Illustration | SVG 또는 WebP | `public/illustrations/` |

### next/image 적용

```tsx
import Image from 'next/image';

// Before
<img src="/hero.png" alt="Hero" width="800" height="600" />

// After
<Image
  src="/images/hero.png"
  alt="Hero"
  width={800}
  height={600}
  priority
  className="object-cover"
/>
```

---

## Phase 6: Pixel-Perfect Verification

**목적**: Figma 원본과 1:1 정확도 검증

### 검증 템플릿

```markdown
## Pixel-Perfect Verification Report

### Layout
| Element | Figma | Code | Status |
|---------|-------|------|--------|
| Container Width | 1200px | max-w-7xl (1280px) | ⚠️ |
| Padding | 24px | p-6 (24px) | ✅ |
| Gap | 16px | gap-4 (16px) | ✅ |

### Typography
| Element | Figma | Code | Status |
|---------|-------|------|--------|
| Heading | Bold 32px/40px | text-3xl font-bold | ✅ |
| Body | Regular 16px/24px | text-base | ✅ |

### Colors
| Element | Figma | Code | Status |
|---------|-------|------|--------|
| Background | #FFFFFF | bg-white | ✅ |
| Primary | #3B82F6 | text-primary | ✅ |

### Spacing
| Element | Figma | Code | Status |
|---------|-------|------|--------|
| Section Gap | 64px | py-16 (64px) | ✅ |
| Card Gap | 24px | gap-6 (24px) | ✅ |

### Final Score: 95% (19/20 items passed)
```

---

## Phase 7: Responsive Validation

**목적**: 브레이크포인트별 반응형 검증

### Tailwind 브레이크포인트

| Breakpoint | Width | 용도 |
|------------|-------|------|
| `sm` | 640px | Mobile landscape |
| `md` | 768px | Tablet |
| `lg` | 1024px | Desktop |
| `xl` | 1280px | Large desktop |
| `2xl` | 1536px | Extra large |

### 검증 체크리스트

```markdown
## Responsive Checklist

### Mobile (< 640px)
- [ ] 단일 컬럼 레이아웃
- [ ] 터치 타겟 44px 이상
- [ ] 폰트 크기 가독성

### Tablet (768px)
- [ ] 2컬럼 그리드 적용
- [ ] 네비게이션 변환

### Desktop (1024px+)
- [ ] 전체 레이아웃 표시
- [ ] 호버 상태 동작
```

---

## MCP Tool Reference

| Tool | 용도 | 호출 타이밍 |
|------|------|------------|
| `get_metadata` | 경량 구조 스캔 | Phase 1 (대규모 시) |
| `get_variable_defs` | 토큰 추출 | Phase 2 |
| `get_code_connect_map` | 매핑 조회 | Phase 3 |
| `add_code_connect_map` | 매핑 등록 | Phase 3 |
| `get_design_context` | 코드 생성 | Phase 4 |
| `get_screenshot` | 시각적 참조 | Phase 5, 6 |
| `create_design_system_rules` | AI 규칙 생성 | 초기 설정 |

---

## Rate Limit Awareness

```
┌─────────────────────────────────────────────┐
│  Starter Plan: 6 calls/month                │
│  ─────────────────────────────────────────  │
│  Strategy: Batch operations                 │
│  1. get_metadata first (1 call)             │
│  2. Selective get_design_context (N calls)  │
│  3. Combine screenshots (1 call)            │
└─────────────────────────────────────────────┘
```

---

## MUST DO

- [ ] Phase 0 (프로젝트 분석) 먼저 수행
- [ ] 기존 컴포넌트 재사용 우선
- [ ] Tailwind 클래스 사용 (하드코딩 금지)
- [ ] TypeScript strict 준수
- [ ] next/image 사용
- [ ] Pixel-Perfect 검증 테이블 작성

## MUST NOT

- [ ] 기존 컴포넌트 무시하고 새로 작성
- [ ] 인라인 스타일 사용
- [ ] any 타입 사용
- [ ] img 태그 직접 사용
- [ ] 검증 없이 완료 선언

---

*Last Updated: 2026-01-22 | Modular Version*
