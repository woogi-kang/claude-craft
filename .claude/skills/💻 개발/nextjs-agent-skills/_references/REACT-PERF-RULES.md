# React Performance Rules Reference

> Based on Vercel Engineering's React/Next.js performance best practices.
> 코드 생성 및 리뷰 시 이 규칙들을 자동으로 적용합니다.

---

## Impact Level System

| Level | Symbol | 의미 | 액션 |
|-------|--------|------|------|
| CRITICAL | 🔴 | 2-10x 성능 영향 | 반드시 적용 |
| HIGH | 🟠 | 현저한 성능 개선 | 강력 권고 |
| MEDIUM-HIGH | 🟡 | 의미있는 개선 | 권고 |
| MEDIUM | 🔵 | 점진적 개선 | 고려 |
| LOW-MEDIUM | ⚪ | 마이크로 최적화 | 핫패스만 |
| LOW | ⬜ | 특수 상황 | 필요시 |

---

## 1. Eliminating Waterfalls (Waterfall 제거)

### 1.1 async-parallel: Promise.all for Independent Operations

**Impact**: 🔴 CRITICAL (2-10x faster)

독립적인 비동기 작업을 순차적으로 await하면 불필요한 대기 시간이 발생합니다.

```typescript
// ❌ Bad: Sequential awaits create waterfall (3초 = 1초 + 1초 + 1초)
async function loadDashboard() {
  const user = await fetchUser()         // 1초
  const posts = await fetchPosts()       // 1초
  const comments = await fetchComments() // 1초
  return { user, posts, comments }
}

// ✅ Good: Parallel execution (1초 = max(1초, 1초, 1초))
async function loadDashboard() {
  const [user, posts, comments] = await Promise.all([
    fetchUser(),
    fetchPosts(),
    fetchComments()
  ])
  return { user, posts, comments }
}
```

**적용 기준:**
- 2개 이상의 독립적인 fetch/API 호출
- 서로 의존성이 없는 비동기 작업
- Server Component 내 데이터 로딩

---

### 1.2 async-suspense-boundaries: Strategic Suspense Placement

**Impact**: 🔴 CRITICAL (faster initial paint, better UX)

전체 페이지가 모든 데이터를 기다리지 않고, 준비된 부분부터 스트리밍됩니다.

```tsx
// ❌ Bad: Entire page waits for all data
async function Dashboard() {
  const stats = await getStats()
  const posts = await getPosts()
  const analytics = await getAnalytics()

  return (
    <div>
      <Header />
      <StatsCards stats={stats} />
      <PostList posts={posts} />
      <AnalyticsChart data={analytics} />
    </div>
  )
}

// ✅ Good: Static UI renders immediately, data streams when ready
function Dashboard() {
  return (
    <div>
      <Header />  {/* Renders immediately */}
      <Suspense fallback={<StatsSkeleton />}>
        <StatsSection />  {/* Streams when ready */}
      </Suspense>
      <Suspense fallback={<PostsSkeleton />}>
        <PostsSection />  {/* Streams independently */}
      </Suspense>
      <Suspense fallback={<AnalyticsSkeleton />}>
        <AnalyticsSection />  {/* Streams independently */}
      </Suspense>
    </div>
  )
}

// 각 섹션은 독립적인 async Server Component
async function StatsSection() {
  const stats = await getStats()
  return <StatsCards stats={stats} />
}
```

**Suspense 배치 원칙:**
- 정적 UI (헤더, 네비게이션)는 Suspense 바깥에
- 데이터 의존 컴포넌트만 Suspense로 감싸기
- 독립적인 데이터는 별도 Suspense 경계
- Skeleton은 실제 컴포넌트와 동일한 크기로

---

### 1.3 async-sibling-components: Component Composition for Parallelization

**Impact**: 🔴 CRITICAL (eliminates server-side waterfalls)

Server Component에서 형제 컴포넌트는 병렬로 fetch합니다.

```tsx
// ❌ Bad: Waterfall in parent component
async function UserPage() {
  const user = await getUser()  // 먼저 완료되어야
  const posts = await getUserPosts(user.id)  // 그 다음 실행

  return (
    <div>
      <UserProfile user={user} />
      <PostList posts={posts} />
    </div>
  )
}

// ✅ Good: Sibling components fetch in parallel
function UserPage() {
  return (
    <div>
      <Suspense fallback={<ProfileSkeleton />}>
        <UserProfile />  {/* Fetches user */}
      </Suspense>
      <Suspense fallback={<PostsSkeleton />}>
        <UserPosts />   {/* Fetches posts in parallel */}
      </Suspense>
    </div>
  )
}

async function UserProfile() {
  const user = await getUser()
  return <ProfileCard user={user} />
}

async function UserPosts() {
  const posts = await getPosts()
  return <PostList posts={posts} />
}
```

---

### 1.4 async-dependency-parallel: Optimize Dependent Data Fetching

**Impact**: 🟠 HIGH

의존성이 있는 데이터도 최대한 병렬화합니다.

```typescript
// ❌ Bad: Full waterfall
async function getPageData(userId: string) {
  const user = await getUser(userId)           // 1. 먼저
  const posts = await getUserPosts(user.id)    // 2. 의존
  const comments = await getPostComments(posts[0].id)  // 3. 의존
  return { user, posts, comments }
}

// ✅ Better: Partial parallelization where possible
async function getPageData(userId: string) {
  // userId만 알면 병렬 가능
  const [user, posts] = await Promise.all([
    getUser(userId),
    getUserPosts(userId)  // userId로 직접 쿼리 가능하게 API 설계
  ])

  // posts 결과 필요한 것만 순차
  const comments = await getPostComments(posts[0].id)
  return { user, posts, comments }
}
```

---

### 1.5 async-preload-data: Data Preloading Pattern

**Impact**: 🟠 HIGH

데이터 로딩을 최대한 일찍 시작합니다.

```typescript
// lib/preload.ts
import { cache } from 'react'

// 캐시된 데이터 로더
export const getUser = cache(async (id: string) => {
  return await db.user.findUnique({ where: { id } })
})

// 프리로드 함수 (Promise 반환, await하지 않음)
export const preloadUser = (id: string) => {
  void getUser(id)
}

// 사용처 - 레이아웃에서 일찍 시작
export default function Layout({ params }: { params: { id: string } }) {
  preloadUser(params.id)  // 여기서 시작
  return <div>{/* children */}</div>
}

// 실제 사용 컴포넌트 - 이미 로딩 중인 결과 사용
async function UserProfile({ id }: { id: string }) {
  const user = await getUser(id)  // 캐시된 결과 사용
  return <Profile user={user} />
}
```

---

## 2. Bundle Size Optimization (번들 최적화)

### 2.1 bundle-barrel-imports: Avoid Barrel Files

**Impact**: 🔴 CRITICAL (200-800ms savings, 15-70% faster dev boot)

Barrel file (index.ts에서 re-export)은 전체 모듈을 로드합니다.

```typescript
// ❌ Bad: Barrel import loads ALL icons (~10,000 modules)
import { Check, X, Menu } from 'lucide-react'

// ✅ Good: Direct imports load only what's needed
import Check from 'lucide-react/dist/esm/icons/check'
import X from 'lucide-react/dist/esm/icons/x'
import Menu from 'lucide-react/dist/esm/icons/menu'

// ✅ Better: Configure optimizePackageImports (Next.js 13.5+)
// next.config.ts
const nextConfig = {
  experimental: {
    optimizePackageImports: [
      'lucide-react',
      '@radix-ui/react-icons',
      'lodash',
      'date-fns',
      '@heroicons/react',
    ],
  },
}
```

**영향받는 주요 라이브러리:**
- `lucide-react` - 아이콘
- `@radix-ui/*` - UI 컴포넌트
- `lodash` - 유틸리티
- `date-fns` - 날짜
- `@heroicons/react` - 아이콘
- `react-icons` - 아이콘

---

### 2.2 bundle-dynamic-imports: Dynamic Import for Heavy Components

**Impact**: 🔴 CRITICAL (reduces initial bundle 30-70%)

무거운 컴포넌트는 필요할 때 로드합니다.

```typescript
// ❌ Bad: Heavy component in main bundle
import { MonacoEditor } from '@monaco-editor/react'  // ~300KB
import { Chart } from 'chart.js/auto'                 // ~200KB
import { PDFViewer } from '@react-pdf/renderer'       // ~500KB

// ✅ Good: Lazy load when needed
import dynamic from 'next/dynamic'

const MonacoEditor = dynamic(
  () => import('@monaco-editor/react'),
  {
    loading: () => <EditorSkeleton />,
    ssr: false,  // 클라이언트 전용
  }
)

const Chart = dynamic(
  () => import('chart.js/auto').then(mod => mod.Chart),
  { loading: () => <ChartSkeleton /> }
)

const PDFViewer = dynamic(
  () => import('@react-pdf/renderer').then(mod => mod.PDFViewer),
  { ssr: false }
)
```

**Dynamic Import 대상:**
- 에디터 (Monaco, CodeMirror)
- 차트 라이브러리
- PDF 뷰어/생성기
- 지도 컴포넌트
- 리치 텍스트 에디터
- 3D/Canvas 라이브러리
- 날짜 피커 (복잡한 경우)

---

### 2.3 bundle-preload-intent: Preload on User Intent

**Impact**: 🟠 HIGH (perceived performance improvement)

사용자 의도를 감지하여 미리 로드합니다.

```tsx
'use client'

import { useCallback } from 'react'
import Link from 'next/link'

export function NavigationItem({ href, children }) {
  const handleMouseEnter = useCallback(() => {
    // 호버 시 라우트 프리페치
    const link = document.createElement('link')
    link.rel = 'prefetch'
    link.href = href
    document.head.appendChild(link)
  }, [href])

  return (
    <Link
      href={href}
      onMouseEnter={handleMouseEnter}
      prefetch={false}  // 기본 프리페치 비활성화
    >
      {children}
    </Link>
  )
}

// 무거운 기능 프리로드
export function FeatureButton({ onClick }) {
  const handleMouseEnter = useCallback(() => {
    // 호버 시 컴포넌트 프리로드
    import('@/features/heavy-feature/components')
  }, [])

  return (
    <Button
      onMouseEnter={handleMouseEnter}
      onClick={onClick}
    >
      Open Feature
    </Button>
  )
}
```

---

### 2.4 bundle-tree-shaking: Ensure Tree-Shakeable Imports

**Impact**: 🟡 MEDIUM-HIGH

Tree shaking이 작동하는 import 패턴을 사용합니다.

```typescript
// ❌ Bad: Default export can't be tree-shaken well
import utils from '@/lib/utils'
utils.formatDate()

// ✅ Good: Named exports are tree-shakeable
import { formatDate } from '@/lib/utils'
formatDate()

// ❌ Bad: Import entire lodash
import _ from 'lodash'
_.debounce()

// ✅ Good: Import specific function
import debounce from 'lodash/debounce'
// 또는
import { debounce } from 'lodash-es'
```

---

### 2.5 bundle-code-splitting: Route-Based Code Splitting

**Impact**: 🟠 HIGH

App Router는 자동으로 라우트별 코드 스플리팅을 수행합니다.

```tsx
// Next.js App Router - 자동 코드 스플리팅
// app/dashboard/page.tsx - 별도 청크
// app/settings/page.tsx - 별도 청크

// 레이아웃 그룹으로 공유 코드 최소화
app/
├── (marketing)/        // 마케팅 페이지 그룹
│   ├── layout.tsx      // 마케팅 전용 레이아웃
│   ├── page.tsx
│   └── pricing/
├── (dashboard)/        // 대시보드 그룹
│   ├── layout.tsx      // 대시보드 전용 레이아웃
│   ├── page.tsx
│   └── settings/

// 공유 컴포넌트는 필요한 곳에서만
'use client'

// ❌ Bad: 모든 페이지에서 무거운 컴포넌트 import
import { HeavyChart } from '@/components/charts'

// ✅ Good: 필요한 페이지에서만 dynamic import
const HeavyChart = dynamic(() => import('@/components/charts/HeavyChart'))
```

---

## 3. Server-Side Performance (서버 성능)

### 3.1 server-cache-react: Per-Request Deduplication with React.cache()

**Impact**: 🟠 HIGH (eliminates redundant queries)

동일 요청 내 중복 데이터 호출을 제거합니다.

```typescript
import { cache } from 'react'
import { db } from '@/lib/db'

// ✅ cache()로 감싸서 요청 내 중복 제거
export const getCurrentUser = cache(async () => {
  const session = await auth()
  if (!session?.user?.id) return null
  return await db.user.findUnique({
    where: { id: session.user.id },
    include: { preferences: true }
  })
})

// 여러 컴포넌트에서 호출해도 1번만 실행
// Header.tsx
async function Header() {
  const user = await getCurrentUser()  // DB 쿼리 1회
  return <nav>{user?.name}</nav>
}

// Sidebar.tsx
async function Sidebar() {
  const user = await getCurrentUser()  // 캐시된 결과 반환
  return <aside>{user?.preferences}</aside>
}

// Dashboard.tsx
async function Dashboard() {
  const user = await getCurrentUser()  // 캐시된 결과 반환
  return <main>Welcome, {user?.name}</main>
}
```

**사용 시점:**
- 여러 Server Component에서 동일 데이터 필요
- 인증된 사용자 정보
- 공통 설정/환경 데이터

---

### 3.2 server-cache-lru: Cross-Request Caching

**Impact**: 🟠 HIGH

요청 간 데이터 캐싱으로 DB 부하를 줄입니다.

```typescript
import { unstable_cache } from 'next/cache'

// ✅ unstable_cache로 요청 간 캐싱
export const getProducts = unstable_cache(
  async (category: string) => {
    return await db.product.findMany({
      where: { category },
      orderBy: { createdAt: 'desc' }
    })
  },
  ['products'],  // 캐시 키
  {
    tags: ['products'],  // 재검증 태그
    revalidate: 60 * 5   // 5분 TTL
  }
)

// 재검증
import { revalidateTag } from 'next/cache'

export async function createProduct(data: ProductInput) {
  await db.product.create({ data })
  revalidateTag('products')  // 캐시 무효화
}
```

---

### 3.3 server-after: Non-Blocking Operations with after()

**Impact**: 🟠 HIGH (faster response times)

응답 후 실행할 작업을 분리합니다.

```typescript
import { after } from 'next/server'

export async function POST(request: Request) {
  const data = await request.json()

  // 핵심 작업 - 응답에 필요
  const result = await db.order.create({ data })

  // 부수 작업 - 응답 후 실행
  after(async () => {
    await sendOrderConfirmationEmail(result.id)
    await updateInventory(result.items)
    await notifyWarehouse(result.id)
    await trackAnalytics('order_created', result)
  })

  // 즉시 응답
  return Response.json(result)
}
```

**after() 사용 대상:**
- 이메일/알림 발송
- 로깅/분석
- 캐시 워밍
- 외부 서비스 동기화
- 비동기 웹훅 발송

---

### 3.4 server-serialization: Minimize RSC Boundary Data

**Impact**: 🟠 HIGH (reduces payload size)

Server → Client 경계에서 전달되는 데이터를 최소화합니다.

```tsx
// ❌ Bad: Pass entire object (불필요한 데이터 직렬화)
async function Page() {
  const user = await getUser()
  // { id, name, email, avatar, settings, metadata, ... } 전체 전달
  return <ClientComponent user={user} />
}

// ✅ Good: Pass only needed fields
async function Page() {
  const user = await getUser()
  return (
    <ClientComponent
      name={user.name}
      avatar={user.avatar}
    />
  )
}

// ✅ Better: 서버에서 가공하여 필요한 것만 전달
async function ProductPage({ id }: { id: string }) {
  const product = await getProduct(id)

  // 클라이언트에 필요한 최소 데이터만
  const clientData = {
    name: product.name,
    price: formatPrice(product.price),
    inStock: product.inventory > 0,
  }

  return <ProductClient data={clientData} />
}
```

---

### 3.5 server-streaming-order: Optimize Streaming Order

**Impact**: 🟡 MEDIUM-HIGH

중요한 콘텐츠가 먼저 스트리밍되도록 순서를 조정합니다.

```tsx
// ✅ 중요도 순으로 Suspense 배치
function ArticlePage() {
  return (
    <article>
      {/* 1. 핵심 콘텐츠 먼저 */}
      <Suspense fallback={<ArticleSkeleton />}>
        <ArticleContent />
      </Suspense>

      {/* 2. 부가 정보 */}
      <Suspense fallback={<AuthorSkeleton />}>
        <AuthorInfo />
      </Suspense>

      {/* 3. 덜 중요한 콘텐츠 */}
      <Suspense fallback={<CommentsSkeleton />}>
        <Comments />
      </Suspense>

      {/* 4. 추천 (가장 나중) */}
      <Suspense fallback={<RelatedSkeleton />}>
        <RelatedArticles />
      </Suspense>
    </article>
  )
}
```

---

## 4. Client-Side Data Fetching (클라이언트 데이터)

### 4.1 client-swr-deduplication: Automatic Request Deduplication

**Impact**: 🟡 MEDIUM-HIGH

SWR/TanStack Query로 자동 중복 요청 제거.

```typescript
// ✅ SWR - 자동 중복 제거
import useSWR from 'swr'

function UserAvatar() {
  // 동일 키로 여러 컴포넌트에서 호출해도 1번만 fetch
  const { data: user } = useSWR('/api/user', fetcher)
  return <Avatar src={user?.avatar} />
}

function UserName() {
  const { data: user } = useSWR('/api/user', fetcher)  // 캐시된 결과
  return <span>{user?.name}</span>
}

// ✅ TanStack Query - 동일한 동작
import { useQuery } from '@tanstack/react-query'

function UserAvatar() {
  const { data: user } = useQuery({
    queryKey: ['user'],
    queryFn: () => fetch('/api/user').then(r => r.json())
  })
  return <Avatar src={user?.avatar} />
}
```

---

### 4.2 client-swr-subscription: Real-Time Data with useSWRSubscription

**Impact**: 🔵 MEDIUM

실시간 데이터를 효율적으로 처리합니다.

```typescript
import useSWRSubscription from 'swr/subscription'

function LivePrice({ symbol }: { symbol: string }) {
  const { data: price } = useSWRSubscription(
    ['price', symbol],
    ([, symbol], { next }) => {
      const ws = new WebSocket(`wss://api.example.com/price/${symbol}`)

      ws.onmessage = (event) => {
        next(null, JSON.parse(event.data))
      }
      ws.onerror = (error) => next(error)

      return () => ws.close()
    }
  )

  return <span>${price?.toFixed(2)}</span>
}
```

---

## 5. Re-render Optimization (리렌더링 최적화)

### 5.1 rerender-memo: Extract to Memoized Components

**Impact**: 🔵 MEDIUM

비용이 높은 계산을 별도 컴포넌트로 분리합니다.

```tsx
// ❌ Bad: Expensive computation runs during loading state
function UserProfile({ userId }: { userId: string }) {
  const { data: user, isLoading } = useUser(userId)

  // 데이터 없어도 계산 실행됨
  const processedData = useMemo(() =>
    expensiveProcess(user), [user]
  )

  if (isLoading) return <Skeleton />
  return <Profile data={processedData} />
}

// ✅ Good: Extracted component with early return
function UserProfile({ userId }: { userId: string }) {
  const { data: user, isLoading } = useUser(userId)

  if (isLoading) return <Skeleton />
  return <UserProfileContent user={user} />  // 데이터 있을 때만 렌더
}

const UserProfileContent = memo(function UserProfileContent({
  user
}: {
  user: User
}) {
  // 이제 user가 확실히 존재할 때만 실행
  const processedData = useMemo(() =>
    expensiveProcess(user), [user]
  )
  return <Profile data={processedData} />
})
```

---

### 5.2 rerender-transitions: Non-Urgent Updates with startTransition

**Impact**: 🔵 MEDIUM (smoother UI)

긴급하지 않은 업데이트를 지연시켜 UI를 부드럽게 유지합니다.

```tsx
'use client'

import { useState, useTransition } from 'react'

function SearchResults() {
  const [query, setQuery] = useState('')
  const [results, setResults] = useState([])
  const [isPending, startTransition] = useTransition()

  const handleSearch = (e: React.ChangeEvent<HTMLInputElement>) => {
    const value = e.target.value
    setQuery(value)  // 긴급: 입력 필드 즉시 업데이트

    startTransition(() => {
      // 비긴급: 결과 업데이트는 지연 가능
      const filtered = filterItems(value)
      setResults(filtered)
    })
  }

  return (
    <div>
      <input value={query} onChange={handleSearch} />
      {isPending && <LoadingIndicator />}
      <ResultList results={results} />
    </div>
  )
}
```

**startTransition 사용 대상:**
- 검색 결과 필터링
- 탭 전환 콘텐츠
- 목록 정렬/필터
- 대량 UI 업데이트

---

### 5.3 rerender-functional-setstate: Functional State Updates

**Impact**: 🔵 MEDIUM

상태 업데이트 시 최신 값을 보장합니다.

```tsx
// ❌ Bad: Stale closure problem
function Counter() {
  const [count, setCount] = useState(0)

  const incrementTwice = () => {
    setCount(count + 1)  // count는 클로저 값
    setCount(count + 1)  // 같은 클로저 값 사용 → 1만 증가
  }
}

// ✅ Good: Functional update ensures latest value
function Counter() {
  const [count, setCount] = useState(0)

  const incrementTwice = () => {
    setCount(prev => prev + 1)  // 최신 값 사용
    setCount(prev => prev + 1)  // 최신 값 사용 → 2 증가
  }
}

// 복잡한 객체 상태도 동일
const [user, setUser] = useState({ name: '', age: 0 })

// ❌ Bad
setUser({ ...user, name: 'John' })

// ✅ Good
setUser(prev => ({ ...prev, name: 'John' }))
```

---

### 5.4 rerender-lazy-initial-state: Lazy State Initialization

**Impact**: ⚪ LOW-MEDIUM

비용이 높은 초기값 계산을 지연시킵니다.

```tsx
// ❌ Bad: Expensive computation on every render
function Editor() {
  // parseDocument가 매 렌더마다 실행됨
  const [content, setContent] = useState(parseDocument(rawContent))
}

// ✅ Good: Lazy initialization - 초기 렌더에만 실행
function Editor() {
  const [content, setContent] = useState(() => parseDocument(rawContent))
}

// localStorage 읽기도 동일
// ❌ Bad
const [theme, setTheme] = useState(
  typeof window !== 'undefined'
    ? localStorage.getItem('theme')
    : 'light'
)

// ✅ Good
const [theme, setTheme] = useState(() => {
  if (typeof window === 'undefined') return 'light'
  return localStorage.getItem('theme') || 'light'
})
```

---

### 5.5 rerender-avoid-inline-objects: Stable Object References

**Impact**: 🔵 MEDIUM

인라인 객체는 매 렌더마다 새 참조를 생성합니다.

```tsx
// ❌ Bad: New object every render → child re-renders
function Parent() {
  return (
    <Child
      style={{ padding: 16, margin: 8 }}  // 새 객체
      config={{ enabled: true }}           // 새 객체
    />
  )
}

// ✅ Good: Stable references
const CHILD_STYLE = { padding: 16, margin: 8 }
const CHILD_CONFIG = { enabled: true }

function Parent() {
  return <Child style={CHILD_STYLE} config={CHILD_CONFIG} />
}

// 동적 값이 필요한 경우
function Parent({ padding }) {
  const style = useMemo(() => ({ padding, margin: 8 }), [padding])
  return <Child style={style} />
}
```

---

### 5.6 rerender-callback-memoization: Stable Callback References

**Impact**: 🔵 MEDIUM

```tsx
// ❌ Bad: New function every render
function List({ items }) {
  return items.map(item => (
    <Item
      key={item.id}
      onClick={() => handleClick(item.id)}  // 새 함수
    />
  ))
}

// ✅ Good: useCallback for stable reference
function List({ items }) {
  const handleClick = useCallback((id: string) => {
    console.log('Clicked:', id)
  }, [])

  return items.map(item => (
    <Item
      key={item.id}
      onClick={handleClick}
      id={item.id}
    />
  ))
}

// 또는 Item 내부에서 처리
const Item = memo(function Item({ id, onClick }) {
  return <button onClick={() => onClick(id)}>...</button>
})
```

---

### 5.7 rerender-context-split: Split Context by Update Frequency

**Impact**: 🟡 MEDIUM-HIGH

업데이트 빈도가 다른 값은 Context를 분리합니다.

```tsx
// ❌ Bad: 모든 값이 같은 Context에
const AppContext = createContext({
  theme: 'light',      // 드물게 변경
  user: null,          // 드물게 변경
  notifications: [],   // 자주 변경
  unreadCount: 0       // 자주 변경
})

// ✅ Good: 업데이트 빈도별 분리
const ThemeContext = createContext({ theme: 'light' })
const UserContext = createContext({ user: null })
const NotificationContext = createContext({
  notifications: [],
  unreadCount: 0
})

// 자주 변경되는 값만 해당 Consumer 리렌더
function NotificationBadge() {
  const { unreadCount } = useContext(NotificationContext)
  return <Badge count={unreadCount} />
}
```

---

## 6. Rendering Performance (렌더링 성능)

### 6.1 rendering-content-visibility: Defer Off-Screen Content

**Impact**: 🟠 HIGH (10x faster initial render for long lists)

화면 밖 콘텐츠 렌더링을 지연시킵니다.

```css
/* 긴 리스트 아이템에 적용 */
.list-item {
  content-visibility: auto;
  contain-intrinsic-size: 0 80px;  /* 예상 높이 */
}

/* 카드 그리드 */
.card {
  content-visibility: auto;
  contain-intrinsic-size: 300px 200px;
}

/* 섹션 단위 */
.page-section {
  content-visibility: auto;
  contain-intrinsic-size: 0 500px;
}
```

```tsx
// Tailwind 커스텀 클래스
// tailwind.config.ts
module.exports = {
  theme: {
    extend: {
      // 커스텀 유틸리티
    }
  },
  plugins: [
    function({ addUtilities }) {
      addUtilities({
        '.content-auto': {
          'content-visibility': 'auto',
        },
        '.contain-intrinsic-80': {
          'contain-intrinsic-size': '0 80px',
        }
      })
    }
  ]
}

// 사용
function MessageList({ messages }) {
  return (
    <div className="overflow-y-auto h-screen">
      {messages.map(msg => (
        <div
          key={msg.id}
          className="content-auto contain-intrinsic-80"
        >
          <MessageItem message={msg} />
        </div>
      ))}
    </div>
  )
}
```

---

### 6.2 rendering-hoist-jsx: Static JSX Outside Components

**Impact**: 🔵 MEDIUM

정적 JSX를 컴포넌트 밖으로 호이스팅합니다.

```tsx
// ❌ Bad: Icon recreated every render
function Button({ children }) {
  return (
    <button className="flex items-center gap-2">
      <svg className="w-4 h-4">
        <path d="..." />
      </svg>
      {children}
    </button>
  )
}

// ✅ Good: Static JSX hoisted
const ArrowIcon = (
  <svg className="w-4 h-4" aria-hidden="true">
    <path d="..." />
  </svg>
)

function Button({ children }) {
  return (
    <button className="flex items-center gap-2">
      {ArrowIcon}
      {children}
    </button>
  )
}

// 조건부 정적 요소도 호이스팅
const LoadingSpinner = <Loader2 className="w-4 h-4 animate-spin" />
const CheckIcon = <Check className="w-4 h-4" />

function SubmitButton({ isLoading, isSuccess }) {
  return (
    <button>
      {isLoading ? LoadingSpinner : isSuccess ? CheckIcon : 'Submit'}
    </button>
  )
}
```

---

### 6.3 rendering-svg-precision: Optimize SVG Precision

**Impact**: ⚪ LOW-MEDIUM

SVG 경로 정밀도를 최적화합니다.

```tsx
// ❌ Bad: Excessive precision
<path d="M12.000000 4.000000 L20.000000 12.000000" />

// ✅ Good: Reasonable precision (2-3 decimal places)
<path d="M12 4 L20 12" />

// SVG 최적화 도구 사용
// SVGO, SVGOMG 등으로 자동 최적화
```

---

### 6.4 rendering-children-pattern: Children as Props

**Impact**: 🔵 MEDIUM

children을 props로 전달하면 불필요한 리렌더를 방지합니다.

```tsx
// ❌ Bad: 상태 변경 시 children도 리렌더
function Modal({ isOpen, children }) {
  const [position, setPosition] = useState({ x: 0, y: 0 })

  return (
    <div style={position}>
      {children}  {/* position 변경 시 리렌더 */}
    </div>
  )
}

// ✅ Good: children은 이미 생성된 요소로 전달
function Modal({ isOpen, children }) {
  const [position, setPosition] = useState({ x: 0, y: 0 })

  return (
    <ModalContainer style={position}>
      {children}  {/* 부모에서 생성되어 참조 유지 */}
    </ModalContainer>
  )
}

// 사용처
function Page() {
  return (
    <Modal>
      <ExpensiveComponent />  {/* Modal 상태 변경에 영향 없음 */}
    </Modal>
  )
}
```

---

### 6.5 rendering-key-stability: Stable Keys for Lists

**Impact**: 🔵 MEDIUM

리스트 key는 안정적인 식별자를 사용합니다.

```tsx
// ❌ Bad: Index as key - 순서 변경 시 문제
{items.map((item, index) => (
  <Item key={index} data={item} />
))}

// ❌ Bad: Random key - 매번 리렌더
{items.map(item => (
  <Item key={Math.random()} data={item} />
))}

// ✅ Good: Stable unique identifier
{items.map(item => (
  <Item key={item.id} data={item} />
))}

// ID가 없는 경우 - 고유 조합 생성
{items.map(item => (
  <Item key={`${item.type}-${item.name}`} data={item} />
))}
```

---

### 6.6 rendering-virtualization: Virtualize Long Lists

**Impact**: 🟠 HIGH (50+ items)

50개 이상의 아이템은 가상화합니다.

```tsx
import { useVirtualizer } from '@tanstack/react-virtual'

function VirtualList({ items }: { items: Item[] }) {
  const parentRef = useRef<HTMLDivElement>(null)

  const virtualizer = useVirtualizer({
    count: items.length,
    getScrollElement: () => parentRef.current,
    estimateSize: () => 50,  // 예상 아이템 높이
    overscan: 5,  // 버퍼 아이템 수
  })

  return (
    <div
      ref={parentRef}
      className="h-[400px] overflow-auto"
    >
      <div
        style={{
          height: `${virtualizer.getTotalSize()}px`,
          position: 'relative',
        }}
      >
        {virtualizer.getVirtualItems().map(virtualRow => (
          <div
            key={items[virtualRow.index].id}
            style={{
              position: 'absolute',
              top: 0,
              left: 0,
              width: '100%',
              height: `${virtualRow.size}px`,
              transform: `translateY(${virtualRow.start}px)`,
            }}
          >
            <ListItem item={items[virtualRow.index]} />
          </div>
        ))}
      </div>
    </div>
  )
}
```

---

### 6.7 rendering-hydration: Selective Hydration

**Impact**: 🔵 MEDIUM

인터랙션이 없는 부분은 hydration을 건너뜁니다.

```tsx
// 정적 콘텐츠 - 클라이언트 JS 불필요
function StaticContent() {
  return (
    <article>
      <h1>Article Title</h1>
      <p>Static content...</p>
    </article>
  )
}

// 인터랙티브 부분만 Client Component
function ArticlePage() {
  return (
    <div>
      <StaticContent />  {/* Server Component - no hydration */}
      <Suspense fallback={<CommentsSkeleton />}>
        <CommentsSection />  {/* Client Component - hydrated */}
      </Suspense>
    </div>
  )
}
```

---

## 7. JavaScript Performance (JS 성능)

### 7.1 js-set-map-lookups: O(1) Membership Checks

**Impact**: ⚪ LOW-MEDIUM (O(n) → O(1))

대용량 배열 검색은 Set/Map을 사용합니다.

```typescript
// ❌ Bad: O(n) lookup per item - 100,000 items × 1,000 checks
const allowedIds = ['id1', 'id2', ..., 'id1000']  // 1000개
items.filter(item => allowedIds.includes(item.id))  // O(n * m)

// ✅ Good: O(1) lookup - 훨씬 빠름
const allowedIdSet = new Set(allowedIds)  // O(n) 생성
items.filter(item => allowedIdSet.has(item.id))  // O(n)

// Map for key-value lookups
// ❌ Bad: 반복적인 find
const users = [{ id: '1', name: 'A' }, ...]
items.map(item => users.find(u => u.id === item.userId)?.name)

// ✅ Good: Map lookup
const userMap = new Map(users.map(u => [u.id, u]))
items.map(item => userMap.get(item.userId)?.name)
```

**Set/Map 사용 시점:**
- 배열 길이 > 10
- 반복적인 검색
- includes/find/indexOf가 루프 내에서 사용될 때

---

### 7.2 js-loop-optimization: Efficient Loop Patterns

**Impact**: ⚪ LOW-MEDIUM

루프 내 반복 계산을 최소화합니다.

```typescript
// ❌ Bad: .length 매번 계산 (대부분 최적화되지만 명시적이 좋음)
for (let i = 0; i < array.length; i++) {
  // ...
}

// ✅ Good: 캐시된 길이
for (let i = 0, len = array.length; i < len; i++) {
  // ...
}

// ❌ Bad: 루프 내 객체 생성
items.forEach(item => {
  const config = { setting: true }  // 매번 생성
  process(item, config)
})

// ✅ Good: 루프 밖에서 생성
const config = { setting: true }
items.forEach(item => {
  process(item, config)
})
```

---

### 7.3 js-string-concatenation: Efficient String Building

**Impact**: ⚪ LOW-MEDIUM

대량 문자열 연결은 배열 join을 사용합니다.

```typescript
// ❌ Bad: 반복적인 문자열 연결
let result = ''
for (const item of items) {
  result += item.name + ', '
}

// ✅ Good: Array join
const result = items.map(item => item.name).join(', ')

// ✅ Good: Template literal for known parts
const greeting = `Hello, ${firstName} ${lastName}!`
```

---

### 7.4 js-early-returns: Exit Early

**Impact**: ⚪ LOW-MEDIUM

가드 절로 일찍 반환합니다.

```typescript
// ❌ Bad: Nested conditions
function processUser(user: User | null) {
  if (user) {
    if (user.isActive) {
      if (user.hasPermission) {
        return doSomething(user)
      }
    }
  }
  return null
}

// ✅ Good: Early returns
function processUser(user: User | null) {
  if (!user) return null
  if (!user.isActive) return null
  if (!user.hasPermission) return null

  return doSomething(user)
}
```

---

### 7.5 js-optional-chaining: Safe Property Access

**Impact**: ⚪ LOW-MEDIUM

옵셔널 체이닝으로 안전하게 접근합니다.

```typescript
// ❌ Bad: Verbose null checks
const street = user && user.address && user.address.street

// ✅ Good: Optional chaining
const street = user?.address?.street

// ❌ Bad: 기본값 처리
const name = user && user.name ? user.name : 'Anonymous'

// ✅ Good: Nullish coalescing
const name = user?.name ?? 'Anonymous'
```

---

## 8. Advanced Patterns (고급 패턴)

### 8.1 advanced-use-effect-event: Stable Event Handlers

**Impact**: ⬜ LOW (specific use cases)

useEffectEvent로 최신 값을 참조하면서 안정적인 참조를 유지합니다.

```tsx
import { useEffectEvent } from 'react'

function Chat({ roomId, onMessage }) {
  // ✅ 최신 onMessage를 항상 참조하지만 Effect 의존성에 불필요
  const onMessageEvent = useEffectEvent((message) => {
    onMessage(message)
  })

  useEffect(() => {
    const connection = createConnection(roomId)
    connection.on('message', onMessageEvent)
    return () => connection.disconnect()
  }, [roomId])  // onMessage가 변경되어도 재연결 안 함
}
```

---

### 8.2 advanced-ref-stable-callback: Ref for Stable Callbacks

**Impact**: ⬜ LOW

ref를 사용하여 콜백의 안정적인 참조를 유지합니다.

```tsx
function useStableCallback<T extends (...args: any[]) => any>(callback: T) {
  const callbackRef = useRef(callback)

  useLayoutEffect(() => {
    callbackRef.current = callback
  })

  return useCallback((...args: Parameters<T>) => {
    return callbackRef.current(...args)
  }, []) as T
}

// 사용
function Component({ onSubmit }) {
  // onSubmit이 변경되어도 stableSubmit 참조는 유지
  const stableSubmit = useStableCallback(onSubmit)

  useEffect(() => {
    // Effect가 재실행되지 않음
    form.onSubmit(stableSubmit)
  }, [stableSubmit])
}
```

---

### 8.3 advanced-debounce-throttle: Rate Limiting Updates

**Impact**: 🔵 MEDIUM

빈번한 업데이트를 제한합니다.

```tsx
import { useDebouncedCallback } from 'use-debounce'

function SearchInput() {
  const [query, setQuery] = useState('')
  const [results, setResults] = useState([])

  // 300ms 디바운스 - 타이핑 중 검색 방지
  const debouncedSearch = useDebouncedCallback(async (term: string) => {
    const data = await searchAPI(term)
    setResults(data)
  }, 300)

  return (
    <div>
      <input
        value={query}
        onChange={(e) => {
          setQuery(e.target.value)
          debouncedSearch(e.target.value)
        }}
      />
      <Results data={results} />
    </div>
  )
}

// 스크롤 이벤트 쓰로틀
import { useThrottledCallback } from 'use-debounce'

function InfiniteList() {
  const throttledScroll = useThrottledCallback((e) => {
    // 100ms마다 최대 1번 실행
    checkLoadMore(e.target.scrollTop)
  }, 100)

  return <div onScroll={throttledScroll}>...</div>
}
```

---

## Quick Reference Checklist

### 🔴 CRITICAL (반드시 적용)

- [ ] 독립적인 비동기 작업 → `Promise.all()`
- [ ] 데이터 의존 컴포넌트만 → `<Suspense>`
- [ ] 서버 컴포넌트 형제 구성 → 병렬 fetch
- [ ] Barrel file import → `optimizePackageImports` 또는 직접 import
- [ ] 대용량 컴포넌트 → `dynamic(() => import())`

### 🟠 HIGH (강력 권고)

- [ ] 동일 요청 내 중복 호출 → `React.cache()`
- [ ] 요청 간 캐싱 → `unstable_cache()`
- [ ] RSC 경계 → 필요한 데이터만 전달
- [ ] 긴 리스트 → `content-visibility` 또는 가상화
- [ ] hover 시 → 다음 경로/컴포넌트 프리로드
- [ ] 응답 후 작업 → `after()`

### 🔵 MEDIUM (권고)

- [ ] 비용 높은 계산 → 메모된 별도 컴포넌트
- [ ] 빈번한 UI 업데이트 → `startTransition`
- [ ] 상태 업데이트 → functional updater `prev => ...`
- [ ] 정적 JSX → 컴포넌트 밖 호이스팅
- [ ] 인라인 객체/함수 → `useMemo`/`useCallback`
- [ ] Context → 업데이트 빈도별 분리

### ⚪ LOW-MEDIUM (핫패스에서 적용)

- [ ] 대용량 배열 검색 → `Set`/`Map`
- [ ] 루프 최적화 → 캐시된 길이, 밖에서 객체 생성
- [ ] 문자열 연결 → `array.join()`
- [ ] 비용 높은 초기값 → lazy initialization `() => ...`
