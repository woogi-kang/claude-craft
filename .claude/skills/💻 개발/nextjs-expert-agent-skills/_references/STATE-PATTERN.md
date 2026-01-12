# State Management Pattern Reference

TanStack Query + Zustand 상태관리 패턴 및 샘플 코드 레퍼런스입니다.

## 상태 분리 원칙

```
┌─────────────────────────────────────────────────────────────┐
│                    State Management                          │
├─────────────────────────────────────────────────────────────┤
│  Server State (Async)     │  Client State (Sync)            │
│  ─────────────────────    │  ────────────────────           │
│  TanStack Query           │  Zustand                        │
│  • API 데이터             │  • UI 상태 (모달, 사이드바)      │
│  • 캐싱, 동기화           │  • 폼 상태                       │
│  • 백그라운드 리프레시    │  • 사용자 선호도                 │
├─────────────────────────────────────────────────────────────┤
│  URL State                                                   │
│  ─────────────────────                                      │
│  nuqs                                                        │
│  • 필터, 정렬, 페이지네이션                                  │
│  • 공유 가능한 상태                                          │
└─────────────────────────────────────────────────────────────┘
```

---

## TanStack Query 패턴

### Provider 설정

```tsx
// app/providers.tsx
'use client';

import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { ReactQueryDevtools } from '@tanstack/react-query-devtools';
import { useState } from 'react';

export function Providers({ children }: { children: React.ReactNode }) {
  const [queryClient] = useState(
    () =>
      new QueryClient({
        defaultOptions: {
          queries: {
            staleTime: 60 * 1000, // 1분
            gcTime: 5 * 60 * 1000, // 5분
            retry: 1,
            refetchOnWindowFocus: false,
          },
          mutations: {
            retry: 0,
          },
        },
      })
  );

  return (
    <QueryClientProvider client={queryClient}>
      {children}
      <ReactQueryDevtools initialIsOpen={false} />
    </QueryClientProvider>
  );
}
```

### Query Key Factory

```typescript
// features/users/hooks/user-keys.ts
export const userKeys = {
  all: ['users'] as const,
  lists: () => [...userKeys.all, 'list'] as const,
  list: (filters: Record<string, unknown>) => [...userKeys.lists(), filters] as const,
  details: () => [...userKeys.all, 'detail'] as const,
  detail: (id: string) => [...userKeys.details(), id] as const,
};

// 사용 예시
// userKeys.all          → ['users']
// userKeys.lists()      → ['users', 'list']
// userKeys.list({page:1}) → ['users', 'list', {page: 1}]
// userKeys.detail('1')  → ['users', 'detail', '1']
```

### Query Hook 패턴

```typescript
// features/users/hooks/use-users.ts
'use client';

import { useQuery, useSuspenseQuery } from '@tanstack/react-query';
import { userKeys } from './user-keys';

// 기본 Query
export function useUsers(options?: { enabled?: boolean }) {
  return useQuery({
    queryKey: userKeys.lists(),
    queryFn: async () => {
      const res = await fetch('/api/users');
      if (!res.ok) throw new Error('Failed to fetch users');
      return res.json();
    },
    ...options,
  });
}

// Suspense Query (React Suspense와 함께 사용)
export function useUsersSuspense() {
  return useSuspenseQuery({
    queryKey: userKeys.lists(),
    queryFn: async () => {
      const res = await fetch('/api/users');
      if (!res.ok) throw new Error('Failed to fetch users');
      return res.json();
    },
  });
}

// 단일 아이템 Query
export function useUser(id: string) {
  return useQuery({
    queryKey: userKeys.detail(id),
    queryFn: async () => {
      const res = await fetch(`/api/users/${id}`);
      if (!res.ok) throw new Error('Failed to fetch user');
      return res.json();
    },
    enabled: !!id,
  });
}

// 필터링된 Query
export function useFilteredUsers(filters: { search?: string; role?: string }) {
  return useQuery({
    queryKey: userKeys.list(filters),
    queryFn: async () => {
      const params = new URLSearchParams();
      if (filters.search) params.set('search', filters.search);
      if (filters.role) params.set('role', filters.role);

      const res = await fetch(`/api/users?${params}`);
      if (!res.ok) throw new Error('Failed to fetch users');
      return res.json();
    },
  });
}
```

### Mutation Hook 패턴

```typescript
// features/users/hooks/use-user-mutations.ts
'use client';

import { useMutation, useQueryClient } from '@tanstack/react-query';
import { userKeys } from './user-keys';
import { createUserAction, updateUserAction, deleteUserAction } from '../actions/user.action';
import { toast } from 'sonner';

// Create Mutation
export function useCreateUser() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: createUserAction,
    onSuccess: (data) => {
      queryClient.invalidateQueries({ queryKey: userKeys.lists() });
      toast.success('사용자가 생성되었습니다');
    },
    onError: (error) => {
      toast.error(error.message || '사용자 생성에 실패했습니다');
    },
  });
}

// Update Mutation with Optimistic Update
export function useUpdateUser() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: updateUserAction,
    onMutate: async ({ id, data }) => {
      // 진행 중인 쿼리 취소
      await queryClient.cancelQueries({ queryKey: userKeys.detail(id) });

      // 이전 값 스냅샷
      const previousUser = queryClient.getQueryData(userKeys.detail(id));

      // Optimistic update
      queryClient.setQueryData(userKeys.detail(id), (old: any) => ({
        ...old,
        ...data,
      }));

      return { previousUser };
    },
    onError: (err, { id }, context) => {
      // 에러 시 롤백
      if (context?.previousUser) {
        queryClient.setQueryData(userKeys.detail(id), context.previousUser);
      }
      toast.error('업데이트에 실패했습니다');
    },
    onSuccess: (_, { id }) => {
      queryClient.invalidateQueries({ queryKey: userKeys.detail(id) });
      queryClient.invalidateQueries({ queryKey: userKeys.lists() });
      toast.success('사용자 정보가 업데이트되었습니다');
    },
  });
}

// Delete Mutation
export function useDeleteUser() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: deleteUserAction,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: userKeys.lists() });
      toast.success('사용자가 삭제되었습니다');
    },
    onError: () => {
      toast.error('삭제에 실패했습니다');
    },
  });
}
```

### Infinite Query (무한 스크롤)

```typescript
// features/posts/hooks/use-infinite-posts.ts
'use client';

import { useInfiniteQuery } from '@tanstack/react-query';

interface PostsResponse {
  data: Post[];
  nextCursor: string | null;
}

export function useInfinitePosts() {
  return useInfiniteQuery({
    queryKey: ['posts', 'infinite'],
    queryFn: async ({ pageParam }) => {
      const params = new URLSearchParams();
      if (pageParam) params.set('cursor', pageParam);

      const res = await fetch(`/api/posts?${params}`);
      return res.json() as Promise<PostsResponse>;
    },
    initialPageParam: null as string | null,
    getNextPageParam: (lastPage) => lastPage.nextCursor,
  });
}

// 사용 예시
function PostsList() {
  const {
    data,
    fetchNextPage,
    hasNextPage,
    isFetchingNextPage,
  } = useInfinitePosts();

  const allPosts = data?.pages.flatMap((page) => page.data) ?? [];

  return (
    <div>
      {allPosts.map((post) => (
        <PostCard key={post.id} post={post} />
      ))}
      {hasNextPage && (
        <Button
          onClick={() => fetchNextPage()}
          disabled={isFetchingNextPage}
        >
          {isFetchingNextPage ? '로딩 중...' : '더 보기'}
        </Button>
      )}
    </div>
  );
}
```

---

## Zustand 패턴

### 기본 Store

```typescript
// stores/app.store.ts
import { create } from 'zustand';
import { devtools, persist } from 'zustand/middleware';

interface AppState {
  // State
  sidebarOpen: boolean;
  theme: 'light' | 'dark' | 'system';

  // Actions
  toggleSidebar: () => void;
  setSidebarOpen: (open: boolean) => void;
  setTheme: (theme: 'light' | 'dark' | 'system') => void;
}

export const useAppStore = create<AppState>()(
  devtools(
    persist(
      (set) => ({
        // Initial State
        sidebarOpen: true,
        theme: 'system',

        // Actions
        toggleSidebar: () =>
          set((state) => ({ sidebarOpen: !state.sidebarOpen })),
        setSidebarOpen: (open) => set({ sidebarOpen: open }),
        setTheme: (theme) => set({ theme }),
      }),
      {
        name: 'app-storage',
        partialize: (state) => ({ theme: state.theme }), // 일부만 persist
      }
    ),
    { name: 'AppStore' }
  )
);
```

### Feature Store (Slice 패턴)

```typescript
// features/cart/stores/cart.store.ts
import { create } from 'zustand';
import { devtools, persist } from 'zustand/middleware';
import { immer } from 'zustand/middleware/immer';

interface CartItem {
  id: string;
  name: string;
  price: number;
  quantity: number;
}

interface CartState {
  items: CartItem[];

  // Computed
  totalItems: () => number;
  totalPrice: () => number;

  // Actions
  addItem: (item: Omit<CartItem, 'quantity'>) => void;
  removeItem: (id: string) => void;
  updateQuantity: (id: string, quantity: number) => void;
  clearCart: () => void;
}

export const useCartStore = create<CartState>()(
  devtools(
    persist(
      immer((set, get) => ({
        items: [],

        // Computed (함수로 구현)
        totalItems: () =>
          get().items.reduce((sum, item) => sum + item.quantity, 0),
        totalPrice: () =>
          get().items.reduce((sum, item) => sum + item.price * item.quantity, 0),

        // Actions (immer로 불변성 자동 처리)
        addItem: (newItem) =>
          set((state) => {
            const existing = state.items.find((item) => item.id === newItem.id);
            if (existing) {
              existing.quantity += 1;
            } else {
              state.items.push({ ...newItem, quantity: 1 });
            }
          }),

        removeItem: (id) =>
          set((state) => {
            state.items = state.items.filter((item) => item.id !== id);
          }),

        updateQuantity: (id, quantity) =>
          set((state) => {
            const item = state.items.find((item) => item.id === id);
            if (item) {
              item.quantity = Math.max(0, quantity);
              if (item.quantity === 0) {
                state.items = state.items.filter((i) => i.id !== id);
              }
            }
          }),

        clearCart: () => set({ items: [] }),
      })),
      { name: 'cart-storage' }
    ),
    { name: 'CartStore' }
  )
);
```

### Selector 패턴

```typescript
// stores/selectors.ts
import { useAppStore } from './app.store';
import { useCartStore } from '@/features/cart/stores/cart.store';
import { useShallow } from 'zustand/react/shallow';

// 단일 값 선택
export const useSidebarOpen = () => useAppStore((state) => state.sidebarOpen);
export const useTheme = () => useAppStore((state) => state.theme);

// 여러 값 선택 (useShallow로 불필요한 리렌더링 방지)
// 주의: useShallow는 selector 함수를 감싸서 사용
export const useCartSummary = () =>
  useCartStore(
    useShallow((state) => ({
      totalItems: state.totalItems(),
      totalPrice: state.totalPrice(),
    }))
  );

// Actions만 선택 (리렌더링 없음)
export const useCartActions = () =>
  useCartStore(
    useShallow((state) => ({
      addItem: state.addItem,
      removeItem: state.removeItem,
      updateQuantity: state.updateQuantity,
      clearCart: state.clearCart,
    }))
  );

// 참고: Zustand v5+ 에서 shallow import 변경
// v4: import { shallow } from 'zustand/shallow' (deprecated)
// v5: import { useShallow } from 'zustand/react/shallow'
```

---

## nuqs (URL State) 패턴

### 설정

```tsx
// app/layout.tsx
import { NuqsAdapter } from 'nuqs/adapters/next/app';

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html>
      <body>
        <NuqsAdapter>{children}</NuqsAdapter>
      </body>
    </html>
  );
}
```

### 기본 사용

```typescript
// features/products/hooks/use-product-filters.ts
'use client';

import { useQueryState, parseAsString, parseAsInteger } from 'nuqs';

export function useProductFilters() {
  const [search, setSearch] = useQueryState('q', parseAsString.withDefault(''));
  const [page, setPage] = useQueryState('page', parseAsInteger.withDefault(1));
  const [sort, setSort] = useQueryState('sort', parseAsString.withDefault('created_at'));
  const [order, setOrder] = useQueryState('order', parseAsString.withDefault('desc'));

  return {
    search,
    setSearch,
    page,
    setPage,
    sort,
    setSort,
    order,
    setOrder,
  };
}
```

### 복잡한 필터 (다중 상태)

```typescript
// features/products/hooks/use-product-filters.ts
'use client';

import { useQueryStates, parseAsString, parseAsInteger, parseAsArrayOf } from 'nuqs';

export function useProductFilters() {
  const [filters, setFilters] = useQueryStates({
    q: parseAsString.withDefault(''),
    page: parseAsInteger.withDefault(1),
    limit: parseAsInteger.withDefault(20),
    sort: parseAsString.withDefault('created_at'),
    order: parseAsString.withDefault('desc'),
    categories: parseAsArrayOf(parseAsString).withDefault([]),
    minPrice: parseAsInteger,
    maxPrice: parseAsInteger,
  });

  const resetFilters = () => {
    setFilters({
      q: '',
      page: 1,
      categories: [],
      minPrice: null,
      maxPrice: null,
    });
  };

  return { filters, setFilters, resetFilters };
}
```

### TanStack Query와 통합

```typescript
// features/products/hooks/use-products.ts
'use client';

import { useQuery } from '@tanstack/react-query';
import { useProductFilters } from './use-product-filters';

export function useProducts() {
  const { filters } = useProductFilters();

  return useQuery({
    queryKey: ['products', filters],
    queryFn: async () => {
      const params = new URLSearchParams();

      if (filters.q) params.set('q', filters.q);
      params.set('page', String(filters.page));
      params.set('limit', String(filters.limit));
      params.set('sort', filters.sort);
      params.set('order', filters.order);
      filters.categories.forEach((c) => params.append('category', c));
      if (filters.minPrice) params.set('minPrice', String(filters.minPrice));
      if (filters.maxPrice) params.set('maxPrice', String(filters.maxPrice));

      const res = await fetch(`/api/products?${params}`);
      return res.json();
    },
  });
}
```

---

## 조합 패턴

### Query + Store 조합

```typescript
// features/notifications/hooks/use-notifications.ts
'use client';

import { useQuery } from '@tanstack/react-query';
import { create } from 'zustand';

// Zustand: 읽음 상태 (클라이언트 상태)
interface NotificationUIState {
  readIds: Set<string>;
  markAsRead: (id: string) => void;
  isRead: (id: string) => boolean;
}

const useNotificationUIStore = create<NotificationUIState>((set, get) => ({
  readIds: new Set(),
  markAsRead: (id) =>
    set((state) => ({
      readIds: new Set([...state.readIds, id]),
    })),
  isRead: (id) => get().readIds.has(id),
}));

// TanStack Query: 알림 목록 (서버 상태)
export function useNotifications() {
  const query = useQuery({
    queryKey: ['notifications'],
    queryFn: () => fetch('/api/notifications').then((res) => res.json()),
  });

  const { readIds, markAsRead, isRead } = useNotificationUIStore();

  // 읽지 않은 알림 수 계산
  const unreadCount =
    query.data?.filter((n: { id: string }) => !readIds.has(n.id)).length ?? 0;

  return {
    ...query,
    unreadCount,
    markAsRead,
    isRead,
  };
}
```
