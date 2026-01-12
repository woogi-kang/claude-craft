# Mobile-First Design Skill

모바일 퍼스트 디자인 및 앱 같은 웹 경험을 위한 종합 스킬입니다.

## Triggers

- "모바일", "mobile", "앱", "app", "PWA", "반응형"

---

## Input

| 항목 | 필수 | 설명 |
|------|------|------|
| `appType` | ✅ | 애플리케이션 유형 (pwa, hybrid, responsive) |
| `targetPlatform` | ❌ | 타겟 플랫폼 (ios, android, both) |
| `features` | ❌ | 필요한 기능 목록 |

---

## Mobile-First 원칙

### 디자인 철학

```markdown
## Mobile-First 설계 원칙

1. **콘텐츠 우선**
   - 핵심 콘텐츠와 기능을 먼저 정의
   - 불필요한 요소 제거
   - 점진적으로 데스크톱 기능 추가

2. **터치 우선**
   - 모든 인터랙티브 요소 44px 이상
   - 충분한 여백으로 오탭 방지
   - 제스처 지원 (스와이프, 핀치)

3. **성능 우선**
   - 초기 로딩 최소화
   - 이미지 지연 로딩
   - 오프라인 지원 고려

4. **네이티브 경험**
   - 플랫폼 관습 존중
   - 익숙한 패턴 사용
   - 부드러운 애니메이션
```

---

## Mobile Navigation

### 1. Bottom Tab Navigation

```tsx
// components/mobile/bottom-nav.tsx
"use client";

import { usePathname } from "next/navigation";
import Link from "next/link";
import { cn } from "@/lib/utils";
import { Home, Search, Plus, Bell, User, LucideIcon } from "lucide-react";
import { motion } from "framer-motion";

interface NavItem {
  icon: LucideIcon;
  label: string;
  href: string;
  badge?: number;
}

const navItems: NavItem[] = [
  { icon: Home, label: "홈", href: "/" },
  { icon: Search, label: "검색", href: "/search" },
  { icon: Plus, label: "만들기", href: "/create" },
  { icon: Bell, label: "알림", href: "/notifications", badge: 3 },
  { icon: User, label: "프로필", href: "/profile" },
];

export function BottomNav() {
  const pathname = usePathname();

  return (
    <nav
      className="fixed bottom-0 left-0 right-0 z-50 bg-background/80 backdrop-blur-lg border-t border-border pb-safe"
      role="navigation"
      aria-label="하단 네비게이션"
    >
      <div className="flex items-center justify-around h-16 max-w-lg mx-auto">
        {navItems.map((item) => {
          const isActive = pathname === item.href;
          const Icon = item.icon;

          return (
            <Link
              key={item.href}
              href={item.href}
              className={cn(
                "relative flex flex-col items-center justify-center flex-1 h-full",
                "transition-colors",
                isActive ? "text-primary" : "text-muted-foreground"
              )}
            >
              <div className="relative">
                <Icon
                  className={cn(
                    "h-6 w-6 transition-transform",
                    isActive && "scale-110"
                  )}
                />

                {/* Badge */}
                {item.badge && item.badge > 0 && (
                  <span className="absolute -top-1 -right-1 min-w-[18px] h-[18px] px-1 flex items-center justify-center text-xs font-medium bg-red-500 text-white rounded-full">
                    {item.badge > 99 ? "99+" : item.badge}
                  </span>
                )}
              </div>

              <span className="mt-1 text-xs font-medium">{item.label}</span>

              {/* Active Indicator */}
              {isActive && (
                <motion.div
                  className="absolute top-0 left-1/2 -translate-x-1/2 w-8 h-0.5 bg-primary rounded-full"
                  layoutId="bottomNavIndicator"
                />
              )}
            </Link>
          );
        })}
      </div>
    </nav>
  );
}

// Safe Area 대응 CSS
// globals.css에 추가
/*
:root {
  --safe-area-inset-bottom: env(safe-area-inset-bottom, 0px);
}

.pb-safe {
  padding-bottom: max(0.5rem, var(--safe-area-inset-bottom));
}
*/
```

### 2. Hamburger Menu (Side Drawer)

```tsx
// components/mobile/mobile-menu.tsx
"use client";

import { useState, useEffect } from "react";
import { usePathname } from "next/navigation";
import Link from "next/link";
import { motion, AnimatePresence } from "framer-motion";
import { Button } from "@/components/ui/button";
import { cn } from "@/lib/utils";
import {
  Menu,
  X,
  Home,
  Settings,
  User,
  ChevronRight,
  LogOut,
} from "lucide-react";

interface MenuItem {
  icon: React.ComponentType<{ className?: string }>;
  label: string;
  href?: string;
  onClick?: () => void;
  children?: MenuItem[];
}

const menuItems: MenuItem[] = [
  { icon: Home, label: "홈", href: "/" },
  { icon: User, label: "프로필", href: "/profile" },
  {
    icon: Settings,
    label: "설정",
    children: [
      { icon: Settings, label: "계정", href: "/settings/account" },
      { icon: Settings, label: "알림", href: "/settings/notifications" },
      { icon: Settings, label: "보안", href: "/settings/security" },
    ],
  },
];

export function MobileMenu() {
  const [isOpen, setIsOpen] = useState(false);
  const [expandedItem, setExpandedItem] = useState<string | null>(null);
  const pathname = usePathname();

  // 페이지 이동 시 메뉴 닫기
  useEffect(() => {
    setIsOpen(false);
  }, [pathname]);

  // 스크롤 잠금
  useEffect(() => {
    if (isOpen) {
      document.body.style.overflow = "hidden";
    } else {
      document.body.style.overflow = "";
    }
    return () => {
      document.body.style.overflow = "";
    };
  }, [isOpen]);

  return (
    <>
      {/* Trigger Button */}
      <Button
        variant="ghost"
        size="icon"
        className="lg:hidden"
        onClick={() => setIsOpen(true)}
        aria-label="메뉴 열기"
      >
        <Menu className="h-6 w-6" />
      </Button>

      {/* Overlay & Drawer */}
      <AnimatePresence>
        {isOpen && (
          <>
            {/* Backdrop */}
            <motion.div
              className="fixed inset-0 z-50 bg-black/50 lg:hidden"
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              exit={{ opacity: 0 }}
              onClick={() => setIsOpen(false)}
            />

            {/* Drawer */}
            <motion.aside
              className="fixed top-0 left-0 z-50 h-full w-[280px] bg-background border-r border-border lg:hidden"
              initial={{ x: "-100%" }}
              animate={{ x: 0 }}
              exit={{ x: "-100%" }}
              transition={{ type: "spring", damping: 25, stiffness: 300 }}
            >
              {/* Header */}
              <div className="flex items-center justify-between h-16 px-4 border-b border-border">
                <span className="font-semibold text-lg">메뉴</span>
                <Button
                  variant="ghost"
                  size="icon"
                  onClick={() => setIsOpen(false)}
                  aria-label="메뉴 닫기"
                >
                  <X className="h-5 w-5" />
                </Button>
              </div>

              {/* User Info */}
              <div className="p-4 border-b border-border">
                <div className="flex items-center gap-3">
                  <div className="w-12 h-12 rounded-full bg-gradient-to-br from-primary to-primary/60" />
                  <div>
                    <p className="font-medium">사용자 이름</p>
                    <p className="text-sm text-muted-foreground">user@email.com</p>
                  </div>
                </div>
              </div>

              {/* Menu Items */}
              <nav className="flex-1 overflow-y-auto p-2">
                <ul className="space-y-1">
                  {menuItems.map((item) => (
                    <li key={item.label}>
                      {item.children ? (
                        // Expandable Item
                        <div>
                          <button
                            className={cn(
                              "w-full flex items-center justify-between px-3 py-3 rounded-lg",
                              "text-foreground hover:bg-muted transition-colors"
                            )}
                            onClick={() =>
                              setExpandedItem(
                                expandedItem === item.label ? null : item.label
                              )
                            }
                          >
                            <div className="flex items-center gap-3">
                              <item.icon className="h-5 w-5" />
                              <span className="font-medium">{item.label}</span>
                            </div>
                            <ChevronRight
                              className={cn(
                                "h-5 w-5 transition-transform",
                                expandedItem === item.label && "rotate-90"
                              )}
                            />
                          </button>

                          {/* Submenu */}
                          <AnimatePresence>
                            {expandedItem === item.label && (
                              <motion.ul
                                className="ml-8 mt-1 space-y-1"
                                initial={{ height: 0, opacity: 0 }}
                                animate={{ height: "auto", opacity: 1 }}
                                exit={{ height: 0, opacity: 0 }}
                              >
                                {item.children.map((child) => (
                                  <li key={child.label}>
                                    <Link
                                      href={child.href!}
                                      className={cn(
                                        "flex items-center px-3 py-2.5 rounded-lg text-sm",
                                        pathname === child.href
                                          ? "bg-primary/10 text-primary"
                                          : "text-muted-foreground hover:text-foreground hover:bg-muted"
                                      )}
                                    >
                                      {child.label}
                                    </Link>
                                  </li>
                                ))}
                              </motion.ul>
                            )}
                          </AnimatePresence>
                        </div>
                      ) : (
                        // Regular Item
                        <Link
                          href={item.href!}
                          className={cn(
                            "flex items-center gap-3 px-3 py-3 rounded-lg",
                            pathname === item.href
                              ? "bg-primary/10 text-primary"
                              : "text-foreground hover:bg-muted"
                          )}
                        >
                          <item.icon className="h-5 w-5" />
                          <span className="font-medium">{item.label}</span>
                        </Link>
                      )}
                    </li>
                  ))}
                </ul>
              </nav>

              {/* Footer */}
              <div className="p-4 border-t border-border">
                <button className="flex items-center gap-3 w-full px-3 py-3 text-red-600 hover:bg-red-50 dark:hover:bg-red-950/50 rounded-lg transition-colors">
                  <LogOut className="h-5 w-5" />
                  <span className="font-medium">로그아웃</span>
                </button>
              </div>
            </motion.aside>
          </>
        )}
      </AnimatePresence>
    </>
  );
}
```

---

## Touch-Friendly Design

### 터치 타겟 사이즈 가이드

```tsx
// components/mobile/touch-target.tsx
import { cn } from "@/lib/utils";
import { Slot } from "@radix-ui/react-slot";

interface TouchTargetProps {
  children: React.ReactNode;
  className?: string;
  asChild?: boolean;
}

/**
 * 터치 타겟 래퍼 컴포넌트
 * WCAG 2.5.5 기준: 최소 44x44px
 */
export function TouchTarget({
  children,
  className,
  asChild,
}: TouchTargetProps) {
  const Comp = asChild ? Slot : "div";

  return (
    <Comp
      className={cn(
        // 최소 터치 영역 보장
        "min-h-[44px] min-w-[44px]",
        // 터치 하이라이트 제거 (iOS)
        "touch-manipulation",
        // 탭 하이라이트 커스텀 (Android)
        "-webkit-tap-highlight-color-transparent",
        className
      )}
    >
      {children}
    </Comp>
  );
}

// 사용 예시
function ExampleButton() {
  return (
    <TouchTarget asChild>
      <button className="p-2 rounded-lg bg-primary text-primary-foreground">
        <span className="text-sm">작은 텍스트여도 터치 영역은 44px</span>
      </button>
    </TouchTarget>
  );
}
```

### 터치 타겟 체크리스트

```markdown
## 터치 타겟 디자인 체크리스트

### 최소 사이즈
- [ ] 버튼: 최소 44x44px (권장: 48x48px)
- [ ] 링크: 최소 44px 높이
- [ ] 아이콘 버튼: 48x48px 터치 영역

### 간격
- [ ] 인접 터치 요소 간 최소 8px 간격
- [ ] 밀집된 영역(목록)에서 최소 12px 간격

### 시각적 피드백
- [ ] 터치 시 즉각적인 피드백 (0.1초 이내)
- [ ] 활성 상태 스타일 명확
- [ ] 비활성 상태 시각적으로 구분

### 제스처
- [ ] 스와이프 영역 명확하게 표시
- [ ] 실수로 트리거되지 않도록 임계값 설정
- [ ] 제스처 + 대체 버튼 제공
```

---

## Swipe Gestures

### 스와이프 가능한 카드

```tsx
// components/mobile/swipeable-card.tsx
"use client";

import { useState } from "react";
import {
  motion,
  useMotionValue,
  useTransform,
  PanInfo,
} from "framer-motion";
import { cn } from "@/lib/utils";
import { Trash2, Archive, Edit } from "lucide-react";

interface SwipeableCardProps {
  children: React.ReactNode;
  onDelete?: () => void;
  onArchive?: () => void;
  onEdit?: () => void;
}

export function SwipeableCard({
  children,
  onDelete,
  onArchive,
  onEdit,
}: SwipeableCardProps) {
  const [isDragging, setIsDragging] = useState(false);
  const x = useMotionValue(0);

  // 배경 액션 불투명도
  const leftOpacity = useTransform(x, [-100, 0], [1, 0]);
  const rightOpacity = useTransform(x, [0, 100], [0, 1]);

  const handleDragEnd = (
    event: MouseEvent | TouchEvent | PointerEvent,
    info: PanInfo
  ) => {
    const threshold = 100;

    if (info.offset.x < -threshold && onDelete) {
      onDelete();
    } else if (info.offset.x > threshold && onArchive) {
      onArchive();
    }

    setIsDragging(false);
  };

  return (
    <div className="relative overflow-hidden rounded-lg">
      {/* Left Action (Delete) */}
      <motion.div
        className="absolute inset-y-0 left-0 w-24 bg-red-500 flex items-center justify-center"
        style={{ opacity: leftOpacity }}
      >
        <Trash2 className="h-6 w-6 text-white" />
      </motion.div>

      {/* Right Action (Archive) */}
      <motion.div
        className="absolute inset-y-0 right-0 w-24 bg-blue-500 flex items-center justify-center"
        style={{ opacity: rightOpacity }}
      >
        <Archive className="h-6 w-6 text-white" />
      </motion.div>

      {/* Main Content */}
      <motion.div
        className={cn(
          "relative bg-card border border-border rounded-lg cursor-grab active:cursor-grabbing",
          isDragging && "shadow-lg"
        )}
        drag="x"
        dragConstraints={{ left: -120, right: 120 }}
        dragElastic={0.2}
        onDragStart={() => setIsDragging(true)}
        onDragEnd={handleDragEnd}
        style={{ x }}
      >
        {children}
      </motion.div>
    </div>
  );
}

// 사용 예시
function SwipeableListItem() {
  return (
    <SwipeableCard
      onDelete={() => console.log("Delete")}
      onArchive={() => console.log("Archive")}
    >
      <div className="p-4">
        <h3 className="font-medium">스와이프하여 액션</h3>
        <p className="text-sm text-muted-foreground">
          왼쪽으로 스와이프하여 삭제, 오른쪽으로 스와이프하여 보관
        </p>
      </div>
    </SwipeableCard>
  );
}
```

### 스와이프 캐러셀

```tsx
// components/mobile/swipe-carousel.tsx
"use client";

import { useRef, useState } from "react";
import { motion } from "framer-motion";
import { cn } from "@/lib/utils";

interface SwipeCarouselProps {
  children: React.ReactNode[];
  showDots?: boolean;
  autoPlay?: boolean;
  interval?: number;
}

export function SwipeCarousel({
  children,
  showDots = true,
  autoPlay = false,
  interval = 5000,
}: SwipeCarouselProps) {
  const [currentIndex, setCurrentIndex] = useState(0);
  const containerRef = useRef<HTMLDivElement>(null);

  const handleDragEnd = (
    e: MouseEvent | TouchEvent | PointerEvent,
    { offset, velocity }: { offset: { x: number }; velocity: { x: number } }
  ) => {
    const swipeThreshold = 50;
    const swipeVelocity = 500;

    if (offset.x < -swipeThreshold || velocity.x < -swipeVelocity) {
      // Swipe left (next)
      setCurrentIndex((prev) => Math.min(prev + 1, children.length - 1));
    } else if (offset.x > swipeThreshold || velocity.x > swipeVelocity) {
      // Swipe right (prev)
      setCurrentIndex((prev) => Math.max(prev - 1, 0));
    }
  };

  return (
    <div className="relative overflow-hidden" ref={containerRef}>
      {/* Slides */}
      <motion.div
        className="flex"
        animate={{ x: `-${currentIndex * 100}%` }}
        transition={{ type: "spring", stiffness: 300, damping: 30 }}
        drag="x"
        dragConstraints={{ left: 0, right: 0 }}
        dragElastic={0.1}
        onDragEnd={handleDragEnd}
      >
        {children.map((child, index) => (
          <div key={index} className="w-full flex-shrink-0">
            {child}
          </div>
        ))}
      </motion.div>

      {/* Dots */}
      {showDots && (
        <div className="flex justify-center gap-2 mt-4">
          {children.map((_, index) => (
            <button
              key={index}
              className={cn(
                "w-2 h-2 rounded-full transition-all",
                index === currentIndex
                  ? "bg-primary w-6"
                  : "bg-muted-foreground/30"
              )}
              onClick={() => setCurrentIndex(index)}
              aria-label={`슬라이드 ${index + 1}로 이동`}
            />
          ))}
        </div>
      )}
    </div>
  );
}
```

---

## Pull-to-Refresh

```tsx
// components/mobile/pull-to-refresh.tsx
"use client";

import { useState, useRef } from "react";
import {
  motion,
  useMotionValue,
  useTransform,
  useAnimation,
} from "framer-motion";
import { RefreshCw } from "lucide-react";

interface PullToRefreshProps {
  children: React.ReactNode;
  onRefresh: () => Promise<void>;
  threshold?: number;
}

export function PullToRefresh({
  children,
  onRefresh,
  threshold = 80,
}: PullToRefreshProps) {
  const [isRefreshing, setIsRefreshing] = useState(false);
  const containerRef = useRef<HTMLDivElement>(null);
  const y = useMotionValue(0);
  const controls = useAnimation();

  // 인디케이터 애니메이션
  const indicatorOpacity = useTransform(y, [0, threshold / 2, threshold], [0, 0.5, 1]);
  const indicatorScale = useTransform(y, [0, threshold], [0.5, 1]);
  const indicatorRotate = useTransform(y, [0, threshold * 2], [0, 360]);

  const handleDragEnd = async () => {
    const currentY = y.get();

    if (currentY >= threshold && !isRefreshing) {
      setIsRefreshing(true);

      // 리프레시 위치 유지
      await controls.start({ y: threshold / 2 });

      try {
        await onRefresh();
      } finally {
        setIsRefreshing(false);
        await controls.start({ y: 0 });
      }
    } else {
      // 원위치로 복귀
      await controls.start({ y: 0 });
    }
  };

  return (
    <div className="relative overflow-hidden" ref={containerRef}>
      {/* Pull Indicator */}
      <motion.div
        className="absolute top-0 left-0 right-0 flex items-center justify-center h-16 -translate-y-full"
        style={{
          opacity: indicatorOpacity,
          scale: indicatorScale,
          y: useTransform(y, [0, threshold], [-64, 0]),
        }}
      >
        <motion.div
          style={{ rotate: isRefreshing ? undefined : indicatorRotate }}
          animate={isRefreshing ? { rotate: 360 } : undefined}
          transition={
            isRefreshing
              ? { duration: 1, repeat: Infinity, ease: "linear" }
              : undefined
          }
        >
          <RefreshCw className="h-6 w-6 text-primary" />
        </motion.div>
      </motion.div>

      {/* Content */}
      <motion.div
        drag="y"
        dragConstraints={{ top: 0, bottom: 0 }}
        dragElastic={{ top: 0.5, bottom: 0 }}
        onDragEnd={handleDragEnd}
        animate={controls}
        style={{ y }}
        className="touch-pan-y"
      >
        {children}
      </motion.div>
    </div>
  );
}

// 사용 예시
function FeedPage() {
  const handleRefresh = async () => {
    await new Promise((resolve) => setTimeout(resolve, 2000));
    console.log("Refreshed!");
  };

  return (
    <PullToRefresh onRefresh={handleRefresh}>
      <div className="space-y-4 p-4">
        {/* Feed items */}
      </div>
    </PullToRefresh>
  );
}
```

---

## Bottom Sheet

```tsx
// components/mobile/bottom-sheet.tsx
"use client";

import { useRef, useEffect } from "react";
import {
  motion,
  useMotionValue,
  useTransform,
  useAnimation,
  PanInfo,
} from "framer-motion";
import { cn } from "@/lib/utils";

interface BottomSheetProps {
  isOpen: boolean;
  onClose: () => void;
  children: React.ReactNode;
  snapPoints?: number[]; // 퍼센트 (예: [0.25, 0.5, 0.9])
  initialSnap?: number;
  title?: string;
}

export function BottomSheet({
  isOpen,
  onClose,
  children,
  snapPoints = [0.4, 0.9],
  initialSnap = 0,
  title,
}: BottomSheetProps) {
  const sheetRef = useRef<HTMLDivElement>(null);
  const y = useMotionValue(0);
  const controls = useAnimation();

  // 화면 높이 기준 스냅 포인트 계산
  const windowHeight = typeof window !== "undefined" ? window.innerHeight : 800;
  const snapHeights = snapPoints.map((point) => windowHeight * (1 - point));

  const handleDragEnd = (
    event: MouseEvent | TouchEvent | PointerEvent,
    info: PanInfo
  ) => {
    const currentY = y.get();
    const velocity = info.velocity.y;

    // 빠르게 아래로 스와이프하면 닫기
    if (velocity > 500) {
      onClose();
      return;
    }

    // 가장 가까운 스냅 포인트 찾기
    const closestSnap = snapHeights.reduce((prev, curr) => {
      return Math.abs(curr - currentY) < Math.abs(prev - currentY)
        ? curr
        : prev;
    });

    // 가장 낮은 스냅 포인트보다 아래면 닫기
    if (currentY > snapHeights[0] + 100) {
      onClose();
    } else {
      controls.start({ y: closestSnap });
    }
  };

  useEffect(() => {
    if (isOpen) {
      controls.start({ y: snapHeights[initialSnap] });
    }
  }, [isOpen, initialSnap]);

  if (!isOpen) return null;

  return (
    <>
      {/* Backdrop */}
      <motion.div
        className="fixed inset-0 z-40 bg-black/50"
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        exit={{ opacity: 0 }}
        onClick={onClose}
      />

      {/* Sheet */}
      <motion.div
        ref={sheetRef}
        className="fixed inset-x-0 bottom-0 z-50 bg-background rounded-t-2xl shadow-2xl"
        style={{ y, height: windowHeight }}
        initial={{ y: windowHeight }}
        animate={controls}
        exit={{ y: windowHeight }}
        transition={{ type: "spring", damping: 30, stiffness: 300 }}
        drag="y"
        dragConstraints={{ top: snapHeights[snapHeights.length - 1], bottom: windowHeight }}
        dragElastic={0.2}
        onDragEnd={handleDragEnd}
      >
        {/* Handle */}
        <div className="flex justify-center pt-3 pb-2">
          <div className="w-10 h-1 rounded-full bg-muted-foreground/30" />
        </div>

        {/* Header */}
        {title && (
          <div className="px-4 py-2 border-b border-border">
            <h2 className="text-lg font-semibold text-center">{title}</h2>
          </div>
        )}

        {/* Content */}
        <div className="overflow-y-auto overscroll-contain px-4 py-4 h-full pb-safe">
          {children}
        </div>
      </motion.div>
    </>
  );
}

// 사용 예시
function ExamplePage() {
  const [isOpen, setIsOpen] = useState(false);

  return (
    <>
      <button onClick={() => setIsOpen(true)}>Open Sheet</button>

      <BottomSheet
        isOpen={isOpen}
        onClose={() => setIsOpen(false)}
        title="옵션 선택"
        snapPoints={[0.3, 0.6, 0.9]}
      >
        <div className="space-y-4">
          <button className="w-full p-4 text-left hover:bg-muted rounded-lg">
            옵션 1
          </button>
          <button className="w-full p-4 text-left hover:bg-muted rounded-lg">
            옵션 2
          </button>
          <button className="w-full p-4 text-left hover:bg-muted rounded-lg">
            옵션 3
          </button>
        </div>
      </BottomSheet>
    </>
  );
}
```

---

## Mobile Forms

```tsx
// components/mobile/mobile-form.tsx
"use client";

import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { z } from "zod";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { cn } from "@/lib/utils";

// 모바일 최적화된 입력 필드
interface MobileInputProps
  extends React.InputHTMLAttributes<HTMLInputElement> {
  label: string;
  error?: string;
}

export function MobileInput({
  label,
  error,
  className,
  ...props
}: MobileInputProps) {
  return (
    <div className="space-y-2">
      <label className="text-sm font-medium text-foreground">{label}</label>
      <input
        className={cn(
          // 기본 스타일
          "w-full px-4 py-3 text-base rounded-lg",
          "border border-input bg-background",
          "focus:outline-none focus:ring-2 focus:ring-primary focus:border-transparent",
          // 모바일 최적화
          "text-[16px]", // iOS 줌 방지 (16px 이상)
          "appearance-none", // 기본 스타일 제거
          // 에러 상태
          error && "border-red-500 focus:ring-red-500",
          className
        )}
        {...props}
      />
      {error && (
        <p className="text-sm text-red-500">{error}</p>
      )}
    </div>
  );
}

// 모바일 최적화 폼 예시
const loginSchema = z.object({
  email: z.string().email("올바른 이메일 주소를 입력하세요"),
  password: z.string().min(8, "비밀번호는 8자 이상이어야 합니다"),
});

export function MobileLoginForm() {
  const {
    register,
    handleSubmit,
    formState: { errors, isSubmitting },
  } = useForm({
    resolver: zodResolver(loginSchema),
  });

  const onSubmit = async (data: z.infer<typeof loginSchema>) => {
    // 로그인 처리
  };

  return (
    <form onSubmit={handleSubmit(onSubmit)} className="space-y-6 p-4">
      <MobileInput
        label="이메일"
        type="email"
        autoComplete="email"
        inputMode="email"
        placeholder="example@email.com"
        error={errors.email?.message}
        {...register("email")}
      />

      <MobileInput
        label="비밀번호"
        type="password"
        autoComplete="current-password"
        placeholder="비밀번호 입력"
        error={errors.password?.message}
        {...register("password")}
      />

      <Button
        type="submit"
        className="w-full h-12 text-base"
        disabled={isSubmitting}
      >
        {isSubmitting ? "로그인 중..." : "로그인"}
      </Button>
    </form>
  );
}
```

### 모바일 키보드 처리

```tsx
// hooks/use-keyboard.ts
"use client";

import { useEffect, useState } from "react";

export function useKeyboard() {
  const [isKeyboardOpen, setIsKeyboardOpen] = useState(false);
  const [keyboardHeight, setKeyboardHeight] = useState(0);

  useEffect(() => {
    // Visual Viewport API (iOS Safari, Chrome)
    if ("visualViewport" in window && window.visualViewport) {
      const viewport = window.visualViewport;

      const handleResize = () => {
        const heightDiff = window.innerHeight - viewport.height;
        setIsKeyboardOpen(heightDiff > 100);
        setKeyboardHeight(heightDiff);
      };

      viewport.addEventListener("resize", handleResize);
      return () => viewport.removeEventListener("resize", handleResize);
    }

    // Fallback: Focus/Blur 이벤트
    const handleFocus = () => setIsKeyboardOpen(true);
    const handleBlur = () => setIsKeyboardOpen(false);

    document.addEventListener("focusin", handleFocus);
    document.addEventListener("focusout", handleBlur);

    return () => {
      document.removeEventListener("focusin", handleFocus);
      document.removeEventListener("focusout", handleBlur);
    };
  }, []);

  return { isKeyboardOpen, keyboardHeight };
}

// 사용 예시: 키보드가 열리면 요소 위치 조정
function ChatInput() {
  const { isKeyboardOpen, keyboardHeight } = useKeyboard();

  return (
    <div
      className="fixed bottom-0 left-0 right-0 p-4 bg-background border-t"
      style={{ paddingBottom: isKeyboardOpen ? keyboardHeight : undefined }}
    >
      <input
        type="text"
        className="w-full p-3 rounded-full border"
        placeholder="메시지 입력..."
      />
    </div>
  );
}
```

---

## App-Like Transitions

```tsx
// components/mobile/page-transition.tsx
"use client";

import { motion, AnimatePresence } from "framer-motion";
import { usePathname } from "next/navigation";

interface PageTransitionProps {
  children: React.ReactNode;
}

// iOS 스타일 페이지 전환
export function IOSPageTransition({ children }: PageTransitionProps) {
  const pathname = usePathname();

  return (
    <AnimatePresence mode="wait" initial={false}>
      <motion.div
        key={pathname}
        initial={{ x: "100%", opacity: 0 }}
        animate={{ x: 0, opacity: 1 }}
        exit={{ x: "-30%", opacity: 0.5 }}
        transition={{
          type: "spring",
          stiffness: 300,
          damping: 30,
        }}
        className="min-h-screen"
      >
        {children}
      </motion.div>
    </AnimatePresence>
  );
}

// Android 스타일 페이지 전환 (Fade + Scale)
export function AndroidPageTransition({ children }: PageTransitionProps) {
  const pathname = usePathname();

  return (
    <AnimatePresence mode="wait" initial={false}>
      <motion.div
        key={pathname}
        initial={{ opacity: 0, scale: 0.95 }}
        animate={{ opacity: 1, scale: 1 }}
        exit={{ opacity: 0, scale: 1.05 }}
        transition={{ duration: 0.2 }}
        className="min-h-screen"
      >
        {children}
      </motion.div>
    </AnimatePresence>
  );
}

// Shared Element Transition (Hero Animation)
export function SharedElementTransition({
  children,
  layoutId,
}: {
  children: React.ReactNode;
  layoutId: string;
}) {
  return (
    <motion.div
      layoutId={layoutId}
      transition={{
        type: "spring",
        stiffness: 300,
        damping: 30,
      }}
    >
      {children}
    </motion.div>
  );
}
```

---

## Safe Area Handling

```tsx
// components/mobile/safe-area.tsx
import { cn } from "@/lib/utils";

interface SafeAreaProps {
  children: React.ReactNode;
  className?: string;
  top?: boolean;
  bottom?: boolean;
  left?: boolean;
  right?: boolean;
}

export function SafeArea({
  children,
  className,
  top = false,
  bottom = false,
  left = false,
  right = false,
}: SafeAreaProps) {
  return (
    <div
      className={cn(
        top && "pt-safe",
        bottom && "pb-safe",
        left && "pl-safe",
        right && "pr-safe",
        className
      )}
    >
      {children}
    </div>
  );
}

// globals.css에 추가할 유틸리티 클래스
/*
@supports (padding: max(0px)) {
  .pt-safe {
    padding-top: max(0px, env(safe-area-inset-top));
  }
  .pb-safe {
    padding-bottom: max(0px, env(safe-area-inset-bottom));
  }
  .pl-safe {
    padding-left: max(0px, env(safe-area-inset-left));
  }
  .pr-safe {
    padding-right: max(0px, env(safe-area-inset-right));
  }
  .min-h-screen-safe {
    min-height: calc(100vh - env(safe-area-inset-top) - env(safe-area-inset-bottom));
  }
}
*/
```

---

## iOS vs Android Considerations

### 플랫폼별 스타일 구분

```tsx
// lib/platform.ts
"use client";

import { useEffect, useState } from "react";

type Platform = "ios" | "android" | "other";

export function usePlatform(): Platform {
  const [platform, setPlatform] = useState<Platform>("other");

  useEffect(() => {
    const userAgent = navigator.userAgent.toLowerCase();

    if (/iphone|ipad|ipod/.test(userAgent)) {
      setPlatform("ios");
    } else if (/android/.test(userAgent)) {
      setPlatform("android");
    }
  }, []);

  return platform;
}

// 플랫폼별 컴포넌트
interface PlatformAwareProps {
  ios?: React.ReactNode;
  android?: React.ReactNode;
  fallback?: React.ReactNode;
}

export function PlatformAware({
  ios,
  android,
  fallback,
}: PlatformAwareProps) {
  const platform = usePlatform();

  if (platform === "ios" && ios) return <>{ios}</>;
  if (platform === "android" && android) return <>{android}</>;
  return <>{fallback || ios || android}</>;
}
```

### 플랫폼별 디자인 가이드

```markdown
## iOS vs Android 디자인 차이점

### 네비게이션
| 요소 | iOS | Android |
|------|-----|---------|
| 뒤로가기 | 왼쪽 상단 | 시스템 백 버튼 |
| 탭 바 | 하단 고정 | 하단 또는 상단 탭 |
| 햄버거 메뉴 | 거의 사용 안 함 | 일반적 |

### 버튼/액션
| 요소 | iOS | Android |
|------|-----|---------|
| 주요 버튼 | 전체 너비 또는 둥근 모서리 | FAB, Contained 버튼 |
| 취소 위치 | 왼쪽 | 오른쪽 또는 왼쪽 |
| 스와이프 액션 | 일반적 | 덜 일반적 |

### 시각적 스타일
| 요소 | iOS | Android |
|------|-----|---------|
| 모서리 반경 | 크게 (12-20px) | 보통 (4-8px) |
| 그림자 | 미묘한 그림자 | Elevation 시스템 |
| 블러 효과 | 일반적 | 덜 일반적 |
| 아이콘 스타일 | SF Symbols | Material Icons |

### 피드백
| 요소 | iOS | Android |
|------|-----|---------|
| 햅틱 | 세밀한 햅틱 | 기본 진동 |
| 로딩 | 스피너 | Progress indicator |
| 알림 | 배너 스타일 | Snackbar |
```

---

## PWA Patterns

### manifest.json 설정

```json
// public/manifest.json
{
  "name": "My App",
  "short_name": "MyApp",
  "description": "A Progressive Web App",
  "start_url": "/",
  "display": "standalone",
  "background_color": "#ffffff",
  "theme_color": "#6366f1",
  "orientation": "portrait-primary",
  "icons": [
    {
      "src": "/icons/icon-192.png",
      "sizes": "192x192",
      "type": "image/png",
      "purpose": "any maskable"
    },
    {
      "src": "/icons/icon-512.png",
      "sizes": "512x512",
      "type": "image/png",
      "purpose": "any maskable"
    }
  ],
  "screenshots": [
    {
      "src": "/screenshots/mobile.png",
      "sizes": "750x1334",
      "type": "image/png",
      "form_factor": "narrow"
    }
  ],
  "shortcuts": [
    {
      "name": "새 글 작성",
      "url": "/create",
      "icons": [{ "src": "/icons/create.png", "sizes": "96x96" }]
    }
  ]
}
```

### PWA 설치 프롬프트

```tsx
// components/mobile/pwa-install-prompt.tsx
"use client";

import { useEffect, useState } from "react";
import { Button } from "@/components/ui/button";
import { X, Download } from "lucide-react";

interface BeforeInstallPromptEvent extends Event {
  prompt: () => Promise<void>;
  userChoice: Promise<{ outcome: "accepted" | "dismissed" }>;
}

export function PWAInstallPrompt() {
  const [deferredPrompt, setDeferredPrompt] =
    useState<BeforeInstallPromptEvent | null>(null);
  const [showPrompt, setShowPrompt] = useState(false);

  useEffect(() => {
    const handler = (e: Event) => {
      e.preventDefault();
      setDeferredPrompt(e as BeforeInstallPromptEvent);
      setShowPrompt(true);
    };

    window.addEventListener("beforeinstallprompt", handler);

    return () => window.removeEventListener("beforeinstallprompt", handler);
  }, []);

  const handleInstall = async () => {
    if (!deferredPrompt) return;

    deferredPrompt.prompt();
    const { outcome } = await deferredPrompt.userChoice;

    if (outcome === "accepted") {
      setDeferredPrompt(null);
      setShowPrompt(false);
    }
  };

  if (!showPrompt) return null;

  return (
    <div className="fixed bottom-20 left-4 right-4 z-50 p-4 bg-card border border-border rounded-xl shadow-lg">
      <div className="flex items-start gap-4">
        <div className="flex-shrink-0 w-12 h-12 rounded-lg bg-primary/10 flex items-center justify-center">
          <Download className="h-6 w-6 text-primary" />
        </div>
        <div className="flex-1">
          <h3 className="font-semibold text-foreground">앱 설치</h3>
          <p className="text-sm text-muted-foreground mt-1">
            홈 화면에 추가하여 더 빠르게 접근하세요
          </p>
          <div className="flex gap-2 mt-3">
            <Button size="sm" onClick={handleInstall}>
              설치
            </Button>
            <Button
              size="sm"
              variant="ghost"
              onClick={() => setShowPrompt(false)}
            >
              나중에
            </Button>
          </div>
        </div>
        <button
          className="p-1 hover:bg-muted rounded"
          onClick={() => setShowPrompt(false)}
        >
          <X className="h-4 w-4 text-muted-foreground" />
        </button>
      </div>
    </div>
  );
}
```

---

## 접근성 요구사항

```markdown
## Mobile 접근성 체크리스트

### 터치 타겟
- [ ] 모든 인터랙티브 요소 최소 44x44px
- [ ] 인접 요소 간 충분한 간격 (8px+)
- [ ] 제스처에 대한 대체 수단 제공

### 시각적
- [ ] 대비율 4.5:1 이상
- [ ] 가로/세로 모드 모두 지원
- [ ] 텍스트 크기 조절 지원 (200%까지)

### 네비게이션
- [ ] 현재 위치 명확하게 표시
- [ ] 뒤로가기 항상 가능
- [ ] Focus 순서 논리적

### 폼
- [ ] 입력 필드 레이블 명확
- [ ] 에러 메시지 접근 가능
- [ ] 자동 완성 적절히 활용
- [ ] 키보드 타입 적절히 설정 (email, tel 등)

### 스크린 리더
- [ ] 모든 이미지에 alt 텍스트
- [ ] 버튼/링크 목적 명확
- [ ] 동적 콘텐츠 변경 알림 (aria-live)
```

---

## References

- `_references/COMPONENT-PATTERN.md`
- `7-motion/SKILL.md`
- `11-interactions/SKILL.md`
