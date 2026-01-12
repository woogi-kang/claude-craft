# Primitives Skill

Primitive UI 컴포넌트 (Atoms) 설계 및 구현 스킬입니다.
shadcn/ui 기반으로 커스터마이징된 기본 빌딩 블록을 제공합니다.

## Triggers

- "프리미티브", "기본 컴포넌트", "atoms", "primitives"
- "버튼 디자인", "인풋 디자인", "뱃지", "칩"
- "로딩 스피너", "스켈레톤"

---

## Input

| 항목 | 필수 | 설명 |
|------|------|------|
| `componentType` | ✅ | 컴포넌트 유형 (button, input, badge, chip, icon-button, loading) |
| `variant` | ❌ | 변형 스타일 (primary, secondary, ghost 등) |
| `size` | ❌ | 크기 (sm, md, lg) |
| `aesthetic` | ❌ | 미학적 방향 (minimal, playful, corporate, luxury) |

---

## cn() 유틸리티

모든 컴포넌트는 `cn()` 유틸리티로 클래스를 병합합니다.

```typescript
// lib/utils.ts
import { type ClassValue, clsx } from 'clsx';
import { twMerge } from 'tailwind-merge';

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs));
}
```

---

## Button Variants

### 기본 Button 확장

```tsx
// components/ui/button.tsx
import * as React from 'react';
import { Slot } from '@radix-ui/react-slot';
import { cva, type VariantProps } from 'class-variance-authority';
import { cn } from '@/lib/utils';

const buttonVariants = cva(
  // Base styles
  'inline-flex items-center justify-center gap-2 whitespace-nowrap rounded-md text-sm font-medium transition-all duration-200 disabled:pointer-events-none disabled:opacity-50 [&_svg]:pointer-events-none [&_svg]:size-4 [&_svg]:shrink-0',
  {
    variants: {
      variant: {
        default:
          'bg-primary text-primary-foreground shadow-sm hover:bg-primary/90 active:scale-[0.98]',
        secondary:
          'bg-secondary text-secondary-foreground shadow-sm hover:bg-secondary/80 active:scale-[0.98]',
        destructive:
          'bg-destructive text-destructive-foreground shadow-sm hover:bg-destructive/90 active:scale-[0.98]',
        outline:
          'border border-input bg-background shadow-sm hover:bg-accent hover:text-accent-foreground',
        ghost:
          'hover:bg-accent hover:text-accent-foreground',
        link:
          'text-primary underline-offset-4 hover:underline',
        // 추가 variants
        success:
          'bg-success text-success-foreground shadow-sm hover:bg-success/90 active:scale-[0.98]',
        warning:
          'bg-warning text-warning-foreground shadow-sm hover:bg-warning/90 active:scale-[0.98]',
        gradient:
          'bg-gradient-to-r from-primary to-primary/70 text-primary-foreground shadow-sm hover:opacity-90 active:scale-[0.98]',
      },
      size: {
        default: 'h-9 px-4 py-2',
        sm: 'h-8 rounded-md px-3 text-xs',
        lg: 'h-10 rounded-md px-6 text-base',
        xl: 'h-12 rounded-lg px-8 text-lg',
        icon: 'h-9 w-9',
      },
    },
    defaultVariants: {
      variant: 'default',
      size: 'default',
    },
  }
);

export interface ButtonProps
  extends React.ButtonHTMLAttributes<HTMLButtonElement>,
    VariantProps<typeof buttonVariants> {
  asChild?: boolean;
  loading?: boolean;
}

const Button = React.forwardRef<HTMLButtonElement, ButtonProps>(
  ({ className, variant, size, asChild = false, loading, children, disabled, ...props }, ref) => {
    const Comp = asChild ? Slot : 'button';
    return (
      <Comp
        className={cn(buttonVariants({ variant, size, className }))}
        ref={ref}
        disabled={disabled || loading}
        {...props}
      >
        {loading ? (
          <>
            <svg
              className="animate-spin -ml-1 h-4 w-4"
              xmlns="http://www.w3.org/2000/svg"
              fill="none"
              viewBox="0 0 24 24"
              aria-hidden="true"
            >
              <circle
                className="opacity-25"
                cx="12"
                cy="12"
                r="10"
                stroke="currentColor"
                strokeWidth="4"
              />
              <path
                className="opacity-75"
                fill="currentColor"
                d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
              />
            </svg>
            <span>처리 중...</span>
          </>
        ) : (
          children
        )}
      </Comp>
    );
  }
);
Button.displayName = 'Button';

export { Button, buttonVariants };
```

### 미학적 방향별 Button

```tsx
// Minimal 스타일
<Button className="rounded-none border-b-2 border-primary bg-transparent text-primary hover:bg-primary/5">
  Minimal Button
</Button>

// Playful 스타일
<Button className="rounded-full bg-gradient-to-r from-pink-500 to-violet-500 px-6 shadow-lg shadow-pink-500/30 hover:shadow-xl hover:shadow-pink-500/40">
  Playful Button
</Button>

// Corporate 스타일
<Button className="rounded-sm bg-slate-900 font-semibold tracking-wide text-white hover:bg-slate-800">
  Corporate Button
</Button>

// Luxury 스타일
<Button className="rounded-none border border-amber-600 bg-transparent px-8 font-light tracking-[0.2em] text-amber-600 hover:bg-amber-600 hover:text-white">
  LUXURY BUTTON
</Button>
```

---

## Input Components

### Text Input 변형

```tsx
// components/ui/input.tsx
import * as React from 'react';
import { cva, type VariantProps } from 'class-variance-authority';
import { cn } from '@/lib/utils';

const inputVariants = cva(
  'flex w-full rounded-md border bg-transparent text-base transition-colors file:border-0 file:bg-transparent file:text-sm file:font-medium placeholder:text-muted-foreground disabled:cursor-not-allowed disabled:opacity-50 md:text-sm',
  {
    variants: {
      variant: {
        default: 'border-input focus-visible:outline-none focus-visible:ring-1 focus-visible:ring-ring',
        filled: 'border-transparent bg-muted focus-visible:outline-none focus-visible:ring-1 focus-visible:ring-ring focus-visible:bg-background',
        underline: 'rounded-none border-0 border-b-2 border-input px-0 focus-visible:border-primary focus-visible:outline-none',
        ghost: 'border-transparent hover:bg-muted focus-visible:bg-muted focus-visible:outline-none',
      },
      inputSize: {
        default: 'h-9 px-3 py-1',
        sm: 'h-8 px-2 py-1 text-xs',
        lg: 'h-11 px-4 py-2 text-base',
      },
    },
    defaultVariants: {
      variant: 'default',
      inputSize: 'default',
    },
  }
);

export interface InputProps
  extends Omit<React.InputHTMLAttributes<HTMLInputElement>, 'size'>,
    VariantProps<typeof inputVariants> {
  error?: boolean;
  leftIcon?: React.ReactNode;
  rightIcon?: React.ReactNode;
}

const Input = React.forwardRef<HTMLInputElement, InputProps>(
  ({ className, variant, inputSize, error, leftIcon, rightIcon, type, ...props }, ref) => {
    return (
      <div className="relative flex items-center">
        {leftIcon && (
          <div className="absolute left-3 text-muted-foreground">
            {leftIcon}
          </div>
        )}
        <input
          type={type}
          className={cn(
            inputVariants({ variant, inputSize }),
            error && 'border-destructive focus-visible:ring-destructive',
            leftIcon && 'pl-10',
            rightIcon && 'pr-10',
            className
          )}
          ref={ref}
          aria-invalid={error}
          {...props}
        />
        {rightIcon && (
          <div className="absolute right-3 text-muted-foreground">
            {rightIcon}
          </div>
        )}
      </div>
    );
  }
);
Input.displayName = 'Input';

export { Input, inputVariants };
```

### Password Input

```tsx
// components/ui/password-input.tsx
'use client';

import * as React from 'react';
import { Eye, EyeOff } from 'lucide-react';
import { Input, type InputProps } from './input';
import { Button } from './button';
import { cn } from '@/lib/utils';

const PasswordInput = React.forwardRef<HTMLInputElement, Omit<InputProps, 'type'>>(
  ({ className, ...props }, ref) => {
    const [showPassword, setShowPassword] = React.useState(false);

    return (
      <div className="relative">
        <Input
          type={showPassword ? 'text' : 'password'}
          className={cn('pr-10', className)}
          ref={ref}
          autoComplete="current-password"
          {...props}
        />
        <Button
          type="button"
          variant="ghost"
          size="icon"
          className="absolute right-0 top-0 h-full px-3 py-2 hover:bg-transparent"
          onClick={() => setShowPassword(!showPassword)}
          aria-label={showPassword ? '비밀번호 숨기기' : '비밀번호 보기'}
        >
          {showPassword ? (
            <EyeOff className="h-4 w-4 text-muted-foreground" aria-hidden="true" />
          ) : (
            <Eye className="h-4 w-4 text-muted-foreground" aria-hidden="true" />
          )}
        </Button>
      </div>
    );
  }
);
PasswordInput.displayName = 'PasswordInput';

export { PasswordInput };
```

### Search Input

```tsx
// components/ui/search-input.tsx
'use client';

import * as React from 'react';
import { Search, X } from 'lucide-react';
import { Input, type InputProps } from './input';
import { Button } from './button';
import { cn } from '@/lib/utils';

interface SearchInputProps extends Omit<InputProps, 'type'> {
  onClear?: () => void;
  onSearch?: (value: string) => void;
}

const SearchInput = React.forwardRef<HTMLInputElement, SearchInputProps>(
  ({ className, value, onChange, onClear, onSearch, ...props }, ref) => {
    const [internalValue, setInternalValue] = React.useState('');
    const currentValue = value ?? internalValue;

    const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
      setInternalValue(e.target.value);
      onChange?.(e);
    };

    const handleClear = () => {
      setInternalValue('');
      onClear?.();
    };

    const handleKeyDown = (e: React.KeyboardEvent<HTMLInputElement>) => {
      if (e.key === 'Enter') {
        onSearch?.(currentValue as string);
      }
    };

    return (
      <div className="relative">
        <Search className="absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-muted-foreground" />
        <Input
          type="search"
          className={cn('pl-10', currentValue && 'pr-10', className)}
          ref={ref}
          value={currentValue}
          onChange={handleChange}
          onKeyDown={handleKeyDown}
          {...props}
        />
        {currentValue && (
          <Button
            type="button"
            variant="ghost"
            size="icon"
            className="absolute right-0 top-0 h-full px-3 py-2 hover:bg-transparent"
            onClick={handleClear}
            aria-label="검색어 지우기"
          >
            <X className="h-4 w-4 text-muted-foreground" />
          </Button>
        )}
      </div>
    );
  }
);
SearchInput.displayName = 'SearchInput';

export { SearchInput };
```

---

## Badge, Tag, Chip Components

### Badge 확장

```tsx
// components/ui/badge.tsx
import * as React from 'react';
import { cva, type VariantProps } from 'class-variance-authority';
import { cn } from '@/lib/utils';

const badgeVariants = cva(
  'inline-flex items-center rounded-md border px-2.5 py-0.5 text-xs font-semibold transition-colors focus:outline-none focus:ring-2 focus:ring-ring focus:ring-offset-2',
  {
    variants: {
      variant: {
        default: 'border-transparent bg-primary text-primary-foreground shadow',
        secondary: 'border-transparent bg-secondary text-secondary-foreground',
        destructive: 'border-transparent bg-destructive text-destructive-foreground shadow',
        outline: 'text-foreground',
        success: 'border-transparent bg-success text-success-foreground',
        warning: 'border-transparent bg-warning text-warning-foreground',
        info: 'border-transparent bg-info text-info-foreground',
        // 추가 스타일
        dot: 'gap-1.5 bg-transparent border-0 px-0 font-medium',
        subtle: 'border-transparent bg-primary/10 text-primary',
      },
      size: {
        default: 'px-2.5 py-0.5 text-xs',
        sm: 'px-2 py-0.5 text-[10px]',
        lg: 'px-3 py-1 text-sm',
      },
    },
    defaultVariants: {
      variant: 'default',
      size: 'default',
    },
  }
);

export interface BadgeProps
  extends React.HTMLAttributes<HTMLDivElement>,
    VariantProps<typeof badgeVariants> {
  dot?: boolean;
  dotColor?: string;
}

function Badge({ className, variant, size, dot, dotColor, children, ...props }: BadgeProps) {
  return (
    <div className={cn(badgeVariants({ variant: dot ? 'dot' : variant, size }), className)} {...props}>
      {dot && (
        <span
          className={cn('h-2 w-2 rounded-full', dotColor || 'bg-current')}
          aria-hidden="true"
        />
      )}
      {children}
    </div>
  );
}

export { Badge, badgeVariants };
```

### Tag Component (삭제 가능)

```tsx
// components/ui/tag.tsx
'use client';

import * as React from 'react';
import { X } from 'lucide-react';
import { cva, type VariantProps } from 'class-variance-authority';
import { cn } from '@/lib/utils';

const tagVariants = cva(
  'inline-flex items-center gap-1 rounded-full border px-3 py-1 text-sm transition-colors',
  {
    variants: {
      variant: {
        default: 'border-border bg-background text-foreground hover:bg-accent',
        filled: 'border-transparent bg-muted text-foreground',
        outline: 'border-primary text-primary hover:bg-primary/5',
        colored: 'border-transparent',
      },
    },
    defaultVariants: {
      variant: 'default',
    },
  }
);

export interface TagProps
  extends React.HTMLAttributes<HTMLSpanElement>,
    VariantProps<typeof tagVariants> {
  onRemove?: () => void;
  removable?: boolean;
  color?: string; // Tailwind color class (e.g., "bg-blue-100 text-blue-800")
}

function Tag({
  className,
  variant,
  onRemove,
  removable = true,
  color,
  children,
  ...props
}: TagProps) {
  return (
    <span
      className={cn(
        tagVariants({ variant: color ? 'colored' : variant }),
        color,
        className
      )}
      {...props}
    >
      {children}
      {removable && onRemove && (
        <button
          type="button"
          onClick={onRemove}
          className="ml-1 rounded-full p-0.5 hover:bg-foreground/10"
          aria-label={`${children} 삭제`}
        >
          <X className="h-3 w-3" />
        </button>
      )}
    </span>
  );
}

export { Tag, tagVariants };
```

### Chip Component (선택 가능)

```tsx
// components/ui/chip.tsx
'use client';

import * as React from 'react';
import { Check } from 'lucide-react';
import { cva, type VariantProps } from 'class-variance-authority';
import { cn } from '@/lib/utils';

const chipVariants = cva(
  'inline-flex items-center gap-1.5 rounded-full border px-3 py-1.5 text-sm font-medium transition-all cursor-pointer select-none',
  {
    variants: {
      variant: {
        default: 'border-border bg-background text-foreground hover:bg-accent',
        primary: 'border-primary bg-primary/5 text-primary hover:bg-primary/10',
      },
    },
    defaultVariants: {
      variant: 'default',
    },
  }
);

export interface ChipProps
  extends Omit<React.HTMLAttributes<HTMLButtonElement>, 'onChange'>,
    VariantProps<typeof chipVariants> {
  selected?: boolean;
  onChange?: (selected: boolean) => void;
  icon?: React.ReactNode;
}

function Chip({
  className,
  variant,
  selected = false,
  onChange,
  icon,
  children,
  ...props
}: ChipProps) {
  return (
    <button
      type="button"
      role="checkbox"
      aria-checked={selected}
      onClick={() => onChange?.(!selected)}
      className={cn(
        chipVariants({ variant }),
        selected && 'border-primary bg-primary text-primary-foreground',
        className
      )}
      {...props}
    >
      {selected ? (
        <Check className="h-3.5 w-3.5" aria-hidden="true" />
      ) : (
        icon
      )}
      {children}
    </button>
  );
}

// Chip Group for managing multiple selections
interface ChipGroupProps {
  children: React.ReactNode;
  value?: string[];
  onChange?: (value: string[]) => void;
  multiple?: boolean;
}

function ChipGroup({ children, value = [], onChange, multiple = true }: ChipGroupProps) {
  const handleSelect = (chipValue: string, selected: boolean) => {
    if (multiple) {
      const newValue = selected
        ? [...value, chipValue]
        : value.filter((v) => v !== chipValue);
      onChange?.(newValue);
    } else {
      onChange?.(selected ? [chipValue] : []);
    }
  };

  return (
    <div className="flex flex-wrap gap-2" role="group">
      {React.Children.map(children, (child) => {
        if (React.isValidElement<ChipProps & { value?: string }>(child)) {
          const chipValue = child.props.value || (child.props.children as string);
          return React.cloneElement(child, {
            selected: value.includes(chipValue),
            onChange: (selected: boolean) => handleSelect(chipValue, selected),
          });
        }
        return child;
      })}
    </div>
  );
}

export { Chip, ChipGroup, chipVariants };
```

---

## Icon Button

```tsx
// components/ui/icon-button.tsx
import * as React from 'react';
import { Slot } from '@radix-ui/react-slot';
import { cva, type VariantProps } from 'class-variance-authority';
import { cn } from '@/lib/utils';

const iconButtonVariants = cva(
  'inline-flex items-center justify-center rounded-md transition-colors disabled:pointer-events-none disabled:opacity-50',
  {
    variants: {
      variant: {
        default: 'bg-primary text-primary-foreground shadow-sm hover:bg-primary/90',
        secondary: 'bg-secondary text-secondary-foreground shadow-sm hover:bg-secondary/80',
        destructive: 'bg-destructive text-destructive-foreground shadow-sm hover:bg-destructive/90',
        outline: 'border border-input bg-background shadow-sm hover:bg-accent hover:text-accent-foreground',
        ghost: 'hover:bg-accent hover:text-accent-foreground',
        subtle: 'bg-muted text-muted-foreground hover:bg-muted/80 hover:text-foreground',
      },
      size: {
        default: 'h-9 w-9',
        sm: 'h-8 w-8',
        lg: 'h-10 w-10',
        xl: 'h-12 w-12',
      },
    },
    defaultVariants: {
      variant: 'default',
      size: 'default',
    },
  }
);

export interface IconButtonProps
  extends React.ButtonHTMLAttributes<HTMLButtonElement>,
    VariantProps<typeof iconButtonVariants> {
  asChild?: boolean;
  'aria-label': string; // 접근성 필수
}

const IconButton = React.forwardRef<HTMLButtonElement, IconButtonProps>(
  ({ className, variant, size, asChild = false, ...props }, ref) => {
    const Comp = asChild ? Slot : 'button';
    return (
      <Comp
        className={cn(iconButtonVariants({ variant, size, className }))}
        ref={ref}
        {...props}
      />
    );
  }
);
IconButton.displayName = 'IconButton';

export { IconButton, iconButtonVariants };
```

---

## Loading States

### Loading Spinner

```tsx
// components/ui/loading-spinner.tsx
import { cn } from '@/lib/utils';

interface LoadingSpinnerProps {
  size?: 'xs' | 'sm' | 'md' | 'lg' | 'xl';
  className?: string;
  label?: string;
}

const sizeClasses = {
  xs: 'h-3 w-3 border',
  sm: 'h-4 w-4 border-2',
  md: 'h-6 w-6 border-2',
  lg: 'h-8 w-8 border-2',
  xl: 'h-12 w-12 border-3',
};

export function LoadingSpinner({ size = 'md', className, label }: LoadingSpinnerProps) {
  return (
    <div className="flex items-center gap-2" role="status">
      <div
        className={cn(
          'animate-spin rounded-full border-muted-foreground/30 border-t-primary',
          sizeClasses[size],
          className
        )}
        aria-hidden="true"
      />
      {label && <span className="text-sm text-muted-foreground">{label}</span>}
      <span className="sr-only">{label || '로딩 중...'}</span>
    </div>
  );
}
```

### Skeleton

```tsx
// components/ui/skeleton.tsx
import { cn } from '@/lib/utils';

interface SkeletonProps extends React.HTMLAttributes<HTMLDivElement> {
  variant?: 'default' | 'circle' | 'text';
}

function Skeleton({ className, variant = 'default', ...props }: SkeletonProps) {
  return (
    <div
      className={cn(
        'animate-pulse bg-muted',
        variant === 'default' && 'rounded-md',
        variant === 'circle' && 'rounded-full',
        variant === 'text' && 'rounded h-4 w-full',
        className
      )}
      {...props}
    />
  );
}

// Skeleton 조합 패턴
function SkeletonCard() {
  return (
    <div className="rounded-lg border p-4 space-y-4">
      <Skeleton className="h-32 w-full" />
      <div className="space-y-2">
        <Skeleton variant="text" className="w-3/4" />
        <Skeleton variant="text" className="w-1/2" />
      </div>
      <div className="flex gap-2">
        <Skeleton variant="circle" className="h-8 w-8" />
        <div className="flex-1 space-y-1">
          <Skeleton variant="text" className="w-24" />
          <Skeleton variant="text" className="w-16" />
        </div>
      </div>
    </div>
  );
}

function SkeletonTable({ rows = 5 }: { rows?: number }) {
  return (
    <div className="space-y-3">
      {/* Header */}
      <div className="flex gap-4">
        <Skeleton className="h-8 w-[200px]" />
        <Skeleton className="h-8 w-[150px]" />
        <Skeleton className="h-8 w-[100px]" />
        <Skeleton className="h-8 flex-1" />
      </div>
      {/* Rows */}
      {Array.from({ length: rows }).map((_, i) => (
        <div key={i} className="flex gap-4">
          <Skeleton className="h-12 w-[200px]" />
          <Skeleton className="h-12 w-[150px]" />
          <Skeleton className="h-12 w-[100px]" />
          <Skeleton className="h-12 flex-1" />
        </div>
      ))}
    </div>
  );
}

function SkeletonAvatar({ size = 'md' }: { size?: 'sm' | 'md' | 'lg' }) {
  const sizeClasses = {
    sm: 'h-8 w-8',
    md: 'h-10 w-10',
    lg: 'h-14 w-14',
  };

  return <Skeleton variant="circle" className={sizeClasses[size]} />;
}

export { Skeleton, SkeletonCard, SkeletonTable, SkeletonAvatar };
```

### Loading Overlay

```tsx
// components/ui/loading-overlay.tsx
import { cn } from '@/lib/utils';
import { LoadingSpinner } from './loading-spinner';

interface LoadingOverlayProps {
  loading: boolean;
  children: React.ReactNode;
  message?: string;
  blur?: boolean;
  className?: string;
}

export function LoadingOverlay({
  loading,
  children,
  message,
  blur = true,
  className,
}: LoadingOverlayProps) {
  return (
    <div className={cn('relative', className)}>
      {children}
      {loading && (
        <div
          className={cn(
            'absolute inset-0 z-50 flex flex-col items-center justify-center bg-background/80',
            blur && 'backdrop-blur-sm'
          )}
          role="alert"
          aria-busy="true"
        >
          <LoadingSpinner size="lg" />
          {message && (
            <p className="mt-4 text-sm text-muted-foreground">{message}</p>
          )}
        </div>
      )}
    </div>
  );
}
```

---

## Accessibility Considerations

### 필수 접근성 패턴

```tsx
// 1. 아이콘 버튼은 항상 aria-label 필수
<IconButton aria-label="설정 열기">
  <Settings className="h-4 w-4" />
</IconButton>

// 2. 로딩 상태 알림
<Button loading aria-live="polite" aria-busy="true">
  저장 중...
</Button>

// 3. 에러 상태 연결
<Input
  aria-invalid={!!error}
  aria-describedby={error ? 'email-error' : undefined}
/>
{error && <p id="email-error" role="alert">{error}</p>}

// 4. 스크린 리더 전용 텍스트
<span className="sr-only">새 알림 3개</span>

// 5. 포커스 표시 (never remove)
// 기본 focus-visible 스타일 유지
```

### 색상 대비 검증

```tsx
// 최소 4.5:1 대비 유지
// OKLCH 색상 시스템에서 밝기(L) 차이 확보

// Good: 충분한 대비
'--primary: oklch(0.205 0 0)' // 어두운 배경
'--primary-foreground: oklch(0.985 0 0)' // 밝은 텍스트

// Check: https://webaim.org/resources/contrastchecker/
```

---

## Anti-Patterns

### 1. 하드코딩된 색상

```tsx
// ❌ Bad: Tailwind 색상 직접 사용
<Button className="bg-blue-500 hover:bg-blue-600">
  Click
</Button>

// ✅ Good: 시맨틱 토큰 사용
<Button variant="default">
  Click
</Button>
```

### 2. 접근성 속성 누락

```tsx
// ❌ Bad: 아이콘만 있는 버튼에 레이블 없음
<button onClick={onClose}>
  <X />
</button>

// ✅ Good: 스크린 리더용 레이블 제공
<IconButton onClick={onClose} aria-label="닫기">
  <X className="h-4 w-4" />
</IconButton>
```

### 3. 불필요한 div 래핑

```tsx
// ❌ Bad: 과도한 DOM 중첩
<div>
  <div>
    <Button>Click</Button>
  </div>
</div>

// ✅ Good: 필요한 경우만 래핑
<Button>Click</Button>
```

### 4. 인라인 스타일 오버라이드

```tsx
// ❌ Bad: 인라인으로 variant 무시
<Button className="bg-red-500 text-white">
  Delete
</Button>

// ✅ Good: variant 시스템 활용
<Button variant="destructive">
  Delete
</Button>
```

---

## References

- `_references/COMPONENT-PATTERN.md`
- `3-design-system/SKILL.md` (globals.css, 토큰 정의)
- shadcn/ui 공식 문서: https://ui.shadcn.com/
