# Responsive Design Skill

반응형 디자인 검증 및 최적화를 위한 종합 가이드입니다.

## Triggers

- "반응형", "responsive", "브레이크포인트", "모바일", "breakpoint"

---

## 반응형 설계 전략

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                      Responsive Design Strategy                              │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│   Mobile First Approach                                                      │
│   ─────────────────────                                                      │
│                                                                              │
│   📱 320px    →    📱 640px    →    💻 1024px    →    🖥️ 1280px+           │
│   (base)          (sm)              (lg)               (xl)                 │
│                                                                              │
│   ┌─────────┐    ┌─────────┐    ┌───────────────┐    ┌───────────────────┐ │
│   │ Stack   │    │ 2-col   │    │ Sidebar +     │    │ Full Dashboard    │ │
│   │ Layout  │    │ Grid    │    │ Main Content  │    │ with Panels       │ │
│   └─────────┘    └─────────┘    └───────────────┘    └───────────────────┘ │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 1. 브레이크포인트 시스템

### Tailwind CSS v4 브레이크포인트

```css
/* globals.css - Tailwind v4 기본 브레이크포인트 */
@theme {
  --breakpoint-sm: 640px;   /* 소형 태블릿, 대형 폰 (가로) */
  --breakpoint-md: 768px;   /* 태블릿 세로 */
  --breakpoint-lg: 1024px;  /* 태블릿 가로, 소형 노트북 */
  --breakpoint-xl: 1280px;  /* 데스크톱 */
  --breakpoint-2xl: 1536px; /* 대형 데스크톱 */
}
```

### 브레이크포인트 사용 가이드

| 브레이크포인트 | 너비 | 대상 디바이스 | 주요 레이아웃 변화 |
|---------------|------|--------------|-------------------|
| **base** | < 640px | 모바일 | 단일 컬럼, 풀 너비 |
| **sm** | >= 640px | 대형 폰, 소형 태블릿 | 2컬럼 그리드 시작 |
| **md** | >= 768px | 태블릿 세로 | 네비게이션 확장 |
| **lg** | >= 1024px | 태블릿 가로, 노트북 | 사이드바 표시 |
| **xl** | >= 1280px | 데스크톱 | 전체 레이아웃 |
| **2xl** | >= 1536px | 대형 모니터 | 최대 너비 제한 |

### 커스텀 브레이크포인트

```css
/* 필요시 커스텀 브레이크포인트 추가 */
@theme {
  --breakpoint-xs: 475px;   /* 소형 폰 */
  --breakpoint-3xl: 1920px; /* 초대형 모니터 */
}
```

---

## 2. Mobile-First 접근법

### 기본 원칙

```tsx
// ❌ Bad: Desktop-first (min-width에서 시작)
<div className="grid grid-cols-3 md:grid-cols-2 sm:grid-cols-1">

// ✅ Good: Mobile-first (base에서 시작하여 확장)
<div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3">
```

### 구현 패턴

```tsx
// 레이아웃 예시
function DashboardLayout({ children }: { children: React.ReactNode }) {
  return (
    <div className="min-h-screen flex flex-col lg:flex-row">
      {/* 모바일: 상단 헤더 / 데스크톱: 좌측 사이드바 */}
      <Sidebar className="w-full lg:w-64 lg:min-h-screen" />

      <main className="flex-1 p-4 lg:p-8">
        {children}
      </main>
    </div>
  );
}

// 그리드 예시
function CardGrid({ items }: { items: Item[] }) {
  return (
    <div className="
      grid gap-4
      grid-cols-1      /* 모바일: 1열 */
      sm:grid-cols-2   /* sm: 2열 */
      lg:grid-cols-3   /* lg: 3열 */
      xl:grid-cols-4   /* xl: 4열 */
    ">
      {items.map(item => <Card key={item.id} {...item} />)}
    </div>
  );
}
```

### 반응형 간격

```tsx
// 섹션 간격
<section className="py-8 md:py-12 lg:py-16 xl:py-20">
  <div className="container px-4 md:px-6 lg:px-8">
    {/* 콘텐츠 */}
  </div>
</section>

// 카드 내부 패딩
<Card className="p-4 md:p-6 lg:p-8">
  <CardHeader className="space-y-2 md:space-y-4">
    {/* 헤더 */}
  </CardHeader>
</Card>
```

---

## 3. Container Queries

### 설정

```css
/* globals.css */
@import "tailwindcss";

/* Container Query 지원 */
.card-container {
  container-type: inline-size;
  container-name: card;
}
```

### 사용법

```tsx
// 컨테이너 기반 반응형
function ResponsiveCard({ children }: { children: React.ReactNode }) {
  return (
    <div className="card-container">
      <div className="
        flex flex-col
        @[400px]:flex-row
        @[600px]:gap-6
      ">
        {children}
      </div>
    </div>
  );
}

// Tailwind v4 컨테이너 쿼리
<div className="@container">
  <div className="
    flex flex-col
    @sm:flex-row       /* 컨테이너 >= 640px */
    @md:gap-4          /* 컨테이너 >= 768px */
    @lg:items-center   /* 컨테이너 >= 1024px */
  ">
    {/* 콘텐츠 */}
  </div>
</div>
```

### 컨테이너 vs 뷰포트

```tsx
// 뷰포트 기반: 화면 전체 크기에 반응
<div className="sm:flex md:grid">
  {/* 화면 크기에 따라 변경 */}
</div>

// 컨테이너 기반: 부모 요소 크기에 반응
<div className="@container">
  <div className="@sm:flex @md:grid">
    {/* 부모 컨테이너 크기에 따라 변경 */}
  </div>
</div>
```

---

## 4. 반응형 타이포그래피

### Fluid Typography

```css
/* globals.css */
:root {
  /* clamp(최소, 선호, 최대) */
  --font-size-xs: clamp(0.75rem, 0.7rem + 0.25vw, 0.875rem);
  --font-size-sm: clamp(0.875rem, 0.8rem + 0.375vw, 1rem);
  --font-size-base: clamp(1rem, 0.9rem + 0.5vw, 1.125rem);
  --font-size-lg: clamp(1.125rem, 1rem + 0.625vw, 1.25rem);
  --font-size-xl: clamp(1.25rem, 1.1rem + 0.75vw, 1.5rem);
  --font-size-2xl: clamp(1.5rem, 1.25rem + 1.25vw, 2rem);
  --font-size-3xl: clamp(1.875rem, 1.5rem + 1.875vw, 2.5rem);
  --font-size-4xl: clamp(2.25rem, 1.75rem + 2.5vw, 3rem);
  --font-size-5xl: clamp(3rem, 2rem + 5vw, 4rem);
}

/* 적용 */
h1 { font-size: var(--font-size-5xl); }
h2 { font-size: var(--font-size-4xl); }
h3 { font-size: var(--font-size-3xl); }
h4 { font-size: var(--font-size-2xl); }
p { font-size: var(--font-size-base); }
```

### 브레이크포인트 기반 타이포그래피

```tsx
// 제목 컴포넌트
function Heading({ children }: { children: React.ReactNode }) {
  return (
    <h1 className="
      text-2xl        /* 모바일: 24px */
      sm:text-3xl     /* sm: 30px */
      md:text-4xl     /* md: 36px */
      lg:text-5xl     /* lg: 48px */
      font-bold
      tracking-tight
    ">
      {children}
    </h1>
  );
}

// 본문 컴포넌트
function Body({ children }: { children: React.ReactNode }) {
  return (
    <p className="
      text-base       /* 모바일: 16px */
      md:text-lg      /* md: 18px */
      leading-relaxed
      md:leading-loose
    ">
      {children}
    </p>
  );
}
```

---

## 5. 이미지 최적화

### srcset과 sizes

```tsx
// next/image 사용
import Image from 'next/image';

function ResponsiveHero() {
  return (
    <div className="relative aspect-video w-full">
      <Image
        src="/hero.jpg"
        alt="Hero image"
        fill
        sizes="
          (max-width: 640px) 100vw,
          (max-width: 1024px) 80vw,
          1200px
        "
        priority
        className="object-cover"
      />
    </div>
  );
}

// 아트 디렉션 (다른 크기에 다른 이미지)
function ArtDirectedImage() {
  return (
    <picture>
      <source
        media="(min-width: 1024px)"
        srcSet="/hero-desktop.jpg"
      />
      <source
        media="(min-width: 640px)"
        srcSet="/hero-tablet.jpg"
      />
      <Image
        src="/hero-mobile.jpg"
        alt="Hero"
        width={640}
        height={360}
        className="w-full h-auto"
      />
    </picture>
  );
}
```

### 반응형 이미지 패턴

```tsx
// 가로세로비 유지
<div className="relative aspect-[16/9] md:aspect-[21/9]">
  <Image
    src="/banner.jpg"
    alt="Banner"
    fill
    className="object-cover"
  />
</div>

// 배경 이미지
<div
  className="
    bg-cover bg-center
    h-48 sm:h-64 md:h-80 lg:h-96
  "
  style={{ backgroundImage: 'url(/hero.jpg)' }}
/>
```

---

## 6. 레이아웃 시프트 방지

### 이미지 공간 예약

```tsx
// ❌ Bad: 크기 미지정
<Image src="/photo.jpg" alt="Photo" />

// ✅ Good: 크기 명시
<Image
  src="/photo.jpg"
  alt="Photo"
  width={800}
  height={600}
  className="w-full h-auto"
/>

// ✅ Good: 컨테이너로 비율 유지
<div className="relative aspect-video">
  <Image
    src="/photo.jpg"
    alt="Photo"
    fill
    className="object-cover"
  />
</div>
```

### Skeleton 로딩

```tsx
// 카드 스켈레톤
function CardSkeleton() {
  return (
    <Card className="overflow-hidden">
      {/* 이미지 영역 */}
      <Skeleton className="aspect-video w-full" />

      <CardContent className="p-4 space-y-3">
        {/* 제목 */}
        <Skeleton className="h-6 w-3/4" />
        {/* 설명 */}
        <Skeleton className="h-4 w-full" />
        <Skeleton className="h-4 w-5/6" />
      </CardContent>
    </Card>
  );
}

// 그리드 스켈레톤
function GridSkeleton({ count = 6 }: { count?: number }) {
  return (
    <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
      {Array.from({ length: count }).map((_, i) => (
        <CardSkeleton key={i} />
      ))}
    </div>
  );
}
```

### 폰트 레이아웃 시프트 방지

```tsx
// app/layout.tsx
import { DM_Sans } from 'next/font/google';

const dmSans = DM_Sans({
  subsets: ['latin'],
  display: 'swap',
  variable: '--font-dm-sans',
  // 폴백 폰트 메트릭스 조정
  adjustFontFallback: true,
});

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="ko" className={inter.variable}>
      <body className="font-sans">{children}</body>
    </html>
  );
}
```

---

## 7. Touch vs Hover 감지

### CSS 미디어 쿼리

```css
/* 포인터 장치 감지 */
@media (hover: hover) and (pointer: fine) {
  /* 마우스/트랙패드 사용자 */
  .interactive-card:hover {
    transform: translateY(-4px);
    box-shadow: var(--shadow-lg);
  }
}

@media (hover: none) and (pointer: coarse) {
  /* 터치 스크린 사용자 */
  .interactive-card:active {
    transform: scale(0.98);
  }
}

/* Tailwind CSS로 적용 */
.card {
  @apply transition-all duration-200;
  @apply hover:[@media(hover:hover)]:shadow-lg hover:[@media(hover:hover)]:-translate-y-1;
  @apply active:[@media(hover:none)]:scale-[0.98];
}
```

### JavaScript 감지

```tsx
'use client';

import { useState, useEffect } from 'react';

export function useTouchDevice(): boolean {
  const [isTouch, setIsTouch] = useState(false);

  useEffect(() => {
    const checkTouch = () => {
      setIsTouch(
        'ontouchstart' in window ||
        navigator.maxTouchPoints > 0 ||
        window.matchMedia('(hover: none)').matches
      );
    };

    checkTouch();
    window.addEventListener('resize', checkTouch);
    return () => window.removeEventListener('resize', checkTouch);
  }, []);

  return isTouch;
}

// 사용 예시
function InteractiveCard({ children }: { children: React.ReactNode }) {
  const isTouch = useTouchDevice();

  return (
    <div
      className={cn(
        'transition-all duration-200',
        !isTouch && 'hover:shadow-lg hover:-translate-y-1',
        isTouch && 'active:scale-[0.98]'
      )}
    >
      {children}
    </div>
  );
}
```

---

## 8. 브레이크포인트별 테스트 체크리스트

### 모바일 (< 640px)

```markdown
## 모바일 테스트 체크리스트

### 레이아웃
- [ ] 단일 컬럼 레이아웃
- [ ] 수평 스크롤 없음
- [ ] 터치 타겟 최소 44x44px
- [ ] 충분한 탭 간격 (8px+)

### 네비게이션
- [ ] 햄버거 메뉴 작동
- [ ] 모바일 드로어 적절한 크기
- [ ] 쉬운 닫기 (X 버튼, 오버레이 탭)

### 폼
- [ ] 입력 필드 100% 너비
- [ ] 적절한 키보드 타입 (email, tel, number)
- [ ] 레이블 가시성
- [ ] 에러 메시지 표시

### 콘텐츠
- [ ] 텍스트 가독성 (최소 16px)
- [ ] 이미지 적절한 크기
- [ ] 테이블 → 카드 변환
```

### 태블릿 (640px - 1024px)

```markdown
## 태블릿 테스트 체크리스트

### 레이아웃
- [ ] 2컬럼 그리드 적용
- [ ] 사이드바 숨김/축소
- [ ] 충분한 콘텐츠 영역

### 네비게이션
- [ ] 네비게이션 바 확장 또는 유지
- [ ] 드롭다운 메뉴 작동

### 인터랙션
- [ ] 호버/터치 둘 다 고려
- [ ] 스와이프 제스처 (캐러셀 등)
```

### 데스크톱 (>= 1024px)

```markdown
## 데스크톱 테스트 체크리스트

### 레이아웃
- [ ] 전체 레이아웃 표시 (사이드바 + 메인)
- [ ] 최대 너비 제한 (1280px 또는 1440px)
- [ ] 중앙 정렬

### 네비게이션
- [ ] 전체 네비게이션 바 표시
- [ ] 드롭다운 호버 작동
- [ ] 키보드 네비게이션

### 인터랙션
- [ ] 호버 상태 명확
- [ ] 포커스 표시 명확
- [ ] 툴팁 표시
```

---

## 9. 일반적인 반응형 패턴

### Stack to Grid

```tsx
// 모바일: 세로 스택 → 데스크톱: 그리드
function FeatureSection() {
  return (
    <div className="
      flex flex-col gap-6
      md:grid md:grid-cols-2
      lg:grid-cols-3
    ">
      <FeatureCard icon={<Zap />} title="빠름" />
      <FeatureCard icon={<Shield />} title="안전" />
      <FeatureCard icon={<Heart />} title="신뢰" />
    </div>
  );
}
```

### Sidebar Collapse

```tsx
'use client';

import { useState } from 'react';
import { Sheet, SheetContent, SheetTrigger } from '@/components/ui/sheet';
import { Menu } from 'lucide-react';

function ResponsiveSidebar() {
  const [open, setOpen] = useState(false);

  return (
    <>
      {/* 모바일: 시트 트리거 */}
      <div className="lg:hidden">
        <Sheet open={open} onOpenChange={setOpen}>
          <SheetTrigger asChild>
            <Button variant="ghost" size="icon">
              <Menu />
            </Button>
          </SheetTrigger>
          <SheetContent side="left" className="w-64">
            <SidebarContent />
          </SheetContent>
        </Sheet>
      </div>

      {/* 데스크톱: 항상 표시 */}
      <aside className="hidden lg:block w-64 border-r min-h-screen">
        <SidebarContent />
      </aside>
    </>
  );
}
```

### Navigation Transformation

```tsx
function ResponsiveNav() {
  return (
    <header className="sticky top-0 z-50 bg-background border-b">
      <div className="container flex items-center justify-between h-16">
        <Logo />

        {/* 모바일: 햄버거 메뉴 */}
        <div className="lg:hidden">
          <MobileMenu />
        </div>

        {/* 데스크톱: 전체 네비게이션 */}
        <nav className="hidden lg:flex items-center gap-6">
          <NavLink href="/features">기능</NavLink>
          <NavLink href="/pricing">가격</NavLink>
          <NavLink href="/docs">문서</NavLink>
          <Button>시작하기</Button>
        </nav>
      </div>
    </header>
  );
}
```

### Table to Card

```tsx
function ResponsiveDataDisplay({ data }: { data: User[] }) {
  return (
    <>
      {/* 데스크톱: 테이블 */}
      <div className="hidden md:block">
        <Table>
          <TableHeader>
            <TableRow>
              <TableHead>이름</TableHead>
              <TableHead>이메일</TableHead>
              <TableHead>역할</TableHead>
              <TableHead>가입일</TableHead>
            </TableRow>
          </TableHeader>
          <TableBody>
            {data.map(user => (
              <TableRow key={user.id}>
                <TableCell>{user.name}</TableCell>
                <TableCell>{user.email}</TableCell>
                <TableCell>{user.role}</TableCell>
                <TableCell>{user.createdAt}</TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </div>

      {/* 모바일: 카드 리스트 */}
      <div className="md:hidden space-y-4">
        {data.map(user => (
          <Card key={user.id}>
            <CardContent className="p-4 space-y-2">
              <div className="font-medium">{user.name}</div>
              <div className="text-sm text-muted-foreground">{user.email}</div>
              <div className="flex justify-between text-sm">
                <Badge>{user.role}</Badge>
                <span className="text-muted-foreground">{user.createdAt}</span>
              </div>
            </CardContent>
          </Card>
        ))}
      </div>
    </>
  );
}
```

---

## 10. 브라우저 테스트 매트릭스

### 지원 브라우저

| 브라우저 | 최소 버전 | 테스트 우선순위 |
|----------|-----------|-----------------|
| **Chrome** | 최신 2버전 | 높음 |
| **Safari** | 최신 2버전 | 높음 (iOS 필수) |
| **Firefox** | 최신 2버전 | 중간 |
| **Edge** | 최신 2버전 | 중간 |
| **Samsung Internet** | 최신 버전 | 중간 (Android) |

### 테스트 디바이스

| 디바이스 | 화면 크기 | 테스트 포인트 |
|----------|-----------|---------------|
| **iPhone SE** | 375 x 667 | 최소 모바일 |
| **iPhone 14 Pro** | 393 x 852 | 일반 모바일 |
| **iPad** | 768 x 1024 | 태블릿 세로 |
| **iPad Pro** | 1024 x 1366 | 태블릿 가로 |
| **Laptop** | 1366 x 768 | 소형 데스크톱 |
| **Desktop** | 1920 x 1080 | 일반 데스크톱 |
| **4K Monitor** | 2560 x 1440 | 대형 데스크톱 |

### Playwright 테스트

```typescript
// e2e/responsive.spec.ts
import { test, expect, devices } from '@playwright/test';

const viewports = [
  { name: 'Mobile', ...devices['iPhone 14'] },
  { name: 'Tablet', ...devices['iPad'] },
  { name: 'Desktop', viewport: { width: 1280, height: 720 } },
];

viewports.forEach(({ name, viewport }) => {
  test.describe(`${name} viewport`, () => {
    test.use({ viewport });

    test('navigation is accessible', async ({ page }) => {
      await page.goto('/');

      if (name === 'Mobile') {
        // 햄버거 메뉴 확인
        const menuButton = page.getByRole('button', { name: /menu/i });
        await expect(menuButton).toBeVisible();
        await menuButton.click();
        await expect(page.getByRole('navigation')).toBeVisible();
      } else {
        // 전체 네비게이션 확인
        await expect(page.getByRole('navigation')).toBeVisible();
        await expect(page.getByRole('link', { name: '기능' })).toBeVisible();
      }
    });

    test('no horizontal scroll', async ({ page }) => {
      await page.goto('/');

      const hasHorizontalScroll = await page.evaluate(() => {
        return document.documentElement.scrollWidth > document.documentElement.clientWidth;
      });

      expect(hasHorizontalScroll).toBe(false);
    });

    test('touch targets are adequate', async ({ page }) => {
      await page.goto('/');

      const buttons = page.getByRole('button');
      const buttonCount = await buttons.count();

      for (let i = 0; i < buttonCount; i++) {
        const button = buttons.nth(i);
        const box = await button.boundingBox();

        if (box) {
          expect(box.width).toBeGreaterThanOrEqual(44);
          expect(box.height).toBeGreaterThanOrEqual(44);
        }
      }
    });
  });
});
```

---

## 11. 성능 고려사항

### 조건부 렌더링

```tsx
// ❌ Bad: 모든 뷰포트에서 모두 렌더링 후 숨김
<div className="hidden lg:block">
  <HeavyDesktopComponent />
</div>
<div className="lg:hidden">
  <HeavyMobileComponent />
</div>

// ✅ Good: 필요한 것만 렌더링
'use client';

import { useMediaQuery } from '@/hooks/use-media-query';

function ResponsiveComponent() {
  const isDesktop = useMediaQuery('(min-width: 1024px)');

  // 하나만 렌더링
  return isDesktop ? <DesktopComponent /> : <MobileComponent />;
}
```

### useMediaQuery 훅

```tsx
// hooks/use-media-query.ts
'use client';

import { useState, useEffect } from 'react';

export function useMediaQuery(query: string): boolean {
  const [matches, setMatches] = useState(false);

  useEffect(() => {
    const mediaQuery = window.matchMedia(query);
    setMatches(mediaQuery.matches);

    const handler = (e: MediaQueryListEvent) => setMatches(e.matches);
    mediaQuery.addEventListener('change', handler);
    return () => mediaQuery.removeEventListener('change', handler);
  }, [query]);

  return matches;
}

// 사전 정의된 훅
export function useIsMobile() {
  return useMediaQuery('(max-width: 639px)');
}

export function useIsTablet() {
  return useMediaQuery('(min-width: 640px) and (max-width: 1023px)');
}

export function useIsDesktop() {
  return useMediaQuery('(min-width: 1024px)');
}
```

### 이미지 반응형 로딩

```tsx
// 뷰포트별 다른 이미지
function ResponsiveImage() {
  return (
    <picture>
      {/* 대형 화면용 고해상도 */}
      <source
        media="(min-width: 1024px)"
        srcSet="/hero-lg.webp 1x, /hero-lg@2x.webp 2x"
        type="image/webp"
      />
      {/* 중간 화면 */}
      <source
        media="(min-width: 640px)"
        srcSet="/hero-md.webp"
        type="image/webp"
      />
      {/* 모바일 (기본) */}
      <Image
        src="/hero-sm.jpg"
        alt="Hero"
        width={640}
        height={360}
        priority
        className="w-full h-auto"
      />
    </picture>
  );
}
```

---

## 12. 일반적인 문제 및 해결

### 문제: 수평 스크롤

```css
/* 원인: 요소가 뷰포트를 넘침 */

/* 해결 1: 오버플로우 제어 */
html, body {
  overflow-x: hidden;
}

/* 해결 2: 너비 제한 */
.container {
  max-width: 100%;
  padding-inline: 1rem;
}

/* 해결 3: 문제 요소 찾기 */
* {
  outline: 1px solid red; /* 디버깅용 */
}
```

### 문제: 폰트 크기 자동 확대 (iOS)

```css
/* iOS Safari에서 입력 필드 포커스 시 확대 방지 */
input, select, textarea {
  font-size: 16px; /* 최소 16px */
}

/* 또는 메타 태그로 제어 (비권장) */
/* <meta name="viewport" content="width=device-width, initial-scale=1, maximum-scale=1"> */
```

### 문제: 100vh 모바일 이슈

```css
/* 모바일 브라우저 주소창 고려 */
.full-height {
  /* 폴백 */
  min-height: 100vh;
  /* 모던 브라우저 */
  min-height: 100dvh;
}

/* CSS 변수 활용 */
:root {
  --vh: 1vh;
}

.full-height {
  min-height: calc(var(--vh, 1vh) * 100);
}
```

```tsx
// JavaScript로 실제 뷰포트 높이 계산
'use client';

import { useEffect } from 'react';

export function ViewportHeightFix() {
  useEffect(() => {
    const setVh = () => {
      const vh = window.innerHeight * 0.01;
      document.documentElement.style.setProperty('--vh', `${vh}px`);
    };

    setVh();
    window.addEventListener('resize', setVh);
    return () => window.removeEventListener('resize', setVh);
  }, []);

  return null;
}
```

---

## 체크리스트 요약

### 설계 단계
- [ ] Mobile-first 접근법 적용
- [ ] 브레이크포인트 전략 수립
- [ ] 콘텐츠 우선순위 정의

### 개발 단계
- [ ] Fluid 타이포그래피 적용
- [ ] 반응형 이미지 최적화
- [ ] Container queries 활용 (필요시)
- [ ] 터치/호버 인터랙션 분리

### 테스트 단계
- [ ] 모든 브레이크포인트 테스트
- [ ] 실제 디바이스 테스트
- [ ] 레이아웃 시프트 확인
- [ ] 수평 스크롤 확인

---

## References

- `6-spacing/SKILL.md` (반응형 간격 시스템)
- `4-typography/SKILL.md` (반응형 타이포그래피)
- `15-mobile/SKILL.md` (모바일 특화 패턴)
