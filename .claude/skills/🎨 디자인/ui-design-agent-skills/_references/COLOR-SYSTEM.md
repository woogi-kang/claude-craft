# COLOR-SYSTEM.md

색상 시스템과 테마 구축 가이드

---

## 목차

1. [OKLCH 색 공간 이해](#oklch-색-공간-이해)
2. [12가지 미적 팔레트](#12가지-미적-팔레트)
3. [다크 모드 구현](#다크-모드-구현)
4. [시맨틱 색상 토큰](#시맨틱-색상-토큰)
5. [접근성 대비율](#접근성-대비율)
6. [Tailwind 통합](#tailwind-통합)

---

## OKLCH 색 공간 이해

### OKLCH란?

OKLCH는 **인간의 색 인식에 기반한** 새로운 색 공간입니다.

```
oklch(L% C H)
      │  │ │
      │  │ └── Hue (색상): 0-360도
      │  └──── Chroma (채도): 0-0.4+
      └─────── Lightness (밝기): 0-100%
```

### OKLCH의 장점

1. **일관된 밝기**: 같은 L 값은 실제로 동일한 밝기로 보임
2. **예측 가능한 대비**: 밝기 차이로 대비율 계산 가능
3. **색 보간 품질**: 그라데이션에서 회색 영역 없음
4. **다크 모드 용이**: L 값만 조정하면 됨

### HSL vs OKLCH 비교

```css
/* HSL - 같은 saturation이어도 밝기가 다르게 보임 */
.hsl-blue { color: hsl(220, 100%, 50%); }   /* 실제로 더 어두워 보임 */
.hsl-yellow { color: hsl(60, 100%, 50%); }  /* 실제로 더 밝아 보임 */

/* OKLCH - 같은 L값은 동일한 밝기로 인식 */
.oklch-blue { color: oklch(60% 0.15 250); }
.oklch-yellow { color: oklch(60% 0.15 90); }
```

### 기본 색상 공식

```css
/* Primary 색상 스케일 생성 공식 */
:root {
  /* Base: 주 색상 정의 */
  --primary-hue: 250;        /* Blue */
  --primary-chroma: 0.15;    /* Saturation level */

  /* 자동 스케일 생성 */
  --primary-50:  oklch(97% calc(var(--primary-chroma) * 0.3) var(--primary-hue));
  --primary-100: oklch(94% calc(var(--primary-chroma) * 0.4) var(--primary-hue));
  --primary-200: oklch(88% calc(var(--primary-chroma) * 0.6) var(--primary-hue));
  --primary-300: oklch(80% calc(var(--primary-chroma) * 0.8) var(--primary-hue));
  --primary-400: oklch(70% var(--primary-chroma) var(--primary-hue));
  --primary-500: oklch(60% var(--primary-chroma) var(--primary-hue));
  --primary-600: oklch(50% var(--primary-chroma) var(--primary-hue));
  --primary-700: oklch(40% var(--primary-chroma) var(--primary-hue));
  --primary-800: oklch(30% calc(var(--primary-chroma) * 0.8) var(--primary-hue));
  --primary-900: oklch(20% calc(var(--primary-chroma) * 0.6) var(--primary-hue));
  --primary-950: oklch(12% calc(var(--primary-chroma) * 0.4) var(--primary-hue));
}
```

---

## 12가지 미적 팔레트

### 1. Midnight Noir (다크 럭셔리)

```css
/* 깊고 신비로운 다크 팔레트 */
:root {
  --midnight-noir-bg: oklch(8% 0.02 270);
  --midnight-noir-surface: oklch(12% 0.02 270);
  --midnight-noir-border: oklch(20% 0.03 270);
  --midnight-noir-muted: oklch(50% 0.02 270);
  --midnight-noir-text: oklch(90% 0.01 270);
  --midnight-noir-accent: oklch(70% 0.18 280);
  --midnight-noir-accent-hover: oklch(75% 0.20 280);
}
```

```tsx
// Midnight Noir Theme Config
export const midnightNoirTheme = {
  name: 'midnight-noir',
  colors: {
    background: 'oklch(8% 0.02 270)',
    foreground: 'oklch(90% 0.01 270)',
    card: 'oklch(12% 0.02 270)',
    cardForeground: 'oklch(90% 0.01 270)',
    primary: 'oklch(70% 0.18 280)',
    primaryForeground: 'oklch(98% 0.01 270)',
    secondary: 'oklch(20% 0.03 270)',
    secondaryForeground: 'oklch(80% 0.02 270)',
    muted: 'oklch(15% 0.02 270)',
    mutedForeground: 'oklch(50% 0.02 270)',
    accent: 'oklch(25% 0.04 280)',
    accentForeground: 'oklch(90% 0.01 270)',
    border: 'oklch(20% 0.03 270)',
    ring: 'oklch(70% 0.18 280)',
  },
} as const;
```

### 2. Sage Garden (자연/힐링)

```css
/* 부드럽고 자연스러운 그린 팔레트 */
:root {
  --sage-garden-bg: oklch(98% 0.01 140);
  --sage-garden-surface: oklch(96% 0.02 140);
  --sage-garden-border: oklch(88% 0.04 140);
  --sage-garden-muted: oklch(55% 0.06 140);
  --sage-garden-text: oklch(20% 0.03 140);
  --sage-garden-accent: oklch(55% 0.12 145);
  --sage-garden-accent-hover: oklch(50% 0.14 145);
}
```

```tsx
export const sageGardenTheme = {
  name: 'sage-garden',
  colors: {
    background: 'oklch(98% 0.01 140)',
    foreground: 'oklch(20% 0.03 140)',
    card: 'oklch(96% 0.02 140)',
    cardForeground: 'oklch(20% 0.03 140)',
    primary: 'oklch(55% 0.12 145)',
    primaryForeground: 'oklch(98% 0.01 140)',
    secondary: 'oklch(92% 0.04 140)',
    secondaryForeground: 'oklch(30% 0.05 140)',
    muted: 'oklch(94% 0.02 140)',
    mutedForeground: 'oklch(55% 0.06 140)',
    accent: 'oklch(88% 0.06 140)',
    accentForeground: 'oklch(25% 0.04 140)',
    border: 'oklch(88% 0.04 140)',
    ring: 'oklch(55% 0.12 145)',
  },
} as const;
```

### 3. Coral Sunset (따뜻하고 에너지틱)

```css
/* 활기차고 따뜻한 오렌지-핑크 팔레트 */
:root {
  --coral-sunset-bg: oklch(99% 0.01 30);
  --coral-sunset-surface: oklch(97% 0.02 25);
  --coral-sunset-border: oklch(90% 0.04 25);
  --coral-sunset-muted: oklch(60% 0.05 25);
  --coral-sunset-text: oklch(15% 0.02 25);
  --coral-sunset-accent: oklch(65% 0.18 25);
  --coral-sunset-accent-hover: oklch(60% 0.20 25);
}
```

### 4. Arctic Frost (깨끗하고 프로페셔널)

```css
/* 차갑고 깨끗한 블루-그레이 팔레트 */
:root {
  --arctic-frost-bg: oklch(99% 0.005 220);
  --arctic-frost-surface: oklch(97% 0.01 220);
  --arctic-frost-border: oklch(90% 0.02 220);
  --arctic-frost-muted: oklch(55% 0.03 220);
  --arctic-frost-text: oklch(15% 0.01 220);
  --arctic-frost-accent: oklch(55% 0.15 230);
  --arctic-frost-accent-hover: oklch(50% 0.17 230);
}
```

### 5. Lavender Dream (부드럽고 창의적)

```css
/* 몽환적인 라벤더 팔레트 */
:root {
  --lavender-dream-bg: oklch(98% 0.02 290);
  --lavender-dream-surface: oklch(96% 0.03 290);
  --lavender-dream-border: oklch(88% 0.05 290);
  --lavender-dream-muted: oklch(55% 0.08 290);
  --lavender-dream-text: oklch(20% 0.04 290);
  --lavender-dream-accent: oklch(60% 0.16 290);
  --lavender-dream-accent-hover: oklch(55% 0.18 290);
}
```

### 6. Charcoal Ember (모던 다크 + 액센트)

```css
/* 숯과 불씨 느낌의 다크 팔레트 */
:root {
  --charcoal-ember-bg: oklch(12% 0.01 30);
  --charcoal-ember-surface: oklch(16% 0.01 30);
  --charcoal-ember-border: oklch(25% 0.02 30);
  --charcoal-ember-muted: oklch(50% 0.02 30);
  --charcoal-ember-text: oklch(92% 0.01 30);
  --charcoal-ember-accent: oklch(65% 0.20 25);
  --charcoal-ember-accent-hover: oklch(70% 0.22 25);
}
```

### 7. Ocean Depths (딥 블루)

```css
/* 깊은 바다 느낌의 블루 팔레트 */
:root {
  --ocean-depths-bg: oklch(15% 0.03 240);
  --ocean-depths-surface: oklch(20% 0.04 240);
  --ocean-depths-border: oklch(30% 0.05 240);
  --ocean-depths-muted: oklch(55% 0.04 240);
  --ocean-depths-text: oklch(95% 0.01 240);
  --ocean-depths-accent: oklch(70% 0.15 200);
  --ocean-depths-accent-hover: oklch(75% 0.17 200);
}
```

### 8. Sand Dune (뉴트럴 웜)

```css
/* 따뜻한 모래색 뉴트럴 팔레트 */
:root {
  --sand-dune-bg: oklch(96% 0.02 70);
  --sand-dune-surface: oklch(93% 0.03 70);
  --sand-dune-border: oklch(85% 0.04 70);
  --sand-dune-muted: oklch(55% 0.04 70);
  --sand-dune-text: oklch(20% 0.02 70);
  --sand-dune-accent: oklch(55% 0.10 70);
  --sand-dune-accent-hover: oklch(50% 0.12 70);
}
```

### 9. Neon Cyber (사이버펑크)

```css
/* 네온 사이버펑크 팔레트 */
:root {
  --neon-cyber-bg: oklch(8% 0.02 280);
  --neon-cyber-surface: oklch(12% 0.03 280);
  --neon-cyber-border: oklch(20% 0.05 280);
  --neon-cyber-muted: oklch(45% 0.04 280);
  --neon-cyber-text: oklch(92% 0.02 280);
  --neon-cyber-accent: oklch(75% 0.25 320);
  --neon-cyber-accent-secondary: oklch(75% 0.22 180);
  --neon-cyber-accent-hover: oklch(80% 0.28 320);
}
```

### 10. Terracotta Earth (어스 톤)

```css
/* 따뜻한 테라코타 어스 팔레트 */
:root {
  --terracotta-earth-bg: oklch(95% 0.02 50);
  --terracotta-earth-surface: oklch(92% 0.03 50);
  --terracotta-earth-border: oklch(82% 0.05 50);
  --terracotta-earth-muted: oklch(55% 0.05 50);
  --terracotta-earth-text: oklch(18% 0.03 50);
  --terracotta-earth-accent: oklch(55% 0.14 35);
  --terracotta-earth-accent-hover: oklch(50% 0.16 35);
}
```

### 11. Mint Fresh (청량한 민트)

```css
/* 상쾌한 민트 팔레트 */
:root {
  --mint-fresh-bg: oklch(98% 0.01 170);
  --mint-fresh-surface: oklch(96% 0.02 170);
  --mint-fresh-border: oklch(88% 0.04 170);
  --mint-fresh-muted: oklch(55% 0.06 170);
  --mint-fresh-text: oklch(18% 0.03 170);
  --mint-fresh-accent: oklch(65% 0.14 170);
  --mint-fresh-accent-hover: oklch(60% 0.16 170);
}
```

### 12. Monochrome Pro (무채색 프로)

```css
/* 순수 무채색 프로페셔널 팔레트 */
:root {
  --mono-pro-bg: oklch(99% 0 0);
  --mono-pro-surface: oklch(96% 0 0);
  --mono-pro-border: oklch(88% 0 0);
  --mono-pro-muted: oklch(55% 0 0);
  --mono-pro-text: oklch(10% 0 0);
  --mono-pro-accent: oklch(25% 0 0);
  --mono-pro-accent-hover: oklch(15% 0 0);
}
```

---

## 다크 모드 구현

### CSS Variables 기반 테마 전환

```css
/* app/globals.css */
@import "tailwindcss";

@theme {
  /* Light Mode (default) */
  --color-background: oklch(99% 0.005 220);
  --color-foreground: oklch(15% 0.01 220);
  --color-card: oklch(100% 0 0);
  --color-card-foreground: oklch(15% 0.01 220);
  --color-primary: oklch(55% 0.15 250);
  --color-primary-foreground: oklch(98% 0.01 250);
  --color-secondary: oklch(96% 0.01 220);
  --color-secondary-foreground: oklch(25% 0.01 220);
  --color-muted: oklch(96% 0.01 220);
  --color-muted-foreground: oklch(50% 0.02 220);
  --color-accent: oklch(96% 0.01 220);
  --color-accent-foreground: oklch(25% 0.01 220);
  --color-destructive: oklch(55% 0.2 25);
  --color-destructive-foreground: oklch(98% 0.01 25);
  --color-border: oklch(90% 0.01 220);
  --color-input: oklch(90% 0.01 220);
  --color-ring: oklch(55% 0.15 250);
}

/* Dark Mode */
.dark {
  --color-background: oklch(12% 0.01 250);
  --color-foreground: oklch(95% 0.01 250);
  --color-card: oklch(15% 0.01 250);
  --color-card-foreground: oklch(95% 0.01 250);
  --color-primary: oklch(70% 0.15 250);
  --color-primary-foreground: oklch(10% 0.01 250);
  --color-secondary: oklch(20% 0.01 250);
  --color-secondary-foreground: oklch(90% 0.01 250);
  --color-muted: oklch(20% 0.01 250);
  --color-muted-foreground: oklch(60% 0.02 250);
  --color-accent: oklch(20% 0.01 250);
  --color-accent-foreground: oklch(90% 0.01 250);
  --color-destructive: oklch(60% 0.2 25);
  --color-destructive-foreground: oklch(98% 0.01 25);
  --color-border: oklch(25% 0.02 250);
  --color-input: oklch(25% 0.02 250);
  --color-ring: oklch(70% 0.15 250);
}
```

### Next.js 테마 프로바이더

```tsx
// components/providers/theme-provider.tsx
'use client';

import * as React from 'react';
import { ThemeProvider as NextThemesProvider } from 'next-themes';

export function ThemeProvider({
  children,
  ...props
}: React.ComponentProps<typeof NextThemesProvider>) {
  return (
    <NextThemesProvider
      attribute="class"
      defaultTheme="system"
      enableSystem
      disableTransitionOnChange
      {...props}
    >
      {children}
    </NextThemesProvider>
  );
}
```

```tsx
// app/layout.tsx
import { ThemeProvider } from '@/components/providers/theme-provider';

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="ko" suppressHydrationWarning>
      <body>
        <ThemeProvider>{children}</ThemeProvider>
      </body>
    </html>
  );
}
```

### 테마 토글 컴포넌트

```tsx
// components/ui/theme-toggle.tsx
'use client';

import { useTheme } from 'next-themes';
import { useEffect, useState } from 'react';
import { Moon, Sun, Monitor } from 'lucide-react';

export function ThemeToggle() {
  const [mounted, setMounted] = useState(false);
  const { theme, setTheme } = useTheme();

  useEffect(() => {
    setMounted(true);
  }, []);

  if (!mounted) {
    return <div className="w-9 h-9" />; // Skeleton to prevent layout shift
  }

  return (
    <div className="flex items-center gap-1 p-1 rounded-full bg-muted">
      <button
        onClick={() => setTheme('light')}
        className={`p-2 rounded-full transition-colors ${
          theme === 'light' ? 'bg-background shadow-sm' : 'hover:bg-background/50'
        }`}
        aria-label="Light mode"
      >
        <Sun className="w-4 h-4" />
      </button>
      <button
        onClick={() => setTheme('dark')}
        className={`p-2 rounded-full transition-colors ${
          theme === 'dark' ? 'bg-background shadow-sm' : 'hover:bg-background/50'
        }`}
        aria-label="Dark mode"
      >
        <Moon className="w-4 h-4" />
      </button>
      <button
        onClick={() => setTheme('system')}
        className={`p-2 rounded-full transition-colors ${
          theme === 'system' ? 'bg-background shadow-sm' : 'hover:bg-background/50'
        }`}
        aria-label="System theme"
      >
        <Monitor className="w-4 h-4" />
      </button>
    </div>
  );
}
```

### 부드러운 테마 전환 애니메이션

```css
/* Smooth transition for theme changes */
html.transitioning,
html.transitioning *,
html.transitioning *::before,
html.transitioning *::after {
  transition: background-color 300ms ease-out,
              border-color 300ms ease-out,
              color 150ms ease-out !important;
}
```

```tsx
// Enable transition class temporarily during theme change
const handleThemeChange = (newTheme: string) => {
  document.documentElement.classList.add('transitioning');
  setTheme(newTheme);
  setTimeout(() => {
    document.documentElement.classList.remove('transitioning');
  }, 300);
};
```

---

## 시맨틱 색상 토큰

### 상태 색상 시스템

```css
/* app/globals.css */
@theme {
  /* Success - Green */
  --color-success: oklch(60% 0.15 145);
  --color-success-foreground: oklch(98% 0.01 145);
  --color-success-muted: oklch(92% 0.05 145);

  /* Warning - Amber */
  --color-warning: oklch(70% 0.15 80);
  --color-warning-foreground: oklch(15% 0.02 80);
  --color-warning-muted: oklch(92% 0.06 80);

  /* Error/Destructive - Red */
  --color-error: oklch(55% 0.2 25);
  --color-error-foreground: oklch(98% 0.01 25);
  --color-error-muted: oklch(92% 0.05 25);

  /* Info - Blue */
  --color-info: oklch(60% 0.15 240);
  --color-info-foreground: oklch(98% 0.01 240);
  --color-info-muted: oklch(92% 0.05 240);
}

/* Dark mode adjustments */
.dark {
  --color-success: oklch(65% 0.15 145);
  --color-success-muted: oklch(25% 0.08 145);

  --color-warning: oklch(75% 0.15 80);
  --color-warning-muted: oklch(25% 0.08 80);

  --color-error: oklch(60% 0.2 25);
  --color-error-muted: oklch(25% 0.08 25);

  --color-info: oklch(65% 0.15 240);
  --color-info-muted: oklch(25% 0.08 240);
}
```

### Alert 컴포넌트 예제

```tsx
// components/ui/alert.tsx
import { cva, type VariantProps } from 'class-variance-authority';
import { cn } from '@/lib/utils';
import { AlertCircle, CheckCircle, Info, AlertTriangle } from 'lucide-react';

const alertVariants = cva(
  'relative w-full rounded-lg border px-4 py-3 text-sm flex items-start gap-3',
  {
    variants: {
      variant: {
        default: 'bg-background text-foreground border-border',
        success: 'bg-success-muted text-success border-success/30',
        warning: 'bg-warning-muted text-warning-foreground border-warning/30',
        error: 'bg-error-muted text-error border-error/30',
        info: 'bg-info-muted text-info border-info/30',
      },
    },
    defaultVariants: {
      variant: 'default',
    },
  }
);

const iconMap = {
  default: Info,
  success: CheckCircle,
  warning: AlertTriangle,
  error: AlertCircle,
  info: Info,
};

interface AlertProps
  extends React.HTMLAttributes<HTMLDivElement>,
    VariantProps<typeof alertVariants> {
  title?: string;
}

export function Alert({
  className,
  variant = 'default',
  title,
  children,
  ...props
}: AlertProps) {
  const Icon = iconMap[variant || 'default'];

  return (
    <div
      role="alert"
      className={cn(alertVariants({ variant }), className)}
      {...props}
    >
      <Icon className="h-4 w-4 mt-0.5 shrink-0" />
      <div>
        {title && <h5 className="font-medium mb-1">{title}</h5>}
        {children}
      </div>
    </div>
  );
}
```

### Badge 컴포넌트 예제

```tsx
// components/ui/badge.tsx
import { cva, type VariantProps } from 'class-variance-authority';
import { cn } from '@/lib/utils';

const badgeVariants = cva(
  'inline-flex items-center rounded-full px-2.5 py-0.5 text-xs font-medium transition-colors',
  {
    variants: {
      variant: {
        default: 'bg-primary text-primary-foreground',
        secondary: 'bg-secondary text-secondary-foreground',
        success: 'bg-success text-success-foreground',
        warning: 'bg-warning text-warning-foreground',
        error: 'bg-error text-error-foreground',
        info: 'bg-info text-info-foreground',
        outline: 'border border-current bg-transparent',
      },
    },
    defaultVariants: {
      variant: 'default',
    },
  }
);

interface BadgeProps
  extends React.HTMLAttributes<HTMLSpanElement>,
    VariantProps<typeof badgeVariants> {}

export function Badge({ className, variant, ...props }: BadgeProps) {
  return (
    <span className={cn(badgeVariants({ variant }), className)} {...props} />
  );
}
```

---

## 접근성 대비율

### WCAG 대비 요구사항

| 레벨 | 일반 텍스트 | 큰 텍스트 (18pt+) |
|------|------------|------------------|
| **AA** | 4.5:1 | 3:1 |
| **AAA** | 7:1 | 4.5:1 |

### OKLCH에서 대비율 계산

```typescript
// lib/color-contrast.ts

/**
 * Calculate contrast ratio between two OKLCH colors
 * Based on OKLCH lightness values
 */
export function calculateContrastRatio(
  l1: number, // Lightness of color 1 (0-1)
  l2: number  // Lightness of color 2 (0-1)
): number {
  // Convert OKLCH lightness to relative luminance (approximation)
  const lum1 = l1 ** 2.4;
  const lum2 = l2 ** 2.4;

  const lighter = Math.max(lum1, lum2);
  const darker = Math.min(lum1, lum2);

  return (lighter + 0.05) / (darker + 0.05);
}

/**
 * Check if colors meet WCAG requirements
 */
export function meetsWCAG(
  l1: number,
  l2: number,
  level: 'AA' | 'AAA' = 'AA',
  isLargeText: boolean = false
): boolean {
  const ratio = calculateContrastRatio(l1, l2);
  const required = level === 'AAA'
    ? (isLargeText ? 4.5 : 7)
    : (isLargeText ? 3 : 4.5);

  return ratio >= required;
}

/**
 * Find accessible text color for a given background
 */
export function getAccessibleTextColor(
  bgLightness: number,
  preferDark: boolean = true
): number {
  // Target contrast ratio of 7:1 for AAA
  const targetRatio = 7;

  if (preferDark) {
    // Calculate required lightness for dark text
    let l = 0.15;
    while (l > 0 && calculateContrastRatio(bgLightness, l) < targetRatio) {
      l -= 0.05;
    }
    if (calculateContrastRatio(bgLightness, l) >= targetRatio) return l;
  }

  // Calculate required lightness for light text
  let l = 0.95;
  while (l < 1 && calculateContrastRatio(bgLightness, l) < targetRatio) {
    l += 0.05;
  }
  return l;
}
```

### 접근성 검증 컴포넌트

```tsx
// components/dev/contrast-checker.tsx
'use client';

import { useState } from 'react';
import { calculateContrastRatio, meetsWCAG } from '@/lib/color-contrast';

export function ContrastChecker() {
  const [bgL, setBgL] = useState(0.98);
  const [fgL, setFgL] = useState(0.15);

  const ratio = calculateContrastRatio(bgL, fgL);
  const aaSmall = meetsWCAG(bgL, fgL, 'AA', false);
  const aaLarge = meetsWCAG(bgL, fgL, 'AA', true);
  const aaaSmall = meetsWCAG(bgL, fgL, 'AAA', false);
  const aaaLarge = meetsWCAG(bgL, fgL, 'AAA', true);

  return (
    <div className="p-6 rounded-xl border bg-card space-y-4">
      <h3 className="font-semibold">Contrast Checker</h3>

      <div className="grid grid-cols-2 gap-4">
        <div>
          <label className="text-sm text-muted-foreground">
            Background Lightness: {(bgL * 100).toFixed(0)}%
          </label>
          <input
            type="range"
            min="0"
            max="100"
            value={bgL * 100}
            onChange={(e) => setBgL(Number(e.target.value) / 100)}
            className="w-full"
          />
        </div>
        <div>
          <label className="text-sm text-muted-foreground">
            Foreground Lightness: {(fgL * 100).toFixed(0)}%
          </label>
          <input
            type="range"
            min="0"
            max="100"
            value={fgL * 100}
            onChange={(e) => setFgL(Number(e.target.value) / 100)}
            className="w-full"
          />
        </div>
      </div>

      {/* Preview */}
      <div
        className="p-4 rounded-lg text-center"
        style={{
          backgroundColor: `oklch(${bgL * 100}% 0 0)`,
          color: `oklch(${fgL * 100}% 0 0)`,
        }}
      >
        <p className="text-lg font-semibold">Sample Text</p>
        <p className="text-sm">This is smaller body text</p>
      </div>

      {/* Results */}
      <div className="space-y-2 text-sm">
        <p className="font-mono">Contrast Ratio: {ratio.toFixed(2)}:1</p>
        <div className="flex gap-4">
          <span className={aaSmall ? 'text-success' : 'text-error'}>
            AA (Normal): {aaSmall ? 'Pass' : 'Fail'}
          </span>
          <span className={aaLarge ? 'text-success' : 'text-error'}>
            AA (Large): {aaLarge ? 'Pass' : 'Fail'}
          </span>
          <span className={aaaSmall ? 'text-success' : 'text-error'}>
            AAA (Normal): {aaaSmall ? 'Pass' : 'Fail'}
          </span>
          <span className={aaaLarge ? 'text-success' : 'text-error'}>
            AAA (Large): {aaaLarge ? 'Pass' : 'Fail'}
          </span>
        </div>
      </div>
    </div>
  );
}
```

### 안전한 색상 조합 레시피

```css
/* Pre-tested accessible color combinations */

/* Light Mode - AA Compliant */
.accessible-light {
  /* Background: L=98% / Text: L=15% → Ratio: ~12:1 */
  --bg: oklch(98% 0.01 250);
  --text: oklch(15% 0.01 250);

  /* Muted text: L=40% on L=98% → Ratio: ~5:1 */
  --muted: oklch(40% 0.02 250);

  /* Primary on white: L=50% → Ratio: ~5:1 */
  --primary: oklch(50% 0.15 250);
}

/* Dark Mode - AA Compliant */
.accessible-dark {
  /* Background: L=12% / Text: L=92% → Ratio: ~11:1 */
  --bg: oklch(12% 0.01 250);
  --text: oklch(92% 0.01 250);

  /* Muted text: L=65% on L=12% → Ratio: ~5:1 */
  --muted: oklch(65% 0.02 250);

  /* Primary on dark: L=70% → Ratio: ~6:1 */
  --primary: oklch(70% 0.15 250);
}
```

---

## Tailwind 통합

### Tailwind v4 Theme 설정

```css
/* app/globals.css */
@import "tailwindcss";

@theme {
  /* Base Colors */
  --color-background: oklch(99% 0.005 250);
  --color-foreground: oklch(12% 0.01 250);

  /* Card */
  --color-card: oklch(100% 0 0);
  --color-card-foreground: oklch(12% 0.01 250);

  /* Popover */
  --color-popover: oklch(100% 0 0);
  --color-popover-foreground: oklch(12% 0.01 250);

  /* Primary */
  --color-primary: oklch(55% 0.15 250);
  --color-primary-foreground: oklch(98% 0.01 250);

  /* Secondary */
  --color-secondary: oklch(96% 0.01 250);
  --color-secondary-foreground: oklch(25% 0.01 250);

  /* Muted */
  --color-muted: oklch(96% 0.01 250);
  --color-muted-foreground: oklch(45% 0.02 250);

  /* Accent */
  --color-accent: oklch(96% 0.01 250);
  --color-accent-foreground: oklch(25% 0.01 250);

  /* Destructive */
  --color-destructive: oklch(55% 0.2 25);
  --color-destructive-foreground: oklch(98% 0.01 25);

  /* Border & Input */
  --color-border: oklch(90% 0.01 250);
  --color-input: oklch(90% 0.01 250);
  --color-ring: oklch(55% 0.15 250);

  /* Chart Colors */
  --color-chart-1: oklch(60% 0.15 250);
  --color-chart-2: oklch(60% 0.15 170);
  --color-chart-3: oklch(60% 0.15 290);
  --color-chart-4: oklch(60% 0.15 50);
  --color-chart-5: oklch(60% 0.15 320);

  /* Semantic Colors */
  --color-success: oklch(60% 0.15 145);
  --color-success-foreground: oklch(98% 0.01 145);
  --color-warning: oklch(70% 0.15 80);
  --color-warning-foreground: oklch(15% 0.02 80);
  --color-error: oklch(55% 0.2 25);
  --color-error-foreground: oklch(98% 0.01 25);
  --color-info: oklch(60% 0.15 240);
  --color-info-foreground: oklch(98% 0.01 240);

  /* Radius */
  --radius-sm: 0.25rem;
  --radius-md: 0.5rem;
  --radius-lg: 0.75rem;
  --radius-xl: 1rem;
  --radius-2xl: 1.5rem;
  --radius-full: 9999px;
}

/* Dark mode overrides */
.dark {
  --color-background: oklch(12% 0.01 250);
  --color-foreground: oklch(95% 0.01 250);
  --color-card: oklch(15% 0.01 250);
  --color-card-foreground: oklch(95% 0.01 250);
  --color-popover: oklch(15% 0.01 250);
  --color-popover-foreground: oklch(95% 0.01 250);
  --color-primary: oklch(70% 0.15 250);
  --color-primary-foreground: oklch(10% 0.01 250);
  --color-secondary: oklch(20% 0.01 250);
  --color-secondary-foreground: oklch(90% 0.01 250);
  --color-muted: oklch(20% 0.01 250);
  --color-muted-foreground: oklch(60% 0.02 250);
  --color-accent: oklch(20% 0.01 250);
  --color-accent-foreground: oklch(90% 0.01 250);
  --color-border: oklch(25% 0.02 250);
  --color-input: oklch(25% 0.02 250);
}
```

### 색상 유틸리티 함수

```typescript
// lib/colors.ts

/**
 * Parse OKLCH color string to values
 */
export function parseOklch(color: string): {
  l: number;
  c: number;
  h: number;
} | null {
  const match = color.match(/oklch\(([\d.]+)%?\s+([\d.]+)\s+([\d.]+)\)/);
  if (!match) return null;

  return {
    l: parseFloat(match[1]) / 100,
    c: parseFloat(match[2]),
    h: parseFloat(match[3]),
  };
}

/**
 * Generate color scale from base color
 */
export function generateColorScale(
  baseHue: number,
  baseChroma: number = 0.15
): Record<string, string> {
  return {
    50: `oklch(97% ${baseChroma * 0.3} ${baseHue})`,
    100: `oklch(94% ${baseChroma * 0.4} ${baseHue})`,
    200: `oklch(88% ${baseChroma * 0.6} ${baseHue})`,
    300: `oklch(80% ${baseChroma * 0.8} ${baseHue})`,
    400: `oklch(70% ${baseChroma} ${baseHue})`,
    500: `oklch(60% ${baseChroma} ${baseHue})`,
    600: `oklch(50% ${baseChroma} ${baseHue})`,
    700: `oklch(40% ${baseChroma} ${baseHue})`,
    800: `oklch(30% ${baseChroma * 0.8} ${baseHue})`,
    900: `oklch(20% ${baseChroma * 0.6} ${baseHue})`,
    950: `oklch(12% ${baseChroma * 0.4} ${baseHue})`,
  };
}

/**
 * Adjust lightness for hover states
 */
export function adjustLightness(
  color: string,
  amount: number // positive = lighter, negative = darker
): string {
  const parsed = parseOklch(color);
  if (!parsed) return color;

  const newL = Math.max(0, Math.min(1, parsed.l + amount));
  return `oklch(${newL * 100}% ${parsed.c} ${parsed.h})`;
}
```

### 동적 테마 생성

```tsx
// hooks/use-theme-generator.ts
'use client';

import { useMemo } from 'react';
import { generateColorScale } from '@/lib/colors';

interface ThemeConfig {
  primaryHue: number;
  primaryChroma?: number;
  neutralHue?: number;
  mode: 'light' | 'dark';
}

export function useThemeGenerator(config: ThemeConfig) {
  const {
    primaryHue,
    primaryChroma = 0.15,
    neutralHue = primaryHue,
    mode,
  } = config;

  const theme = useMemo(() => {
    const primaryScale = generateColorScale(primaryHue, primaryChroma);
    const neutralScale = generateColorScale(neutralHue, 0.02);

    if (mode === 'light') {
      return {
        background: neutralScale[50],
        foreground: neutralScale[950],
        card: 'oklch(100% 0 0)',
        primary: primaryScale[500],
        primaryForeground: 'oklch(98% 0.01 0)',
        secondary: neutralScale[100],
        muted: neutralScale[100],
        mutedForeground: neutralScale[500],
        border: neutralScale[200],
      };
    }

    return {
      background: neutralScale[950],
      foreground: neutralScale[50],
      card: neutralScale[900],
      primary: primaryScale[400],
      primaryForeground: neutralScale[950],
      secondary: neutralScale[800],
      muted: neutralScale[800],
      mutedForeground: neutralScale[400],
      border: neutralScale[800],
    };
  }, [primaryHue, primaryChroma, neutralHue, mode]);

  return theme;
}
```
