# Content Page Design Skill

콘텐츠 및 에디토리얼 페이지 디자인을 위한 종합 스킬입니다.

## Triggers

- "콘텐츠", "블로그", "아티클", "content", "article", "editorial"

---

## Input

| 항목 | 필수 | 설명 |
|------|------|------|
| `contentType` | ✅ | 콘텐츠 유형 (blog, documentation, magazine, portfolio) |
| `brand` | ✅ | 브랜드 정보 (colors, fonts) |
| `features` | ❌ | 필요한 기능 목록 |

---

## Article Typography

### Prose 스타일 시스템

```tsx
// components/content/prose.tsx
import { cn } from "@/lib/utils";

interface ProseProps {
  children: React.ReactNode;
  className?: string;
  size?: "sm" | "base" | "lg";
}

export function Prose({ children, className, size = "base" }: ProseProps) {
  return (
    <div
      className={cn(
        "prose prose-neutral dark:prose-invert",
        // Size variants
        size === "sm" && "prose-sm",
        size === "lg" && "prose-lg",
        // Base typography
        "prose-headings:scroll-mt-24",
        "prose-headings:font-bold",
        "prose-h1:text-4xl prose-h1:tracking-tight",
        "prose-h2:text-3xl prose-h2:tracking-tight prose-h2:border-b prose-h2:pb-2 prose-h2:border-border",
        "prose-h3:text-2xl",
        "prose-h4:text-xl",
        // Body text
        "prose-p:leading-7",
        "prose-p:text-muted-foreground",
        // Links
        "prose-a:text-primary prose-a:no-underline hover:prose-a:underline",
        "prose-a:font-medium",
        // Lists
        "prose-li:text-muted-foreground",
        "prose-li:marker:text-muted-foreground/60",
        // Code
        "prose-code:rounded prose-code:bg-muted prose-code:px-1.5 prose-code:py-0.5",
        "prose-code:before:content-none prose-code:after:content-none",
        "prose-code:font-mono prose-code:text-sm",
        // Pre/Code blocks
        "prose-pre:bg-zinc-900 prose-pre:border prose-pre:border-border",
        "prose-pre:rounded-lg",
        // Blockquote
        "prose-blockquote:border-l-primary prose-blockquote:bg-primary/5",
        "prose-blockquote:py-1 prose-blockquote:not-italic",
        // Images
        "prose-img:rounded-lg prose-img:shadow-md",
        // Tables
        "prose-table:border prose-table:border-border",
        "prose-th:bg-muted prose-th:text-left",
        "prose-td:border-border",
        // HR
        "prose-hr:border-border",
        // Strong
        "prose-strong:text-foreground prose-strong:font-semibold",
        className
      )}
    >
      {children}
    </div>
  );
}
```

### Tailwind Typography 플러그인 설정

```js
// tailwind.config.js
const { fontFamily } = require("tailwindcss/defaultTheme");

module.exports = {
  // ...
  plugins: [require("@tailwindcss/typography")],
  theme: {
    extend: {
      typography: ({ theme }) => ({
        DEFAULT: {
          css: {
            "--tw-prose-body": theme("colors.muted.foreground"),
            "--tw-prose-headings": theme("colors.foreground"),
            "--tw-prose-lead": theme("colors.muted.foreground"),
            "--tw-prose-links": theme("colors.primary.DEFAULT"),
            "--tw-prose-bold": theme("colors.foreground"),
            "--tw-prose-counters": theme("colors.muted.foreground"),
            "--tw-prose-bullets": theme("colors.muted.foreground"),
            "--tw-prose-hr": theme("colors.border"),
            "--tw-prose-quotes": theme("colors.foreground"),
            "--tw-prose-quote-borders": theme("colors.primary.DEFAULT"),
            "--tw-prose-captions": theme("colors.muted.foreground"),
            "--tw-prose-code": theme("colors.foreground"),
            "--tw-prose-pre-code": theme("colors.zinc.100"),
            "--tw-prose-pre-bg": theme("colors.zinc.900"),
            "--tw-prose-th-borders": theme("colors.border"),
            "--tw-prose-td-borders": theme("colors.border"),
            maxWidth: "none",
            a: {
              fontWeight: "500",
              textDecoration: "none",
              "&:hover": {
                textDecoration: "underline",
              },
            },
            "h2, h3, h4": {
              scrollMarginTop: "6rem",
            },
            code: {
              fontWeight: "400",
            },
          },
        },
        invert: {
          css: {
            "--tw-prose-body": theme("colors.zinc.400"),
            "--tw-prose-headings": theme("colors.zinc.100"),
            "--tw-prose-lead": theme("colors.zinc.400"),
            "--tw-prose-links": theme("colors.primary.DEFAULT"),
            "--tw-prose-bold": theme("colors.zinc.100"),
            "--tw-prose-counters": theme("colors.zinc.400"),
            "--tw-prose-bullets": theme("colors.zinc.400"),
            "--tw-prose-hr": theme("colors.zinc.700"),
            "--tw-prose-quotes": theme("colors.zinc.100"),
            "--tw-prose-quote-borders": theme("colors.primary.DEFAULT"),
            "--tw-prose-captions": theme("colors.zinc.400"),
            "--tw-prose-code": theme("colors.zinc.100"),
            "--tw-prose-pre-code": theme("colors.zinc.200"),
            "--tw-prose-pre-bg": "rgb(24 24 27)",
            "--tw-prose-th-borders": theme("colors.zinc.700"),
            "--tw-prose-td-borders": theme("colors.zinc.700"),
          },
        },
      }),
    },
  },
};
```

---

## Blog Post Layout

### 기본 블로그 포스트 레이아웃

```tsx
// app/blog/[slug]/page.tsx
import Image from "next/image";
import Link from "next/link";
import { Prose } from "@/components/content/prose";
import { TableOfContents } from "@/components/content/toc";
import { AuthorCard } from "@/components/content/author-card";
import { RelatedPosts } from "@/components/content/related-posts";
import { ReadingProgress } from "@/components/content/reading-progress";
import { ShareButtons } from "@/components/content/share-buttons";
import { format } from "date-fns";
import { ko } from "date-fns/locale";
import { Clock, Calendar, Eye } from "lucide-react";

interface BlogPostPageProps {
  params: { slug: string };
}

export default async function BlogPostPage({ params }: BlogPostPageProps) {
  const post = await getPost(params.slug);

  return (
    <>
      {/* Reading Progress Indicator */}
      <ReadingProgress />

      <article className="relative">
        {/* Hero Section */}
        <header className="relative py-16 lg:py-24 bg-gradient-to-b from-muted/50 to-background">
          <div className="container mx-auto px-4">
            {/* Category Badge */}
            <Link
              href={`/blog/category/${post.category.slug}`}
              className="inline-flex items-center px-3 py-1 text-sm font-medium bg-primary/10 text-primary rounded-full hover:bg-primary/20 transition-colors"
            >
              {post.category.name}
            </Link>

            {/* Title */}
            <h1 className="mt-6 text-3xl md:text-4xl lg:text-5xl font-bold text-foreground tracking-tight max-w-4xl">
              {post.title}
            </h1>

            {/* Excerpt */}
            <p className="mt-6 text-lg md:text-xl text-muted-foreground max-w-3xl">
              {post.excerpt}
            </p>

            {/* Meta Info */}
            <div className="mt-8 flex flex-wrap items-center gap-6 text-sm text-muted-foreground">
              <div className="flex items-center gap-2">
                <Calendar className="h-4 w-4" />
                <time dateTime={post.publishedAt}>
                  {format(new Date(post.publishedAt), "yyyy년 M월 d일", { locale: ko })}
                </time>
              </div>
              <div className="flex items-center gap-2">
                <Clock className="h-4 w-4" />
                <span>{post.readingTime}분 읽기</span>
              </div>
              <div className="flex items-center gap-2">
                <Eye className="h-4 w-4" />
                <span>{post.views.toLocaleString()} 조회</span>
              </div>
            </div>

            {/* Author */}
            <div className="mt-8 flex items-center gap-4">
              <Image
                src={post.author.avatar}
                alt={post.author.name}
                width={48}
                height={48}
                className="rounded-full"
              />
              <div>
                <p className="font-medium text-foreground">{post.author.name}</p>
                <p className="text-sm text-muted-foreground">{post.author.role}</p>
              </div>
            </div>
          </div>
        </header>

        {/* Featured Image */}
        {post.featuredImage && (
          <div className="container mx-auto px-4 -mt-8 lg:-mt-16">
            <div className="relative aspect-[21/9] rounded-2xl overflow-hidden shadow-2xl">
              <Image
                src={post.featuredImage}
                alt={post.title}
                fill
                className="object-cover"
                priority
              />
            </div>
          </div>
        )}

        {/* Content Grid */}
        <div className="container mx-auto px-4 py-12 lg:py-16">
          <div className="grid lg:grid-cols-[1fr_280px] gap-12 lg:gap-16">
            {/* Main Content */}
            <div>
              <Prose className="max-w-none">
                <div dangerouslySetInnerHTML={{ __html: post.content }} />
              </Prose>

              {/* Tags */}
              {post.tags && post.tags.length > 0 && (
                <div className="mt-12 pt-8 border-t border-border">
                  <div className="flex flex-wrap gap-2">
                    {post.tags.map((tag) => (
                      <Link
                        key={tag.slug}
                        href={`/blog/tag/${tag.slug}`}
                        className="px-3 py-1.5 text-sm bg-muted hover:bg-muted/80 text-muted-foreground rounded-full transition-colors"
                      >
                        #{tag.name}
                      </Link>
                    ))}
                  </div>
                </div>
              )}

              {/* Share */}
              <div className="mt-8 pt-8 border-t border-border">
                <p className="text-sm font-medium text-foreground mb-4">
                  이 글이 도움이 되었다면 공유해주세요
                </p>
                <ShareButtons url={post.url} title={post.title} />
              </div>

              {/* Author Bio */}
              <div className="mt-12">
                <AuthorCard author={post.author} />
              </div>
            </div>

            {/* Sidebar */}
            <aside className="hidden lg:block">
              <div className="sticky top-24 space-y-8">
                <TableOfContents headings={post.headings} />

                {/* Newsletter CTA */}
                <div className="p-6 rounded-xl bg-muted/50 border border-border">
                  <h3 className="font-semibold text-foreground mb-2">
                    뉴스레터 구독
                  </h3>
                  <p className="text-sm text-muted-foreground mb-4">
                    새로운 글을 이메일로 받아보세요
                  </p>
                  <form className="space-y-3">
                    <input
                      type="email"
                      placeholder="이메일 주소"
                      className="w-full px-3 py-2 text-sm rounded-md border border-input bg-background"
                    />
                    <button className="w-full px-3 py-2 text-sm font-medium bg-primary text-primary-foreground rounded-md hover:bg-primary/90 transition-colors">
                      구독하기
                    </button>
                  </form>
                </div>
              </div>
            </aside>
          </div>
        </div>

        {/* Related Posts */}
        <section className="py-16 bg-muted/30">
          <div className="container mx-auto px-4">
            <h2 className="text-2xl font-bold text-foreground mb-8">
              관련 글
            </h2>
            <RelatedPosts posts={post.relatedPosts} />
          </div>
        </section>
      </article>
    </>
  );
}
```

---

## Table of Contents

```tsx
// components/content/toc.tsx
"use client";

import { useEffect, useState } from "react";
import { cn } from "@/lib/utils";

interface Heading {
  id: string;
  text: string;
  level: number;
}

interface TableOfContentsProps {
  headings: Heading[];
}

export function TableOfContents({ headings }: TableOfContentsProps) {
  const [activeId, setActiveId] = useState<string>("");

  useEffect(() => {
    const observer = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting) {
            setActiveId(entry.target.id);
          }
        });
      },
      {
        rootMargin: "-100px 0% -80% 0%",
        threshold: 0,
      }
    );

    headings.forEach((heading) => {
      const element = document.getElementById(heading.id);
      if (element) {
        observer.observe(element);
      }
    });

    return () => observer.disconnect();
  }, [headings]);

  const handleClick = (e: React.MouseEvent<HTMLAnchorElement>, id: string) => {
    e.preventDefault();
    const element = document.getElementById(id);
    if (element) {
      const top = element.offsetTop - 100;
      window.scrollTo({ top, behavior: "smooth" });
    }
  };

  if (headings.length === 0) return null;

  return (
    <nav className="space-y-1">
      <p className="text-sm font-semibold text-foreground mb-4">목차</p>
      <ul className="space-y-1 text-sm">
        {headings.map((heading) => (
          <li
            key={heading.id}
            style={{ paddingLeft: `${(heading.level - 2) * 12}px` }}
          >
            <a
              href={`#${heading.id}`}
              onClick={(e) => handleClick(e, heading.id)}
              className={cn(
                "block py-1.5 text-muted-foreground hover:text-foreground transition-colors border-l-2 pl-3 -ml-px",
                activeId === heading.id
                  ? "border-primary text-foreground font-medium"
                  : "border-transparent"
              )}
            >
              {heading.text}
            </a>
          </li>
        ))}
      </ul>
    </nav>
  );
}
```

---

## Code Block Styling

### Syntax Highlighting (Shiki/Prism)

```tsx
// components/content/code-block.tsx
"use client";

import { useState } from "react";
import { Button } from "@/components/ui/button";
import { Check, Copy, Terminal } from "lucide-react";
import { cn } from "@/lib/utils";

interface CodeBlockProps {
  code: string;
  language: string;
  filename?: string;
  showLineNumbers?: boolean;
  highlightLines?: number[];
  className?: string;
}

export function CodeBlock({
  code,
  language,
  filename,
  showLineNumbers = true,
  highlightLines = [],
  className,
}: CodeBlockProps) {
  const [copied, setCopied] = useState(false);

  const handleCopy = async () => {
    await navigator.clipboard.writeText(code);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  const lines = code.split("\n");

  return (
    <div className={cn("relative group my-6", className)}>
      {/* Header */}
      {(filename || language) && (
        <div className="flex items-center justify-between px-4 py-2 bg-zinc-800 border-b border-zinc-700 rounded-t-lg">
          <div className="flex items-center gap-2">
            <Terminal className="h-4 w-4 text-zinc-400" />
            {filename ? (
              <span className="text-sm text-zinc-300 font-mono">{filename}</span>
            ) : (
              <span className="text-sm text-zinc-400">{language}</span>
            )}
          </div>
          <Button
            variant="ghost"
            size="sm"
            className="h-7 px-2 text-zinc-400 hover:text-zinc-100 hover:bg-zinc-700"
            onClick={handleCopy}
          >
            {copied ? (
              <>
                <Check className="h-3.5 w-3.5 mr-1" />
                복사됨
              </>
            ) : (
              <>
                <Copy className="h-3.5 w-3.5 mr-1" />
                복사
              </>
            )}
          </Button>
        </div>
      )}

      {/* Code */}
      <div
        className={cn(
          "overflow-x-auto bg-zinc-900 p-4",
          filename || language ? "rounded-b-lg" : "rounded-lg"
        )}
      >
        <pre className="text-sm font-mono">
          <code>
            {lines.map((line, index) => (
              <div
                key={index}
                className={cn(
                  "table-row",
                  highlightLines.includes(index + 1) &&
                    "bg-primary/10 -mx-4 px-4"
                )}
              >
                {showLineNumbers && (
                  <span className="table-cell pr-4 text-right text-zinc-600 select-none w-8">
                    {index + 1}
                  </span>
                )}
                <span className="table-cell text-zinc-100">{line || " "}</span>
              </div>
            ))}
          </code>
        </pre>
      </div>

      {/* Copy button (no header) */}
      {!filename && !language && (
        <Button
          variant="ghost"
          size="icon"
          className="absolute top-2 right-2 h-8 w-8 text-zinc-400 hover:text-zinc-100 hover:bg-zinc-700 opacity-0 group-hover:opacity-100 transition-opacity"
          onClick={handleCopy}
        >
          {copied ? (
            <Check className="h-4 w-4" />
          ) : (
            <Copy className="h-4 w-4" />
          )}
        </Button>
      )}
    </div>
  );
}
```

### 코드 블록 MDX 설정

```tsx
// lib/mdx-components.tsx
import { CodeBlock } from "@/components/content/code-block";

export const mdxComponents = {
  pre: ({ children, ...props }: any) => {
    const code = children?.props?.children || "";
    const language = children?.props?.className?.replace("language-", "") || "";
    const meta = children?.props?.__rawString__ || "";

    // 메타 정보 파싱 (예: ```tsx filename="app.tsx" showLineNumbers {1,3-5})
    const filename = meta.match(/filename="([^"]+)"/)?.[1];
    const showLineNumbers = meta.includes("showLineNumbers");
    const highlightLines = parseHighlightLines(meta);

    return (
      <CodeBlock
        code={code.trim()}
        language={language}
        filename={filename}
        showLineNumbers={showLineNumbers}
        highlightLines={highlightLines}
      />
    );
  },
  code: ({ children, className, ...props }: any) => {
    // 인라인 코드
    if (!className) {
      return (
        <code
          className="px-1.5 py-0.5 text-sm font-mono bg-muted rounded text-foreground"
          {...props}
        >
          {children}
        </code>
      );
    }
    return <code className={className} {...props}>{children}</code>;
  },
};

function parseHighlightLines(meta: string): number[] {
  const match = meta.match(/\{([^}]+)\}/);
  if (!match) return [];

  const lines: number[] = [];
  const parts = match[1].split(",");

  parts.forEach((part) => {
    if (part.includes("-")) {
      const [start, end] = part.split("-").map(Number);
      for (let i = start; i <= end; i++) {
        lines.push(i);
      }
    } else {
      lines.push(Number(part));
    }
  });

  return lines;
}
```

---

## Image Gallery

```tsx
// components/content/image-gallery.tsx
"use client";

import { useState } from "react";
import Image from "next/image";
import { Dialog, DialogContent } from "@/components/ui/dialog";
import { Button } from "@/components/ui/button";
import { ChevronLeft, ChevronRight, X, ZoomIn } from "lucide-react";
import { cn } from "@/lib/utils";

interface GalleryImage {
  src: string;
  alt: string;
  caption?: string;
}

interface ImageGalleryProps {
  images: GalleryImage[];
  columns?: 2 | 3 | 4;
  gap?: "sm" | "md" | "lg";
}

export function ImageGallery({
  images,
  columns = 3,
  gap = "md",
}: ImageGalleryProps) {
  const [selectedIndex, setSelectedIndex] = useState<number | null>(null);

  const columnClasses = {
    2: "grid-cols-2",
    3: "grid-cols-2 md:grid-cols-3",
    4: "grid-cols-2 md:grid-cols-3 lg:grid-cols-4",
  };

  const gapClasses = {
    sm: "gap-2",
    md: "gap-4",
    lg: "gap-6",
  };

  const handlePrev = () => {
    if (selectedIndex !== null) {
      setSelectedIndex(selectedIndex === 0 ? images.length - 1 : selectedIndex - 1);
    }
  };

  const handleNext = () => {
    if (selectedIndex !== null) {
      setSelectedIndex(selectedIndex === images.length - 1 ? 0 : selectedIndex + 1);
    }
  };

  return (
    <>
      {/* Gallery Grid */}
      <div className={cn("grid", columnClasses[columns], gapClasses[gap])}>
        {images.map((image, index) => (
          <button
            key={index}
            className="group relative aspect-square overflow-hidden rounded-lg bg-muted"
            onClick={() => setSelectedIndex(index)}
          >
            <Image
              src={image.src}
              alt={image.alt}
              fill
              className="object-cover transition-transform group-hover:scale-105"
            />
            <div className="absolute inset-0 bg-black/0 group-hover:bg-black/30 transition-colors flex items-center justify-center">
              <ZoomIn className="h-8 w-8 text-white opacity-0 group-hover:opacity-100 transition-opacity" />
            </div>
          </button>
        ))}
      </div>

      {/* Lightbox */}
      <Dialog
        open={selectedIndex !== null}
        onOpenChange={() => setSelectedIndex(null)}
      >
        <DialogContent className="max-w-5xl p-0 bg-black/95 border-none">
          {selectedIndex !== null && (
            <>
              {/* Image */}
              <div className="relative aspect-[16/10] w-full">
                <Image
                  src={images[selectedIndex].src}
                  alt={images[selectedIndex].alt}
                  fill
                  className="object-contain"
                />
              </div>

              {/* Caption */}
              {images[selectedIndex].caption && (
                <div className="p-4 text-center text-sm text-white/80">
                  {images[selectedIndex].caption}
                </div>
              )}

              {/* Navigation */}
              <Button
                variant="ghost"
                size="icon"
                className="absolute left-2 top-1/2 -translate-y-1/2 text-white hover:bg-white/20"
                onClick={handlePrev}
              >
                <ChevronLeft className="h-8 w-8" />
              </Button>
              <Button
                variant="ghost"
                size="icon"
                className="absolute right-2 top-1/2 -translate-y-1/2 text-white hover:bg-white/20"
                onClick={handleNext}
              >
                <ChevronRight className="h-8 w-8" />
              </Button>

              {/* Close */}
              <Button
                variant="ghost"
                size="icon"
                className="absolute top-2 right-2 text-white hover:bg-white/20"
                onClick={() => setSelectedIndex(null)}
              >
                <X className="h-6 w-6" />
              </Button>

              {/* Counter */}
              <div className="absolute bottom-4 left-1/2 -translate-x-1/2 text-sm text-white/60">
                {selectedIndex + 1} / {images.length}
              </div>
            </>
          )}
        </DialogContent>
      </Dialog>
    </>
  );
}
```

---

## Pull Quotes & Callouts

```tsx
// components/content/callout.tsx
import { cn } from "@/lib/utils";
import {
  Info,
  AlertTriangle,
  CheckCircle,
  XCircle,
  Lightbulb,
  Quote,
} from "lucide-react";

interface CalloutProps {
  type?: "info" | "warning" | "success" | "error" | "tip" | "note";
  title?: string;
  children: React.ReactNode;
}

const calloutStyles = {
  info: {
    container: "bg-blue-50 border-blue-200 dark:bg-blue-950/50 dark:border-blue-900",
    icon: "text-blue-600 dark:text-blue-400",
    title: "text-blue-900 dark:text-blue-200",
    Icon: Info,
  },
  warning: {
    container: "bg-yellow-50 border-yellow-200 dark:bg-yellow-950/50 dark:border-yellow-900",
    icon: "text-yellow-600 dark:text-yellow-400",
    title: "text-yellow-900 dark:text-yellow-200",
    Icon: AlertTriangle,
  },
  success: {
    container: "bg-green-50 border-green-200 dark:bg-green-950/50 dark:border-green-900",
    icon: "text-green-600 dark:text-green-400",
    title: "text-green-900 dark:text-green-200",
    Icon: CheckCircle,
  },
  error: {
    container: "bg-red-50 border-red-200 dark:bg-red-950/50 dark:border-red-900",
    icon: "text-red-600 dark:text-red-400",
    title: "text-red-900 dark:text-red-200",
    Icon: XCircle,
  },
  tip: {
    container: "bg-purple-50 border-purple-200 dark:bg-purple-950/50 dark:border-purple-900",
    icon: "text-purple-600 dark:text-purple-400",
    title: "text-purple-900 dark:text-purple-200",
    Icon: Lightbulb,
  },
  note: {
    container: "bg-gray-50 border-gray-200 dark:bg-gray-900/50 dark:border-gray-800",
    icon: "text-gray-600 dark:text-gray-400",
    title: "text-gray-900 dark:text-gray-200",
    Icon: Info,
  },
};

export function Callout({ type = "info", title, children }: CalloutProps) {
  const styles = calloutStyles[type];
  const Icon = styles.Icon;

  return (
    <div
      className={cn(
        "my-6 rounded-lg border p-4",
        styles.container
      )}
      role="note"
    >
      <div className="flex gap-3">
        <Icon className={cn("h-5 w-5 flex-shrink-0 mt-0.5", styles.icon)} />
        <div className="flex-1 min-w-0">
          {title && (
            <p className={cn("font-semibold mb-1", styles.title)}>
              {title}
            </p>
          )}
          <div className="text-sm [&>p]:mb-0">{children}</div>
        </div>
      </div>
    </div>
  );
}

// Pull Quote 컴포넌트
interface PullQuoteProps {
  children: React.ReactNode;
  author?: string;
  source?: string;
}

export function PullQuote({ children, author, source }: PullQuoteProps) {
  return (
    <figure className="my-8 py-8 border-y border-border">
      <blockquote className="relative">
        <Quote className="absolute -top-4 -left-2 h-12 w-12 text-primary/20" />
        <p className="relative z-10 text-2xl md:text-3xl font-medium text-foreground leading-relaxed italic">
          {children}
        </p>
      </blockquote>
      {(author || source) && (
        <figcaption className="mt-4 text-right">
          {author && (
            <span className="font-medium text-foreground">{author}</span>
          )}
          {author && source && <span className="text-muted-foreground"> - </span>}
          {source && (
            <cite className="text-muted-foreground not-italic">{source}</cite>
          )}
        </figcaption>
      )}
    </figure>
  );
}
```

---

## Author Card

```tsx
// components/content/author-card.tsx
import Image from "next/image";
import Link from "next/link";
import { Button } from "@/components/ui/button";
import { Twitter, Linkedin, Github, Globe } from "lucide-react";

interface Author {
  name: string;
  slug: string;
  avatar: string;
  role: string;
  bio: string;
  social?: {
    twitter?: string;
    linkedin?: string;
    github?: string;
    website?: string;
  };
}

interface AuthorCardProps {
  author: Author;
  variant?: "default" | "compact";
}

export function AuthorCard({ author, variant = "default" }: AuthorCardProps) {
  if (variant === "compact") {
    return (
      <Link
        href={`/blog/author/${author.slug}`}
        className="flex items-center gap-3 group"
      >
        <Image
          src={author.avatar}
          alt={author.name}
          width={40}
          height={40}
          className="rounded-full"
        />
        <div>
          <p className="font-medium text-foreground group-hover:text-primary transition-colors">
            {author.name}
          </p>
          <p className="text-sm text-muted-foreground">{author.role}</p>
        </div>
      </Link>
    );
  }

  return (
    <div className="flex flex-col sm:flex-row gap-6 p-6 rounded-xl bg-muted/50 border border-border">
      <Link href={`/blog/author/${author.slug}`} className="flex-shrink-0">
        <Image
          src={author.avatar}
          alt={author.name}
          width={80}
          height={80}
          className="rounded-full"
        />
      </Link>
      <div className="flex-1">
        <Link
          href={`/blog/author/${author.slug}`}
          className="font-semibold text-lg text-foreground hover:text-primary transition-colors"
        >
          {author.name}
        </Link>
        <p className="text-sm text-primary mb-2">{author.role}</p>
        <p className="text-sm text-muted-foreground mb-4">{author.bio}</p>

        {author.social && (
          <div className="flex items-center gap-2">
            {author.social.twitter && (
              <Button variant="ghost" size="icon" className="h-8 w-8" asChild>
                <a href={author.social.twitter} target="_blank" rel="noopener noreferrer">
                  <Twitter className="h-4 w-4" />
                </a>
              </Button>
            )}
            {author.social.linkedin && (
              <Button variant="ghost" size="icon" className="h-8 w-8" asChild>
                <a href={author.social.linkedin} target="_blank" rel="noopener noreferrer">
                  <Linkedin className="h-4 w-4" />
                </a>
              </Button>
            )}
            {author.social.github && (
              <Button variant="ghost" size="icon" className="h-8 w-8" asChild>
                <a href={author.social.github} target="_blank" rel="noopener noreferrer">
                  <Github className="h-4 w-4" />
                </a>
              </Button>
            )}
            {author.social.website && (
              <Button variant="ghost" size="icon" className="h-8 w-8" asChild>
                <a href={author.social.website} target="_blank" rel="noopener noreferrer">
                  <Globe className="h-4 w-4" />
                </a>
              </Button>
            )}
          </div>
        )}
      </div>
    </div>
  );
}
```

---

## Related Posts Section

```tsx
// components/content/related-posts.tsx
import Image from "next/image";
import Link from "next/link";
import { format } from "date-fns";
import { ko } from "date-fns/locale";

interface RelatedPost {
  slug: string;
  title: string;
  excerpt: string;
  featuredImage?: string;
  publishedAt: string;
  category: { name: string; slug: string };
}

interface RelatedPostsProps {
  posts: RelatedPost[];
}

export function RelatedPosts({ posts }: RelatedPostsProps) {
  if (posts.length === 0) return null;

  return (
    <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
      {posts.map((post) => (
        <article
          key={post.slug}
          className="group flex flex-col rounded-xl overflow-hidden border border-border bg-card hover:shadow-lg transition-shadow"
        >
          {/* Image */}
          <Link href={`/blog/${post.slug}`} className="relative aspect-[16/9] overflow-hidden">
            {post.featuredImage ? (
              <Image
                src={post.featuredImage}
                alt={post.title}
                fill
                className="object-cover transition-transform group-hover:scale-105"
              />
            ) : (
              <div className="w-full h-full bg-gradient-to-br from-primary/20 to-primary/5" />
            )}
          </Link>

          {/* Content */}
          <div className="flex-1 p-5">
            <Link
              href={`/blog/category/${post.category.slug}`}
              className="text-xs font-medium text-primary hover:underline"
            >
              {post.category.name}
            </Link>
            <Link href={`/blog/${post.slug}`}>
              <h3 className="mt-2 font-semibold text-foreground line-clamp-2 group-hover:text-primary transition-colors">
                {post.title}
              </h3>
            </Link>
            <p className="mt-2 text-sm text-muted-foreground line-clamp-2">
              {post.excerpt}
            </p>
            <time
              dateTime={post.publishedAt}
              className="mt-4 block text-xs text-muted-foreground"
            >
              {format(new Date(post.publishedAt), "yyyy년 M월 d일", { locale: ko })}
            </time>
          </div>
        </article>
      ))}
    </div>
  );
}
```

---

## Reading Progress Indicator

```tsx
// components/content/reading-progress.tsx
"use client";

import { useEffect, useState } from "react";
import { motion, useScroll, useSpring } from "framer-motion";

export function ReadingProgress() {
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

// 읽기 시간과 함께 표시
export function ReadingProgressWithTime() {
  const { scrollYProgress } = useScroll();
  const [readingProgress, setReadingProgress] = useState(0);

  useEffect(() => {
    return scrollYProgress.on("change", (latest) => {
      setReadingProgress(Math.round(latest * 100));
    });
  }, [scrollYProgress]);

  return (
    <>
      {/* Progress Bar */}
      <div className="fixed top-0 left-0 right-0 h-1 bg-muted z-50">
        <motion.div
          className="h-full bg-primary"
          style={{ scaleX: scrollYProgress, transformOrigin: "left" }}
        />
      </div>

      {/* Floating Progress Indicator */}
      {readingProgress > 0 && readingProgress < 100 && (
        <motion.div
          className="fixed bottom-6 right-6 w-12 h-12 rounded-full bg-card border border-border shadow-lg flex items-center justify-center z-40"
          initial={{ opacity: 0, scale: 0 }}
          animate={{ opacity: 1, scale: 1 }}
          exit={{ opacity: 0, scale: 0 }}
        >
          <span className="text-sm font-medium text-foreground">
            {readingProgress}%
          </span>
        </motion.div>
      )}
    </>
  );
}
```

---

## Magazine-Style Layouts

### 피처드 아티클 그리드

```tsx
// components/content/featured-grid.tsx
import Image from "next/image";
import Link from "next/link";
import { format } from "date-fns";
import { ko } from "date-fns/locale";
import { cn } from "@/lib/utils";

interface FeaturedPost {
  slug: string;
  title: string;
  excerpt: string;
  featuredImage: string;
  publishedAt: string;
  category: { name: string; slug: string };
  author: { name: string; avatar: string };
}

interface FeaturedGridProps {
  posts: FeaturedPost[];
  layout?: "hero" | "magazine" | "mosaic";
}

export function FeaturedGrid({ posts, layout = "hero" }: FeaturedGridProps) {
  if (posts.length === 0) return null;

  // Hero Layout: 1 large + 2 small
  if (layout === "hero") {
    const [main, ...rest] = posts.slice(0, 3);

    return (
      <div className="grid lg:grid-cols-2 gap-6">
        {/* Main Feature */}
        <Link
          href={`/blog/${main.slug}`}
          className="group relative aspect-[4/3] lg:aspect-auto lg:row-span-2 rounded-2xl overflow-hidden"
        >
          <Image
            src={main.featuredImage}
            alt={main.title}
            fill
            className="object-cover transition-transform group-hover:scale-105"
            priority
          />
          <div className="absolute inset-0 bg-gradient-to-t from-black/80 via-black/20 to-transparent" />
          <div className="absolute bottom-0 left-0 right-0 p-6 lg:p-8">
            <span className="inline-block px-3 py-1 text-xs font-medium bg-primary text-primary-foreground rounded-full mb-3">
              {main.category.name}
            </span>
            <h2 className="text-2xl lg:text-3xl font-bold text-white mb-2 group-hover:text-primary transition-colors">
              {main.title}
            </h2>
            <p className="text-white/80 line-clamp-2 mb-4">
              {main.excerpt}
            </p>
            <div className="flex items-center gap-3 text-white/60 text-sm">
              <Image
                src={main.author.avatar}
                alt={main.author.name}
                width={32}
                height={32}
                className="rounded-full"
              />
              <span>{main.author.name}</span>
              <span>·</span>
              <time>{format(new Date(main.publishedAt), "M월 d일", { locale: ko })}</time>
            </div>
          </div>
        </Link>

        {/* Secondary Features */}
        <div className="grid gap-6">
          {rest.map((post) => (
            <Link
              key={post.slug}
              href={`/blog/${post.slug}`}
              className="group relative aspect-[2/1] rounded-xl overflow-hidden"
            >
              <Image
                src={post.featuredImage}
                alt={post.title}
                fill
                className="object-cover transition-transform group-hover:scale-105"
              />
              <div className="absolute inset-0 bg-gradient-to-t from-black/70 to-transparent" />
              <div className="absolute bottom-0 left-0 right-0 p-5">
                <span className="inline-block px-2 py-0.5 text-xs font-medium bg-white/20 text-white rounded-full mb-2">
                  {post.category.name}
                </span>
                <h3 className="text-lg font-semibold text-white group-hover:text-primary transition-colors line-clamp-2">
                  {post.title}
                </h3>
              </div>
            </Link>
          ))}
        </div>
      </div>
    );
  }

  // Magazine Layout: Varied sizes
  if (layout === "magazine") {
    return (
      <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-6">
        {posts.slice(0, 5).map((post, index) => (
          <Link
            key={post.slug}
            href={`/blog/${post.slug}`}
            className={cn(
              "group relative rounded-xl overflow-hidden",
              index === 0 && "md:col-span-2 lg:col-span-2 lg:row-span-2 aspect-[4/3] lg:aspect-auto",
              index > 0 && "aspect-[3/2]"
            )}
          >
            <Image
              src={post.featuredImage}
              alt={post.title}
              fill
              className="object-cover transition-transform group-hover:scale-105"
            />
            <div className="absolute inset-0 bg-gradient-to-t from-black/70 to-transparent" />
            <div className="absolute bottom-0 left-0 right-0 p-4 lg:p-6">
              <span className="inline-block px-2 py-0.5 text-xs font-medium bg-white/20 text-white rounded-full mb-2">
                {post.category.name}
              </span>
              <h3
                className={cn(
                  "font-semibold text-white group-hover:text-primary transition-colors line-clamp-2",
                  index === 0 ? "text-xl lg:text-2xl" : "text-base"
                )}
              >
                {post.title}
              </h3>
            </div>
          </Link>
        ))}
      </div>
    );
  }

  // Mosaic Layout
  return (
    <div className="grid grid-cols-2 lg:grid-cols-4 gap-4">
      {posts.slice(0, 6).map((post, index) => {
        const sizes = [
          "col-span-2 row-span-2",
          "col-span-1 row-span-1",
          "col-span-1 row-span-1",
          "col-span-1 row-span-2",
          "col-span-1 row-span-1",
          "col-span-1 row-span-1",
        ];

        return (
          <Link
            key={post.slug}
            href={`/blog/${post.slug}`}
            className={cn(
              "group relative rounded-lg overflow-hidden",
              sizes[index] || "col-span-1"
            )}
          >
            <div className="aspect-square">
              <Image
                src={post.featuredImage}
                alt={post.title}
                fill
                className="object-cover transition-transform group-hover:scale-105"
              />
            </div>
            <div className="absolute inset-0 bg-black/40 group-hover:bg-black/50 transition-colors" />
            <div className="absolute bottom-0 left-0 right-0 p-4">
              <h3 className="font-medium text-white text-sm lg:text-base line-clamp-2">
                {post.title}
              </h3>
            </div>
          </Link>
        );
      })}
    </div>
  );
}
```

---

## Blog List Page

```tsx
// app/blog/page.tsx
import { FeaturedGrid } from "@/components/content/featured-grid";
import { BlogPostCard } from "@/components/content/blog-post-card";
import { CategoryFilter } from "@/components/content/category-filter";
import { Pagination } from "@/components/content/pagination";

interface BlogPageProps {
  searchParams: {
    page?: string;
    category?: string;
  };
}

export default async function BlogPage({ searchParams }: BlogPageProps) {
  const page = Number(searchParams.page) || 1;
  const category = searchParams.category;

  const { posts, totalPages, featuredPosts, categories } = await getPosts({
    page,
    category,
  });

  return (
    <div className="min-h-screen">
      {/* Hero Section */}
      <section className="py-16 lg:py-24 bg-gradient-to-b from-muted/50 to-background">
        <div className="container mx-auto px-4">
          <h1 className="text-4xl md:text-5xl lg:text-6xl font-bold text-foreground tracking-tight">
            블로그
          </h1>
          <p className="mt-4 text-lg text-muted-foreground max-w-2xl">
            개발, 디자인, 프로덕트에 관한 인사이트를 공유합니다.
          </p>
        </div>
      </section>

      {/* Featured Posts */}
      {page === 1 && !category && (
        <section className="py-12">
          <div className="container mx-auto px-4">
            <h2 className="text-2xl font-bold text-foreground mb-8">
              추천 글
            </h2>
            <FeaturedGrid posts={featuredPosts} layout="hero" />
          </div>
        </section>
      )}

      {/* Category Filter */}
      <section className="py-8 border-b border-border">
        <div className="container mx-auto px-4">
          <CategoryFilter
            categories={categories}
            activeCategory={category}
          />
        </div>
      </section>

      {/* Posts Grid */}
      <section className="py-12">
        <div className="container mx-auto px-4">
          <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-8">
            {posts.map((post) => (
              <BlogPostCard key={post.slug} post={post} />
            ))}
          </div>

          {/* Pagination */}
          <div className="mt-12">
            <Pagination
              currentPage={page}
              totalPages={totalPages}
              basePath={category ? `/blog?category=${category}` : "/blog"}
            />
          </div>
        </div>
      </section>
    </div>
  );
}
```

---

## 접근성 요구사항

```markdown
## Content Page 접근성 체크리스트

### 구조
- [ ] 적절한 heading 계층 (h1 → h2 → h3)
- [ ] article, section 등 시맨틱 요소 사용
- [ ] Skip to content 링크
- [ ] 목차(TOC) 제공

### 이미지
- [ ] 모든 이미지에 의미있는 alt 텍스트
- [ ] 장식용 이미지는 alt="" 또는 role="presentation"
- [ ] 복잡한 이미지에 긴 설명 제공

### 코드 블록
- [ ] 문법 강조에 색상만 의존하지 않음
- [ ] 복사 버튼 키보드 접근 가능
- [ ] aria-label로 언어 표시

### 링크
- [ ] 링크 텍스트가 목적지 설명
- [ ] "여기를 클릭하세요" 대신 구체적인 텍스트
- [ ] 외부 링크 표시 (아이콘 + aria-label)

### 읽기 경험
- [ ] 충분한 줄 간격 (line-height 1.5+)
- [ ] 적절한 단락 길이
- [ ] 본문 너비 제한 (45-75자)
```

---

## 반응형 고려사항

```markdown
## Content Page 반응형 가이드

### Typography
| 요소 | Mobile | Tablet | Desktop |
|------|--------|--------|---------|
| h1 | 2rem | 2.5rem | 3rem |
| h2 | 1.5rem | 1.875rem | 2.25rem |
| body | 1rem | 1rem | 1.125rem |
| line-height | 1.6 | 1.7 | 1.8 |

### Layout
- Mobile: 단일 컬럼, TOC 숨김
- Tablet: 단일 컬럼, TOC 접이식
- Desktop: 사이드바 TOC 고정

### Images
- Mobile: 전체 너비, aspect-ratio 유지
- Desktop: max-width 제한, 캡션 표시

### Code Blocks
- Mobile: 가로 스크롤, 줄번호 숨김 가능
- Desktop: 전체 표시, 파일명 + 복사 버튼
```

---

## References

- `_references/COMPONENT-PATTERN.md`
- `4-typography/SKILL.md`
- `5-color/SKILL.md`
