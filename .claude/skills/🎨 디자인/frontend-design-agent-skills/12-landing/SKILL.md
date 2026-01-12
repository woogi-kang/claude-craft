# Landing Page Design Skill

랜딩 페이지 디자인 및 구성을 위한 종합 스킬입니다.

## Triggers

- "랜딩", "landing", "히어로", "hero", "LP", "랜딩페이지"

---

## Input

| 항목 | 필수 | 설명 |
|------|------|------|
| `pageType` | ✅ | 페이지 유형 (product, saas, portfolio, event) |
| `brand` | ✅ | 브랜드 정보 (colors, fonts) |
| `sections` | ❌ | 포함할 섹션 목록 |

---

## 랜딩 페이지 구조

```
┌─────────────────────────────────────────────────────────────┐
│  Navigation (sticky)                                        │
├─────────────────────────────────────────────────────────────┤
│  Hero Section (above the fold)                              │
│  - Headline + Subheadline                                   │
│  - CTA Button(s)                                            │
│  - Hero Image/Video                                         │
├─────────────────────────────────────────────────────────────┤
│  Social Proof (logos, trust badges)                         │
├─────────────────────────────────────────────────────────────┤
│  Features Section                                           │
├─────────────────────────────────────────────────────────────┤
│  Benefits / How It Works                                    │
├─────────────────────────────────────────────────────────────┤
│  Testimonials                                               │
├─────────────────────────────────────────────────────────────┤
│  Pricing                                                    │
├─────────────────────────────────────────────────────────────┤
│  FAQ                                                        │
├─────────────────────────────────────────────────────────────┤
│  Final CTA                                                  │
├─────────────────────────────────────────────────────────────┤
│  Footer                                                     │
└─────────────────────────────────────────────────────────────┘
```

---

## Hero Section Patterns

### 1. Centered Hero (가장 일반적)

```tsx
// components/sections/hero-centered.tsx
'use client';

import { Button } from "@/components/ui/button";
import { motion } from "framer-motion";

interface HeroCenteredProps {
  headline: string;
  subheadline: string;
  primaryCta: { label: string; href: string };
  secondaryCta?: { label: string; href: string };
  trustedBy?: string[];
}

export function HeroCentered({
  headline,
  subheadline,
  primaryCta,
  secondaryCta,
  trustedBy,
}: HeroCenteredProps) {
  return (
    <section className="relative min-h-[90vh] flex items-center justify-center overflow-hidden">
      {/* Background Gradient */}
      <div className="absolute inset-0 bg-gradient-to-b from-primary/5 via-background to-background" />

      {/* Grid Pattern (optional) */}
      <div
        className="absolute inset-0 bg-[linear-gradient(to_right,#8882_1px,transparent_1px),linear-gradient(to_bottom,#8882_1px,transparent_1px)] bg-[size:14px_24px]"
        aria-hidden="true"
      />

      <div className="relative z-10 container mx-auto px-4 text-center">
        {/* Badge (optional) */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5 }}
        >
          <span className="inline-flex items-center gap-2 px-3 py-1 text-sm font-medium bg-primary/10 text-primary rounded-full mb-6">
            <span className="relative flex h-2 w-2">
              <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-primary opacity-75" />
              <span className="relative inline-flex rounded-full h-2 w-2 bg-primary" />
            </span>
            새로운 기능 출시
          </span>
        </motion.div>

        {/* Headline */}
        <motion.h1
          className="text-4xl md:text-5xl lg:text-6xl xl:text-7xl font-bold tracking-tight text-foreground max-w-4xl mx-auto"
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5, delay: 0.1 }}
        >
          {headline.split(" ").map((word, i) => (
            <span
              key={i}
              className={word === "강조단어" ? "text-primary" : ""}
            >
              {word}{" "}
            </span>
          ))}
        </motion.h1>

        {/* Subheadline */}
        <motion.p
          className="mt-6 text-lg md:text-xl text-muted-foreground max-w-2xl mx-auto leading-relaxed"
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5, delay: 0.2 }}
        >
          {subheadline}
        </motion.p>

        {/* CTA Buttons */}
        <motion.div
          className="mt-10 flex flex-col sm:flex-row items-center justify-center gap-4"
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5, delay: 0.3 }}
        >
          <Button size="lg" className="min-w-[180px] h-12 text-base" asChild>
            <a href={primaryCta.href}>{primaryCta.label}</a>
          </Button>
          {secondaryCta && (
            <Button
              size="lg"
              variant="outline"
              className="min-w-[180px] h-12 text-base"
              asChild
            >
              <a href={secondaryCta.href}>{secondaryCta.label}</a>
            </Button>
          )}
        </motion.div>

        {/* Trusted By */}
        {trustedBy && (
          <motion.div
            className="mt-16"
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ duration: 0.5, delay: 0.5 }}
          >
            <p className="text-sm text-muted-foreground mb-6">
              1,000+ 기업이 신뢰합니다
            </p>
            <div className="flex flex-wrap items-center justify-center gap-8 opacity-60 grayscale hover:opacity-100 hover:grayscale-0 transition-all duration-300">
              {trustedBy.map((logo, i) => (
                <img
                  key={i}
                  src={logo}
                  alt="Partner logo"
                  className="h-8 md:h-10 object-contain"
                />
              ))}
            </div>
          </motion.div>
        )}
      </div>
    </section>
  );
}
```

### 2. Split Hero (이미지/영상 + 텍스트)

```tsx
// components/sections/hero-split.tsx
'use client';

import { Button } from "@/components/ui/button";
import { motion } from "framer-motion";
import { PlayCircle } from "lucide-react";

interface HeroSplitProps {
  headline: string;
  subheadline: string;
  primaryCta: { label: string; href: string };
  secondaryCta?: { label: string; href: string; icon?: boolean };
  media: {
    type: "image" | "video";
    src: string;
    alt?: string;
  };
  reverse?: boolean; // 이미지 좌우 반전
}

export function HeroSplit({
  headline,
  subheadline,
  primaryCta,
  secondaryCta,
  media,
  reverse = false,
}: HeroSplitProps) {
  return (
    <section className="relative py-20 lg:py-32 overflow-hidden">
      <div className="container mx-auto px-4">
        <div className={`grid lg:grid-cols-2 gap-12 lg:gap-20 items-center ${reverse ? "lg:flex-row-reverse" : ""}`}>
          {/* Text Content */}
          <motion.div
            className={`${reverse ? "lg:order-2" : ""}`}
            initial={{ opacity: 0, x: reverse ? 50 : -50 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ duration: 0.6 }}
          >
            <h1 className="text-4xl md:text-5xl lg:text-6xl font-bold tracking-tight text-foreground">
              {headline}
            </h1>
            <p className="mt-6 text-lg text-muted-foreground leading-relaxed">
              {subheadline}
            </p>

            <div className="mt-10 flex flex-wrap gap-4">
              <Button size="lg" asChild>
                <a href={primaryCta.href}>{primaryCta.label}</a>
              </Button>
              {secondaryCta && (
                <Button size="lg" variant="ghost" className="gap-2" asChild>
                  <a href={secondaryCta.href}>
                    {secondaryCta.icon && <PlayCircle className="h-5 w-5" />}
                    {secondaryCta.label}
                  </a>
                </Button>
              )}
            </div>

            {/* Stats Row */}
            <div className="mt-12 grid grid-cols-3 gap-8">
              {[
                { value: "10K+", label: "활성 사용자" },
                { value: "99.9%", label: "가동률" },
                { value: "24/7", label: "고객 지원" },
              ].map((stat, i) => (
                <div key={i}>
                  <div className="text-2xl md:text-3xl font-bold text-foreground">
                    {stat.value}
                  </div>
                  <div className="text-sm text-muted-foreground mt-1">
                    {stat.label}
                  </div>
                </div>
              ))}
            </div>
          </motion.div>

          {/* Media */}
          <motion.div
            className={`relative ${reverse ? "lg:order-1" : ""}`}
            initial={{ opacity: 0, x: reverse ? -50 : 50 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ duration: 0.6, delay: 0.2 }}
          >
            {/* Decorative Elements */}
            <div className="absolute -inset-4 bg-gradient-to-r from-primary/20 to-secondary/20 rounded-3xl blur-3xl opacity-30" />

            <div className="relative rounded-2xl overflow-hidden shadow-2xl border border-border/50">
              {media.type === "video" ? (
                <video
                  src={media.src}
                  autoPlay
                  loop
                  muted
                  playsInline
                  className="w-full aspect-[4/3] object-cover"
                />
              ) : (
                <img
                  src={media.src}
                  alt={media.alt || "Hero image"}
                  className="w-full aspect-[4/3] object-cover"
                />
              )}
            </div>

            {/* Floating Badge */}
            <motion.div
              className="absolute -bottom-6 -left-6 bg-background border border-border rounded-xl p-4 shadow-lg"
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.5, delay: 0.5 }}
            >
              <div className="flex items-center gap-3">
                <div className="flex -space-x-2">
                  {[1, 2, 3].map((i) => (
                    <div
                      key={i}
                      className="w-8 h-8 rounded-full bg-gradient-to-br from-primary to-secondary border-2 border-background"
                    />
                  ))}
                </div>
                <div className="text-sm">
                  <div className="font-semibold">+500명</div>
                  <div className="text-muted-foreground">이번 주 가입</div>
                </div>
              </div>
            </motion.div>
          </motion.div>
        </div>
      </div>
    </section>
  );
}
```

### 3. Full-Bleed Hero (전체 배경 이미지/영상)

```tsx
// components/sections/hero-fullbleed.tsx
'use client';

import { Button } from "@/components/ui/button";
import { motion } from "framer-motion";
import { ChevronDown } from "lucide-react";

interface HeroFullBleedProps {
  headline: string;
  subheadline: string;
  primaryCta: { label: string; href: string };
  backgroundMedia: {
    type: "image" | "video";
    src: string;
    poster?: string; // video poster
  };
  overlay?: "dark" | "light" | "gradient";
}

export function HeroFullBleed({
  headline,
  subheadline,
  primaryCta,
  backgroundMedia,
  overlay = "dark",
}: HeroFullBleedProps) {
  const overlayStyles = {
    dark: "bg-black/60",
    light: "bg-white/60",
    gradient: "bg-gradient-to-t from-black/80 via-black/40 to-transparent",
  };

  return (
    <section className="relative h-screen min-h-[600px] flex items-center justify-center overflow-hidden">
      {/* Background Media */}
      {backgroundMedia.type === "video" ? (
        <video
          src={backgroundMedia.src}
          poster={backgroundMedia.poster}
          autoPlay
          loop
          muted
          playsInline
          className="absolute inset-0 w-full h-full object-cover"
        />
      ) : (
        <img
          src={backgroundMedia.src}
          alt=""
          className="absolute inset-0 w-full h-full object-cover"
        />
      )}

      {/* Overlay */}
      <div className={`absolute inset-0 ${overlayStyles[overlay]}`} />

      {/* Content */}
      <div className="relative z-10 container mx-auto px-4 text-center text-white">
        <motion.h1
          className="text-4xl md:text-6xl lg:text-7xl font-bold tracking-tight max-w-4xl mx-auto"
          initial={{ opacity: 0, y: 30 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.7 }}
        >
          {headline}
        </motion.h1>

        <motion.p
          className="mt-6 text-lg md:text-xl text-white/80 max-w-2xl mx-auto"
          initial={{ opacity: 0, y: 30 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.7, delay: 0.2 }}
        >
          {subheadline}
        </motion.p>

        <motion.div
          initial={{ opacity: 0, y: 30 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.7, delay: 0.4 }}
        >
          <Button
            size="lg"
            className="mt-10 min-w-[200px] h-14 text-lg"
            asChild
          >
            <a href={primaryCta.href}>{primaryCta.label}</a>
          </Button>
        </motion.div>
      </div>

      {/* Scroll Indicator */}
      <motion.div
        className="absolute bottom-10 left-1/2 -translate-x-1/2 text-white/60"
        initial={{ opacity: 0 }}
        animate={{ opacity: 1, y: [0, 10, 0] }}
        transition={{
          opacity: { delay: 1, duration: 0.5 },
          y: { delay: 1, duration: 1.5, repeat: Infinity }
        }}
      >
        <ChevronDown className="h-8 w-8" />
      </motion.div>
    </section>
  );
}
```

---

## Above-the-Fold Optimization

### 체크리스트

```markdown
## Above-the-Fold 최적화 체크리스트

### 콘텐츠 우선순위
- [ ] 핵심 가치 제안 (Value Proposition) 1초 내 인식 가능
- [ ] 주요 CTA 버튼 즉시 보임
- [ ] 신뢰 요소 (로고, 평점) 포함

### 성능 최적화
- [ ] Hero 이미지 LCP (Largest Contentful Paint) 2.5초 이하
- [ ] Critical CSS 인라인 처리
- [ ] 이미지 preload (priority)
- [ ] 폰트 preconnect

### 반응형 고려
- [ ] 모바일: 핵심 정보만 (간결한 헤드라인)
- [ ] 태블릿: 이미지 비율 조정
- [ ] 데스크톱: 풍부한 시각 요소

### 접근성
- [ ] 대비율 4.5:1 이상 (텍스트)
- [ ] CTA 버튼 터치 타겟 44px 이상
- [ ] 스크린 리더 읽기 순서 논리적
```

### LCP 최적화 코드

```tsx
// app/page.tsx
import Image from "next/image";

export default function HomePage() {
  return (
    <section>
      {/* LCP 이미지 - priority 설정 */}
      <Image
        src="/hero-image.webp"
        alt="Hero"
        width={1200}
        height={600}
        priority // preload
        quality={85}
        sizes="100vw"
        className="w-full h-auto"
      />
    </section>
  );
}
```

```tsx
// app/layout.tsx - 폰트 프리로드
import { DM_Sans } from "next/font/google";

const dmSans = DM_Sans({
  subsets: ["latin"],
  display: "swap", // FOUT 허용
  preload: true,
});
```

---

## CTA Button Design

### 버튼 배치 원칙

```
┌────────────────────────────────────────────────────────────┐
│                                                            │
│     Primary CTA: 왼쪽 또는 위 (시선 흐름)                  │
│     Secondary CTA: 오른쪽 또는 아래                        │
│                                                            │
│     [ 무료 시작하기 ]    [ 데모 보기 → ]                  │
│          Primary             Secondary                     │
│                                                            │
└────────────────────────────────────────────────────────────┘
```

### CTA 버튼 컴포넌트

```tsx
// components/cta-button.tsx
import { Button } from "@/components/ui/button";
import { ArrowRight, Sparkles } from "lucide-react";
import { cn } from "@/lib/utils";

interface CTAButtonProps {
  children: React.ReactNode;
  href: string;
  variant?: "primary" | "secondary" | "gradient";
  size?: "default" | "lg" | "xl";
  showArrow?: boolean;
  showSparkle?: boolean;
  className?: string;
}

export function CTAButton({
  children,
  href,
  variant = "primary",
  size = "lg",
  showArrow = false,
  showSparkle = false,
  className,
}: CTAButtonProps) {
  const sizeClasses = {
    default: "h-10 px-6 text-sm",
    lg: "h-12 px-8 text-base",
    xl: "h-14 px-10 text-lg",
  };

  if (variant === "gradient") {
    return (
      <a
        href={href}
        className={cn(
          "group relative inline-flex items-center justify-center gap-2 font-medium text-white rounded-lg overflow-hidden transition-all hover:scale-105",
          sizeClasses[size],
          className
        )}
      >
        {/* Gradient Background */}
        <span className="absolute inset-0 bg-gradient-to-r from-primary via-purple-500 to-pink-500" />

        {/* Animated Gradient Overlay */}
        <span className="absolute inset-0 bg-gradient-to-r from-primary via-purple-500 to-pink-500 opacity-0 group-hover:opacity-100 blur-xl transition-opacity" />

        {/* Content */}
        <span className="relative flex items-center gap-2">
          {showSparkle && <Sparkles className="h-4 w-4" />}
          {children}
          {showArrow && (
            <ArrowRight className="h-4 w-4 transition-transform group-hover:translate-x-1" />
          )}
        </span>
      </a>
    );
  }

  return (
    <Button
      size={size === "xl" ? "lg" : size}
      variant={variant === "secondary" ? "outline" : "default"}
      className={cn(
        sizeClasses[size],
        "group",
        className
      )}
      asChild
    >
      <a href={href}>
        {showSparkle && <Sparkles className="h-4 w-4 mr-2" />}
        {children}
        {showArrow && (
          <ArrowRight className="h-4 w-4 ml-2 transition-transform group-hover:translate-x-1" />
        )}
      </a>
    </Button>
  );
}
```

---

## Feature Sections

### 1. Grid Layout (3-4열)

```tsx
// components/sections/features-grid.tsx
'use client';

import { motion } from "framer-motion";
import { LucideIcon } from "lucide-react";

interface Feature {
  icon: LucideIcon;
  title: string;
  description: string;
}

interface FeaturesGridProps {
  headline: string;
  subheadline?: string;
  features: Feature[];
  columns?: 2 | 3 | 4;
}

export function FeaturesGrid({
  headline,
  subheadline,
  features,
  columns = 3,
}: FeaturesGridProps) {
  const columnClasses = {
    2: "md:grid-cols-2",
    3: "md:grid-cols-2 lg:grid-cols-3",
    4: "md:grid-cols-2 lg:grid-cols-4",
  };

  return (
    <section className="py-20 lg:py-32">
      <div className="container mx-auto px-4">
        {/* Section Header */}
        <motion.div
          className="text-center max-w-3xl mx-auto mb-16"
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
        >
          <h2 className="text-3xl md:text-4xl lg:text-5xl font-bold text-foreground">
            {headline}
          </h2>
          {subheadline && (
            <p className="mt-4 text-lg text-muted-foreground">
              {subheadline}
            </p>
          )}
        </motion.div>

        {/* Features Grid */}
        <div className={`grid gap-8 ${columnClasses[columns]}`}>
          {features.map((feature, index) => (
            <motion.div
              key={index}
              className="group relative p-6 rounded-2xl border border-border bg-card hover:border-primary/50 hover:shadow-lg transition-all duration-300"
              initial={{ opacity: 0, y: 20 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              transition={{ delay: index * 0.1 }}
            >
              {/* Icon */}
              <div className="w-12 h-12 rounded-xl bg-primary/10 flex items-center justify-center mb-4 group-hover:bg-primary/20 transition-colors">
                <feature.icon className="h-6 w-6 text-primary" />
              </div>

              {/* Content */}
              <h3 className="text-xl font-semibold text-foreground mb-2">
                {feature.title}
              </h3>
              <p className="text-muted-foreground leading-relaxed">
                {feature.description}
              </p>

              {/* Hover Gradient */}
              <div className="absolute inset-0 rounded-2xl bg-gradient-to-br from-primary/5 to-transparent opacity-0 group-hover:opacity-100 transition-opacity" />
            </motion.div>
          ))}
        </div>
      </div>
    </section>
  );
}
```

### 2. Bento Grid Layout

```tsx
// components/sections/features-bento.tsx
'use client';

import { motion } from "framer-motion";
import { cn } from "@/lib/utils";

interface BentoItem {
  title: string;
  description: string;
  image?: string;
  className?: string; // 크기 조절용 (col-span-2, row-span-2)
  gradient?: string;
}

interface FeaturesBentoProps {
  headline: string;
  subheadline?: string;
  items: BentoItem[];
}

export function FeaturesBento({
  headline,
  subheadline,
  items,
}: FeaturesBentoProps) {
  return (
    <section className="py-20 lg:py-32 bg-muted/30">
      <div className="container mx-auto px-4">
        {/* Section Header */}
        <motion.div
          className="text-center max-w-3xl mx-auto mb-16"
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
        >
          <h2 className="text-3xl md:text-4xl lg:text-5xl font-bold text-foreground">
            {headline}
          </h2>
          {subheadline && (
            <p className="mt-4 text-lg text-muted-foreground">
              {subheadline}
            </p>
          )}
        </motion.div>

        {/* Bento Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4 lg:gap-6 auto-rows-[200px] lg:auto-rows-[240px]">
          {items.map((item, index) => (
            <motion.div
              key={index}
              className={cn(
                "group relative rounded-3xl overflow-hidden bg-card border border-border p-6 flex flex-col justify-end",
                item.className
              )}
              initial={{ opacity: 0, scale: 0.95 }}
              whileInView={{ opacity: 1, scale: 1 }}
              viewport={{ once: true }}
              transition={{ delay: index * 0.1 }}
            >
              {/* Background Gradient */}
              {item.gradient && (
                <div
                  className={cn(
                    "absolute inset-0 opacity-50 group-hover:opacity-70 transition-opacity",
                    item.gradient
                  )}
                />
              )}

              {/* Background Image */}
              {item.image && (
                <div className="absolute inset-0">
                  <img
                    src={item.image}
                    alt=""
                    className="w-full h-full object-cover opacity-20 group-hover:opacity-30 group-hover:scale-105 transition-all duration-500"
                  />
                </div>
              )}

              {/* Content */}
              <div className="relative z-10">
                <h3 className="text-xl lg:text-2xl font-semibold text-foreground mb-2">
                  {item.title}
                </h3>
                <p className="text-muted-foreground text-sm lg:text-base">
                  {item.description}
                </p>
              </div>
            </motion.div>
          ))}
        </div>
      </div>
    </section>
  );
}

// 사용 예시
const bentoItems: BentoItem[] = [
  {
    title: "실시간 협업",
    description: "팀원들과 동시에 작업하세요",
    className: "lg:col-span-2 lg:row-span-2",
    gradient: "bg-gradient-to-br from-blue-500/20 to-purple-500/20",
  },
  {
    title: "AI 자동화",
    description: "반복 작업을 자동화합니다",
    gradient: "bg-gradient-to-br from-green-500/20 to-emerald-500/20",
  },
  {
    title: "보안 우선",
    description: "엔터프라이즈급 보안",
    gradient: "bg-gradient-to-br from-orange-500/20 to-red-500/20",
  },
  {
    title: "무제한 스토리지",
    description: "용량 걱정 없이 사용하세요",
    className: "md:col-span-2 lg:col-span-1",
    gradient: "bg-gradient-to-br from-pink-500/20 to-rose-500/20",
  },
];
```

### 3. Alternating Layout (좌우 교대)

```tsx
// components/sections/features-alternating.tsx
'use client';

import { motion } from "framer-motion";
import Image from "next/image";

interface AlternatingFeature {
  title: string;
  description: string;
  image: string;
  bullets?: string[];
}

interface FeaturesAlternatingProps {
  features: AlternatingFeature[];
}

export function FeaturesAlternating({ features }: FeaturesAlternatingProps) {
  return (
    <section className="py-20 lg:py-32">
      <div className="container mx-auto px-4 space-y-24 lg:space-y-32">
        {features.map((feature, index) => (
          <motion.div
            key={index}
            className={`grid lg:grid-cols-2 gap-12 lg:gap-20 items-center ${
              index % 2 === 1 ? "lg:flex-row-reverse" : ""
            }`}
            initial={{ opacity: 0, y: 40 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true, margin: "-100px" }}
          >
            {/* Image */}
            <div className={index % 2 === 1 ? "lg:order-2" : ""}>
              <div className="relative rounded-2xl overflow-hidden shadow-2xl">
                <Image
                  src={feature.image}
                  alt={feature.title}
                  width={600}
                  height={400}
                  className="w-full aspect-[3/2] object-cover"
                />
              </div>
            </div>

            {/* Content */}
            <div className={index % 2 === 1 ? "lg:order-1" : ""}>
              <h3 className="text-3xl lg:text-4xl font-bold text-foreground">
                {feature.title}
              </h3>
              <p className="mt-4 text-lg text-muted-foreground leading-relaxed">
                {feature.description}
              </p>

              {feature.bullets && (
                <ul className="mt-6 space-y-3">
                  {feature.bullets.map((bullet, i) => (
                    <li key={i} className="flex items-start gap-3">
                      <svg
                        className="h-6 w-6 text-primary flex-shrink-0 mt-0.5"
                        fill="none"
                        viewBox="0 0 24 24"
                        stroke="currentColor"
                      >
                        <path
                          strokeLinecap="round"
                          strokeLinejoin="round"
                          strokeWidth={2}
                          d="M5 13l4 4L19 7"
                        />
                      </svg>
                      <span className="text-foreground">{bullet}</span>
                    </li>
                  ))}
                </ul>
              )}
            </div>
          </motion.div>
        ))}
      </div>
    </section>
  );
}
```

---

## Social Proof Sections

### 1. Logo Cloud

```tsx
// components/sections/logo-cloud.tsx
'use client';

import { motion } from "framer-motion";

interface LogoCloudProps {
  title?: string;
  logos: { src: string; alt: string }[];
  animated?: boolean;
}

export function LogoCloud({
  title = "신뢰받는 파트너사",
  logos,
  animated = false,
}: LogoCloudProps) {
  if (animated) {
    return (
      <section className="py-12 overflow-hidden">
        <div className="container mx-auto px-4">
          <p className="text-center text-sm text-muted-foreground mb-8">
            {title}
          </p>
        </div>

        {/* Infinite Scroll Animation */}
        <div className="relative">
          <div className="flex animate-scroll">
            {[...logos, ...logos].map((logo, i) => (
              <div
                key={i}
                className="flex-shrink-0 mx-8 grayscale hover:grayscale-0 opacity-60 hover:opacity-100 transition-all"
              >
                <img
                  src={logo.src}
                  alt={logo.alt}
                  className="h-8 md:h-10 w-auto object-contain"
                />
              </div>
            ))}
          </div>
        </div>

        <style jsx>{`
          @keyframes scroll {
            0% { transform: translateX(0); }
            100% { transform: translateX(-50%); }
          }
          .animate-scroll {
            animation: scroll 30s linear infinite;
          }
        `}</style>
      </section>
    );
  }

  return (
    <section className="py-12 bg-muted/30">
      <div className="container mx-auto px-4">
        <p className="text-center text-sm text-muted-foreground mb-8">
          {title}
        </p>
        <div className="flex flex-wrap items-center justify-center gap-8 md:gap-12">
          {logos.map((logo, i) => (
            <motion.div
              key={i}
              className="grayscale hover:grayscale-0 opacity-60 hover:opacity-100 transition-all"
              initial={{ opacity: 0 }}
              whileInView={{ opacity: 0.6 }}
              whileHover={{ opacity: 1 }}
              viewport={{ once: true }}
            >
              <img
                src={logo.src}
                alt={logo.alt}
                className="h-8 md:h-10 w-auto object-contain"
              />
            </motion.div>
          ))}
        </div>
      </div>
    </section>
  );
}
```

### 2. Testimonials

```tsx
// components/sections/testimonials.tsx
'use client';

import { motion } from "framer-motion";
import { Star, Quote } from "lucide-react";

interface Testimonial {
  quote: string;
  author: string;
  role: string;
  company: string;
  avatar?: string;
  rating?: number;
}

interface TestimonialsProps {
  headline: string;
  testimonials: Testimonial[];
  layout?: "grid" | "carousel";
}

export function Testimonials({
  headline,
  testimonials,
  layout = "grid",
}: TestimonialsProps) {
  return (
    <section className="py-20 lg:py-32 bg-muted/30">
      <div className="container mx-auto px-4">
        {/* Header */}
        <motion.div
          className="text-center max-w-3xl mx-auto mb-16"
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
        >
          <h2 className="text-3xl md:text-4xl lg:text-5xl font-bold text-foreground">
            {headline}
          </h2>
        </motion.div>

        {/* Grid Layout */}
        <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
          {testimonials.map((testimonial, index) => (
            <motion.div
              key={index}
              className="relative p-6 lg:p-8 rounded-2xl bg-card border border-border"
              initial={{ opacity: 0, y: 20 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              transition={{ delay: index * 0.1 }}
            >
              {/* Quote Icon */}
              <Quote className="absolute top-6 right-6 h-8 w-8 text-primary/20" />

              {/* Rating */}
              {testimonial.rating && (
                <div className="flex gap-1 mb-4">
                  {Array.from({ length: 5 }).map((_, i) => (
                    <Star
                      key={i}
                      className={`h-4 w-4 ${
                        i < testimonial.rating!
                          ? "text-yellow-400 fill-yellow-400"
                          : "text-gray-300"
                      }`}
                    />
                  ))}
                </div>
              )}

              {/* Quote */}
              <p className="text-foreground leading-relaxed mb-6">
                "{testimonial.quote}"
              </p>

              {/* Author */}
              <div className="flex items-center gap-4">
                {testimonial.avatar ? (
                  <img
                    src={testimonial.avatar}
                    alt={testimonial.author}
                    className="w-12 h-12 rounded-full object-cover"
                  />
                ) : (
                  <div className="w-12 h-12 rounded-full bg-gradient-to-br from-primary to-primary/60 flex items-center justify-center text-white font-semibold">
                    {testimonial.author[0]}
                  </div>
                )}
                <div>
                  <div className="font-semibold text-foreground">
                    {testimonial.author}
                  </div>
                  <div className="text-sm text-muted-foreground">
                    {testimonial.role}, {testimonial.company}
                  </div>
                </div>
              </div>
            </motion.div>
          ))}
        </div>
      </div>
    </section>
  );
}
```

---

## Pricing Section

```tsx
// components/sections/pricing.tsx
'use client';

import { useState } from "react";
import { motion } from "framer-motion";
import { Button } from "@/components/ui/button";
import { Check } from "lucide-react";
import { cn } from "@/lib/utils";

interface PricingPlan {
  name: string;
  description: string;
  price: { monthly: number; yearly: number };
  features: string[];
  cta: string;
  popular?: boolean;
}

interface PricingProps {
  headline: string;
  subheadline?: string;
  plans: PricingPlan[];
}

export function Pricing({ headline, subheadline, plans }: PricingProps) {
  const [isYearly, setIsYearly] = useState(false);

  return (
    <section className="py-20 lg:py-32">
      <div className="container mx-auto px-4">
        {/* Header */}
        <motion.div
          className="text-center max-w-3xl mx-auto mb-12"
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
        >
          <h2 className="text-3xl md:text-4xl lg:text-5xl font-bold text-foreground">
            {headline}
          </h2>
          {subheadline && (
            <p className="mt-4 text-lg text-muted-foreground">
              {subheadline}
            </p>
          )}
        </motion.div>

        {/* Billing Toggle */}
        <div className="flex items-center justify-center gap-4 mb-12">
          <span className={cn("text-sm", !isYearly && "text-foreground font-medium")}>
            월간
          </span>
          <button
            onClick={() => setIsYearly(!isYearly)}
            className={cn(
              "relative w-14 h-7 rounded-full transition-colors",
              isYearly ? "bg-primary" : "bg-muted"
            )}
          >
            <span
              className={cn(
                "absolute top-1 left-1 w-5 h-5 rounded-full bg-white transition-transform",
                isYearly && "translate-x-7"
              )}
            />
          </button>
          <span className={cn("text-sm", isYearly && "text-foreground font-medium")}>
            연간
            <span className="ml-1.5 text-xs text-primary font-medium">
              20% 할인
            </span>
          </span>
        </div>

        {/* Pricing Cards */}
        <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-8 max-w-5xl mx-auto">
          {plans.map((plan, index) => (
            <motion.div
              key={index}
              className={cn(
                "relative rounded-2xl border p-8",
                plan.popular
                  ? "border-primary bg-primary/5 shadow-lg scale-105"
                  : "border-border bg-card"
              )}
              initial={{ opacity: 0, y: 20 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              transition={{ delay: index * 0.1 }}
            >
              {/* Popular Badge */}
              {plan.popular && (
                <div className="absolute -top-4 left-1/2 -translate-x-1/2">
                  <span className="bg-primary text-primary-foreground text-sm font-medium px-4 py-1 rounded-full">
                    인기
                  </span>
                </div>
              )}

              {/* Plan Info */}
              <div className="text-center mb-8">
                <h3 className="text-xl font-semibold text-foreground">
                  {plan.name}
                </h3>
                <p className="mt-2 text-sm text-muted-foreground">
                  {plan.description}
                </p>
                <div className="mt-6">
                  <span className="text-4xl font-bold text-foreground">
                    ₩{(isYearly ? plan.price.yearly : plan.price.monthly).toLocaleString()}
                  </span>
                  <span className="text-muted-foreground">/월</span>
                </div>
              </div>

              {/* Features */}
              <ul className="space-y-3 mb-8">
                {plan.features.map((feature, i) => (
                  <li key={i} className="flex items-start gap-3">
                    <Check className="h-5 w-5 text-primary flex-shrink-0 mt-0.5" />
                    <span className="text-sm text-foreground">{feature}</span>
                  </li>
                ))}
              </ul>

              {/* CTA */}
              <Button
                className="w-full"
                variant={plan.popular ? "default" : "outline"}
              >
                {plan.cta}
              </Button>
            </motion.div>
          ))}
        </div>
      </div>
    </section>
  );
}
```

---

## FAQ Section

```tsx
// components/sections/faq.tsx
'use client';

import { motion } from "framer-motion";
import {
  Accordion,
  AccordionContent,
  AccordionItem,
  AccordionTrigger,
} from "@/components/ui/accordion";

interface FAQItem {
  question: string;
  answer: string;
}

interface FAQProps {
  headline: string;
  subheadline?: string;
  items: FAQItem[];
  columns?: 1 | 2;
}

export function FAQ({ headline, subheadline, items, columns = 1 }: FAQProps) {
  return (
    <section className="py-20 lg:py-32">
      <div className="container mx-auto px-4">
        {/* Header */}
        <motion.div
          className="text-center max-w-3xl mx-auto mb-16"
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
        >
          <h2 className="text-3xl md:text-4xl lg:text-5xl font-bold text-foreground">
            {headline}
          </h2>
          {subheadline && (
            <p className="mt-4 text-lg text-muted-foreground">
              {subheadline}
            </p>
          )}
        </motion.div>

        {/* FAQ Items */}
        {columns === 2 ? (
          <div className="grid md:grid-cols-2 gap-6 max-w-4xl mx-auto">
            {items.map((item, index) => (
              <motion.div
                key={index}
                initial={{ opacity: 0, y: 20 }}
                whileInView={{ opacity: 1, y: 0 }}
                viewport={{ once: true }}
                transition={{ delay: index * 0.05 }}
              >
                <Accordion type="single" collapsible>
                  <AccordionItem value={`item-${index}`} className="border rounded-lg px-4">
                    <AccordionTrigger className="text-left hover:no-underline">
                      {item.question}
                    </AccordionTrigger>
                    <AccordionContent className="text-muted-foreground">
                      {item.answer}
                    </AccordionContent>
                  </AccordionItem>
                </Accordion>
              </motion.div>
            ))}
          </div>
        ) : (
          <div className="max-w-3xl mx-auto">
            <Accordion type="single" collapsible className="space-y-4">
              {items.map((item, index) => (
                <motion.div
                  key={index}
                  initial={{ opacity: 0, y: 20 }}
                  whileInView={{ opacity: 1, y: 0 }}
                  viewport={{ once: true }}
                  transition={{ delay: index * 0.05 }}
                >
                  <AccordionItem
                    value={`item-${index}`}
                    className="border rounded-lg px-6 data-[state=open]:bg-muted/50"
                  >
                    <AccordionTrigger className="text-left hover:no-underline py-5">
                      {item.question}
                    </AccordionTrigger>
                    <AccordionContent className="text-muted-foreground pb-5">
                      {item.answer}
                    </AccordionContent>
                  </AccordionItem>
                </motion.div>
              ))}
            </Accordion>
          </div>
        )}
      </div>
    </section>
  );
}
```

---

## Footer Pattern

```tsx
// components/sections/footer.tsx
import Link from "next/link";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import {
  Twitter,
  Github,
  Linkedin,
  Instagram,
  Mail
} from "lucide-react";

interface FooterLink {
  label: string;
  href: string;
}

interface FooterColumn {
  title: string;
  links: FooterLink[];
}

interface FooterProps {
  logo: React.ReactNode;
  description: string;
  columns: FooterColumn[];
  newsletter?: boolean;
  social?: { platform: string; href: string }[];
}

export function Footer({
  logo,
  description,
  columns,
  newsletter = true,
  social,
}: FooterProps) {
  const socialIcons: Record<string, React.ComponentType<{ className?: string }>> = {
    twitter: Twitter,
    github: Github,
    linkedin: Linkedin,
    instagram: Instagram,
  };

  return (
    <footer className="border-t border-border bg-muted/30">
      <div className="container mx-auto px-4 py-12 lg:py-16">
        <div className="grid gap-8 lg:grid-cols-2">
          {/* Left: Logo & Description */}
          <div className="lg:pr-16">
            {/* Logo */}
            <div className="mb-4">{logo}</div>

            {/* Description */}
            <p className="text-muted-foreground max-w-md mb-6">
              {description}
            </p>

            {/* Newsletter */}
            {newsletter && (
              <div className="max-w-md">
                <p className="text-sm font-medium text-foreground mb-3">
                  뉴스레터 구독
                </p>
                <form className="flex gap-2">
                  <Input
                    type="email"
                    placeholder="이메일 주소"
                    className="flex-1"
                  />
                  <Button type="submit">
                    <Mail className="h-4 w-4 mr-2" />
                    구독
                  </Button>
                </form>
              </div>
            )}
          </div>

          {/* Right: Link Columns */}
          <div className="grid grid-cols-2 md:grid-cols-3 gap-8">
            {columns.map((column, index) => (
              <div key={index}>
                <h4 className="text-sm font-semibold text-foreground mb-4">
                  {column.title}
                </h4>
                <ul className="space-y-3">
                  {column.links.map((link, linkIndex) => (
                    <li key={linkIndex}>
                      <Link
                        href={link.href}
                        className="text-sm text-muted-foreground hover:text-foreground transition-colors"
                      >
                        {link.label}
                      </Link>
                    </li>
                  ))}
                </ul>
              </div>
            ))}
          </div>
        </div>

        {/* Bottom Bar */}
        <div className="mt-12 pt-8 border-t border-border flex flex-col md:flex-row items-center justify-between gap-4">
          {/* Copyright */}
          <p className="text-sm text-muted-foreground">
            &copy; {new Date().getFullYear()} 회사명. All rights reserved.
          </p>

          {/* Social Links */}
          {social && (
            <div className="flex items-center gap-4">
              {social.map((item, index) => {
                const Icon = socialIcons[item.platform.toLowerCase()];
                return Icon ? (
                  <a
                    key={index}
                    href={item.href}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="text-muted-foreground hover:text-foreground transition-colors"
                  >
                    <Icon className="h-5 w-5" />
                  </a>
                ) : null;
              })}
            </div>
          )}
        </div>
      </div>
    </footer>
  );
}
```

---

## Full Page Composition Example

```tsx
// app/page.tsx - 전체 랜딩 페이지 구성
import { HeroCentered } from "@/components/sections/hero-centered";
import { LogoCloud } from "@/components/sections/logo-cloud";
import { FeaturesGrid } from "@/components/sections/features-grid";
import { FeaturesBento } from "@/components/sections/features-bento";
import { Testimonials } from "@/components/sections/testimonials";
import { Pricing } from "@/components/sections/pricing";
import { FAQ } from "@/components/sections/faq";
import { Footer } from "@/components/sections/footer";
import {
  Zap,
  Shield,
  Clock,
  Users,
  BarChart,
  Globe
} from "lucide-react";

export default function LandingPage() {
  return (
    <main>
      {/* Hero */}
      <HeroCentered
        headline="복잡한 업무를 단순하게"
        subheadline="AI 기반 자동화로 반복 작업을 줄이고 핵심 업무에 집중하세요. 10,000개 이상의 팀이 생산성을 200% 향상시켰습니다."
        primaryCta={{ label: "무료로 시작하기", href: "/signup" }}
        secondaryCta={{ label: "데모 보기", href: "/demo" }}
        trustedBy={[
          "/logos/google.svg",
          "/logos/netflix.svg",
          "/logos/spotify.svg",
          "/logos/slack.svg",
        ]}
      />

      {/* Logo Cloud */}
      <LogoCloud
        title="1,000+ 기업이 신뢰합니다"
        logos={[
          { src: "/logos/company1.svg", alt: "Company 1" },
          { src: "/logos/company2.svg", alt: "Company 2" },
          // ...
        ]}
        animated
      />

      {/* Features */}
      <FeaturesGrid
        headline="모든 것을 한 곳에서"
        subheadline="팀 협업에 필요한 모든 도구를 제공합니다"
        features={[
          {
            icon: Zap,
            title: "초고속 성능",
            description: "밀리초 단위의 응답 속도로 끊김 없는 경험을 제공합니다.",
          },
          {
            icon: Shield,
            title: "엔터프라이즈 보안",
            description: "SOC 2 Type II 인증, 엔드투엔드 암호화를 지원합니다.",
          },
          {
            icon: Clock,
            title: "실시간 동기화",
            description: "모든 기기에서 실시간으로 데이터가 동기화됩니다.",
          },
          {
            icon: Users,
            title: "팀 협업",
            description: "역할 기반 권한 관리와 실시간 편집을 지원합니다.",
          },
          {
            icon: BarChart,
            title: "분석 대시보드",
            description: "팀 성과를 한눈에 파악할 수 있는 인사이트를 제공합니다.",
          },
          {
            icon: Globe,
            title: "글로벌 인프라",
            description: "전 세계 15개 리전에서 빠른 접속을 보장합니다.",
          },
        ]}
        columns={3}
      />

      {/* Testimonials */}
      <Testimonials
        headline="고객들의 이야기"
        testimonials={[
          {
            quote: "업무 효율이 3배 이상 향상되었습니다. 이제 없으면 안 될 도구입니다.",
            author: "김철수",
            role: "CTO",
            company: "테크스타트업",
            rating: 5,
          },
          // ...
        ]}
      />

      {/* Pricing */}
      <Pricing
        headline="간단한 요금제"
        subheadline="팀 규모에 맞는 플랜을 선택하세요"
        plans={[
          {
            name: "스타터",
            description: "소규모 팀을 위한 플랜",
            price: { monthly: 19000, yearly: 15200 },
            features: ["5명 사용자", "10GB 스토리지", "기본 분석"],
            cta: "시작하기",
          },
          {
            name: "프로",
            description: "성장하는 팀을 위한 플랜",
            price: { monthly: 49000, yearly: 39200 },
            features: ["무제한 사용자", "100GB 스토리지", "고급 분석", "우선 지원"],
            cta: "시작하기",
            popular: true,
          },
          {
            name: "엔터프라이즈",
            description: "대규모 조직을 위한 플랜",
            price: { monthly: 99000, yearly: 79200 },
            features: ["무제한 사용자", "무제한 스토리지", "전용 지원", "SLA 보장"],
            cta: "문의하기",
          },
        ]}
      />

      {/* FAQ */}
      <FAQ
        headline="자주 묻는 질문"
        items={[
          {
            question: "무료 체험 기간은 얼마인가요?",
            answer: "14일간 모든 기능을 무료로 체험하실 수 있습니다. 신용카드 정보 없이 시작할 수 있습니다.",
          },
          // ...
        ]}
      />

      {/* Final CTA */}
      <section className="py-20 lg:py-32 bg-primary text-primary-foreground">
        <div className="container mx-auto px-4 text-center">
          <h2 className="text-3xl md:text-4xl lg:text-5xl font-bold">
            지금 바로 시작하세요
          </h2>
          <p className="mt-4 text-lg opacity-90 max-w-2xl mx-auto">
            14일 무료 체험으로 팀의 생산성을 경험해보세요
          </p>
          <Button
            size="lg"
            variant="secondary"
            className="mt-8 min-w-[200px]"
          >
            무료로 시작하기
          </Button>
        </div>
      </section>

      {/* Footer */}
      <Footer
        logo={<img src="/logo.svg" alt="Logo" className="h-8" />}
        description="업무 자동화의 새로운 기준을 제시합니다."
        columns={[
          {
            title: "제품",
            links: [
              { label: "기능", href: "/features" },
              { label: "가격", href: "/pricing" },
              { label: "통합", href: "/integrations" },
            ],
          },
          {
            title: "리소스",
            links: [
              { label: "문서", href: "/docs" },
              { label: "블로그", href: "/blog" },
              { label: "고객 사례", href: "/customers" },
            ],
          },
          {
            title: "회사",
            links: [
              { label: "소개", href: "/about" },
              { label: "채용", href: "/careers" },
              { label: "연락처", href: "/contact" },
            ],
          },
        ]}
        newsletter
        social={[
          { platform: "twitter", href: "https://twitter.com" },
          { platform: "github", href: "https://github.com" },
          { platform: "linkedin", href: "https://linkedin.com" },
        ]}
      />
    </main>
  );
}
```

---

## Scroll Animations

### Framer Motion 섹션 애니메이션

```tsx
// lib/animations.ts
export const fadeInUp = {
  initial: { opacity: 0, y: 30 },
  animate: { opacity: 1, y: 0 },
  transition: { duration: 0.5 }
};

export const fadeInLeft = {
  initial: { opacity: 0, x: -30 },
  animate: { opacity: 1, x: 0 },
  transition: { duration: 0.5 }
};

export const fadeInRight = {
  initial: { opacity: 0, x: 30 },
  animate: { opacity: 1, x: 0 },
  transition: { duration: 0.5 }
};

export const staggerContainer = {
  animate: {
    transition: {
      staggerChildren: 0.1
    }
  }
};

export const scaleIn = {
  initial: { opacity: 0, scale: 0.9 },
  animate: { opacity: 1, scale: 1 },
  transition: { duration: 0.4 }
};
```

### 스크롤 기반 Parallax

```tsx
// hooks/use-parallax.ts
'use client';

import { useScroll, useTransform, MotionValue } from "framer-motion";
import { useRef } from "react";

export function useParallax(offset: number = 50) {
  const ref = useRef<HTMLDivElement>(null);

  const { scrollYProgress } = useScroll({
    target: ref,
    offset: ["start end", "end start"]
  });

  const y = useTransform(scrollYProgress, [0, 1], [offset, -offset]);

  return { ref, y };
}

// 사용 예시
function ParallaxImage() {
  const { ref, y } = useParallax(100);

  return (
    <div ref={ref} className="overflow-hidden">
      <motion.img
        src="/image.jpg"
        style={{ y }}
        className="w-full"
      />
    </div>
  );
}
```

---

## 접근성 요구사항

```markdown
## Landing Page 접근성 체크리스트

### 구조
- [ ] 논리적인 heading 계층 구조 (h1 → h2 → h3)
- [ ] Skip to content 링크 제공
- [ ] Landmark roles 사용 (main, nav, footer)

### 네비게이션
- [ ] 키보드로 모든 인터랙티브 요소 접근 가능
- [ ] Focus visible 스타일 명확
- [ ] Tab 순서 논리적

### 콘텐츠
- [ ] 이미지에 적절한 alt 텍스트
- [ ] 색상만으로 정보 전달하지 않음
- [ ] 대비율 4.5:1 이상 (본문), 3:1 이상 (큰 텍스트)

### 인터랙션
- [ ] 버튼/링크 터치 타겟 44px 이상
- [ ] 폼 필드 레이블 연결
- [ ] 에러 메시지 명확하게 전달

### 모션
- [ ] prefers-reduced-motion 존중
- [ ] 자동 재생 콘텐츠 정지 가능
```

---

## References

- `_references/COMPONENT-PATTERN.md`
- `7-motion/SKILL.md`
- `5-color/SKILL.md`
