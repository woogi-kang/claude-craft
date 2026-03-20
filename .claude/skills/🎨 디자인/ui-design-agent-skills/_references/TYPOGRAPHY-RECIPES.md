# TYPOGRAPHY-RECIPES.md

타이포그래피 시스템과 폰트 페어링 레시피

---

> **⚠️ 금지 폰트 경고 (BANNED FONTS WARNING)**
>
> 다음 폰트는 **절대 사용 금지**입니다. 코드에서 발견 시 즉시 대체하세요:
>
> | 금지 폰트 | 대체 폰트 |
> |-----------|-----------|
> | ~~Inter~~ | **Geist**, Satoshi, Albert Sans, DM Sans |
> | ~~Roboto~~ | **Source Sans 3**, Nunito Sans, Work Sans |
> | ~~Arial~~ | **Geist**, system-ui |
> | ~~Open Sans~~ | **Source Sans 3**, Nunito Sans |
> | ~~Poppins~~ | **Plus Jakarta Sans**, Outfit |
>
> **Geist 폰트 주의**: Geist는 Google Fonts가 아닌 Vercel 폰트입니다. `next/font/google`에서 import하지 마세요!
> ```tsx
> // ❌ 잘못된 방법
> import { Geist } from 'next/font/google';
>
> // ✅ 올바른 방법
> import { GeistSans, GeistMono } from 'geist/font';
> // 또는 로컬 폰트로:
> import localFont from 'next/font/local';
> const geist = localFont({ src: './GeistVF.woff2' });
> ```

---

## 목차

1. [폰트 페어링 원칙](#폰트-페어링-원칙)
2. [미적 방향별 폰트 조합](#미적-방향별-폰트-조합)
3. [Variable Font 설정](#variable-font-설정)
4. [금지 폰트 목록](#금지-폰트-목록)
5. [폰트 로딩 최적화](#폰트-로딩-최적화)
6. [반응형 타이포그래피 스케일](#반응형-타이포그래피-스케일)
7. [Tailwind 설정 코드](#tailwind-설정-코드)

---

## 폰트 페어링 원칙

### 기본 규칙

1. **대비 원칙**: Serif + Sans-serif 조합으로 시각적 대비 생성
2. **X-height 매칭**: 본문용 폰트는 x-height가 유사해야 조화로움
3. **역할 분리**: Display(제목) + Text(본문) + Mono(코드) 3가지 역할 구분
4. **최대 3개**: 한 프로젝트에서 폰트 패밀리는 3개 이하로 제한

### 조합 공식

```
Display (Impact) + Text (Readability) + Accent (Optional)
```

---

## 미적 방향별 폰트 조합

### 1. 모던 미니멀 (Modern Minimal)

| # | Display | Text | 특징 |
|---|---------|------|------|
| 1 | **Geist** | Geist | Vercel 디자인 시스템, 단일 폰트 |
| 2 | **Satoshi** | Satoshi | 현대적 기하학, 완벽한 일관성 |
| 3 | **Plus Jakarta Sans** | Plus Jakarta Sans | 기하학적이면서 친근함 |
| 4 | **Satoshi** | DM Sans | 현대적 기하학 + 중립 |
| 5 | **Outfit** | Outfit | Variable, 부드러운 기하학 |
| 6 | **Manrope** | Albert Sans | 세미 기하학적 우아함 |
| 7 | **Sora** | Geist | 미래지향적 + 기술적 |

```tsx
// Modern Minimal Example
// Geist is from Vercel, not Google Fonts
import { GeistSans } from 'geist/font';
import { DM_Sans } from 'next/font/google';

// Geist - Vercel's font package
// Install: npm install geist
const geistSans = GeistSans;

const dmSans = DM_Sans({
  subsets: ['latin'],
  variable: '--font-dm-sans',
  display: 'swap',
});
```

### 2. 럭셔리 에디토리얼 (Luxury Editorial)

| # | Display | Text | 특징 |
|---|---------|------|------|
| 8 | **Playfair Display** | Source Serif Pro | 클래식 럭셔리 |
| 9 | **Cormorant Garamond** | Lora | 우아한 세리프 조합 |
| 10 | **Fraunces** | Work Sans | 빈티지 + 현대적 |
| 11 | **Bodoni Moda** | Libre Baskerville | 하이패션 에디토리얼 |
| 12 | **DM Serif Display** | DM Sans | 대비가 강한 모던 럭셔리 |
| 13 | **Newsreader** | Source Sans 3 | 에디토리얼 신문 스타일 |
| 14 | **Spectral** | Spectral | 긴 본문에 최적화된 세리프 |

```tsx
// Luxury Editorial Example
import { Playfair_Display, Source_Serif_4 } from 'next/font/google';

const playfair = Playfair_Display({
  subsets: ['latin'],
  variable: '--font-display',
  display: 'swap',
  weight: ['400', '500', '600', '700', '800', '900'],
});

const sourceSerif = Source_Serif_4({
  subsets: ['latin'],
  variable: '--font-text',
  display: 'swap',
});
```

### 3. 테크 스타트업 (Tech Startup)

| # | Display | Text | 특징 |
|---|---------|------|------|
| 15 | **Space Grotesk** | IBM Plex Sans | 우주/기술 테마 |
| 16 | **Lexend** | Lexend | 읽기 최적화 (난독증 친화적) |
| 17 | **General Sans** | DM Sans | 중립적이면서 현대적 |
| 18 | **Urbanist** | Urbanist | 기하학적 + 친근함 |
| 19 | **Rubik** | Nunito Sans | 둥근 모서리 + 부드러움 |
| 20 | **Cabinet Grotesk** | Geist | 강렬한 + 기술적 |
| 21 | **Clash Display** | Satoshi | 대담한 + 현대적 |

```tsx
// Tech Startup Example
import { Space_Grotesk, IBM_Plex_Sans } from 'next/font/google';

const spaceGrotesk = Space_Grotesk({
  subsets: ['latin'],
  variable: '--font-display',
  display: 'swap',
});

const ibmPlex = IBM_Plex_Sans({
  subsets: ['latin'],
  variable: '--font-text',
  display: 'swap',
  weight: ['400', '500', '600'],
});
```

### 4. 크리에이티브 에이전시 (Creative Agency)

| # | Display | Text | 특징 |
|---|---------|------|------|
| 22 | **Unbounded** | Albert Sans | 연결된 글자, 독특함 |
| 23 | **Familjen Grotesk** | Work Sans | 스칸디나비안 모던 |
| 24 | **Schibsted Grotesk** | Schibsted Grotesk | 북유럽 + 미니멀 |
| 25 | **Instrument Sans** | Instrument Sans | 날카로운 + 현대적 |
| 26 | **Switzer** | Switzer | 스위스 스타일 |
| 27 | **Chillax** | Satoshi | 캐주얼 + 대담함 |
| 28 | **Zodiak** | DM Sans | 세리프 + 테크 믹스 |

```tsx
// Creative Agency Example - Using local font
import localFont from 'next/font/local';

const unbounded = localFont({
  src: [
    { path: './fonts/Unbounded-Light.woff2', weight: '300' },
    { path: './fonts/Unbounded-Regular.woff2', weight: '400' },
    { path: './fonts/Unbounded-Medium.woff2', weight: '500' },
    { path: './fonts/Unbounded-Bold.woff2', weight: '700' },
  ],
  variable: '--font-display',
  display: 'swap',
});
```

### 5. 친근한 브랜드 (Friendly Brand)

| # | Display | Text | 특징 |
|---|---------|------|------|
| 29 | **Plus Jakarta Sans** | Nunito | 둥글고 친근함 |
| 30 | **Quicksand** | Quicksand | 부드러운 곡선 |
| 31 | **Comfortaa** | Nunito Sans | 매우 둥근 스타일 |
| 32 | **Baloo 2** | Nunito | 재미있고 활기참 |
| 33 | **Fredoka** | Nunito Sans | 아동 친화적 |
| 34 | **Varela Round** | Source Sans 3 | 둥근 + 가독성 |
| 35 | **Itim** | Sarabun | 손글씨 느낌 |

### 6. 전문가/기업 (Professional Corporate)

| # | Display | Text | 특징 |
|---|---------|------|------|
| 36 | **Archivo** | Archivo | 뉴스 + 전문적 |
| 37 | **Public Sans** | Public Sans | 미국 정부 디자인 시스템 |
| 38 | **Figtree** | Figtree | 깔끔한 산세리프 |
| 39 | **Albert Sans** | Albert Sans | 중립적 현대 |
| 40 | **Commissioner** | Commissioner | Variable 전문가용 |
| 41 | **Epilogue** | Epilogue | 미니멀 비즈니스 |
| 42 | **Atkinson Hyperlegible** | Atkinson Hyperlegible | 최고 가독성 |

### 7. 한글 + 영문 조합

| # | 한글 | 영문 Display | 영문 Text | 특징 |
|---|------|-------------|-----------|------|
| 43 | **Pretendard** | Geist | Satoshi | 시스템 UI 스타일 |
| 44 | **SUIT** | Space Grotesk | IBM Plex Sans | 테크 스타트업 |
| 45 | **Noto Sans KR** | Plus Jakarta Sans | Nunito Sans | 범용 친근함 |
| 46 | **Spoqa Han Sans Neo** | Manrope | Work Sans | SaaS 제품 |
| 47 | **IBM Plex Sans KR** | IBM Plex Sans | IBM Plex Serif | 기업/엔터프라이즈 |
| 48 | **KoPub Batang** | Playfair Display | Source Serif Pro | 럭셔리 에디토리얼 |
| 49 | **Nanum Myeongjo** | Cormorant Garamond | Lora | 전통적 우아함 |
| 50 | **Gmarket Sans** | Outfit | Outfit | 커머스/이커머스 |

```tsx
// Korean + English Combination
import { Noto_Sans_KR } from 'next/font/google';
import localFont from 'next/font/local';

const pretendard = localFont({
  src: './fonts/PretendardVariable.woff2',
  variable: '--font-pretendard',
  display: 'swap',
  weight: '45 920',
});

const notoSansKR = Noto_Sans_KR({
  subsets: ['latin'],
  variable: '--font-noto',
  display: 'swap',
  weight: ['400', '500', '700'],
});
```

---

## Variable Font 설정

### Tailwind CSS v4 설정

```css
/* app/globals.css */
@import "tailwindcss";

@theme {
  /* Variable Font Setup */
  --font-display: "Geist Variable", system-ui, sans-serif;
  --font-text: "Satoshi Variable", system-ui, sans-serif;
  --font-mono: "JetBrains Mono Variable", ui-monospace, monospace;
  --font-korean: "Pretendard Variable", "Noto Sans KR", sans-serif;

  /* Font Feature Settings */
  --font-feature-default: "kern" 1, "liga" 1, "calt" 1;
  --font-feature-tabular: "tnum" 1;
  --font-feature-stylistic: "ss01" 1, "ss02" 1;
}

/* Variable Font Weight Range */
@font-face {
  font-family: 'Satoshi Variable';
  src: url('/fonts/SatoshiVariable.woff2') format('woff2');
  font-weight: 100 900;
  font-display: swap;
  font-style: normal;
}

@font-face {
  font-family: 'Geist Variable';
  src: url('/fonts/GeistVariableVF.woff2') format('woff2');
  font-weight: 100 900;
  font-display: swap;
  font-style: normal;
}
```

### Next.js Font 설정

```tsx
// app/fonts.ts
// Geist is from Vercel, NOT Google Fonts
import { GeistSans, GeistMono } from 'geist/font';
import { DM_Sans } from 'next/font/google';
import localFont from 'next/font/local';

// Geist - from Vercel's geist package (npm install geist)
export const geistSans = GeistSans;
export const geistMono = GeistMono;

// Alternative: Load Satoshi as local font
export const satoshi = localFont({
  src: './fonts/SatoshiVariable.woff2',
  variable: '--font-satoshi',
  display: 'swap',
  weight: '300 900',
});

export const dmSans = DM_Sans({
  subsets: ['latin'],
  variable: '--font-dm-sans',
  display: 'swap',
});

export const pretendard = localFont({
  src: './fonts/PretendardVariable.woff2',
  variable: '--font-pretendard',
  display: 'swap',
  weight: '45 920',
  preload: true,
});

// Combined class names for <html>
export const fontVariables = `${geistSans.variable} ${geistMono.variable} ${satoshi.variable} ${pretendard.variable}`;
```

```tsx
// app/layout.tsx
import { fontVariables } from './fonts';

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="ko" className={fontVariables}>
      <body className="font-text antialiased">
        {children}
      </body>
    </html>
  );
}
```

---

## 금지 폰트 목록

### 절대 사용 금지

| 폰트 | 금지 이유 | 대안 |
|------|----------|------|
| **Inter** | 과도한 사용, 차별화 불가 | Geist, Satoshi, Albert Sans, DM Sans |
| **Roboto** | Google 기본폰트, 개성 없음 | Source Sans 3, Nunito Sans, Work Sans |
| **Arial** | 너무 범용적, 개성 없음 | Geist, system-ui |
| **Open Sans** | 너무 중립적, 차별화 불가 | Source Sans 3, Nunito Sans |
| **Poppins** | 과도한 사용으로 클리셰화 | Plus Jakarta Sans, Outfit |
| **Comic Sans** | 비전문적, 과도한 사용 | Quicksand, Baloo 2 |
| **Papyrus** | 클리셰, 아마추어적 | Cormorant, Spectral |
| **Impact** | 밈/인터넷 클리셰 | Bebas Neue, Oswald |
| **Brush Script** | 시대에 뒤떨어짐 | Dancing Script, Pacifico |
| **Curlz MT** | 전문성 부족 | Fredoka, Comfortaa |
| **Jokerman** | 진지하지 않음 | Bangers, Bungee |

### 주의해서 사용

| 폰트 | 주의 이유 | 사용 가능 상황 |
|------|----------|---------------|
| **Times New Roman** | 기본값 느낌, 게으름 | 학술 문서만 |
| **Helvetica** | 비싸고 Arial과 혼동 | 명확한 의도가 있을 때 |
| **Lobster** | 과도한 사용으로 클리셰화 | 빈티지 테마 한정 |
| **Raleway** | 너무 흔함 | 다른 선택이 없을 때 |

### 한글 주의 폰트

| 폰트 | 주의 이유 | 대안 |
|------|----------|------|
| **굴림/돋움** | 시스템 기본, 구시대적 | Pretendard, SUIT |
| **맑은 고딕** | 기본값 느낌 | Spoqa Han Sans Neo |
| **HY헤드라인** | 90년대 스타일 | Gmarket Sans |
| **궁서** | 과도한 장식 | Nanum Myeongjo |

---

## 폰트 로딩 최적화

### font-display 전략

```css
/* Swap: 즉시 fallback 표시, 로드 후 교체 */
@font-face {
  font-family: 'Custom Font';
  src: url('/fonts/custom.woff2') format('woff2');
  font-display: swap;
}

/* Optional: 100ms 내 로드 안 되면 fallback 유지 */
@font-face {
  font-family: 'Optional Font';
  src: url('/fonts/optional.woff2') format('woff2');
  font-display: optional;
}

/* Fallback: 100ms block + 3s swap */
@font-face {
  font-family: 'Fallback Font';
  src: url('/fonts/fallback.woff2') format('woff2');
  font-display: fallback;
}
```

### Preload 전략

```tsx
// app/layout.tsx
export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="ko">
      <head>
        {/* Critical fonts only */}
        <link
          rel="preload"
          href="/fonts/GeistVariableVF.woff2"
          as="font"
          type="font/woff2"
          crossOrigin="anonymous"
        />
        <link
          rel="preload"
          href="/fonts/PretendardVariable.woff2"
          as="font"
          type="font/woff2"
          crossOrigin="anonymous"
        />
      </head>
      <body>{children}</body>
    </html>
  );
}
```

### Subset 전략

```tsx
// Google Fonts with specific subsets
const notoSansKR = Noto_Sans_KR({
  subsets: ['latin'],
  weight: ['400', '500', '700'],
  display: 'swap',
  // Preload only frequently used weights
  preload: true,
});
```

### Size-Adjust로 CLS 방지

```css
/* Match fallback metrics to custom font */
@font-face {
  font-family: 'Satoshi';
  src: url('/fonts/Satoshi.woff2') format('woff2');
  font-display: swap;
  /* Metrics to match system font */
  ascent-override: 90%;
  descent-override: 25%;
  line-gap-override: 0%;
  size-adjust: 107%;
}
```

---

## 반응형 타이포그래피 스케일

### Fluid Typography (clamp 기반)

```css
/* app/globals.css */
@import "tailwindcss";

@theme {
  /* Fluid Type Scale */
  --font-size-xs: clamp(0.75rem, 0.7rem + 0.25vw, 0.875rem);
  --font-size-sm: clamp(0.875rem, 0.8rem + 0.375vw, 1rem);
  --font-size-base: clamp(1rem, 0.9rem + 0.5vw, 1.125rem);
  --font-size-lg: clamp(1.125rem, 1rem + 0.625vw, 1.25rem);
  --font-size-xl: clamp(1.25rem, 1.1rem + 0.75vw, 1.5rem);
  --font-size-2xl: clamp(1.5rem, 1.25rem + 1.25vw, 2rem);
  --font-size-3xl: clamp(1.875rem, 1.5rem + 1.875vw, 2.5rem);
  --font-size-4xl: clamp(2.25rem, 1.75rem + 2.5vw, 3rem);
  --font-size-5xl: clamp(3rem, 2rem + 5vw, 4.5rem);
  --font-size-6xl: clamp(3.75rem, 2.5rem + 6.25vw, 6rem);

  /* Line Heights */
  --line-height-tight: 1.1;
  --line-height-snug: 1.25;
  --line-height-normal: 1.5;
  --line-height-relaxed: 1.625;
  --line-height-loose: 2;

  /* Letter Spacing */
  --letter-spacing-tighter: -0.05em;
  --letter-spacing-tight: -0.025em;
  --letter-spacing-normal: 0;
  --letter-spacing-wide: 0.025em;
  --letter-spacing-wider: 0.05em;
  --letter-spacing-widest: 0.1em;
}
```

### 반응형 Heading 컴포넌트

```tsx
// components/ui/heading.tsx
import { cva, type VariantProps } from 'class-variance-authority';
import { cn } from '@/lib/utils';

const headingVariants = cva(
  'font-display tracking-tight text-balance',
  {
    variants: {
      level: {
        h1: 'text-5xl font-bold leading-tight',    // 3rem → 4.5rem
        h2: 'text-4xl font-semibold leading-tight', // 2.25rem → 3rem
        h3: 'text-3xl font-semibold leading-snug',  // 1.875rem → 2.5rem
        h4: 'text-2xl font-medium leading-snug',    // 1.5rem → 2rem
        h5: 'text-xl font-medium leading-normal',   // 1.25rem → 1.5rem
        h6: 'text-lg font-medium leading-normal',   // 1.125rem → 1.25rem
      },
    },
    defaultVariants: {
      level: 'h2',
    },
  }
);

interface HeadingProps
  extends React.HTMLAttributes<HTMLHeadingElement>,
    VariantProps<typeof headingVariants> {
  as?: 'h1' | 'h2' | 'h3' | 'h4' | 'h5' | 'h6';
}

export function Heading({
  as,
  level,
  className,
  children,
  ...props
}: HeadingProps) {
  const Component = as || level || 'h2';

  return (
    <Component
      className={cn(headingVariants({ level: level || as }), className)}
      {...props}
    >
      {children}
    </Component>
  );
}
```

### 본문 텍스트 컴포넌트

```tsx
// components/ui/text.tsx
import { cva, type VariantProps } from 'class-variance-authority';
import { cn } from '@/lib/utils';

const textVariants = cva(
  'font-text text-foreground',
  {
    variants: {
      size: {
        xs: 'text-xs',
        sm: 'text-sm',
        base: 'text-base',
        lg: 'text-lg',
        xl: 'text-xl',
      },
      weight: {
        normal: 'font-normal',
        medium: 'font-medium',
        semibold: 'font-semibold',
        bold: 'font-bold',
      },
      leading: {
        tight: 'leading-tight',
        snug: 'leading-snug',
        normal: 'leading-normal',
        relaxed: 'leading-relaxed',
        loose: 'leading-loose',
      },
      color: {
        default: 'text-foreground',
        muted: 'text-muted-foreground',
        accent: 'text-accent-foreground',
      },
    },
    defaultVariants: {
      size: 'base',
      weight: 'normal',
      leading: 'normal',
      color: 'default',
    },
  }
);

interface TextProps
  extends React.HTMLAttributes<HTMLParagraphElement>,
    VariantProps<typeof textVariants> {
  as?: 'p' | 'span' | 'div';
}

export function Text({
  as: Component = 'p',
  size,
  weight,
  leading,
  color,
  className,
  children,
  ...props
}: TextProps) {
  return (
    <Component
      className={cn(textVariants({ size, weight, leading, color }), className)}
      {...props}
    >
      {children}
    </Component>
  );
}
```

---

## Tailwind 설정 코드

### tailwind.config.ts (v4 호환)

```ts
// tailwind.config.ts
import type { Config } from 'tailwindcss';

const config: Config = {
  content: [
    './app/**/*.{js,ts,jsx,tsx,mdx}',
    './components/**/*.{js,ts,jsx,tsx,mdx}',
  ],
  theme: {
    extend: {
      fontFamily: {
        // Display fonts
        display: ['var(--font-geist)', 'var(--font-pretendard)', 'system-ui', 'sans-serif'],
        // Text fonts
        text: ['var(--font-satoshi)', 'var(--font-pretendard)', 'system-ui', 'sans-serif'],
        // Mono fonts
        mono: ['var(--font-geist-mono)', 'ui-monospace', 'monospace'],
        // Korean specific
        korean: ['var(--font-pretendard)', 'var(--font-noto)', 'sans-serif'],
      },
      fontSize: {
        // Fluid type scale
        'xs': ['clamp(0.75rem, 0.7rem + 0.25vw, 0.875rem)', { lineHeight: '1.5' }],
        'sm': ['clamp(0.875rem, 0.8rem + 0.375vw, 1rem)', { lineHeight: '1.5' }],
        'base': ['clamp(1rem, 0.9rem + 0.5vw, 1.125rem)', { lineHeight: '1.6' }],
        'lg': ['clamp(1.125rem, 1rem + 0.625vw, 1.25rem)', { lineHeight: '1.5' }],
        'xl': ['clamp(1.25rem, 1.1rem + 0.75vw, 1.5rem)', { lineHeight: '1.4' }],
        '2xl': ['clamp(1.5rem, 1.25rem + 1.25vw, 2rem)', { lineHeight: '1.3' }],
        '3xl': ['clamp(1.875rem, 1.5rem + 1.875vw, 2.5rem)', { lineHeight: '1.2' }],
        '4xl': ['clamp(2.25rem, 1.75rem + 2.5vw, 3rem)', { lineHeight: '1.1' }],
        '5xl': ['clamp(3rem, 2rem + 5vw, 4.5rem)', { lineHeight: '1.05' }],
        '6xl': ['clamp(3.75rem, 2.5rem + 6.25vw, 6rem)', { lineHeight: '1' }],
      },
      letterSpacing: {
        tightest: '-0.075em',
        tighter: '-0.05em',
        tight: '-0.025em',
        normal: '0',
        wide: '0.025em',
        wider: '0.05em',
        widest: '0.1em',
      },
    },
  },
  plugins: [],
};

export default config;
```

### CSS Variables 방식 (Tailwind v4)

```css
/* app/globals.css */
@import "tailwindcss";

@theme {
  /* Font Families */
  --font-family-display: "Geist Variable", "Pretendard Variable", system-ui, sans-serif;
  --font-family-text: "Satoshi Variable", "Pretendard Variable", system-ui, sans-serif;
  --font-family-mono: "Geist Mono Variable", ui-monospace, SFMono-Regular, monospace;

  /* Font Sizes - Fluid */
  --font-size-display-2xl: clamp(4.5rem, 3rem + 7.5vw, 8rem);
  --font-size-display-xl: clamp(3.75rem, 2.5rem + 6.25vw, 6rem);
  --font-size-display-lg: clamp(3rem, 2rem + 5vw, 4.5rem);
  --font-size-display-md: clamp(2.25rem, 1.75rem + 2.5vw, 3rem);
  --font-size-display-sm: clamp(1.875rem, 1.5rem + 1.875vw, 2.5rem);

  /* Font Weights */
  --font-weight-thin: 100;
  --font-weight-extralight: 200;
  --font-weight-light: 300;
  --font-weight-normal: 400;
  --font-weight-medium: 500;
  --font-weight-semibold: 600;
  --font-weight-bold: 700;
  --font-weight-extrabold: 800;
  --font-weight-black: 900;
}

/* Prose styles for long-form content */
.prose-custom {
  font-family: var(--font-family-text);
  font-size: var(--font-size-base);
  line-height: 1.75;

  & h1, & h2, & h3, & h4, & h5, & h6 {
    font-family: var(--font-family-display);
    font-weight: var(--font-weight-bold);
    letter-spacing: -0.025em;
    text-wrap: balance;
  }

  & code {
    font-family: var(--font-family-mono);
    font-size: 0.875em;
  }
}
```

---

## 실전 예제

### Hero Section 타이포그래피

```tsx
// components/sections/hero.tsx
export function HeroSection() {
  return (
    <section className="py-24 lg:py-32">
      <div className="container max-w-4xl text-center">
        {/* Eyebrow */}
        <p className="text-sm font-medium uppercase tracking-widest text-muted-foreground mb-4">
          Introducing Our Platform
        </p>

        {/* Main Headline */}
        <h1 className="font-display text-5xl font-bold tracking-tighter text-balance mb-6">
          Build beautiful products{' '}
          <span className="text-primary">faster than ever</span>
        </h1>

        {/* Subheadline */}
        <p className="font-text text-xl text-muted-foreground leading-relaxed max-w-2xl mx-auto mb-8">
          The modern toolkit for designers and developers.
          Ship stunning interfaces in record time.
        </p>

        {/* CTA */}
        <div className="flex justify-center gap-4">
          <button className="font-medium">Get Started</button>
          <button className="font-medium text-muted-foreground">Learn More</button>
        </div>
      </div>
    </section>
  );
}
```

### 카드 타이포그래피

```tsx
// components/ui/feature-card.tsx
interface FeatureCardProps {
  title: string;
  description: string;
  icon: React.ReactNode;
}

export function FeatureCard({ title, description, icon }: FeatureCardProps) {
  return (
    <div className="group p-6 rounded-2xl border bg-card hover:shadow-lg transition-shadow">
      {/* Icon */}
      <div className="mb-4">{icon}</div>

      {/* Title */}
      <h3 className="font-display text-lg font-semibold tracking-tight mb-2 group-hover:text-primary transition-colors">
        {title}
      </h3>

      {/* Description */}
      <p className="font-text text-sm text-muted-foreground leading-relaxed">
        {description}
      </p>
    </div>
  );
}
```
