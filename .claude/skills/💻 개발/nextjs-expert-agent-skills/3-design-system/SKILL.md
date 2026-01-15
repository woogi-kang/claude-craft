# Design System Skill

shadcn/ui + Tailwind CSS v4 기반 디자인 시스템을 구성합니다.

> **Reference**: `_references/UI-GUIDELINES.md` - UI 접근성 및 성능 가이드라인 참조

## Triggers

- "디자인 시스템", "design system", "shadcn", "ui 설정"

---

## Input

| 항목 | 필수 | 설명 |
|------|------|------|
| `projectPath` | ✅ | Next.js 프로젝트 경로 |
| `theme` | ❌ | 테마 스타일 (default, new-york) |
| `baseColor` | ❌ | 기본 색상 (zinc, slate, gray 등) |

---

## 설정

### shadcn/ui 초기화

```bash
npx shadcn@latest init -d

# 또는 대화형 설정
npx shadcn@latest init
```

### components.json

```json
{
  "$schema": "https://ui.shadcn.com/schema.json",
  "style": "new-york",
  "rsc": true,
  "tsx": true,
  "tailwind": {
    "config": "",
    "css": "src/app/globals.css",
    "baseColor": "zinc",
    "cssVariables": true,
    "prefix": ""
  },
  "aliases": {
    "components": "@/components",
    "utils": "@/lib/utils",
    "ui": "@/components/ui",
    "lib": "@/lib",
    "hooks": "@/hooks"
  },
  "iconLibrary": "lucide"
}
```

---

## 디렉토리 구조

```
src/components/
├── ui/                        # shadcn/ui 컴포넌트
│   ├── button.tsx
│   ├── card.tsx
│   ├── input.tsx
│   ├── label.tsx
│   ├── form.tsx
│   └── ...
│
├── atoms/                     # 커스텀 Atoms
│   ├── loading-spinner.tsx
│   ├── badge-status.tsx
│   └── logo.tsx
│
├── molecules/                 # 조합 컴포넌트
│   ├── search-bar.tsx
│   ├── form-field.tsx
│   ├── user-avatar.tsx
│   ├── nav-link.tsx
│   └── theme-toggle.tsx
│
├── organisms/                 # 복합 컴포넌트
│   ├── header.tsx
│   ├── sidebar.tsx
│   ├── footer.tsx
│   └── data-table/
│       ├── data-table.tsx
│       ├── columns.tsx
│       └── toolbar.tsx
│
└── templates/                 # 레이아웃 템플릿
    ├── dashboard-layout.tsx
    ├── auth-layout.tsx
    └── marketing-layout.tsx
```

---

## globals.css (Tailwind v4)

```css
@import "tailwindcss";
@import "tw-animate-css";

@custom-variant dark (&:is(.dark *));

:root {
  /* Core Colors */
  --background: oklch(1 0 0);
  --foreground: oklch(0.145 0 0);
  --card: oklch(1 0 0);
  --card-foreground: oklch(0.145 0 0);
  --popover: oklch(1 0 0);
  --popover-foreground: oklch(0.145 0 0);
  --primary: oklch(0.205 0 0);
  --primary-foreground: oklch(0.985 0 0);
  --secondary: oklch(0.97 0 0);
  --secondary-foreground: oklch(0.205 0 0);
  --muted: oklch(0.97 0 0);
  --muted-foreground: oklch(0.556 0 0);
  --accent: oklch(0.97 0 0);
  --accent-foreground: oklch(0.205 0 0);
  --destructive: oklch(0.577 0.245 27.325);
  --destructive-foreground: oklch(0.985 0 0);
  --border: oklch(0.922 0 0);
  --input: oklch(0.922 0 0);
  --ring: oklch(0.708 0 0);

  /* Custom Semantic Colors */
  --success: oklch(0.76 0.18 145);
  --success-foreground: oklch(0.20 0.05 145);
  --warning: oklch(0.84 0.16 84);
  --warning-foreground: oklch(0.28 0.07 46);
  --info: oklch(0.70 0.15 250);
  --info-foreground: oklch(0.20 0.05 250);

  /* Layout */
  --radius: 0.625rem;
  --sidebar-width: 280px;
  --header-height: 64px;
}

.dark {
  --background: oklch(0.145 0 0);
  --foreground: oklch(0.985 0 0);
  --card: oklch(0.145 0 0);
  --card-foreground: oklch(0.985 0 0);
  --popover: oklch(0.145 0 0);
  --popover-foreground: oklch(0.985 0 0);
  --primary: oklch(0.985 0 0);
  --primary-foreground: oklch(0.205 0 0);
  --secondary: oklch(0.269 0 0);
  --secondary-foreground: oklch(0.985 0 0);
  --muted: oklch(0.269 0 0);
  --muted-foreground: oklch(0.708 0 0);
  --accent: oklch(0.269 0 0);
  --accent-foreground: oklch(0.985 0 0);
  --destructive: oklch(0.396 0.141 25.723);
  --destructive-foreground: oklch(0.985 0 0);
  --border: oklch(0.269 0 0);
  --input: oklch(0.269 0 0);
  --ring: oklch(0.439 0 0);

  /* Custom Semantic Colors - Dark */
  --success: oklch(0.45 0.12 145);
  --success-foreground: oklch(0.95 0.03 145);
  --warning: oklch(0.41 0.11 46);
  --warning-foreground: oklch(0.99 0.02 95);
  --info: oklch(0.45 0.12 250);
  --info-foreground: oklch(0.95 0.03 250);
}

@theme inline {
  --color-background: var(--background);
  --color-foreground: var(--foreground);
  --color-card: var(--card);
  --color-card-foreground: var(--card-foreground);
  --color-popover: var(--popover);
  --color-popover-foreground: var(--popover-foreground);
  --color-primary: var(--primary);
  --color-primary-foreground: var(--primary-foreground);
  --color-secondary: var(--secondary);
  --color-secondary-foreground: var(--secondary-foreground);
  --color-muted: var(--muted);
  --color-muted-foreground: var(--muted-foreground);
  --color-accent: var(--accent);
  --color-accent-foreground: var(--accent-foreground);
  --color-destructive: var(--destructive);
  --color-destructive-foreground: var(--destructive-foreground);
  --color-success: var(--success);
  --color-success-foreground: var(--success-foreground);
  --color-warning: var(--warning);
  --color-warning-foreground: var(--warning-foreground);
  --color-info: var(--info);
  --color-info-foreground: var(--info-foreground);
  --color-border: var(--border);
  --color-input: var(--input);
  --color-ring: var(--ring);
  --radius-sm: calc(var(--radius) - 4px);
  --radius-md: calc(var(--radius) - 2px);
  --radius-lg: var(--radius);
  --radius-xl: calc(var(--radius) + 4px);
}

@layer base {
  * {
    @apply border-border;
  }
  body {
    @apply bg-background text-foreground;
  }
}
```

---

## Dark Mode 설정

### Theme Provider

```bash
npm install next-themes
```

```tsx
// components/theme-provider.tsx
'use client';

import { ThemeProvider as NextThemesProvider } from 'next-themes';

export function ThemeProvider({
  children,
  ...props
}: React.ComponentProps<typeof NextThemesProvider>) {
  return <NextThemesProvider {...props}>{children}</NextThemesProvider>;
}
```

### Layout 적용

```tsx
// app/layout.tsx
import { ThemeProvider } from '@/components/theme-provider';

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="ko" suppressHydrationWarning>
      <body>
        <ThemeProvider
          attribute="class"
          defaultTheme="system"
          enableSystem
          disableTransitionOnChange
        >
          {children}
        </ThemeProvider>
      </body>
    </html>
  );
}
```

### Theme Toggle

```tsx
// components/molecules/theme-toggle.tsx
'use client';

import { useTheme } from 'next-themes';
import { Button } from '@/components/ui/button';
import { Moon, Sun } from 'lucide-react';

export function ThemeToggle() {
  const { setTheme, theme } = useTheme();

  return (
    <Button
      variant="ghost"
      size="icon"
      onClick={() => setTheme(theme === 'light' ? 'dark' : 'light')}
    >
      <Sun className="h-5 w-5 rotate-0 scale-100 transition-all dark:-rotate-90 dark:scale-0" />
      <Moon className="absolute h-5 w-5 rotate-90 scale-0 transition-all dark:rotate-0 dark:scale-100" />
      <span className="sr-only">테마 변경</span>
    </Button>
  );
}
```

---

## 컴포넌트 추가

```bash
# 기본 컴포넌트
npx shadcn@latest add button card input label form

# 폼 관련
npx shadcn@latest add checkbox radio-group select switch textarea

# 레이아웃
npx shadcn@latest add separator scroll-area sheet dialog

# 네비게이션
npx shadcn@latest add tabs navigation-menu dropdown-menu

# 피드백
npx shadcn@latest add alert badge progress skeleton tooltip

# 데이터
npx shadcn@latest add table avatar calendar

# 전체 추가
npx shadcn@latest add --all
```

---

## 테스트 예제

### 컴포넌트 Unit Test

```typescript
// components/ui/__tests__/button.test.tsx
import { render, screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { Button } from '../button';

describe('Button', () => {
  it('renders children correctly', () => {
    render(<Button>Click me</Button>);
    expect(screen.getByRole('button', { name: /click me/i })).toBeInTheDocument();
  });

  it('applies variant classes', () => {
    render(<Button variant="destructive">Delete</Button>);
    const button = screen.getByRole('button');
    expect(button).toHaveClass('bg-destructive');
  });

  it('handles click events', async () => {
    const handleClick = vi.fn();
    render(<Button onClick={handleClick}>Click</Button>);

    await userEvent.click(screen.getByRole('button'));
    expect(handleClick).toHaveBeenCalledTimes(1);
  });

  it('is disabled when disabled prop is true', () => {
    render(<Button disabled>Disabled</Button>);
    expect(screen.getByRole('button')).toBeDisabled();
  });

  it('renders as child component with asChild', () => {
    render(
      <Button asChild>
        <a href="/link">Link Button</a>
      </Button>
    );
    expect(screen.getByRole('link')).toHaveAttribute('href', '/link');
  });
});
```

### 접근성 테스트

```typescript
// components/ui/__tests__/accessibility.test.tsx
import { render } from '@testing-library/react';
import { axe, toHaveNoViolations } from 'jest-axe';
import { Button } from '../button';
import { Input } from '../input';
import { Label } from '../label';

expect.extend(toHaveNoViolations);

describe('Accessibility', () => {
  it('Button has no accessibility violations', async () => {
    const { container } = render(<Button>Click me</Button>);
    const results = await axe(container);
    expect(results).toHaveNoViolations();
  });

  it('Form field has no accessibility violations', async () => {
    const { container } = render(
      <div>
        <Label htmlFor="email">Email</Label>
        <Input id="email" type="email" placeholder="email@example.com" />
      </div>
    );
    const results = await axe(container);
    expect(results).toHaveNoViolations();
  });

  it('Button with icon has accessible name', async () => {
    const { container } = render(
      <Button aria-label="Close dialog">
        <svg aria-hidden="true" />
      </Button>
    );
    const results = await axe(container);
    expect(results).toHaveNoViolations();
  });
});
```

### 다크모드 테스트

```typescript
// components/__tests__/theme-toggle.test.tsx
import { render, screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { ThemeProvider } from 'next-themes';
import { ThemeToggle } from '../molecules/theme-toggle';

const wrapper = ({ children }: { children: React.ReactNode }) => (
  <ThemeProvider attribute="class" defaultTheme="light">
    {children}
  </ThemeProvider>
);

describe('ThemeToggle', () => {
  it('toggles between light and dark mode', async () => {
    render(<ThemeToggle />, { wrapper });

    const button = screen.getByRole('button', { name: /테마 변경/i });
    await userEvent.click(button);

    // Theme should toggle (실제 테스트에서는 next-themes mock 필요)
    expect(button).toBeInTheDocument();
  });
});
```

---

## 안티패턴

### 1. 색상 직접 사용 vs 디자인 토큰

```typescript
// ❌ Bad: Tailwind 색상 직접 사용
<div className="bg-blue-500 text-white border-gray-200">
  <p className="text-red-600">Error message</p>
</div>

// ✅ Good: 디자인 토큰 사용
<div className="bg-primary text-primary-foreground border-border">
  <p className="text-destructive">Error message</p>
</div>
```

### 2. 하드코딩 vs 시맨틱 변수

```css
/* ❌ Bad: 하드코딩된 값 */
.card {
  border-radius: 8px;
  padding: 16px;
  background: #ffffff;
}

/* ✅ Good: CSS 변수 사용 */
.card {
  border-radius: var(--radius-lg);
  padding: theme(spacing.4);
  background: hsl(var(--card));
}
```

### 3. 인라인 스타일 vs 컴포넌트 variants

```tsx
// ❌ Bad: 인라인으로 스타일 변형
<Button className="bg-red-500 hover:bg-red-600 text-white">
  Delete
</Button>

// ✅ Good: variant 시스템 사용
<Button variant="destructive">
  Delete
</Button>
```

### 4. 중복 클래스 vs cn() 유틸리티

```tsx
// ❌ Bad: className 덮어쓰기 충돌
<Button className="bg-primary px-8 py-4">  {/* 기본 padding과 충돌 */}
  Large Button
</Button>

// ✅ Good: cn()으로 안전하게 병합
import { cn } from '@/lib/utils';

<Button className={cn('px-8 py-4')}>
  Large Button
</Button>
```

### 5. 접근성 무시 vs 접근성 준수

```tsx
// ❌ Bad: 접근성 무시
<button onClick={handleClick}>
  <svg viewBox="0 0 24 24" />  {/* 레이블 없음 */}
</button>

// ✅ Good: 접근성 준수
<Button onClick={handleClick} aria-label="설정 열기">
  <svg viewBox="0 0 24 24" aria-hidden="true" />
</Button>

// 또는 sr-only 사용
<Button onClick={handleClick}>
  <svg viewBox="0 0 24 24" aria-hidden="true" />
  <span className="sr-only">설정 열기</span>
</Button>
```

---

## 에러 처리

### 테마 로딩 깜빡임 방지

```tsx
// app/layout.tsx
export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="ko" suppressHydrationWarning>
      <head>
        {/* 깜빡임 방지 스크립트 */}
        <script
          dangerouslySetInnerHTML={{
            __html: `
              try {
                const theme = localStorage.getItem('theme');
                if (theme === 'dark' || (!theme && window.matchMedia('(prefers-color-scheme: dark)').matches)) {
                  document.documentElement.classList.add('dark');
                }
              } catch {}
            `,
          }}
        />
      </head>
      <body>
        <ThemeProvider attribute="class" defaultTheme="system" enableSystem>
          {children}
        </ThemeProvider>
      </body>
    </html>
  );
}
```

### CSS 변수 폴백

```css
/* 변수가 정의되지 않은 경우 폴백 값 제공 */
.component {
  background: var(--custom-bg, var(--background));
  color: var(--custom-text, var(--foreground));
  border-radius: var(--radius, 0.5rem);
}
```

### 컴포넌트 로딩 에러

```tsx
// components/ui/error-boundary.tsx
'use client';

import { Component, type ReactNode } from 'react';
import { Button } from './button';
import { AlertTriangle } from 'lucide-react';

interface Props {
  children: ReactNode;
  fallback?: ReactNode;
}

interface State {
  hasError: boolean;
}

export class ComponentErrorBoundary extends Component<Props, State> {
  constructor(props: Props) {
    super(props);
    this.state = { hasError: false };
  }

  static getDerivedStateFromError(): State {
    return { hasError: true };
  }

  render() {
    if (this.state.hasError) {
      return this.props.fallback || (
        <div className="flex flex-col items-center justify-center p-6 text-center">
          <AlertTriangle className="h-8 w-8 text-destructive mb-2" />
          <p className="text-sm text-muted-foreground">컴포넌트를 불러올 수 없습니다</p>
          <Button
            variant="outline"
            size="sm"
            className="mt-2"
            onClick={() => this.setState({ hasError: false })}
          >
            다시 시도
          </Button>
        </div>
      );
    }

    return this.props.children;
  }
}
```

---

## 성능 고려사항

### 1. CSS 번들 최적화

```typescript
// next.config.ts
import type { NextConfig } from 'next';

const nextConfig: NextConfig = {
  experimental: {
    optimizeCss: true,  // CSS 최적화 (실험적)
  },
};

export default nextConfig;
```

### 2. 컴포넌트 지연 로딩

```tsx
// 무거운 컴포넌트는 dynamic import
import dynamic from 'next/dynamic';

const DataTable = dynamic(
  () => import('@/components/organisms/data-table/data-table'),
  {
    loading: () => <TableSkeleton />,
    ssr: false,  // 클라이언트 전용
  }
);

const Calendar = dynamic(
  () => import('@/components/ui/calendar').then((mod) => mod.Calendar),
  {
    loading: () => <div className="h-[300px] animate-pulse bg-muted rounded-md" />,
  }
);
```

---

## 접근성 체크리스트 (UI-GUIDELINES.md 기반)

### 🔴 Critical (반드시 적용)

```tsx
// 1. 아이콘 버튼에 aria-label 필수
// ❌ Bad
<button onClick={handleClose}>
  <X className="h-4 w-4" />
</button>

// ✅ Good
<button onClick={handleClose} aria-label="닫기">
  <X className="h-4 w-4" aria-hidden="true" />
</button>

// 2. Semantic HTML 사용
// ❌ Bad
<div onClick={handleClick} className="cursor-pointer">Click</div>

// ✅ Good
<button onClick={handleClick}>Click</button>

// 3. Form input에 label 연결
// ❌ Bad
<input type="email" placeholder="이메일" />

// ✅ Good
<label htmlFor="email">이메일</label>
<input id="email" type="email" autoComplete="email" />
```

### 🟠 High (강력 권고)

```tsx
// 1. focus-visible 스타일 (outline-none 대체)
// ❌ Bad
<button className="outline-none">Click</button>

// ✅ Good
<button className="outline-none focus-visible:ring-2 focus-visible:ring-ring">
  Click
</button>

// 2. 에러 메시지 연결
<input
  id="email"
  aria-invalid={!!error}
  aria-describedby={error ? 'email-error' : undefined}
/>
{error && (
  <span id="email-error" role="alert" className="text-destructive">
    {error}
  </span>
)}

// 3. 모션 감도 존중
import { useReducedMotion } from 'framer-motion'

function AnimatedComponent() {
  const shouldReduce = useReducedMotion()
  return (
    <motion.div
      animate={{ scale: shouldReduce ? 1 : 1.1 }}
      transition={{ duration: shouldReduce ? 0 : 0.2 }}
    />
  )
}
```

### 폼 필수 속성

| 필드 유형 | type | autocomplete |
|----------|------|--------------|
| 이메일 | `email` | `email` |
| 비밀번호 (현재) | `password` | `current-password` |
| 비밀번호 (새) | `password` | `new-password` |
| 이름 | `text` | `name` |
| 전화번호 | `tel` | `tel` |
| 주소 | `text` | `street-address` |

### Anti-Patterns 체크리스트

모든 컴포넌트 생성 시 다음을 검출하고 수정합니다:

- [ ] `outline-none` without `focus-visible` replacement
- [ ] `div` with `onClick` but no `role`/`tabIndex`
- [ ] Icon button without `aria-label`
- [ ] Form input without `label`
- [ ] Form input without `autocomplete`
- [ ] `transition: all` - 특정 속성만 지정
- [ ] Animation without `prefers-reduced-motion` check
- [ ] Paste blocked on inputs

---

## 보안 고려사항

### XSS 방지

```tsx
// ❌ 위험: dangerouslySetInnerHTML 사용
<div dangerouslySetInnerHTML={{ __html: userContent }} />

// ✅ 안전: DOMPurify로 sanitize
import DOMPurify from 'isomorphic-dompurify';

<div dangerouslySetInnerHTML={{ __html: DOMPurify.sanitize(userContent) }} />

// ✅ 더 안전: React 기본 렌더링 사용
<p>{userContent}</p>  {/* 자동으로 escape됨 */}
```

### 민감 정보 노출 방지

```tsx
// components/ui/input.tsx
interface InputProps extends React.ComponentProps<'input'> {
  // 비밀번호 입력 시 자동완성 속성
}

export function PasswordInput(props: InputProps) {
  return (
    <Input
      type="password"
      autoComplete="current-password"  // 또는 "new-password"
      {...props}
    />
  );
}
```

---

## References

- `_references/UI-GUIDELINES.md` - **UI 접근성 및 성능 가이드라인**
- `_references/COMPONENT-PATTERN.md`
- `_references/TEST-PATTERN.md`
- `_references/ARCHITECTURE-PATTERN.md`
- 관련 스킬: `21-integration-test`, `23-visual-test`
