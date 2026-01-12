# Performance Skill

프론트엔드 성능 최적화 및 Core Web Vitals 달성을 위한 종합 가이드입니다.

## Triggers

- "성능", "performance", "최적화", "Core Web Vitals", "LCP", "CLS", "lighthouse"

---

## 성능 최적화 영역

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                     Frontend Performance Optimization                        │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  ┌──────────────────┐ │
│  │ Core Web     │  │ Font         │  │ Image        │  │ Animation       │ │
│  │ Vitals       │  │ Optimization │  │ Optimization │  │ Performance     │ │
│  ├──────────────┤  ├──────────────┤  ├──────────────┤  ├──────────────────┤ │
│  │ LCP < 2.5s   │  │ font-display │  │ next/image   │  │ GPU Accel       │ │
│  │ INP < 200ms  │  │ Subsetting   │  │ WebP/AVIF    │  │ will-change     │ │
│  │ CLS < 0.1    │  │ Preload      │  │ Lazy Load    │  │ Layout Thrash   │ │
│  └──────────────┘  └──────────────┘  └──────────────┘  └──────────────────┘ │
│                                                                              │
│  ┌──────────────┐  ┌──────────────┐                                         │
│  │ CSS          │  │ Bundle       │                                         │
│  │ Optimization │  │ Analysis     │                                         │
│  ├──────────────┤  ├──────────────┤                                         │
│  │ Critical CSS │  │ Tree Shaking │                                         │
│  │ Purge Unused │  │ Code Split   │                                         │
│  │ @layer       │  │ Dynamic      │                                         │
│  └──────────────┘  └──────────────┘                                         │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 1. Core Web Vitals 목표

### 핵심 메트릭

| 메트릭 | 이름 | 목표 (Good) | 개선 필요 | 측정 방식 |
|--------|------|-------------|-----------|-----------|
| **LCP** | Largest Contentful Paint | < 2.5s | > 4.0s | 가장 큰 콘텐츠 렌더링 시간 |
| **INP** | Interaction to Next Paint | < 200ms | > 500ms | 인터랙션 후 페인트 시간 |
| **CLS** | Cumulative Layout Shift | < 0.1 | > 0.25 | 레이아웃 이동 누적 점수 |

### LCP 최적화

```tsx
// 1. LCP 요소에 priority 설정
import Image from 'next/image';

function HeroSection() {
  return (
    <section className="relative h-[60vh]">
      {/* LCP 요소 - priority로 즉시 로드 */}
      <Image
        src="/hero.jpg"
        alt="Hero"
        fill
        priority  // preload 추가됨
        sizes="100vw"
        className="object-cover"
      />
      <div className="relative z-10 container py-20">
        <h1 className="text-5xl font-bold">Welcome</h1>
      </div>
    </section>
  );
}

// 2. 중요 리소스 프리로드
// app/layout.tsx
export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html>
      <head>
        {/* 중요 폰트 프리로드 */}
        <link
          rel="preload"
          href="/fonts/pretendard-variable.woff2"
          as="font"
          type="font/woff2"
          crossOrigin="anonymous"
        />
        {/* LCP 이미지 프리로드 */}
        <link
          rel="preload"
          href="/hero.jpg"
          as="image"
          fetchPriority="high"
        />
      </head>
      <body>{children}</body>
    </html>
  );
}
```

### INP 최적화

```tsx
'use client';

import { useTransition, useOptimistic } from 'react';

// 무거운 상태 업데이트를 트랜지션으로 처리
function SearchForm() {
  const [isPending, startTransition] = useTransition();
  const [results, setResults] = useState<Result[]>([]);

  const handleSearch = (query: string) => {
    // UI 즉시 반응, 무거운 작업은 트랜지션으로
    startTransition(() => {
      const filtered = heavyFilterOperation(query);
      setResults(filtered);
    });
  };

  return (
    <div>
      <input
        type="search"
        onChange={(e) => handleSearch(e.target.value)}
        className="w-full px-4 py-2 border rounded"
      />
      {isPending && <Spinner className="animate-spin" />}
      <ResultList results={results} />
    </div>
  );
}

// Optimistic UI로 즉각적인 피드백
function LikeButton({ postId, initialLiked }: { postId: string; initialLiked: boolean }) {
  const [optimisticLiked, setOptimisticLiked] = useOptimistic(initialLiked);

  const handleLike = async () => {
    setOptimisticLiked(!optimisticLiked);  // 즉시 UI 업데이트
    await toggleLike(postId);  // 서버 요청
  };

  return (
    <button onClick={handleLike} aria-pressed={optimisticLiked}>
      <Heart fill={optimisticLiked ? 'red' : 'none'} />
    </button>
  );
}
```

### CLS 최적화

```tsx
// 1. 이미지 크기 명시
<Image
  src="/photo.jpg"
  alt="Photo"
  width={800}
  height={600}  // 비율 유지
  className="w-full h-auto"
/>

// 2. aspect-ratio로 공간 예약
<div className="relative aspect-video">
  <Image src="/video-thumb.jpg" alt="Video" fill />
</div>

// 3. 동적 콘텐츠에 min-height 설정
<div className="min-h-[200px]">
  <Suspense fallback={<Skeleton className="h-[200px]" />}>
    <AsyncContent />
  </Suspense>
</div>

// 4. 폰트 로딩 시 레이아웃 시프트 방지
const font = DM_Sans({
  subsets: ['latin'],
  display: 'swap',  // 폴백 폰트 먼저 표시
  adjustFontFallback: true,  // 폴백 메트릭스 조정
});
```

---

## 2. 폰트 최적화

### font-display 전략

```css
/* 폰트 로딩 전략 */
@font-face {
  font-family: 'Pretendard';
  src: url('/fonts/pretendard.woff2') format('woff2');
  font-weight: 400;
  font-style: normal;
  font-display: swap;  /* 폴백 → 커스텀 폰트로 교체 */
}

/*
  font-display 옵션:
  - auto: 브라우저 기본 동작
  - block: 최대 3초 보이지 않음 → 커스텀 폰트
  - swap: 폴백 즉시 표시 → 커스텀 폰트로 교체 (권장)
  - fallback: 100ms 보이지 않음 → 폴백, 3초 내 로드되면 교체
  - optional: 100ms 보이지 않음 → 폴백 유지 (네트워크 고려)
*/
```

### Next.js 폰트 최적화

```tsx
// app/layout.tsx
import { DM_Sans, Noto_Sans_KR } from 'next/font/google';
import localFont from 'next/font/local';

// Google Fonts (자동 최적화)
const dmSans = DM_Sans({
  subsets: ['latin'],
  display: 'swap',
  variable: '--font-dm-sans',
  preload: true,
});

// 한글 폰트 (필요한 weight만)
const notoSansKR = Noto_Sans_KR({
  subsets: ['latin'],
  weight: ['400', '500', '700'],  // 필요한 것만
  display: 'swap',
  variable: '--font-noto',
});

// 로컬 폰트 (Variable Font 권장)
const pretendard = localFont({
  src: [
    {
      path: '../public/fonts/Pretendard-Regular.woff2',
      weight: '400',
      style: 'normal',
    },
    {
      path: '../public/fonts/Pretendard-Medium.woff2',
      weight: '500',
      style: 'normal',
    },
    {
      path: '../public/fonts/Pretendard-Bold.woff2',
      weight: '700',
      style: 'normal',
    },
  ],
  display: 'swap',
  variable: '--font-pretendard',
});

// Variable Font (더 효율적)
const pretendardVariable = localFont({
  src: '../public/fonts/PretendardVariable.woff2',
  display: 'swap',
  variable: '--font-pretendard',
  weight: '100 900',  // Variable 범위
});

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="ko" className={`${pretendardVariable.variable}`}>
      <body className="font-sans">{children}</body>
    </html>
  );
}
```

### 폰트 서브셋팅

```bash
# pyftsubset으로 서브셋 생성
pip install fonttools brotli

# 한글 자주 사용 글자 + 영문 + 숫자 + 특수문자
pyftsubset Pretendard-Regular.ttf \
  --text-file=korean-subset.txt \
  --output-file=Pretendard-Regular-subset.woff2 \
  --flavor=woff2

# 또는 Unicode 범위 지정
pyftsubset Pretendard-Regular.ttf \
  --unicodes="U+0020-007E,U+AC00-D7AF,U+1100-11FF" \
  --output-file=Pretendard-Regular-subset.woff2 \
  --flavor=woff2
```

### Variable Font 이점

```css
/* Static Font: 여러 파일 필요 */
@font-face {
  font-family: 'Pretendard';
  src: url('/fonts/Pretendard-Regular.woff2') format('woff2');
  font-weight: 400;
}
@font-face {
  font-family: 'Pretendard';
  src: url('/fonts/Pretendard-Medium.woff2') format('woff2');
  font-weight: 500;
}
@font-face {
  font-family: 'Pretendard';
  src: url('/fonts/Pretendard-Bold.woff2') format('woff2');
  font-weight: 700;
}
/* 3개 파일 = ~150KB */

/* Variable Font: 하나의 파일로 모든 weight */
@font-face {
  font-family: 'Pretendard Variable';
  src: url('/fonts/PretendardVariable.woff2') format('woff2');
  font-weight: 100 900;
}
/* 1개 파일 = ~80KB (압축 효율 높음) */

/* 사용 시 어떤 weight도 가능 */
.text-thin { font-weight: 100; }
.text-regular { font-weight: 400; }
.text-semibold { font-weight: 600; }
.text-bold { font-weight: 700; }
.text-heavy { font-weight: 850; }  /* 중간 값도 가능 */
```

---

## 3. 이미지 최적화

### next/image 활용

```tsx
import Image from 'next/image';

// 기본 사용 - 자동 최적화
<Image
  src="/photo.jpg"
  alt="Photo"
  width={800}
  height={600}
/>

// Fill 모드 - 컨테이너 채우기
<div className="relative aspect-video">
  <Image
    src="/hero.jpg"
    alt="Hero"
    fill
    sizes="(max-width: 768px) 100vw, (max-width: 1200px) 50vw, 33vw"
    className="object-cover"
  />
</div>

// 플레이스홀더 - Blur
<Image
  src="/photo.jpg"
  alt="Photo"
  width={800}
  height={600}
  placeholder="blur"
  blurDataURL="data:image/jpeg;base64,/9j/4AAQSkZJRg..."
/>
```

### 이미지 포맷 설정

```typescript
// next.config.ts
import type { NextConfig } from 'next';

const nextConfig: NextConfig = {
  images: {
    formats: ['image/avif', 'image/webp'],  // 최신 포맷 우선
    remotePatterns: [
      {
        protocol: 'https',
        hostname: '**.cloudinary.com',
      },
    ],
    deviceSizes: [640, 750, 828, 1080, 1200, 1920, 2048, 3840],
    imageSizes: [16, 32, 48, 64, 96, 128, 256, 384],
    minimumCacheTTL: 60 * 60 * 24 * 30,  // 30일 캐시
  },
};

export default nextConfig;
```

### 지연 로딩

```tsx
// 기본: 뷰포트 진입 시 로드
<Image
  src="/photo.jpg"
  alt="Photo"
  width={800}
  height={600}
  loading="lazy"  // 기본값
/>

// Above the fold: 즉시 로드
<Image
  src="/hero.jpg"
  alt="Hero"
  width={1200}
  height={600}
  priority  // loading="eager" + preload
/>

// 커스텀 지연 로딩 거리
// next.config.ts
const nextConfig: NextConfig = {
  images: {
    lazyBoundary: '500px',  // 뷰포트 500px 전에 로드 시작
  },
};
```

### 이미지 CDN 최적화

```tsx
// Cloudinary 통합 예시
function cloudinaryLoader({ src, width, quality }: {
  src: string;
  width: number;
  quality?: number;
}) {
  const params = [
    `w_${width}`,
    `q_${quality || 'auto'}`,
    'f_auto',  // 자동 포맷 선택
    'c_limit',  // 비율 유지
  ];
  return `https://res.cloudinary.com/demo/image/upload/${params.join(',')}/${src}`;
}

<Image
  loader={cloudinaryLoader}
  src="sample.jpg"
  alt="Sample"
  width={800}
  height={600}
/>
```

---

## 4. 애니메이션 성능

### GPU 가속 속성

```css
/* GPU 가속되는 속성 (Compositor-only) */
.gpu-accelerated {
  transform: translateX(100px);  /* ✅ GPU */
  opacity: 0.5;  /* ✅ GPU */
  filter: blur(5px);  /* ✅ GPU */
}

/* GPU 가속되지 않는 속성 (Layout/Paint 트리거) */
.cpu-bound {
  left: 100px;  /* ❌ Layout 트리거 */
  width: 200px;  /* ❌ Layout 트리거 */
  background-color: red;  /* ❌ Paint 트리거 */
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);  /* ❌ Paint 트리거 */
}
```

### 성능 좋은 애니메이션 패턴

```css
/* ❌ Bad: left/top 애니메이션 */
@keyframes slideLeft {
  from { left: 0; }
  to { left: 100px; }
}

/* ✅ Good: transform 애니메이션 */
@keyframes slideLeft {
  from { transform: translateX(0); }
  to { transform: translateX(100px); }
}

/* ❌ Bad: width 애니메이션 */
@keyframes grow {
  from { width: 0; }
  to { width: 100%; }
}

/* ✅ Good: scaleX 애니메이션 */
@keyframes grow {
  from { transform: scaleX(0); }
  to { transform: scaleX(1); }
}
```

### will-change 사용법

```css
/* will-change 주의사항:
   - 필요할 때만 적용 (항상 적용 X)
   - 사용 후 제거
   - 너무 많은 요소에 적용 X
*/

/* ❌ Bad: 모든 요소에 적용 */
* {
  will-change: transform;
}

/* ✅ Good: 호버 시에만 적용 */
.card {
  transition: transform 0.2s;
}

.card:hover {
  will-change: transform;
  transform: translateY(-4px);
}

/* ✅ Good: 애니메이션 중에만 적용 */
.animating {
  will-change: transform, opacity;
}
```

```tsx
// JavaScript로 동적 관리
function AnimatedCard() {
  const [isAnimating, setIsAnimating] = useState(false);

  return (
    <div
      className={cn(
        'transition-transform duration-200',
        isAnimating && 'will-change-transform'
      )}
      onMouseEnter={() => setIsAnimating(true)}
      onMouseLeave={() => setIsAnimating(false)}
      onTransitionEnd={() => setIsAnimating(false)}
    >
      {/* 콘텐츠 */}
    </div>
  );
}
```

### 레이아웃 스래싱 방지

```tsx
// ❌ Bad: 강제 동기 레이아웃
function badExample() {
  const elements = document.querySelectorAll('.item');

  elements.forEach(el => {
    const height = el.offsetHeight;  // Read → Layout 강제
    el.style.height = height + 10 + 'px';  // Write → Layout 무효화
    // 다음 루프에서 다시 Layout...
  });
}

// ✅ Good: 읽기/쓰기 분리
function goodExample() {
  const elements = document.querySelectorAll('.item');

  // 1. 먼저 모두 읽기
  const heights = Array.from(elements).map(el => el.offsetHeight);

  // 2. 그 다음 모두 쓰기
  elements.forEach((el, i) => {
    el.style.height = heights[i] + 10 + 'px';
  });
}

// ✅ Better: requestAnimationFrame 사용
function betterExample() {
  requestAnimationFrame(() => {
    // 읽기
    const heights = Array.from(elements).map(el => el.offsetHeight);

    requestAnimationFrame(() => {
      // 쓰기 (다음 프레임)
      elements.forEach((el, i) => {
        el.style.height = heights[i] + 10 + 'px';
      });
    });
  });
}
```

---

## 5. CSS 최적화

### Critical CSS

```tsx
// app/layout.tsx
// Next.js는 자동으로 critical CSS 인라인

// 수동으로 critical CSS 인라인 (특수 케이스)
export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html>
      <head>
        <style
          dangerouslySetInnerHTML={{
            __html: `
              /* Critical CSS - Above the fold */
              body { margin: 0; font-family: system-ui; }
              .hero { min-height: 100vh; display: flex; }
            `,
          }}
        />
      </head>
      <body>{children}</body>
    </html>
  );
}
```

### 미사용 CSS 제거

```typescript
// next.config.ts - Tailwind v4는 자동 purge
// 추가 설정 필요 없음

// Tailwind v3 설정 (참고)
// tailwind.config.js
module.exports = {
  content: [
    './app/**/*.{js,ts,jsx,tsx}',
    './components/**/*.{js,ts,jsx,tsx}',
  ],
  // safelist는 최소화
  safelist: [],
};
```

### CSS 레이어 최적화

```css
/* globals.css */
@import "tailwindcss";

/* 레이어 순서 정의 */
@layer reset, base, tokens, components, utilities;

/* 레이어별 스타일 */
@layer reset {
  *, *::before, *::after {
    box-sizing: border-box;
  }
}

@layer base {
  body {
    @apply bg-background text-foreground;
  }
}

@layer components {
  .btn-primary {
    @apply px-4 py-2 bg-primary text-primary-foreground rounded-md;
  }
}

/* utilities는 항상 마지막 (Tailwind 자동) */
```

---

## 6. 번들 분석

### Next.js 번들 분석

```bash
# 번들 분석기 설치
npm install -D @next/bundle-analyzer

# 분석 실행
ANALYZE=true npm run build
```

```typescript
// next.config.ts
import bundleAnalyzer from '@next/bundle-analyzer';

const withBundleAnalyzer = bundleAnalyzer({
  enabled: process.env.ANALYZE === 'true',
  openAnalyzer: true,
});

const nextConfig = {
  // ...설정
};

export default withBundleAnalyzer(nextConfig);
```

### 동적 임포트

```tsx
import dynamic from 'next/dynamic';

// 기본 동적 임포트
const HeavyChart = dynamic(() => import('@/components/charts/heavy-chart'), {
  loading: () => <Skeleton className="h-[400px]" />,
});

// SSR 비활성화 (클라이언트 전용)
const ClientOnlyMap = dynamic(
  () => import('@/components/map/interactive-map'),
  {
    ssr: false,
    loading: () => <div className="h-[400px] bg-muted animate-pulse" />,
  }
);

// 조건부 로딩
function Dashboard({ isAdmin }: { isAdmin: boolean }) {
  return (
    <div>
      <CommonContent />
      {isAdmin && <AdminPanel />}  {/* 필요시에만 로드 */}
    </div>
  );
}

const AdminPanel = dynamic(() => import('@/features/admin/panel'));
```

### Tree Shaking 최적화

```typescript
// ❌ Bad: 전체 라이브러리 임포트
import _ from 'lodash';
const result = _.debounce(fn, 300);

// ✅ Good: 필요한 함수만 임포트
import debounce from 'lodash/debounce';
const result = debounce(fn, 300);

// ❌ Bad: 아이콘 전체 임포트
import * as Icons from 'lucide-react';

// ✅ Good: 필요한 아이콘만
import { Home, Settings, User } from 'lucide-react';

// ✅ Best: barrel 파일 피하기
// 직접 임포트
import { Button } from '@/components/ui/button';
import { Card } from '@/components/ui/card';

// ❌ 피하기
import { Button, Card } from '@/components/ui';  // barrel 파일
```

### 패키지 크기 분석

```bash
# 패키지 크기 확인
npx cost-of-modules

# 특정 패키지 번들 크기 확인
npx bundlephobia <package-name>
```

---

## 7. Lighthouse 감사 체크리스트

### 성능 (Performance)

```markdown
## Lighthouse Performance Checklist

### First Contentful Paint (FCP)
- [ ] 서버 응답 시간 최적화 (TTFB < 600ms)
- [ ] 렌더링 차단 리소스 제거
- [ ] 텍스트 압축 활성화 (gzip/brotli)

### Largest Contentful Paint (LCP)
- [ ] LCP 요소에 priority 설정
- [ ] 서버 사이드 렌더링 활용
- [ ] 이미지 최적화 (포맷, 크기)
- [ ] CDN 사용

### Total Blocking Time (TBT) / INP
- [ ] JavaScript 번들 최소화
- [ ] 긴 작업 분할 (Long Tasks)
- [ ] 메인 스레드 작업 최소화
- [ ] 서드파티 스크립트 지연 로드

### Cumulative Layout Shift (CLS)
- [ ] 이미지/비디오에 크기 지정
- [ ] 동적 콘텐츠 공간 예약
- [ ] 웹폰트 FOUT/FOIT 최소화
- [ ] 광고/임베드 공간 예약
```

### 접근성 (Accessibility)

```markdown
## Lighthouse Accessibility Checklist

- [ ] 이미지 alt 텍스트
- [ ] 폼 레이블
- [ ] 색상 대비
- [ ] 포커스 표시
- [ ] 시맨틱 HTML
- [ ] ARIA 속성
```

### 모범 사례 (Best Practices)

```markdown
## Lighthouse Best Practices Checklist

- [ ] HTTPS 사용
- [ ] 안전하지 않은 라이브러리 없음
- [ ] 콘솔 오류 없음
- [ ] 올바른 이미지 비율
```

### SEO

```markdown
## Lighthouse SEO Checklist

- [ ] 메타 description
- [ ] 문서 title
- [ ] 크롤링 가능한 링크
- [ ] 모바일 친화적
- [ ] robots.txt
```

---

## 8. 성능 모니터링

### Web Vitals 측정

```tsx
// app/layout.tsx
import { SpeedInsights } from '@vercel/speed-insights/next';
import { Analytics } from '@vercel/analytics/next';

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html>
      <body>
        {children}
        <SpeedInsights />  {/* Core Web Vitals 측정 */}
        <Analytics />  {/* 페이지뷰 분석 */}
      </body>
    </html>
  );
}
```

### 커스텀 Web Vitals 리포팅

```tsx
// lib/web-vitals.ts
import { onCLS, onINP, onLCP, onFCP, onTTFB, Metric } from 'web-vitals';

function sendToAnalytics(metric: Metric) {
  const body = JSON.stringify({
    id: metric.id,
    name: metric.name,
    value: metric.value,
    rating: metric.rating,  // 'good' | 'needs-improvement' | 'poor'
    navigationType: metric.navigationType,
  });

  // Beacon API로 전송 (페이지 이탈 시에도 전송됨)
  if (navigator.sendBeacon) {
    navigator.sendBeacon('/api/analytics/vitals', body);
  } else {
    fetch('/api/analytics/vitals', {
      method: 'POST',
      body,
      keepalive: true,
    });
  }
}

export function reportWebVitals() {
  onCLS(sendToAnalytics);
  onINP(sendToAnalytics);
  onLCP(sendToAnalytics);
  onFCP(sendToAnalytics);
  onTTFB(sendToAnalytics);
}

// 클라이언트에서 호출
// components/web-vitals-reporter.tsx
'use client';

import { useEffect } from 'react';
import { reportWebVitals } from '@/lib/web-vitals';

export function WebVitalsReporter() {
  useEffect(() => {
    reportWebVitals();
  }, []);

  return null;
}
```

### 성능 경고 시스템

```typescript
// lib/performance/thresholds.ts
export const THRESHOLDS = {
  LCP: { good: 2500, poor: 4000 },
  INP: { good: 200, poor: 500 },
  CLS: { good: 0.1, poor: 0.25 },
  FCP: { good: 1800, poor: 3000 },
  TTFB: { good: 800, poor: 1800 },
} as const;

export function getMetricRating(
  name: keyof typeof THRESHOLDS,
  value: number
): 'good' | 'needs-improvement' | 'poor' {
  const threshold = THRESHOLDS[name];
  if (value <= threshold.good) return 'good';
  if (value <= threshold.poor) return 'needs-improvement';
  return 'poor';
}

// 슬랙/디스코드 알림
async function alertPoorMetric(metric: Metric) {
  if (metric.rating === 'poor') {
    await fetch(process.env.SLACK_WEBHOOK_URL!, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        text: `⚠️ Poor ${metric.name}: ${metric.value.toFixed(2)}`,
        blocks: [
          {
            type: 'section',
            text: {
              type: 'mrkdwn',
              text: `*Performance Alert*\n${metric.name}: ${metric.value.toFixed(2)} (${metric.rating})`,
            },
          },
        ],
      }),
    });
  }
}
```

---

## 9. 테스트 자동화

### Playwright 성능 테스트

```typescript
// e2e/performance.spec.ts
import { test, expect } from '@playwright/test';

test.describe('Performance', () => {
  test('homepage loads within performance budget', async ({ page }) => {
    // 성능 메트릭 수집
    await page.goto('/', { waitUntil: 'networkidle' });

    const metrics = await page.evaluate(() => {
      const paint = performance.getEntriesByType('paint');
      const navigation = performance.getEntriesByType('navigation')[0] as PerformanceNavigationTiming;

      return {
        fcp: paint.find(p => p.name === 'first-contentful-paint')?.startTime,
        lcp: 0,  // PerformanceObserver로 측정 필요
        ttfb: navigation.responseStart - navigation.requestStart,
        domContentLoaded: navigation.domContentLoadedEventEnd,
        load: navigation.loadEventEnd,
      };
    });

    // 예산 검증
    expect(metrics.fcp).toBeLessThan(1800);
    expect(metrics.ttfb).toBeLessThan(600);
    expect(metrics.domContentLoaded).toBeLessThan(3000);
  });

  test('LCP element loads quickly', async ({ page }) => {
    await page.goto('/');

    const lcp = await page.evaluate(() => {
      return new Promise<number>((resolve) => {
        new PerformanceObserver((list) => {
          const entries = list.getEntries();
          const lastEntry = entries[entries.length - 1];
          resolve(lastEntry.startTime);
        }).observe({ type: 'largest-contentful-paint', buffered: true });

        // 5초 타임아웃
        setTimeout(() => resolve(5000), 5000);
      });
    });

    expect(lcp).toBeLessThan(2500);
  });

  test('no layout shifts during load', async ({ page }) => {
    await page.goto('/');

    // 5초 대기 후 CLS 측정
    await page.waitForTimeout(5000);

    const cls = await page.evaluate(() => {
      return new Promise<number>((resolve) => {
        let clsValue = 0;
        new PerformanceObserver((list) => {
          for (const entry of list.getEntries()) {
            if (!(entry as any).hadRecentInput) {
              clsValue += (entry as any).value;
            }
          }
        }).observe({ type: 'layout-shift', buffered: true });

        setTimeout(() => resolve(clsValue), 100);
      });
    });

    expect(cls).toBeLessThan(0.1);
  });
});
```

### Lighthouse CI

```yaml
# .github/workflows/lighthouse.yml
name: Lighthouse CI

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  lighthouse:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - uses: actions/setup-node@v4
        with:
          node-version: 20

      - name: Install dependencies
        run: npm ci

      - name: Build
        run: npm run build

      - name: Run Lighthouse CI
        uses: treosh/lighthouse-ci-action@v12
        with:
          configPath: ./lighthouserc.js
          uploadArtifacts: true
          temporaryPublicStorage: true
```

```javascript
// lighthouserc.js
module.exports = {
  ci: {
    collect: {
      url: [
        'http://localhost:3000/',
        'http://localhost:3000/products',
        'http://localhost:3000/about',
      ],
      numberOfRuns: 3,
      startServerCommand: 'npm run start',
    },
    assert: {
      preset: 'lighthouse:recommended',
      assertions: {
        // Core Web Vitals
        'largest-contentful-paint': ['error', { maxNumericValue: 2500 }],
        'cumulative-layout-shift': ['error', { maxNumericValue: 0.1 }],
        'total-blocking-time': ['error', { maxNumericValue: 300 }],

        // 카테고리 점수
        'categories:performance': ['error', { minScore: 0.9 }],
        'categories:accessibility': ['error', { minScore: 0.95 }],
        'categories:best-practices': ['error', { minScore: 0.9 }],
        'categories:seo': ['error', { minScore: 0.9 }],

        // 개별 감사
        'first-contentful-paint': ['warn', { maxNumericValue: 1800 }],
        'speed-index': ['warn', { maxNumericValue: 3400 }],
        'interactive': ['warn', { maxNumericValue: 3800 }],
      },
    },
    upload: {
      target: 'temporary-public-storage',
    },
  },
};
```

---

## 10. 일반적인 문제 및 해결

### 문제: 느린 페이지 로드

```tsx
// 원인 1: 서버 컴포넌트에서 직렬 데이터 페칭

// ❌ Bad: 순차 페칭
async function Page() {
  const user = await getUser();  // 1초
  const posts = await getPosts();  // 1초
  const comments = await getComments();  // 1초
  // 총 3초
}

// ✅ Good: 병렬 페칭
async function Page() {
  const [user, posts, comments] = await Promise.all([
    getUser(),
    getPosts(),
    getComments(),
  ]);
  // 총 1초 (가장 느린 것)
}

// ✅ Better: Suspense로 스트리밍
async function Page() {
  return (
    <div>
      <Suspense fallback={<UserSkeleton />}>
        <UserSection />
      </Suspense>
      <Suspense fallback={<PostsSkeleton />}>
        <PostsSection />
      </Suspense>
    </div>
  );
}
```

### 문제: 큰 JavaScript 번들

```typescript
// 원인: 모든 코드가 한 번에 로드됨

// ❌ Bad: 정적 임포트
import { FullCalendar } from 'some-huge-calendar';
import { RichTextEditor } from 'some-huge-editor';

// ✅ Good: 동적 임포트
const FullCalendar = dynamic(() => import('some-huge-calendar'), {
  ssr: false,
  loading: () => <CalendarSkeleton />,
});

// ✅ Good: 라우트 기반 코드 분할
// Next.js는 페이지별 자동 코드 분할
// app/calendar/page.tsx (별도 청크)
// app/editor/page.tsx (별도 청크)
```

### 문제: 이미지 레이아웃 시프트

```tsx
// 원인: 이미지 크기 미지정

// ❌ Bad
<img src="/photo.jpg" alt="Photo" />

// ✅ Good: 크기 명시
<Image src="/photo.jpg" alt="Photo" width={800} height={600} />

// ✅ Good: aspect-ratio로 공간 예약
<div className="aspect-video relative">
  <Image src="/photo.jpg" alt="Photo" fill className="object-cover" />
</div>
```

### 문제: 느린 Third-Party 스크립트

```tsx
// 원인: 렌더링 차단

// ❌ Bad: 동기 로드
<script src="https://analytics.example.com/script.js" />

// ✅ Good: Script 컴포넌트 사용
import Script from 'next/script';

<Script
  src="https://analytics.example.com/script.js"
  strategy="lazyOnload"  // 페이지 로드 후 로드
/>

// 전략 옵션:
// - beforeInteractive: 페이지 수화 전 (필수 스크립트만)
// - afterInteractive: 페이지 수화 후 (기본값)
// - lazyOnload: 브라우저 유휴 시간에 (분석 등)
// - worker: Web Worker에서 실행 (실험적)
```

---

## 체크리스트 요약

### 개발 전
- [ ] 성능 예산 정의 (LCP, CLS, INP)
- [ ] 이미지 포맷 전략 수립
- [ ] 폰트 로딩 전략 수립

### 개발 중
- [ ] next/image 사용
- [ ] 이미지에 priority/sizes 설정
- [ ] 동적 임포트 활용
- [ ] Suspense 경계 설정
- [ ] GPU 가속 애니메이션 사용

### 개발 후
- [ ] Lighthouse 90+ 달성
- [ ] Core Web Vitals 통과
- [ ] 번들 크기 분석
- [ ] 실제 사용자 모니터링 (RUM) 설정

---

## References

- `17-responsive/SKILL.md` (반응형 이미지 최적화)
- `4-typography/SKILL.md` (폰트 최적화)
- `7-motion/SKILL.md` (애니메이션 성능)
