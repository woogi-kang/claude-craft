# MOTION-PATTERNS.md

Framer Motion 애니메이션 레시피와 패턴

---

## 목차

1. [애니메이션 토큰](#애니메이션-토큰)
2. [마이크로 인터랙션](#마이크로-인터랙션)
3. [페이지 전환](#페이지-전환)
4. [레이아웃 애니메이션](#레이아웃-애니메이션)
5. [스크롤 트리거 애니메이션](#스크롤-트리거-애니메이션)
6. [접근성 고려사항](#접근성-고려사항)
7. [고급 패턴](#고급-패턴)

---

## 애니메이션 토큰

### Duration 토큰

```tsx
// lib/motion/tokens.ts
export const duration = {
  instant: 0.1,      // Micro feedback
  fast: 0.15,        // Hover states
  normal: 0.25,      // Standard transitions
  slow: 0.4,         // Complex animations
  slower: 0.6,       // Page transitions
  slowest: 0.8,      // Dramatic reveals
} as const;

export const stagger = {
  fast: 0.03,        // Rapid sequence
  normal: 0.05,      // Default stagger
  slow: 0.08,        // Deliberate sequence
  slower: 0.12,      // Dramatic buildup
} as const;
```

### Easing 토큰

```tsx
// lib/motion/tokens.ts
export const ease = {
  // Standard easings
  linear: [0, 0, 1, 1],
  easeIn: [0.4, 0, 1, 1],
  easeOut: [0, 0, 0.2, 1],
  easeInOut: [0.4, 0, 0.2, 1],

  // Custom easings
  spring: [0.175, 0.885, 0.32, 1.275],   // Slight overshoot
  bounce: [0.68, -0.55, 0.265, 1.55],    // Bouncy
  smooth: [0.25, 0.1, 0.25, 1],          // Apple-like
  snappy: [0.16, 1, 0.3, 1],             // Quick snap
  gentle: [0.4, 0, 0.6, 1],              // Soft movement

  // Spring physics
  springConfig: {
    soft: { type: 'spring', stiffness: 100, damping: 15 },
    medium: { type: 'spring', stiffness: 200, damping: 20 },
    stiff: { type: 'spring', stiffness: 300, damping: 30 },
    bouncy: { type: 'spring', stiffness: 400, damping: 10 },
  },
} as const;
```

### Preset Variants

```tsx
// lib/motion/variants.ts
import { Variants } from 'framer-motion';
import { duration, ease } from './tokens';

export const fadeIn: Variants = {
  hidden: { opacity: 0 },
  visible: {
    opacity: 1,
    transition: { duration: duration.normal, ease: ease.easeOut },
  },
};

export const fadeInUp: Variants = {
  hidden: { opacity: 0, y: 20 },
  visible: {
    opacity: 1,
    y: 0,
    transition: { duration: duration.normal, ease: ease.easeOut },
  },
};

export const fadeInDown: Variants = {
  hidden: { opacity: 0, y: -20 },
  visible: {
    opacity: 1,
    y: 0,
    transition: { duration: duration.normal, ease: ease.easeOut },
  },
};

export const slideInLeft: Variants = {
  hidden: { opacity: 0, x: -30 },
  visible: {
    opacity: 1,
    x: 0,
    transition: { duration: duration.normal, ease: ease.easeOut },
  },
};

export const slideInRight: Variants = {
  hidden: { opacity: 0, x: 30 },
  visible: {
    opacity: 1,
    x: 0,
    transition: { duration: duration.normal, ease: ease.easeOut },
  },
};

export const scaleIn: Variants = {
  hidden: { opacity: 0, scale: 0.95 },
  visible: {
    opacity: 1,
    scale: 1,
    transition: { duration: duration.normal, ease: ease.spring },
  },
};

export const staggerContainer: Variants = {
  hidden: { opacity: 0 },
  visible: {
    opacity: 1,
    transition: {
      staggerChildren: 0.05,
      delayChildren: 0.1,
    },
  },
};
```

---

## 마이크로 인터랙션

### 1. 버튼 호버/탭

```tsx
// components/ui/button-animated.tsx
'use client';

import { motion } from 'framer-motion';
import { ReactNode } from 'react';

interface AnimatedButtonProps {
  children: ReactNode;
  onClick?: () => void;
  variant?: 'default' | 'outline' | 'ghost';
}

export function AnimatedButton({
  children,
  onClick,
  variant = 'default',
}: AnimatedButtonProps) {
  return (
    <motion.button
      onClick={onClick}
      className="px-4 py-2 rounded-lg bg-primary text-primary-foreground font-medium"
      whileHover={{ scale: 1.02 }}
      whileTap={{ scale: 0.98 }}
      transition={{
        type: 'spring',
        stiffness: 400,
        damping: 17,
      }}
    >
      {children}
    </motion.button>
  );
}
```

### 2. 아이콘 버튼 회전

```tsx
// components/ui/icon-button.tsx
'use client';

import { motion } from 'framer-motion';
import { RefreshCw } from 'lucide-react';

interface IconButtonProps {
  onClick?: () => void;
  isLoading?: boolean;
}

export function RefreshButton({ onClick, isLoading }: IconButtonProps) {
  return (
    <motion.button
      onClick={onClick}
      className="p-2 rounded-lg hover:bg-muted transition-colors"
      whileHover={{ rotate: 90 }}
      whileTap={{ scale: 0.9 }}
      transition={{ type: 'spring', stiffness: 400, damping: 17 }}
    >
      <motion.div
        animate={isLoading ? { rotate: 360 } : { rotate: 0 }}
        transition={isLoading ? { repeat: Infinity, duration: 1, ease: 'linear' } : {}}
      >
        <RefreshCw className="w-5 h-5" />
      </motion.div>
    </motion.button>
  );
}
```

### 3. 체크박스 애니메이션

```tsx
// components/ui/checkbox-animated.tsx
'use client';

import { motion } from 'framer-motion';
import { Check } from 'lucide-react';

interface AnimatedCheckboxProps {
  checked: boolean;
  onChange: (checked: boolean) => void;
  label?: string;
}

export function AnimatedCheckbox({
  checked,
  onChange,
  label,
}: AnimatedCheckboxProps) {
  return (
    <label className="flex items-center gap-3 cursor-pointer group">
      <motion.div
        className="w-5 h-5 rounded border-2 flex items-center justify-center"
        animate={{
          backgroundColor: checked ? 'var(--primary)' : 'transparent',
          borderColor: checked ? 'var(--primary)' : 'var(--border)',
        }}
        whileHover={{ scale: 1.05 }}
        whileTap={{ scale: 0.95 }}
        transition={{ duration: 0.15 }}
        onClick={() => onChange(!checked)}
      >
        <motion.div
          initial={false}
          animate={{
            scale: checked ? 1 : 0,
            opacity: checked ? 1 : 0,
          }}
          transition={{ type: 'spring', stiffness: 500, damping: 30 }}
        >
          <Check className="w-3 h-3 text-primary-foreground" />
        </motion.div>
      </motion.div>
      {label && (
        <span className="text-sm group-hover:text-foreground transition-colors">
          {label}
        </span>
      )}
    </label>
  );
}
```

### 4. 스위치/토글

```tsx
// components/ui/switch-animated.tsx
'use client';

import { motion } from 'framer-motion';

interface AnimatedSwitchProps {
  checked: boolean;
  onChange: (checked: boolean) => void;
}

export function AnimatedSwitch({ checked, onChange }: AnimatedSwitchProps) {
  return (
    <motion.button
      className="w-12 h-7 rounded-full p-1 cursor-pointer"
      animate={{
        backgroundColor: checked
          ? 'var(--primary)'
          : 'var(--muted)',
      }}
      onClick={() => onChange(!checked)}
      whileTap={{ scale: 0.95 }}
    >
      <motion.div
        className="w-5 h-5 rounded-full bg-white shadow-md"
        animate={{
          x: checked ? 20 : 0,
        }}
        transition={{
          type: 'spring',
          stiffness: 500,
          damping: 30,
        }}
      />
    </motion.button>
  );
}
```

### 5. 인풋 포커스 애니메이션

```tsx
// components/ui/input-animated.tsx
'use client';

import { motion } from 'framer-motion';
import { useState } from 'react';

interface AnimatedInputProps {
  placeholder?: string;
  value: string;
  onChange: (value: string) => void;
}

export function AnimatedInput({
  placeholder,
  value,
  onChange,
}: AnimatedInputProps) {
  const [isFocused, setIsFocused] = useState(false);

  return (
    <div className="relative">
      <motion.div
        className="absolute inset-0 rounded-lg bg-primary/20"
        initial={false}
        animate={{
          scale: isFocused ? 1.02 : 1,
          opacity: isFocused ? 1 : 0,
        }}
        transition={{ duration: 0.2 }}
      />
      <input
        type="text"
        value={value}
        onChange={(e) => onChange(e.target.value)}
        onFocus={() => setIsFocused(true)}
        onBlur={() => setIsFocused(false)}
        placeholder={placeholder}
        className="relative w-full px-4 py-2 rounded-lg border bg-background focus:outline-none focus:border-primary transition-colors"
      />
    </div>
  );
}
```

### 6. 플로팅 라벨 인풋

```tsx
// components/ui/floating-input.tsx
'use client';

import { motion, AnimatePresence } from 'framer-motion';
import { useState } from 'react';

interface FloatingInputProps {
  label: string;
  value: string;
  onChange: (value: string) => void;
  type?: string;
}

export function FloatingInput({
  label,
  value,
  onChange,
  type = 'text',
}: FloatingInputProps) {
  const [isFocused, setIsFocused] = useState(false);
  const isActive = isFocused || value.length > 0;

  return (
    <div className="relative">
      <motion.label
        className="absolute left-3 pointer-events-none text-muted-foreground origin-left"
        animate={{
          y: isActive ? -24 : 8,
          scale: isActive ? 0.85 : 1,
          color: isFocused ? 'var(--primary)' : 'var(--muted-foreground)',
        }}
        transition={{ duration: 0.2 }}
      >
        {label}
      </motion.label>
      <input
        type={type}
        value={value}
        onChange={(e) => onChange(e.target.value)}
        onFocus={() => setIsFocused(true)}
        onBlur={() => setIsFocused(false)}
        className="w-full px-3 py-2 pt-4 rounded-lg border bg-background focus:outline-none focus:border-primary transition-colors"
      />
      <motion.div
        className="absolute bottom-0 left-0 h-0.5 bg-primary"
        initial={{ scaleX: 0 }}
        animate={{ scaleX: isFocused ? 1 : 0 }}
        transition={{ duration: 0.2 }}
        style={{ originX: 0 }}
      />
    </div>
  );
}
```

### 7. 리플 이펙트

```tsx
// components/ui/ripple-button.tsx
'use client';

import { motion, AnimatePresence } from 'framer-motion';
import { useState, MouseEvent } from 'react';

interface Ripple {
  id: number;
  x: number;
  y: number;
}

export function RippleButton({ children }: { children: React.ReactNode }) {
  const [ripples, setRipples] = useState<Ripple[]>([]);

  const addRipple = (e: MouseEvent<HTMLButtonElement>) => {
    const button = e.currentTarget;
    const rect = button.getBoundingClientRect();
    const x = e.clientX - rect.left;
    const y = e.clientY - rect.top;

    const newRipple = { id: Date.now(), x, y };
    setRipples((prev) => [...prev, newRipple]);

    setTimeout(() => {
      setRipples((prev) => prev.filter((r) => r.id !== newRipple.id));
    }, 600);
  };

  return (
    <button
      onClick={addRipple}
      className="relative overflow-hidden px-6 py-3 rounded-lg bg-primary text-primary-foreground"
    >
      <AnimatePresence>
        {ripples.map((ripple) => (
          <motion.span
            key={ripple.id}
            className="absolute rounded-full bg-white/30 pointer-events-none"
            style={{
              left: ripple.x,
              top: ripple.y,
            }}
            initial={{ width: 0, height: 0, x: 0, y: 0, opacity: 0.5 }}
            animate={{
              width: 300,
              height: 300,
              x: -150,
              y: -150,
              opacity: 0,
            }}
            exit={{ opacity: 0 }}
            transition={{ duration: 0.6, ease: 'easeOut' }}
          />
        ))}
      </AnimatePresence>
      <span className="relative z-10">{children}</span>
    </button>
  );
}
```

### 8. 프로그레스 바

```tsx
// components/ui/progress-animated.tsx
'use client';

import { motion } from 'framer-motion';

interface AnimatedProgressProps {
  value: number; // 0-100
  showLabel?: boolean;
}

export function AnimatedProgress({
  value,
  showLabel = false,
}: AnimatedProgressProps) {
  return (
    <div className="w-full">
      <div className="h-2 bg-muted rounded-full overflow-hidden">
        <motion.div
          className="h-full bg-primary rounded-full"
          initial={{ width: 0 }}
          animate={{ width: `${value}%` }}
          transition={{
            type: 'spring',
            stiffness: 100,
            damping: 15,
          }}
        />
      </div>
      {showLabel && (
        <motion.span
          className="text-sm text-muted-foreground mt-1 block"
          key={value}
          initial={{ opacity: 0, y: -10 }}
          animate={{ opacity: 1, y: 0 }}
        >
          {value}%
        </motion.span>
      )}
    </div>
  );
}
```

### 9. 카운트 애니메이션

```tsx
// components/ui/animated-counter.tsx
'use client';

import { motion, useSpring, useTransform, useMotionValue, animate } from 'framer-motion';
import { useEffect } from 'react';

interface AnimatedCounterProps {
  value: number;
  duration?: number;
  formatFn?: (value: number) => string;
}

export function AnimatedCounter({
  value,
  duration = 1,
  formatFn = (v) => Math.round(v).toLocaleString(),
}: AnimatedCounterProps) {
  const motionValue = useMotionValue(0);
  const springValue = useSpring(motionValue, {
    stiffness: 100,
    damping: 30,
    duration: duration * 1000,
  });
  const displayValue = useTransform(springValue, (v) => formatFn(v));

  useEffect(() => {
    animate(motionValue, value, { duration });
  }, [value, motionValue, duration]);

  return <motion.span>{displayValue}</motion.span>;
}

// Usage
export function StatsCard() {
  return (
    <div className="text-4xl font-bold">
      <AnimatedCounter value={12847} />
    </div>
  );
}
```

### 10. 알림 뱃지 펄스

```tsx
// components/ui/notification-badge.tsx
'use client';

import { motion } from 'framer-motion';

interface NotificationBadgeProps {
  count: number;
}

export function NotificationBadge({ count }: NotificationBadgeProps) {
  if (count === 0) return null;

  return (
    <motion.div
      className="absolute -top-1 -right-1 min-w-5 h-5 px-1.5 rounded-full bg-error text-error-foreground text-xs font-medium flex items-center justify-center"
      initial={{ scale: 0 }}
      animate={{ scale: 1 }}
      transition={{ type: 'spring', stiffness: 500, damping: 25 }}
    >
      <motion.span
        key={count}
        initial={{ opacity: 0, y: -10 }}
        animate={{ opacity: 1, y: 0 }}
      >
        {count > 99 ? '99+' : count}
      </motion.span>
      {/* Pulse effect */}
      <motion.div
        className="absolute inset-0 rounded-full bg-error"
        animate={{
          scale: [1, 1.5],
          opacity: [0.5, 0],
        }}
        transition={{
          duration: 1,
          repeat: Infinity,
          repeatType: 'loop',
        }}
      />
    </motion.div>
  );
}
```

---

## 페이지 전환

### 11. 페이드 페이지 전환

```tsx
// components/page-transition.tsx
'use client';

import { motion, AnimatePresence } from 'framer-motion';
import { usePathname } from 'next/navigation';
import { ReactNode } from 'react';

export function PageTransition({ children }: { children: ReactNode }) {
  const pathname = usePathname();

  return (
    <AnimatePresence mode="wait">
      <motion.div
        key={pathname}
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        exit={{ opacity: 0, y: -20 }}
        transition={{
          duration: 0.3,
          ease: [0.25, 0.1, 0.25, 1],
        }}
      >
        {children}
      </motion.div>
    </AnimatePresence>
  );
}
```

### 12. 슬라이드 페이지 전환

```tsx
// components/slide-page-transition.tsx
'use client';

import { motion, AnimatePresence } from 'framer-motion';
import { usePathname } from 'next/navigation';
import { ReactNode } from 'react';

const variants = {
  initial: (direction: number) => ({
    x: direction > 0 ? '100%' : '-100%',
    opacity: 0,
  }),
  animate: {
    x: 0,
    opacity: 1,
  },
  exit: (direction: number) => ({
    x: direction > 0 ? '-100%' : '100%',
    opacity: 0,
  }),
};

export function SlidePageTransition({
  children,
  direction = 1,
}: {
  children: ReactNode;
  direction?: number;
}) {
  const pathname = usePathname();

  return (
    <AnimatePresence mode="wait" custom={direction}>
      <motion.div
        key={pathname}
        custom={direction}
        variants={variants}
        initial="initial"
        animate="animate"
        exit="exit"
        transition={{
          type: 'spring',
          stiffness: 300,
          damping: 30,
        }}
        className="w-full"
      >
        {children}
      </motion.div>
    </AnimatePresence>
  );
}
```

### 13. 모달 오버레이

```tsx
// components/ui/modal.tsx
'use client';

import { motion, AnimatePresence } from 'framer-motion';
import { ReactNode } from 'react';
import { X } from 'lucide-react';

interface ModalProps {
  isOpen: boolean;
  onClose: () => void;
  children: ReactNode;
  title?: string;
}

export function Modal({ isOpen, onClose, children, title }: ModalProps) {
  return (
    <AnimatePresence>
      {isOpen && (
        <>
          {/* Backdrop */}
          <motion.div
            className="fixed inset-0 bg-black/50 backdrop-blur-sm z-40"
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            onClick={onClose}
          />

          {/* Modal */}
          <motion.div
            className="fixed inset-0 flex items-center justify-center z-50 p-4"
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
          >
            <motion.div
              className="bg-background rounded-2xl shadow-xl max-w-lg w-full max-h-[90vh] overflow-auto"
              initial={{ scale: 0.95, y: 20 }}
              animate={{ scale: 1, y: 0 }}
              exit={{ scale: 0.95, y: 20 }}
              transition={{
                type: 'spring',
                stiffness: 300,
                damping: 30,
              }}
              onClick={(e) => e.stopPropagation()}
            >
              {/* Header */}
              <div className="flex items-center justify-between p-6 border-b">
                {title && <h2 className="text-xl font-semibold">{title}</h2>}
                <button
                  onClick={onClose}
                  className="p-2 rounded-lg hover:bg-muted transition-colors"
                >
                  <X className="w-5 h-5" />
                </button>
              </div>

              {/* Content */}
              <div className="p-6">{children}</div>
            </motion.div>
          </motion.div>
        </>
      )}
    </AnimatePresence>
  );
}
```

### 14. 드로어/시트

```tsx
// components/ui/drawer.tsx
'use client';

import { motion, AnimatePresence, useDragControls, PanInfo } from 'framer-motion';
import { ReactNode, useRef } from 'react';

interface DrawerProps {
  isOpen: boolean;
  onClose: () => void;
  children: ReactNode;
  side?: 'left' | 'right' | 'bottom';
}

export function Drawer({
  isOpen,
  onClose,
  children,
  side = 'right',
}: DrawerProps) {
  const constraintsRef = useRef(null);

  const variants = {
    left: {
      initial: { x: '-100%' },
      animate: { x: 0 },
      exit: { x: '-100%' },
    },
    right: {
      initial: { x: '100%' },
      animate: { x: 0 },
      exit: { x: '100%' },
    },
    bottom: {
      initial: { y: '100%' },
      animate: { y: 0 },
      exit: { y: '100%' },
    },
  };

  const handleDragEnd = (_: MouseEvent | TouchEvent, info: PanInfo) => {
    const threshold = 100;
    if (
      (side === 'right' && info.offset.x > threshold) ||
      (side === 'left' && info.offset.x < -threshold) ||
      (side === 'bottom' && info.offset.y > threshold)
    ) {
      onClose();
    }
  };

  return (
    <AnimatePresence>
      {isOpen && (
        <>
          <motion.div
            className="fixed inset-0 bg-black/50 z-40"
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            onClick={onClose}
          />

          <motion.div
            ref={constraintsRef}
            className={`fixed z-50 bg-background shadow-xl ${
              side === 'bottom'
                ? 'inset-x-0 bottom-0 rounded-t-2xl max-h-[90vh]'
                : side === 'left'
                  ? 'inset-y-0 left-0 w-80'
                  : 'inset-y-0 right-0 w-80'
            }`}
            variants={variants[side]}
            initial="initial"
            animate="animate"
            exit="exit"
            transition={{ type: 'spring', stiffness: 300, damping: 30 }}
            drag={side === 'bottom' ? 'y' : 'x'}
            dragConstraints={{ top: 0, bottom: 0, left: 0, right: 0 }}
            dragElastic={0.2}
            onDragEnd={handleDragEnd}
          >
            {/* Drag handle for bottom sheet */}
            {side === 'bottom' && (
              <div className="flex justify-center py-3">
                <div className="w-12 h-1.5 rounded-full bg-muted" />
              </div>
            )}
            {children}
          </motion.div>
        </>
      )}
    </AnimatePresence>
  );
}
```

---

## 레이아웃 애니메이션

### 15. 리스트 순서 변경

```tsx
// components/ui/sortable-list.tsx
'use client';

import { motion, AnimatePresence, Reorder } from 'framer-motion';
import { useState } from 'react';

interface Item {
  id: string;
  content: string;
}

export function SortableList() {
  const [items, setItems] = useState<Item[]>([
    { id: '1', content: 'First item' },
    { id: '2', content: 'Second item' },
    { id: '3', content: 'Third item' },
  ]);

  return (
    <Reorder.Group
      axis="y"
      values={items}
      onReorder={setItems}
      className="space-y-2"
    >
      <AnimatePresence>
        {items.map((item) => (
          <Reorder.Item
            key={item.id}
            value={item}
            className="p-4 bg-card rounded-lg border cursor-grab active:cursor-grabbing"
            initial={{ opacity: 0, y: -20 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: 20 }}
            whileDrag={{
              scale: 1.02,
              boxShadow: '0 10px 30px rgba(0,0,0,0.1)',
            }}
          >
            {item.content}
          </Reorder.Item>
        ))}
      </AnimatePresence>
    </Reorder.Group>
  );
}
```

### 16. 그리드 레이아웃 전환

```tsx
// components/ui/animated-grid.tsx
'use client';

import { motion, LayoutGroup } from 'framer-motion';
import { useState } from 'react';

interface GridItem {
  id: string;
  title: string;
  expanded?: boolean;
}

export function AnimatedGrid() {
  const [items, setItems] = useState<GridItem[]>([
    { id: '1', title: 'Card 1' },
    { id: '2', title: 'Card 2' },
    { id: '3', title: 'Card 3' },
    { id: '4', title: 'Card 4' },
  ]);

  const toggleExpand = (id: string) => {
    setItems(items.map(item =>
      item.id === id ? { ...item, expanded: !item.expanded } : item
    ));
  };

  return (
    <LayoutGroup>
      <div className="grid grid-cols-2 gap-4">
        {items.map((item) => (
          <motion.div
            key={item.id}
            layoutId={item.id}
            className={`bg-card rounded-xl border p-6 cursor-pointer ${
              item.expanded ? 'col-span-2 row-span-2' : ''
            }`}
            onClick={() => toggleExpand(item.id)}
            transition={{
              layout: { type: 'spring', stiffness: 300, damping: 30 },
            }}
          >
            <motion.h3
              layout="position"
              className="font-semibold"
            >
              {item.title}
            </motion.h3>
            {item.expanded && (
              <motion.p
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                className="mt-4 text-muted-foreground"
              >
                Expanded content goes here...
              </motion.p>
            )}
          </motion.div>
        ))}
      </div>
    </LayoutGroup>
  );
}
```

### 17. 공유 레이아웃 (Shared Element)

```tsx
// components/ui/shared-layout-card.tsx
'use client';

import { motion, AnimatePresence } from 'framer-motion';
import { useState } from 'react';

interface CardData {
  id: string;
  title: string;
  image: string;
  description: string;
}

export function SharedLayoutGallery({ cards }: { cards: CardData[] }) {
  const [selectedId, setSelectedId] = useState<string | null>(null);
  const selectedCard = cards.find((c) => c.id === selectedId);

  return (
    <>
      <div className="grid grid-cols-3 gap-4">
        {cards.map((card) => (
          <motion.div
            key={card.id}
            layoutId={`card-${card.id}`}
            onClick={() => setSelectedId(card.id)}
            className="cursor-pointer rounded-xl overflow-hidden bg-card border"
          >
            <motion.img
              layoutId={`image-${card.id}`}
              src={card.image}
              alt={card.title}
              className="w-full aspect-video object-cover"
            />
            <motion.div layoutId={`content-${card.id}`} className="p-4">
              <motion.h3 layoutId={`title-${card.id}`} className="font-semibold">
                {card.title}
              </motion.h3>
            </motion.div>
          </motion.div>
        ))}
      </div>

      <AnimatePresence>
        {selectedId && selectedCard && (
          <>
            <motion.div
              className="fixed inset-0 bg-black/50 z-40"
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              exit={{ opacity: 0 }}
              onClick={() => setSelectedId(null)}
            />
            <motion.div
              layoutId={`card-${selectedId}`}
              className="fixed inset-4 md:inset-20 z-50 rounded-2xl overflow-hidden bg-card"
            >
              <motion.img
                layoutId={`image-${selectedId}`}
                src={selectedCard.image}
                alt={selectedCard.title}
                className="w-full h-64 object-cover"
              />
              <motion.div layoutId={`content-${selectedId}`} className="p-6">
                <motion.h3 layoutId={`title-${selectedId}`} className="text-2xl font-bold mb-4">
                  {selectedCard.title}
                </motion.h3>
                <motion.p
                  initial={{ opacity: 0 }}
                  animate={{ opacity: 1 }}
                  exit={{ opacity: 0 }}
                  className="text-muted-foreground"
                >
                  {selectedCard.description}
                </motion.p>
              </motion.div>
              <button
                onClick={() => setSelectedId(null)}
                className="absolute top-4 right-4 p-2 rounded-full bg-black/50 text-white"
              >
                Close
              </button>
            </motion.div>
          </>
        )}
      </AnimatePresence>
    </>
  );
}
```

---

## 스크롤 트리거 애니메이션

### 18. 뷰포트 진입 애니메이션

```tsx
// components/ui/scroll-reveal.tsx
'use client';

import { motion, useInView } from 'framer-motion';
import { ReactNode, useRef } from 'react';

interface ScrollRevealProps {
  children: ReactNode;
  delay?: number;
  direction?: 'up' | 'down' | 'left' | 'right';
}

export function ScrollReveal({
  children,
  delay = 0,
  direction = 'up',
}: ScrollRevealProps) {
  const ref = useRef(null);
  const isInView = useInView(ref, { once: true, margin: '-100px' });

  const directions = {
    up: { y: 40 },
    down: { y: -40 },
    left: { x: 40 },
    right: { x: -40 },
  };

  return (
    <motion.div
      ref={ref}
      initial={{
        opacity: 0,
        ...directions[direction],
      }}
      animate={isInView ? { opacity: 1, x: 0, y: 0 } : {}}
      transition={{
        duration: 0.6,
        delay,
        ease: [0.25, 0.1, 0.25, 1],
      }}
    >
      {children}
    </motion.div>
  );
}
```

### 19. 스태거 리스트

```tsx
// components/ui/stagger-list.tsx
'use client';

import { motion, useInView } from 'framer-motion';
import { ReactNode, useRef, Children } from 'react';

interface StaggerListProps {
  children: ReactNode;
  staggerDelay?: number;
}

export function StaggerList({ children, staggerDelay = 0.1 }: StaggerListProps) {
  const ref = useRef(null);
  const isInView = useInView(ref, { once: true, margin: '-50px' });

  const container = {
    hidden: { opacity: 0 },
    show: {
      opacity: 1,
      transition: {
        staggerChildren: staggerDelay,
      },
    },
  };

  const item = {
    hidden: { opacity: 0, y: 20 },
    show: { opacity: 1, y: 0 },
  };

  return (
    <motion.div
      ref={ref}
      variants={container}
      initial="hidden"
      animate={isInView ? 'show' : 'hidden'}
      className="space-y-4"
    >
      {Children.map(children, (child) => (
        <motion.div variants={item}>{child}</motion.div>
      ))}
    </motion.div>
  );
}
```

### 20. 패럴랙스 스크롤

```tsx
// components/ui/parallax.tsx
'use client';

import { motion, useScroll, useTransform } from 'framer-motion';
import { ReactNode, useRef } from 'react';

interface ParallaxProps {
  children: ReactNode;
  speed?: number; // -1 to 1, negative = slower, positive = faster
}

export function Parallax({ children, speed = 0.5 }: ParallaxProps) {
  const ref = useRef(null);
  const { scrollYProgress } = useScroll({
    target: ref,
    offset: ['start end', 'end start'],
  });

  const y = useTransform(scrollYProgress, [0, 1], [speed * -100, speed * 100]);

  return (
    <motion.div ref={ref} style={{ y }}>
      {children}
    </motion.div>
  );
}

// Usage example
export function ParallaxHero() {
  return (
    <div className="relative h-screen overflow-hidden">
      {/* Background - moves slower */}
      <Parallax speed={-0.3}>
        <div className="absolute inset-0 bg-gradient-to-b from-primary/20 to-background" />
      </Parallax>

      {/* Content - stays relatively still */}
      <div className="relative z-10 flex items-center justify-center h-full">
        <h1 className="text-6xl font-bold">Welcome</h1>
      </div>

      {/* Foreground element - moves faster */}
      <Parallax speed={0.5}>
        <div className="absolute bottom-0 w-full h-32 bg-card" />
      </Parallax>
    </div>
  );
}
```

### 21. 스크롤 프로그레스 바

```tsx
// components/ui/scroll-progress.tsx
'use client';

import { motion, useScroll, useSpring } from 'framer-motion';

export function ScrollProgress() {
  const { scrollYProgress } = useScroll();
  const scaleX = useSpring(scrollYProgress, {
    stiffness: 100,
    damping: 30,
    restDelta: 0.001,
  });

  return (
    <motion.div
      className="fixed top-0 left-0 right-0 h-1 bg-primary origin-left z-50"
      style={{ scaleX }}
    />
  );
}
```

### 22. 섹션 스냅 스크롤

```tsx
// components/ui/snap-scroll.tsx
'use client';

import { motion, useScroll, useTransform } from 'framer-motion';
import { ReactNode, useRef } from 'react';

interface SnapSectionProps {
  children: ReactNode;
  index: number;
}

export function SnapSection({ children, index }: SnapSectionProps) {
  const ref = useRef(null);
  const { scrollYProgress } = useScroll({
    target: ref,
    offset: ['start end', 'end start'],
  });

  const opacity = useTransform(
    scrollYProgress,
    [0, 0.3, 0.7, 1],
    [0, 1, 1, 0]
  );

  const scale = useTransform(
    scrollYProgress,
    [0, 0.3, 0.7, 1],
    [0.8, 1, 1, 0.8]
  );

  return (
    <motion.section
      ref={ref}
      className="min-h-screen flex items-center justify-center snap-start"
      style={{ opacity, scale }}
    >
      {children}
    </motion.section>
  );
}

export function SnapContainer({ children }: { children: ReactNode }) {
  return (
    <div className="h-screen overflow-y-auto snap-y snap-mandatory">
      {children}
    </div>
  );
}
```

---

## 접근성 고려사항

### 23. Reduced Motion 지원

```tsx
// hooks/use-reduced-motion.ts
'use client';

import { useEffect, useState } from 'react';

export function useReducedMotion(): boolean {
  const [prefersReducedMotion, setPrefersReducedMotion] = useState(false);

  useEffect(() => {
    const mediaQuery = window.matchMedia('(prefers-reduced-motion: reduce)');
    setPrefersReducedMotion(mediaQuery.matches);

    const handler = (event: MediaQueryListEvent) => {
      setPrefersReducedMotion(event.matches);
    };

    mediaQuery.addEventListener('change', handler);
    return () => mediaQuery.removeEventListener('change', handler);
  }, []);

  return prefersReducedMotion;
}
```

### 24. 접근성 친화적 애니메이션 컴포넌트

```tsx
// components/ui/accessible-motion.tsx
'use client';

import { motion, MotionProps, Transition } from 'framer-motion';
import { useReducedMotion } from '@/hooks/use-reduced-motion';
import { ComponentProps, forwardRef } from 'react';

type AccessibleMotionProps = MotionProps & {
  reducedMotionProps?: MotionProps;
};

// Create accessible motion components
function createAccessibleComponent<T extends keyof JSX.IntrinsicElements>(
  element: T
) {
  const MotionComponent = motion[element] as any;

  return forwardRef<HTMLElement, AccessibleMotionProps & ComponentProps<T>>(
    function AccessibleMotion(
      { reducedMotionProps, ...props },
      ref
    ) {
      const prefersReducedMotion = useReducedMotion();

      // If reduced motion is preferred, use simpler animations
      if (prefersReducedMotion) {
        return (
          <MotionComponent
            ref={ref}
            {...props}
            // Override with reduced motion props or use simple fade
            animate={reducedMotionProps?.animate ?? { opacity: 1 }}
            initial={reducedMotionProps?.initial ?? { opacity: 0 }}
            exit={reducedMotionProps?.exit ?? { opacity: 0 }}
            transition={{ duration: 0.01 }}
          />
        );
      }

      return <MotionComponent ref={ref} {...props} />;
    }
  );
}

export const AccessibleMotionDiv = createAccessibleComponent('div');
export const AccessibleMotionSpan = createAccessibleComponent('span');
```

### 25. 애니메이션 토글 컨텍스트

```tsx
// contexts/animation-context.tsx
'use client';

import { createContext, useContext, useState, ReactNode } from 'react';
import { useReducedMotion } from '@/hooks/use-reduced-motion';

interface AnimationContextType {
  animationsEnabled: boolean;
  toggleAnimations: () => void;
  getTransition: (transition: object) => object;
}

const AnimationContext = createContext<AnimationContextType | null>(null);

export function AnimationProvider({ children }: { children: ReactNode }) {
  const prefersReducedMotion = useReducedMotion();
  const [userOverride, setUserOverride] = useState<boolean | null>(null);

  const animationsEnabled = userOverride ?? !prefersReducedMotion;

  const toggleAnimations = () => {
    setUserOverride(prev => prev === null ? !prefersReducedMotion : !prev);
  };

  const getTransition = (transition: object) => {
    if (!animationsEnabled) {
      return { duration: 0 };
    }
    return transition;
  };

  return (
    <AnimationContext.Provider
      value={{ animationsEnabled, toggleAnimations, getTransition }}
    >
      {children}
    </AnimationContext.Provider>
  );
}

export function useAnimationSettings() {
  const context = useContext(AnimationContext);
  if (!context) {
    throw new Error('useAnimationSettings must be used within AnimationProvider');
  }
  return context;
}
```

---

## 고급 패턴

### 26. 인터랙티브 마우스 팔로우

```tsx
// components/ui/mouse-follow.tsx
'use client';

import { motion, useMotionValue, useSpring } from 'framer-motion';
import { useEffect, ReactNode } from 'react';

interface MouseFollowProps {
  children: ReactNode;
  springConfig?: { stiffness: number; damping: number };
}

export function MouseFollow({
  children,
  springConfig = { stiffness: 100, damping: 20 },
}: MouseFollowProps) {
  const mouseX = useMotionValue(0);
  const mouseY = useMotionValue(0);

  const springX = useSpring(mouseX, springConfig);
  const springY = useSpring(mouseY, springConfig);

  useEffect(() => {
    const handleMouseMove = (e: MouseEvent) => {
      mouseX.set(e.clientX);
      mouseY.set(e.clientY);
    };

    window.addEventListener('mousemove', handleMouseMove);
    return () => window.removeEventListener('mousemove', handleMouseMove);
  }, [mouseX, mouseY]);

  return (
    <motion.div
      className="pointer-events-none fixed z-50"
      style={{
        x: springX,
        y: springY,
        translateX: '-50%',
        translateY: '-50%',
      }}
    >
      {children}
    </motion.div>
  );
}

// Custom cursor example
export function CustomCursor() {
  return (
    <MouseFollow>
      <div className="w-4 h-4 rounded-full bg-primary mix-blend-difference" />
    </MouseFollow>
  );
}
```

### 27. 3D 카드 틸트

```tsx
// components/ui/tilt-card.tsx
'use client';

import { motion, useMotionValue, useSpring, useTransform } from 'framer-motion';
import { ReactNode, MouseEvent } from 'react';

interface TiltCardProps {
  children: ReactNode;
  className?: string;
}

export function TiltCard({ children, className }: TiltCardProps) {
  const x = useMotionValue(0.5);
  const y = useMotionValue(0.5);

  const rotateX = useSpring(useTransform(y, [0, 1], [10, -10]), {
    stiffness: 300,
    damping: 30,
  });
  const rotateY = useSpring(useTransform(x, [0, 1], [-10, 10]), {
    stiffness: 300,
    damping: 30,
  });

  const handleMouseMove = (e: MouseEvent<HTMLDivElement>) => {
    const rect = e.currentTarget.getBoundingClientRect();
    x.set((e.clientX - rect.left) / rect.width);
    y.set((e.clientY - rect.top) / rect.height);
  };

  const handleMouseLeave = () => {
    x.set(0.5);
    y.set(0.5);
  };

  return (
    <motion.div
      className={className}
      style={{
        rotateX,
        rotateY,
        transformStyle: 'preserve-3d',
        perspective: 1000,
      }}
      onMouseMove={handleMouseMove}
      onMouseLeave={handleMouseLeave}
    >
      {children}
    </motion.div>
  );
}
```

### 28. 텍스트 타이핑 애니메이션

```tsx
// components/ui/typing-text.tsx
'use client';

import { motion, useMotionValue, useTransform, animate } from 'framer-motion';
import { useEffect, useState } from 'react';

interface TypingTextProps {
  text: string;
  duration?: number;
  delay?: number;
}

export function TypingText({
  text,
  duration = 2,
  delay = 0,
}: TypingTextProps) {
  const [displayText, setDisplayText] = useState('');
  const count = useMotionValue(0);

  useEffect(() => {
    const controls = animate(count, text.length, {
      type: 'tween',
      duration,
      delay,
      ease: 'linear',
      onUpdate: (latest) => {
        setDisplayText(text.slice(0, Math.round(latest)));
      },
    });

    return controls.stop;
  }, [text, duration, delay, count]);

  return (
    <span>
      {displayText}
      <motion.span
        animate={{ opacity: [0, 1] }}
        transition={{ repeat: Infinity, duration: 0.5 }}
      >
        |
      </motion.span>
    </span>
  );
}

// Character by character animation
export function AnimatedText({ text }: { text: string }) {
  return (
    <motion.div
      initial="hidden"
      animate="visible"
      variants={{
        visible: { transition: { staggerChildren: 0.03 } },
      }}
    >
      {text.split('').map((char, index) => (
        <motion.span
          key={`${char}-${index}`}
          variants={{
            hidden: { opacity: 0, y: 20 },
            visible: { opacity: 1, y: 0 },
          }}
          className="inline-block"
        >
          {char === ' ' ? '\u00A0' : char}
        </motion.span>
      ))}
    </motion.div>
  );
}
```

### 29. 무한 스크롤 배너

```tsx
// components/ui/infinite-scroll-banner.tsx
'use client';

import { motion } from 'framer-motion';
import { ReactNode } from 'react';

interface InfiniteScrollBannerProps {
  children: ReactNode;
  speed?: number;
  direction?: 'left' | 'right';
}

export function InfiniteScrollBanner({
  children,
  speed = 25,
  direction = 'left',
}: InfiniteScrollBannerProps) {
  const directionValue = direction === 'left' ? -1 : 1;

  return (
    <div className="overflow-hidden whitespace-nowrap">
      <motion.div
        className="inline-flex"
        animate={{
          x: [`${directionValue * 0}%`, `${directionValue * -50}%`],
        }}
        transition={{
          x: {
            repeat: Infinity,
            repeatType: 'loop',
            duration: speed,
            ease: 'linear',
          },
        }}
      >
        {/* Duplicate content for seamless loop */}
        <div className="flex shrink-0">{children}</div>
        <div className="flex shrink-0">{children}</div>
      </motion.div>
    </div>
  );
}

// Usage
export function LogoBanner({ logos }: { logos: string[] }) {
  return (
    <InfiniteScrollBanner speed={30}>
      {logos.map((logo, i) => (
        <img
          key={i}
          src={logo}
          alt=""
          className="h-12 mx-8 grayscale hover:grayscale-0 transition-all"
        />
      ))}
    </InfiniteScrollBanner>
  );
}
```

### 30. 카운트다운 플립 애니메이션

```tsx
// components/ui/flip-counter.tsx
'use client';

import { motion, AnimatePresence } from 'framer-motion';
import { useEffect, useState } from 'react';

interface FlipDigitProps {
  digit: number;
}

function FlipDigit({ digit }: FlipDigitProps) {
  return (
    <div className="relative w-12 h-16 bg-card rounded-lg overflow-hidden shadow-lg">
      <AnimatePresence mode="popLayout">
        <motion.div
          key={digit}
          className="absolute inset-0 flex items-center justify-center text-3xl font-bold"
          initial={{ rotateX: -90, opacity: 0 }}
          animate={{ rotateX: 0, opacity: 1 }}
          exit={{ rotateX: 90, opacity: 0 }}
          transition={{
            type: 'spring',
            stiffness: 300,
            damping: 30,
          }}
          style={{ transformOrigin: 'bottom center' }}
        >
          {digit}
        </motion.div>
      </AnimatePresence>
      {/* Center line */}
      <div className="absolute inset-x-0 top-1/2 h-px bg-border" />
    </div>
  );
}

interface CountdownProps {
  targetDate: Date;
}

export function Countdown({ targetDate }: CountdownProps) {
  const [timeLeft, setTimeLeft] = useState({
    days: 0,
    hours: 0,
    minutes: 0,
    seconds: 0,
  });

  useEffect(() => {
    const timer = setInterval(() => {
      const now = new Date().getTime();
      const target = targetDate.getTime();
      const diff = target - now;

      if (diff > 0) {
        setTimeLeft({
          days: Math.floor(diff / (1000 * 60 * 60 * 24)),
          hours: Math.floor((diff % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60)),
          minutes: Math.floor((diff % (1000 * 60 * 60)) / (1000 * 60)),
          seconds: Math.floor((diff % (1000 * 60)) / 1000),
        });
      }
    }, 1000);

    return () => clearInterval(timer);
  }, [targetDate]);

  const formatDigits = (num: number): [number, number] => {
    return [Math.floor(num / 10), num % 10];
  };

  return (
    <div className="flex gap-4">
      {Object.entries(timeLeft).map(([unit, value]) => {
        const [tens, ones] = formatDigits(value);
        return (
          <div key={unit} className="text-center">
            <div className="flex gap-1">
              <FlipDigit digit={tens} />
              <FlipDigit digit={ones} />
            </div>
            <span className="text-sm text-muted-foreground mt-2 block capitalize">
              {unit}
            </span>
          </div>
        );
      })}
    </div>
  );
}
```

### 추가 유틸리티 함수

```tsx
// lib/motion/utils.ts
import { Variants } from 'framer-motion';

/**
 * Create stagger variants with custom settings
 */
export function createStaggerVariants(
  staggerDelay: number = 0.1,
  initialY: number = 20
): { container: Variants; item: Variants } {
  return {
    container: {
      hidden: { opacity: 0 },
      visible: {
        opacity: 1,
        transition: { staggerChildren: staggerDelay },
      },
    },
    item: {
      hidden: { opacity: 0, y: initialY },
      visible: { opacity: 1, y: 0 },
    },
  };
}

/**
 * Create fade in variants with direction
 */
export function createFadeInVariants(
  direction: 'up' | 'down' | 'left' | 'right' = 'up',
  distance: number = 20
): Variants {
  const directionMap = {
    up: { y: distance },
    down: { y: -distance },
    left: { x: distance },
    right: { x: -distance },
  };

  return {
    hidden: { opacity: 0, ...directionMap[direction] },
    visible: {
      opacity: 1,
      x: 0,
      y: 0,
      transition: { duration: 0.6, ease: [0.25, 0.1, 0.25, 1] },
    },
  };
}

/**
 * Create scale variants
 */
export function createScaleVariants(
  scale: number = 0.95,
  duration: number = 0.3
): Variants {
  return {
    hidden: { opacity: 0, scale },
    visible: {
      opacity: 1,
      scale: 1,
      transition: {
        type: 'spring',
        stiffness: 300,
        damping: 30,
      },
    },
  };
}
```
