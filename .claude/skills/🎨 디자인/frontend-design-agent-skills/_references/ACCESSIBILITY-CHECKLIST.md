# ACCESSIBILITY-CHECKLIST.md

WCAG 2.2 기반 접근성 체크리스트와 구현 가이드

---

## 목차

1. [WCAG 2.2 핵심 요구사항](#wcag-22-핵심-요구사항)
2. [뉴로다양성 고려사항](#뉴로다양성-고려사항)
3. [모션 민감도](#모션-민감도)
4. [색상 대비 검증](#색상-대비-검증)
5. [키보드 네비게이션](#키보드-네비게이션)
6. [스크린 리더 호환성](#스크린-리더-호환성)
7. [실전 코드 패턴](#실전-코드-패턴)

---

## WCAG 2.2 핵심 요구사항

### 레벨별 요구사항 요약

| 레벨 | 대상 | 주요 요구사항 |
|------|------|--------------|
| **A** | 필수 | 기본 접근성 - 모든 웹사이트 충족 필요 |
| **AA** | 권장 | 대부분 조직의 법적 요구사항 |
| **AAA** | 이상적 | 최고 수준 접근성 |

### WCAG 2.2 새로운 기준

#### 2.4.11 Focus Not Obscured (Minimum) - AA

```tsx
// BAD: Focus hidden by sticky header
function BadStickyHeader() {
  return (
    <header className="fixed top-0 z-50 bg-background">
      {/* Focus on elements below can be hidden */}
    </header>
  );
}

// GOOD: Scroll padding for focus
export function GoodLayout() {
  return (
    <>
      <style>{`
        html {
          scroll-padding-top: 80px; /* Match header height */
        }
      `}</style>
      <header className="fixed top-0 h-16 z-50 bg-background">
        <nav>{/* Navigation */}</nav>
      </header>
      <main className="mt-16">
        {/* Content */}
      </main>
    </>
  );
}
```

#### 2.4.12 Focus Not Obscured (Enhanced) - AAA

```css
/* Ensure focus is never fully obscured */
:focus {
  scroll-margin: 100px; /* Extra margin for focus */
}

/* Handle modals/overlays */
[aria-hidden="true"] {
  pointer-events: none;
}
```

#### 2.5.7 Dragging Movements - AA

```tsx
// BAD: Drag-only slider
function BadSlider() {
  return <input type="range" /> // No keyboard alternative
}

// GOOD: Multiple input methods
function GoodSlider({ value, onChange, min, max, step }: SliderProps) {
  return (
    <div className="flex items-center gap-4">
      {/* Decrement button */}
      <button
        onClick={() => onChange(Math.max(min, value - step))}
        aria-label="Decrease value"
        className="p-2 rounded-lg border hover:bg-muted"
      >
        <Minus className="w-4 h-4" />
      </button>

      {/* Range slider */}
      <input
        type="range"
        value={value}
        onChange={(e) => onChange(Number(e.target.value))}
        min={min}
        max={max}
        step={step}
        className="flex-1"
        aria-valuemin={min}
        aria-valuemax={max}
        aria-valuenow={value}
      />

      {/* Increment button */}
      <button
        onClick={() => onChange(Math.min(max, value + step))}
        aria-label="Increase value"
        className="p-2 rounded-lg border hover:bg-muted"
      >
        <Plus className="w-4 h-4" />
      </button>

      {/* Direct input */}
      <input
        type="number"
        value={value}
        onChange={(e) => onChange(Number(e.target.value))}
        min={min}
        max={max}
        className="w-16 px-2 py-1 border rounded text-center"
        aria-label="Enter value directly"
      />
    </div>
  );
}
```

#### 2.5.8 Target Size (Minimum) - AA

```css
/* Minimum target size: 24x24 CSS pixels */
.interactive-element {
  min-width: 24px;
  min-height: 24px;
}

/* Recommended: 44x44 for touch */
.touch-target {
  min-width: 44px;
  min-height: 44px;
}

/* For inline links, use adequate padding */
.inline-link {
  padding: 4px; /* Adds to target size */
}
```

```tsx
// components/ui/accessible-button.tsx
import { cn } from '@/lib/utils';
import { ReactNode } from 'react';

interface AccessibleButtonProps {
  children: ReactNode;
  className?: string;
  size?: 'sm' | 'md' | 'lg';
}

const sizeClasses = {
  sm: 'min-h-8 min-w-8 px-3', // 32px - meets AA
  md: 'min-h-10 min-w-10 px-4', // 40px
  lg: 'min-h-12 min-w-12 px-6', // 48px - exceeds AAA
};

export function AccessibleButton({
  children,
  className,
  size = 'md',
  ...props
}: AccessibleButtonProps) {
  return (
    <button
      className={cn(
        'inline-flex items-center justify-center rounded-lg',
        'focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring',
        sizeClasses[size],
        className
      )}
      {...props}
    >
      {children}
    </button>
  );
}
```

#### 3.2.6 Consistent Help - A

```tsx
// components/ui/consistent-help.tsx
'use client';

import { HelpCircle, MessageCircle, Mail, Phone } from 'lucide-react';

// Help should be in consistent location across pages
export function ConsistentHelp() {
  return (
    <footer className="border-t py-8 mt-auto">
      <div className="container">
        <div className="flex flex-wrap gap-6 justify-center">
          <a
            href="/help"
            className="flex items-center gap-2 text-muted-foreground hover:text-foreground"
          >
            <HelpCircle className="w-5 h-5" />
            <span>Help Center</span>
          </a>
          <a
            href="/contact"
            className="flex items-center gap-2 text-muted-foreground hover:text-foreground"
          >
            <MessageCircle className="w-5 h-5" />
            <span>Live Chat</span>
          </a>
          <a
            href="mailto:support@example.com"
            className="flex items-center gap-2 text-muted-foreground hover:text-foreground"
          >
            <Mail className="w-5 h-5" />
            <span>Email Support</span>
          </a>
          <a
            href="tel:+1234567890"
            className="flex items-center gap-2 text-muted-foreground hover:text-foreground"
          >
            <Phone className="w-5 h-5" />
            <span>Phone</span>
          </a>
        </div>
      </div>
    </footer>
  );
}
```

---

## 뉴로다양성 고려사항

### ADHD 친화적 디자인

```tsx
// components/adhd-friendly/clear-hierarchy.tsx

// 1. Clear visual hierarchy
export function ClearHierarchy() {
  return (
    <article className="space-y-6">
      {/* Large, bold headings */}
      <h1 className="text-4xl font-bold">Main Topic</h1>

      {/* Clear section breaks */}
      <section className="p-6 bg-card rounded-xl border">
        <h2 className="text-2xl font-semibold mb-4">Section Title</h2>

        {/* Short paragraphs */}
        <p className="text-muted-foreground mb-4">
          Keep paragraphs short. One idea per paragraph.
        </p>

        {/* Bullet points for lists */}
        <ul className="list-disc list-inside space-y-2">
          <li>Clear, concise points</li>
          <li>Easy to scan</li>
          <li>Reduces cognitive load</li>
        </ul>
      </section>
    </article>
  );
}

// 2. Progress indicators
export function ProgressIndicator({ current, total }: { current: number; total: number }) {
  return (
    <div className="flex items-center gap-4">
      {/* Visual progress */}
      <div className="flex gap-1">
        {Array.from({ length: total }).map((_, i) => (
          <div
            key={i}
            className={`w-8 h-2 rounded-full transition-colors ${
              i < current ? 'bg-primary' : 'bg-muted'
            }`}
          />
        ))}
      </div>

      {/* Text indicator */}
      <span className="text-sm text-muted-foreground">
        Step {current} of {total}
      </span>
    </div>
  );
}

// 3. Reduce distractions
export function FocusMode() {
  return (
    <div className="relative">
      {/* Clean, minimal interface */}
      <main className="max-w-2xl mx-auto py-12 px-4">
        {/* Single column layout */}
        <article className="prose prose-lg">
          {/* Content without sidebars or ads */}
        </article>
      </main>

      {/* Optional: Focus mode toggle */}
      <button
        className="fixed bottom-4 right-4 p-3 rounded-full bg-card border shadow-lg"
        aria-label="Toggle focus mode"
      >
        <Eye className="w-5 h-5" />
      </button>
    </div>
  );
}
```

### 자폐 스펙트럼 친화적 디자인

```tsx
// components/autism-friendly/predictable-ui.tsx

// 1. Predictable patterns
export function PredictableNavigation() {
  return (
    <nav className="flex gap-1">
      {/* Consistent button style */}
      {[
        { href: '/', label: 'Home', icon: Home },
        { href: '/products', label: 'Products', icon: Box },
        { href: '/about', label: 'About', icon: Info },
        { href: '/contact', label: 'Contact', icon: Mail },
      ].map((item) => (
        <Link
          key={item.href}
          href={item.href}
          className="flex items-center gap-2 px-4 py-2 rounded-lg hover:bg-muted transition-colors"
        >
          <item.icon className="w-5 h-5" />
          <span>{item.label}</span>
        </Link>
      ))}
    </nav>
  );
}

// 2. Clear expectations
export function ClearInstructions() {
  return (
    <form className="space-y-6">
      <div>
        {/* Explicit labels */}
        <label className="block text-sm font-medium mb-2">
          Email Address
          <span className="text-muted-foreground ml-1">(required)</span>
        </label>

        {/* Clear placeholder */}
        <input
          type="email"
          placeholder="example@email.com"
          required
          className="w-full px-4 py-2 border rounded-lg"
        />

        {/* Helper text */}
        <p className="mt-1 text-sm text-muted-foreground">
          We will send a confirmation to this email.
        </p>
      </div>

      {/* Clear button text */}
      <button
        type="submit"
        className="w-full py-3 bg-primary text-primary-foreground rounded-lg font-medium"
      >
        Submit Form
      </button>
    </form>
  );
}

// 3. Avoid ambiguity
export function UnambiguousUI() {
  return (
    <div className="space-y-4">
      {/* Clear, literal labels - no idioms */}
      <button className="px-4 py-2 bg-primary text-primary-foreground rounded-lg">
        Save Changes {/* Not "Push it live" or "Ship it" */}
      </button>

      <button className="px-4 py-2 border rounded-lg">
        Cancel {/* Not "Nevermind" or "Bail" */}
      </button>

      {/* Avoid metaphors in icons without labels */}
      <button className="flex items-center gap-2 px-4 py-2 border rounded-lg">
        <Trash2 className="w-4 h-4" />
        <span>Delete Item</span> {/* Always include text */}
      </button>
    </div>
  );
}
```

### 난독증 친화적 디자인

```css
/* styles/dyslexia-friendly.css */

/* Font recommendations */
.dyslexia-friendly {
  /* Use sans-serif with clear letter shapes */
  font-family: 'Lexend', 'Atkinson Hyperlegible', sans-serif;

  /* Increased letter spacing */
  letter-spacing: 0.05em;

  /* Increased word spacing */
  word-spacing: 0.1em;

  /* Increased line height */
  line-height: 1.8;

  /* Limit line length */
  max-width: 70ch;

  /* Left alignment (not justified) */
  text-align: left;
}

/* Avoid */
.avoid-for-dyslexia {
  /* Don't use italic for long text */
  font-style: italic; /* BAD for body text */

  /* Don't use all caps */
  text-transform: uppercase; /* BAD for sentences */

  /* Don't justify text */
  text-align: justify; /* Creates uneven spacing */

  /* Don't use pure black on white */
  color: #000;
  background: #fff; /* Too high contrast can cause glare */
}

/* Better contrast */
.comfortable-contrast {
  color: oklch(20% 0.02 250); /* Soft black */
  background: oklch(97% 0.01 250); /* Off-white */
}
```

```tsx
// components/dyslexia-friendly/readable-text.tsx
export function ReadableText({ children }: { children: React.ReactNode }) {
  return (
    <div
      className="text-lg leading-loose tracking-wide"
      style={{
        fontFamily: '"Lexend", "Atkinson Hyperlegible", sans-serif',
        wordSpacing: '0.1em',
        maxWidth: '70ch',
      }}
    >
      {children}
    </div>
  );
}

// Reading ruler component
export function ReadingRuler() {
  const [position, setPosition] = useState(0);

  useEffect(() => {
    const handleMouseMove = (e: MouseEvent) => {
      setPosition(e.clientY);
    };
    window.addEventListener('mousemove', handleMouseMove);
    return () => window.removeEventListener('mousemove', handleMouseMove);
  }, []);

  return (
    <div
      className="fixed left-0 right-0 pointer-events-none z-50"
      style={{ top: position - 15, height: 30 }}
    >
      <div className="h-full bg-yellow-200/30 border-y border-yellow-400/50" />
    </div>
  );
}
```

---

## 모션 민감도

### prefers-reduced-motion 구현

```css
/* styles/reduced-motion.css */

/* Default animations */
.animate-fade-in {
  animation: fadeIn 0.3s ease-out;
}

.animate-slide-up {
  animation: slideUp 0.4s ease-out;
}

@keyframes fadeIn {
  from { opacity: 0; }
  to { opacity: 1; }
}

@keyframes slideUp {
  from { opacity: 0; transform: translateY(20px); }
  to { opacity: 1; transform: translateY(0); }
}

/* Reduce motion when preferred */
@media (prefers-reduced-motion: reduce) {
  *,
  *::before,
  *::after {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
    scroll-behavior: auto !important;
  }

  /* Keep essential animations but simplify */
  .essential-animation {
    animation: none;
    /* Show final state instead */
    opacity: 1;
    transform: none;
  }
}
```

### React Hook for Reduced Motion

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

### 안전한 Framer Motion 패턴

```tsx
// components/motion/safe-motion.tsx
'use client';

import { motion, MotionProps, Variant } from 'framer-motion';
import { useReducedMotion } from '@/hooks/use-reduced-motion';
import { ReactNode } from 'react';

interface SafeMotionProps extends MotionProps {
  children: ReactNode;
  className?: string;
}

export function SafeMotion({
  children,
  className,
  initial,
  animate,
  exit,
  transition,
  ...props
}: SafeMotionProps) {
  const prefersReducedMotion = useReducedMotion();

  if (prefersReducedMotion) {
    // Render static element
    return <div className={className}>{children}</div>;
  }

  return (
    <motion.div
      className={className}
      initial={initial}
      animate={animate}
      exit={exit}
      transition={transition}
      {...props}
    >
      {children}
    </motion.div>
  );
}

// Fade-only animation (safer for vestibular)
export function SafeFade({ children, className }: { children: ReactNode; className?: string }) {
  const prefersReducedMotion = useReducedMotion();

  return (
    <motion.div
      className={className}
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      transition={{
        duration: prefersReducedMotion ? 0 : 0.3,
      }}
    >
      {children}
    </motion.div>
  );
}

// Completely disable motion variant
export function createReducedMotionVariants(
  fullVariants: { hidden: Variant; visible: Variant },
  reducedVariants?: { hidden: Variant; visible: Variant }
) {
  return {
    full: fullVariants,
    reduced: reducedVariants || {
      hidden: { opacity: 0 },
      visible: { opacity: 1 },
    },
  };
}
```

### 자동재생 콘텐츠 제어

```tsx
// components/video/accessible-video.tsx
'use client';

import { useReducedMotion } from '@/hooks/use-reduced-motion';
import { useRef, useState, useEffect } from 'react';
import { Play, Pause } from 'lucide-react';

interface AccessibleVideoProps {
  src: string;
  poster?: string;
}

export function AccessibleVideo({ src, poster }: AccessibleVideoProps) {
  const videoRef = useRef<HTMLVideoElement>(null);
  const prefersReducedMotion = useReducedMotion();
  const [isPlaying, setIsPlaying] = useState(false);

  useEffect(() => {
    // Auto-pause if reduced motion preferred
    if (prefersReducedMotion && videoRef.current) {
      videoRef.current.pause();
      setIsPlaying(false);
    }
  }, [prefersReducedMotion]);

  const togglePlay = () => {
    if (videoRef.current) {
      if (isPlaying) {
        videoRef.current.pause();
      } else {
        videoRef.current.play();
      }
      setIsPlaying(!isPlaying);
    }
  };

  return (
    <div className="relative group">
      <video
        ref={videoRef}
        src={src}
        poster={poster}
        loop
        muted
        playsInline
        // Never autoplay
        autoPlay={false}
        className="w-full rounded-xl"
      />

      {/* Always visible controls */}
      <button
        onClick={togglePlay}
        className="absolute bottom-4 right-4 p-3 rounded-full bg-background/80 backdrop-blur-sm shadow-lg"
        aria-label={isPlaying ? 'Pause video' : 'Play video'}
      >
        {isPlaying ? (
          <Pause className="w-5 h-5" />
        ) : (
          <Play className="w-5 h-5" />
        )}
      </button>

      {/* Reduced motion notice */}
      {prefersReducedMotion && !isPlaying && (
        <div className="absolute inset-0 flex items-center justify-center bg-background/60 rounded-xl">
          <p className="text-center p-4">
            Video paused due to motion preferences.
            <button
              onClick={togglePlay}
              className="block mx-auto mt-2 text-primary underline"
            >
              Play anyway
            </button>
          </p>
        </div>
      )}
    </div>
  );
}
```

---

## 색상 대비 검증

### OKLCH 기반 대비 계산

```typescript
// lib/a11y/contrast.ts

/**
 * Calculate relative luminance from OKLCH lightness
 * Approximation based on OKLCH L value
 */
function getLuminance(lightness: number): number {
  // OKLCH lightness is already perceptually uniform
  // Convert to relative luminance approximation
  return Math.pow(lightness, 2.4);
}

/**
 * Calculate WCAG contrast ratio
 */
export function getContrastRatio(l1: number, l2: number): number {
  const lum1 = getLuminance(l1);
  const lum2 = getLuminance(l2);

  const lighter = Math.max(lum1, lum2);
  const darker = Math.min(lum1, lum2);

  return (lighter + 0.05) / (darker + 0.05);
}

/**
 * Check WCAG compliance
 */
export function checkWCAG(
  foregroundL: number,
  backgroundL: number
): {
  ratio: number;
  AANormal: boolean;
  AALarge: boolean;
  AAANormal: boolean;
  AAALarge: boolean;
} {
  const ratio = getContrastRatio(foregroundL, backgroundL);

  return {
    ratio: Math.round(ratio * 100) / 100,
    AANormal: ratio >= 4.5,
    AALarge: ratio >= 3,
    AAANormal: ratio >= 7,
    AAALarge: ratio >= 4.5,
  };
}

/**
 * Find accessible text color for a background
 */
export function getAccessibleTextColor(
  backgroundL: number,
  targetRatio: number = 4.5
): number {
  // Try dark text first (more common)
  for (let l = 0; l < 0.5; l += 0.01) {
    if (getContrastRatio(l, backgroundL) >= targetRatio) {
      return l;
    }
  }

  // Try light text
  for (let l = 1; l > 0.5; l -= 0.01) {
    if (getContrastRatio(l, backgroundL) >= targetRatio) {
      return l;
    }
  }

  // Return extreme if no match
  return backgroundL > 0.5 ? 0 : 1;
}
```

### 대비 검사 컴포넌트

```tsx
// components/dev/contrast-checker.tsx
'use client';

import { useState, useMemo } from 'react';
import { checkWCAG } from '@/lib/a11y/contrast';
import { Check, X } from 'lucide-react';

export function ContrastChecker() {
  const [bgLightness, setBgLightness] = useState(0.95);
  const [fgLightness, setFgLightness] = useState(0.15);

  const results = useMemo(
    () => checkWCAG(fgLightness, bgLightness),
    [fgLightness, bgLightness]
  );

  const PassFail = ({ pass }: { pass: boolean }) => (
    <span className={`flex items-center gap-1 ${pass ? 'text-success' : 'text-error'}`}>
      {pass ? <Check className="w-4 h-4" /> : <X className="w-4 h-4" />}
      {pass ? 'Pass' : 'Fail'}
    </span>
  );

  return (
    <div className="p-6 rounded-xl border bg-card space-y-6">
      <h3 className="text-lg font-semibold">Contrast Checker</h3>

      <div className="grid grid-cols-2 gap-6">
        <div>
          <label className="block text-sm mb-2">
            Background: {Math.round(bgLightness * 100)}%
          </label>
          <input
            type="range"
            min="0"
            max="100"
            value={bgLightness * 100}
            onChange={(e) => setBgLightness(Number(e.target.value) / 100)}
            className="w-full"
          />
        </div>
        <div>
          <label className="block text-sm mb-2">
            Foreground: {Math.round(fgLightness * 100)}%
          </label>
          <input
            type="range"
            min="0"
            max="100"
            value={fgLightness * 100}
            onChange={(e) => setFgLightness(Number(e.target.value) / 100)}
            className="w-full"
          />
        </div>
      </div>

      {/* Preview */}
      <div
        className="p-8 rounded-lg text-center"
        style={{
          backgroundColor: `oklch(${bgLightness * 100}% 0 0)`,
          color: `oklch(${fgLightness * 100}% 0 0)`,
        }}
      >
        <p className="text-2xl font-bold">Sample Text</p>
        <p className="text-sm mt-2">Small text preview</p>
      </div>

      {/* Results */}
      <div className="grid grid-cols-2 gap-4 text-sm">
        <div className="p-4 rounded-lg bg-muted">
          <p className="font-medium mb-2">Contrast Ratio</p>
          <p className="text-2xl font-bold">{results.ratio}:1</p>
        </div>
        <div className="p-4 rounded-lg bg-muted space-y-2">
          <div className="flex justify-between">
            <span>AA Normal (4.5:1)</span>
            <PassFail pass={results.AANormal} />
          </div>
          <div className="flex justify-between">
            <span>AA Large (3:1)</span>
            <PassFail pass={results.AALarge} />
          </div>
          <div className="flex justify-between">
            <span>AAA Normal (7:1)</span>
            <PassFail pass={results.AAANormal} />
          </div>
          <div className="flex justify-between">
            <span>AAA Large (4.5:1)</span>
            <PassFail pass={results.AAALarge} />
          </div>
        </div>
      </div>
    </div>
  );
}
```

---

## 키보드 네비게이션

### Focus 관리

```css
/* styles/focus.css */

/* Remove default focus, add custom */
:focus {
  outline: none;
}

:focus-visible {
  outline: 2px solid var(--ring);
  outline-offset: 2px;
}

/* Skip link */
.skip-link {
  position: absolute;
  top: -100px;
  left: 0;
  padding: 1rem;
  background: var(--background);
  z-index: 100;
}

.skip-link:focus {
  top: 0;
}

/* Focus within for containers */
.focus-within-ring:focus-within {
  outline: 2px solid var(--ring);
  outline-offset: 2px;
}
```

```tsx
// components/a11y/skip-link.tsx
export function SkipLink() {
  return (
    <a
      href="#main-content"
      className="sr-only focus:not-sr-only focus:absolute focus:top-4 focus:left-4 focus:z-50 focus:px-4 focus:py-2 focus:bg-background focus:rounded-lg focus:shadow-lg"
    >
      Skip to main content
    </a>
  );
}
```

### Focus Trap

```tsx
// hooks/use-focus-trap.ts
'use client';

import { useEffect, useRef } from 'react';

export function useFocusTrap<T extends HTMLElement>(isActive: boolean) {
  const containerRef = useRef<T>(null);

  useEffect(() => {
    if (!isActive || !containerRef.current) return;

    const container = containerRef.current;
    const focusableElements = container.querySelectorAll<HTMLElement>(
      'button, [href], input, select, textarea, [tabindex]:not([tabindex="-1"])'
    );

    const firstElement = focusableElements[0];
    const lastElement = focusableElements[focusableElements.length - 1];

    // Focus first element on mount
    firstElement?.focus();

    const handleKeyDown = (e: KeyboardEvent) => {
      if (e.key !== 'Tab') return;

      if (e.shiftKey) {
        // Shift + Tab
        if (document.activeElement === firstElement) {
          e.preventDefault();
          lastElement?.focus();
        }
      } else {
        // Tab
        if (document.activeElement === lastElement) {
          e.preventDefault();
          firstElement?.focus();
        }
      }
    };

    container.addEventListener('keydown', handleKeyDown);
    return () => container.removeEventListener('keydown', handleKeyDown);
  }, [isActive]);

  return containerRef;
}

// Usage in Modal
export function Modal({ isOpen, onClose, children }: ModalProps) {
  const modalRef = useFocusTrap<HTMLDivElement>(isOpen);

  if (!isOpen) return null;

  return (
    <div
      ref={modalRef}
      role="dialog"
      aria-modal="true"
      className="fixed inset-0 z-50 flex items-center justify-center"
    >
      {children}
    </div>
  );
}
```

### Roving Tabindex

```tsx
// components/a11y/roving-tabindex.tsx
'use client';

import { useState, KeyboardEvent, ReactNode, Children, cloneElement, isValidElement } from 'react';

interface RovingTabindexProps {
  children: ReactNode;
  orientation?: 'horizontal' | 'vertical';
}

export function RovingTabindex({
  children,
  orientation = 'horizontal',
}: RovingTabindexProps) {
  const [activeIndex, setActiveIndex] = useState(0);
  const items = Children.toArray(children).filter(isValidElement);

  const handleKeyDown = (e: KeyboardEvent, index: number) => {
    const prevKey = orientation === 'horizontal' ? 'ArrowLeft' : 'ArrowUp';
    const nextKey = orientation === 'horizontal' ? 'ArrowRight' : 'ArrowDown';

    let newIndex = index;

    if (e.key === nextKey) {
      e.preventDefault();
      newIndex = (index + 1) % items.length;
    } else if (e.key === prevKey) {
      e.preventDefault();
      newIndex = (index - 1 + items.length) % items.length;
    } else if (e.key === 'Home') {
      e.preventDefault();
      newIndex = 0;
    } else if (e.key === 'End') {
      e.preventDefault();
      newIndex = items.length - 1;
    }

    if (newIndex !== index) {
      setActiveIndex(newIndex);
      // Focus the new element
      const element = document.querySelector(
        `[data-roving-index="${newIndex}"]`
      ) as HTMLElement;
      element?.focus();
    }
  };

  return (
    <div role="group">
      {items.map((child, index) =>
        cloneElement(child as React.ReactElement, {
          tabIndex: index === activeIndex ? 0 : -1,
          'data-roving-index': index,
          onKeyDown: (e: KeyboardEvent) => handleKeyDown(e, index),
          onFocus: () => setActiveIndex(index),
        })
      )}
    </div>
  );
}
```

---

## 스크린 리더 호환성

### ARIA 패턴

```tsx
// components/a11y/aria-patterns.tsx

// 1. Live Region
export function LiveRegion({ message, type = 'polite' }: {
  message: string;
  type?: 'polite' | 'assertive';
}) {
  return (
    <div
      role="status"
      aria-live={type}
      aria-atomic="true"
      className="sr-only"
    >
      {message}
    </div>
  );
}

// 2. Accessible Toggle Button
export function AccessibleToggle({
  pressed,
  onToggle,
  label,
}: {
  pressed: boolean;
  onToggle: () => void;
  label: string;
}) {
  return (
    <button
      aria-pressed={pressed}
      onClick={onToggle}
      className={`px-4 py-2 rounded-lg ${
        pressed ? 'bg-primary text-primary-foreground' : 'bg-muted'
      }`}
    >
      {label}
    </button>
  );
}

// 3. Accessible Tabs
export function AccessibleTabs({
  tabs,
  activeTab,
  onTabChange,
}: {
  tabs: { id: string; label: string; content: React.ReactNode }[];
  activeTab: string;
  onTabChange: (id: string) => void;
}) {
  return (
    <div>
      <div role="tablist" aria-label="Content tabs" className="flex gap-1">
        {tabs.map((tab) => (
          <button
            key={tab.id}
            role="tab"
            id={`tab-${tab.id}`}
            aria-selected={activeTab === tab.id}
            aria-controls={`panel-${tab.id}`}
            onClick={() => onTabChange(tab.id)}
            className={`px-4 py-2 rounded-lg ${
              activeTab === tab.id
                ? 'bg-primary text-primary-foreground'
                : 'bg-muted'
            }`}
          >
            {tab.label}
          </button>
        ))}
      </div>

      {tabs.map((tab) => (
        <div
          key={tab.id}
          role="tabpanel"
          id={`panel-${tab.id}`}
          aria-labelledby={`tab-${tab.id}`}
          hidden={activeTab !== tab.id}
          className="mt-4"
        >
          {tab.content}
        </div>
      ))}
    </div>
  );
}

// 4. Accessible Accordion
export function AccessibleAccordion({
  items,
}: {
  items: { id: string; title: string; content: React.ReactNode }[];
}) {
  const [expandedItems, setExpandedItems] = useState<Set<string>>(new Set());

  const toggle = (id: string) => {
    setExpandedItems((prev) => {
      const next = new Set(prev);
      if (next.has(id)) {
        next.delete(id);
      } else {
        next.add(id);
      }
      return next;
    });
  };

  return (
    <div className="divide-y">
      {items.map((item) => {
        const isExpanded = expandedItems.has(item.id);

        return (
          <div key={item.id}>
            <h3>
              <button
                id={`accordion-header-${item.id}`}
                aria-expanded={isExpanded}
                aria-controls={`accordion-panel-${item.id}`}
                onClick={() => toggle(item.id)}
                className="w-full py-4 flex items-center justify-between text-left"
              >
                {item.title}
                <ChevronDown
                  className={`w-5 h-5 transition-transform ${
                    isExpanded ? 'rotate-180' : ''
                  }`}
                />
              </button>
            </h3>
            <div
              id={`accordion-panel-${item.id}`}
              role="region"
              aria-labelledby={`accordion-header-${item.id}`}
              hidden={!isExpanded}
              className="pb-4"
            >
              {item.content}
            </div>
          </div>
        );
      })}
    </div>
  );
}
```

### 스크린 리더 전용 텍스트

```tsx
// components/ui/sr-only.tsx
interface SrOnlyProps {
  children: React.ReactNode;
  as?: 'span' | 'div' | 'p';
}

export function SrOnly({ children, as: Component = 'span' }: SrOnlyProps) {
  return (
    <Component className="sr-only">
      {children}
    </Component>
  );
}

// Usage examples
export function IconButton() {
  return (
    <button className="p-2 rounded-lg">
      <Settings className="w-5 h-5" aria-hidden="true" />
      <SrOnly>Open settings</SrOnly>
    </button>
  );
}

export function DataTable() {
  return (
    <table>
      <caption className="sr-only">
        Sales data for Q4 2024
      </caption>
      {/* Table content */}
    </table>
  );
}
```

---

## 실전 코드 패턴

### 접근성 완전 체크리스트 컴포넌트

```tsx
// components/dev/a11y-checklist.tsx
'use client';

import { useState } from 'react';
import { Check, X, AlertCircle } from 'lucide-react';

const CHECKLIST = {
  perceivable: {
    title: '인지 가능',
    items: [
      { id: 'alt-text', text: '모든 이미지에 대체 텍스트 제공', level: 'A' },
      { id: 'color-contrast', text: '텍스트 대비율 4.5:1 이상 (일반), 3:1 이상 (큰 텍스트)', level: 'AA' },
      { id: 'resize-text', text: '200% 확대해도 콘텐츠 손실 없음', level: 'AA' },
      { id: 'color-alone', text: '색상만으로 정보 전달하지 않음', level: 'A' },
      { id: 'captions', text: '비디오에 자막 제공', level: 'A' },
      { id: 'responsive', text: '가로/세로 모드 모두 지원', level: 'AA' },
    ],
  },
  operable: {
    title: '운용 가능',
    items: [
      { id: 'keyboard', text: '모든 기능 키보드로 접근 가능', level: 'A' },
      { id: 'focus-visible', text: '포커스 상태 시각적으로 표시', level: 'AA' },
      { id: 'skip-link', text: '건너뛰기 링크 제공', level: 'A' },
      { id: 'no-trap', text: '키보드 트랩 없음', level: 'A' },
      { id: 'target-size', text: '터치 타겟 최소 24x24px', level: 'AA' },
      { id: 'motion-control', text: '자동 재생 콘텐츠 제어 가능', level: 'A' },
      { id: 'reduced-motion', text: 'prefers-reduced-motion 지원', level: 'AAA' },
    ],
  },
  understandable: {
    title: '이해 가능',
    items: [
      { id: 'lang', text: '페이지 언어 명시 (lang 속성)', level: 'A' },
      { id: 'labels', text: '폼 요소에 레이블 연결', level: 'A' },
      { id: 'error-msg', text: '오류 메시지 명확하게 표시', level: 'A' },
      { id: 'consistent-nav', text: '일관된 네비게이션', level: 'AA' },
      { id: 'help', text: '도움말 접근 일관성', level: 'A' },
    ],
  },
  robust: {
    title: '견고함',
    items: [
      { id: 'valid-html', text: 'HTML 유효성 검증', level: 'A' },
      { id: 'aria', text: 'ARIA 속성 올바르게 사용', level: 'A' },
      { id: 'name-role', text: '모든 컴포넌트에 이름과 역할', level: 'A' },
    ],
  },
};

export function A11yChecklist() {
  const [checked, setChecked] = useState<Set<string>>(new Set());

  const toggle = (id: string) => {
    setChecked((prev) => {
      const next = new Set(prev);
      if (next.has(id)) {
        next.delete(id);
      } else {
        next.add(id);
      }
      return next;
    });
  };

  const totalItems = Object.values(CHECKLIST).flatMap((c) => c.items).length;
  const checkedCount = checked.size;
  const progress = Math.round((checkedCount / totalItems) * 100);

  return (
    <div className="p-6 rounded-xl border bg-card space-y-6">
      <div className="flex items-center justify-between">
        <h2 className="text-xl font-semibold">Accessibility Checklist</h2>
        <span className="text-2xl font-bold text-primary">{progress}%</span>
      </div>

      {/* Progress bar */}
      <div className="h-2 bg-muted rounded-full overflow-hidden">
        <div
          className="h-full bg-primary transition-all duration-300"
          style={{ width: `${progress}%` }}
        />
      </div>

      {/* Categories */}
      {Object.entries(CHECKLIST).map(([key, category]) => (
        <div key={key} className="space-y-3">
          <h3 className="font-semibold text-lg">{category.title}</h3>
          <div className="space-y-2">
            {category.items.map((item) => (
              <label
                key={item.id}
                className="flex items-center gap-3 p-3 rounded-lg hover:bg-muted cursor-pointer"
              >
                <input
                  type="checkbox"
                  checked={checked.has(item.id)}
                  onChange={() => toggle(item.id)}
                  className="sr-only"
                />
                <div
                  className={`w-5 h-5 rounded border-2 flex items-center justify-center transition-colors ${
                    checked.has(item.id)
                      ? 'bg-primary border-primary'
                      : 'border-muted-foreground'
                  }`}
                >
                  {checked.has(item.id) && (
                    <Check className="w-3 h-3 text-primary-foreground" />
                  )}
                </div>
                <span className="flex-1">{item.text}</span>
                <span className="text-xs px-2 py-0.5 rounded bg-muted">
                  {item.level}
                </span>
              </label>
            ))}
          </div>
        </div>
      ))}
    </div>
  );
}
```

### 접근성 테스트 유틸리티

```typescript
// lib/a11y/test-utils.ts

/**
 * Check for common accessibility issues
 */
export function auditAccessibility(element: HTMLElement): {
  errors: string[];
  warnings: string[];
} {
  const errors: string[] = [];
  const warnings: string[] = [];

  // Check images for alt text
  const images = element.querySelectorAll('img');
  images.forEach((img, i) => {
    if (!img.hasAttribute('alt')) {
      errors.push(`Image ${i + 1} is missing alt attribute`);
    } else if (img.alt === '') {
      warnings.push(`Image ${i + 1} has empty alt (decorative?)`);
    }
  });

  // Check form labels
  const inputs = element.querySelectorAll('input, select, textarea');
  inputs.forEach((input, i) => {
    const id = input.getAttribute('id');
    const ariaLabel = input.getAttribute('aria-label');
    const ariaLabelledby = input.getAttribute('aria-labelledby');

    if (!id && !ariaLabel && !ariaLabelledby) {
      errors.push(`Form element ${i + 1} has no associated label`);
    } else if (id) {
      const label = element.querySelector(`label[for="${id}"]`);
      if (!label && !ariaLabel && !ariaLabelledby) {
        errors.push(`Form element ${i + 1} (id: ${id}) has no label`);
      }
    }
  });

  // Check buttons for accessible names
  const buttons = element.querySelectorAll('button');
  buttons.forEach((button, i) => {
    const hasText = button.textContent?.trim();
    const ariaLabel = button.getAttribute('aria-label');
    const ariaLabelledby = button.getAttribute('aria-labelledby');

    if (!hasText && !ariaLabel && !ariaLabelledby) {
      errors.push(`Button ${i + 1} has no accessible name`);
    }
  });

  // Check for heading hierarchy
  const headings = element.querySelectorAll('h1, h2, h3, h4, h5, h6');
  let prevLevel = 0;
  headings.forEach((heading) => {
    const level = parseInt(heading.tagName[1]);
    if (level > prevLevel + 1) {
      warnings.push(`Heading level skipped: h${prevLevel} to h${level}`);
    }
    prevLevel = level;
  });

  // Check for focus-visible on interactive elements
  const interactives = element.querySelectorAll('a, button, input, select, textarea');
  // This would need to be checked with computed styles in practice

  return { errors, warnings };
}
```

---

## Web Interface Guidelines 통합

> Vercel의 web-interface-guidelines 기반 추가 규칙

### Interaction Rules (상호작용 규칙)

```tsx
// ✅ 필수 사항
const INTERACTION_RULES = {
  // 1. 키보드로 모든 flow 완료 가능해야 함
  keyboardComplete: true,

  // 2. WAI-ARIA 패턴 준수
  ariaPatterns: true,

  // 3. 포커스 트랩 적절히 구현 (모달, 드롭다운)
  focusTrap: true,

  // 4. 터치 타겟 크기
  touchTarget: {
    mobile: 44,   // 44x44px 이상
    desktop: 24,  // 24x24px 이상 (WCAG 2.5.8)
  },

  // 5. 텍스트 입력 크기 (iOS 줌 방지)
  inputFontSize: 16,  // 16px 이상
};
```

### Focus Rules (포커스 규칙)

```tsx
// ❌ Bad
<button className="outline-none">No focus indicator</button>

// ✅ Good
<button className="outline-none focus-visible:ring-2 focus-visible:ring-ring">
  Visible focus
</button>

// 규칙 요약
const FOCUS_RULES = [
  'outline-none 사용 시 반드시 focus-visible 대체 스타일 제공',
  ':focus 대신 :focus-visible 사용 (마우스 클릭 시 링 방지)',
  '모든 interactive element에 focus-visible 스타일 필수',
  '포커스 순서가 논리적이어야 함 (tabindex 남용 금지)',
];
```

### Form Rules (폼 규칙)

```tsx
// ✅ 폼 요소 필수 사항
const FORM_RULES = {
  // 1. 모든 input에 label 연결
  label: 'htmlFor 또는 aria-label/aria-labelledby',

  // 2. autocomplete 속성 필수
  autocomplete: {
    email: 'email',
    password: 'current-password | new-password',
    name: 'name | given-name | family-name',
    tel: 'tel',
  },

  // 3. paste 차단 금지
  noPasteBlock: '비밀번호 관리자 사용 허용',

  // 4. 제출 중에도 버튼 활성 유지 (스피너로 상태 표시)
  submitButton: 'disabled 대신 스피너 사용',

  // 5. 인라인 에러 + 첫 에러 필드 포커스
  errorHandling: 'role="alert" + setFocus',
};
```

---

## Anti-Patterns 종합 체크리스트

코드 생성/리뷰 시 다음을 자동 검출하고 수정합니다.

### 🔴 Critical (반드시 수정)

| 패턴 | 문제 | 해결책 |
|------|------|--------|
| `user-scalable=no` | 줌 차단 | 메타 태그에서 제거 |
| `transition: all` | 성능 저하 + 의도치 않은 전환 | 명시적 속성 지정 |
| `outline-none` (단독) | 포커스 인디케이터 없음 | focus-visible 추가 |
| `<div onClick>` (role 없음) | 접근성 불가 | button 또는 role+tabIndex |
| `<img>` (width/height 없음) | CLS 유발 | 차원 명시 |
| `onPaste={e.preventDefault()}` | 비밀번호 관리자 차단 | 제거 |
| 50+ items 직접 렌더링 | 성능 저하 | 가상화 사용 |

### 🟠 High (강력 권고)

| 패턴 | 문제 | 해결책 |
|------|------|--------|
| 하드코딩된 날짜/숫자 | 로컬라이제이션 불가 | `Intl.*` 사용 |
| 아이콘 버튼 (label 없음) | 스크린 리더 무시 | aria-label 추가 |
| input (label 없음) | 접근성 불가 | Label htmlFor 연결 |
| input (autocomplete 없음) | 자동완성 불가 | autocomplete 속성 |
| 에러 (role="alert" 없음) | 스크린 리더 알림 안됨 | role="alert" 추가 |
| 애니메이션 (reduced-motion 무시) | 접근성 위반 | prefers-reduced-motion 체크 |

### 🟡 Medium (권고)

| 패턴 | 문제 | 해결책 |
|------|------|--------|
| `:focus` 사용 | 마우스에도 표시됨 | `:focus-visible` 사용 |
| ASCII 따옴표/말줄임표 | 타이포그래피 품질 저하 | 유니코드 사용 ("" … →) |
| 제목에 text-wrap 없음 | 불균형한 줄바꿈 | `text-wrap: balance` |
| 비시맨틱 interactive 요소 | 접근성 저하 | 시맨틱 HTML 사용 |

---

## Quick Reference (빠른 참조)

### 접근성 필수 체크

```tsx
// 1. 아이콘 버튼
<Button aria-label="닫기">
  <X className="h-4 w-4" aria-hidden="true" />
</Button>

// 2. 폼 입력
<Label htmlFor="email">이메일</Label>
<Input id="email" type="email" autoComplete="email" />

// 3. 에러 메시지
<span id="email-error" role="alert">{error}</span>

// 4. 이미지
<Image src={url} alt="설명" width={400} height={300} />

// 5. 링크
<Link href="/about">소개</Link>  // div onClick 금지
```

### 포커스 스타일

```tsx
// Tailwind 클래스
className="focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2"

// shadcn/ui 컴포넌트는 자동 적용
<Button>클릭</Button>
```

### 모션 접근성

```tsx
// Framer Motion
const shouldReduceMotion = useReducedMotion();
transition={{ duration: shouldReduceMotion ? 0 : 0.3 }}

// CSS
@media (prefers-reduced-motion: reduce) {
  * { animation-duration: 0.01ms !important; }
}

// Tailwind
className="motion-safe:animate-bounce motion-reduce:animate-none"
```

### 터치 타겟

```tsx
// 모바일 최소 44x44px
<button className="min-w-[44px] min-h-[44px] p-3">
  <Icon className="h-4 w-4" />
</button>

// 데스크톱 최소 24x24px (WCAG 2.5.8)
<button className="min-w-6 min-h-6 p-1">
  <Icon className="h-4 w-4" />
</button>
```

### iOS 줌 방지

```tsx
// 입력 필드 폰트 16px 이상
<input className="text-base" />  // 16px ✅
<input className="text-sm" />    // 14px ❌ (iOS 줌 트리거)
```

---

## 검증 코드

### Playwright 접근성 테스트

```typescript
// e2e/accessibility.spec.ts
import { test, expect } from '@playwright/test';
import AxeBuilder from '@axe-core/playwright';

test.describe('Accessibility', () => {
  test('should not have any automatically detectable accessibility issues', async ({ page }) => {
    await page.goto('/');

    const accessibilityScanResults = await new AxeBuilder({ page })
      .withTags(['wcag2a', 'wcag2aa', 'wcag21a', 'wcag21aa', 'wcag22aa'])
      .analyze();

    expect(accessibilityScanResults.violations).toEqual([]);
  });

  test('should be navigable by keyboard', async ({ page }) => {
    await page.goto('/');

    // Tab through interactive elements
    await page.keyboard.press('Tab');
    const firstFocused = await page.evaluate(() => document.activeElement?.tagName);
    expect(['A', 'BUTTON', 'INPUT']).toContain(firstFocused);

    // Skip link should be focusable
    await page.keyboard.press('Tab');
    const skipLink = page.locator('a:has-text("Skip to")');
    if (await skipLink.count() > 0) {
      await expect(skipLink).toBeFocused();
    }
  });

  test('should have visible focus indicators', async ({ page }) => {
    await page.goto('/');

    const button = page.locator('button').first();
    await button.focus();

    // Check for focus ring (outline or box-shadow)
    const styles = await button.evaluate((el) => {
      const computed = window.getComputedStyle(el);
      return {
        outline: computed.outline,
        boxShadow: computed.boxShadow,
      };
    });

    const hasFocusIndicator =
      styles.outline !== 'none' ||
      styles.boxShadow !== 'none';

    expect(hasFocusIndicator).toBe(true);
  });
});
```

### React Testing Library 접근성

```tsx
// components/__tests__/form.a11y.test.tsx
import { render, screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { axe, toHaveNoViolations } from 'jest-axe';
import { LoginForm } from '../LoginForm';

expect.extend(toHaveNoViolations);

describe('LoginForm Accessibility', () => {
  it('should have no accessibility violations', async () => {
    const { container } = render(<LoginForm />);
    const results = await axe(container);
    expect(results).toHaveNoViolations();
  });

  it('should have labels for all inputs', () => {
    render(<LoginForm />);

    const emailInput = screen.getByLabelText(/email/i);
    const passwordInput = screen.getByLabelText(/password/i);

    expect(emailInput).toBeInTheDocument();
    expect(passwordInput).toBeInTheDocument();
  });

  it('should announce errors to screen readers', async () => {
    const user = userEvent.setup();
    render(<LoginForm />);

    // Submit empty form
    const submitButton = screen.getByRole('button', { name: /submit/i });
    await user.click(submitButton);

    // Error should have role="alert"
    const error = screen.getByRole('alert');
    expect(error).toBeInTheDocument();
  });
});
```

---

## 부록: WCAG 2.2 준수 수준 매트릭스

| 기준 | 레벨 | 필수 여부 | 설명 |
|------|------|----------|------|
| 1.1.1 Non-text Content | A | ✅ 필수 | 이미지 alt 텍스트 |
| 1.3.1 Info and Relationships | A | ✅ 필수 | 시맨틱 마크업 |
| 1.4.3 Contrast (Minimum) | AA | ✅ 필수 | 4.5:1 대비 |
| 1.4.11 Non-text Contrast | AA | ✅ 필수 | UI 요소 3:1 |
| 2.1.1 Keyboard | A | ✅ 필수 | 키보드 접근 |
| 2.4.7 Focus Visible | AA | ✅ 필수 | 포커스 표시 |
| 2.4.11 Focus Not Obscured | AA | ✅ 필수 | 포커스 가림 방지 |
| 2.5.7 Dragging Movements | AA | ✅ 필수 | 드래그 대안 제공 |
| 2.5.8 Target Size | AA | ✅ 필수 | 24x24px 최소 |
| 3.2.6 Consistent Help | A | ✅ 필수 | 일관된 도움말 위치 |
| 3.3.8 Accessible Authentication | AA | ✅ 필수 | 인지 기능 테스트 금지 |

---

## References

- [WCAG 2.2 Guidelines](https://www.w3.org/TR/WCAG22/)
- [Vercel Web Interface Guidelines](https://vercel.com/blog/web-interface-guidelines)
- [Axe DevTools](https://www.deque.com/axe/)
- `UI-GUIDELINES.md` - Next.js Expert Agent UI 가이드라인
```
