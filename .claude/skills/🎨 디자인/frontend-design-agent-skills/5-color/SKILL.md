# Color Skill

프로젝트의 디자인 방향에 맞는 색상 팔레트와 테마 시스템을 구성합니다.

## Triggers

- "색상", "컬러", "팔레트", "color", "palette", "theme", "테마", "다크모드"

---

## Input

| 항목 | 필수 | 설명 |
|------|------|------|
| `aestheticDirection` | ✅ | 이전 Direction 스킬에서 결정된 미적 방향 |
| `brandColors` | ❌ | 기존 브랜드 색상 (HEX 또는 oklch) |
| `colorMode` | ❌ | 지원할 모드 (light, dark, both) - 기본값: both |
| `accessibilityLevel` | ❌ | WCAG 레벨 (AA, AAA) - 기본값: AA |

---

## Output

| 산출물 | 설명 |
|--------|------|
| `globals.css` | oklch 기반 CSS 변수 정의 |
| `color-tokens.ts` | TypeScript 색상 토큰 상수 |
| `theme-provider.tsx` | Dark mode 지원 Provider |

---

## Workflow

### Step 1: oklch 색상 공간 이해

**왜 oklch인가?**

| 색상 공간 | 장점 | 단점 |
|-----------|------|------|
| HEX/RGB | 친숙함, 도구 지원 | 인지적 균일성 없음 |
| HSL | 직관적 조정 | 밝기 불일치 |
| **oklch** | 인지적 균일성, 접근성 | 비교적 새로움 |

```css
/* oklch(Lightness Chroma Hue) */
/* L: 0-1 (밝기), C: 0-0.4 (채도), H: 0-360 (색상) */

/* 예시: 밝기만 조절해도 색조 일관성 유지 */
--primary-100: oklch(0.95 0.02 250);  /* 아주 밝은 */
--primary-500: oklch(0.60 0.15 250);  /* 기준 */
--primary-900: oklch(0.25 0.08 250);  /* 아주 어두운 */
```

---

### Step 2: 방향별 색상 팔레트

**Direction별 추천 팔레트:**

#### Minimal (미니멀)
```css
:root {
  /* Neutral-focused with subtle accent */
  --primary: oklch(0.20 0.01 0);       /* Near black */
  --secondary: oklch(0.96 0.01 0);     /* Near white */
  --accent: oklch(0.60 0.15 250);      /* Subtle blue */
  --muted: oklch(0.55 0.02 0);         /* Gray */
}
```

#### Elegant (우아함)
```css
:root {
  /* Rich, sophisticated tones */
  --primary: oklch(0.35 0.08 270);     /* Deep purple */
  --secondary: oklch(0.92 0.02 60);    /* Warm cream */
  --accent: oklch(0.70 0.12 80);       /* Gold */
  --muted: oklch(0.50 0.04 270);       /* Dusty purple */
}
```

#### Bold (대담함)
```css
:root {
  /* High contrast, vibrant */
  --primary: oklch(0.55 0.25 30);      /* Vibrant red-orange */
  --secondary: oklch(0.15 0.02 0);     /* Near black */
  --accent: oklch(0.75 0.20 90);       /* Electric yellow */
  --muted: oklch(0.40 0.05 0);         /* Dark gray */
}
```

#### Playful (장난스러움)
```css
:root {
  /* Bright, fun colors */
  --primary: oklch(0.65 0.22 290);     /* Bright purple */
  --secondary: oklch(0.70 0.18 180);   /* Teal */
  --accent: oklch(0.80 0.20 60);       /* Warm yellow */
  --muted: oklch(0.88 0.08 290);       /* Light lavender */
}
```

#### Technical (기술적)
```css
:root {
  /* Cool, precise colors */
  --primary: oklch(0.50 0.15 250);     /* Electric blue */
  --secondary: oklch(0.12 0.02 250);   /* Dark navy */
  --accent: oklch(0.75 0.18 165);      /* Cyan */
  --muted: oklch(0.55 0.03 250);       /* Steel blue */
}
```

#### Luxury (럭셔리)
```css
:root {
  /* Rich, opulent tones */
  --primary: oklch(0.25 0.05 50);      /* Dark brown/black */
  --secondary: oklch(0.70 0.10 80);    /* Gold */
  --accent: oklch(0.92 0.03 60);       /* Champagne */
  --muted: oklch(0.45 0.03 50);        /* Bronze */
}
```

---

### Step 3: 시맨틱 토큰 정의

#### 전체 globals.css 템플릿

```css
/* app/globals.css */
@import "tailwindcss";
@import "tw-animate-css";

@custom-variant dark (&:is(.dark *));

:root {
  /* =========================================
   * Core Semantic Colors
   * ========================================= */

  /* Background & Surface */
  --background: oklch(1 0 0);
  --foreground: oklch(0.145 0 0);

  --card: oklch(1 0 0);
  --card-foreground: oklch(0.145 0 0);

  --popover: oklch(1 0 0);
  --popover-foreground: oklch(0.145 0 0);

  /* Primary - Main brand color */
  --primary: oklch(0.205 0 0);
  --primary-foreground: oklch(0.985 0 0);

  /* Secondary - Supporting color */
  --secondary: oklch(0.97 0 0);
  --secondary-foreground: oklch(0.205 0 0);

  /* Muted - Subtle backgrounds */
  --muted: oklch(0.97 0 0);
  --muted-foreground: oklch(0.556 0 0);

  /* Accent - Highlights & interactions */
  --accent: oklch(0.97 0 0);
  --accent-foreground: oklch(0.205 0 0);

  /* =========================================
   * Semantic Status Colors
   * ========================================= */

  /* Destructive - Errors & dangerous actions */
  --destructive: oklch(0.577 0.245 27.325);
  --destructive-foreground: oklch(0.985 0 0);

  /* Success - Positive feedback */
  --success: oklch(0.76 0.18 145);
  --success-foreground: oklch(0.20 0.05 145);

  /* Warning - Caution needed */
  --warning: oklch(0.84 0.16 84);
  --warning-foreground: oklch(0.28 0.07 46);

  /* Info - Neutral information */
  --info: oklch(0.70 0.15 250);
  --info-foreground: oklch(0.20 0.05 250);

  /* =========================================
   * Interactive Elements
   * ========================================= */

  --border: oklch(0.922 0 0);
  --input: oklch(0.922 0 0);
  --ring: oklch(0.708 0 0);

  /* =========================================
   * Component-specific tokens
   * ========================================= */

  /* Sidebar */
  --sidebar-background: oklch(0.985 0 0);
  --sidebar-foreground: oklch(0.145 0 0);
  --sidebar-primary: oklch(0.205 0 0);
  --sidebar-primary-foreground: oklch(0.985 0 0);
  --sidebar-accent: oklch(0.97 0 0);
  --sidebar-accent-foreground: oklch(0.205 0 0);
  --sidebar-border: oklch(0.922 0 0);
  --sidebar-ring: oklch(0.708 0 0);

  /* =========================================
   * Layout & Spacing
   * ========================================= */

  --radius: 0.625rem;
}

/* =========================================
 * Dark Mode
 * ========================================= */

.dark {
  /* Background & Surface */
  --background: oklch(0.145 0 0);
  --foreground: oklch(0.985 0 0);

  --card: oklch(0.175 0 0);
  --card-foreground: oklch(0.985 0 0);

  --popover: oklch(0.145 0 0);
  --popover-foreground: oklch(0.985 0 0);

  /* Primary */
  --primary: oklch(0.985 0 0);
  --primary-foreground: oklch(0.205 0 0);

  /* Secondary */
  --secondary: oklch(0.269 0 0);
  --secondary-foreground: oklch(0.985 0 0);

  /* Muted */
  --muted: oklch(0.269 0 0);
  --muted-foreground: oklch(0.708 0 0);

  /* Accent */
  --accent: oklch(0.269 0 0);
  --accent-foreground: oklch(0.985 0 0);

  /* Status Colors - Adjusted for dark mode */
  --destructive: oklch(0.50 0.20 27);
  --destructive-foreground: oklch(0.985 0 0);

  --success: oklch(0.55 0.15 145);
  --success-foreground: oklch(0.95 0.03 145);

  --warning: oklch(0.55 0.14 84);
  --warning-foreground: oklch(0.99 0.02 95);

  --info: oklch(0.55 0.13 250);
  --info-foreground: oklch(0.95 0.03 250);

  /* Interactive */
  --border: oklch(0.269 0 0);
  --input: oklch(0.269 0 0);
  --ring: oklch(0.439 0 0);

  /* Sidebar - Dark */
  --sidebar-background: oklch(0.145 0 0);
  --sidebar-foreground: oklch(0.985 0 0);
  --sidebar-primary: oklch(0.488 0.243 264.376);
  --sidebar-primary-foreground: oklch(0.985 0 0);
  --sidebar-accent: oklch(0.269 0 0);
  --sidebar-accent-foreground: oklch(0.985 0 0);
  --sidebar-border: oklch(0.269 0 0);
  --sidebar-ring: oklch(0.439 0 0);
}

/* =========================================
 * Tailwind v4 Theme Integration
 * ========================================= */

@theme inline {
  /* Color Token Mapping */
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

  /* Radius */
  --radius-sm: calc(var(--radius) - 4px);
  --radius-md: calc(var(--radius) - 2px);
  --radius-lg: var(--radius);
  --radius-xl: calc(var(--radius) + 4px);
  --radius-2xl: calc(var(--radius) + 8px);
  --radius-full: 9999px;
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

### Step 4: 색상 스케일 생성

#### 단일 색상에서 스케일 생성

```typescript
// lib/color-utils.ts

/**
 * oklch 색상에서 10단계 스케일 생성
 * @param baseHue - 기준 색상 (0-360)
 * @param baseChroma - 기준 채도 (0-0.4)
 */
export function generateColorScale(
  baseHue: number,
  baseChroma: number = 0.15
): Record<string, string> {
  return {
    50:  `oklch(0.97 ${baseChroma * 0.2} ${baseHue})`,
    100: `oklch(0.93 ${baseChroma * 0.3} ${baseHue})`,
    200: `oklch(0.87 ${baseChroma * 0.5} ${baseHue})`,
    300: `oklch(0.78 ${baseChroma * 0.7} ${baseHue})`,
    400: `oklch(0.68 ${baseChroma * 0.9} ${baseHue})`,
    500: `oklch(0.58 ${baseChroma} ${baseHue})`,        // Base
    600: `oklch(0.50 ${baseChroma * 0.95} ${baseHue})`,
    700: `oklch(0.42 ${baseChroma * 0.85} ${baseHue})`,
    800: `oklch(0.34 ${baseChroma * 0.7} ${baseHue})`,
    900: `oklch(0.26 ${baseChroma * 0.5} ${baseHue})`,
    950: `oklch(0.18 ${baseChroma * 0.3} ${baseHue})`,
  };
}

// 사용 예시
const blueScale = generateColorScale(250, 0.18);
// → { 50: "oklch(0.97 0.036 250)", 500: "oklch(0.58 0.18 250)", ... }
```

#### CSS 변수로 내보내기

```css
/* 생성된 색상 스케일 */
:root {
  /* Blue scale */
  --blue-50: oklch(0.97 0.036 250);
  --blue-100: oklch(0.93 0.054 250);
  --blue-200: oklch(0.87 0.090 250);
  --blue-300: oklch(0.78 0.126 250);
  --blue-400: oklch(0.68 0.162 250);
  --blue-500: oklch(0.58 0.180 250);
  --blue-600: oklch(0.50 0.171 250);
  --blue-700: oklch(0.42 0.153 250);
  --blue-800: oklch(0.34 0.126 250);
  --blue-900: oklch(0.26 0.090 250);
  --blue-950: oklch(0.18 0.054 250);
}
```

---

### Step 5: 대비 비율 검증

#### WCAG 접근성 기준

| Level | 일반 텍스트 | 큰 텍스트 (18pt+) | UI 컴포넌트 |
|-------|-------------|-------------------|-------------|
| AA | 4.5:1 | 3:1 | 3:1 |
| AAA | 7:1 | 4.5:1 | 4.5:1 |

#### 대비 검사 유틸리티

```typescript
// lib/contrast-check.ts

/**
 * oklch 색상의 상대적 휘도 계산
 */
function getRelativeLuminance(oklchColor: string): number {
  // oklch를 RGB로 변환 후 휘도 계산
  // 실제로는 color.js 등의 라이브러리 사용 권장
  const match = oklchColor.match(/oklch\(([\d.]+)\s/);
  if (!match) return 0;
  return parseFloat(match[1]); // 간략화: L값 직접 사용
}

/**
 * 두 색상의 대비 비율 계산
 */
export function getContrastRatio(color1: string, color2: string): number {
  const l1 = getRelativeLuminance(color1);
  const l2 = getRelativeLuminance(color2);
  const lighter = Math.max(l1, l2);
  const darker = Math.min(l1, l2);
  return (lighter + 0.05) / (darker + 0.05);
}

/**
 * WCAG 기준 충족 여부 확인
 */
export function meetsContrastRequirement(
  foreground: string,
  background: string,
  level: 'AA' | 'AAA' = 'AA',
  isLargeText: boolean = false
): boolean {
  const ratio = getContrastRatio(foreground, background);

  if (level === 'AAA') {
    return isLargeText ? ratio >= 4.5 : ratio >= 7;
  }
  return isLargeText ? ratio >= 3 : ratio >= 4.5;
}
```

#### 테스트에서 검증

```typescript
// tests/color-contrast.test.ts
import { describe, it, expect } from 'vitest';
import { meetsContrastRequirement } from '@/lib/contrast-check';

describe('Color Contrast Validation', () => {
  it('primary text on background meets AA standard', () => {
    const foreground = 'oklch(0.145 0 0)';  // --foreground
    const background = 'oklch(1 0 0)';       // --background

    expect(meetsContrastRequirement(foreground, background, 'AA')).toBe(true);
  });

  it('muted text on background meets AA standard', () => {
    const foreground = 'oklch(0.556 0 0)';   // --muted-foreground
    const background = 'oklch(1 0 0)';        // --background

    expect(meetsContrastRequirement(foreground, background, 'AA')).toBe(true);
  });

  it('destructive button text meets AA standard', () => {
    const foreground = 'oklch(0.985 0 0)';          // --destructive-foreground
    const background = 'oklch(0.577 0.245 27.325)'; // --destructive

    expect(meetsContrastRequirement(foreground, background, 'AA')).toBe(true);
  });
});
```

---

### Step 6: Dark Mode 구현

#### Theme Provider 설정

```tsx
// components/theme-provider.tsx
'use client';

import { ThemeProvider as NextThemesProvider } from 'next-themes';

type ThemeProviderProps = React.ComponentProps<typeof NextThemesProvider>;

export function ThemeProvider({ children, ...props }: ThemeProviderProps) {
  return <NextThemesProvider {...props}>{children}</NextThemesProvider>;
}
```

#### Layout 적용

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
      <head>
        {/* FOUC 방지 스크립트 */}
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

#### Theme Toggle 컴포넌트

```tsx
// components/molecules/theme-toggle.tsx
'use client';

import { useTheme } from 'next-themes';
import { useEffect, useState } from 'react';
import { Button } from '@/components/ui/button';
import { Moon, Sun, Monitor } from 'lucide-react';
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuTrigger,
} from '@/components/ui/dropdown-menu';

export function ThemeToggle() {
  const { theme, setTheme } = useTheme();
  const [mounted, setMounted] = useState(false);

  useEffect(() => {
    setMounted(true);
  }, []);

  if (!mounted) {
    return (
      <Button variant="ghost" size="icon" disabled>
        <Sun className="h-5 w-5" />
        <span className="sr-only">테마 변경</span>
      </Button>
    );
  }

  return (
    <DropdownMenu>
      <DropdownMenuTrigger asChild>
        <Button variant="ghost" size="icon">
          <Sun className="h-5 w-5 rotate-0 scale-100 transition-all dark:-rotate-90 dark:scale-0" />
          <Moon className="absolute h-5 w-5 rotate-90 scale-0 transition-all dark:rotate-0 dark:scale-100" />
          <span className="sr-only">테마 변경</span>
        </Button>
      </DropdownMenuTrigger>
      <DropdownMenuContent align="end">
        <DropdownMenuItem onClick={() => setTheme('light')}>
          <Sun className="mr-2 h-4 w-4" />
          라이트
        </DropdownMenuItem>
        <DropdownMenuItem onClick={() => setTheme('dark')}>
          <Moon className="mr-2 h-4 w-4" />
          다크
        </DropdownMenuItem>
        <DropdownMenuItem onClick={() => setTheme('system')}>
          <Monitor className="mr-2 h-4 w-4" />
          시스템
        </DropdownMenuItem>
      </DropdownMenuContent>
    </DropdownMenu>
  );
}
```

---

## 테스트/검증

### 색상 토큰 테스트

```typescript
// tests/colors.test.ts
import { describe, it, expect } from 'vitest';

describe('Color Tokens', () => {
  it('all semantic colors are defined', () => {
    const root = document.documentElement;
    const computedStyle = getComputedStyle(root);

    const requiredColors = [
      '--background',
      '--foreground',
      '--primary',
      '--primary-foreground',
      '--secondary',
      '--secondary-foreground',
      '--muted',
      '--muted-foreground',
      '--accent',
      '--accent-foreground',
      '--destructive',
      '--destructive-foreground',
      '--success',
      '--warning',
      '--info',
      '--border',
      '--input',
      '--ring',
    ];

    requiredColors.forEach((color) => {
      const value = computedStyle.getPropertyValue(color);
      expect(value).not.toBe('');
    });
  });
});
```

### 다크모드 테스트

```tsx
// components/__tests__/theme-toggle.test.tsx
import { render, screen, waitFor } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { ThemeProvider } from 'next-themes';
import { ThemeToggle } from '../molecules/theme-toggle';

const Wrapper = ({ children }: { children: React.ReactNode }) => (
  <ThemeProvider attribute="class" defaultTheme="light" enableSystem={false}>
    {children}
  </ThemeProvider>
);

describe('ThemeToggle', () => {
  it('renders toggle button', async () => {
    render(<ThemeToggle />, { wrapper: Wrapper });

    await waitFor(() => {
      expect(screen.getByRole('button', { name: /테마 변경/i })).toBeInTheDocument();
    });
  });

  it('opens dropdown menu on click', async () => {
    render(<ThemeToggle />, { wrapper: Wrapper });

    await waitFor(() => {
      expect(screen.getByRole('button')).not.toBeDisabled();
    });

    await userEvent.click(screen.getByRole('button'));

    expect(screen.getByText('라이트')).toBeInTheDocument();
    expect(screen.getByText('다크')).toBeInTheDocument();
    expect(screen.getByText('시스템')).toBeInTheDocument();
  });
});
```

### Storybook 시각적 검증

```tsx
// stories/ColorPalette.stories.tsx
import type { Meta, StoryObj } from '@storybook/react';

const ColorSwatch = ({
  name,
  variable
}: {
  name: string;
  variable: string;
}) => (
  <div className="flex items-center gap-4">
    <div
      className="h-12 w-12 rounded-lg border shadow-sm"
      style={{ backgroundColor: `var(${variable})` }}
    />
    <div>
      <p className="font-medium">{name}</p>
      <code className="text-sm text-muted-foreground">{variable}</code>
    </div>
  </div>
);

const meta: Meta = {
  title: 'Design System/Colors',
};

export default meta;

export const SemanticColors: StoryObj = {
  render: () => (
    <div className="grid gap-6 p-6">
      <h2 className="text-xl font-semibold">Semantic Colors</h2>
      <div className="grid grid-cols-2 gap-4">
        <ColorSwatch name="Background" variable="--background" />
        <ColorSwatch name="Foreground" variable="--foreground" />
        <ColorSwatch name="Primary" variable="--primary" />
        <ColorSwatch name="Primary Foreground" variable="--primary-foreground" />
        <ColorSwatch name="Secondary" variable="--secondary" />
        <ColorSwatch name="Muted" variable="--muted" />
        <ColorSwatch name="Accent" variable="--accent" />
        <ColorSwatch name="Destructive" variable="--destructive" />
        <ColorSwatch name="Success" variable="--success" />
        <ColorSwatch name="Warning" variable="--warning" />
        <ColorSwatch name="Info" variable="--info" />
        <ColorSwatch name="Border" variable="--border" />
      </div>
    </div>
  ),
};

export const DarkModeComparison: StoryObj = {
  render: () => (
    <div className="grid grid-cols-2 gap-4">
      <div className="p-6 rounded-lg" style={{ background: 'white' }}>
        <h3 className="font-semibold mb-4">Light Mode</h3>
        {/* Light mode swatches */}
      </div>
      <div className="p-6 rounded-lg dark" style={{ background: '#1a1a1a' }}>
        <h3 className="font-semibold mb-4 text-white">Dark Mode</h3>
        {/* Dark mode swatches */}
      </div>
    </div>
  ),
};
```

---

## 안티패턴

### 1. 시맨틱 토큰 미사용

```tsx
// ❌ Bad: Tailwind 기본 색상 직접 사용
<div className="bg-blue-500 text-white border-gray-200">
  <button className="bg-red-600">Delete</button>
</div>

// ✅ Good: 시맨틱 토큰 사용
<div className="bg-primary text-primary-foreground border-border">
  <button className="bg-destructive text-destructive-foreground">Delete</button>
</div>
```

### 2. 다크모드 색상 수동 지정

```tsx
// ❌ Bad: 각 요소마다 다크모드 색상 지정
<div className="bg-white dark:bg-gray-900 text-black dark:text-white">
  <p className="text-gray-600 dark:text-gray-400">Muted text</p>
</div>

// ✅ Good: CSS 변수로 자동 전환
<div className="bg-background text-foreground">
  <p className="text-muted-foreground">Muted text</p>
</div>
```

### 3. 불투명도로 색상 변형

```css
/* ❌ Bad: 불투명도로 변형 시 겹침 문제 */
.hover-state {
  background: oklch(0.5 0.2 250 / 0.5);  /* 배경색과 섞임 */
}

/* ✅ Good: 별도의 hover 색상 정의 */
.hover-state {
  background: var(--primary-hover);  /* 계산된 색상 */
}
```

### 4. 접근성 미검증

```css
/* ❌ Bad: 대비 비율 검증 없이 사용 */
:root {
  --muted-foreground: oklch(0.75 0 0);  /* 너무 밝아 배경과 대비 부족 */
}

/* ✅ Good: WCAG AA 기준 충족 */
:root {
  --muted-foreground: oklch(0.556 0 0);  /* 4.5:1 대비비 확보 */
}
```

### 5. 하드코딩된 HEX 값

```css
/* ❌ Bad: 유지보수 어려운 HEX 값 */
.button {
  background: #3b82f6;
  border: 1px solid #e5e7eb;
}

/* ✅ Good: CSS 변수 사용 */
.button {
  background: var(--primary);
  border: 1px solid var(--border);
}
```

---

## 성능 고려사항

### CSS 변수 성능

```css
/*
 * CSS 변수는 런타임에 계산되므로 성능에 미미한 영향
 * 하지만 너무 깊은 변수 체이닝은 피하기
 */

/* ❌ 피하기: 깊은 체이닝 */
:root {
  --base: oklch(0.5 0.2 250);
  --primary-base: var(--base);
  --primary: var(--primary-base);
  --button-bg: var(--primary);  /* 4단계 참조 */
}

/* ✅ 권장: 직접 참조 */
:root {
  --primary: oklch(0.5 0.2 250);
  --button-bg: var(--primary);  /* 1단계 참조 */
}
```

### 테마 전환 성능

```tsx
// ThemeProvider 최적화 설정
<ThemeProvider
  attribute="class"
  defaultTheme="system"
  enableSystem
  disableTransitionOnChange  // 전환 시 트랜지션 비활성화
  storageKey="app-theme"     // localStorage 키 커스텀
>
```

---

## 보안 고려사항

### 사용자 입력 색상

```typescript
// ❌ 위험: 사용자 입력을 그대로 CSS에 적용
function UserTheme({ customColor }: { customColor: string }) {
  return <div style={{ background: customColor }} />;  // XSS 가능
}

// ✅ 안전: 색상 값 검증
function UserTheme({ customColor }: { customColor: string }) {
  const safeColor = validateOklchColor(customColor)
    ? customColor
    : 'var(--primary)';
  return <div style={{ background: safeColor }} />;
}

function validateOklchColor(color: string): boolean {
  const pattern = /^oklch\(([\d.]+)\s+([\d.]+)\s+([\d.]+)\)$/;
  return pattern.test(color);
}
```

---

## References

- `_references/COLOR-SYSTEM.md` - oklch 색상 체계 상세 가이드
- `3-direction/` - 디자인 방향 결정 (선행 스킬)
- `4-typography/` - 타이포그래피 시스템 (연계 스킬)
- `7-motion/` - 모션 시스템 (연계 스킬)
