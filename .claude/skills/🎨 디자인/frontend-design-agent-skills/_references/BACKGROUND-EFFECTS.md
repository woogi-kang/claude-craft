# BACKGROUND-EFFECTS.md

배경 효과와 비주얼 이펙트 레시피

---

## 목차

1. [그라데이션 메시](#그라데이션-메시)
2. [노이즈/그레인 필터](#노이즈그레인-필터)
3. [글래스모피즘](#글래스모피즘)
4. [기하학 패턴](#기하학-패턴)
5. [레이어드 배경](#레이어드-배경)
6. [애니메이션 배경](#애니메이션-배경)
7. [Tailwind 유틸리티](#tailwind-유틸리티)

---

## 그라데이션 메시

### 1. CSS Mesh Gradient

```css
/* styles/mesh-gradient.css */

/* Basic mesh gradient */
.mesh-gradient-1 {
  background-color: oklch(95% 0.02 250);
  background-image:
    radial-gradient(at 40% 20%, oklch(85% 0.12 280) 0px, transparent 50%),
    radial-gradient(at 80% 0%, oklch(90% 0.10 200) 0px, transparent 50%),
    radial-gradient(at 0% 50%, oklch(88% 0.08 320) 0px, transparent 50%),
    radial-gradient(at 80% 50%, oklch(92% 0.06 150) 0px, transparent 50%),
    radial-gradient(at 0% 100%, oklch(85% 0.10 250) 0px, transparent 50%),
    radial-gradient(at 80% 100%, oklch(90% 0.08 180) 0px, transparent 50%);
}

/* Dark mode mesh */
.mesh-gradient-dark {
  background-color: oklch(12% 0.02 250);
  background-image:
    radial-gradient(at 40% 20%, oklch(25% 0.08 280) 0px, transparent 50%),
    radial-gradient(at 80% 0%, oklch(20% 0.06 200) 0px, transparent 50%),
    radial-gradient(at 0% 50%, oklch(22% 0.05 320) 0px, transparent 50%),
    radial-gradient(at 80% 50%, oklch(18% 0.04 150) 0px, transparent 50%);
}

/* Vibrant mesh */
.mesh-gradient-vibrant {
  background-color: oklch(20% 0.02 280);
  background-image:
    radial-gradient(at 0% 0%, oklch(50% 0.25 320) 0px, transparent 50%),
    radial-gradient(at 100% 0%, oklch(55% 0.20 250) 0px, transparent 50%),
    radial-gradient(at 100% 100%, oklch(45% 0.22 180) 0px, transparent 50%),
    radial-gradient(at 0% 100%, oklch(50% 0.18 290) 0px, transparent 50%);
}
```

### 2. 메시 그라데이션 컴포넌트

```tsx
// components/ui/mesh-gradient.tsx
'use client';

import { useMemo } from 'react';

interface MeshGradientProps {
  colors?: string[];
  className?: string;
  animate?: boolean;
}

export function MeshGradient({
  colors = [
    'oklch(85% 0.12 280)',
    'oklch(90% 0.10 200)',
    'oklch(88% 0.08 320)',
    'oklch(92% 0.06 150)',
  ],
  className = '',
  animate = false,
}: MeshGradientProps) {
  const gradients = useMemo(() => {
    const positions = [
      { x: 40, y: 20 },
      { x: 80, y: 0 },
      { x: 0, y: 50 },
      { x: 80, y: 50 },
      { x: 0, y: 100 },
      { x: 80, y: 100 },
    ];

    return colors.map((color, i) => {
      const pos = positions[i % positions.length];
      return `radial-gradient(at ${pos.x}% ${pos.y}%, ${color} 0px, transparent 50%)`;
    }).join(', ');
  }, [colors]);

  return (
    <div
      className={`absolute inset-0 ${className}`}
      style={{
        backgroundColor: 'oklch(95% 0.02 250)',
        backgroundImage: gradients,
        animation: animate ? 'meshMove 20s ease-in-out infinite' : undefined,
      }}
    />
  );
}
```

```css
/* Animation keyframes */
@keyframes meshMove {
  0%, 100% {
    background-position: 0% 0%, 100% 0%, 0% 50%, 100% 50%, 0% 100%, 100% 100%;
  }
  25% {
    background-position: 100% 0%, 0% 50%, 50% 0%, 50% 100%, 100% 50%, 0% 50%;
  }
  50% {
    background-position: 50% 100%, 50% 0%, 100% 50%, 0% 0%, 50% 50%, 50% 50%;
  }
  75% {
    background-position: 0% 50%, 100% 100%, 0% 0%, 100% 50%, 50% 0%, 100% 100%;
  }
}
```

### 3. 코닉 그라데이션 메시

```css
/* Conic gradient mesh */
.conic-mesh {
  background:
    conic-gradient(
      from 180deg at 50% 50%,
      oklch(85% 0.12 280) 0deg,
      oklch(90% 0.10 200) 72deg,
      oklch(88% 0.08 320) 144deg,
      oklch(92% 0.06 150) 216deg,
      oklch(85% 0.12 280) 360deg
    );
  filter: blur(100px);
}

/* Multiple conic layers */
.conic-mesh-complex {
  position: relative;
}

.conic-mesh-complex::before,
.conic-mesh-complex::after {
  content: '';
  position: absolute;
  inset: 0;
  background: conic-gradient(
    from 0deg at 30% 30%,
    oklch(85% 0.15 320) 0deg,
    transparent 180deg
  );
}

.conic-mesh-complex::after {
  background: conic-gradient(
    from 180deg at 70% 70%,
    oklch(80% 0.12 200) 0deg,
    transparent 180deg
  );
}
```

---

## 노이즈/그레인 필터

### 4. SVG 노이즈 필터

```tsx
// components/ui/noise-filter.tsx
export function NoiseFilter() {
  return (
    <svg className="hidden">
      <defs>
        {/* Fine grain noise */}
        <filter id="noise-fine">
          <feTurbulence
            type="fractalNoise"
            baseFrequency="0.8"
            numOctaves="4"
            stitchTiles="stitch"
          />
          <feColorMatrix type="saturate" values="0" />
        </filter>

        {/* Coarse grain noise */}
        <filter id="noise-coarse">
          <feTurbulence
            type="fractalNoise"
            baseFrequency="0.4"
            numOctaves="3"
            stitchTiles="stitch"
          />
          <feColorMatrix type="saturate" values="0" />
        </filter>

        {/* Film grain effect */}
        <filter id="noise-film">
          <feTurbulence
            type="fractalNoise"
            baseFrequency="0.65"
            numOctaves="3"
            stitchTiles="stitch"
            result="noise"
          />
          <feColorMatrix
            type="matrix"
            values="1 0 0 0 0
                    0 1 0 0 0
                    0 0 1 0 0
                    0 0 0 15 -7"
            in="noise"
            result="monoNoise"
          />
          <feBlend in="SourceGraphic" in2="monoNoise" mode="multiply" />
        </filter>
      </defs>
    </svg>
  );
}
```

### 5. CSS 노이즈 오버레이

```css
/* styles/noise.css */

/* Noise overlay using SVG data URI */
.noise-overlay {
  position: relative;
}

.noise-overlay::after {
  content: '';
  position: absolute;
  inset: 0;
  background-image: url("data:image/svg+xml,%3Csvg viewBox='0 0 200 200' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='noiseFilter'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.65' numOctaves='3' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23noiseFilter)'/%3E%3C/svg%3E");
  opacity: 0.05;
  pointer-events: none;
  mix-blend-mode: overlay;
}

/* Dark mode noise */
.dark .noise-overlay::after {
  opacity: 0.08;
  mix-blend-mode: soft-light;
}

/* Animated noise */
.noise-animated::after {
  animation: noiseAnimation 0.5s steps(10) infinite;
}

@keyframes noiseAnimation {
  0%, 100% { transform: translate(0, 0); }
  10% { transform: translate(-5%, -10%); }
  20% { transform: translate(-15%, 5%); }
  30% { transform: translate(7%, -15%); }
  40% { transform: translate(-5%, 15%); }
  50% { transform: translate(-15%, 10%); }
  60% { transform: translate(15%, 0); }
  70% { transform: translate(0, 15%); }
  80% { transform: translate(3%, 10%); }
  90% { transform: translate(-10%, 5%); }
}
```

### 6. 노이즈 배경 컴포넌트

```tsx
// components/ui/noise-background.tsx
'use client';

interface NoiseBackgroundProps {
  opacity?: number;
  className?: string;
  blend?: 'overlay' | 'soft-light' | 'multiply' | 'screen';
}

export function NoiseBackground({
  opacity = 0.05,
  className = '',
  blend = 'overlay',
}: NoiseBackgroundProps) {
  // Generate noise SVG data URL
  const noiseSvg = `
    <svg viewBox="0 0 200 200" xmlns="http://www.w3.org/2000/svg">
      <filter id="noiseFilter">
        <feTurbulence
          type="fractalNoise"
          baseFrequency="0.65"
          numOctaves="3"
          stitchTiles="stitch"
        />
      </filter>
      <rect width="100%" height="100%" filter="url(#noiseFilter)"/>
    </svg>
  `;

  const encodedSvg = encodeURIComponent(noiseSvg.trim());

  return (
    <div
      className={`absolute inset-0 pointer-events-none ${className}`}
      style={{
        backgroundImage: `url("data:image/svg+xml,${encodedSvg}")`,
        backgroundRepeat: 'repeat',
        opacity,
        mixBlendMode: blend,
      }}
    />
  );
}
```

### 7. 그레인 텍스처 생성기

```tsx
// lib/generate-noise.ts

/**
 * Generate a noise texture as a canvas data URL
 */
export function generateNoiseTexture(
  width: number = 200,
  height: number = 200,
  opacity: number = 0.1
): string {
  if (typeof window === 'undefined') return '';

  const canvas = document.createElement('canvas');
  canvas.width = width;
  canvas.height = height;

  const ctx = canvas.getContext('2d');
  if (!ctx) return '';

  const imageData = ctx.createImageData(width, height);
  const data = imageData.data;

  for (let i = 0; i < data.length; i += 4) {
    const value = Math.random() * 255;
    data[i] = value;     // R
    data[i + 1] = value; // G
    data[i + 2] = value; // B
    data[i + 3] = opacity * 255; // A
  }

  ctx.putImageData(imageData, 0, 0);
  return canvas.toDataURL('image/png');
}
```

---

## 글래스모피즘

### 8. 기본 글래스 효과

```css
/* styles/glass.css */

/* Basic glassmorphism */
.glass {
  background: oklch(100% 0 0 / 0.7);
  backdrop-filter: blur(16px) saturate(180%);
  -webkit-backdrop-filter: blur(16px) saturate(180%);
  border: 1px solid oklch(100% 0 0 / 0.2);
  border-radius: 1rem;
}

/* Dark glass */
.glass-dark {
  background: oklch(0% 0 0 / 0.5);
  backdrop-filter: blur(16px) saturate(180%);
  -webkit-backdrop-filter: blur(16px) saturate(180%);
  border: 1px solid oklch(100% 0 0 / 0.1);
}

/* Frosted glass (heavier blur) */
.glass-frosted {
  background: oklch(100% 0 0 / 0.5);
  backdrop-filter: blur(40px) saturate(150%);
  -webkit-backdrop-filter: blur(40px) saturate(150%);
  border: 1px solid oklch(100% 0 0 / 0.3);
}

/* Colored glass */
.glass-primary {
  background: oklch(55% 0.15 250 / 0.2);
  backdrop-filter: blur(16px) saturate(180%);
  -webkit-backdrop-filter: blur(16px) saturate(180%);
  border: 1px solid oklch(55% 0.15 250 / 0.3);
}
```

### 9. 글래스 카드 컴포넌트

```tsx
// components/ui/glass-card.tsx
import { ReactNode } from 'react';
import { cn } from '@/lib/utils';

interface GlassCardProps {
  children: ReactNode;
  className?: string;
  blur?: 'sm' | 'md' | 'lg' | 'xl';
  opacity?: number;
  border?: boolean;
}

const blurValues = {
  sm: 'backdrop-blur-sm',
  md: 'backdrop-blur-md',
  lg: 'backdrop-blur-lg',
  xl: 'backdrop-blur-xl',
};

export function GlassCard({
  children,
  className,
  blur = 'lg',
  opacity = 0.7,
  border = true,
}: GlassCardProps) {
  return (
    <div
      className={cn(
        'rounded-2xl',
        blurValues[blur],
        border && 'border border-white/20',
        className
      )}
      style={{
        backgroundColor: `oklch(100% 0 0 / ${opacity})`,
        WebkitBackdropFilter: 'blur(16px) saturate(180%)',
        backdropFilter: 'blur(16px) saturate(180%)',
      }}
    >
      {children}
    </div>
  );
}
```

### 10. 글래스 네비게이션 바

```tsx
// components/ui/glass-navbar.tsx
'use client';

import { motion, useScroll, useTransform } from 'framer-motion';
import Link from 'next/link';

export function GlassNavbar() {
  const { scrollY } = useScroll();
  const opacity = useTransform(scrollY, [0, 100], [0.5, 0.9]);
  const blur = useTransform(scrollY, [0, 100], [8, 20]);

  return (
    <motion.header
      className="fixed top-0 inset-x-0 z-50"
      style={{
        backgroundColor: 'oklch(100% 0 0 / var(--glass-opacity))',
        backdropFilter: `blur(var(--glass-blur))`,
        WebkitBackdropFilter: `blur(var(--glass-blur))`,
        // @ts-ignore - CSS custom properties
        '--glass-opacity': opacity,
        '--glass-blur': blur.get() + 'px',
      }}
    >
      <nav className="container mx-auto px-4 h-16 flex items-center justify-between">
        <Link href="/" className="font-bold text-lg">
          Logo
        </Link>
        <div className="flex items-center gap-6">
          <Link href="/about" className="hover:text-primary transition-colors">
            About
          </Link>
          <Link href="/contact" className="hover:text-primary transition-colors">
            Contact
          </Link>
        </div>
      </nav>
      {/* Bottom border that fades in on scroll */}
      <motion.div
        className="absolute bottom-0 inset-x-0 h-px bg-border"
        style={{ opacity: useTransform(scrollY, [0, 100], [0, 1]) }}
      />
    </motion.header>
  );
}
```

### 11. 글래스 모달

```tsx
// components/ui/glass-modal.tsx
'use client';

import { motion, AnimatePresence } from 'framer-motion';
import { ReactNode } from 'react';
import { X } from 'lucide-react';

interface GlassModalProps {
  isOpen: boolean;
  onClose: () => void;
  children: ReactNode;
}

export function GlassModal({ isOpen, onClose, children }: GlassModalProps) {
  return (
    <AnimatePresence>
      {isOpen && (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4">
          {/* Backdrop with blur */}
          <motion.div
            className="absolute inset-0 bg-black/30 backdrop-blur-sm"
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            onClick={onClose}
          />

          {/* Glass modal */}
          <motion.div
            className="relative max-w-lg w-full rounded-3xl p-6 shadow-2xl"
            initial={{ opacity: 0, scale: 0.9, y: 20 }}
            animate={{ opacity: 1, scale: 1, y: 0 }}
            exit={{ opacity: 0, scale: 0.9, y: 20 }}
            style={{
              background: 'oklch(100% 0 0 / 0.8)',
              backdropFilter: 'blur(24px) saturate(180%)',
              WebkitBackdropFilter: 'blur(24px) saturate(180%)',
              border: '1px solid oklch(100% 0 0 / 0.3)',
            }}
          >
            <button
              onClick={onClose}
              className="absolute top-4 right-4 p-2 rounded-full hover:bg-black/5 transition-colors"
            >
              <X className="w-5 h-5" />
            </button>
            {children}
          </motion.div>
        </div>
      )}
    </AnimatePresence>
  );
}
```

---

## 기하학 패턴

### 12. 도트 그리드

```css
/* styles/patterns.css */

/* Dot grid pattern */
.pattern-dots {
  background-image: radial-gradient(
    oklch(50% 0 0 / 0.15) 1px,
    transparent 1px
  );
  background-size: 20px 20px;
}

/* Dot grid with gradient fade */
.pattern-dots-fade {
  background:
    linear-gradient(
      to bottom,
      transparent,
      oklch(99% 0 0) 80%
    ),
    radial-gradient(
      oklch(50% 0 0 / 0.15) 1px,
      transparent 1px
    );
  background-size: 100% 100%, 20px 20px;
}

/* Dense dots */
.pattern-dots-dense {
  background-image: radial-gradient(
    oklch(50% 0 0 / 0.1) 1px,
    transparent 1px
  );
  background-size: 10px 10px;
}
```

### 13. 그리드 라인

```css
/* Grid lines */
.pattern-grid {
  background-image:
    linear-gradient(oklch(50% 0 0 / 0.1) 1px, transparent 1px),
    linear-gradient(90deg, oklch(50% 0 0 / 0.1) 1px, transparent 1px);
  background-size: 40px 40px;
}

/* Grid with emphasis lines */
.pattern-grid-accent {
  background-image:
    linear-gradient(oklch(50% 0 0 / 0.2) 2px, transparent 2px),
    linear-gradient(90deg, oklch(50% 0 0 / 0.2) 2px, transparent 2px),
    linear-gradient(oklch(50% 0 0 / 0.1) 1px, transparent 1px),
    linear-gradient(90deg, oklch(50% 0 0 / 0.1) 1px, transparent 1px);
  background-size: 100px 100px, 100px 100px, 20px 20px, 20px 20px;
}

/* Isometric grid */
.pattern-isometric {
  background:
    linear-gradient(30deg, oklch(50% 0 0 / 0.1) 12%, transparent 12.5%, transparent 87%, oklch(50% 0 0 / 0.1) 87.5%, oklch(50% 0 0 / 0.1)),
    linear-gradient(150deg, oklch(50% 0 0 / 0.1) 12%, transparent 12.5%, transparent 87%, oklch(50% 0 0 / 0.1) 87.5%, oklch(50% 0 0 / 0.1)),
    linear-gradient(30deg, oklch(50% 0 0 / 0.1) 12%, transparent 12.5%, transparent 87%, oklch(50% 0 0 / 0.1) 87.5%, oklch(50% 0 0 / 0.1)),
    linear-gradient(150deg, oklch(50% 0 0 / 0.1) 12%, transparent 12.5%, transparent 87%, oklch(50% 0 0 / 0.1) 87.5%, oklch(50% 0 0 / 0.1)),
    linear-gradient(60deg, oklch(50% 0 0 / 0.1) 25%, transparent 25.5%, transparent 75%, oklch(50% 0 0 / 0.1) 75%, oklch(50% 0 0 / 0.1)),
    linear-gradient(60deg, oklch(50% 0 0 / 0.1) 25%, transparent 25.5%, transparent 75%, oklch(50% 0 0 / 0.1) 75%, oklch(50% 0 0 / 0.1));
  background-size: 40px 70px;
  background-position: 0 0, 0 0, 20px 35px, 20px 35px, 0 0, 20px 35px;
}
```

### 14. 크로스 해치

```css
/* Cross hatch pattern */
.pattern-crosshatch {
  background:
    repeating-linear-gradient(
      45deg,
      oklch(50% 0 0 / 0.05),
      oklch(50% 0 0 / 0.05) 1px,
      transparent 1px,
      transparent 8px
    ),
    repeating-linear-gradient(
      -45deg,
      oklch(50% 0 0 / 0.05),
      oklch(50% 0 0 / 0.05) 1px,
      transparent 1px,
      transparent 8px
    );
}

/* Diagonal lines */
.pattern-diagonal {
  background: repeating-linear-gradient(
    45deg,
    oklch(50% 0 0 / 0.1),
    oklch(50% 0 0 / 0.1) 1px,
    transparent 1px,
    transparent 10px
  );
}
```

### 15. 헥사곤 패턴

```tsx
// components/ui/hexagon-pattern.tsx
export function HexagonPattern({ className = '' }: { className?: string }) {
  return (
    <svg className={`absolute inset-0 w-full h-full ${className}`}>
      <defs>
        <pattern
          id="hexagons"
          width="50"
          height="43.4"
          patternUnits="userSpaceOnUse"
          patternTransform="scale(2)"
        >
          <polygon
            points="24.8,22 37.3,29.2 37.3,43.7 24.8,50.9 12.3,43.7 12.3,29.2"
            fill="none"
            stroke="currentColor"
            strokeWidth="0.5"
            opacity="0.1"
          />
        </pattern>
      </defs>
      <rect width="100%" height="100%" fill="url(#hexagons)" />
    </svg>
  );
}
```

### 16. 웨이브 패턴

```tsx
// components/ui/wave-pattern.tsx
export function WavePattern({
  className = '',
  color = 'currentColor',
}: {
  className?: string;
  color?: string;
}) {
  return (
    <svg
      className={`absolute inset-0 w-full h-full ${className}`}
      preserveAspectRatio="none"
    >
      <defs>
        <pattern
          id="waves"
          x="0"
          y="0"
          width="100"
          height="20"
          patternUnits="userSpaceOnUse"
        >
          <path
            d="M0 10 Q 25 0, 50 10 T 100 10"
            fill="none"
            stroke={color}
            strokeWidth="0.5"
            opacity="0.15"
          />
        </pattern>
      </defs>
      <rect width="100%" height="100%" fill="url(#waves)" />
    </svg>
  );
}
```

---

## 레이어드 배경

### 17. 멀티 레이어 배경

```tsx
// components/ui/layered-background.tsx
import { ReactNode } from 'react';

interface LayeredBackgroundProps {
  children: ReactNode;
  className?: string;
}

export function LayeredBackground({
  children,
  className = '',
}: LayeredBackgroundProps) {
  return (
    <div className={`relative overflow-hidden ${className}`}>
      {/* Base gradient */}
      <div
        className="absolute inset-0"
        style={{
          background: 'linear-gradient(135deg, oklch(98% 0.02 250), oklch(95% 0.01 200))',
        }}
      />

      {/* Mesh gradient layer */}
      <div
        className="absolute inset-0"
        style={{
          backgroundImage: `
            radial-gradient(at 20% 30%, oklch(85% 0.12 280 / 0.4) 0px, transparent 50%),
            radial-gradient(at 80% 20%, oklch(90% 0.10 200 / 0.3) 0px, transparent 40%),
            radial-gradient(at 60% 80%, oklch(88% 0.08 320 / 0.3) 0px, transparent 50%)
          `,
        }}
      />

      {/* Noise overlay */}
      <div
        className="absolute inset-0 opacity-[0.03] mix-blend-overlay"
        style={{
          backgroundImage: `url("data:image/svg+xml,%3Csvg viewBox='0 0 200 200' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.65'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23n)'/%3E%3C/svg%3E")`,
        }}
      />

      {/* Grid pattern layer */}
      <div
        className="absolute inset-0 opacity-[0.05]"
        style={{
          backgroundImage: `
            linear-gradient(oklch(20% 0 0) 1px, transparent 1px),
            linear-gradient(90deg, oklch(20% 0 0) 1px, transparent 1px)
          `,
          backgroundSize: '40px 40px',
        }}
      />

      {/* Content */}
      <div className="relative z-10">{children}</div>
    </div>
  );
}
```

### 18. 그라데이션 블러 오버레이

```tsx
// components/ui/gradient-blur.tsx
'use client';

import { ReactNode } from 'react';

interface GradientBlurProps {
  children: ReactNode;
  direction?: 'top' | 'bottom' | 'both';
  height?: string;
}

export function GradientBlur({
  children,
  direction = 'bottom',
  height = '200px',
}: GradientBlurProps) {
  return (
    <div className="relative">
      {children}

      {(direction === 'top' || direction === 'both') && (
        <div
          className="absolute top-0 left-0 right-0 pointer-events-none"
          style={{
            height,
            background: 'linear-gradient(to bottom, var(--background), transparent)',
            maskImage: 'linear-gradient(to bottom, black, transparent)',
            WebkitMaskImage: 'linear-gradient(to bottom, black, transparent)',
          }}
        />
      )}

      {(direction === 'bottom' || direction === 'both') && (
        <div
          className="absolute bottom-0 left-0 right-0 pointer-events-none"
          style={{
            height,
            background: 'linear-gradient(to top, var(--background), transparent)',
            maskImage: 'linear-gradient(to top, black, transparent)',
            WebkitMaskImage: 'linear-gradient(to top, black, transparent)',
          }}
        />
      )}
    </div>
  );
}
```

### 19. 스포트라이트 효과

```tsx
// components/ui/spotlight.tsx
'use client';

import { motion, useMotionTemplate, useMotionValue } from 'framer-motion';
import { MouseEvent, ReactNode } from 'react';

interface SpotlightProps {
  children: ReactNode;
  className?: string;
  size?: number;
}

export function Spotlight({
  children,
  className = '',
  size = 400,
}: SpotlightProps) {
  const mouseX = useMotionValue(0);
  const mouseY = useMotionValue(0);

  const handleMouseMove = (e: MouseEvent<HTMLDivElement>) => {
    const rect = e.currentTarget.getBoundingClientRect();
    mouseX.set(e.clientX - rect.left);
    mouseY.set(e.clientY - rect.top);
  };

  const background = useMotionTemplate`
    radial-gradient(
      ${size}px circle at ${mouseX}px ${mouseY}px,
      oklch(55% 0.15 250 / 0.15),
      transparent 80%
    )
  `;

  return (
    <div
      className={`relative overflow-hidden ${className}`}
      onMouseMove={handleMouseMove}
    >
      <motion.div
        className="pointer-events-none absolute inset-0 z-10"
        style={{ background }}
      />
      {children}
    </div>
  );
}
```

### 20. Aurora 배경

```tsx
// components/ui/aurora-background.tsx
'use client';

import { motion } from 'framer-motion';

export function AuroraBackground() {
  return (
    <div className="absolute inset-0 overflow-hidden bg-background">
      {/* Aurora layers */}
      <motion.div
        className="absolute inset-0"
        animate={{
          backgroundPosition: ['0% 50%', '100% 50%', '0% 50%'],
        }}
        transition={{
          duration: 20,
          repeat: Infinity,
          ease: 'linear',
        }}
        style={{
          background: `
            linear-gradient(
              45deg,
              oklch(85% 0.12 280 / 0.3) 0%,
              oklch(90% 0.10 200 / 0.3) 25%,
              oklch(88% 0.08 320 / 0.3) 50%,
              oklch(92% 0.06 150 / 0.3) 75%,
              oklch(85% 0.12 280 / 0.3) 100%
            )
          `,
          backgroundSize: '400% 100%',
          filter: 'blur(100px)',
        }}
      />

      {/* Secondary aurora layer */}
      <motion.div
        className="absolute inset-0"
        animate={{
          backgroundPosition: ['100% 50%', '0% 50%', '100% 50%'],
        }}
        transition={{
          duration: 15,
          repeat: Infinity,
          ease: 'linear',
        }}
        style={{
          background: `
            linear-gradient(
              -45deg,
              oklch(80% 0.10 180 / 0.2) 0%,
              oklch(85% 0.08 250 / 0.2) 50%,
              oklch(80% 0.10 180 / 0.2) 100%
            )
          `,
          backgroundSize: '300% 100%',
          filter: 'blur(80px)',
        }}
      />

      {/* Noise texture */}
      <div
        className="absolute inset-0 opacity-[0.02] mix-blend-overlay"
        style={{
          backgroundImage: `url("data:image/svg+xml,%3Csvg viewBox='0 0 200 200' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.7'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23n)'/%3E%3C/svg%3E")`,
        }}
      />
    </div>
  );
}
```

---

## 애니메이션 배경

### 21. 플로팅 오브

```tsx
// components/ui/floating-orbs.tsx
'use client';

import { motion } from 'framer-motion';

interface Orb {
  id: number;
  size: number;
  x: string;
  y: string;
  color: string;
  duration: number;
}

const orbs: Orb[] = [
  { id: 1, size: 400, x: '20%', y: '20%', color: 'oklch(85% 0.15 280 / 0.4)', duration: 20 },
  { id: 2, size: 300, x: '70%', y: '30%', color: 'oklch(80% 0.12 200 / 0.3)', duration: 25 },
  { id: 3, size: 350, x: '40%', y: '70%', color: 'oklch(85% 0.10 320 / 0.35)', duration: 22 },
  { id: 4, size: 250, x: '80%', y: '80%', color: 'oklch(90% 0.08 150 / 0.25)', duration: 18 },
];

export function FloatingOrbs() {
  return (
    <div className="absolute inset-0 overflow-hidden">
      {orbs.map((orb) => (
        <motion.div
          key={orb.id}
          className="absolute rounded-full"
          style={{
            width: orb.size,
            height: orb.size,
            left: orb.x,
            top: orb.y,
            background: `radial-gradient(circle, ${orb.color}, transparent 70%)`,
            filter: 'blur(60px)',
          }}
          animate={{
            x: [0, 50, -30, 0],
            y: [0, -40, 30, 0],
            scale: [1, 1.1, 0.9, 1],
          }}
          transition={{
            duration: orb.duration,
            repeat: Infinity,
            ease: 'easeInOut',
          }}
        />
      ))}
    </div>
  );
}
```

### 22. 파티클 시스템

```tsx
// components/ui/particles.tsx
'use client';

import { useCallback, useEffect, useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';

interface Particle {
  id: number;
  x: number;
  y: number;
  size: number;
  opacity: number;
}

export function Particles({ count = 50 }: { count?: number }) {
  const [particles, setParticles] = useState<Particle[]>([]);

  const generateParticles = useCallback(() => {
    return Array.from({ length: count }, (_, i) => ({
      id: i,
      x: Math.random() * 100,
      y: Math.random() * 100,
      size: Math.random() * 4 + 1,
      opacity: Math.random() * 0.5 + 0.1,
    }));
  }, [count]);

  useEffect(() => {
    setParticles(generateParticles());
  }, [generateParticles]);

  return (
    <div className="absolute inset-0 overflow-hidden pointer-events-none">
      {particles.map((particle) => (
        <motion.div
          key={particle.id}
          className="absolute rounded-full bg-primary"
          style={{
            width: particle.size,
            height: particle.size,
            left: `${particle.x}%`,
            top: `${particle.y}%`,
          }}
          animate={{
            y: [0, -20, 0],
            opacity: [particle.opacity, particle.opacity * 1.5, particle.opacity],
          }}
          transition={{
            duration: Math.random() * 3 + 2,
            repeat: Infinity,
            ease: 'easeInOut',
            delay: Math.random() * 2,
          }}
        />
      ))}
    </div>
  );
}
```

### 23. 애니메이션 그리드

```tsx
// components/ui/animated-grid.tsx
'use client';

import { motion } from 'framer-motion';
import { useMemo } from 'react';

interface AnimatedGridProps {
  rows?: number;
  cols?: number;
}

export function AnimatedGrid({ rows = 10, cols = 20 }: AnimatedGridProps) {
  const cells = useMemo(() => {
    return Array.from({ length: rows * cols }, (_, i) => ({
      id: i,
      delay: (i % cols) * 0.05 + Math.floor(i / cols) * 0.05,
    }));
  }, [rows, cols]);

  return (
    <div
      className="absolute inset-0 grid"
      style={{
        gridTemplateColumns: `repeat(${cols}, 1fr)`,
        gridTemplateRows: `repeat(${rows}, 1fr)`,
      }}
    >
      {cells.map((cell) => (
        <motion.div
          key={cell.id}
          className="border border-border/10"
          initial={{ opacity: 0 }}
          animate={{ opacity: [0, 0.5, 0] }}
          transition={{
            duration: 4,
            delay: cell.delay,
            repeat: Infinity,
            ease: 'easeInOut',
          }}
        />
      ))}
    </div>
  );
}
```

---

## Tailwind 유틸리티

### Tailwind 설정

```css
/* app/globals.css */
@import "tailwindcss";

@theme {
  /* Background patterns */
  --background-dots: radial-gradient(oklch(50% 0 0 / 0.15) 1px, transparent 1px);
  --background-grid: linear-gradient(oklch(50% 0 0 / 0.1) 1px, transparent 1px),
                     linear-gradient(90deg, oklch(50% 0 0 / 0.1) 1px, transparent 1px);

  /* Blur values */
  --blur-glass: 16px;
  --blur-frosted: 40px;
}

/* Utility classes */
@utility pattern-dots {
  background-image: var(--background-dots);
  background-size: 20px 20px;
}

@utility pattern-grid {
  background-image: var(--background-grid);
  background-size: 40px 40px;
}

@utility glass {
  background: oklch(100% 0 0 / 0.7);
  backdrop-filter: blur(var(--blur-glass)) saturate(180%);
  -webkit-backdrop-filter: blur(var(--blur-glass)) saturate(180%);
}

@utility glass-dark {
  background: oklch(0% 0 0 / 0.5);
  backdrop-filter: blur(var(--blur-glass)) saturate(180%);
  -webkit-backdrop-filter: blur(var(--blur-glass)) saturate(180%);
}

@utility noise {
  position: relative;
}

@utility noise::after {
  content: '';
  position: absolute;
  inset: 0;
  background-image: url("data:image/svg+xml,%3Csvg viewBox='0 0 200 200' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.65'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23n)'/%3E%3C/svg%3E");
  opacity: 0.05;
  pointer-events: none;
  mix-blend-mode: overlay;
}
```

### 사용 예제

```tsx
// Example usage
export function BackgroundDemo() {
  return (
    <div className="min-h-screen relative">
      {/* Mesh gradient base */}
      <div className="absolute inset-0 bg-gradient-to-br from-primary/20 via-background to-secondary/20" />

      {/* Pattern overlay */}
      <div className="absolute inset-0 pattern-dots opacity-50" />

      {/* Noise texture */}
      <div className="absolute inset-0 noise" />

      {/* Glass card */}
      <div className="relative z-10 p-8">
        <div className="glass rounded-2xl p-6 border border-white/20">
          <h1 className="text-2xl font-bold">Glass Card</h1>
          <p className="text-muted-foreground">With backdrop blur effect</p>
        </div>
      </div>
    </div>
  );
}
```
