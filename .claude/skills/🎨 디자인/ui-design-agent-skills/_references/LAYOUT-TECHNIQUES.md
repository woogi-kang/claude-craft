# LAYOUT-TECHNIQUES.md

고급 레이아웃 테크닉과 패턴

---

## 목차

1. [비대칭 그리드](#비대칭-그리드)
2. [오버랩 전략](#오버랩-전략)
3. [벤토 그리드](#벤토-그리드)
4. [그리드 브레이킹](#그리드-브레이킹)
5. [네거티브 스페이스](#네거티브-스페이스)
6. [스크롤 기반 레이아웃](#스크롤-기반-레이아웃)
7. [반응형 레이아웃 패턴](#반응형-레이아웃-패턴)

---

## 비대칭 그리드

### 1. 기본 비대칭 그리드

```tsx
// components/layouts/asymmetric-grid.tsx
import { ReactNode } from 'react';

interface AsymmetricGridProps {
  children: ReactNode;
}

export function AsymmetricGrid({ children }: AsymmetricGridProps) {
  return (
    <div
      className="grid gap-6"
      style={{
        gridTemplateColumns: 'repeat(12, 1fr)',
        gridAutoRows: 'minmax(200px, auto)',
      }}
    >
      {children}
    </div>
  );
}

// Usage with different span sizes
export function AsymmetricGridExample() {
  return (
    <AsymmetricGrid>
      {/* Large hero item */}
      <div className="col-span-8 row-span-2 bg-primary rounded-2xl p-8">
        <h2 className="text-4xl font-bold text-primary-foreground">
          Featured Content
        </h2>
      </div>

      {/* Small items */}
      <div className="col-span-4 bg-card rounded-2xl p-6 border">Item 2</div>
      <div className="col-span-4 bg-card rounded-2xl p-6 border">Item 3</div>

      {/* Medium items */}
      <div className="col-span-5 bg-card rounded-2xl p-6 border">Item 4</div>
      <div className="col-span-7 bg-card rounded-2xl p-6 border">Item 5</div>
    </AsymmetricGrid>
  );
}
```

### 2. 황금비 그리드

```tsx
// components/layouts/golden-ratio-grid.tsx
export function GoldenRatioGrid() {
  return (
    <div className="grid gap-6" style={{ gridTemplateColumns: '1.618fr 1fr' }}>
      {/* Main content - Golden ratio (1.618) */}
      <div className="bg-card rounded-2xl p-8 border">
        <h2 className="text-2xl font-bold mb-4">Main Content</h2>
        <p className="text-muted-foreground">
          This area takes up approximately 61.8% of the width,
          following the golden ratio.
        </p>
      </div>

      {/* Sidebar - 1 unit */}
      <div className="bg-card rounded-2xl p-6 border">
        <h3 className="font-semibold mb-4">Sidebar</h3>
        <p className="text-sm text-muted-foreground">
          This area takes up approximately 38.2% of the width.
        </p>
      </div>
    </div>
  );
}
```

### 3. 동적 비대칭 그리드

```css
/* styles/asymmetric.css */

/* Named grid areas for asymmetric layout */
.asymmetric-layout {
  display: grid;
  gap: 1.5rem;
  grid-template-columns: repeat(6, 1fr);
  grid-template-rows: repeat(4, minmax(150px, auto));
  grid-template-areas:
    "hero hero hero hero side side"
    "hero hero hero hero side side"
    "feat feat feat feat feat feat"
    "sm1 sm1 sm2 sm2 sm3 sm3";
}

.asymmetric-layout > *:nth-child(1) { grid-area: hero; }
.asymmetric-layout > *:nth-child(2) { grid-area: side; }
.asymmetric-layout > *:nth-child(3) { grid-area: feat; }
.asymmetric-layout > *:nth-child(4) { grid-area: sm1; }
.asymmetric-layout > *:nth-child(5) { grid-area: sm2; }
.asymmetric-layout > *:nth-child(6) { grid-area: sm3; }

@media (max-width: 768px) {
  .asymmetric-layout {
    grid-template-columns: 1fr;
    grid-template-rows: auto;
    grid-template-areas:
      "hero"
      "side"
      "feat"
      "sm1"
      "sm2"
      "sm3";
  }
}
```

### 4. Masonry 스타일 레이아웃

```tsx
// components/layouts/masonry-grid.tsx
'use client';

import { ReactNode, useEffect, useRef, useState } from 'react';

interface MasonryGridProps {
  children: ReactNode[];
  columns?: number;
  gap?: number;
}

export function MasonryGrid({
  children,
  columns = 3,
  gap = 24,
}: MasonryGridProps) {
  const containerRef = useRef<HTMLDivElement>(null);
  const [columnHeights, setColumnHeights] = useState<number[]>([]);

  // CSS-only masonry (supported in Firefox, Safari TP)
  const supportsMasonry =
    typeof CSS !== 'undefined' &&
    CSS.supports('grid-template-rows', 'masonry');

  if (supportsMasonry) {
    return (
      <div
        className="grid"
        style={{
          gridTemplateColumns: `repeat(${columns}, 1fr)`,
          gridTemplateRows: 'masonry',
          gap,
        }}
      >
        {children}
      </div>
    );
  }

  // Fallback: Column-based layout
  return (
    <div
      className="flex gap-6"
      style={{ gap }}
    >
      {Array.from({ length: columns }).map((_, colIndex) => (
        <div key={colIndex} className="flex-1 flex flex-col" style={{ gap }}>
          {children.filter((_, i) => i % columns === colIndex)}
        </div>
      ))}
    </div>
  );
}

// Usage
export function MasonryExample() {
  const items = [
    { id: 1, height: 200 },
    { id: 2, height: 300 },
    { id: 3, height: 150 },
    { id: 4, height: 250 },
    { id: 5, height: 180 },
    { id: 6, height: 220 },
  ];

  return (
    <MasonryGrid columns={3}>
      {items.map((item) => (
        <div
          key={item.id}
          className="bg-card rounded-2xl p-6 border"
          style={{ height: item.height }}
        >
          Item {item.id}
        </div>
      ))}
    </MasonryGrid>
  );
}
```

---

## 오버랩 전략

### 5. Z-index 오버랩

```tsx
// components/layouts/overlap-cards.tsx
export function OverlapCards() {
  return (
    <div className="relative h-96">
      {/* Background card */}
      <div
        className="absolute w-72 h-48 bg-primary/10 rounded-2xl border"
        style={{ top: 0, left: 0, zIndex: 1 }}
      />

      {/* Middle card */}
      <div
        className="absolute w-72 h-48 bg-card rounded-2xl border shadow-lg"
        style={{ top: '40px', left: '60px', zIndex: 2 }}
      >
        <div className="p-6">
          <h3 className="font-semibold">Middle Card</h3>
        </div>
      </div>

      {/* Front card */}
      <div
        className="absolute w-72 h-48 bg-primary rounded-2xl shadow-xl"
        style={{ top: '80px', left: '120px', zIndex: 3 }}
      >
        <div className="p-6 text-primary-foreground">
          <h3 className="font-semibold">Front Card</h3>
        </div>
      </div>
    </div>
  );
}
```

### 6. 네거티브 마진 오버랩

```tsx
// components/layouts/negative-margin-overlap.tsx
export function NegativeMarginOverlap() {
  return (
    <div className="relative">
      {/* Hero section */}
      <div className="bg-primary h-96 flex items-center justify-center">
        <h1 className="text-4xl font-bold text-primary-foreground">
          Hero Section
        </h1>
      </div>

      {/* Overlapping cards section */}
      <div className="container mx-auto px-4 -mt-24 relative z-10">
        <div className="grid md:grid-cols-3 gap-6">
          {[1, 2, 3].map((i) => (
            <div
              key={i}
              className="bg-card rounded-2xl shadow-xl border p-8"
            >
              <h3 className="font-semibold text-lg mb-2">Feature {i}</h3>
              <p className="text-muted-foreground">
                This card overlaps with the hero section above.
              </p>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
```

### 7. 이미지와 텍스트 오버랩

```tsx
// components/layouts/image-text-overlap.tsx
export function ImageTextOverlap() {
  return (
    <div className="grid md:grid-cols-2 gap-8 items-center">
      {/* Image side */}
      <div className="relative">
        <div className="aspect-[4/5] rounded-2xl overflow-hidden">
          <img
            src="/image.jpg"
            alt=""
            className="w-full h-full object-cover"
          />
        </div>
        {/* Decorative element behind */}
        <div className="absolute -bottom-4 -right-4 w-full h-full bg-primary/10 rounded-2xl -z-10" />
      </div>

      {/* Text side - overlapping into image */}
      <div className="md:-ml-16 bg-background p-8 rounded-2xl shadow-xl relative z-10">
        <h2 className="text-3xl font-bold mb-4">
          Overlapping Content
        </h2>
        <p className="text-muted-foreground mb-6">
          This text block extends over the image, creating
          an interesting visual overlap effect.
        </p>
        <button className="px-6 py-2 bg-primary text-primary-foreground rounded-lg">
          Learn More
        </button>
      </div>
    </div>
  );
}
```

### 8. 플로팅 요소 오버랩

```tsx
// components/layouts/floating-elements.tsx
'use client';

import { motion } from 'framer-motion';

export function FloatingElements() {
  return (
    <div className="relative min-h-[600px] flex items-center justify-center">
      {/* Main content */}
      <div className="max-w-lg text-center relative z-10">
        <h1 className="text-5xl font-bold mb-6">Welcome</h1>
        <p className="text-xl text-muted-foreground">
          Experience the future of design
        </p>
      </div>

      {/* Floating decorative elements */}
      <motion.div
        className="absolute w-64 h-64 rounded-full bg-primary/20 blur-3xl"
        style={{ top: '10%', left: '10%' }}
        animate={{
          y: [0, -20, 0],
          scale: [1, 1.1, 1],
        }}
        transition={{
          duration: 6,
          repeat: Infinity,
          ease: 'easeInOut',
        }}
      />

      <motion.div
        className="absolute w-32 h-32 rounded-2xl bg-card border shadow-lg"
        style={{ top: '20%', right: '15%', zIndex: 5 }}
        animate={{ y: [0, -15, 0], rotate: [0, 5, 0] }}
        transition={{ duration: 5, repeat: Infinity, ease: 'easeInOut' }}
      >
        <div className="p-4">
          <div className="w-8 h-8 rounded-full bg-primary mb-2" />
          <div className="h-2 bg-muted rounded w-16" />
        </div>
      </motion.div>

      <motion.div
        className="absolute w-48 h-48 rounded-2xl bg-card border shadow-lg"
        style={{ bottom: '15%', left: '20%', zIndex: 5 }}
        animate={{ y: [0, 20, 0], rotate: [0, -3, 0] }}
        transition={{ duration: 7, repeat: Infinity, ease: 'easeInOut' }}
      >
        <div className="p-6">
          <div className="h-3 bg-muted rounded w-full mb-3" />
          <div className="h-3 bg-muted rounded w-3/4" />
        </div>
      </motion.div>
    </div>
  );
}
```

---

## 벤토 그리드

### 9. 기본 벤토 그리드

```tsx
// components/layouts/bento-grid.tsx
import { ReactNode } from 'react';
import { cn } from '@/lib/utils';

interface BentoItemProps {
  children: ReactNode;
  className?: string;
  colSpan?: 1 | 2 | 3 | 4;
  rowSpan?: 1 | 2;
}

export function BentoItem({
  children,
  className,
  colSpan = 1,
  rowSpan = 1,
}: BentoItemProps) {
  return (
    <div
      className={cn(
        'bg-card rounded-3xl border p-6 overflow-hidden',
        `col-span-${colSpan}`,
        `row-span-${rowSpan}`,
        className
      )}
    >
      {children}
    </div>
  );
}

export function BentoGrid({ children }: { children: ReactNode }) {
  return (
    <div className="grid grid-cols-4 auto-rows-[180px] gap-4">
      {children}
    </div>
  );
}

// Usage
export function BentoGridExample() {
  return (
    <BentoGrid>
      {/* Large featured item */}
      <BentoItem colSpan={2} rowSpan={2} className="bg-primary text-primary-foreground">
        <h2 className="text-3xl font-bold mb-4">Featured</h2>
        <p>Large featured content area</p>
      </BentoItem>

      {/* Standard items */}
      <BentoItem>
        <h3 className="font-semibold mb-2">Analytics</h3>
        <p className="text-sm text-muted-foreground">Track your progress</p>
      </BentoItem>

      <BentoItem>
        <h3 className="font-semibold mb-2">Security</h3>
        <p className="text-sm text-muted-foreground">Keep data safe</p>
      </BentoItem>

      {/* Wide item */}
      <BentoItem colSpan={2}>
        <h3 className="font-semibold mb-2">Integration</h3>
        <p className="text-sm text-muted-foreground">Connect your tools</p>
      </BentoItem>

      {/* Tall item */}
      <BentoItem rowSpan={2}>
        <h3 className="font-semibold mb-2">Activity</h3>
        <div className="space-y-2 mt-4">
          {[1, 2, 3, 4].map((i) => (
            <div key={i} className="h-3 bg-muted rounded" />
          ))}
        </div>
      </BentoItem>

      <BentoItem>
        <h3 className="font-semibold mb-2">Settings</h3>
      </BentoItem>
    </BentoGrid>
  );
}
```

### 10. 인터랙티브 벤토 그리드

```tsx
// components/layouts/interactive-bento.tsx
'use client';

import { motion } from 'framer-motion';
import { ReactNode } from 'react';
import { cn } from '@/lib/utils';

interface InteractiveBentoItemProps {
  children: ReactNode;
  className?: string;
  href?: string;
  colSpan?: 1 | 2;
  rowSpan?: 1 | 2;
}

export function InteractiveBentoItem({
  children,
  className,
  href,
  colSpan = 1,
  rowSpan = 1,
}: InteractiveBentoItemProps) {
  const Component = href ? motion.a : motion.div;

  return (
    <Component
      href={href}
      className={cn(
        'group relative bg-card rounded-3xl border p-6 overflow-hidden cursor-pointer',
        colSpan === 2 && 'col-span-2',
        rowSpan === 2 && 'row-span-2',
        className
      )}
      whileHover={{ scale: 1.02 }}
      whileTap={{ scale: 0.98 }}
      transition={{ type: 'spring', stiffness: 400, damping: 25 }}
    >
      {/* Hover gradient */}
      <motion.div
        className="absolute inset-0 bg-gradient-to-br from-primary/10 to-transparent opacity-0 group-hover:opacity-100 transition-opacity"
      />

      {/* Content */}
      <div className="relative z-10">{children}</div>

      {/* Arrow indicator */}
      <motion.div
        className="absolute bottom-4 right-4 opacity-0 group-hover:opacity-100"
        initial={{ x: -10, opacity: 0 }}
        whileHover={{ x: 0, opacity: 1 }}
      >
        <svg className="w-6 h-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17 8l4 4m0 0l-4 4m4-4H3" />
        </svg>
      </motion.div>
    </Component>
  );
}
```

### 11. 반응형 벤토 그리드

```css
/* styles/bento.css */

.bento-responsive {
  display: grid;
  gap: 1rem;
  grid-template-columns: repeat(4, 1fr);
  grid-auto-rows: minmax(150px, auto);
}

/* Mobile: Stack */
@media (max-width: 640px) {
  .bento-responsive {
    grid-template-columns: 1fr;
  }

  .bento-responsive > * {
    grid-column: span 1 !important;
    grid-row: span 1 !important;
  }
}

/* Tablet: 2 columns */
@media (min-width: 641px) and (max-width: 1024px) {
  .bento-responsive {
    grid-template-columns: repeat(2, 1fr);
  }

  .bento-responsive > .col-span-2 {
    grid-column: span 2;
  }

  .bento-responsive > .row-span-2 {
    grid-row: span 2;
  }
}

/* Desktop: Full 4 columns */
@media (min-width: 1025px) {
  .bento-responsive {
    grid-template-columns: repeat(4, 1fr);
  }
}
```

---

## 그리드 브레이킹

### 12. 컨테이너 브레이크아웃

```tsx
// components/layouts/breakout.tsx
import { ReactNode } from 'react';

interface BreakoutProps {
  children: ReactNode;
  type?: 'full' | 'wide' | 'popout';
}

export function Breakout({ children, type = 'full' }: BreakoutProps) {
  const widthClasses = {
    full: 'w-screen relative left-1/2 right-1/2 -ml-[50vw] -mr-[50vw]',
    wide: 'w-[calc(100%+4rem)] -ml-8',
    popout: 'w-[calc(100%+2rem)] -ml-4',
  };

  return (
    <div className={widthClasses[type]}>
      {children}
    </div>
  );
}

// Usage
export function ArticleWithBreakout() {
  return (
    <article className="container max-w-2xl mx-auto px-4">
      <h1 className="text-4xl font-bold mb-6">Article Title</h1>
      <p className="mb-6">Regular paragraph within container width.</p>

      {/* Full-width breakout */}
      <Breakout type="full">
        <div className="bg-primary/10 py-16 px-4">
          <div className="container max-w-2xl mx-auto">
            <blockquote className="text-2xl italic">
              "This is a full-width breakout quote section."
            </blockquote>
          </div>
        </div>
      </Breakout>

      <p className="mt-6">Back to regular container width.</p>

      {/* Wide breakout */}
      <Breakout type="wide">
        <img
          src="/wide-image.jpg"
          alt=""
          className="w-full rounded-xl"
        />
      </Breakout>

      <p className="mt-6">More regular content.</p>
    </article>
  );
}
```

### 13. CSS Grid 브레이크아웃

```css
/* styles/grid-breakout.css */

.article-grid {
  display: grid;
  grid-template-columns:
    1fr
    min(65ch, 100%)
    1fr;
}

.article-grid > * {
  grid-column: 2;
}

.article-grid > .full-bleed {
  grid-column: 1 / -1;
}

.article-grid > .wide {
  grid-column: 1 / -1;
  width: min(100ch, 100%);
  justify-self: center;
}

.article-grid > .popout {
  grid-column: 1 / -1;
  width: min(75ch, 100%);
  justify-self: center;
}
```

```tsx
// Usage with CSS Grid breakout
export function ArticleGridBreakout() {
  return (
    <article className="article-grid">
      <h1 className="text-4xl font-bold mb-6">Article Title</h1>

      <p className="mb-6">Regular paragraph content.</p>

      {/* Full bleed image */}
      <figure className="full-bleed">
        <img src="/hero.jpg" alt="" className="w-full h-96 object-cover" />
        <figcaption className="text-center text-sm text-muted-foreground mt-2">
          Full-bleed image
        </figcaption>
      </figure>

      <p className="mt-6">More regular content.</p>

      {/* Wide content */}
      <div className="wide bg-card rounded-2xl p-8 border mt-6">
        <h3 className="font-semibold mb-4">Wide Section</h3>
        <p className="text-muted-foreground">
          This section breaks out wider than the text column.
        </p>
      </div>
    </article>
  );
}
```

### 14. 오프셋 그리드

```tsx
// components/layouts/offset-grid.tsx
export function OffsetGrid() {
  const items = Array.from({ length: 6 }, (_, i) => i + 1);

  return (
    <div className="grid grid-cols-2 gap-6">
      {/* Left column - normal */}
      <div className="space-y-6">
        {items.filter((_, i) => i % 2 === 0).map((item) => (
          <div
            key={item}
            className="bg-card rounded-2xl border p-6 h-64"
          >
            Item {item}
          </div>
        ))}
      </div>

      {/* Right column - offset down */}
      <div className="space-y-6 mt-32">
        {items.filter((_, i) => i % 2 === 1).map((item) => (
          <div
            key={item}
            className="bg-card rounded-2xl border p-6 h-64"
          >
            Item {item}
          </div>
        ))}
      </div>
    </div>
  );
}
```

---

## 네거티브 스페이스

### 15. 의도적인 여백

```tsx
// components/layouts/whitespace-layout.tsx
export function WhitespaceLayout() {
  return (
    <div className="min-h-screen py-32">
      <div className="container max-w-3xl mx-auto px-4">
        {/* Lots of top whitespace before content */}
        <div className="pt-24">
          <span className="text-sm font-medium text-muted-foreground uppercase tracking-widest">
            Case Study
          </span>
        </div>

        {/* Generous spacing between elements */}
        <h1 className="text-6xl font-bold mt-8 mb-16">
          Minimal Design
        </h1>

        {/* Intentional asymmetric padding */}
        <div className="pl-16 mb-24">
          <p className="text-xl text-muted-foreground leading-relaxed">
            This paragraph is intentionally offset to create visual tension
            and draw the eye through strategic use of negative space.
          </p>
        </div>

        {/* Large gap before next section */}
        <div className="pt-32 border-t">
          <h2 className="text-3xl font-bold mb-8">The Approach</h2>
          <p className="text-muted-foreground">
            Generous whitespace communicates confidence and clarity.
          </p>
        </div>
      </div>
    </div>
  );
}
```

### 16. 텍스트 중심 여백

```tsx
// components/layouts/text-centered-whitespace.tsx
export function TextCenteredWhitespace() {
  return (
    <section className="py-40">
      <div className="container">
        {/* Centered text with massive surrounding space */}
        <div className="max-w-xl mx-auto text-center">
          <h2 className="text-5xl font-bold mb-8">
            Focus on what matters
          </h2>
          <p className="text-xl text-muted-foreground mb-12">
            Sometimes less is more. Strategic use of empty space
            creates focus and improves readability.
          </p>
        </div>

        {/* Single element with lots of breathing room */}
        <div className="flex justify-center mt-24">
          <button className="px-8 py-4 bg-primary text-primary-foreground rounded-full text-lg font-medium">
            Get Started
          </button>
        </div>
      </div>
    </section>
  );
}
```

### 17. 비대칭 여백

```tsx
// components/layouts/asymmetric-whitespace.tsx
export function AsymmetricWhitespace() {
  return (
    <div className="grid lg:grid-cols-12 gap-8 items-center min-h-screen">
      {/* Content pushed to the right with left whitespace */}
      <div className="lg:col-start-5 lg:col-span-8">
        <div className="max-w-2xl">
          <h1 className="text-5xl font-bold mb-8">
            Breaking the Grid
          </h1>
          <p className="text-xl text-muted-foreground mb-8">
            By pushing content to one side and leaving
            intentional whitespace on the other, we create
            a dynamic and engaging layout.
          </p>
          <div className="flex gap-4">
            <button className="px-6 py-3 bg-primary text-primary-foreground rounded-lg">
              Primary Action
            </button>
            <button className="px-6 py-3 border rounded-lg">
              Secondary
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}
```

---

## 스크롤 기반 레이아웃

### 18. 스티키 사이드바

```tsx
// components/layouts/sticky-sidebar.tsx
export function StickySidebar() {
  return (
    <div className="grid lg:grid-cols-12 gap-12">
      {/* Main content - scrolls */}
      <main className="lg:col-span-8 space-y-8">
        {Array.from({ length: 5 }).map((_, i) => (
          <article key={i} className="bg-card rounded-2xl border p-8">
            <h2 className="text-2xl font-bold mb-4">Section {i + 1}</h2>
            <p className="text-muted-foreground">
              Lorem ipsum dolor sit amet, consectetur adipiscing elit.
              Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.
            </p>
          </article>
        ))}
      </main>

      {/* Sticky sidebar */}
      <aside className="lg:col-span-4">
        <div className="sticky top-8">
          <div className="bg-card rounded-2xl border p-6">
            <h3 className="font-semibold mb-4">Table of Contents</h3>
            <nav className="space-y-2">
              {Array.from({ length: 5 }).map((_, i) => (
                <a
                  key={i}
                  href={`#section-${i + 1}`}
                  className="block text-sm text-muted-foreground hover:text-foreground transition-colors"
                >
                  Section {i + 1}
                </a>
              ))}
            </nav>
          </div>
        </div>
      </aside>
    </div>
  );
}
```

### 19. 스크롤 스냅 섹션

```tsx
// components/layouts/scroll-snap-sections.tsx
export function ScrollSnapSections() {
  const sections = [
    { title: 'Introduction', color: 'bg-primary' },
    { title: 'Features', color: 'bg-secondary' },
    { title: 'Pricing', color: 'bg-accent' },
    { title: 'Contact', color: 'bg-muted' },
  ];

  return (
    <div className="h-screen overflow-y-auto snap-y snap-mandatory">
      {sections.map((section, i) => (
        <section
          key={i}
          className={`h-screen snap-start flex items-center justify-center ${section.color}`}
        >
          <h2 className="text-5xl font-bold">{section.title}</h2>
        </section>
      ))}
    </div>
  );
}
```

### 20. 수평 스크롤 섹션

```tsx
// components/layouts/horizontal-scroll.tsx
'use client';

import { useRef } from 'react';
import { motion, useScroll, useTransform } from 'framer-motion';

export function HorizontalScrollSection() {
  const containerRef = useRef<HTMLDivElement>(null);
  const { scrollYProgress } = useScroll({
    target: containerRef,
    offset: ['start start', 'end end'],
  });

  const x = useTransform(scrollYProgress, [0, 1], ['0%', '-75%']);

  return (
    <section
      ref={containerRef}
      className="relative h-[300vh]" // 3x viewport height for scroll distance
    >
      <div className="sticky top-0 h-screen flex items-center overflow-hidden">
        <motion.div
          style={{ x }}
          className="flex gap-8 pl-8"
        >
          {Array.from({ length: 5 }).map((_, i) => (
            <div
              key={i}
              className="w-[80vw] md:w-[60vw] lg:w-[40vw] shrink-0 bg-card rounded-3xl border p-8 h-[70vh]"
            >
              <h3 className="text-3xl font-bold mb-4">Card {i + 1}</h3>
              <p className="text-muted-foreground">
                This card scrolls horizontally as you scroll vertically.
              </p>
            </div>
          ))}
        </motion.div>
      </div>
    </section>
  );
}
```

---

## 반응형 레이아웃 패턴

### 21. 컨테이너 쿼리 레이아웃

```css
/* styles/container-queries.css */

.card-container {
  container-type: inline-size;
  container-name: card;
}

.responsive-card {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

/* When container is > 400px */
@container card (min-width: 400px) {
  .responsive-card {
    flex-direction: row;
    align-items: center;
  }

  .responsive-card .card-image {
    flex-shrink: 0;
    width: 150px;
  }
}

/* When container is > 600px */
@container card (min-width: 600px) {
  .responsive-card .card-image {
    width: 200px;
  }

  .responsive-card .card-content {
    padding-left: 2rem;
  }
}
```

```tsx
// components/layouts/container-query-card.tsx
export function ContainerQueryCard() {
  return (
    <div className="card-container">
      <div className="responsive-card bg-card rounded-2xl border p-4">
        <div className="card-image aspect-video bg-muted rounded-lg" />
        <div className="card-content">
          <h3 className="font-semibold mb-2">Responsive Card</h3>
          <p className="text-sm text-muted-foreground">
            This card layout changes based on its container width,
            not the viewport.
          </p>
        </div>
      </div>
    </div>
  );
}
```

### 22. 유동적 그리드

```tsx
// components/layouts/fluid-grid.tsx
export function FluidGrid() {
  return (
    <div
      className="grid gap-6"
      style={{
        gridTemplateColumns: 'repeat(auto-fit, minmax(min(300px, 100%), 1fr))',
      }}
    >
      {Array.from({ length: 6 }).map((_, i) => (
        <div key={i} className="bg-card rounded-2xl border p-6">
          <h3 className="font-semibold mb-2">Item {i + 1}</h3>
          <p className="text-sm text-muted-foreground">
            This grid automatically adjusts the number of columns.
          </p>
        </div>
      ))}
    </div>
  );
}
```

### 23. 클램프 기반 레이아웃

```css
/* styles/clamp-layouts.css */

.clamp-container {
  /* Min 320px, max 1200px, fluid between */
  width: clamp(320px, 90vw, 1200px);
  margin-inline: auto;
  padding-inline: clamp(1rem, 5vw, 3rem);
}

.clamp-grid {
  display: grid;
  gap: clamp(1rem, 3vw, 2rem);
  /* Min 1 col, max 3 cols based on available space */
  grid-template-columns: repeat(
    auto-fit,
    minmax(clamp(200px, 30vw, 350px), 1fr)
  );
}

.clamp-text {
  /* Fluid padding based on container */
  padding: clamp(1.5rem, 4vw, 3rem);
}
```

### 24. RAM (Repeat, Auto, Minmax) 패턴

```tsx
// components/layouts/ram-grid.tsx
interface RAMGridProps {
  children: React.ReactNode;
  minItemWidth?: string;
  gap?: string;
}

export function RAMGrid({
  children,
  minItemWidth = '250px',
  gap = '1.5rem',
}: RAMGridProps) {
  return (
    <div
      style={{
        display: 'grid',
        gap,
        gridTemplateColumns: `repeat(auto-fit, minmax(min(${minItemWidth}, 100%), 1fr))`,
      }}
    >
      {children}
    </div>
  );
}

// Usage
export function RAMGridExample() {
  return (
    <RAMGrid minItemWidth="300px" gap="2rem">
      {Array.from({ length: 6 }).map((_, i) => (
        <div key={i} className="bg-card rounded-xl border p-6">
          Card {i + 1}
        </div>
      ))}
    </RAMGrid>
  );
}
```
