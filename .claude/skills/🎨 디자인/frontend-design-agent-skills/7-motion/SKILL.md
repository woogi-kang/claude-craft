# Motion Skill

프로젝트의 애니메이션 시스템과 모션 언어를 구성합니다.

## Triggers

- "모션", "애니메이션", "motion", "animation", "트랜지션", "transition", "인터랙션"

---

## Input

| 항목 | 필수 | 설명 |
|------|------|------|
| `aestheticDirection` | ✅ | 디자인 방향 (minimal, bold, playful 등) |
| `motionIntensity` | ❌ | 모션 강도 (subtle, moderate, expressive) - 기본값: moderate |
| `reducedMotionSupport` | ❌ | prefers-reduced-motion 지원 여부 - 기본값: true |

---

## Output

| 산출물 | 설명 |
|--------|------|
| `motion-tokens.css` | CSS 변수로 정의된 모션 토큰 |
| `motion-variants.ts` | Framer Motion variants 프리셋 |
| `globals.css` 업데이트 | Tailwind @theme 및 tw-animate-css 통합 |

---

## Workflow

### Step 1: 모션 원칙 정립

**디자인 방향별 모션 성격:**

| Direction | 모션 성격 | Duration | Easing | 특징 |
|-----------|----------|----------|--------|------|
| **Minimal** | 절제된 | Short (150-200ms) | ease-out | 미세한 피드백 |
| **Elegant** | 우아한 | Medium (300-400ms) | ease-in-out | 부드러운 흐름 |
| **Bold** | 역동적 | Short (100-150ms) | ease-out | 즉각적, 강렬함 |
| **Playful** | 활발한 | Variable | spring | 튀는 느낌 |
| **Technical** | 정밀한 | Short (100-200ms) | linear/ease-out | 기계적, 정확함 |
| **Luxury** | 고급스러운 | Long (400-600ms) | cubic-bezier | 여유로운 전환 |
| **Organic** | 자연스러운 | Medium (250-350ms) | spring | 물리적 느낌 |

---

### Step 2: Duration 토큰 정의

```css
/* app/globals.css - Motion tokens */
:root {
  /* =========================================
   * Duration Scale
   * ========================================= */

  /* Instant - No perception of delay */
  --duration-instant: 0ms;

  /* Fast - Micro-interactions, tooltips */
  --duration-fast: 150ms;

  /* Normal - Standard transitions */
  --duration-normal: 300ms;

  /* Slow - Complex animations, overlays */
  --duration-slow: 500ms;

  /* Slower - Dramatic reveals, page transitions */
  --duration-slower: 700ms;

  /* Slowest - Cinematic effects */
  --duration-slowest: 1000ms;

  /* =========================================
   * Semantic Duration Aliases
   * ========================================= */

  /* UI Feedback */
  --duration-button: var(--duration-fast);
  --duration-hover: var(--duration-fast);
  --duration-focus: var(--duration-fast);

  /* Overlays & Modals */
  --duration-modal: var(--duration-normal);
  --duration-drawer: var(--duration-slow);
  --duration-toast: var(--duration-normal);

  /* Page Transitions */
  --duration-page-enter: var(--duration-slow);
  --duration-page-exit: var(--duration-normal);

  /* Content */
  --duration-fade: var(--duration-normal);
  --duration-slide: var(--duration-normal);
  --duration-collapse: var(--duration-normal);
}
```

---

### Step 3: Easing 함수 정의

```css
/* app/globals.css - Easing curves */
:root {
  /* =========================================
   * Standard Easing Curves
   * ========================================= */

  /* Linear - Constant speed */
  --ease-linear: linear;

  /* Ease Out - Fast start, slow end (entering) */
  --ease-out: cubic-bezier(0, 0, 0.2, 1);

  /* Ease In - Slow start, fast end (exiting) */
  --ease-in: cubic-bezier(0.4, 0, 1, 1);

  /* Ease In-Out - Slow both ends */
  --ease-in-out: cubic-bezier(0.4, 0, 0.2, 1);

  /* =========================================
   * Custom Easing Curves
   * ========================================= */

  /* Smooth - Very subtle ease */
  --ease-smooth: cubic-bezier(0.25, 0.1, 0.25, 1);

  /* Bounce - Playful overshoot */
  --ease-bounce: cubic-bezier(0.34, 1.56, 0.64, 1);

  /* Elastic - Springy return */
  --ease-elastic: cubic-bezier(0.68, -0.55, 0.265, 1.55);

  /* Anticipate - Pull back before action */
  --ease-anticipate: cubic-bezier(0.38, -0.4, 0.88, 0.65);

  /* Overshoot - Goes past target */
  --ease-overshoot: cubic-bezier(0.34, 1.3, 0.64, 1);

  /* Snap - Quick with sudden stop */
  --ease-snap: cubic-bezier(0.2, 0.8, 0.2, 1);

  /* =========================================
   * Semantic Easing Aliases
   * ========================================= */

  /* Default for most transitions */
  --ease-default: var(--ease-out);

  /* Enter animations (appearing) */
  --ease-enter: var(--ease-out);

  /* Exit animations (disappearing) */
  --ease-exit: var(--ease-in);

  /* Hover/Focus states */
  --ease-interactive: var(--ease-out);

  /* Modal/Overlay */
  --ease-modal: var(--ease-smooth);
}
```

---

### Step 4: Framer Motion Variants 설정

#### 기본 variants 프리셋

```typescript
// lib/motion/variants.ts
import { type Variants } from 'framer-motion';

// =========================================
// Fade Variants
// =========================================

export const fadeVariants: Variants = {
  hidden: {
    opacity: 0,
  },
  visible: {
    opacity: 1,
    transition: {
      duration: 0.3,
      ease: [0, 0, 0.2, 1],  // ease-out
    },
  },
  exit: {
    opacity: 0,
    transition: {
      duration: 0.2,
      ease: [0.4, 0, 1, 1],  // ease-in
    },
  },
};

// =========================================
// Slide Variants
// =========================================

export const slideUpVariants: Variants = {
  hidden: {
    opacity: 0,
    y: 20,
  },
  visible: {
    opacity: 1,
    y: 0,
    transition: {
      duration: 0.3,
      ease: [0, 0, 0.2, 1],
    },
  },
  exit: {
    opacity: 0,
    y: -10,
    transition: {
      duration: 0.2,
      ease: [0.4, 0, 1, 1],
    },
  },
};

export const slideDownVariants: Variants = {
  hidden: {
    opacity: 0,
    y: -20,
  },
  visible: {
    opacity: 1,
    y: 0,
    transition: {
      duration: 0.3,
      ease: [0, 0, 0.2, 1],
    },
  },
  exit: {
    opacity: 0,
    y: 10,
    transition: {
      duration: 0.2,
      ease: [0.4, 0, 1, 1],
    },
  },
};

export const slideLeftVariants: Variants = {
  hidden: {
    opacity: 0,
    x: 20,
  },
  visible: {
    opacity: 1,
    x: 0,
    transition: {
      duration: 0.3,
      ease: [0, 0, 0.2, 1],
    },
  },
  exit: {
    opacity: 0,
    x: -20,
    transition: {
      duration: 0.2,
      ease: [0.4, 0, 1, 1],
    },
  },
};

export const slideRightVariants: Variants = {
  hidden: {
    opacity: 0,
    x: -20,
  },
  visible: {
    opacity: 1,
    x: 0,
    transition: {
      duration: 0.3,
      ease: [0, 0, 0.2, 1],
    },
  },
  exit: {
    opacity: 0,
    x: 20,
    transition: {
      duration: 0.2,
      ease: [0.4, 0, 1, 1],
    },
  },
};

// =========================================
// Scale Variants
// =========================================

export const scaleVariants: Variants = {
  hidden: {
    opacity: 0,
    scale: 0.95,
  },
  visible: {
    opacity: 1,
    scale: 1,
    transition: {
      duration: 0.3,
      ease: [0, 0, 0.2, 1],
    },
  },
  exit: {
    opacity: 0,
    scale: 0.95,
    transition: {
      duration: 0.2,
      ease: [0.4, 0, 1, 1],
    },
  },
};

export const popVariants: Variants = {
  hidden: {
    opacity: 0,
    scale: 0.8,
  },
  visible: {
    opacity: 1,
    scale: 1,
    transition: {
      type: 'spring',
      damping: 25,
      stiffness: 400,
    },
  },
  exit: {
    opacity: 0,
    scale: 0.9,
    transition: {
      duration: 0.15,
    },
  },
};

// =========================================
// Stagger Container Variants
// =========================================

export const staggerContainerVariants: Variants = {
  hidden: {
    opacity: 0,
  },
  visible: {
    opacity: 1,
    transition: {
      staggerChildren: 0.1,
      delayChildren: 0.1,
    },
  },
  exit: {
    opacity: 0,
    transition: {
      staggerChildren: 0.05,
      staggerDirection: -1,
    },
  },
};

export const staggerItemVariants: Variants = {
  hidden: {
    opacity: 0,
    y: 20,
  },
  visible: {
    opacity: 1,
    y: 0,
    transition: {
      duration: 0.3,
      ease: [0, 0, 0.2, 1],
    },
  },
  exit: {
    opacity: 0,
    y: -10,
  },
};

// =========================================
// Modal/Dialog Variants
// =========================================

export const modalOverlayVariants: Variants = {
  hidden: {
    opacity: 0,
  },
  visible: {
    opacity: 1,
    transition: {
      duration: 0.2,
    },
  },
  exit: {
    opacity: 0,
    transition: {
      duration: 0.15,
      delay: 0.1,
    },
  },
};

export const modalContentVariants: Variants = {
  hidden: {
    opacity: 0,
    scale: 0.96,
    y: 10,
  },
  visible: {
    opacity: 1,
    scale: 1,
    y: 0,
    transition: {
      type: 'spring',
      damping: 30,
      stiffness: 400,
    },
  },
  exit: {
    opacity: 0,
    scale: 0.96,
    transition: {
      duration: 0.15,
    },
  },
};

// =========================================
// Drawer Variants
// =========================================

export const drawerVariants = {
  left: {
    hidden: { x: '-100%' },
    visible: {
      x: 0,
      transition: { type: 'spring', damping: 30, stiffness: 300 },
    },
    exit: { x: '-100%', transition: { duration: 0.2 } },
  },
  right: {
    hidden: { x: '100%' },
    visible: {
      x: 0,
      transition: { type: 'spring', damping: 30, stiffness: 300 },
    },
    exit: { x: '100%', transition: { duration: 0.2 } },
  },
  top: {
    hidden: { y: '-100%' },
    visible: {
      y: 0,
      transition: { type: 'spring', damping: 30, stiffness: 300 },
    },
    exit: { y: '-100%', transition: { duration: 0.2 } },
  },
  bottom: {
    hidden: { y: '100%' },
    visible: {
      y: 0,
      transition: { type: 'spring', damping: 30, stiffness: 300 },
    },
    exit: { y: '100%', transition: { duration: 0.2 } },
  },
} satisfies Record<string, Variants>;
```

#### Spring 설정 프리셋

```typescript
// lib/motion/springs.ts

// =========================================
// Spring Configurations
// =========================================

export const springs = {
  // Responsive - Quick response, moderate bounce
  responsive: {
    type: 'spring' as const,
    stiffness: 400,
    damping: 30,
  },

  // Gentle - Soft and slow
  gentle: {
    type: 'spring' as const,
    stiffness: 150,
    damping: 20,
  },

  // Bouncy - Playful with overshoot
  bouncy: {
    type: 'spring' as const,
    stiffness: 500,
    damping: 15,
  },

  // Stiff - Almost no bounce
  stiff: {
    type: 'spring' as const,
    stiffness: 700,
    damping: 40,
  },

  // Wobbly - Lots of bounce
  wobbly: {
    type: 'spring' as const,
    stiffness: 180,
    damping: 12,
  },
} as const;
```

---

### Step 5: tw-animate-css 설정

```css
/* app/globals.css */
@import "tailwindcss";
@import "tw-animate-css";

/* =========================================
 * Custom Animation Classes
 * ========================================= */

@layer utilities {
  /* Fade animations */
  .animate-fade-in {
    animation: fade-in var(--duration-normal) var(--ease-out) forwards;
  }

  .animate-fade-out {
    animation: fade-out var(--duration-fast) var(--ease-in) forwards;
  }

  /* Slide animations */
  .animate-slide-up {
    animation: slide-up var(--duration-normal) var(--ease-out) forwards;
  }

  .animate-slide-down {
    animation: slide-down var(--duration-normal) var(--ease-out) forwards;
  }

  .animate-slide-left {
    animation: slide-left var(--duration-normal) var(--ease-out) forwards;
  }

  .animate-slide-right {
    animation: slide-right var(--duration-normal) var(--ease-out) forwards;
  }

  /* Scale animations */
  .animate-scale-in {
    animation: scale-in var(--duration-normal) var(--ease-out) forwards;
  }

  .animate-pop {
    animation: pop var(--duration-normal) var(--ease-bounce) forwards;
  }

  /* Spin - for loading indicators */
  .animate-spin-slow {
    animation: spin 2s linear infinite;
  }

  /* Pulse - for attention */
  .animate-pulse-subtle {
    animation: pulse 2s ease-in-out infinite;
  }
}

/* =========================================
 * Keyframe Definitions
 * ========================================= */

@keyframes fade-in {
  from { opacity: 0; }
  to { opacity: 1; }
}

@keyframes fade-out {
  from { opacity: 1; }
  to { opacity: 0; }
}

@keyframes slide-up {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

@keyframes slide-down {
  from {
    opacity: 0;
    transform: translateY(-20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

@keyframes slide-left {
  from {
    opacity: 0;
    transform: translateX(20px);
  }
  to {
    opacity: 1;
    transform: translateX(0);
  }
}

@keyframes slide-right {
  from {
    opacity: 0;
    transform: translateX(-20px);
  }
  to {
    opacity: 1;
    transform: translateX(0);
  }
}

@keyframes scale-in {
  from {
    opacity: 0;
    transform: scale(0.95);
  }
  to {
    opacity: 1;
    transform: scale(1);
  }
}

@keyframes pop {
  0% {
    opacity: 0;
    transform: scale(0.8);
  }
  70% {
    transform: scale(1.05);
  }
  100% {
    opacity: 1;
    transform: scale(1);
  }
}
```

---

### Step 6: Animation Guidelines (web-interface-guidelines 기반)

> Vercel의 web-interface-guidelines를 기반으로 한 애니메이션 규칙입니다.

#### 필수 규칙 (Required)

| 규칙 | 설명 | 예시 |
|------|------|------|
| **prefers-reduced-motion** | 사용자의 모션 감도 설정 존중 | CSS media query 또는 `useReducedMotion()` |
| **transform/opacity only** | GPU 가속 속성만 애니메이션 | translate, scale, rotate, opacity |
| **중단 가능** | 애니메이션 중 새 상태로 전환 가능 | spring 애니메이션 |
| **적절한 duration** | 150-300ms 권장, 최대 500ms | 호버: 150ms, 모달: 300ms |

#### 금지 규칙 (Forbidden)

| 패턴 | 문제 | 대안 |
|------|------|------|
| `transition: all` | 의도치 않은 전환 + 성능 저하 | 명시적 속성 지정 |
| `width/height` 애니메이션 | Layout thrashing | `transform: scale()` |
| `top/left/right/bottom` | Layout 트리거 | `transform: translate()` |
| `margin/padding` 애니메이션 | Layout 트리거 | transform 또는 gap |
| 300ms 이상 hover | 사용자 차단 느낌 | 150ms 이하 |
| 무한 반복 (필수 아닌) | 주의 분산 + 접근성 | 조건부 또는 제거 |

#### 코드 예시

```css
/* ❌ Bad: 금지 패턴 */
.element {
  transition: all 0.3s;           /* 1. transition: all */
  transition: width 0.3s;         /* 2. width */
  transition: height 0.3s;        /* 3. height */
  transition: top 0.3s;           /* 4. position */
}

/* ✅ Good: GPU 가속 속성만 */
.element {
  transition: transform 0.2s ease-out, opacity 0.2s ease-out;
}
```

```tsx
// ❌ Bad: 너무 긴 애니메이션
<motion.div transition={{ duration: 1 }} />

// ❌ Bad: reduced motion 무시
<motion.div animate={{ x: 100 }} />

// ✅ Good: 적절한 duration + reduced motion 지원
const shouldReduceMotion = useReducedMotion();

<motion.div
  animate={{ x: shouldReduceMotion ? 0 : 100 }}
  transition={{ duration: shouldReduceMotion ? 0 : 0.2 }}
/>
```

#### Duration 가이드

```typescript
const DURATION_GUIDE = {
  // 마이크로인터랙션 (즉각적 피드백)
  instant: 100,    // 버튼 클릭, 체크박스

  // 빠른 전환 (호버, 토글)
  fast: 150,       // 호버 효과, 드롭다운

  // 일반 전환 (모달, 토스트)
  normal: 200,     // 모달 열기, 페이드

  // 복잡한 전환 (사이드바, 페이지)
  slow: 300,       // 서랍, 페이지 전환

  // 드라마틱 효과 (특별한 경우만)
  slower: 500,     // 히어로 애니메이션 (드물게 사용)
} as const;

// ❌ 피해야 할 duration
// - 500ms 이상: 사용자를 기다리게 함
// - 1000ms 이상: 거의 사용 안 함
```

---

### Step 7: prefers-reduced-motion 지원

```css
/* app/globals.css - Reduced motion support */

/* =========================================
 * Reduced Motion Preferences
 * =========================================
 *
 * WCAG 2.1 Success Criterion 2.3.3:
 * - Respect user's motion preferences
 * - Disable non-essential animations
 * - Keep essential feedback animations (brief)
 */

@media (prefers-reduced-motion: reduce) {
  *,
  *::before,
  *::after {
    /* Remove all animations */
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;

    /* Minimize transitions */
    transition-duration: 0.01ms !important;

    /* Keep scroll behavior for usability */
    scroll-behavior: auto !important;
  }

  /* Exception: Essential loading indicators */
  .essential-animation {
    animation-duration: 150ms !important;
    animation-iteration-count: infinite !important;
  }
}

/* Alternative: Reduce but don't eliminate */
@media (prefers-reduced-motion: reduce) {
  :root {
    --duration-fast: 0ms;
    --duration-normal: 100ms;
    --duration-slow: 150ms;
    --duration-slower: 200ms;
    --duration-slowest: 200ms;
  }
}
```

#### Framer Motion 통합

```typescript
// lib/motion/use-reduced-motion.ts
'use client';

import { useReducedMotion } from 'framer-motion';

/**
 * Hook to get motion-safe animation props
 */
export function useMotionSafeVariants<T extends object>(variants: T): T | null {
  const prefersReducedMotion = useReducedMotion();

  if (prefersReducedMotion) {
    return null; // Skip animations entirely
  }

  return variants;
}

/**
 * Returns reduced duration if user prefers reduced motion
 */
export function useMotionDuration(normalMs: number): number {
  const prefersReducedMotion = useReducedMotion();
  return prefersReducedMotion ? Math.min(normalMs, 100) : normalMs;
}
```

#### Motion-safe 컴포넌트

```tsx
// components/atoms/motion-div.tsx
'use client';

import { motion, useReducedMotion, type Variants } from 'framer-motion';
import { forwardRef } from 'react';

interface MotionDivProps extends React.HTMLAttributes<HTMLDivElement> {
  variants?: Variants;
  initial?: string | boolean;
  animate?: string;
  exit?: string;
  layoutId?: string;
}

export const MotionDiv = forwardRef<HTMLDivElement, MotionDivProps>(
  ({ variants, initial, animate, exit, children, ...props }, ref) => {
    const prefersReducedMotion = useReducedMotion();

    // If user prefers reduced motion, render static div
    if (prefersReducedMotion) {
      return <div ref={ref} {...props}>{children}</div>;
    }

    return (
      <motion.div
        ref={ref}
        variants={variants}
        initial={initial}
        animate={animate}
        exit={exit}
        {...props}
      >
        {children}
      </motion.div>
    );
  }
);

MotionDiv.displayName = 'MotionDiv';
```

---

### Step 8: 실용적 애니메이션 예제

#### Page Transition

```tsx
// components/templates/page-transition.tsx
'use client';

import { motion, AnimatePresence } from 'framer-motion';
import { usePathname } from 'next/navigation';
import { fadeVariants } from '@/lib/motion/variants';

interface PageTransitionProps {
  children: React.ReactNode;
}

export function PageTransition({ children }: PageTransitionProps) {
  const pathname = usePathname();

  return (
    <AnimatePresence mode="wait">
      <motion.div
        key={pathname}
        variants={fadeVariants}
        initial="hidden"
        animate="visible"
        exit="exit"
      >
        {children}
      </motion.div>
    </AnimatePresence>
  );
}
```

#### List Animation

```tsx
// components/organisms/animated-list.tsx
'use client';

import { motion } from 'framer-motion';
import {
  staggerContainerVariants,
  staggerItemVariants,
} from '@/lib/motion/variants';

interface AnimatedListProps<T> {
  items: T[];
  renderItem: (item: T, index: number) => React.ReactNode;
  keyExtractor: (item: T) => string;
  className?: string;
}

export function AnimatedList<T>({
  items,
  renderItem,
  keyExtractor,
  className,
}: AnimatedListProps<T>) {
  return (
    <motion.ul
      className={className}
      variants={staggerContainerVariants}
      initial="hidden"
      animate="visible"
      exit="exit"
    >
      {items.map((item, index) => (
        <motion.li key={keyExtractor(item)} variants={staggerItemVariants}>
          {renderItem(item, index)}
        </motion.li>
      ))}
    </motion.ul>
  );
}
```

#### Hover Animation

```tsx
// components/atoms/hover-card.tsx
'use client';

import { motion } from 'framer-motion';
import { cn } from '@/lib/utils';

interface HoverCardProps extends React.HTMLAttributes<HTMLDivElement> {
  children: React.ReactNode;
}

export function HoverCard({ className, children, ...props }: HoverCardProps) {
  return (
    <motion.div
      className={cn(
        'rounded-lg border bg-card p-6 shadow-sm',
        className
      )}
      whileHover={{
        y: -4,
        boxShadow: '0 10px 40px -10px rgba(0, 0, 0, 0.1)',
      }}
      transition={{
        type: 'spring',
        stiffness: 400,
        damping: 25,
      }}
      {...props}
    >
      {children}
    </motion.div>
  );
}
```

---

## 테스트/검증

### Motion 토큰 테스트

```typescript
// tests/motion.test.ts
import { describe, it, expect } from 'vitest';

describe('Motion Tokens', () => {
  it('has all required duration tokens', () => {
    const root = document.documentElement;
    const style = getComputedStyle(root);

    const tokens = [
      '--duration-fast',
      '--duration-normal',
      '--duration-slow',
    ];

    tokens.forEach((token) => {
      const value = style.getPropertyValue(token);
      expect(value).not.toBe('');
      expect(value).toMatch(/\d+ms/);
    });
  });

  it('has all required easing tokens', () => {
    const root = document.documentElement;
    const style = getComputedStyle(root);

    const tokens = [
      '--ease-out',
      '--ease-in',
      '--ease-in-out',
    ];

    tokens.forEach((token) => {
      const value = style.getPropertyValue(token);
      expect(value).not.toBe('');
    });
  });
});
```

### Framer Motion Variants 테스트

```tsx
// lib/motion/__tests__/variants.test.ts
import { describe, it, expect } from 'vitest';
import { fadeVariants, slideUpVariants, scaleVariants } from '../variants';

describe('Motion Variants', () => {
  it('fadeVariants has required states', () => {
    expect(fadeVariants).toHaveProperty('hidden');
    expect(fadeVariants).toHaveProperty('visible');
    expect(fadeVariants).toHaveProperty('exit');
  });

  it('slideUpVariants starts below', () => {
    const hidden = slideUpVariants.hidden as { y: number };
    expect(hidden.y).toBeGreaterThan(0);
  });

  it('scaleVariants starts smaller', () => {
    const hidden = scaleVariants.hidden as { scale: number };
    expect(hidden.scale).toBeLessThan(1);
  });

  it('visible state returns to normal position', () => {
    const visible = slideUpVariants.visible as { y: number };
    expect(visible.y).toBe(0);
  });
});
```

### Reduced Motion 테스트

```tsx
// components/__tests__/motion-div.test.tsx
import { render, screen } from '@testing-library/react';
import { describe, it, expect, vi } from 'vitest';
import { MotionDiv } from '../atoms/motion-div';
import { fadeVariants } from '@/lib/motion/variants';

// Mock useReducedMotion
vi.mock('framer-motion', async () => {
  const actual = await vi.importActual('framer-motion');
  return {
    ...actual,
    useReducedMotion: vi.fn(),
  };
});

import { useReducedMotion } from 'framer-motion';

describe('MotionDiv', () => {
  it('renders motion.div when motion is allowed', () => {
    vi.mocked(useReducedMotion).mockReturnValue(false);

    render(
      <MotionDiv variants={fadeVariants} data-testid="motion-div">
        Content
      </MotionDiv>
    );

    const element = screen.getByTestId('motion-div');
    expect(element).toBeInTheDocument();
  });

  it('renders static div when reduced motion is preferred', () => {
    vi.mocked(useReducedMotion).mockReturnValue(true);

    render(
      <MotionDiv variants={fadeVariants} data-testid="static-div">
        Content
      </MotionDiv>
    );

    const element = screen.getByTestId('static-div');
    expect(element.tagName).toBe('DIV');
  });
});
```

### Storybook 시각적 검증

```tsx
// stories/Motion.stories.tsx
import type { Meta, StoryObj } from '@storybook/react';
import { motion } from 'framer-motion';
import { useState } from 'react';
import {
  fadeVariants,
  slideUpVariants,
  popVariants,
  staggerContainerVariants,
  staggerItemVariants,
} from '@/lib/motion/variants';

const meta: Meta = {
  title: 'Design System/Motion',
};

export default meta;

export const EasingCurves: StoryObj = {
  render: () => {
    const [isAnimating, setIsAnimating] = useState(false);

    return (
      <div className="space-y-8 p-6">
        <button
          className="px-4 py-2 bg-primary text-primary-foreground rounded"
          onClick={() => setIsAnimating(!isAnimating)}
        >
          Toggle Animation
        </button>

        <div className="grid grid-cols-4 gap-4">
          {['ease-out', 'ease-in', 'ease-in-out', 'bounce'].map((easing) => (
            <div key={easing} className="space-y-2">
              <p className="text-sm text-muted-foreground">{easing}</p>
              <motion.div
                className="h-12 w-12 bg-primary rounded"
                animate={{
                  x: isAnimating ? 100 : 0,
                }}
                transition={{
                  duration: 0.5,
                  ease: easing === 'bounce'
                    ? [0.34, 1.56, 0.64, 1]
                    : easing,
                }}
              />
            </div>
          ))}
        </div>
      </div>
    );
  },
};

export const VariantsDemo: StoryObj = {
  render: () => {
    const [show, setShow] = useState(true);

    return (
      <div className="space-y-8 p-6">
        <button
          className="px-4 py-2 bg-primary text-primary-foreground rounded"
          onClick={() => setShow(!show)}
        >
          Toggle
        </button>

        <div className="grid grid-cols-3 gap-8">
          <div>
            <p className="mb-2 text-sm">Fade</p>
            {show && (
              <motion.div
                className="h-20 w-20 bg-primary rounded"
                variants={fadeVariants}
                initial="hidden"
                animate="visible"
              />
            )}
          </div>

          <div>
            <p className="mb-2 text-sm">Slide Up</p>
            {show && (
              <motion.div
                className="h-20 w-20 bg-primary rounded"
                variants={slideUpVariants}
                initial="hidden"
                animate="visible"
              />
            )}
          </div>

          <div>
            <p className="mb-2 text-sm">Pop</p>
            {show && (
              <motion.div
                className="h-20 w-20 bg-primary rounded"
                variants={popVariants}
                initial="hidden"
                animate="visible"
              />
            )}
          </div>
        </div>
      </div>
    );
  },
};

export const StaggerAnimation: StoryObj = {
  render: () => (
    <motion.ul
      className="space-y-2"
      variants={staggerContainerVariants}
      initial="hidden"
      animate="visible"
    >
      {[1, 2, 3, 4, 5].map((item) => (
        <motion.li
          key={item}
          className="p-4 bg-muted rounded"
          variants={staggerItemVariants}
        >
          Item {item}
        </motion.li>
      ))}
    </motion.ul>
  ),
};
```

---

## 안티패턴

### 1. 과도한 애니메이션

```tsx
// ❌ Bad: 모든 것에 애니메이션
<motion.div
  animate={{ rotate: 360, scale: [1, 1.2, 1], x: [0, 10, 0] }}
  transition={{ repeat: Infinity }}
>
  <motion.p animate={{ opacity: [0.5, 1, 0.5] }}>
    Too much motion!
  </motion.p>
</motion.div>

// ✅ Good: 의미 있는 애니메이션만
<motion.div
  initial={{ opacity: 0 }}
  animate={{ opacity: 1 }}
  transition={{ duration: 0.3 }}
>
  <p>Subtle and purposeful</p>
</motion.div>
```

### 2. 접근성 무시

```tsx
// ❌ Bad: prefers-reduced-motion 무시
<motion.div
  animate={{ x: [0, 100, 0] }}
  transition={{ repeat: Infinity }}
>
  Ignores user preferences
</motion.div>

// ✅ Good: 사용자 설정 존중
const prefersReducedMotion = useReducedMotion();

<motion.div
  animate={prefersReducedMotion ? {} : { x: [0, 100, 0] }}
  transition={prefersReducedMotion ? {} : { repeat: Infinity }}
>
  Respects preferences
</motion.div>
```

### 3. 하드코딩된 값

```tsx
// ❌ Bad: 매직 넘버
<motion.div
  transition={{ duration: 0.287, ease: [0.34, 1.56, 0.64, 1] }}
>

// ✅ Good: 토큰 사용
import { springs } from '@/lib/motion/springs';

<motion.div
  transition={springs.bouncy}
>
```

### 4. 레이아웃 애니메이션 남용

```tsx
// ❌ Bad: 모든 요소에 layout 적용 (성능 문제)
<motion.div layout>
  <motion.div layout>
    <motion.div layout>
      Nested layout animations
    </motion.div>
  </motion.div>
</motion.div>

// ✅ Good: 필요한 곳에만 layout
<motion.div layoutId="shared-element">
  Only where necessary
</motion.div>
```

### 5. 긴 duration

```tsx
// ❌ Bad: 너무 긴 애니메이션
<motion.div
  initial={{ opacity: 0 }}
  animate={{ opacity: 1 }}
  transition={{ duration: 2 }}  // 2초는 너무 길다
>

// ✅ Good: 적절한 duration
<motion.div
  initial={{ opacity: 0 }}
  animate={{ opacity: 1 }}
  transition={{ duration: 0.3 }}  // 300ms
>
```

---

## 성능 고려사항

### GPU 가속 활용

```css
/* transform과 opacity만 애니메이션 (GPU 가속) */
.performant-animation {
  transform: translateX(0);
  opacity: 1;
  will-change: transform, opacity;
}

/* ❌ 피하기: Layout 트리거 속성 애니메이션 */
.avoid {
  width: 100px;  /* Layout */
  height: 100px; /* Layout */
  top: 0;        /* Layout */
  left: 0;       /* Layout */
}
```

### AnimatePresence 최적화

```tsx
// mode="wait"은 순차 실행 (더 부드러움)
// mode="sync"은 동시 실행 (더 빠름)
<AnimatePresence mode="wait">
  {/* Sequential animations */}
</AnimatePresence>
```

### 조건부 애니메이션

```tsx
// 뷰포트에 들어올 때만 애니메이션
import { useInView } from 'framer-motion';

function AnimatedSection() {
  const ref = useRef(null);
  const isInView = useInView(ref, { once: true });

  return (
    <motion.section
      ref={ref}
      initial={{ opacity: 0, y: 50 }}
      animate={isInView ? { opacity: 1, y: 0 } : {}}
    >
      Animates when scrolled into view
    </motion.section>
  );
}
```

---

## 보안 고려사항

### XSS 방지

```tsx
// ❌ 위험: 사용자 입력을 애니메이션 값으로 사용
<motion.div
  animate={{ x: userInput }}  // userInput이 악성 코드일 수 있음
>

// ✅ 안전: 값 검증 및 제한
const safeX = typeof userInput === 'number'
  ? Math.min(Math.max(userInput, -100), 100)
  : 0;

<motion.div animate={{ x: safeX }}>
```

---

## References

- `_references/MOTION-PATTERNS.md` - 모션 패턴 상세 가이드
- `3-direction/` - 디자인 방향 결정 (선행 스킬)
- `5-color/` - 색상 시스템 (연계)
- `6-spacing/` - 스페이싱 시스템 (연계)
- `11-interactions/` - 인터랙션 디자인 (후속 스킬)
