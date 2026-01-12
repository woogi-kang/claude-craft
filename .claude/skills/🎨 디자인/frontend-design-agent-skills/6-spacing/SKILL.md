# Spacing Skill

프로젝트의 레이아웃과 간격 시스템을 구성합니다.

## Triggers

- "간격", "스페이싱", "그리드", "spacing", "grid", "layout", "레이아웃", "여백"

---

## Input

| 항목 | 필수 | 설명 |
|------|------|------|
| `aestheticDirection` | ✅ | 디자인 방향 (minimal, bold, elegant 등) |
| `contentDensity` | ❌ | 콘텐츠 밀도 (compact, normal, spacious) - 기본값: normal |
| `breakpointStrategy` | ❌ | 반응형 전략 (mobile-first, desktop-first) - 기본값: mobile-first |

---

## Output

| 산출물 | 설명 |
|--------|------|
| `spacing-tokens.css` | CSS 변수로 정의된 스페이싱 토큰 |
| `layout-tokens.css` | 레이아웃 관련 CSS 변수 |
| `globals.css` 업데이트 | Tailwind @theme 통합 |

---

## Workflow

### Step 1: 4px 기반 그리드 시스템

**왜 4px인가?**

- 대부분의 디스플레이는 4의 배수로 잘 정렬됨
- 8px 기반보다 유연한 세밀한 조정 가능
- 4, 8, 12, 16, 20, 24... 자연스러운 증가

```css
/*
 * Base unit: 4px
 * Scale: 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 14, 16, 20, 24, ...
 * Value: 0, 4, 8, 12, 16, 20, 24, 28, 32, 36, 40, 44, 48, 56, 64, 80, 96px
 */
```

---

### Step 2: 스페이싱 토큰 정의

#### globals.css 스페이싱 섹션

```css
/* app/globals.css */
:root {
  /* =========================================
   * Spacing Scale (4px base)
   * ========================================= */

  /* Micro spacing */
  --spacing-0: 0px;
  --spacing-px: 1px;
  --spacing-0-5: 2px;   /* 0.5 * 4 */
  --spacing-1: 4px;
  --spacing-1-5: 6px;
  --spacing-2: 8px;
  --spacing-2-5: 10px;
  --spacing-3: 12px;
  --spacing-3-5: 14px;
  --spacing-4: 16px;

  /* Small spacing */
  --spacing-5: 20px;
  --spacing-6: 24px;
  --spacing-7: 28px;
  --spacing-8: 32px;

  /* Medium spacing */
  --spacing-9: 36px;
  --spacing-10: 40px;
  --spacing-11: 44px;
  --spacing-12: 48px;

  /* Large spacing */
  --spacing-14: 56px;
  --spacing-16: 64px;
  --spacing-20: 80px;
  --spacing-24: 96px;

  /* Extra large spacing */
  --spacing-28: 112px;
  --spacing-32: 128px;
  --spacing-36: 144px;
  --spacing-40: 160px;
  --spacing-44: 176px;
  --spacing-48: 192px;

  /* Huge spacing */
  --spacing-52: 208px;
  --spacing-56: 224px;
  --spacing-60: 240px;
  --spacing-64: 256px;
  --spacing-72: 288px;
  --spacing-80: 320px;
  --spacing-96: 384px;

  /* =========================================
   * Semantic Spacing Aliases
   * ========================================= */

  /* Component internal spacing */
  --space-xs: var(--spacing-1);    /* 4px - tight elements */
  --space-sm: var(--spacing-2);    /* 8px - related items */
  --space-md: var(--spacing-4);    /* 16px - standard gap */
  --space-lg: var(--spacing-6);    /* 24px - section padding */
  --space-xl: var(--spacing-8);    /* 32px - major sections */
  --space-2xl: var(--spacing-12);  /* 48px - page sections */
  --space-3xl: var(--spacing-16);  /* 64px - hero sections */

  /* Content density variants */
  --space-content-compact: var(--spacing-4);
  --space-content-normal: var(--spacing-6);
  --space-content-spacious: var(--spacing-8);
}
```

---

### Step 3: 레이아웃 토큰 정의

```css
/* app/globals.css - Layout tokens */
:root {
  /* =========================================
   * Container Widths
   * ========================================= */

  --container-xs: 320px;   /* Mobile small */
  --container-sm: 640px;   /* Mobile large */
  --container-md: 768px;   /* Tablet */
  --container-lg: 1024px;  /* Laptop */
  --container-xl: 1280px;  /* Desktop */
  --container-2xl: 1536px; /* Large desktop */

  /* Content width (readable prose) */
  --container-prose: 65ch;

  /* Maximum content width */
  --container-max: 1440px;

  /* =========================================
   * Fixed Layout Dimensions
   * ========================================= */

  /* Navigation */
  --header-height: 64px;
  --header-height-mobile: 56px;

  /* Sidebar */
  --sidebar-width: 280px;
  --sidebar-width-collapsed: 64px;
  --sidebar-width-mobile: 300px;

  /* Footer */
  --footer-height: 80px;

  /* Modal/Dialog */
  --modal-sm: 400px;
  --modal-md: 560px;
  --modal-lg: 720px;
  --modal-xl: 900px;
  --modal-full: calc(100vw - var(--spacing-8));

  /* =========================================
   * Breakpoints (for JS reference)
   * ========================================= */

  --breakpoint-sm: 640px;
  --breakpoint-md: 768px;
  --breakpoint-lg: 1024px;
  --breakpoint-xl: 1280px;
  --breakpoint-2xl: 1536px;

  /* =========================================
   * Z-Index Scale
   * ========================================= */

  --z-base: 0;
  --z-dropdown: 100;
  --z-sticky: 200;
  --z-fixed: 300;
  --z-overlay: 400;
  --z-modal: 500;
  --z-popover: 600;
  --z-tooltip: 700;
  --z-toast: 800;
  --z-max: 9999;
}
```

---

### Step 4: Tailwind v4 통합

```css
/* app/globals.css */
@theme inline {
  /* =========================================
   * Spacing Theme Integration
   * ========================================= */

  /* Direct spacing mapping */
  --spacing-0: 0px;
  --spacing-px: 1px;
  --spacing-0\.5: 2px;
  --spacing-1: 4px;
  --spacing-1\.5: 6px;
  --spacing-2: 8px;
  --spacing-2\.5: 10px;
  --spacing-3: 12px;
  --spacing-3\.5: 14px;
  --spacing-4: 16px;
  --spacing-5: 20px;
  --spacing-6: 24px;
  --spacing-7: 28px;
  --spacing-8: 32px;
  --spacing-9: 36px;
  --spacing-10: 40px;
  --spacing-11: 44px;
  --spacing-12: 48px;
  --spacing-14: 56px;
  --spacing-16: 64px;
  --spacing-20: 80px;
  --spacing-24: 96px;
  --spacing-28: 112px;
  --spacing-32: 128px;
  --spacing-36: 144px;
  --spacing-40: 160px;
  --spacing-44: 176px;
  --spacing-48: 192px;
  --spacing-52: 208px;
  --spacing-56: 224px;
  --spacing-60: 240px;
  --spacing-64: 256px;
  --spacing-72: 288px;
  --spacing-80: 320px;
  --spacing-96: 384px;

  /* =========================================
   * Container Theme Integration
   * ========================================= */

  --container-xs: 320px;
  --container-sm: 640px;
  --container-md: 768px;
  --container-lg: 1024px;
  --container-xl: 1280px;
  --container-2xl: 1536px;
  --container-prose: 65ch;
}

/* =========================================
 * Custom Container Component
 * ========================================= */

@layer components {
  .container-responsive {
    width: 100%;
    margin-inline: auto;
    padding-inline: var(--spacing-4);

    @media (min-width: 640px) {
      padding-inline: var(--spacing-6);
      max-width: var(--container-sm);
    }

    @media (min-width: 768px) {
      max-width: var(--container-md);
    }

    @media (min-width: 1024px) {
      padding-inline: var(--spacing-8);
      max-width: var(--container-lg);
    }

    @media (min-width: 1280px) {
      max-width: var(--container-xl);
    }

    @media (min-width: 1536px) {
      max-width: var(--container-2xl);
    }
  }
}
```

---

### Step 5: 그리드 시스템 구현

#### 12컬럼 그리드

```css
/* Grid system utilities */
@layer utilities {
  .grid-12 {
    display: grid;
    grid-template-columns: repeat(12, 1fr);
    gap: var(--spacing-4);
  }

  .grid-12-responsive {
    display: grid;
    gap: var(--spacing-4);
    grid-template-columns: repeat(4, 1fr);

    @media (min-width: 640px) {
      grid-template-columns: repeat(8, 1fr);
    }

    @media (min-width: 1024px) {
      grid-template-columns: repeat(12, 1fr);
    }
  }
}
```

#### 반응형 그리드 컴포넌트

```tsx
// components/atoms/grid.tsx
import { cn } from '@/lib/utils';
import { cva, type VariantProps } from 'class-variance-authority';

const gridVariants = cva('grid', {
  variants: {
    cols: {
      1: 'grid-cols-1',
      2: 'grid-cols-1 sm:grid-cols-2',
      3: 'grid-cols-1 sm:grid-cols-2 lg:grid-cols-3',
      4: 'grid-cols-1 sm:grid-cols-2 lg:grid-cols-4',
      6: 'grid-cols-2 sm:grid-cols-3 lg:grid-cols-6',
      12: 'grid-cols-4 sm:grid-cols-8 lg:grid-cols-12',
    },
    gap: {
      none: 'gap-0',
      xs: 'gap-1',      // 4px
      sm: 'gap-2',      // 8px
      md: 'gap-4',      // 16px
      lg: 'gap-6',      // 24px
      xl: 'gap-8',      // 32px
      '2xl': 'gap-12',  // 48px
    },
  },
  defaultVariants: {
    cols: 1,
    gap: 'md',
  },
});

interface GridProps
  extends React.HTMLAttributes<HTMLDivElement>,
    VariantProps<typeof gridVariants> {}

export function Grid({ className, cols, gap, ...props }: GridProps) {
  return (
    <div className={cn(gridVariants({ cols, gap }), className)} {...props} />
  );
}
```

#### Container 컴포넌트

```tsx
// components/atoms/container.tsx
import { cn } from '@/lib/utils';
import { cva, type VariantProps } from 'class-variance-authority';

const containerVariants = cva('mx-auto w-full', {
  variants: {
    size: {
      sm: 'max-w-screen-sm',     // 640px
      md: 'max-w-screen-md',     // 768px
      lg: 'max-w-screen-lg',     // 1024px
      xl: 'max-w-screen-xl',     // 1280px
      '2xl': 'max-w-screen-2xl', // 1536px
      full: 'max-w-full',
      prose: 'max-w-prose',      // 65ch
    },
    padding: {
      none: 'px-0',
      sm: 'px-4',
      md: 'px-4 sm:px-6 lg:px-8',
      lg: 'px-4 sm:px-8 lg:px-12',
    },
  },
  defaultVariants: {
    size: 'xl',
    padding: 'md',
  },
});

interface ContainerProps
  extends React.HTMLAttributes<HTMLDivElement>,
    VariantProps<typeof containerVariants> {
  as?: 'div' | 'section' | 'main' | 'article';
}

export function Container({
  className,
  size,
  padding,
  as: Component = 'div',
  ...props
}: ContainerProps) {
  return (
    <Component
      className={cn(containerVariants({ size, padding }), className)}
      {...props}
    />
  );
}
```

---

### Step 6: 콘텐츠 밀도별 설정

#### Compact (밀집형)

```css
/* Dashboard, Data-heavy UIs */
[data-density="compact"] {
  --space-xs: var(--spacing-0-5);  /* 2px */
  --space-sm: var(--spacing-1);    /* 4px */
  --space-md: var(--spacing-2);    /* 8px */
  --space-lg: var(--spacing-4);    /* 16px */
  --space-xl: var(--spacing-6);    /* 24px */
}
```

#### Normal (일반)

```css
/* Default for most UIs */
[data-density="normal"] {
  --space-xs: var(--spacing-1);    /* 4px */
  --space-sm: var(--spacing-2);    /* 8px */
  --space-md: var(--spacing-4);    /* 16px */
  --space-lg: var(--spacing-6);    /* 24px */
  --space-xl: var(--spacing-8);    /* 32px */
}
```

#### Spacious (여유형)

```css
/* Marketing, Landing pages */
[data-density="spacious"] {
  --space-xs: var(--spacing-2);    /* 8px */
  --space-sm: var(--spacing-4);    /* 16px */
  --space-md: var(--spacing-6);    /* 24px */
  --space-lg: var(--spacing-10);   /* 40px */
  --space-xl: var(--spacing-16);   /* 64px */
}
```

#### Density Provider

```tsx
// components/density-provider.tsx
'use client';

import { createContext, useContext, type ReactNode } from 'react';

type Density = 'compact' | 'normal' | 'spacious';

const DensityContext = createContext<Density>('normal');

export function useDensity() {
  return useContext(DensityContext);
}

interface DensityProviderProps {
  density: Density;
  children: ReactNode;
}

export function DensityProvider({ density, children }: DensityProviderProps) {
  return (
    <DensityContext.Provider value={density}>
      <div data-density={density}>
        {children}
      </div>
    </DensityContext.Provider>
  );
}
```

---

### Step 7: 반응형 스페이싱

#### Fluid Spacing

```css
/* Fluid spacing using clamp() */
:root {
  /* Section padding that scales with viewport */
  --section-padding-y: clamp(
    var(--spacing-8),   /* min: 32px */
    5vw,                /* preferred: 5% of viewport */
    var(--spacing-24)   /* max: 96px */
  );

  /* Hero section padding */
  --hero-padding-y: clamp(
    var(--spacing-16),  /* min: 64px */
    10vw,               /* preferred */
    var(--spacing-40)   /* max: 160px */
  );

  /* Card padding */
  --card-padding: clamp(
    var(--spacing-4),   /* min: 16px */
    2vw,                /* preferred */
    var(--spacing-8)    /* max: 32px */
  );
}
```

#### Responsive Section Component

```tsx
// components/atoms/section.tsx
import { cn } from '@/lib/utils';
import { cva, type VariantProps } from 'class-variance-authority';

const sectionVariants = cva('w-full', {
  variants: {
    spacing: {
      none: 'py-0',
      sm: 'py-8 sm:py-12',
      md: 'py-12 sm:py-16 lg:py-20',
      lg: 'py-16 sm:py-24 lg:py-32',
      xl: 'py-24 sm:py-32 lg:py-40',
      hero: 'py-20 sm:py-32 lg:py-48',
    },
    background: {
      default: 'bg-background',
      muted: 'bg-muted',
      primary: 'bg-primary text-primary-foreground',
      gradient: 'bg-gradient-to-br from-primary/5 to-accent/5',
    },
  },
  defaultVariants: {
    spacing: 'md',
    background: 'default',
  },
});

interface SectionProps
  extends React.HTMLAttributes<HTMLElement>,
    VariantProps<typeof sectionVariants> {}

export function Section({
  className,
  spacing,
  background,
  ...props
}: SectionProps) {
  return (
    <section
      className={cn(sectionVariants({ spacing, background }), className)}
      {...props}
    />
  );
}
```

---

## 테스트/검증

### 스페이싱 토큰 테스트

```typescript
// tests/spacing.test.ts
import { describe, it, expect } from 'vitest';

describe('Spacing Tokens', () => {
  it('follows 4px base grid', () => {
    const spacingValues = [
      { name: '--spacing-1', expected: '4px' },
      { name: '--spacing-2', expected: '8px' },
      { name: '--spacing-4', expected: '16px' },
      { name: '--spacing-8', expected: '32px' },
    ];

    const root = document.documentElement;
    const style = getComputedStyle(root);

    spacingValues.forEach(({ name, expected }) => {
      expect(style.getPropertyValue(name).trim()).toBe(expected);
    });
  });

  it('has all required layout tokens', () => {
    const root = document.documentElement;
    const style = getComputedStyle(root);

    const layoutTokens = [
      '--header-height',
      '--sidebar-width',
      '--container-max',
    ];

    layoutTokens.forEach((token) => {
      expect(style.getPropertyValue(token)).not.toBe('');
    });
  });
});
```

### Grid 컴포넌트 테스트

```tsx
// components/atoms/__tests__/grid.test.tsx
import { render, screen } from '@testing-library/react';
import { describe, it, expect } from 'vitest';
import { Grid } from '../grid';

describe('Grid', () => {
  it('renders with default props', () => {
    render(
      <Grid data-testid="grid">
        <div>Item 1</div>
        <div>Item 2</div>
      </Grid>
    );

    const grid = screen.getByTestId('grid');
    expect(grid).toHaveClass('grid');
    expect(grid).toHaveClass('gap-4');
  });

  it('applies correct column classes', () => {
    render(
      <Grid cols={3} data-testid="grid">
        <div>Item 1</div>
      </Grid>
    );

    const grid = screen.getByTestId('grid');
    expect(grid).toHaveClass('sm:grid-cols-2');
    expect(grid).toHaveClass('lg:grid-cols-3');
  });

  it('applies custom gap', () => {
    render(
      <Grid gap="xl" data-testid="grid">
        <div>Item</div>
      </Grid>
    );

    const grid = screen.getByTestId('grid');
    expect(grid).toHaveClass('gap-8');
  });
});
```

### Container 컴포넌트 테스트

```tsx
// components/atoms/__tests__/container.test.tsx
import { render, screen } from '@testing-library/react';
import { describe, it, expect } from 'vitest';
import { Container } from '../container';

describe('Container', () => {
  it('renders as div by default', () => {
    render(<Container data-testid="container">Content</Container>);

    const container = screen.getByTestId('container');
    expect(container.tagName).toBe('DIV');
  });

  it('renders as custom element', () => {
    render(
      <Container as="section" data-testid="container">
        Content
      </Container>
    );

    const container = screen.getByTestId('container');
    expect(container.tagName).toBe('SECTION');
  });

  it('applies size classes', () => {
    render(
      <Container size="lg" data-testid="container">
        Content
      </Container>
    );

    const container = screen.getByTestId('container');
    expect(container).toHaveClass('max-w-screen-lg');
  });
});
```

### Storybook 시각적 검증

```tsx
// stories/Spacing.stories.tsx
import type { Meta, StoryObj } from '@storybook/react';

const SpacingDemo = () => {
  const spacings = [1, 2, 3, 4, 5, 6, 7, 8, 10, 12, 16, 20, 24];

  return (
    <div className="space-y-4 p-6">
      <h2 className="text-xl font-semibold mb-6">Spacing Scale (4px base)</h2>
      {spacings.map((size) => (
        <div key={size} className="flex items-center gap-4">
          <span className="w-16 text-sm text-muted-foreground">
            spacing-{size}
          </span>
          <div
            className="bg-primary h-4"
            style={{ width: `${size * 4}px` }}
          />
          <span className="text-sm text-muted-foreground">
            {size * 4}px
          </span>
        </div>
      ))}
    </div>
  );
};

const meta: Meta = {
  title: 'Design System/Spacing',
};

export default meta;

export const Scale: StoryObj = {
  render: () => <SpacingDemo />,
};

export const GridExample: StoryObj = {
  render: () => (
    <div className="p-6">
      <h2 className="text-xl font-semibold mb-6">12-Column Grid</h2>
      <div className="grid grid-cols-12 gap-4">
        {Array.from({ length: 12 }).map((_, i) => (
          <div
            key={i}
            className="bg-primary/20 p-4 text-center text-sm rounded"
          >
            {i + 1}
          </div>
        ))}
      </div>
    </div>
  ),
};

export const DensityComparison: StoryObj = {
  render: () => (
    <div className="grid grid-cols-3 gap-8 p-6">
      <div data-density="compact" className="p-4 border rounded">
        <h3 className="font-semibold mb-2">Compact</h3>
        <div className="space-y-[var(--space-sm)]">
          <div className="bg-muted p-[var(--space-sm)] rounded">Item</div>
          <div className="bg-muted p-[var(--space-sm)] rounded">Item</div>
        </div>
      </div>

      <div data-density="normal" className="p-4 border rounded">
        <h3 className="font-semibold mb-2">Normal</h3>
        <div className="space-y-[var(--space-sm)]">
          <div className="bg-muted p-[var(--space-sm)] rounded">Item</div>
          <div className="bg-muted p-[var(--space-sm)] rounded">Item</div>
        </div>
      </div>

      <div data-density="spacious" className="p-4 border rounded">
        <h3 className="font-semibold mb-2">Spacious</h3>
        <div className="space-y-[var(--space-sm)]">
          <div className="bg-muted p-[var(--space-sm)] rounded">Item</div>
          <div className="bg-muted p-[var(--space-sm)] rounded">Item</div>
        </div>
      </div>
    </div>
  ),
};
```

---

## 안티패턴

### 1. 매직 넘버 사용

```tsx
// ❌ Bad: 하드코딩된 픽셀 값
<div className="p-[17px] mt-[23px] gap-[11px]">
  Content
</div>

// ✅ Good: 스페이싱 토큰 사용
<div className="p-4 mt-6 gap-3">
  Content
</div>
```

### 2. 일관성 없는 간격

```tsx
// ❌ Bad: 같은 맥락에서 다른 간격
<div>
  <Card className="mb-4" />
  <Card className="mb-6" />  {/* 왜 다를까? */}
  <Card className="mb-5" />  {/* 혼란스러움 */}
</div>

// ✅ Good: 일관된 간격
<div className="space-y-4">
  <Card />
  <Card />
  <Card />
</div>
```

### 3. 반응형 고려 없음

```tsx
// ❌ Bad: 고정 너비로 모바일에서 깨짐
<div className="w-[800px] p-16">
  Content that breaks on mobile
</div>

// ✅ Good: 반응형 레이아웃
<Container size="lg" padding="md">
  <div className="py-8 sm:py-12 lg:py-16">
    Content that adapts
  </div>
</Container>
```

### 4. 인라인 스페이싱 남용

```tsx
// ❌ Bad: 인라인 스타일로 간격 조정
<div style={{ marginTop: '24px', padding: '16px 32px' }}>
  Content
</div>

// ✅ Good: Tailwind 클래스 사용
<div className="mt-6 px-8 py-4">
  Content
</div>
```

### 5. 너무 많은 커스텀 간격

```css
/* ❌ Bad: 스케일에 없는 값 */
.custom-spacing {
  margin-top: 18px;
  padding: 22px 37px;
  gap: 13px;
}

/* ✅ Good: 스케일 내 값 사용 */
.consistent-spacing {
  margin-top: var(--spacing-5);   /* 20px */
  padding: var(--spacing-6) var(--spacing-10);  /* 24px 40px */
  gap: var(--spacing-3);  /* 12px */
}
```

---

## 성능 고려사항

### CSS 변수 성능

```css
/* CSS 변수는 성능에 미미한 영향
 * 하지만 calc() 중첩은 피하기 */

/* ❌ 피하기: 복잡한 calc 중첩 */
.complex {
  padding: calc(var(--spacing-4) + calc(var(--spacing-2) * 0.5));
}

/* ✅ 권장: 미리 계산된 값 */
.simple {
  padding: var(--spacing-5);  /* 20px */
}
```

### Layout Shift 방지

```tsx
// 고정 높이 요소로 CLS 방지
export function Header() {
  return (
    <header
      className="h-[var(--header-height)]"
      // 높이가 고정되어 레이아웃 시프트 방지
    >
      <nav>...</nav>
    </header>
  );
}
```

---

## 보안 고려사항

### 사용자 입력 간격 제한

```typescript
// 사용자가 간격을 조정할 수 있는 경우 검증
const ALLOWED_SPACING = ['sm', 'md', 'lg', 'xl'] as const;
type Spacing = typeof ALLOWED_SPACING[number];

function validateSpacing(input: string): Spacing {
  if (ALLOWED_SPACING.includes(input as Spacing)) {
    return input as Spacing;
  }
  return 'md'; // 기본값
}
```

---

## References

- `4-typography/` - 타이포그래피 시스템 (연계)
- `5-color/` - 색상 시스템 (연계)
- `7-motion/` - 모션 시스템 (연계)
- `17-responsive/` - 반응형 디자인 (후속 스킬)
