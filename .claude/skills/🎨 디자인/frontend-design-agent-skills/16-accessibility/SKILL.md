# Accessibility Skill

웹 접근성(a11y) 검증 및 WCAG 2.2 준수를 위한 종합 가이드입니다.

## Triggers

- "접근성", "a11y", "accessibility", "WCAG", "스크린리더"

---

## 접근성 영역

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                        Web Accessibility Areas                               │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  ┌──────────────────┐ │
│  │   Visual     │  │   Motor      │  │  Cognitive   │  │  Neurodiversity  │ │
│  ├──────────────┤  ├──────────────┤  ├──────────────┤  ├──────────────────┤ │
│  │ Color        │  │ Keyboard     │  │ Clear        │  │ ADHD:            │ │
│  │ Contrast     │  │ Navigation   │  │ Hierarchy    │  │ Focus, Minimal   │ │
│  │ Text Size    │  │ Touch Target │  │ Predictable  │  │                  │ │
│  │ Screen       │  │ Focus        │  │ Error        │  │ Autism:          │ │
│  │ Reader       │  │ Management   │  │ Prevention   │  │ Patterns, Calm   │ │
│  │              │  │              │  │              │  │                  │ │
│  │              │  │              │  │              │  │ Dyslexia:        │ │
│  │              │  │              │  │              │  │ Typography       │ │
│  └──────────────┘  └──────────────┘  └──────────────┘  └──────────────────┘ │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 1. WCAG 2.2 핵심 요구사항

### 인식 가능 (Perceivable)

| 기준 | Level | 설명 | 체크 |
|------|-------|------|------|
| 1.1.1 | A | 모든 비텍스트 콘텐츠에 대체 텍스트 | [ ] |
| 1.3.1 | A | 정보와 관계가 프로그래밍적으로 결정됨 | [ ] |
| 1.4.1 | A | 색상만으로 정보 전달 안함 | [ ] |
| 1.4.3 | AA | 텍스트 대비율 4.5:1 이상 | [ ] |
| 1.4.4 | AA | 텍스트 200% 확대 가능 | [ ] |
| 1.4.6 | AAA | 텍스트 대비율 7:1 이상 | [ ] |
| 1.4.11 | AA | UI 컴포넌트 대비율 3:1 이상 | [ ] |
| 1.4.12 | AA | 텍스트 간격 조정 가능 | [ ] |

### 조작 가능 (Operable)

| 기준 | Level | 설명 | 체크 |
|------|-------|------|------|
| 2.1.1 | A | 모든 기능 키보드로 접근 가능 | [ ] |
| 2.1.2 | A | 키보드 트랩 없음 | [ ] |
| 2.4.3 | A | 포커스 순서가 논리적 | [ ] |
| 2.4.6 | AA | 제목과 레이블이 명확 | [ ] |
| 2.4.7 | AA | 포커스 표시가 시각적으로 보임 | [ ] |
| 2.4.11 | AA | 포커스가 가려지지 않음 (WCAG 2.2) | [ ] |
| 2.5.5 | AAA | 터치 타겟 최소 44x44px | [ ] |
| 2.5.8 | AA | 터치 타겟 최소 24x24px (WCAG 2.2) | [ ] |

### 이해 가능 (Understandable)

| 기준 | Level | 설명 | 체크 |
|------|-------|------|------|
| 3.1.1 | A | 페이지 언어 명시 | [ ] |
| 3.2.1 | A | 포커스로 인한 예상치 못한 변화 없음 | [ ] |
| 3.2.2 | A | 입력으로 인한 예상치 못한 변화 없음 | [ ] |
| 3.3.1 | A | 오류 식별 | [ ] |
| 3.3.2 | A | 레이블 또는 지침 제공 | [ ] |
| 3.3.3 | AA | 오류 수정 제안 | [ ] |
| 3.3.8 | A | 접근 가능한 인증 (WCAG 2.2) | [ ] |

### 견고함 (Robust)

| 기준 | Level | 설명 | 체크 |
|------|-------|------|------|
| 4.1.2 | A | 컴포넌트 이름, 역할, 값 | [ ] |
| 4.1.3 | AA | 상태 메시지 프로그래밍적 전달 | [ ] |

---

## 2. 색상 대비 검증

### 대비율 기준

```
┌─────────────────────────────────────────────────────────────┐
│              Color Contrast Requirements                     │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│   일반 텍스트 (< 18pt / 14pt bold)                           │
│   ├── AA: 4.5:1 이상                                        │
│   └── AAA: 7:1 이상                                         │
│                                                              │
│   큰 텍스트 (>= 18pt / 14pt bold)                            │
│   ├── AA: 3:1 이상                                          │
│   └── AAA: 4.5:1 이상                                       │
│                                                              │
│   UI 컴포넌트 & 그래픽                                        │
│   └── AA: 3:1 이상                                          │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

### 대비율 계산 유틸리티

```typescript
// lib/accessibility/contrast.ts

/**
 * 상대 휘도 계산 (WCAG 2.1 공식)
 */
function getLuminance(color: string): number {
  const rgb = hexToRgb(color);
  const [r, g, b] = [rgb.r, rgb.g, rgb.b].map((c) => {
    const sRGB = c / 255;
    return sRGB <= 0.03928
      ? sRGB / 12.92
      : Math.pow((sRGB + 0.055) / 1.055, 2.4);
  });
  return 0.2126 * r + 0.7152 * g + 0.0722 * b;
}

/**
 * 대비율 계산
 */
function getContrastRatio(color1: string, color2: string): number {
  const l1 = getLuminance(color1);
  const l2 = getLuminance(color2);
  const lighter = Math.max(l1, l2);
  const darker = Math.min(l1, l2);
  return (lighter + 0.05) / (darker + 0.05);
}

/**
 * WCAG 레벨 확인
 */
function meetsWCAG(
  foreground: string,
  background: string,
  options: { level: 'AA' | 'AAA'; isLargeText?: boolean }
): boolean {
  const ratio = getContrastRatio(foreground, background);
  const { level, isLargeText = false } = options;

  if (level === 'AAA') {
    return isLargeText ? ratio >= 4.5 : ratio >= 7;
  }
  return isLargeText ? ratio >= 3 : ratio >= 4.5;
}

// 사용 예시
const isValid = meetsWCAG('#333333', '#ffffff', { level: 'AA' }); // true
const ratio = getContrastRatio('#666666', '#ffffff'); // 5.74
```

### Tailwind 색상 대비 확인

```typescript
// scripts/check-contrast.ts
const colorPairs = [
  { fg: 'hsl(var(--foreground))', bg: 'hsl(var(--background))', context: 'body text' },
  { fg: 'hsl(var(--primary-foreground))', bg: 'hsl(var(--primary))', context: 'primary button' },
  { fg: 'hsl(var(--muted-foreground))', bg: 'hsl(var(--background))', context: 'muted text' },
  { fg: 'hsl(var(--destructive-foreground))', bg: 'hsl(var(--destructive))', context: 'error button' },
];

// 최소 대비율 검증
colorPairs.forEach(({ fg, bg, context }) => {
  const ratio = getContrastRatio(fg, bg);
  const status = ratio >= 4.5 ? 'PASS' : 'FAIL';
  console.log(`[${status}] ${context}: ${ratio.toFixed(2)}:1`);
});
```

---

## 3. 키보드 네비게이션

### 포커스 관리 패턴

```tsx
// components/ui/focus-trap.tsx
'use client';

import { useRef, useEffect, type ReactNode } from 'react';

interface FocusTrapProps {
  children: ReactNode;
  active?: boolean;
  onEscape?: () => void;
}

export function FocusTrap({ children, active = true, onEscape }: FocusTrapProps) {
  const containerRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (!active) return;

    const container = containerRef.current;
    if (!container) return;

    const focusableElements = container.querySelectorAll<HTMLElement>(
      'button, [href], input, select, textarea, [tabindex]:not([tabindex="-1"])'
    );

    const firstElement = focusableElements[0];
    const lastElement = focusableElements[focusableElements.length - 1];

    // 첫 번째 요소에 포커스
    firstElement?.focus();

    const handleKeyDown = (e: KeyboardEvent) => {
      if (e.key === 'Escape' && onEscape) {
        onEscape();
        return;
      }

      if (e.key !== 'Tab') return;

      if (e.shiftKey) {
        if (document.activeElement === firstElement) {
          e.preventDefault();
          lastElement?.focus();
        }
      } else {
        if (document.activeElement === lastElement) {
          e.preventDefault();
          firstElement?.focus();
        }
      }
    };

    document.addEventListener('keydown', handleKeyDown);
    return () => document.removeEventListener('keydown', handleKeyDown);
  }, [active, onEscape]);

  return <div ref={containerRef}>{children}</div>;
}
```

### Skip Links

```tsx
// components/accessibility/skip-link.tsx
export function SkipLink() {
  return (
    <a
      href="#main-content"
      className="
        sr-only focus:not-sr-only
        focus:fixed focus:top-4 focus:left-4 focus:z-[9999]
        focus:px-4 focus:py-2 focus:bg-primary focus:text-primary-foreground
        focus:rounded-md focus:outline-none focus:ring-2 focus:ring-ring
      "
    >
      본문으로 건너뛰기
    </a>
  );
}

// app/layout.tsx
export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="ko">
      <body>
        <SkipLink />
        <header>...</header>
        <main id="main-content" tabIndex={-1}>
          {children}
        </main>
      </body>
    </html>
  );
}
```

### 포커스 스타일

```css
/* globals.css */

/* 기본 포커스 스타일 */
:focus-visible {
  outline: 2px solid hsl(var(--ring));
  outline-offset: 2px;
}

/* 커스텀 포커스 링 */
.focus-ring {
  @apply focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2;
}

/* 포커스가 가려지지 않도록 (WCAG 2.2 - 2.4.11) */
:focus-visible {
  scroll-margin: 8px;
}

/* 고대비 모드 지원 */
@media (prefers-contrast: more) {
  :focus-visible {
    outline-width: 3px;
  }
}
```

---

## 4. 스크린 리더 호환성

### ARIA 레이블 패턴

```tsx
// 아이콘 버튼
<Button aria-label="설정 열기">
  <Settings aria-hidden="true" />
</Button>

// 또는 sr-only 사용
<Button>
  <Settings aria-hidden="true" />
  <span className="sr-only">설정 열기</span>
</Button>

// 로딩 상태
<Button disabled aria-busy={isLoading}>
  {isLoading ? (
    <>
      <Spinner aria-hidden="true" />
      <span className="sr-only">로딩 중...</span>
    </>
  ) : (
    '저장'
  )}
</Button>

// 동적 영역 알림
<div role="status" aria-live="polite" aria-atomic="true">
  {message && <p>{message}</p>}
</div>

// 에러 메시지 연결
<div>
  <Label htmlFor="email">이메일</Label>
  <Input
    id="email"
    aria-describedby={error ? 'email-error' : undefined}
    aria-invalid={!!error}
  />
  {error && (
    <p id="email-error" role="alert" className="text-destructive text-sm">
      {error}
    </p>
  )}
</div>
```

### ARIA 역할 사용

```tsx
// 탭 패널
<div role="tablist" aria-label="계정 설정">
  <button
    role="tab"
    aria-selected={activeTab === 'profile'}
    aria-controls="profile-panel"
    id="profile-tab"
    tabIndex={activeTab === 'profile' ? 0 : -1}
  >
    프로필
  </button>
  <button
    role="tab"
    aria-selected={activeTab === 'security'}
    aria-controls="security-panel"
    id="security-tab"
    tabIndex={activeTab === 'security' ? 0 : -1}
  >
    보안
  </button>
</div>

<div
  role="tabpanel"
  id="profile-panel"
  aria-labelledby="profile-tab"
  hidden={activeTab !== 'profile'}
>
  프로필 콘텐츠
</div>

// 알림
<div role="alert" aria-live="assertive">
  긴급 알림 내용
</div>

// 상태 메시지
<div role="status" aria-live="polite">
  저장되었습니다
</div>

// 진행 표시
<div
  role="progressbar"
  aria-valuenow={75}
  aria-valuemin={0}
  aria-valuemax={100}
  aria-label="업로드 진행률"
>
  75%
</div>
```

### 시맨틱 HTML 우선

```tsx
// ❌ Bad: div로 만든 버튼
<div onClick={handleClick} className="btn">
  클릭
</div>

// ✅ Good: 네이티브 button
<button onClick={handleClick} className="btn">
  클릭
</button>

// ❌ Bad: div로 만든 리스트
<div className="list">
  <div className="item">항목 1</div>
  <div className="item">항목 2</div>
</div>

// ✅ Good: 시맨틱 ul/li
<ul className="list">
  <li className="item">항목 1</li>
  <li className="item">항목 2</li>
</ul>

// ❌ Bad: div 중첩
<div className="card">
  <div className="header">제목</div>
  <div className="body">내용</div>
</div>

// ✅ Good: article + heading
<article className="card">
  <h2 className="header">제목</h2>
  <p className="body">내용</p>
</article>
```

---

## 5. 신경다양성 고려사항

### ADHD 친화적 디자인

```css
/* 집중을 돕는 디자인 */

/* 중요한 정보 강조 */
.priority-high {
  border-left: 4px solid hsl(var(--primary));
  padding-left: 1rem;
}

/* 명확한 시각적 계층 */
.content-section {
  margin-bottom: 2rem;
  padding: 1.5rem;
  background: hsl(var(--card));
  border-radius: var(--radius);
}

/* 최소한의 애니메이션 (주의분산 방지) */
@media (prefers-reduced-motion: reduce) {
  *,
  *::before,
  *::after {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
  }
}

/* 진행 상태 표시 */
.progress-indicator {
  display: flex;
  gap: 0.5rem;
  align-items: center;
}

.progress-step {
  width: 2rem;
  height: 2rem;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
}

.progress-step.completed {
  background: hsl(var(--primary));
  color: hsl(var(--primary-foreground));
}

.progress-step.current {
  border: 2px solid hsl(var(--primary));
}
```

```tsx
// 명확한 상태 피드백
function SubmitButton({ isLoading, isSuccess }: { isLoading: boolean; isSuccess: boolean }) {
  return (
    <Button disabled={isLoading}>
      {isLoading && <Spinner className="mr-2" />}
      {isSuccess && <Check className="mr-2" />}
      {isLoading ? '저장 중...' : isSuccess ? '저장됨!' : '저장'}
    </Button>
  );
}

// 단계별 가이드
function OnboardingSteps({ currentStep }: { currentStep: number }) {
  const steps = ['프로필 설정', '관심사 선택', '완료'];

  return (
    <nav aria-label="온보딩 진행 상태">
      <ol className="flex gap-4">
        {steps.map((step, index) => (
          <li
            key={step}
            className={cn(
              'flex items-center gap-2',
              index < currentStep && 'text-primary',
              index === currentStep && 'font-bold',
              index > currentStep && 'text-muted-foreground'
            )}
            aria-current={index === currentStep ? 'step' : undefined}
          >
            <span className={cn(
              'w-8 h-8 rounded-full flex items-center justify-center',
              index <= currentStep ? 'bg-primary text-primary-foreground' : 'bg-muted'
            )}>
              {index < currentStep ? <Check size={16} /> : index + 1}
            </span>
            {step}
          </li>
        ))}
      </ol>
    </nav>
  );
}
```

### 자폐 스펙트럼 친화적 디자인

```tsx
// 예측 가능한 패턴
const NAVIGATION_ITEMS = [
  { href: '/dashboard', label: '대시보드', icon: LayoutDashboard },
  { href: '/projects', label: '프로젝트', icon: Folder },
  { href: '/settings', label: '설정', icon: Settings },
] as const;

// 일관된 네비게이션
function Sidebar() {
  const pathname = usePathname();

  return (
    <nav aria-label="주요 메뉴" className="space-y-1">
      {NAVIGATION_ITEMS.map(({ href, label, icon: Icon }) => (
        <Link
          key={href}
          href={href}
          className={cn(
            'flex items-center gap-3 px-3 py-2 rounded-md transition-colors',
            pathname === href
              ? 'bg-primary text-primary-foreground'
              : 'text-muted-foreground hover:bg-accent'
          )}
          aria-current={pathname === href ? 'page' : undefined}
        >
          <Icon size={20} aria-hidden="true" />
          {label}
        </Link>
      ))}
    </nav>
  );
}
```

```css
/* 감각 친화적 색상 */
:root {
  /* 부드러운 색상 팔레트 */
  --calm-blue: oklch(0.75 0.08 240);
  --calm-green: oklch(0.78 0.08 145);
  --calm-neutral: oklch(0.95 0.01 250);

  /* 자극적이지 않은 테두리 */
  --border: oklch(0.90 0.02 250);
}

/* 급격한 변화 방지 */
* {
  transition-timing-function: ease-in-out;
}

/* 패턴 일관성 */
.card, .dialog, .sheet {
  border-radius: var(--radius);
  border: 1px solid hsl(var(--border));
}
```

### 난독증 친화적 타이포그래피

```css
/* 난독증 친화적 폰트 설정 */
:root {
  /* 권장 폰트 */
  --font-dyslexic: 'Open Dyslexic', 'Lexie Readable', 'Comic Sans MS', sans-serif;

  /* 또는 일반적으로 읽기 쉬운 폰트 */
  --font-readable: 'Noto Sans KR', 'Satoshi', 'Source Sans 3', sans-serif;
}

/* 읽기 편한 텍스트 스타일 */
.readable-text {
  /* 줄 간격: 1.5~2.0 권장 */
  line-height: 1.8;

  /* 단어 간격 */
  word-spacing: 0.1em;

  /* 문자 간격 */
  letter-spacing: 0.02em;

  /* 단락 너비 제한 (60-70자) */
  max-width: 65ch;

  /* 양쪽 정렬 피하기 */
  text-align: left;
}

/* 본문 최소 폰트 크기 */
body {
  font-size: clamp(1rem, 2vw, 1.125rem);
}

/* 제목 대비 */
h1, h2, h3 {
  font-weight: 700;
  margin-bottom: 1em;
}

/* 링크 밑줄 유지 */
a {
  text-decoration: underline;
  text-underline-offset: 0.2em;
}
```

---

## 6. 모션 민감도

### prefers-reduced-motion 대응

```css
/* 모션 감소 선호 시 */
@media (prefers-reduced-motion: reduce) {
  *,
  *::before,
  *::after {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
    scroll-behavior: auto !important;
  }

  /* 로딩 스피너는 간단하게 */
  .spinner {
    animation: none;
    border-style: dotted;
  }
}

/* 일반 애니메이션 */
@media (prefers-reduced-motion: no-preference) {
  .fade-in {
    animation: fadeIn 0.3s ease-out;
  }

  .slide-up {
    animation: slideUp 0.3s ease-out;
  }
}

@keyframes fadeIn {
  from { opacity: 0; }
  to { opacity: 1; }
}

@keyframes slideUp {
  from { transform: translateY(10px); opacity: 0; }
  to { transform: translateY(0); opacity: 1; }
}
```

```tsx
// 모션 설정 훅
'use client';

import { useState, useEffect } from 'react';

export function useReducedMotion(): boolean {
  const [prefersReduced, setPrefersReduced] = useState(false);

  useEffect(() => {
    const mediaQuery = window.matchMedia('(prefers-reduced-motion: reduce)');
    setPrefersReduced(mediaQuery.matches);

    const handler = (e: MediaQueryListEvent) => setPrefersReduced(e.matches);
    mediaQuery.addEventListener('change', handler);
    return () => mediaQuery.removeEventListener('change', handler);
  }, []);

  return prefersReduced;
}

// 사용 예시
function AnimatedCard({ children }: { children: React.ReactNode }) {
  const reducedMotion = useReducedMotion();

  return (
    <motion.div
      initial={reducedMotion ? false : { opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={reducedMotion ? { duration: 0 } : { duration: 0.3 }}
    >
      {children}
    </motion.div>
  );
}
```

---

## 7. 폼 접근성

### 레이블과 에러 메시지

```tsx
// components/form/accessible-field.tsx
import { Label } from '@/components/ui/label';
import { Input } from '@/components/ui/input';

interface FieldProps {
  name: string;
  label: string;
  error?: string;
  hint?: string;
  required?: boolean;
}

export function AccessibleField({
  name,
  label,
  error,
  hint,
  required,
  ...props
}: FieldProps & React.ComponentProps<'input'>) {
  const inputId = `field-${name}`;
  const errorId = `${inputId}-error`;
  const hintId = `${inputId}-hint`;

  return (
    <div className="space-y-2">
      <Label htmlFor={inputId}>
        {label}
        {required && <span className="text-destructive ml-1" aria-hidden="true">*</span>}
        {required && <span className="sr-only">(필수)</span>}
      </Label>

      <Input
        id={inputId}
        name={name}
        aria-required={required}
        aria-invalid={!!error}
        aria-describedby={[
          hint ? hintId : '',
          error ? errorId : '',
        ].filter(Boolean).join(' ') || undefined}
        {...props}
      />

      {hint && !error && (
        <p id={hintId} className="text-sm text-muted-foreground">
          {hint}
        </p>
      )}

      {error && (
        <p id={errorId} role="alert" className="text-sm text-destructive">
          {error}
        </p>
      )}
    </div>
  );
}
```

### 폼 검증 안내

```tsx
// 실시간 검증 피드백
function PasswordField() {
  const [password, setPassword] = useState('');
  const [strength, setStrength] = useState<'weak' | 'medium' | 'strong'>('weak');

  const requirements = [
    { met: password.length >= 8, label: '8자 이상' },
    { met: /[A-Z]/.test(password), label: '대문자 포함' },
    { met: /[a-z]/.test(password), label: '소문자 포함' },
    { met: /[0-9]/.test(password), label: '숫자 포함' },
    { met: /[^A-Za-z0-9]/.test(password), label: '특수문자 포함' },
  ];

  return (
    <div className="space-y-2">
      <Label htmlFor="password">비밀번호</Label>
      <Input
        id="password"
        type="password"
        value={password}
        onChange={(e) => setPassword(e.target.value)}
        aria-describedby="password-requirements"
      />

      <div id="password-requirements" className="space-y-1">
        <p className="text-sm font-medium">비밀번호 요구사항:</p>
        <ul className="text-sm space-y-1">
          {requirements.map(({ met, label }) => (
            <li
              key={label}
              className={cn(
                'flex items-center gap-2',
                met ? 'text-green-600' : 'text-muted-foreground'
              )}
            >
              {met ? (
                <Check className="h-4 w-4" aria-hidden="true" />
              ) : (
                <X className="h-4 w-4" aria-hidden="true" />
              )}
              <span>{label}</span>
              <span className="sr-only">
                {met ? '충족됨' : '충족되지 않음'}
              </span>
            </li>
          ))}
        </ul>
      </div>
    </div>
  );
}
```

---

## 8. 에러 메시지 패턴

### 접근성 준수 에러 표시

```tsx
// 인라인 에러 메시지
function InlineError({ id, message }: { id: string; message: string }) {
  return (
    <div
      id={id}
      role="alert"
      className="flex items-center gap-2 text-sm text-destructive mt-1"
    >
      <AlertCircle className="h-4 w-4" aria-hidden="true" />
      {message}
    </div>
  );
}

// 폼 전체 에러 요약
function FormErrorSummary({ errors }: { errors: Record<string, string> }) {
  const errorList = Object.entries(errors);
  if (errorList.length === 0) return null;

  return (
    <div
      role="alert"
      aria-labelledby="error-summary-title"
      className="p-4 border border-destructive rounded-md mb-4"
    >
      <h2 id="error-summary-title" className="font-medium text-destructive mb-2">
        {errorList.length}개의 오류를 수정해주세요:
      </h2>
      <ul className="list-disc list-inside space-y-1 text-sm">
        {errorList.map(([field, message]) => (
          <li key={field}>
            <a href={`#field-${field}`} className="underline hover:no-underline">
              {message}
            </a>
          </li>
        ))}
      </ul>
    </div>
  );
}
```

### 토스트/알림 접근성

```tsx
// 접근 가능한 토스트
function AccessibleToast({ message, type }: { message: string; type: 'success' | 'error' | 'info' }) {
  return (
    <div
      role={type === 'error' ? 'alert' : 'status'}
      aria-live={type === 'error' ? 'assertive' : 'polite'}
      className={cn(
        'fixed bottom-4 right-4 p-4 rounded-md shadow-lg',
        type === 'success' && 'bg-green-600 text-white',
        type === 'error' && 'bg-destructive text-destructive-foreground',
        type === 'info' && 'bg-primary text-primary-foreground'
      )}
    >
      <p className="flex items-center gap-2">
        {type === 'success' && <Check aria-hidden="true" />}
        {type === 'error' && <AlertCircle aria-hidden="true" />}
        {type === 'info' && <Info aria-hidden="true" />}
        {message}
      </p>
    </div>
  );
}
```

---

## 9. 테스트 도구

### axe-core 자동 테스트

```typescript
// tests/accessibility.spec.ts
import { test, expect } from '@playwright/test';
import AxeBuilder from '@axe-core/playwright';

test.describe('Accessibility', () => {
  test('homepage should be accessible', async ({ page }) => {
    await page.goto('/');

    const results = await new AxeBuilder({ page })
      .withTags(['wcag2a', 'wcag2aa', 'wcag21aa', 'wcag22aa'])
      .analyze();

    expect(results.violations).toEqual([]);
  });

  test('form page should be accessible', async ({ page }) => {
    await page.goto('/contact');

    const results = await new AxeBuilder({ page })
      .include('#contact-form')
      .analyze();

    expect(results.violations).toEqual([]);
  });

  test('modal should trap focus', async ({ page }) => {
    await page.goto('/');
    await page.click('button:has-text("Open Modal")');

    // 모달 내 첫 요소에 포커스
    const firstFocusable = page.locator('[role="dialog"] button').first();
    await expect(firstFocusable).toBeFocused();

    // Tab으로 순환 확인
    await page.keyboard.press('Tab');
    await page.keyboard.press('Tab');
    await page.keyboard.press('Tab');

    // 마지막 요소 후 첫 요소로
    await expect(firstFocusable).toBeFocused();
  });
});
```

### 수동 테스트 체크리스트

```markdown
## 수동 접근성 테스트 체크리스트

### 키보드 테스트
- [ ] Tab 키로 모든 인터랙티브 요소 접근 가능
- [ ] Shift+Tab으로 역방향 이동 가능
- [ ] Enter/Space로 버튼, 링크 활성화 가능
- [ ] Escape로 모달/드롭다운 닫기 가능
- [ ] 화살표 키로 메뉴/탭 네비게이션 가능
- [ ] 포커스 순서가 논리적
- [ ] 포커스 표시가 명확하게 보임

### 스크린 리더 테스트
- [ ] 페이지 제목이 의미 있음
- [ ] 헤딩 구조가 논리적 (h1 → h2 → h3...)
- [ ] 이미지에 적절한 alt 텍스트
- [ ] 버튼/링크 레이블이 목적을 설명
- [ ] 폼 필드에 레이블 연결됨
- [ ] 에러 메시지가 읽힘
- [ ] 동적 콘텐츠 변경이 알림됨

### 색상/시각 테스트
- [ ] 색상만으로 정보 전달 안함
- [ ] 대비율 4.5:1 이상
- [ ] 200% 확대해도 레이아웃 유지
- [ ] 고대비 모드에서 정상 표시

### 모션 테스트
- [ ] prefers-reduced-motion 적용됨
- [ ] 깜빡이는 콘텐츠 없음 (3회/초 이하)
- [ ] 자동 재생 콘텐츠 제어 가능
```

---

## 10. 일반적인 문제 및 해결

### 문제: 색상만으로 상태 표시

```tsx
// ❌ Bad: 색상만으로 상태 구분
<span className={isValid ? 'text-green-500' : 'text-red-500'}>
  {value}
</span>

// ✅ Good: 색상 + 아이콘 + 텍스트
<span className={cn(
  'flex items-center gap-1',
  isValid ? 'text-green-600' : 'text-red-600'
)}>
  {isValid ? <Check aria-hidden="true" /> : <X aria-hidden="true" />}
  {value}
  <span className="sr-only">
    {isValid ? '(유효함)' : '(유효하지 않음)'}
  </span>
</span>
```

### 문제: 자동 재생 미디어

```tsx
// ❌ Bad: 자동 재생
<video autoPlay src="/intro.mp4" />

// ✅ Good: 사용자 제어 제공
<video
  src="/intro.mp4"
  controls
  aria-label="제품 소개 영상"
>
  <track
    kind="captions"
    src="/intro-captions.vtt"
    srcLang="ko"
    label="한국어"
    default
  />
</video>
```

### 문제: 시간 제한

```tsx
// ❌ Bad: 자동 타임아웃
useEffect(() => {
  const timer = setTimeout(() => logout(), 30000);
  return () => clearTimeout(timer);
}, []);

// ✅ Good: 사용자에게 경고 및 연장 옵션
function SessionTimeout() {
  const [showWarning, setShowWarning] = useState(false);

  return (
    <Dialog open={showWarning} onOpenChange={setShowWarning}>
      <DialogContent role="alertdialog" aria-labelledby="timeout-title">
        <DialogHeader>
          <DialogTitle id="timeout-title">세션 만료 예정</DialogTitle>
        </DialogHeader>
        <p>2분 후 자동으로 로그아웃됩니다.</p>
        <DialogFooter>
          <Button onClick={extendSession}>연장하기</Button>
          <Button variant="outline" onClick={logout}>로그아웃</Button>
        </DialogFooter>
      </DialogContent>
    </Dialog>
  );
}
```

---

## 도구 및 리소스

### 자동화 도구

| 도구 | 용도 | 링크 |
|------|------|------|
| **axe DevTools** | 브라우저 확장 | [axe DevTools](https://www.deque.com/axe/devtools/) |
| **WAVE** | 웹 접근성 평가 | [WAVE](https://wave.webaim.org/) |
| **Lighthouse** | Chrome 내장 감사 | Chrome DevTools |
| **axe-core** | 자동화 테스트 | [@axe-core/playwright](https://www.npmjs.com/package/@axe-core/playwright) |
| **Pa11y** | CLI 접근성 테스트 | [Pa11y](https://pa11y.org/) |

### 대비율 확인 도구

| 도구 | 설명 |
|------|------|
| **WebAIM Contrast Checker** | 웹 기반 대비율 계산 |
| **Colour Contrast Analyser** | 데스크톱 앱 |
| **Figma Contrast Plugin** | Figma 플러그인 |

### 스크린 리더 테스트

| 스크린 리더 | 플랫폼 |
|-------------|--------|
| **NVDA** | Windows (무료) |
| **JAWS** | Windows (유료) |
| **VoiceOver** | macOS/iOS (내장) |
| **TalkBack** | Android (내장) |

---

## 체크리스트 요약

### 개발 전
- [ ] 디자인에 접근성 고려 확인
- [ ] 색상 대비율 검증
- [ ] 키보드 네비게이션 계획

### 개발 중
- [ ] 시맨틱 HTML 사용
- [ ] ARIA 속성 적절히 사용
- [ ] 포커스 관리 구현
- [ ] 에러 메시지 접근성 확보

### 개발 후
- [ ] axe-core 자동 테스트 통과
- [ ] 스크린 리더 수동 테스트
- [ ] 키보드 전용 네비게이션 테스트
- [ ] 다양한 디바이스/브라우저 테스트

---

## References

- `_references/ACCESSIBILITY-CHECKLIST.md`
- `3-direction/SKILL.md` (디자인 방향 설정 시 접근성 고려)
- `5-color/SKILL.md` (색상 대비 검증)
