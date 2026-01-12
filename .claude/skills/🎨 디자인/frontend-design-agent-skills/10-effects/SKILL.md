# Effects Skill

시각적 효과 및 배경 디자인 스킬입니다.
모던 웹 디자인의 Gradient Mesh, Glassmorphism, Neumorphism 등을 구현합니다.

## Triggers

- "효과", "배경", "effects", "background"
- "그라디언트", "글래스모피즘", "뉴모피즘"
- "노이즈", "텍스처", "패턴"
- "애니메이티드 배경"

---

## Input

| 항목 | 필수 | 설명 |
|------|------|------|
| `effectType` | ✅ | 효과 유형 (gradient, glass, neumorphism, noise, pattern, animated) |
| `colorScheme` | ❌ | 색상 구성 (light, dark, brand) |
| `intensity` | ❌ | 효과 강도 (subtle, medium, strong) |
| `performance` | ❌ | 성능 우선순위 (quality, balanced, performance) |

---

## Gradient Mesh Implementation

### CSS Gradient Mesh

```css
/* globals.css - Gradient Mesh 배경 */

/* 1. 기본 Mesh Gradient */
.gradient-mesh {
  background-color: oklch(0.95 0.02 280);
  background-image:
    radial-gradient(at 40% 20%, oklch(0.85 0.15 280) 0px, transparent 50%),
    radial-gradient(at 80% 0%, oklch(0.80 0.12 320) 0px, transparent 50%),
    radial-gradient(at 0% 50%, oklch(0.88 0.10 200) 0px, transparent 50%),
    radial-gradient(at 80% 50%, oklch(0.82 0.14 150) 0px, transparent 50%),
    radial-gradient(at 0% 100%, oklch(0.85 0.12 60) 0px, transparent 50%),
    radial-gradient(at 80% 100%, oklch(0.90 0.08 30) 0px, transparent 50%);
}

/* 2. 다크모드 Mesh Gradient */
.dark .gradient-mesh {
  background-color: oklch(0.15 0.02 280);
  background-image:
    radial-gradient(at 40% 20%, oklch(0.25 0.10 280) 0px, transparent 50%),
    radial-gradient(at 80% 0%, oklch(0.20 0.08 320) 0px, transparent 50%),
    radial-gradient(at 0% 50%, oklch(0.22 0.06 200) 0px, transparent 50%),
    radial-gradient(at 80% 50%, oklch(0.18 0.09 150) 0px, transparent 50%),
    radial-gradient(at 0% 100%, oklch(0.20 0.07 60) 0px, transparent 50%),
    radial-gradient(at 80% 100%, oklch(0.25 0.05 30) 0px, transparent 50%);
}

/* 3. 브랜드 컬러 Mesh */
.gradient-mesh-brand {
  background-color: oklch(0.98 0.01 var(--hue-primary, 250));
  background-image:
    radial-gradient(at 0% 0%, oklch(0.85 0.18 var(--hue-primary, 250)) 0px, transparent 50%),
    radial-gradient(at 100% 0%, oklch(0.80 0.15 calc(var(--hue-primary, 250) + 30)) 0px, transparent 50%),
    radial-gradient(at 100% 100%, oklch(0.75 0.20 calc(var(--hue-primary, 250) - 30)) 0px, transparent 50%),
    radial-gradient(at 0% 100%, oklch(0.82 0.12 calc(var(--hue-primary, 250) + 60)) 0px, transparent 50%);
}
```

### Gradient Mesh 컴포넌트

```tsx
// components/backgrounds/gradient-mesh.tsx
import { cn } from '@/lib/utils';

type MeshPreset = 'aurora' | 'sunset' | 'ocean' | 'forest' | 'candy' | 'monochrome';

interface GradientMeshProps {
  preset?: MeshPreset;
  className?: string;
  children?: React.ReactNode;
  overlay?: boolean;
}

const meshPresets: Record<MeshPreset, string> = {
  aurora: `
    radial-gradient(at 40% 20%, oklch(0.70 0.20 180) 0px, transparent 50%),
    radial-gradient(at 80% 0%, oklch(0.65 0.25 280) 0px, transparent 50%),
    radial-gradient(at 0% 50%, oklch(0.75 0.15 160) 0px, transparent 50%),
    radial-gradient(at 80% 50%, oklch(0.60 0.22 300) 0px, transparent 50%),
    radial-gradient(at 0% 100%, oklch(0.70 0.18 200) 0px, transparent 50%)
  `,
  sunset: `
    radial-gradient(at 0% 0%, oklch(0.70 0.25 30) 0px, transparent 50%),
    radial-gradient(at 100% 0%, oklch(0.65 0.30 350) 0px, transparent 50%),
    radial-gradient(at 50% 50%, oklch(0.75 0.20 50) 0px, transparent 50%),
    radial-gradient(at 100% 100%, oklch(0.60 0.28 320) 0px, transparent 50%)
  `,
  ocean: `
    radial-gradient(at 0% 0%, oklch(0.65 0.15 220) 0px, transparent 50%),
    radial-gradient(at 100% 0%, oklch(0.70 0.20 200) 0px, transparent 50%),
    radial-gradient(at 50% 100%, oklch(0.60 0.18 240) 0px, transparent 50%),
    radial-gradient(at 0% 100%, oklch(0.75 0.12 180) 0px, transparent 50%)
  `,
  forest: `
    radial-gradient(at 20% 20%, oklch(0.60 0.18 140) 0px, transparent 50%),
    radial-gradient(at 80% 0%, oklch(0.55 0.15 120) 0px, transparent 50%),
    radial-gradient(at 0% 80%, oklch(0.65 0.20 160) 0px, transparent 50%),
    radial-gradient(at 100% 100%, oklch(0.50 0.12 100) 0px, transparent 50%)
  `,
  candy: `
    radial-gradient(at 0% 0%, oklch(0.75 0.25 350) 0px, transparent 50%),
    radial-gradient(at 100% 0%, oklch(0.70 0.22 280) 0px, transparent 50%),
    radial-gradient(at 50% 50%, oklch(0.80 0.18 320) 0px, transparent 50%),
    radial-gradient(at 0% 100%, oklch(0.72 0.20 250) 0px, transparent 50%)
  `,
  monochrome: `
    radial-gradient(at 40% 20%, oklch(0.85 0.02 0) 0px, transparent 50%),
    radial-gradient(at 80% 50%, oklch(0.75 0.01 0) 0px, transparent 50%),
    radial-gradient(at 0% 100%, oklch(0.90 0.02 0) 0px, transparent 50%)
  `,
};

export function GradientMesh({
  preset = 'aurora',
  className,
  children,
  overlay = false,
}: GradientMeshProps) {
  return (
    <div
      className={cn('relative', className)}
      style={{
        backgroundImage: meshPresets[preset],
        backgroundColor: 'oklch(0.98 0.01 0)',
      }}
    >
      {overlay && (
        <div
          className="absolute inset-0 bg-background/60 backdrop-blur-[2px]"
          aria-hidden="true"
        />
      )}
      {children && <div className="relative z-10">{children}</div>}
    </div>
  );
}
```

---

## Noise/Grain Texture

### SVG Filter 방식

```tsx
// components/backgrounds/noise-texture.tsx
import { cn } from '@/lib/utils';

interface NoiseTextureProps {
  opacity?: number;
  className?: string;
  children?: React.ReactNode;
}

export function NoiseTexture({
  opacity = 0.05,
  className,
  children,
}: NoiseTextureProps) {
  return (
    <div className={cn('relative', className)}>
      {/* Noise SVG Filter */}
      <svg className="absolute h-0 w-0" aria-hidden="true">
        <filter id="noise-filter">
          <feTurbulence
            type="fractalNoise"
            baseFrequency="0.8"
            numOctaves="4"
            stitchTiles="stitch"
          />
          <feColorMatrix type="saturate" values="0" />
        </filter>
      </svg>

      {/* Noise Overlay */}
      <div
        className="pointer-events-none absolute inset-0 z-10"
        style={{
          filter: 'url(#noise-filter)',
          opacity,
          mixBlendMode: 'overlay',
        }}
        aria-hidden="true"
      />

      {/* Content */}
      <div className="relative z-0">{children}</div>
    </div>
  );
}
```

### CSS Pseudo-element 방식 (성능 최적화)

```css
/* globals.css - Noise 텍스처 */

/* Base64 인코딩된 작은 노이즈 이미지 사용 */
.noise-overlay::before {
  content: '';
  position: absolute;
  inset: 0;
  background-image: url("data:image/svg+xml,%3Csvg viewBox='0 0 256 256' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='noise'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.65' numOctaves='3' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23noise)'/%3E%3C/svg%3E");
  opacity: 0.05;
  pointer-events: none;
  z-index: 1;
}

/* 다크모드에서 노이즈 강도 조절 */
.dark .noise-overlay::before {
  opacity: 0.08;
  mix-blend-mode: soft-light;
}

/* 강도별 변형 */
.noise-subtle::before {
  opacity: 0.03;
}

.noise-medium::before {
  opacity: 0.06;
}

.noise-strong::before {
  opacity: 0.12;
}
```

### Tailwind Plugin 통합

```typescript
// tailwind.config.ts
import type { Config } from 'tailwindcss';
import plugin from 'tailwindcss/plugin';

const config: Config = {
  // ...
  plugins: [
    plugin(function ({ addUtilities }) {
      addUtilities({
        '.noise-bg': {
          position: 'relative',
          '&::before': {
            content: '""',
            position: 'absolute',
            inset: '0',
            backgroundImage: `url("data:image/svg+xml,%3Csvg viewBox='0 0 256 256' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.7' numOctaves='3'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23n)'/%3E%3C/svg%3E")`,
            opacity: '0.05',
            pointerEvents: 'none',
            zIndex: '1',
          },
        },
        '.noise-bg-subtle': {
          '&::before': {
            opacity: '0.03',
          },
        },
        '.noise-bg-medium': {
          '&::before': {
            opacity: '0.06',
          },
        },
        '.noise-bg-strong': {
          '&::before': {
            opacity: '0.1',
          },
        },
      });
    }),
  ],
};

export default config;
```

---

## Glassmorphism

### 기본 Glass 효과

```css
/* globals.css - Glassmorphism */

/* 라이트모드 Glass */
.glass {
  background: oklch(1 0 0 / 0.7);
  backdrop-filter: blur(16px) saturate(180%);
  -webkit-backdrop-filter: blur(16px) saturate(180%);
  border: 1px solid oklch(1 0 0 / 0.3);
}

/* 다크모드 Glass */
.dark .glass {
  background: oklch(0.2 0 0 / 0.6);
  backdrop-filter: blur(16px) saturate(180%);
  -webkit-backdrop-filter: blur(16px) saturate(180%);
  border: 1px solid oklch(1 0 0 / 0.1);
}

/* 강도별 변형 */
.glass-subtle {
  background: oklch(1 0 0 / 0.4);
  backdrop-filter: blur(8px);
  -webkit-backdrop-filter: blur(8px);
}

.glass-medium {
  background: oklch(1 0 0 / 0.6);
  backdrop-filter: blur(12px);
  -webkit-backdrop-filter: blur(12px);
}

.glass-strong {
  background: oklch(1 0 0 / 0.85);
  backdrop-filter: blur(24px) saturate(200%);
  -webkit-backdrop-filter: blur(24px) saturate(200%);
}

/* Colored Glass */
.glass-primary {
  background: oklch(0.6 0.15 250 / 0.2);
  backdrop-filter: blur(16px);
  -webkit-backdrop-filter: blur(16px);
  border: 1px solid oklch(0.6 0.15 250 / 0.3);
}
```

### Glass Card 컴포넌트

```tsx
// components/ui/glass-card.tsx
import { cn } from '@/lib/utils';

interface GlassCardProps extends React.HTMLAttributes<HTMLDivElement> {
  intensity?: 'subtle' | 'medium' | 'strong';
  color?: 'default' | 'primary' | 'gradient';
}

const intensityClasses = {
  subtle: 'bg-white/40 dark:bg-black/30 backdrop-blur-sm',
  medium: 'bg-white/60 dark:bg-black/50 backdrop-blur-md',
  strong: 'bg-white/80 dark:bg-black/70 backdrop-blur-xl',
};

const colorClasses = {
  default: 'border-white/30 dark:border-white/10',
  primary: 'border-primary/30 bg-primary/5',
  gradient: 'border-transparent bg-gradient-to-br from-white/60 to-white/30 dark:from-white/10 dark:to-white/5',
};

export function GlassCard({
  intensity = 'medium',
  color = 'default',
  className,
  children,
  ...props
}: GlassCardProps) {
  return (
    <div
      className={cn(
        'rounded-xl border shadow-lg',
        intensityClasses[intensity],
        colorClasses[color],
        className
      )}
      {...props}
    >
      {children}
    </div>
  );
}
```

### Glass Navbar 예제

```tsx
// components/organisms/glass-navbar.tsx
'use client';

import Link from 'next/link';
import { cn } from '@/lib/utils';

interface GlassNavbarProps {
  logo: React.ReactNode;
  items: { label: string; href: string }[];
  className?: string;
}

export function GlassNavbar({ logo, items, className }: GlassNavbarProps) {
  return (
    <header
      className={cn(
        'fixed top-4 left-1/2 z-50 -translate-x-1/2',
        'w-[calc(100%-2rem)] max-w-4xl',
        'rounded-full px-6 py-3',
        'bg-white/70 dark:bg-black/50',
        'backdrop-blur-lg backdrop-saturate-150',
        'border border-white/20 dark:border-white/10',
        'shadow-lg shadow-black/5',
        className
      )}
    >
      <nav className="flex items-center justify-between">
        <Link href="/" className="font-semibold">
          {logo}
        </Link>
        <ul className="flex items-center gap-6">
          {items.map((item) => (
            <li key={item.href}>
              <Link
                href={item.href}
                className="text-sm font-medium text-foreground/80 transition-colors hover:text-foreground"
              >
                {item.label}
              </Link>
            </li>
          ))}
        </ul>
      </nav>
    </header>
  );
}
```

---

## Neumorphism

### Soft Shadow 효과

```css
/* globals.css - Neumorphism */

/* 라이트모드 Neumorphism */
.neu {
  background: oklch(0.95 0.01 0);
  border-radius: 1rem;
  box-shadow:
    8px 8px 16px oklch(0.85 0.01 0),
    -8px -8px 16px oklch(1 0 0);
}

/* Pressed/Inset 상태 */
.neu-pressed {
  background: oklch(0.95 0.01 0);
  border-radius: 1rem;
  box-shadow:
    inset 4px 4px 8px oklch(0.85 0.01 0),
    inset -4px -4px 8px oklch(1 0 0);
}

/* 다크모드 Neumorphism */
.dark .neu {
  background: oklch(0.20 0.01 0);
  box-shadow:
    8px 8px 16px oklch(0.12 0.01 0),
    -8px -8px 16px oklch(0.28 0.01 0);
}

.dark .neu-pressed {
  background: oklch(0.20 0.01 0);
  box-shadow:
    inset 4px 4px 8px oklch(0.12 0.01 0),
    inset -4px -4px 8px oklch(0.28 0.01 0);
}

/* 크기별 변형 */
.neu-sm {
  box-shadow:
    4px 4px 8px oklch(0.87 0.01 0),
    -4px -4px 8px oklch(1 0 0);
}

.neu-lg {
  box-shadow:
    12px 12px 24px oklch(0.83 0.01 0),
    -12px -12px 24px oklch(1 0 0);
}
```

### Neumorphic Button

```tsx
// components/ui/neu-button.tsx
'use client';

import * as React from 'react';
import { cn } from '@/lib/utils';

interface NeuButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  size?: 'sm' | 'md' | 'lg';
}

export function NeuButton({
  className,
  size = 'md',
  children,
  ...props
}: NeuButtonProps) {
  const [isPressed, setIsPressed] = React.useState(false);

  const sizeClasses = {
    sm: 'px-4 py-2 text-sm',
    md: 'px-6 py-3 text-base',
    lg: 'px-8 py-4 text-lg',
  };

  return (
    <button
      className={cn(
        'rounded-xl font-medium transition-all duration-200',
        'bg-muted text-foreground',
        // Raised state
        !isPressed && [
          'shadow-[6px_6px_12px_rgba(0,0,0,0.1),-6px_-6px_12px_rgba(255,255,255,0.9)]',
          'dark:shadow-[6px_6px_12px_rgba(0,0,0,0.3),-6px_-6px_12px_rgba(255,255,255,0.05)]',
        ],
        // Pressed state
        isPressed && [
          'shadow-[inset_4px_4px_8px_rgba(0,0,0,0.1),inset_-4px_-4px_8px_rgba(255,255,255,0.9)]',
          'dark:shadow-[inset_4px_4px_8px_rgba(0,0,0,0.3),inset_-4px_-4px_8px_rgba(255,255,255,0.05)]',
        ],
        sizeClasses[size],
        className
      )}
      onMouseDown={() => setIsPressed(true)}
      onMouseUp={() => setIsPressed(false)}
      onMouseLeave={() => setIsPressed(false)}
      {...props}
    >
      {children}
    </button>
  );
}
```

---

## Geometric Patterns

### Dot Grid Pattern

```css
/* globals.css - Geometric Patterns */

/* Dot Grid */
.pattern-dots {
  background-image: radial-gradient(
    oklch(0.7 0.01 0) 1px,
    transparent 1px
  );
  background-size: 20px 20px;
}

.dark .pattern-dots {
  background-image: radial-gradient(
    oklch(0.4 0.01 0) 1px,
    transparent 1px
  );
}

/* Grid Lines */
.pattern-grid {
  background-image:
    linear-gradient(to right, oklch(0.9 0 0) 1px, transparent 1px),
    linear-gradient(to bottom, oklch(0.9 0 0) 1px, transparent 1px);
  background-size: 24px 24px;
}

.dark .pattern-grid {
  background-image:
    linear-gradient(to right, oklch(0.25 0 0) 1px, transparent 1px),
    linear-gradient(to bottom, oklch(0.25 0 0) 1px, transparent 1px);
}

/* Cross Pattern */
.pattern-cross {
  background-image:
    linear-gradient(45deg, transparent 45%, oklch(0.85 0 0) 45%, oklch(0.85 0 0) 55%, transparent 55%),
    linear-gradient(-45deg, transparent 45%, oklch(0.85 0 0) 45%, oklch(0.85 0 0) 55%, transparent 55%);
  background-size: 16px 16px;
}

/* Diagonal Lines */
.pattern-diagonal {
  background-image: repeating-linear-gradient(
    45deg,
    transparent,
    transparent 10px,
    oklch(0.9 0 0) 10px,
    oklch(0.9 0 0) 11px
  );
}

/* Hexagon Pattern */
.pattern-hexagon {
  background-color: oklch(0.97 0 0);
  background-image:
    radial-gradient(circle farthest-side at 0% 50%, oklch(0.95 0 0) 23.5%, transparent 24%),
    radial-gradient(circle farthest-side at 0% 50%, oklch(0.92 0 0) 24%, transparent 25%),
    linear-gradient(oklch(0.95 0 0) 14%, transparent 14.5%),
    linear-gradient(oklch(0.95 0 0) 14%, transparent 14.5%);
  background-size: 40px 69.28px;
  background-position: 0 0, 0 0, 20px 34.64px, 0 0;
}
```

### Pattern 컴포넌트

```tsx
// components/backgrounds/pattern-background.tsx
import { cn } from '@/lib/utils';

type PatternType = 'dots' | 'grid' | 'cross' | 'diagonal' | 'hexagon';

interface PatternBackgroundProps {
  pattern: PatternType;
  fade?: 'none' | 'top' | 'bottom' | 'radial';
  className?: string;
  children?: React.ReactNode;
}

const patternClasses: Record<PatternType, string> = {
  dots: 'bg-[radial-gradient(oklch(0.7_0.01_0)_1px,transparent_1px)] dark:bg-[radial-gradient(oklch(0.4_0.01_0)_1px,transparent_1px)] bg-[length:20px_20px]',
  grid: 'bg-[linear-gradient(to_right,oklch(0.9_0_0)_1px,transparent_1px),linear-gradient(to_bottom,oklch(0.9_0_0)_1px,transparent_1px)] dark:bg-[linear-gradient(to_right,oklch(0.25_0_0)_1px,transparent_1px),linear-gradient(to_bottom,oklch(0.25_0_0)_1px,transparent_1px)] bg-[length:24px_24px]',
  cross: 'bg-[linear-gradient(45deg,transparent_45%,oklch(0.85_0_0)_45%,oklch(0.85_0_0)_55%,transparent_55%),linear-gradient(-45deg,transparent_45%,oklch(0.85_0_0)_45%,oklch(0.85_0_0)_55%,transparent_55%)] bg-[length:16px_16px]',
  diagonal: 'bg-[repeating-linear-gradient(45deg,transparent,transparent_10px,oklch(0.9_0_0)_10px,oklch(0.9_0_0)_11px)]',
  hexagon: 'bg-muted',
};

const fadeClasses = {
  none: '',
  top: 'mask-image-[linear-gradient(to_bottom,transparent,black_50%)]',
  bottom: 'mask-image-[linear-gradient(to_top,transparent,black_50%)]',
  radial: 'mask-image-[radial-gradient(ellipse_at_center,black_30%,transparent_70%)]',
};

export function PatternBackground({
  pattern,
  fade = 'none',
  className,
  children,
}: PatternBackgroundProps) {
  return (
    <div className={cn('relative', className)}>
      <div
        className={cn(
          'absolute inset-0 -z-10',
          patternClasses[pattern],
          fade !== 'none' && fadeClasses[fade]
        )}
        aria-hidden="true"
      />
      {children}
    </div>
  );
}
```

---

## Animated Backgrounds

### Floating Orbs

```tsx
// components/backgrounds/floating-orbs.tsx
'use client';

import { motion } from 'framer-motion';
import { cn } from '@/lib/utils';

interface OrbConfig {
  size: number;
  x: string;
  y: string;
  color: string;
  delay: number;
}

interface FloatingOrbsProps {
  orbs?: OrbConfig[];
  className?: string;
  children?: React.ReactNode;
}

const defaultOrbs: OrbConfig[] = [
  { size: 300, x: '10%', y: '20%', color: 'oklch(0.7 0.2 280)', delay: 0 },
  { size: 400, x: '70%', y: '10%', color: 'oklch(0.65 0.18 320)', delay: 0.5 },
  { size: 250, x: '80%', y: '60%', color: 'oklch(0.72 0.15 200)', delay: 1 },
  { size: 350, x: '20%', y: '70%', color: 'oklch(0.68 0.22 150)', delay: 1.5 },
];

export function FloatingOrbs({
  orbs = defaultOrbs,
  className,
  children,
}: FloatingOrbsProps) {
  return (
    <div className={cn('relative overflow-hidden', className)}>
      {/* Orbs */}
      <div className="absolute inset-0 -z-10" aria-hidden="true">
        {orbs.map((orb, index) => (
          <motion.div
            key={index}
            className="absolute rounded-full blur-3xl"
            style={{
              width: orb.size,
              height: orb.size,
              left: orb.x,
              top: orb.y,
              background: orb.color,
              opacity: 0.4,
            }}
            animate={{
              x: [0, 30, -20, 10, 0],
              y: [0, -20, 30, -10, 0],
              scale: [1, 1.1, 0.95, 1.05, 1],
            }}
            transition={{
              duration: 20,
              repeat: Infinity,
              delay: orb.delay,
              ease: 'easeInOut',
            }}
          />
        ))}
      </div>

      {/* Noise overlay for texture */}
      <div
        className="absolute inset-0 -z-5 opacity-[0.03]"
        style={{
          backgroundImage: `url("data:image/svg+xml,%3Csvg viewBox='0 0 256 256' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.7' numOctaves='3'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23n)'/%3E%3C/svg%3E")`,
        }}
        aria-hidden="true"
      />

      {/* Content */}
      <div className="relative z-10">{children}</div>
    </div>
  );
}
```

### Aurora Effect

```tsx
// components/backgrounds/aurora-background.tsx
'use client';

import { motion } from 'framer-motion';
import { cn } from '@/lib/utils';

interface AuroraBackgroundProps {
  className?: string;
  children?: React.ReactNode;
}

export function AuroraBackground({ className, children }: AuroraBackgroundProps) {
  return (
    <div className={cn('relative overflow-hidden bg-background', className)}>
      {/* Aurora Layers */}
      <div className="absolute inset-0 -z-10" aria-hidden="true">
        {/* Layer 1 */}
        <motion.div
          className="absolute inset-0"
          style={{
            background: `
              radial-gradient(ellipse 80% 50% at 50% 0%, oklch(0.7 0.2 280 / 0.3), transparent),
              radial-gradient(ellipse 60% 40% at 70% 20%, oklch(0.65 0.18 320 / 0.25), transparent)
            `,
          }}
          animate={{
            scale: [1, 1.1, 1],
            opacity: [0.3, 0.4, 0.3],
          }}
          transition={{
            duration: 8,
            repeat: Infinity,
            ease: 'easeInOut',
          }}
        />

        {/* Layer 2 */}
        <motion.div
          className="absolute inset-0"
          style={{
            background: `
              radial-gradient(ellipse 70% 60% at 30% 10%, oklch(0.72 0.15 200 / 0.2), transparent),
              radial-gradient(ellipse 50% 30% at 80% 40%, oklch(0.68 0.22 150 / 0.2), transparent)
            `,
          }}
          animate={{
            scale: [1.1, 1, 1.1],
            opacity: [0.25, 0.35, 0.25],
          }}
          transition={{
            duration: 10,
            repeat: Infinity,
            ease: 'easeInOut',
            delay: 2,
          }}
        />
      </div>

      {/* Content */}
      <div className="relative z-10">{children}</div>
    </div>
  );
}
```

---

## Performance Considerations

### 1. GPU 가속 최적화

```css
/* GPU 레이어 생성 */
.gpu-accelerated {
  will-change: transform, opacity;
  transform: translateZ(0);
  backface-visibility: hidden;
}

/* 애니메이션 종료 후 will-change 해제 */
.animation-done {
  will-change: auto;
}
```

### 2. backdrop-filter 조건부 적용

```tsx
// hooks/use-supports-backdrop.ts
'use client';

import { useEffect, useState } from 'react';

export function useSupportsBackdrop() {
  const [supported, setSupported] = useState(true);

  useEffect(() => {
    // backdrop-filter 지원 여부 확인
    setSupported(CSS.supports('backdrop-filter', 'blur(1px)'));
  }, []);

  return supported;
}

// 사용 예시
function GlassComponent() {
  const supportsBackdrop = useSupportsBackdrop();

  return (
    <div
      className={cn(
        'rounded-lg border',
        supportsBackdrop
          ? 'bg-white/60 backdrop-blur-lg'
          : 'bg-white/90' // 폴백: 더 불투명한 배경
      )}
    >
      {/* 내용 */}
    </div>
  );
}
```

### 3. 애니메이션 성능 최적화

```tsx
// Reduced motion 지원
import { useReducedMotion } from 'framer-motion';

function AnimatedBackground() {
  const shouldReduceMotion = useReducedMotion();

  if (shouldReduceMotion) {
    // 정적 배경 반환
    return <div className="bg-gradient-to-br from-primary/10 to-primary/5" />;
  }

  return (
    <motion.div
      animate={{ /* 애니메이션 */ }}
    />
  );
}
```

### 4. Lazy Loading

```tsx
// 뷰포트에 들어올 때만 애니메이션 시작
import { useInView } from 'framer-motion';

function LazyAnimatedSection() {
  const ref = useRef(null);
  const isInView = useInView(ref, { once: true, margin: '-100px' });

  return (
    <motion.section
      ref={ref}
      initial={{ opacity: 0 }}
      animate={isInView ? { opacity: 1 } : {}}
    >
      {/* 무거운 배경 효과 */}
    </motion.section>
  );
}
```

---

## Accessibility Considerations

```tsx
// 1. 배경 요소는 항상 aria-hidden
<div aria-hidden="true" className="absolute inset-0 gradient-mesh" />

// 2. 콘텐츠 가독성 보장
<div className="relative">
  <div aria-hidden="true" className="absolute inset-0 bg-primary/10" />
  {/* 충분한 대비의 콘텐츠 */}
  <div className="relative z-10 text-foreground">
    {children}
  </div>
</div>

// 3. prefers-reduced-motion 존중
@media (prefers-reduced-motion: reduce) {
  .animated-bg {
    animation: none !important;
  }
}
```

---

## Anti-Patterns

### 1. 과도한 blur 사용

```css
/* ❌ Bad: 성능 저하 */
.heavy-blur {
  backdrop-filter: blur(100px);
}

/* ✅ Good: 적절한 blur */
.optimized-blur {
  backdrop-filter: blur(16px);
}
```

### 2. 여러 backdrop-filter 중첩

```tsx
// ❌ Bad: blur 중첩
<div className="backdrop-blur-lg">
  <div className="backdrop-blur-md">
    {/* 성능 문제 */}
  </div>
</div>

// ✅ Good: 단일 레이어
<div className="relative">
  <div className="absolute inset-0 backdrop-blur-lg" aria-hidden="true" />
  <div className="relative z-10">{children}</div>
</div>
```

### 3. 애니메이션 과다 사용

```tsx
// ❌ Bad: 모든 요소 애니메이션
{items.map(item => (
  <motion.div animate={{ y: [0, 10, 0] }} transition={{ repeat: Infinity }}>
    {item}
  </motion.div>
))}

// ✅ Good: 배경만 애니메이션
<FloatingOrbs className="fixed inset-0 -z-10" />
<div className="relative z-10">
  {items.map(item => <div key={item.id}>{item}</div>)}
</div>
```

---

## References

- `_references/BACKGROUND-EFFECTS.md`
- `11-interactions/SKILL.md` (마이크로 인터랙션)
- CSS Tricks - Gradient Mesh: https://css-tricks.com/gradient-mesh/
- Glassmorphism Generator: https://hype4.academy/tools/glassmorphism-generator
