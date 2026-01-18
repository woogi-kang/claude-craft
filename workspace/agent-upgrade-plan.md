# Agent Level-Up Plan: Vercel Best Practices Integration

> **분석 일자**: 2026-01-15
> **분석 대상**: vercel-labs/agent-skills (react-best-practices, web-design-guidelines)
> **적용 대상**: nextjs-expert-agent, flutter-to-nextjs-agent, frontend-design-agent

---

## Executive Summary

Vercel의 agent-skills는 **구조화된 규칙 시스템**과 **Impact 기반 우선순위**라는 두 가지 핵심 철학을 기반으로 합니다. 현재 우리 Agent들은 풍부한 패턴과 코드 예제를 갖추고 있지만, **성능 최적화 규칙의 체계화**와 **UI 가이드라인 통합**에서 개선 여지가 있습니다.

### 핵심 개선 방향

| 영역 | 현재 상태 | 개선 후 |
|------|----------|---------|
| **성능 규칙** | Core Web Vitals 중심 단일 스킬 | 8개 카테고리 45개 규칙 체계 |
| **Impact 시스템** | 미적용 | CRITICAL → LOW 5단계 |
| **UI 가이드라인** | 접근성 기본 | 100+ UI 규칙 통합 |
| **코드 검증** | 빌드/타입 체크 | Best Practices 자동 검증 |

---

## Part 1: 상세 분석

### 1.1 Vercel react-best-practices 아키텍처

```
skills/react-best-practices/
├── SKILL.md              # Agent 지시사항 (트리거, 워크플로우)
├── AGENTS.md             # 컴파일된 전체 규칙 (자동 생성)
├── metadata.json         # 버전, 조직, 설명
└── rules/
    ├── _sections.md      # 8개 카테고리 정의
    ├── _template.md      # 규칙 작성 템플릿
    ├── async-*.md        # Waterfall 제거 규칙 (5개)
    ├── bundle-*.md       # 번들 최적화 규칙 (5개)
    ├── server-*.md       # 서버 성능 규칙 (5개)
    ├── client-*.md       # 클라이언트 데이터 규칙 (2개)
    ├── rerender-*.md     # 리렌더링 최적화 규칙 (7개)
    ├── rendering-*.md    # 렌더링 성능 규칙 (7개)
    ├── js-*.md           # JavaScript 성능 규칙 (11개)
    └── advanced-*.md     # 고급 패턴 규칙 (3개)
```

#### 규칙 파일 구조 (YAML Frontmatter + Markdown)

```yaml
---
title: Rule Title
impact: CRITICAL|HIGH|MEDIUM-HIGH|MEDIUM|LOW-MEDIUM|LOW
impactDescription: "정량적 성능 개선 수치 (선택)"
tags: tag1, tag2, tag3
---

# 설명
왜 이 규칙이 중요한지 간결하게 설명

## Bad Example
```typescript
// ❌ 문제가 되는 패턴
const data1 = await fetchA()  // 순차 실행
const data2 = await fetchB()  // 대기
```

## Good Example
```typescript
// ✅ 권장 패턴
const [data1, data2] = await Promise.all([fetchA(), fetchB()])
```
```

#### 8개 카테고리 상세

| # | 카테고리 | Impact | 규칙 수 | 핵심 내용 |
|---|---------|--------|---------|-----------|
| 1 | **Eliminating Waterfalls** | CRITICAL | 5 | Promise.all, Suspense boundaries, dependency parallelization |
| 2 | **Bundle Size Optimization** | CRITICAL | 5 | Barrel file 회피, Dynamic import, Preload on intent |
| 3 | **Server-Side Performance** | HIGH | 5 | React.cache(), LRU 캐싱, after() 비동기, RSC 직렬화 최소화 |
| 4 | **Client-Side Data Fetching** | MEDIUM-HIGH | 2 | SWR deduplication, useSWRSubscription |
| 5 | **Re-render Optimization** | MEDIUM | 7 | memo, startTransition, functional setState, lazy state init |
| 6 | **Rendering Performance** | MEDIUM | 7 | content-visibility, hoist JSX, SVG precision, hydration |
| 7 | **JavaScript Performance** | LOW-MEDIUM | 11 | Set/Map O(1), 루프 최적화, 배열 연산 |
| 8 | **Advanced Patterns** | LOW | 3 | useEffectEvent, ref에 핸들러 저장 |

### 1.2 web-interface-guidelines 분석

```
web-interface-guidelines/
├── README.md        # 전체 가이드라인
├── AGENTS.md        # AI Agent 통합 지시사항
├── command.md       # Agent용 컴팩트 버전
└── install.sh       # 설치 스크립트
```

#### 100+ UI 규칙 카테고리

| 카테고리 | 규칙 수 | 핵심 내용 |
|---------|--------|-----------|
| **Accessibility** | 15+ | aria-label, semantic HTML, 키보드 핸들러 |
| **Focus States** | 8+ | focus-visible:ring, outline-none 대안 |
| **Forms** | 12+ | autocomplete, type, label, inline error |
| **Animation** | 10+ | prefers-reduced-motion, transform/opacity only |
| **Typography** | 8+ | 올바른 구두점, text-wrap: balance |
| **Performance** | 15+ | 50+ 리스트 가상화, DOM 배치, preconnect |
| **Navigation** | 10+ | URL 상태 반영, 딥링크, 파괴적 액션 확인 |
| **Layout** | 10+ | 정렬, 간격, 스크롤바 |
| **Content** | 12+ | 로컬라이제이션, semantic HTML, hydration |

#### 핵심 규칙 예시

```markdown
# Accessibility
- Icon buttons require `aria-label`
- Form controls need labels or aria-labels
- Interactive elements need keyboard handlers
- Use semantic HTML (<button>, <a>, <label>) over divs with click handlers

# Focus States
- Interactive elements need visible focus using `focus-visible:ring-*`
- Avoid `outline-none` without replacement
- Prefer `:focus-visible` over `:focus`

# Forms
- Inputs need `autocomplete` and correct `type` attributes
- Never block paste
- Keep submit buttons enabled with spinners during requests
- Show errors inline and focus first error on submit

# Animation
- Respect `prefers-reduced-motion`
- Animate only `transform`/`opacity` (GPU accelerated)
- Avoid `transition: all`
- Make animations interruptible

# Anti-patterns to Flag
- user-scalable=no
- transition: all
- outline-none without replacement
- divs with click handlers
- images without dimensions
```

---

## Part 2: Gap 분석

### 2.1 nextjs-expert-agent Gap

| 영역 | Vercel 접근법 | 현재 상태 | Gap |
|------|--------------|----------|-----|
| **성능 규칙 체계** | 8개 카테고리 45개 규칙 | 단일 스킬 (24-performance) | 규칙 세분화 필요 |
| **Impact 레벨** | CRITICAL → LOW 5단계 | 미적용 | 우선순위 시스템 도입 |
| **Waterfall 제거** | 5개 전용 규칙 | Promise.all 언급만 | 상세 패턴 추가 |
| **Bundle 최적화** | Barrel file, Dynamic import 등 | Dynamic import만 | 규칙 확장 |
| **UI 가이드라인** | 100+ 규칙 | 접근성 기본만 | 전면 통합 필요 |
| **코드 검증** | 규칙 기반 자동 검증 | 빌드 체크만 | 규칙 검증 추가 |

#### 현재 24-performance 스킬 분석

**강점:**
- Core Web Vitals (LCP, CLS, INP) 상세
- next/image, next/font 최적화
- Dynamic import 패턴
- Lighthouse CI 설정

**부족:**
- Barrel file 회피 규칙 없음
- React.cache() 패턴 미흡
- startTransition 패턴 간단
- content-visibility 미언급
- Suspense 병렬화 전략 부족

### 2.2 flutter-to-nextjs-agent Gap

| 영역 | 이상적 상태 | 현재 상태 | Gap |
|------|-----------|----------|-----|
| **변환 시 최적화** | Best practices 자동 적용 | 1:1 변환만 | 최적화 규칙 통합 |
| **접근성 변환** | aria 속성 자동 매핑 | 미언급 | 접근성 규칙 추가 |
| **성능 검증** | 변환 후 성능 체크리스트 | 빌드 체크만 | 검증 확장 |
| **애니메이션 변환** | GPU 가속 속성만 사용 | 기본 변환만 | 애니메이션 가이드 추가 |

#### 현재 4-components 스킬 분석

**강점:**
- 상세한 위젯 → 컴포넌트 매핑
- Tailwind 스타일 변환 가이드
- Framer Motion 애니메이션 예시
- 복잡한 위젯 (SliverAppBar) 변환

**부족:**
- 변환 시 Best Practices 적용 없음
- GestureDetector → button + aria-label 미언급
- 이미지 변환 시 alt 속성 강조 부족
- 성능 최적화 힌트 없음

### 2.3 frontend-design-agent Gap

| 영역 | Vercel 접근법 | 현재 상태 | Gap |
|------|--------------|----------|-----|
| **접근성 규칙** | 15+ 상세 규칙 | 기본 WCAG | 규칙 확장 |
| **폼 가이드라인** | 12+ 규칙 | 미포함 | 폼 스킬 추가 |
| **애니메이션 규칙** | Motion 감도, GPU 가속 | 기본만 | 규칙 상세화 |
| **타이포그래피** | 구두점, text-wrap | 폰트 선택만 | 규칙 추가 |

---

## Part 3: 개선 아키텍처 설계

### 3.1 신규 레퍼런스 문서 구조

```
nextjs-expert-agent-skills/
└── _references/
    ├── ARCHITECTURE-PATTERN.md     # (기존)
    ├── STATE-PATTERN.md            # (기존)
    ├── COMPONENT-PATTERN.md        # (기존)
    ├── TEST-PATTERN.md             # (기존)
    ├── SERVER-ACTION-PATTERN.md    # (기존)
    ├── DATABASE-PATTERN.md         # (기존)
    │
    │ # ===== 신규 추가 =====
    ├── REACT-PERF-RULES.md         # Vercel 45개 규칙 통합
    ├── UI-GUIDELINES.md            # web-interface-guidelines 통합
    └── IMPACT-LEVELS.md            # Impact 레벨 시스템 정의
```

### 3.2 REACT-PERF-RULES.md 설계

```markdown
# React Performance Rules Reference

Vercel Engineering의 React/Next.js 성능 최적화 규칙을 통합한 레퍼런스입니다.
코드 생성 및 리뷰 시 이 규칙들을 자동으로 적용합니다.

## Impact 레벨 정의

| Level | Symbol | 의미 | 액션 |
|-------|--------|------|------|
| CRITICAL | 🔴 | 2-10x 성능 영향 | 반드시 적용 |
| HIGH | 🟠 | 현저한 성능 개선 | 강력 권고 |
| MEDIUM-HIGH | 🟡 | 의미있는 개선 | 권고 |
| MEDIUM | 🔵 | 점진적 개선 | 고려 |
| LOW-MEDIUM | ⚪ | 마이크로 최적화 | 핫패스만 |
| LOW | ⬜ | 특수 상황 | 필요시 |

---

## 1. Eliminating Waterfalls (CRITICAL)

### 1.1 async-parallel: Promise.all for Independent Operations

**Impact**: 🔴 CRITICAL (2-10x faster)

```typescript
// ❌ Bad: Sequential awaits create waterfall
const user = await fetchUser()
const posts = await fetchPosts()
const comments = await fetchComments()

// ✅ Good: Parallel execution
const [user, posts, comments] = await Promise.all([
  fetchUser(),
  fetchPosts(),
  fetchComments()
])
```

### 1.2 async-suspense-boundaries: Strategic Suspense Boundaries

**Impact**: 🔴 CRITICAL (faster initial paint)

```tsx
// ❌ Bad: Entire page waits for all data
async function Dashboard() {
  const stats = await getStats()
  const posts = await getPosts()
  return (
    <div>
      <Header />
      <StatsCards stats={stats} />
      <PostList posts={posts} />
    </div>
  )
}

// ✅ Good: Static UI renders immediately
function Dashboard() {
  return (
    <div>
      <Header />  {/* Renders immediately */}
      <Suspense fallback={<StatsSkeleton />}>
        <StatsSection />  {/* Streams when ready */}
      </Suspense>
      <Suspense fallback={<PostsSkeleton />}>
        <PostsSection />  {/* Streams when ready */}
      </Suspense>
    </div>
  )
}
```

### 1.3 server-parallel-fetching: Component Composition for Parallelization

**Impact**: 🔴 CRITICAL (eliminates server-side waterfalls)

```tsx
// ❌ Bad: Waterfall in server components
async function Page() {
  const user = await getUser()  // Blocks everything
  return <UserProfile user={user} children={<UserPosts userId={user.id} />} />
}

// ✅ Good: Sibling components fetch in parallel
async function Page() {
  return (
    <div>
      <UserHeader />     {/* Fetches user */}
      <UserPosts />      {/* Fetches posts in parallel */}
      <UserActivity />   {/* Fetches activity in parallel */}
    </div>
  )
}
```

---

## 2. Bundle Size Optimization (CRITICAL)

### 2.1 bundle-barrel-imports: Avoid Barrel Files

**Impact**: 🔴 CRITICAL (200-800ms savings, 15-70% faster dev boot)

```typescript
// ❌ Bad: Barrel import loads all icons (~10,000 modules)
import { Check, X, Menu } from 'lucide-react'

// ✅ Good: Direct imports
import Check from 'lucide-react/dist/esm/icons/check'
import X from 'lucide-react/dist/esm/icons/x'
import Menu from 'lucide-react/dist/esm/icons/menu'

// ✅ Better: Configure optimizePackageImports (Next.js 13.5+)
// next.config.ts
const nextConfig = {
  experimental: {
    optimizePackageImports: ['lucide-react', '@radix-ui/react-*', 'lodash'],
  },
}
```

### 2.2 bundle-dynamic-imports: Dynamic Import for Heavy Components

**Impact**: 🔴 CRITICAL (reduces initial bundle)

```typescript
// ❌ Bad: Heavy component in main bundle
import { MonacoEditor } from '@monaco-editor/react'  // ~300KB

// ✅ Good: Lazy load when needed
import dynamic from 'next/dynamic'

const MonacoEditor = dynamic(
  () => import('@monaco-editor/react'),
  {
    loading: () => <EditorSkeleton />,
    ssr: false,
  }
)
```

### 2.3 bundle-preload: Preload on User Intent

**Impact**: 🟠 HIGH

```tsx
'use client'

import { useCallback } from 'react'

export function FeatureButton() {
  const handleMouseEnter = useCallback(() => {
    // Preload on hover
    import('@/features/heavy-feature/components')
  }, [])

  return (
    <Button onMouseEnter={handleMouseEnter} onClick={handleClick}>
      Open Feature
    </Button>
  )
}
```

---

## 3. Server-Side Performance (HIGH)

### 3.1 server-cache-react: Per-Request Deduplication

**Impact**: 🟠 HIGH

```typescript
import { cache } from 'react'

// ✅ Multiple calls within same request = single execution
export const getCurrentUser = cache(async () => {
  const session = await auth()
  if (!session?.user?.id) return null
  return await db.user.findUnique({ where: { id: session.user.id } })
})

// Component A calls getCurrentUser() → DB query
// Component B calls getCurrentUser() → Returns cached result
```

### 3.2 server-serialization: Minimize RSC Boundary Data

**Impact**: 🟠 HIGH

```tsx
// ❌ Bad: Pass entire object
async function Page() {
  const user = await getUser()  // { id, name, email, avatar, settings, ... }
  return <ClientComponent user={user} />  // Serializes everything
}

// ✅ Good: Pass only needed fields
async function Page() {
  const user = await getUser()
  return <ClientComponent name={user.name} avatar={user.avatar} />
}
```

---

## 4. Re-render Optimization (MEDIUM)

### 4.1 rerender-memo: Extract to Memoized Components

**Impact**: 🔵 MEDIUM

```tsx
// ❌ Bad: Expensive computation runs even during loading
function UserProfile({ userId }: { userId: string }) {
  const { data: user, isLoading } = useUser(userId)
  const avatar = useMemo(() => generateAvatar(user), [user])  // Runs anyway

  if (isLoading) return <Skeleton />
  return <Avatar src={avatar} />
}

// ✅ Good: Extracted component enables early return
function UserProfile({ userId }: { userId: string }) {
  const { data: user, isLoading } = useUser(userId)

  if (isLoading) return <Skeleton />
  return <UserAvatar user={user} />  // Only renders when data exists
}

const UserAvatar = memo(function UserAvatar({ user }: { user: User }) {
  const avatar = useMemo(() => generateAvatar(user), [user])
  return <Avatar src={avatar} />
})
```

### 4.2 rerender-transitions: Non-Urgent Updates

**Impact**: 🔵 MEDIUM

```tsx
'use client'

import { useTransition } from 'react'

function SearchResults() {
  const [results, setResults] = useState([])
  const [isPending, startTransition] = useTransition()

  const handleScroll = (e: UIEvent) => {
    // ❌ Bad: Blocks UI on every scroll
    // setScrollPosition(e.target.scrollTop)

    // ✅ Good: Non-blocking update
    startTransition(() => {
      setScrollPosition(e.target.scrollTop)
    })
  }
}
```

---

## 5. Rendering Performance (MEDIUM)

### 5.1 rendering-content-visibility: Defer Off-Screen Content

**Impact**: 🟠 HIGH (10x faster initial render for long lists)

```css
.list-item {
  content-visibility: auto;
  contain-intrinsic-size: 0 80px;
}
```

```tsx
function MessageList({ messages }: { messages: Message[] }) {
  return (
    <div className="overflow-y-auto h-screen">
      {messages.map(msg => (
        <div key={msg.id} className="list-item">
          <MessageItem message={msg} />
        </div>
      ))}
    </div>
  )
}
```

### 5.2 rendering-hoist-jsx: Static JSX Outside Components

**Impact**: 🔵 MEDIUM

```tsx
// ❌ Bad: Icon recreated every render
function Button({ children }) {
  return (
    <button>
      <svg>...</svg>  {/* New object each render */}
      {children}
    </button>
  )
}

// ✅ Good: Static JSX hoisted
const ArrowIcon = <svg>...</svg>

function Button({ children }) {
  return (
    <button>
      {ArrowIcon}  {/* Same reference */}
      {children}
    </button>
  )
}
```

---

## 6. JavaScript Performance (LOW-MEDIUM)

### 6.1 js-set-map-lookups: O(1) Membership Checks

**Impact**: ⚪ LOW-MEDIUM

```typescript
// ❌ Bad: O(n) lookup per item
const allowedIds = ['a', 'b', 'c', ...]
items.filter(item => allowedIds.includes(item.id))

// ✅ Good: O(1) lookup
const allowedIdSet = new Set(allowedIds)
items.filter(item => allowedIdSet.has(item.id))
```

---

## Quick Reference Checklist

코드 생성/리뷰 시 확인:

### CRITICAL (반드시 적용)
- [ ] 독립적인 비동기 작업은 Promise.all 사용
- [ ] 데이터 의존 컴포넌트만 Suspense로 감싸기
- [ ] 서버 컴포넌트 병렬 구성
- [ ] Barrel file import 회피 또는 optimizePackageImports 설정
- [ ] 대용량 컴포넌트 Dynamic import

### HIGH (강력 권고)
- [ ] React.cache()로 요청 내 중복 제거
- [ ] RSC 경계에서 필요한 데이터만 전달
- [ ] 긴 리스트에 content-visibility 적용
- [ ] hover 시 다음 경로 프리로드

### MEDIUM (권고)
- [ ] 비용 높은 계산을 메모된 컴포넌트로 분리
- [ ] 빈번한 업데이트에 startTransition 사용
- [ ] 정적 JSX 호이스팅
- [ ] SWR로 클라이언트 요청 자동 중복 제거
```

### 3.3 UI-GUIDELINES.md 설계

```markdown
# UI Guidelines Reference

web-interface-guidelines를 통합한 UI 코드 검증 레퍼런스입니다.

---

## 1. Accessibility (접근성)

### 1.1 아이콘 버튼

```tsx
// ❌ Bad: 레이블 없음
<button onClick={handleClose}>
  <X className="h-4 w-4" />
</button>

// ✅ Good: aria-label 추가
<button onClick={handleClose} aria-label="닫기">
  <X className="h-4 w-4" aria-hidden="true" />
</button>

// ✅ Alternative: sr-only 사용
<button onClick={handleClose}>
  <X className="h-4 w-4" aria-hidden="true" />
  <span className="sr-only">닫기</span>
</button>
```

### 1.2 Semantic HTML

```tsx
// ❌ Bad: div with click handler
<div onClick={handleClick} className="cursor-pointer">Click me</div>

// ✅ Good: Semantic button
<button onClick={handleClick}>Click me</button>

// ❌ Bad: div as link
<div onClick={() => router.push('/about')}>About</div>

// ✅ Good: Semantic anchor
<Link href="/about">About</Link>
```

### 1.3 키보드 네비게이션

```tsx
// ✅ Interactive elements need keyboard handlers
<div
  role="button"
  tabIndex={0}
  onClick={handleClick}
  onKeyDown={(e) => {
    if (e.key === 'Enter' || e.key === ' ') {
      e.preventDefault()
      handleClick()
    }
  }}
>
  Interactive element
</div>
```

---

## 2. Focus States (포커스 상태)

### 2.1 필수 포커스 인디케이터

```tsx
// ❌ Bad: outline 제거만
<button className="outline-none">Click</button>

// ✅ Good: focus-visible 대체
<button className="outline-none focus-visible:ring-2 focus-visible:ring-ring">
  Click
</button>

// ✅ Better: Tailwind 기본 설정 활용
<Button>Click</Button>  // shadcn/ui가 자동 처리
```

### 2.2 focus vs focus-visible

```css
/* ❌ Bad: 모든 포커스에 스타일 */
button:focus {
  outline: 2px solid blue;
}

/* ✅ Good: 키보드 포커스만 */
button:focus-visible {
  outline: 2px solid blue;
}
```

---

## 3. Forms (폼)

### 3.1 필수 속성

```tsx
// ❌ Bad: 속성 누락
<input type="text" />

// ✅ Good: 필수 속성 포함
<input
  type="email"
  autoComplete="email"
  id="email"
  aria-describedby="email-error"
/>
<label htmlFor="email">Email</label>
<span id="email-error" role="alert">{error}</span>
```

### 3.2 패스워드 입력

```tsx
// ❌ Bad: paste 차단
<input type="password" onPaste={(e) => e.preventDefault()} />

// ✅ Good: paste 허용
<input
  type="password"
  autoComplete="current-password"  // 또는 "new-password"
/>
```

### 3.3 제출 버튼

```tsx
// ❌ Bad: 제출 중 비활성화
<Button type="submit" disabled={isSubmitting}>
  {isSubmitting ? 'Loading...' : 'Submit'}
</Button>

// ✅ Good: 활성 상태 유지 + 스피너
<Button type="submit" disabled={isSubmitting}>
  {isSubmitting && <Loader2 className="mr-2 h-4 w-4 animate-spin" />}
  Submit
</Button>
```

### 3.4 에러 처리

```tsx
// ✅ 인라인 에러 + 첫 에러 포커스
function handleSubmit() {
  const errors = validate(data)
  if (errors.length > 0) {
    setErrors(errors)
    // Focus first error field
    document.getElementById(errors[0].field)?.focus()
  }
}
```

---

## 4. Animation (애니메이션)

### 4.1 모션 감도 존중

```tsx
// ✅ prefers-reduced-motion 감지
import { useReducedMotion } from 'framer-motion'

function AnimatedComponent() {
  const shouldReduceMotion = useReducedMotion()

  return (
    <motion.div
      animate={{ x: shouldReduceMotion ? 0 : 100 }}
      transition={{ duration: shouldReduceMotion ? 0 : 0.3 }}
    />
  )
}
```

```css
/* CSS로 처리 */
@media (prefers-reduced-motion: reduce) {
  * {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
  }
}
```

### 4.2 GPU 가속 속성만 애니메이션

```css
/* ❌ Bad: Layout 속성 애니메이션 */
.element {
  transition: all 0.3s;  /* width, height 등 포함 */
}

/* ✅ Good: transform/opacity만 */
.element {
  transition: transform 0.3s, opacity 0.3s;
}
```

### 4.3 중단 가능한 애니메이션

```tsx
// ✅ 애니메이션 중단 가능
<motion.div
  animate={{ x: isOpen ? 0 : -300 }}
  transition={{ type: 'spring', damping: 20 }}
  // 새 상태 변경 시 현재 위치에서 새 애니메이션 시작
/>
```

---

## 5. Typography (타이포그래피)

### 5.1 올바른 구두점

```tsx
// ❌ Bad
<p>Loading...</p>
<p>"Hello World"</p>

// ✅ Good
<p>Loading…</p>  {/* 말줄임표 */}
<p>"Hello World"</p>  {/* 둥근 따옴표 */}
```

### 5.2 제목 균형 맞추기

```css
/* ✅ 제목에 text-wrap: balance */
h1, h2, h3 {
  text-wrap: balance;
}
```

### 5.3 Non-breaking spaces

```tsx
// ❌ Bad: 단위가 줄바꿈될 수 있음
<span>100 MB</span>

// ✅ Good: &nbsp; 사용
<span>100&nbsp;MB</span>
```

---

## 6. Performance (성능)

### 6.1 리스트 가상화

```tsx
// ❌ Bad: 50개 이상 아이템 직접 렌더링
{items.map(item => <Item key={item.id} {...item} />)}

// ✅ Good: 가상화 사용
import { useVirtualizer } from '@tanstack/react-virtual'

function VirtualList({ items }) {
  const virtualizer = useVirtualizer({
    count: items.length,
    getScrollElement: () => parentRef.current,
    estimateSize: () => 50,
  })

  return (
    <div ref={parentRef} className="h-[400px] overflow-auto">
      <div style={{ height: virtualizer.getTotalSize() }}>
        {virtualizer.getVirtualItems().map(row => (
          <Item key={items[row.index].id} {...items[row.index]} />
        ))}
      </div>
    </div>
  )
}
```

### 6.2 이미지 차원 명시

```tsx
// ❌ Bad: CLS 유발
<img src={url} alt="..." />

// ✅ Good: 차원 명시
<Image src={url} alt="..." width={400} height={300} />
```

### 6.3 CDN Preconnect

```tsx
// app/layout.tsx
export default function RootLayout({ children }) {
  return (
    <html>
      <head>
        <link rel="preconnect" href="https://fonts.googleapis.com" />
        <link rel="preconnect" href="https://images.yourcdn.com" />
      </head>
      <body>{children}</body>
    </html>
  )
}
```

---

## 7. Navigation (네비게이션)

### 7.1 URL 상태 반영

```tsx
// ✅ 필터, 탭, 페이지네이션은 URL에 반영
import { useQueryState } from 'nuqs'

function Filters() {
  const [category, setCategory] = useQueryState('category')
  const [page, setPage] = useQueryState('page')
  // URL: ?category=electronics&page=2
}
```

### 7.2 파괴적 액션 확인

```tsx
// ✅ 삭제 전 확인
<AlertDialog>
  <AlertDialogTrigger asChild>
    <Button variant="destructive">Delete</Button>
  </AlertDialogTrigger>
  <AlertDialogContent>
    <AlertDialogHeader>
      <AlertDialogTitle>정말 삭제하시겠습니까?</AlertDialogTitle>
      <AlertDialogDescription>
        이 작업은 되돌릴 수 없습니다.
      </AlertDialogDescription>
    </AlertDialogHeader>
    <AlertDialogFooter>
      <AlertDialogCancel>취소</AlertDialogCancel>
      <AlertDialogAction onClick={handleDelete}>삭제</AlertDialogAction>
    </AlertDialogFooter>
  </AlertDialogContent>
</AlertDialog>
```

---

## Anti-Patterns Checklist

코드 생성/리뷰 시 다음을 플래그:

- [ ] `user-scalable=no` in viewport
- [ ] `transition: all` without specific properties
- [ ] `outline-none` without focus-visible replacement
- [ ] `div` with onClick but no role/tabIndex
- [ ] `<img>` without width/height
- [ ] paste blocked on inputs
- [ ] 50+ items without virtualization
- [ ] hardcoded date/number formats (use Intl.*)
```

---

## Part 4: 구체적 구현 계획

### 4.1 nextjs-expert-agent 개선

#### Phase 1: 레퍼런스 문서 추가 (Day 1-2)

| 파일 | 내용 | 라인 수 |
|------|------|---------|
| `_references/REACT-PERF-RULES.md` | 45개 성능 규칙 통합 | ~800 |
| `_references/UI-GUIDELINES.md` | 100+ UI 규칙 통합 | ~600 |
| `_references/IMPACT-LEVELS.md` | Impact 레벨 시스템 정의 | ~100 |

#### Phase 2: 기존 스킬 보강 (Day 3-4)

| 스킬 | 변경 내용 |
|------|----------|
| `24-performance/SKILL.md` | Waterfall 제거, Bundle 최적화 섹션 확장 |
| `3-design-system/SKILL.md` | UI Guidelines 접근성 체크리스트 추가 |
| `9-api-client/SKILL.md` | SWR deduplication 패턴 추가 |
| `14-feature/SKILL.md` | 코드 생성 시 Best Practices 자동 적용 가이드 |

#### Phase 3: Agent 정의 업데이트 (Day 5)

```markdown
# nextjs-expert-agent.md 추가 내용

## 코드 생성 원칙 (신규)

### Performance Rules (REACT-PERF-RULES.md 참조)
코드 생성 시 다음 규칙을 자동 적용합니다:

1. **CRITICAL 규칙 (반드시 적용)**
   - 독립적인 비동기 작업 → Promise.all()
   - 데이터 의존 컴포넌트만 → Suspense
   - 대용량 라이브러리 → Dynamic import

2. **HIGH 규칙 (강력 권고)**
   - 동일 요청 내 중복 호출 → React.cache()
   - RSC 경계 → 필요한 데이터만 전달
   - 긴 리스트 → content-visibility

### UI Guidelines (UI-GUIDELINES.md 참조)
모든 UI 코드에 다음을 적용합니다:

1. **접근성**
   - 아이콘 버튼 → aria-label 필수
   - Interactive elements → semantic HTML 우선

2. **폼**
   - input → autocomplete, type 속성 필수
   - 에러 → 인라인 표시 + 첫 필드 포커스

3. **애니메이션**
   - prefers-reduced-motion 존중
   - transform/opacity만 애니메이션
```

### 4.2 flutter-to-nextjs-agent 개선

#### Phase 1: 변환 규칙 추가 (Day 1-2)

```markdown
# 4-components/SKILL.md 추가 내용

## 변환 시 Best Practices 자동 적용

### Accessibility 변환
| Flutter | Next.js | 규칙 |
|---------|---------|------|
| `GestureDetector(onTap:)` | `<button onClick={} aria-label="">` | 접근성 |
| `IconButton(icon:)` | `<Button aria-label="">` | 접근성 |
| `Image.network()` | `<Image alt="" />` | 접근성 |
| `Semantics(label:)` | `aria-label=""` | 접근성 |

### Performance 변환
| Flutter | Next.js | 규칙 |
|---------|---------|------|
| `FutureBuilder` | `<Suspense>` + async component | Waterfall 제거 |
| 대형 위젯 | `dynamic(() => import())` | Bundle 최적화 |
| 병렬 API 호출 | `Promise.all()` | Waterfall 제거 |

### Animation 변환
| Flutter | Next.js | 규칙 |
|---------|---------|------|
| `AnimatedContainer` | `motion.div` + transform only | GPU 가속 |
| 모든 애니메이션 | `prefers-reduced-motion` 체크 | 접근성 |
```

#### Phase 2: 검증 스킬 확장 (Day 3)

```markdown
# 7-validate/SKILL.md 추가 내용

## Performance Checklist

### CRITICAL (통과 필수)
- [ ] 순차 await 없음 (Promise.all 사용)
- [ ] 대용량 import 없음 (Dynamic import 사용)
- [ ] barrel file import 없음 (optimizePackageImports 설정)

### HIGH (강력 권고)
- [ ] React.cache() 적용
- [ ] 긴 리스트에 content-visibility 또는 가상화

### Accessibility Checklist
- [ ] 모든 버튼에 접근 가능한 이름
- [ ] 모든 이미지에 alt 속성
- [ ] 폼 입력에 label 연결
- [ ] focus-visible 스타일 존재
```

### 4.3 frontend-design-agent 개선

#### Phase 1: 참조 문서 확장 (Day 1-2)

```markdown
# _references/ACCESSIBILITY-CHECKLIST.md 확장

## web-interface-guidelines 통합

### Interaction Rules
- [ ] 키보드로 모든 flow 완료 가능
- [ ] WAI-ARIA 패턴 준수
- [ ] 포커스 트랩 적절히 구현
- [ ] 24px 이상 터치 타겟 (모바일 44px)
- [ ] 16px 이상 텍스트 입력 (iOS 줌 방지)

### Focus Rules
- [ ] 모든 interactive element에 focus-visible 스타일
- [ ] outline-none 사용 시 대체 스타일 필수
- [ ] :focus 대신 :focus-visible 사용

### Form Rules
- [ ] 모든 input에 label
- [ ] autocomplete 속성 적용
- [ ] paste 차단 금지
- [ ] 제출 중에도 버튼 활성 (스피너로 표시)
- [ ] 인라인 에러 + 첫 에러 필드 포커스
```

#### Phase 2: 스킬 보강 (Day 3)

```markdown
# 7-motion/SKILL.md 추가

## Animation Guidelines (web-design-guidelines 기반)

### Required
- [ ] `prefers-reduced-motion` 감지 및 존중
- [ ] `transform`, `opacity`만 애니메이션 (GPU 가속)
- [ ] 중단 가능한 애니메이션 설계

### Forbidden
- ❌ `transition: all`
- ❌ width, height, top, left 애니메이션
- ❌ 300ms 이상 지속 시간 (사용자 차단)

### Pattern
```tsx
import { useReducedMotion } from 'framer-motion'

function Component() {
  const shouldReduceMotion = useReducedMotion()

  return (
    <motion.div
      animate={{ scale: shouldReduceMotion ? 1 : 1.1 }}
      transition={{ duration: shouldReduceMotion ? 0 : 0.2 }}
    />
  )
}
```
```

---

## Part 5: 구현 로드맵

### Week 1: Foundation

| Day | Task | Output |
|-----|------|--------|
| 1 | REACT-PERF-RULES.md 작성 | 800줄 레퍼런스 |
| 2 | UI-GUIDELINES.md 작성 | 600줄 레퍼런스 |
| 3 | 24-performance 스킬 확장 | 업데이트된 스킬 |
| 4 | 3-design-system 접근성 추가 | 업데이트된 스킬 |
| 5 | Agent 정의 업데이트 | 3개 Agent 업데이트 |

### Week 2: Enhancement

| Day | Task | Output |
|-----|------|--------|
| 1 | flutter-to-nextjs 변환 규칙 추가 | 4-components 보강 |
| 2 | flutter-to-nextjs 검증 확장 | 7-validate 보강 |
| 3 | frontend-design 접근성 확장 | ACCESSIBILITY-CHECKLIST |
| 4 | frontend-design motion 규칙 | 7-motion 보강 |
| 5 | 통합 테스트 및 문서화 | CLAUDE.md 업데이트 |

---

## Appendix: Impact Level Reference

```
🔴 CRITICAL    : 2-10x 성능 차이, 반드시 적용
🟠 HIGH        : 현저한 성능/UX 개선, 강력 권고
🟡 MEDIUM-HIGH : 의미있는 개선, 권고
🔵 MEDIUM      : 점진적 개선, 고려
⚪ LOW-MEDIUM  : 마이크로 최적화, 핫패스만
⬜ LOW         : 특수 상황, 필요시
```

이 계획은 Vercel의 검증된 best practices를 우리 Agent에 체계적으로 통합하여,
코드 품질과 성능을 한 단계 끌어올리는 것을 목표로 합니다.

---

## Part 6: agent-browser 분석 및 통합 계획

### 6.1 agent-browser 개요

Vercel Labs의 **agent-browser**는 AI 에이전트를 위한 헤드리스 브라우저 자동화 CLI입니다.

```
┌─────────────────────────────────────────────────────────────┐
│                    agent-browser 아키텍처                    │
├─────────────────────────────────────────────────────────────┤
│  ┌──────────────┐     ┌──────────────┐     ┌────────────┐  │
│  │  Rust CLI    │ ──▶ │  Node.js     │ ──▶ │ Playwright │  │
│  │  (파싱)      │     │  Daemon      │     │ (Chromium) │  │
│  └──────────────┘     └──────────────┘     └────────────┘  │
│         │                                                   │
│         ▼                                                   │
│  ┌──────────────────────────────────────────────────────┐  │
│  │           Refs 시스템 (@e1, @e2, @e3...)              │  │
│  │   • 결정론적 요소 선택                                │  │
│  │   • DOM 재쿼리 불필요                                 │  │
│  │   • LLM 워크플로우 최적화                             │  │
│  └──────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
```

### 6.2 핵심 기능

#### 명령어 체계

| 카테고리 | 명령어 | 설명 |
|---------|--------|------|
| **네비게이션** | `open <url>` | 페이지 열기 |
| | `back`, `forward` | 히스토리 이동 |
| | `reload` | 새로고침 |
| **스냅샷** | `snapshot` | 전체 접근성 트리 |
| | `snapshot -i` | 상호작용 요소만 (AI 권장) |
| | `snapshot --compact` | 압축된 트리 |
| **상호작용** | `click @e1` | Ref로 클릭 |
| | `fill @e2 "text"` | 텍스트 입력 |
| | `hover @e3` | 호버 |
| | `scroll down 500` | 스크롤 |
| **정보 조회** | `get text @e1` | 텍스트 추출 |
| | `get value @e2` | 입력 값 |
| | `is visible @e3` | 가시성 확인 |
| **캡처** | `screenshot` | 스크린샷 |
| | `screenshot --full` | 전체 페이지 |
| | `pdf` | PDF 생성 |
| **대기** | `wait @e1` | 요소 대기 |
| | `wait network-idle` | 네트워크 대기 |

#### Refs 시스템 (핵심 혁신)

```bash
# 1. 스냅샷으로 Refs 획득
$ agent-browser snapshot -i
- button "로그인" [ref=e1]
- textbox "이메일" [ref=e2]
- textbox "비밀번호" [ref=e3]
- button "제출" [ref=e4]

# 2. Refs로 상호작용
$ agent-browser fill @e2 "user@example.com"
$ agent-browser fill @e3 "password123"
$ agent-browser click @e4
```

**장점:**
- **결정론적**: CSS 선택자/XPath의 불안정성 해결
- **AI 친화적**: LLM이 쉽게 파싱 가능
- **성능**: DOM 재탐색 불필요
- **안정성**: 페이지 구조 변경에도 Ref 유지

#### 시맨틱 로케이터 (Alternative)

```bash
# Role + Name으로 요소 찾기
agent-browser find role button click --name "Submit"
agent-browser find label "Email" fill "test@test.com"
```

### 6.3 Playwright MCP와의 비교

| 항목 | agent-browser | Playwright MCP |
|------|--------------|----------------|
| **아키텍처** | Native CLI (Rust + Node.js) | MCP Server (JSON-RPC) |
| **요소 선택** | Refs 시스템 (결정론적) | CSS/XPath (상대적 불안정) |
| **AI 최적화** | 접근성 트리 기반 | DOM 기반 |
| **세션 관리** | 내장 (--session) | 별도 구현 필요 |
| **성능** | Rust CLI로 빠름 | IPC 오버헤드 |
| **설치** | `npm i -g agent-browser` | MCP 서버 설정 |
| **JSON 출력** | `--json` 플래그 | 기본 제공 |

### 6.4 개발 프로세스 강화 방안

#### A. E2E 테스트 자동화

```markdown
# nextjs-expert-agent e2e-test 스킬 확장

## agent-browser 기반 E2E 테스트 패턴

### 테스트 워크플로우
1. `agent-browser open http://localhost:3000`
2. `agent-browser snapshot -i --json` → 요소 맵 획득
3. AI가 테스트 시나리오 실행
4. `agent-browser screenshot` → 결과 캡처

### 로그인 테스트 예시
```bash
# 테스트 스크립트 (.sh)
agent-browser open http://localhost:3000/login
agent-browser snapshot -i
agent-browser fill @e2 "test@example.com"
agent-browser fill @e3 "password"
agent-browser click @e4
agent-browser wait network-idle
agent-browser screenshot test-results/login-success.png
```
```

#### B. Visual Regression Testing

```markdown
# 시각적 회귀 테스트

## agent-browser + 이미지 비교
```bash
# 기준 이미지 캡처
agent-browser open http://localhost:3000
agent-browser screenshot baseline/home.png

# 변경 후 비교
agent-browser screenshot current/home.png
# 이미지 비교 도구로 diff 생성
```
```

#### C. 폼 자동화 테스트

```markdown
# 폼 검증 자동화

## 에러 케이스 테스트
```bash
agent-browser open http://localhost:3000/register
agent-browser snapshot -i

# 빈 폼 제출
agent-browser click @submit-btn
agent-browser snapshot  # 에러 메시지 확인

# 잘못된 이메일
agent-browser fill @email "invalid"
agent-browser click @submit-btn
agent-browser get text @email-error
```
```

#### D. Accessibility 테스트

```markdown
# 접근성 자동 검증

## 스냅샷으로 접근성 트리 검사
```bash
agent-browser open http://localhost:3000
agent-browser snapshot --json > a11y-tree.json

# AI가 분석:
# - 모든 버튼에 접근 가능한 이름 있는지
# - 폼 요소에 레이블 연결되어 있는지
# - 이미지에 alt 텍스트 있는지
```
```

### 6.5 새로운 스킬 추가 제안

#### agent-browser-test 스킬

```markdown
# skills/💻 개발/agent-browser-test/SKILL.md

## 개요
agent-browser CLI를 활용한 E2E 테스트 자동화 스킬

## 트리거
- "e2e 테스트", "브라우저 테스트", "agent-browser"

## 워크플로우

### 1. 테스트 환경 설정
```bash
# agent-browser 설치 확인
which agent-browser || npm i -g agent-browser
agent-browser install  # Chromium 설치
```

### 2. 테스트 시나리오 생성
```bash
# 스냅샷으로 요소 맵 획득
agent-browser open $URL
agent-browser snapshot -i --json > elements.json
```

### 3. 테스트 스크립트 실행
```bash
# 세션 사용으로 상태 유지
agent-browser --session test1 open $URL
agent-browser --session test1 fill @email "test@test.com"
agent-browser --session test1 click @submit
agent-browser --session test1 wait network-idle
```

### 4. 결과 검증
```bash
# 텍스트 검증
agent-browser get text @success-message
# 스크린샷 캡처
agent-browser screenshot test-results/$(date +%s).png
```

## 장점 (vs Playwright MCP)
- Refs 기반 결정론적 선택
- AI 친화적 접근성 트리
- 네이티브 CLI 성능
- 세션 관리 내장
```

### 6.6 통합 로드맵

```
Week 1: 기초 통합
├── Day 1: agent-browser 설치 및 기본 사용법 문서화
├── Day 2: e2e-test 스킬에 agent-browser 옵션 추가
├── Day 3: 테스트 스크립트 템플릿 생성
├── Day 4: CI/CD 통합 가이드
└── Day 5: 문서화 및 예제

Week 2: 고급 통합
├── Day 1: Visual Regression 워크플로우
├── Day 2: 접근성 자동 검증 스킬
├── Day 3: 폼 테스트 자동화
├── Day 4: 멀티 세션 테스트
└── Day 5: 성능 벤치마크 및 최적화
```

### 6.7 agent-browser 권장 워크플로우

```
┌─────────────────────────────────────────────────────────────┐
│              AI Agent E2E Testing Workflow                   │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  1. OPEN                                                     │
│     agent-browser open http://localhost:3000                │
│                          │                                   │
│                          ▼                                   │
│  2. SNAPSHOT                                                 │
│     agent-browser snapshot -i --json                        │
│     → 접근성 트리 + Refs 획득                                │
│                          │                                   │
│                          ▼                                   │
│  3. AI ANALYZE                                               │
│     LLM이 스냅샷 분석하여 테스트 대상 Refs 식별              │
│                          │                                   │
│                          ▼                                   │
│  4. INTERACT                                                 │
│     agent-browser click @e1                                 │
│     agent-browser fill @e2 "data"                           │
│                          │                                   │
│                          ▼                                   │
│  5. RE-SNAPSHOT (페이지 변경 시)                             │
│     agent-browser snapshot -i --json                        │
│                          │                                   │
│                          ▼                                   │
│  6. VERIFY                                                   │
│     agent-browser get text @result                          │
│     agent-browser is visible @success                       │
│                          │                                   │
│                          ▼                                   │
│  7. CAPTURE                                                  │
│     agent-browser screenshot result.png                     │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

---

## Part 7: 최종 통합 계획

### 7.1 전체 개선 항목 요약

| 영역 | 개선 항목 | 우선순위 | 예상 작업량 |
|------|----------|---------|------------|
| **nextjs-expert-agent** | REACT-PERF-RULES.md 추가 | HIGH | 2일 |
| | UI-GUIDELINES.md 추가 | HIGH | 1일 |
| | Performance 스킬 확장 | HIGH | 1일 |
| | agent-browser E2E 통합 | MEDIUM | 2일 |
| **flutter-to-nextjs-agent** | 변환 Best Practices | HIGH | 1일 |
| | 접근성 변환 규칙 | HIGH | 1일 |
| | 검증 체크리스트 확장 | MEDIUM | 1일 |
| **frontend-design-agent** | UI Guidelines 통합 | MEDIUM | 1일 |
| | Animation 규칙 확장 | MEDIUM | 1일 |

### 7.2 예상 효과

```
Before (현재)                      After (개선 후)
─────────────────────────────────────────────────────────────
성능 규칙: 1개 스킬 (CWV)     →    45개 규칙, 8개 카테고리
Impact 시스템: 없음           →    CRITICAL → LOW 5단계
UI 가이드라인: 기본           →    100+ 규칙 통합
코드 품질: 빌드 체크          →    Best Practices 자동 적용
E2E 테스트: Playwright MCP    →    agent-browser 옵션 추가
```

### 7.3 최종 구현 타임라인

```
┌─────────────────────────────────────────────────────────────┐
│                    Implementation Timeline                   │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  Week 1: Foundation                                          │
│  ├── Day 1-2: REACT-PERF-RULES.md 작성 (800줄)              │
│  ├── Day 3: UI-GUIDELINES.md 작성 (600줄)                   │
│  ├── Day 4: nextjs-expert 스킬 업데이트                     │
│  └── Day 5: Agent 정의 업데이트                             │
│                                                              │
│  Week 2: Enhancement                                         │
│  ├── Day 1-2: flutter-to-nextjs 변환 규칙 추가              │
│  ├── Day 3: frontend-design 가이드라인 확장                 │
│  ├── Day 4: agent-browser 통합                              │
│  └── Day 5: 문서화 및 CLAUDE.md 업데이트                    │
│                                                              │
│  Week 3: Testing & Polish                                    │
│  ├── Day 1-2: 통합 테스트                                   │
│  ├── Day 3: 버그 수정                                       │
│  └── Day 4-5: 최종 문서화                                   │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```
