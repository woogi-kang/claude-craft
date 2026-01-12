# Typography Skill

프로젝트의 디자인 방향에 맞는 타이포그래피 시스템을 구성합니다.

## Triggers

- "타이포그래피", "폰트", "typography", "font", "글꼴", "텍스트 스타일"

---

## Input

| 항목 | 필수 | 설명 |
|------|------|------|
| `aestheticDirection` | ✅ | 이전 Direction 스킬에서 결정된 미적 방향 |
| `brandPersonality` | ❌ | 브랜드 성격 키워드 (professional, playful, luxury 등) |
| `targetLanguage` | ❌ | 주 사용 언어 (ko, en, multi) - 기본값: multi |
| `fontBudget` | ❌ | 폰트 로딩 예산 (light, normal, heavy) - 기본값: normal |

---

## Output

| 산출물 | 설명 |
|--------|------|
| `fonts/` | 폰트 파일 또는 설정 |
| `typography-tokens.css` | CSS 변수로 정의된 타이포그래피 토큰 |
| `font-setup.tsx` | Next.js next/font 설정 컴포넌트 |

---

## Workflow

### Step 1: 미적 방향에 따른 폰트 선정

**Direction별 추천 폰트 조합:**

| Direction | Display Font | Body Font | 특징 |
|-----------|-------------|-----------|------|
| **Minimal** | Satoshi | Satoshi | 단일 폰트, 깔끔함 |
| **Elegant** | Playfair Display | Source Serif 4 | 세리프 기반 고급스러움 |
| **Bold** | Space Grotesk | DM Sans | 기하학적 강렬함 |
| **Playful** | Quicksand | Nunito | 둥글고 친근함 |
| **Technical** | JetBrains Mono | IBM Plex Sans | 정밀함과 신뢰감 |
| **Luxury** | Cormorant Garamond | Lora | 클래식 세리프 |
| **Modern** | Satoshi | General Sans | 현대적 산세리프 |
| **Organic** | Fraunces | Literata | 자연스러운 곡선 |

**한글 폰트 페어링:**

| 영문 스타일 | 한글 Display | 한글 Body | 비고 |
|-------------|-------------|-----------|------|
| Sans-serif | Pretendard | Pretendard | 범용성 최고 |
| Sans-serif (Modern) | SUIT | SUIT | 더 날렵한 느낌 |
| Serif | Noto Serif KR | Noto Serif KR | 격식 있는 느낌 |
| Rounded | Gmarket Sans | Pretendard | 친근한 느낌 |
| Technical | D2Coding | Pretendard | 개발자 타겟 |

---

### Step 2: next/font 설정

#### 기본 설정 (Google Fonts)

```tsx
// lib/fonts.ts
import { DM_Sans, Playfair_Display } from 'next/font/google';

// Body font - Variable font for flexibility
export const fontSans = DM_Sans({
  subsets: ['latin'],
  variable: '--font-sans',
  display: 'swap',
  // Preload for critical text
  preload: true,
  // Fallback for FOIT prevention
  fallback: ['system-ui', 'sans-serif'],
});

// Display font - For headings
export const fontDisplay = Playfair_Display({
  subsets: ['latin'],
  variable: '--font-display',
  display: 'swap',
  weight: ['400', '500', '600', '700'],
  style: ['normal', 'italic'],
});

// Monospace font - For code blocks
export const fontMono = JetBrains_Mono({
  subsets: ['latin'],
  variable: '--font-mono',
  display: 'swap',
  weight: ['400', '500', '600'],
});
```

#### 한글 폰트 설정 (Local Font)

```tsx
// lib/fonts.ts
import localFont from 'next/font/local';

// Pretendard - 한글 + 영문 통합
export const fontPretendard = localFont({
  src: [
    {
      path: '../public/fonts/Pretendard-Regular.subset.woff2',
      weight: '400',
      style: 'normal',
    },
    {
      path: '../public/fonts/Pretendard-Medium.subset.woff2',
      weight: '500',
      style: 'normal',
    },
    {
      path: '../public/fonts/Pretendard-SemiBold.subset.woff2',
      weight: '600',
      style: 'normal',
    },
    {
      path: '../public/fonts/Pretendard-Bold.subset.woff2',
      weight: '700',
      style: 'normal',
    },
  ],
  variable: '--font-sans',
  display: 'swap',
  fallback: ['system-ui', '-apple-system', 'sans-serif'],
  preload: true,
});
```

#### Layout에 적용

```tsx
// app/layout.tsx
import { fontSans, fontDisplay, fontMono } from '@/lib/fonts';

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html
      lang="ko"
      className={`${fontSans.variable} ${fontDisplay.variable} ${fontMono.variable}`}
      suppressHydrationWarning
    >
      <body className="font-sans antialiased">
        {children}
      </body>
    </html>
  );
}
```

---

### Step 3: 타이포그래피 스케일 정의

**7단계 타이포그래피 계층:**

| Level | Name | Size (px) | Line Height | Weight | Use Case |
|-------|------|-----------|-------------|--------|----------|
| 1 | `hero` | 72-96 | 1.0-1.1 | 700-800 | 랜딩 히어로, 임팩트 |
| 2 | `h1` | 48-60 | 1.1-1.2 | 600-700 | 페이지 타이틀 |
| 3 | `h2` | 36-42 | 1.2 | 600 | 섹션 타이틀 |
| 4 | `h3` | 28-32 | 1.3 | 600 | 서브섹션 |
| 5 | `h4` | 20-24 | 1.4 | 500-600 | 카드 타이틀 |
| 6 | `body` | 16-18 | 1.5-1.6 | 400 | 본문 텍스트 |
| 7 | `small` | 12-14 | 1.4-1.5 | 400-500 | 캡션, 라벨 |

#### CSS 변수 정의

```css
/* globals.css - Typography tokens */
:root {
  /* Font Families */
  --font-sans: var(--font-pretendard), system-ui, sans-serif;
  --font-display: var(--font-playfair), Georgia, serif;
  --font-mono: var(--font-jetbrains), 'Fira Code', monospace;

  /* Font Sizes - Using clamp for fluid typography */
  --text-hero: clamp(3rem, 5vw + 1rem, 6rem);
  --text-h1: clamp(2.5rem, 4vw + 0.5rem, 3.75rem);
  --text-h2: clamp(2rem, 3vw + 0.5rem, 2.625rem);
  --text-h3: clamp(1.5rem, 2vw + 0.5rem, 2rem);
  --text-h4: clamp(1.25rem, 1.5vw + 0.5rem, 1.5rem);
  --text-body: clamp(1rem, 0.5vw + 0.875rem, 1.125rem);
  --text-small: clamp(0.75rem, 0.25vw + 0.7rem, 0.875rem);

  /* Line Heights */
  --leading-hero: 1.05;
  --leading-heading: 1.2;
  --leading-body: 1.6;
  --leading-tight: 1.3;
  --leading-relaxed: 1.75;

  /* Font Weights */
  --weight-normal: 400;
  --weight-medium: 500;
  --weight-semibold: 600;
  --weight-bold: 700;
  --weight-extrabold: 800;

  /* Letter Spacing */
  --tracking-tighter: -0.05em;
  --tracking-tight: -0.025em;
  --tracking-normal: 0;
  --tracking-wide: 0.025em;
  --tracking-wider: 0.05em;

  /* Paragraph Spacing */
  --paragraph-spacing: 1.5em;
}
```

#### Tailwind v4 @theme 통합

```css
/* globals.css */
@theme inline {
  /* Font Family Mapping */
  --font-family-sans: var(--font-sans);
  --font-family-display: var(--font-display);
  --font-family-mono: var(--font-mono);

  /* Font Size Mapping */
  --font-size-hero: var(--text-hero);
  --font-size-h1: var(--text-h1);
  --font-size-h2: var(--text-h2);
  --font-size-h3: var(--text-h3);
  --font-size-h4: var(--text-h4);
  --font-size-body: var(--text-body);
  --font-size-small: var(--text-small);

  /* Line Height Mapping */
  --line-height-hero: var(--leading-hero);
  --line-height-heading: var(--leading-heading);
  --line-height-body: var(--leading-body);
}
```

---

### Step 4: 타이포그래피 컴포넌트 생성

#### Heading 컴포넌트

```tsx
// components/atoms/heading.tsx
import { Slot } from '@radix-ui/react-slot';
import { cva, type VariantProps } from 'class-variance-authority';
import { cn } from '@/lib/utils';

const headingVariants = cva(
  'font-display tracking-tight text-foreground',
  {
    variants: {
      level: {
        hero: 'text-hero font-extrabold leading-hero',
        h1: 'text-h1 font-bold leading-heading',
        h2: 'text-h2 font-semibold leading-heading',
        h3: 'text-h3 font-semibold leading-tight',
        h4: 'text-h4 font-medium leading-tight',
      },
      align: {
        left: 'text-left',
        center: 'text-center',
        right: 'text-right',
      },
    },
    defaultVariants: {
      level: 'h2',
      align: 'left',
    },
  }
);

type HeadingLevel = 'h1' | 'h2' | 'h3' | 'h4' | 'h5' | 'h6';

interface HeadingProps
  extends React.HTMLAttributes<HTMLHeadingElement>,
    VariantProps<typeof headingVariants> {
  as?: HeadingLevel;
  asChild?: boolean;
}

export function Heading({
  className,
  level,
  align,
  as,
  asChild = false,
  ...props
}: HeadingProps) {
  // Determine the HTML tag based on level or explicit 'as' prop
  const Tag = asChild ? Slot : (as || levelToTag(level));

  return (
    <Tag
      className={cn(headingVariants({ level, align }), className)}
      {...props}
    />
  );
}

function levelToTag(level: string | null | undefined): HeadingLevel {
  switch (level) {
    case 'hero':
    case 'h1':
      return 'h1';
    case 'h2':
      return 'h2';
    case 'h3':
      return 'h3';
    case 'h4':
      return 'h4';
    default:
      return 'h2';
  }
}
```

#### Text 컴포넌트

```tsx
// components/atoms/text.tsx
import { Slot } from '@radix-ui/react-slot';
import { cva, type VariantProps } from 'class-variance-authority';
import { cn } from '@/lib/utils';

const textVariants = cva('text-foreground', {
  variants: {
    size: {
      xs: 'text-xs leading-4',
      sm: 'text-small leading-5',
      base: 'text-body leading-body',
      lg: 'text-lg leading-7',
      xl: 'text-xl leading-8',
    },
    weight: {
      normal: 'font-normal',
      medium: 'font-medium',
      semibold: 'font-semibold',
      bold: 'font-bold',
    },
    color: {
      default: 'text-foreground',
      muted: 'text-muted-foreground',
      primary: 'text-primary',
      destructive: 'text-destructive',
      success: 'text-success',
    },
    align: {
      left: 'text-left',
      center: 'text-center',
      right: 'text-right',
      justify: 'text-justify',
    },
  },
  defaultVariants: {
    size: 'base',
    weight: 'normal',
    color: 'default',
    align: 'left',
  },
});

interface TextProps
  extends React.HTMLAttributes<HTMLParagraphElement>,
    VariantProps<typeof textVariants> {
  as?: 'p' | 'span' | 'div' | 'label';
  asChild?: boolean;
}

export function Text({
  className,
  size,
  weight,
  color,
  align,
  as = 'p',
  asChild = false,
  ...props
}: TextProps) {
  const Tag = asChild ? Slot : as;

  return (
    <Tag
      className={cn(textVariants({ size, weight, color, align }), className)}
      {...props}
    />
  );
}
```

---

### Step 5: 반응형 타이포그래피

#### Fluid Typography with clamp()

```css
/* globals.css - Fluid type scale */
:root {
  /*
   * Fluid Typography Formula:
   * clamp(min, preferred, max)
   * preferred = min + (max - min) * ((100vw - 320px) / (1440 - 320))
   */

  /* Mobile-first fluid scale */
  --text-hero: clamp(2.5rem, 8vw, 6rem);      /* 40px → 96px */
  --text-h1: clamp(2rem, 5vw, 3.75rem);       /* 32px → 60px */
  --text-h2: clamp(1.5rem, 3.5vw, 2.625rem);  /* 24px → 42px */
  --text-h3: clamp(1.25rem, 2.5vw, 2rem);     /* 20px → 32px */
  --text-h4: clamp(1.125rem, 1.5vw, 1.5rem);  /* 18px → 24px */
  --text-body: clamp(0.9375rem, 1vw, 1.125rem); /* 15px → 18px */
  --text-small: clamp(0.75rem, 0.8vw, 0.875rem); /* 12px → 14px */
}

/* Optional: Step-based responsive (for more control) */
@media (min-width: 640px) {
  :root {
    --text-body: 1rem;    /* 16px on tablet+ */
    --text-small: 0.8125rem; /* 13px */
  }
}

@media (min-width: 1024px) {
  :root {
    --text-body: 1.0625rem; /* 17px on desktop */
    --text-small: 0.875rem;  /* 14px */
  }
}

@media (min-width: 1280px) {
  :root {
    --text-body: 1.125rem;  /* 18px on large desktop */
  }
}
```

#### 읽기 최적화 (Optimal Line Length)

```css
/* Prose content - optimal reading width */
.prose {
  max-width: 65ch; /* ~65 characters per line */
  margin-inline: auto;
}

/* Headline - shorter lines for impact */
.headline {
  max-width: 20ch;
}

/* Full-width for UI elements */
.ui-text {
  max-width: none;
}
```

---

## 테스트/검증

### 폰트 로딩 검증

```tsx
// tests/fonts.test.tsx
import { describe, it, expect } from 'vitest';
import { fontSans, fontDisplay, fontMono } from '@/lib/fonts';

describe('Font Configuration', () => {
  it('has CSS variable defined for sans font', () => {
    expect(fontSans.variable).toBe('--font-sans');
  });

  it('has CSS variable defined for display font', () => {
    expect(fontDisplay.variable).toBe('--font-display');
  });

  it('has CSS variable defined for mono font', () => {
    expect(fontMono.variable).toBe('--font-mono');
  });

  it('uses swap display strategy', () => {
    expect(fontSans.style).toBeDefined();
  });
});
```

### 타이포그래피 컴포넌트 테스트

```tsx
// components/atoms/__tests__/heading.test.tsx
import { render, screen } from '@testing-library/react';
import { describe, it, expect } from 'vitest';
import { Heading } from '../heading';

describe('Heading', () => {
  it('renders with correct tag based on level', () => {
    render(<Heading level="h1">Title</Heading>);
    const heading = screen.getByRole('heading', { level: 1 });
    expect(heading).toBeInTheDocument();
  });

  it('applies hero styles correctly', () => {
    render(<Heading level="hero">Hero Title</Heading>);
    const heading = screen.getByRole('heading');
    expect(heading).toHaveClass('text-hero');
    expect(heading).toHaveClass('font-extrabold');
  });

  it('respects alignment prop', () => {
    render(<Heading level="h2" align="center">Centered</Heading>);
    const heading = screen.getByRole('heading');
    expect(heading).toHaveClass('text-center');
  });

  it('allows custom tag with as prop', () => {
    render(<Heading level="h2" as="h3">Custom Tag</Heading>);
    const heading = screen.getByRole('heading', { level: 3 });
    expect(heading).toBeInTheDocument();
  });
});
```

### 접근성 테스트

```tsx
// components/atoms/__tests__/typography-a11y.test.tsx
import { render } from '@testing-library/react';
import { axe, toHaveNoViolations } from 'jest-axe';
import { Heading } from '../heading';
import { Text } from '../text';

expect.extend(toHaveNoViolations);

describe('Typography Accessibility', () => {
  it('Heading has no accessibility violations', async () => {
    const { container } = render(
      <article>
        <Heading level="h1">Main Title</Heading>
        <Heading level="h2">Section Title</Heading>
        <Text>Paragraph content.</Text>
      </article>
    );
    const results = await axe(container);
    expect(results).toHaveNoViolations();
  });

  it('maintains heading hierarchy', async () => {
    const { container } = render(
      <main>
        <Heading level="h1">Page Title</Heading>
        <section>
          <Heading level="h2">Section</Heading>
          <Heading level="h3">Subsection</Heading>
        </section>
      </main>
    );
    const results = await axe(container);
    expect(results).toHaveNoViolations();
  });
});
```

### 시각적 확인 (Storybook)

```tsx
// components/atoms/heading.stories.tsx
import type { Meta, StoryObj } from '@storybook/react';
import { Heading } from './heading';

const meta: Meta<typeof Heading> = {
  title: 'Atoms/Heading',
  component: Heading,
  argTypes: {
    level: {
      control: 'select',
      options: ['hero', 'h1', 'h2', 'h3', 'h4'],
    },
    align: {
      control: 'select',
      options: ['left', 'center', 'right'],
    },
  },
};

export default meta;
type Story = StoryObj<typeof Heading>;

export const AllLevels: Story = {
  render: () => (
    <div className="space-y-6">
      <Heading level="hero">Hero: 대담한 임팩트</Heading>
      <Heading level="h1">H1: 페이지 제목</Heading>
      <Heading level="h2">H2: 섹션 제목</Heading>
      <Heading level="h3">H3: 서브섹션</Heading>
      <Heading level="h4">H4: 카드 제목</Heading>
    </div>
  ),
};

export const Responsive: Story = {
  render: () => (
    <div className="space-y-4">
      <Heading level="h1">
        Resize the window to see fluid typography in action
      </Heading>
      <p className="text-muted-foreground text-body">
        창 크기를 조절하면 텍스트가 자연스럽게 반응합니다.
      </p>
    </div>
  ),
};
```

---

## 안티패턴

### 1. 폰트 로딩 최적화 무시

```tsx
// ❌ Bad: 모든 weight를 로드
import { DM_Sans } from 'next/font/google';

const font = DM_Sans({
  subsets: ['latin'],
  weight: ['100', '200', '300', '400', '500', '600', '700', '800', '900'],
  // 9개 weight = 매우 큰 번들
});

// ✅ Good: 필요한 weight만 로드하거나 Variable font 사용
const font = DM_Sans({
  subsets: ['latin'],
  variable: '--font-sans',
  // Variable font는 모든 weight를 하나의 파일로
});
```

### 2. 하드코딩된 폰트 사이즈

```css
/* ❌ Bad: 픽셀 하드코딩 */
.title {
  font-size: 48px;
  line-height: 56px;
}

.paragraph {
  font-size: 16px;
  line-height: 24px;
}

/* ✅ Good: 토큰 시스템 사용 */
.title {
  font-size: var(--text-h1);
  line-height: var(--leading-heading);
}

.paragraph {
  font-size: var(--text-body);
  line-height: var(--leading-body);
}
```

### 3. 폰트 페어링 불일치

```tsx
// ❌ Bad: 일관성 없는 폰트 조합
<h1 className="font-serif">Title</h1>       {/* Georgia */}
<p className="font-sans">Body text</p>       {/* Satoshi */}
<span className="font-mono">Code</span>      {/* Fira Code */}
<h2 className="font-cursive">Subtitle</h2>   {/* ???: 정의되지 않음 */}

// ✅ Good: 디자인 시스템에 정의된 폰트만 사용
<h1 className="font-display">Title</h1>      {/* Display font */}
<p className="font-sans">Body text</p>        {/* Body font */}
<code className="font-mono">Code</code>       {/* Mono font */}
```

### 4. 접근성 무시

```css
/* ❌ Bad: 너무 작은 폰트, 낮은 대비 */
.caption {
  font-size: 10px;
  color: #999;  /* 낮은 대비비 */
  line-height: 1.1;  /* 읽기 어려움 */
}

/* ✅ Good: 접근성 기준 준수 */
.caption {
  font-size: var(--text-small);  /* 최소 12px */
  color: var(--muted-foreground);  /* WCAG AA 준수 */
  line-height: var(--leading-tight);  /* 최소 1.3 */
}
```

### 5. 반응형 고려 없음

```tsx
// ❌ Bad: 고정 사이즈로 모바일에서 문제
<h1 className="text-6xl">Very Long Title Text Here</h1>

// ✅ Good: 반응형 타이포그래피
<h1 className="text-h1">Very Long Title Text Here</h1>
// text-h1 = clamp(2rem, 5vw + 0.5rem, 3.75rem)
```

---

## 성능 고려사항

### Font Loading Strategy

```tsx
// next.config.ts
import type { NextConfig } from 'next';

const nextConfig: NextConfig = {
  // 폰트 최적화 활성화
  optimizeFonts: true,

  experimental: {
    // 사용하지 않는 CSS 제거
    optimizeCss: true,
  },
};

export default nextConfig;
```

### Font Subsetting

```tsx
// 한글 서브셋 예시 (자주 사용하는 글자만)
export const fontKorean = localFont({
  src: [
    {
      path: '../public/fonts/Pretendard-Regular.subset.woff2',
      weight: '400',
    },
  ],
  // 서브셋된 폰트 = 더 작은 파일 크기
});

// 서브셋 생성 스크립트
// npx subfont --formats woff2 --subset "가-힣"
```

### Font Display Strategy

```tsx
// display 옵션 선택 가이드
const font = DM_Sans({
  display: 'swap',    // 기본: 빠른 렌더링, FOUT 허용
  // display: 'block', // 폰트 로드까지 텍스트 숨김 (FOIT)
  // display: 'fallback', // 짧은 FOIT 후 fallback
  // display: 'optional', // 느리면 fallback 유지
});
```

---

## 보안 고려사항

### 외부 폰트 CDN 주의

```tsx
// ❌ 위험: 외부 CDN 직접 사용 (프라이버시, 가용성 문제)
<link
  href="https://fonts.googleapis.com/css2?family=DM+Sans"
  rel="stylesheet"
/>

// ✅ 안전: next/font 사용 (빌드 시 최적화)
import { DM_Sans } from 'next/font/google';

const font = DM_Sans({
  subsets: ['latin'],
  // Google Fonts를 빌드 시점에 다운로드하여 self-host
});
```

### CSP 설정

```typescript
// middleware.ts
export function middleware(request: NextRequest) {
  const response = NextResponse.next();

  // 폰트 로딩 허용 CSP
  response.headers.set(
    'Content-Security-Policy',
    "font-src 'self' data:;"
  );

  return response;
}
```

---

## References

- `_references/TYPOGRAPHY-RECIPES.md` - 방향별 폰트 조합 레시피
- `3-direction/` - 디자인 방향 결정 (선행 스킬)
- `5-color/` - 색상 시스템 (연계 스킬)
