# Interactions Skill

마이크로 인터랙션 및 애니메이션 디자인 스킬입니다.
Framer Motion 기반 hover, tap, focus, loading, scroll 애니메이션을 구현합니다.

## Triggers

- "인터랙션", "마이크로", "interactions", "micro-interactions"
- "hover", "호버", "탭", "tap"
- "포커스", "focus", "로딩", "loading"
- "스크롤 애니메이션", "scroll animation"

---

## Input

| 항목 | 필수 | 설명 |
|------|------|------|
| `interactionType` | ✅ | 인터랙션 유형 (hover, tap, focus, loading, scroll) |
| `intensity` | ❌ | 애니메이션 강도 (subtle, medium, expressive) |
| `duration` | ❌ | 지속 시간 (fast, normal, slow) |
| `easing` | ❌ | 이징 함수 (spring, ease, bounce) |

---

## Framer Motion 기본 설정

### Provider 설정

```tsx
// app/providers.tsx
'use client';

import { LazyMotion, domAnimation } from 'framer-motion';

export function Providers({ children }: { children: React.ReactNode }) {
  return (
    <LazyMotion features={domAnimation}>
      {children}
    </LazyMotion>
  );
}
```

### 공통 애니메이션 Variants

```typescript
// lib/motion/variants.ts
import type { Variants, Transition } from 'framer-motion';

// 기본 트랜지션
export const springTransition: Transition = {
  type: 'spring',
  stiffness: 400,
  damping: 25,
};

export const easeTransition: Transition = {
  type: 'tween',
  duration: 0.2,
  ease: [0.25, 0.1, 0.25, 1],
};

// Hover Variants
export const hoverScale: Variants = {
  initial: { scale: 1 },
  hover: { scale: 1.02 },
  tap: { scale: 0.98 },
};

export const hoverLift: Variants = {
  initial: { y: 0, boxShadow: '0 0 0 rgba(0,0,0,0)' },
  hover: {
    y: -4,
    boxShadow: '0 10px 30px rgba(0,0,0,0.12)',
  },
};

// Fade Variants
export const fadeIn: Variants = {
  initial: { opacity: 0 },
  animate: { opacity: 1 },
  exit: { opacity: 0 },
};

export const fadeInUp: Variants = {
  initial: { opacity: 0, y: 20 },
  animate: { opacity: 1, y: 0 },
  exit: { opacity: 0, y: -20 },
};

export const fadeInDown: Variants = {
  initial: { opacity: 0, y: -20 },
  animate: { opacity: 1, y: 0 },
  exit: { opacity: 0, y: 20 },
};

// Stagger Container
export const staggerContainer: Variants = {
  animate: {
    transition: {
      staggerChildren: 0.1,
    },
  },
};

// Scale Variants
export const scaleIn: Variants = {
  initial: { scale: 0.9, opacity: 0 },
  animate: { scale: 1, opacity: 1 },
  exit: { scale: 0.9, opacity: 0 },
};
```

---

## Hover Effects

### Scale Hover

```tsx
// components/motion/hover-scale.tsx
'use client';

import { motion } from 'framer-motion';
import { cn } from '@/lib/utils';

interface HoverScaleProps {
  children: React.ReactNode;
  scale?: number;
  className?: string;
}

export function HoverScale({
  children,
  scale = 1.02,
  className,
}: HoverScaleProps) {
  return (
    <motion.div
      className={cn('cursor-pointer', className)}
      whileHover={{ scale }}
      whileTap={{ scale: 0.98 }}
      transition={{ type: 'spring', stiffness: 400, damping: 25 }}
    >
      {children}
    </motion.div>
  );
}
```

### Glow Hover

```tsx
// components/motion/hover-glow.tsx
'use client';

import { motion } from 'framer-motion';
import { cn } from '@/lib/utils';

interface HoverGlowProps {
  children: React.ReactNode;
  glowColor?: string;
  className?: string;
}

export function HoverGlow({
  children,
  glowColor = 'oklch(0.6 0.2 250)',
  className,
}: HoverGlowProps) {
  return (
    <motion.div
      className={cn('relative', className)}
      initial="initial"
      whileHover="hover"
    >
      {/* Glow Effect */}
      <motion.div
        className="absolute inset-0 -z-10 rounded-[inherit] blur-xl"
        style={{ background: glowColor }}
        variants={{
          initial: { opacity: 0, scale: 0.8 },
          hover: { opacity: 0.4, scale: 1 },
        }}
        transition={{ duration: 0.3 }}
        aria-hidden="true"
      />
      {children}
    </motion.div>
  );
}
```

### Lift Hover (Shadow)

```tsx
// components/motion/hover-lift.tsx
'use client';

import { motion } from 'framer-motion';
import { cn } from '@/lib/utils';

interface HoverLiftProps {
  children: React.ReactNode;
  lift?: number;
  shadowIntensity?: 'subtle' | 'medium' | 'strong';
  className?: string;
}

const shadowVariants = {
  subtle: {
    initial: '0 1px 2px rgba(0,0,0,0.05)',
    hover: '0 4px 12px rgba(0,0,0,0.1)',
  },
  medium: {
    initial: '0 2px 4px rgba(0,0,0,0.08)',
    hover: '0 8px 24px rgba(0,0,0,0.15)',
  },
  strong: {
    initial: '0 4px 6px rgba(0,0,0,0.1)',
    hover: '0 20px 40px rgba(0,0,0,0.2)',
  },
};

export function HoverLift({
  children,
  lift = 4,
  shadowIntensity = 'medium',
  className,
}: HoverLiftProps) {
  const shadow = shadowVariants[shadowIntensity];

  return (
    <motion.div
      className={cn('cursor-pointer', className)}
      initial={{ y: 0, boxShadow: shadow.initial }}
      whileHover={{ y: -lift, boxShadow: shadow.hover }}
      whileTap={{ y: 0, boxShadow: shadow.initial }}
      transition={{ type: 'spring', stiffness: 400, damping: 25 }}
    >
      {children}
    </motion.div>
  );
}
```

### Border Hover

```tsx
// components/motion/hover-border.tsx
'use client';

import { motion } from 'framer-motion';
import { cn } from '@/lib/utils';

interface HoverBorderProps {
  children: React.ReactNode;
  borderColor?: string;
  className?: string;
}

export function HoverBorder({
  children,
  borderColor = 'hsl(var(--primary))',
  className,
}: HoverBorderProps) {
  return (
    <motion.div
      className={cn(
        'relative overflow-hidden rounded-lg border-2 border-transparent',
        className
      )}
      initial="initial"
      whileHover="hover"
    >
      {/* Animated Border */}
      <motion.div
        className="absolute inset-0 rounded-[inherit]"
        style={{
          border: `2px solid ${borderColor}`,
        }}
        variants={{
          initial: { opacity: 0 },
          hover: { opacity: 1 },
        }}
        transition={{ duration: 0.2 }}
        aria-hidden="true"
      />
      {children}
    </motion.div>
  );
}
```

### Underline Hover (Link)

```tsx
// components/motion/hover-underline.tsx
'use client';

import { motion } from 'framer-motion';
import Link from 'next/link';
import { cn } from '@/lib/utils';

interface HoverUnderlineProps {
  href: string;
  children: React.ReactNode;
  className?: string;
}

export function HoverUnderline({
  href,
  children,
  className,
}: HoverUnderlineProps) {
  return (
    <Link href={href} className={cn('relative inline-block', className)}>
      <motion.span
        className="relative"
        initial="initial"
        whileHover="hover"
      >
        {children}
        <motion.span
          className="absolute bottom-0 left-0 h-0.5 w-full bg-current"
          variants={{
            initial: { scaleX: 0, originX: 0 },
            hover: { scaleX: 1, originX: 0 },
          }}
          transition={{ duration: 0.3, ease: [0.25, 0.1, 0.25, 1] }}
          aria-hidden="true"
        />
      </motion.span>
    </Link>
  );
}
```

---

## Tap/Click Feedback

### Tap Scale

```tsx
// components/motion/tap-scale.tsx
'use client';

import { motion } from 'framer-motion';
import { cn } from '@/lib/utils';

interface TapScaleProps {
  children: React.ReactNode;
  scale?: number;
  className?: string;
  onClick?: () => void;
}

export function TapScale({
  children,
  scale = 0.95,
  className,
  onClick,
}: TapScaleProps) {
  return (
    <motion.div
      className={cn('cursor-pointer select-none', className)}
      whileTap={{ scale }}
      transition={{ type: 'spring', stiffness: 400, damping: 25 }}
      onClick={onClick}
      role="button"
      tabIndex={0}
      onKeyDown={(e) => {
        if (e.key === 'Enter' || e.key === ' ') {
          e.preventDefault();
          onClick?.();
        }
      }}
    >
      {children}
    </motion.div>
  );
}
```

### Ripple Effect

```tsx
// components/motion/ripple.tsx
'use client';

import * as React from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { cn } from '@/lib/utils';

interface RippleProps {
  children: React.ReactNode;
  color?: string;
  className?: string;
}

interface Ripple {
  id: number;
  x: number;
  y: number;
  size: number;
}

export function Ripple({ children, color = 'currentColor', className }: RippleProps) {
  const [ripples, setRipples] = React.useState<Ripple[]>([]);
  const containerRef = React.useRef<HTMLDivElement>(null);

  const createRipple = (e: React.MouseEvent) => {
    const container = containerRef.current;
    if (!container) return;

    const rect = container.getBoundingClientRect();
    const size = Math.max(rect.width, rect.height) * 2;
    const x = e.clientX - rect.left - size / 2;
    const y = e.clientY - rect.top - size / 2;

    const newRipple: Ripple = {
      id: Date.now(),
      x,
      y,
      size,
    };

    setRipples((prev) => [...prev, newRipple]);

    setTimeout(() => {
      setRipples((prev) => prev.filter((r) => r.id !== newRipple.id));
    }, 600);
  };

  return (
    <div
      ref={containerRef}
      className={cn('relative overflow-hidden', className)}
      onMouseDown={createRipple}
    >
      {children}
      <AnimatePresence>
        {ripples.map((ripple) => (
          <motion.span
            key={ripple.id}
            className="absolute pointer-events-none rounded-full"
            style={{
              left: ripple.x,
              top: ripple.y,
              width: ripple.size,
              height: ripple.size,
              backgroundColor: color,
            }}
            initial={{ scale: 0, opacity: 0.3 }}
            animate={{ scale: 1, opacity: 0 }}
            exit={{ opacity: 0 }}
            transition={{ duration: 0.6, ease: 'easeOut' }}
            aria-hidden="true"
          />
        ))}
      </AnimatePresence>
    </div>
  );
}
```

### Button Press Effect

```tsx
// components/ui/animated-button.tsx
'use client';

import { motion } from 'framer-motion';
import { Button, type ButtonProps } from '@/components/ui/button';
import { cn } from '@/lib/utils';

interface AnimatedButtonProps extends ButtonProps {
  haptic?: boolean;
}

export function AnimatedButton({
  className,
  children,
  haptic = true,
  ...props
}: AnimatedButtonProps) {
  const handleTap = () => {
    // 햅틱 피드백 (지원하는 기기에서)
    if (haptic && 'vibrate' in navigator) {
      navigator.vibrate(10);
    }
  };

  return (
    <motion.div
      whileHover={{ scale: 1.02 }}
      whileTap={{ scale: 0.98 }}
      transition={{ type: 'spring', stiffness: 400, damping: 25 }}
      onTap={handleTap}
    >
      <Button className={cn(className)} {...props}>
        {children}
      </Button>
    </motion.div>
  );
}
```

---

## Focus States

### Focus Ring Animation

```tsx
// components/motion/animated-focus.tsx
'use client';

import { motion } from 'framer-motion';
import { cn } from '@/lib/utils';

interface AnimatedFocusProps {
  children: React.ReactNode;
  className?: string;
}

export function AnimatedFocus({ children, className }: AnimatedFocusProps) {
  return (
    <motion.div
      className={cn(
        'relative rounded-md',
        'focus-within:outline-none',
        className
      )}
      initial="initial"
      whileFocus="focus"
    >
      {/* Animated Focus Ring */}
      <motion.div
        className="absolute -inset-1 rounded-lg"
        style={{
          border: '2px solid hsl(var(--ring))',
        }}
        variants={{
          initial: { opacity: 0, scale: 0.95 },
          focus: { opacity: 1, scale: 1 },
        }}
        transition={{ duration: 0.15 }}
        aria-hidden="true"
      />
      {children}
    </motion.div>
  );
}
```

### Focus Outline Pulse

```css
/* globals.css - Focus 애니메이션 */

@keyframes focus-pulse {
  0%, 100% {
    box-shadow: 0 0 0 2px hsl(var(--ring) / 0.5);
  }
  50% {
    box-shadow: 0 0 0 4px hsl(var(--ring) / 0.3);
  }
}

.focus-pulse:focus-visible {
  outline: none;
  animation: focus-pulse 1.5s ease-in-out infinite;
}

/* 접근성: reduced motion 지원 */
@media (prefers-reduced-motion: reduce) {
  .focus-pulse:focus-visible {
    animation: none;
    box-shadow: 0 0 0 2px hsl(var(--ring));
  }
}
```

---

## Loading States

### Loading Spinner Animation

```tsx
// components/motion/animated-spinner.tsx
'use client';

import { motion } from 'framer-motion';
import { cn } from '@/lib/utils';

interface AnimatedSpinnerProps {
  size?: 'sm' | 'md' | 'lg';
  className?: string;
}

const sizeMap = {
  sm: 16,
  md: 24,
  lg: 32,
};

export function AnimatedSpinner({ size = 'md', className }: AnimatedSpinnerProps) {
  const s = sizeMap[size];

  return (
    <motion.svg
      width={s}
      height={s}
      viewBox="0 0 24 24"
      className={cn('text-primary', className)}
      animate={{ rotate: 360 }}
      transition={{
        duration: 1,
        repeat: Infinity,
        ease: 'linear',
      }}
    >
      <circle
        cx="12"
        cy="12"
        r="10"
        stroke="currentColor"
        strokeWidth="3"
        fill="none"
        strokeLinecap="round"
        strokeDasharray="60 40"
      />
    </motion.svg>
  );
}
```

### Skeleton Shimmer

```tsx
// components/motion/skeleton-shimmer.tsx
'use client';

import { motion } from 'framer-motion';
import { cn } from '@/lib/utils';

interface SkeletonShimmerProps {
  className?: string;
  rounded?: 'sm' | 'md' | 'lg' | 'full';
}

export function SkeletonShimmer({
  className,
  rounded = 'md',
}: SkeletonShimmerProps) {
  const roundedClasses = {
    sm: 'rounded-sm',
    md: 'rounded-md',
    lg: 'rounded-lg',
    full: 'rounded-full',
  };

  return (
    <div
      className={cn(
        'relative overflow-hidden bg-muted',
        roundedClasses[rounded],
        className
      )}
    >
      <motion.div
        className="absolute inset-0 -translate-x-full"
        style={{
          background: 'linear-gradient(90deg, transparent, hsl(var(--background) / 0.5), transparent)',
        }}
        animate={{ translateX: '200%' }}
        transition={{
          duration: 1.5,
          repeat: Infinity,
          ease: 'easeInOut',
        }}
        aria-hidden="true"
      />
    </div>
  );
}
```

### Loading Dots

```tsx
// components/motion/loading-dots.tsx
'use client';

import { motion } from 'framer-motion';
import { cn } from '@/lib/utils';

interface LoadingDotsProps {
  size?: number;
  color?: string;
  className?: string;
}

export function LoadingDots({
  size = 8,
  color = 'currentColor',
  className,
}: LoadingDotsProps) {
  const dotVariants = {
    animate: (i: number) => ({
      y: [0, -size, 0],
      transition: {
        duration: 0.6,
        repeat: Infinity,
        delay: i * 0.1,
        ease: 'easeInOut',
      },
    }),
  };

  return (
    <div className={cn('flex items-center gap-1', className)} role="status">
      {[0, 1, 2].map((i) => (
        <motion.span
          key={i}
          className="rounded-full"
          style={{
            width: size,
            height: size,
            backgroundColor: color,
          }}
          custom={i}
          animate="animate"
          variants={dotVariants}
          aria-hidden="true"
        />
      ))}
      <span className="sr-only">로딩 중...</span>
    </div>
  );
}
```

### Success/Error Feedback

```tsx
// components/motion/status-icon.tsx
'use client';

import { motion, AnimatePresence } from 'framer-motion';
import { Check, X, AlertCircle } from 'lucide-react';
import { cn } from '@/lib/utils';

type Status = 'success' | 'error' | 'warning' | 'loading';

interface StatusIconProps {
  status: Status;
  size?: number;
  className?: string;
}

const iconVariants = {
  initial: { scale: 0, opacity: 0 },
  animate: { scale: 1, opacity: 1 },
  exit: { scale: 0, opacity: 0 },
};

const statusConfig = {
  success: {
    icon: Check,
    color: 'text-success bg-success/10',
    checkVariants: {
      initial: { pathLength: 0 },
      animate: { pathLength: 1, transition: { duration: 0.3, delay: 0.2 } },
    },
  },
  error: {
    icon: X,
    color: 'text-destructive bg-destructive/10',
  },
  warning: {
    icon: AlertCircle,
    color: 'text-warning bg-warning/10',
  },
  loading: {
    icon: null,
    color: 'text-primary bg-primary/10',
  },
};

export function StatusIcon({ status, size = 48, className }: StatusIconProps) {
  const config = statusConfig[status];
  const Icon = config.icon;

  return (
    <AnimatePresence mode="wait">
      <motion.div
        key={status}
        className={cn(
          'flex items-center justify-center rounded-full',
          config.color,
          className
        )}
        style={{ width: size, height: size }}
        variants={iconVariants}
        initial="initial"
        animate="animate"
        exit="exit"
        transition={{ type: 'spring', stiffness: 500, damping: 30 }}
      >
        {status === 'loading' ? (
          <motion.div
            className="rounded-full border-2 border-current border-t-transparent"
            style={{ width: size * 0.5, height: size * 0.5 }}
            animate={{ rotate: 360 }}
            transition={{ duration: 1, repeat: Infinity, ease: 'linear' }}
          />
        ) : Icon ? (
          <Icon size={size * 0.5} />
        ) : null}
      </motion.div>
    </AnimatePresence>
  );
}
```

---

## Scroll-Triggered Animations

### Fade In On Scroll

```tsx
// components/motion/fade-in-on-scroll.tsx
'use client';

import { motion, useInView } from 'framer-motion';
import { useRef } from 'react';
import { cn } from '@/lib/utils';

interface FadeInOnScrollProps {
  children: React.ReactNode;
  direction?: 'up' | 'down' | 'left' | 'right';
  delay?: number;
  duration?: number;
  once?: boolean;
  className?: string;
}

const directionOffset = {
  up: { y: 40 },
  down: { y: -40 },
  left: { x: 40 },
  right: { x: -40 },
};

export function FadeInOnScroll({
  children,
  direction = 'up',
  delay = 0,
  duration = 0.5,
  once = true,
  className,
}: FadeInOnScrollProps) {
  const ref = useRef(null);
  const isInView = useInView(ref, { once, margin: '-100px' });

  const offset = directionOffset[direction];

  return (
    <motion.div
      ref={ref}
      className={className}
      initial={{ opacity: 0, ...offset }}
      animate={isInView ? { opacity: 1, x: 0, y: 0 } : {}}
      transition={{
        duration,
        delay,
        ease: [0.25, 0.1, 0.25, 1],
      }}
    >
      {children}
    </motion.div>
  );
}
```

### Stagger Children On Scroll

```tsx
// components/motion/stagger-on-scroll.tsx
'use client';

import { motion, useInView } from 'framer-motion';
import { useRef } from 'react';
import { cn } from '@/lib/utils';

interface StaggerOnScrollProps {
  children: React.ReactNode;
  staggerDelay?: number;
  once?: boolean;
  className?: string;
}

export function StaggerOnScroll({
  children,
  staggerDelay = 0.1,
  once = true,
  className,
}: StaggerOnScrollProps) {
  const ref = useRef(null);
  const isInView = useInView(ref, { once, margin: '-50px' });

  const containerVariants = {
    hidden: { opacity: 0 },
    visible: {
      opacity: 1,
      transition: {
        staggerChildren: staggerDelay,
      },
    },
  };

  const itemVariants = {
    hidden: { opacity: 0, y: 20 },
    visible: {
      opacity: 1,
      y: 0,
      transition: {
        duration: 0.5,
        ease: [0.25, 0.1, 0.25, 1],
      },
    },
  };

  return (
    <motion.div
      ref={ref}
      className={cn(className)}
      variants={containerVariants}
      initial="hidden"
      animate={isInView ? 'visible' : 'hidden'}
    >
      {Array.isArray(children)
        ? children.map((child, index) => (
            <motion.div key={index} variants={itemVariants}>
              {child}
            </motion.div>
          ))
        : children}
    </motion.div>
  );
}
```

### Parallax Effect

```tsx
// components/motion/parallax.tsx
'use client';

import { motion, useScroll, useTransform } from 'framer-motion';
import { useRef } from 'react';
import { cn } from '@/lib/utils';

interface ParallaxProps {
  children: React.ReactNode;
  speed?: number; // -1 to 1, negative = opposite direction
  className?: string;
}

export function Parallax({ children, speed = 0.5, className }: ParallaxProps) {
  const ref = useRef(null);
  const { scrollYProgress } = useScroll({
    target: ref,
    offset: ['start end', 'end start'],
  });

  const y = useTransform(scrollYProgress, [0, 1], ['0%', `${speed * 100}%`]);

  return (
    <motion.div ref={ref} className={cn('will-change-transform', className)} style={{ y }}>
      {children}
    </motion.div>
  );
}
```

### Reveal On Scroll

```tsx
// components/motion/reveal-on-scroll.tsx
'use client';

import { motion, useInView } from 'framer-motion';
import { useRef } from 'react';
import { cn } from '@/lib/utils';

interface RevealOnScrollProps {
  children: React.ReactNode;
  width?: 'fit-content' | '100%';
  once?: boolean;
  className?: string;
}

export function RevealOnScroll({
  children,
  width = 'fit-content',
  once = true,
  className,
}: RevealOnScrollProps) {
  const ref = useRef(null);
  const isInView = useInView(ref, { once, margin: '-100px' });

  return (
    <div
      ref={ref}
      className={cn('relative overflow-hidden', className)}
      style={{ width }}
    >
      <motion.div
        initial={{ opacity: 0, y: 75 }}
        animate={isInView ? { opacity: 1, y: 0 } : {}}
        transition={{ duration: 0.5, ease: [0.25, 0.1, 0.25, 1] }}
      >
        {children}
      </motion.div>
      {/* Reveal overlay */}
      <motion.div
        className="absolute inset-0 bg-primary z-20"
        initial={{ left: 0 }}
        animate={isInView ? { left: '100%' } : {}}
        transition={{ duration: 0.5, ease: [0.25, 0.1, 0.25, 1] }}
        aria-hidden="true"
      />
    </div>
  );
}
```

---

## Accessibility Considerations

### Reduced Motion 지원

```tsx
// hooks/use-reduced-motion.ts
'use client';

import { useReducedMotion } from 'framer-motion';

export { useReducedMotion };

// 사용 예시
function AnimatedComponent() {
  const shouldReduceMotion = useReducedMotion();

  return (
    <motion.div
      animate={shouldReduceMotion ? {} : { y: [0, 10, 0] }}
      transition={shouldReduceMotion ? {} : { repeat: Infinity }}
    >
      Content
    </motion.div>
  );
}
```

### 안전한 애니메이션 래퍼

```tsx
// components/motion/safe-motion.tsx
'use client';

import { motion, useReducedMotion } from 'framer-motion';
import type { MotionProps, HTMLMotionProps } from 'framer-motion';

type SafeMotionProps<T extends keyof JSX.IntrinsicElements> = HTMLMotionProps<T> & {
  fallback?: React.ReactNode;
};

export function SafeMotion<T extends keyof JSX.IntrinsicElements>({
  children,
  fallback,
  animate,
  whileHover,
  whileTap,
  whileFocus,
  transition,
  ...props
}: SafeMotionProps<T>) {
  const shouldReduceMotion = useReducedMotion();

  if (shouldReduceMotion) {
    // 애니메이션 비활성화
    return (
      <motion.div {...props}>
        {fallback || children}
      </motion.div>
    );
  }

  return (
    <motion.div
      animate={animate}
      whileHover={whileHover}
      whileTap={whileTap}
      whileFocus={whileFocus}
      transition={transition}
      {...props}
    >
      {children}
    </motion.div>
  );
}
```

### 포커스 관리

```tsx
// Focus trap for modals/menus
import { FocusTrap } from '@radix-ui/react-focus-scope';

function AnimatedModal({ open, children }) {
  return (
    <AnimatePresence>
      {open && (
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          exit={{ opacity: 0 }}
        >
          <FocusTrap>
            {children}
          </FocusTrap>
        </motion.div>
      )}
    </AnimatePresence>
  );
}
```

---

## Performance Best Practices

### 1. GPU 가속 속성만 애니메이션

```tsx
// ✅ Good: transform, opacity만 애니메이션
<motion.div
  animate={{ x: 100, opacity: 0.5 }}
/>

// ❌ Bad: width, height, color 애니메이션
<motion.div
  animate={{ width: '100%', backgroundColor: 'red' }}
/>
```

### 2. Layout 애니메이션 최적화

```tsx
// layoutId로 자연스러운 레이아웃 전환
<motion.div layoutId="shared-element">
  {isExpanded ? <ExpandedContent /> : <CollapsedContent />}
</motion.div>

// layout="position"으로 위치만 애니메이션
<motion.div layout="position">
  {/* 크기는 즉시 변경, 위치만 애니메이션 */}
</motion.div>
```

### 3. 대량 요소 최적화

```tsx
// AnimatePresence mode="popLayout"으로 리스트 최적화
<AnimatePresence mode="popLayout">
  {items.map((item) => (
    <motion.li
      key={item.id}
      layout
      initial={{ opacity: 0, scale: 0.8 }}
      animate={{ opacity: 1, scale: 1 }}
      exit={{ opacity: 0, scale: 0.8 }}
    >
      {item.content}
    </motion.li>
  ))}
</AnimatePresence>
```

---

## Anti-Patterns

### 1. 과도한 애니메이션

```tsx
// ❌ Bad: 모든 요소에 애니메이션
{items.map(item => (
  <motion.div
    whileHover={{ scale: 1.1, rotate: 5, backgroundColor: '#f00' }}
    transition={{ duration: 0.5 }}
  >
    {item}
  </motion.div>
))}

// ✅ Good: 핵심 요소에만 미묘한 애니메이션
<motion.div whileHover={{ scale: 1.02 }}>
  {items.map(item => <div key={item.id}>{item}</div>)}
</motion.div>
```

### 2. 느린 트랜지션

```tsx
// ❌ Bad: 너무 느린 애니메이션
<motion.div transition={{ duration: 2 }} />

// ✅ Good: 빠른 피드백 (200-500ms)
<motion.div transition={{ duration: 0.2 }} />
```

### 3. 레이아웃 트리거

```tsx
// ❌ Bad: width/height 애니메이션
<motion.div animate={{ width: open ? '100%' : '0%' }} />

// ✅ Good: transform으로 대체
<motion.div animate={{ scaleX: open ? 1 : 0 }} />
```

### 4. Reduced Motion 무시

```tsx
// ❌ Bad: 항상 애니메이션
<motion.div animate={{ y: [0, 10, 0] }} transition={{ repeat: Infinity }} />

// ✅ Good: 사용자 설정 존중
const shouldReduceMotion = useReducedMotion();
<motion.div
  animate={shouldReduceMotion ? {} : { y: [0, 10, 0] }}
  transition={shouldReduceMotion ? {} : { repeat: Infinity }}
/>
```

---

## References

- `_references/MOTION-PATTERNS.md`
- `10-effects/SKILL.md` (시각적 효과)
- Framer Motion 공식 문서: https://www.framer.com/motion/
- 접근성 가이드: https://www.w3.org/WAI/WCAG21/Understanding/animation-from-interactions.html
