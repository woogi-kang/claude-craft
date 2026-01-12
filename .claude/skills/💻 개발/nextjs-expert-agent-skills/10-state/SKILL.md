# State Management Skill

Zustand를 사용하여 클라이언트 상태를 관리합니다.

## Triggers

- "상태 관리", "zustand", "store", "client state"

---

## Input

| 항목 | 필수 | 설명 |
|------|------|------|
| `storeName` | ✅ | 스토어 이름 |
| `state` | ✅ | 상태 정의 |

---

## 설치

```bash
npm install zustand
```

---

## 기본 Store 패턴

```typescript
// stores/app.store.ts
import { create } from 'zustand';
import { devtools, persist } from 'zustand/middleware';

interface AppState {
  sidebarOpen: boolean;
  theme: 'light' | 'dark' | 'system';
  toggleSidebar: () => void;
  setSidebarOpen: (open: boolean) => void;
  setTheme: (theme: 'light' | 'dark' | 'system') => void;
}

export const useAppStore = create<AppState>()(
  devtools(
    persist(
      (set) => ({
        sidebarOpen: true,
        theme: 'system',
        toggleSidebar: () => set((s) => ({ sidebarOpen: !s.sidebarOpen })),
        setSidebarOpen: (open) => set({ sidebarOpen: open }),
        setTheme: (theme) => set({ theme }),
      }),
      { name: 'app-storage', partialize: (s) => ({ theme: s.theme }) }
    ),
    { name: 'AppStore' }
  )
);
```

---

## Feature Store 패턴 (immer)

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
  totalItems: () => number;
  totalPrice: () => number;
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
        totalItems: () => get().items.reduce((sum, i) => sum + i.quantity, 0),
        totalPrice: () => get().items.reduce((sum, i) => sum + i.price * i.quantity, 0),
        addItem: (newItem) =>
          set((state) => {
            const existing = state.items.find((i) => i.id === newItem.id);
            if (existing) {
              existing.quantity += 1;
            } else {
              state.items.push({ ...newItem, quantity: 1 });
            }
          }),
        removeItem: (id) =>
          set((state) => {
            state.items = state.items.filter((i) => i.id !== id);
          }),
        updateQuantity: (id, quantity) =>
          set((state) => {
            const item = state.items.find((i) => i.id === id);
            if (item) item.quantity = Math.max(0, quantity);
          }),
        clearCart: () => set({ items: [] }),
      })),
      { name: 'cart-storage' }
    ),
    { name: 'CartStore' }
  )
);
```

---

## Selector 패턴

```typescript
// stores/selectors.ts
import { useAppStore } from './app.store';
import { useCartStore } from '@/features/cart/stores/cart.store';
import { shallow } from 'zustand/shallow';

export const useSidebarOpen = () => useAppStore((s) => s.sidebarOpen);
export const useTheme = () => useAppStore((s) => s.theme);

export const useCartSummary = () =>
  useCartStore(
    (s) => ({ totalItems: s.totalItems(), totalPrice: s.totalPrice() }),
    shallow
  );

export const useCartActions = () =>
  useCartStore(
    (s) => ({
      addItem: s.addItem,
      removeItem: s.removeItem,
      updateQuantity: s.updateQuantity,
      clearCart: s.clearCart,
    }),
    shallow
  );
```

---

## Modal Store

```typescript
// stores/modal.store.ts
import { create } from 'zustand';

type ModalType = 'confirm' | 'alert' | 'custom';

interface ModalState {
  isOpen: boolean;
  type: ModalType | null;
  data: unknown;
  open: (type: ModalType, data?: unknown) => void;
  close: () => void;
}

export const useModalStore = create<ModalState>((set) => ({
  isOpen: false,
  type: null,
  data: null,
  open: (type, data) => set({ isOpen: true, type, data }),
  close: () => set({ isOpen: false, type: null, data: null }),
}));
```

---

## 테스트 예제

### Store 유닛 테스트

```typescript
// stores/__tests__/cart.store.test.ts
import { describe, it, expect, beforeEach } from 'vitest';
import { useCartStore } from '../cart.store';

describe('Cart Store', () => {
  beforeEach(() => {
    // 각 테스트 전 스토어 리셋
    useCartStore.setState({ items: [] });
  });

  it('adds item to cart', () => {
    const { addItem } = useCartStore.getState();

    addItem({ id: '1', name: 'Product', price: 1000 });

    const { items } = useCartStore.getState();
    expect(items).toHaveLength(1);
    expect(items[0]).toEqual({ id: '1', name: 'Product', price: 1000, quantity: 1 });
  });

  it('increases quantity when adding existing item', () => {
    const { addItem } = useCartStore.getState();

    addItem({ id: '1', name: 'Product', price: 1000 });
    addItem({ id: '1', name: 'Product', price: 1000 });

    const { items } = useCartStore.getState();
    expect(items).toHaveLength(1);
    expect(items[0].quantity).toBe(2);
  });

  it('removes item from cart', () => {
    useCartStore.setState({
      items: [{ id: '1', name: 'Product', price: 1000, quantity: 1 }],
    });

    const { removeItem } = useCartStore.getState();
    removeItem('1');

    const { items } = useCartStore.getState();
    expect(items).toHaveLength(0);
  });

  it('calculates total correctly', () => {
    useCartStore.setState({
      items: [
        { id: '1', name: 'A', price: 1000, quantity: 2 },
        { id: '2', name: 'B', price: 500, quantity: 3 },
      ],
    });

    const { totalItems, totalPrice } = useCartStore.getState();
    expect(totalItems()).toBe(5);
    expect(totalPrice()).toBe(3500);
  });
});
```

### 컴포넌트와 Store 통합 테스트

```tsx
// components/__tests__/cart-summary.test.tsx
import { describe, it, expect, beforeEach } from 'vitest';
import { render, screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { useCartStore } from '@/stores/cart.store';
import { CartSummary } from '../cart-summary';

describe('CartSummary', () => {
  beforeEach(() => {
    useCartStore.setState({ items: [] });
  });

  it('displays cart total', () => {
    useCartStore.setState({
      items: [{ id: '1', name: 'Product', price: 1000, quantity: 2 }],
    });

    render(<CartSummary />);

    expect(screen.getByText(/2,000원/)).toBeInTheDocument();
  });

  it('clears cart on button click', async () => {
    useCartStore.setState({
      items: [{ id: '1', name: 'Product', price: 1000, quantity: 1 }],
    });

    render(<CartSummary />);
    await userEvent.click(screen.getByRole('button', { name: /비우기/ }));

    const { items } = useCartStore.getState();
    expect(items).toHaveLength(0);
  });
});
```

---

## 안티패턴 (❌ Bad → ✅ Good)

### 1. 불필요한 리렌더링

```typescript
// ❌ Bad: 전체 스토어 구독 (모든 변경에 리렌더링)
function Cart() {
  const store = useCartStore();  // 전체 구독!
  return <div>{store.items.length}</div>;
}

// ✅ Good: 필요한 상태만 구독
function Cart() {
  const itemCount = useCartStore((s) => s.items.length);
  return <div>{itemCount}</div>;
}
```

### 2. 객체/배열 셀렉터에서 shallow 누락

```typescript
// ❌ Bad: 매번 새 객체 생성 → 무한 리렌더링
function CartActions() {
  const { addItem, removeItem } = useCartStore((s) => ({
    addItem: s.addItem,
    removeItem: s.removeItem,
  }));  // 매 렌더마다 새 객체!
}

// ✅ Good: shallow 비교 사용
import { shallow } from 'zustand/shallow';

function CartActions() {
  const { addItem, removeItem } = useCartStore(
    (s) => ({ addItem: s.addItem, removeItem: s.removeItem }),
    shallow
  );
}
```

### 3. 서버 상태를 Zustand에 저장

```typescript
// ❌ Bad: API 응답을 Zustand에 저장
interface PostsState {
  posts: Post[];
  fetchPosts: () => Promise<void>;
  isLoading: boolean;
}

// ✅ Good: 서버 상태는 TanStack Query로
// Zustand는 UI 상태만 관리
interface UIState {
  sidebarOpen: boolean;
  selectedPostId: string | null;
}
```

### 4. persist 남용

```typescript
// ❌ Bad: 모든 상태 persist
persist(
  (set) => ({ ... }),
  { name: 'app-storage' }  // 전체 저장!
)

// ✅ Good: 필요한 상태만 persist
persist(
  (set) => ({ ... }),
  {
    name: 'app-storage',
    partialize: (state) => ({
      theme: state.theme,
      // isLoading 같은 임시 상태는 제외
    }),
  }
)
```

---

## 에러 처리

### 액션 에러 핸들링

```typescript
interface AppState {
  error: string | null;
  setError: (error: string | null) => void;
  clearError: () => void;
}

export const useAppStore = create<AppState>((set) => ({
  error: null,
  setError: (error) => set({ error }),
  clearError: () => set({ error: null }),
}));

// 사용
try {
  await riskyOperation();
} catch (error) {
  useAppStore.getState().setError(error.message);
}
```

---

## 성능 고려사항

### 액션과 상태 분리

```typescript
// 액션은 스토어 외부에서 가져오기 (리렌더링 안 함)
const addItem = useCartStore.getState().addItem;

// 또는 useCallback 대신 액션 셀렉터
const addItem = useCartStore((s) => s.addItem);
// 함수는 참조 안정적이라 리렌더링 안 함
```

### 선택적 구독

```typescript
// 특정 아이템만 구독
function CartItem({ id }: { id: string }) {
  const item = useCartStore((s) => s.items.find((i) => i.id === id));
  if (!item) return null;
  return <div>{item.name}</div>;
}
```

---

## 보안 고려사항

### 민감 데이터 persist 제외

```typescript
persist(
  (set) => ({ ... }),
  {
    name: 'user-storage',
    partialize: (state) => ({
      preferences: state.preferences,
      // 토큰, 비밀번호 등 제외!
      // token: state.token,
    }),
  }
)
```

### 로그아웃 시 스토어 초기화

```typescript
export const useAuthStore = create<AuthState>((set) => ({
  user: null,
  logout: () => {
    // 스토어 초기화
    set({ user: null });
    // localStorage 정리
    localStorage.removeItem('user-storage');
  },
}));
```

---

## References

- `_references/STATE-PATTERN.md` - TanStack Query + Zustand 패턴
- `_references/TEST-PATTERN.md` - 테스트 피라미드
