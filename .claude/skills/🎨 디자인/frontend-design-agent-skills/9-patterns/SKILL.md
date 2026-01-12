# Patterns Skill

복합 UI 패턴 (Molecules, Organisms) 설계 및 구현 스킬입니다.
Atomic Design의 조합 단계로, 재사용 가능한 복합 컴포넌트를 제공합니다.

## Triggers

- "패턴", "molecules", "organisms", "patterns"
- "카드 디자인", "모달", "드롭다운"
- "네비게이션", "사이드바", "탭"
- "폼 패턴", "테이블", "리스트"

---

## Input

| 항목 | 필수 | 설명 |
|------|------|------|
| `patternType` | ✅ | 패턴 유형 (card, modal, dropdown, nav, form, data-display) |
| `variant` | ❌ | 변형 스타일 |
| `interactive` | ❌ | 인터랙션 포함 여부 |
| `responsive` | ❌ | 반응형 동작 정의 |

---

## Card Variants

### Basic Card

```tsx
// components/ui/card.tsx (shadcn/ui 기본)
import * as React from 'react';
import { cn } from '@/lib/utils';

const Card = React.forwardRef<
  HTMLDivElement,
  React.HTMLAttributes<HTMLDivElement>
>(({ className, ...props }, ref) => (
  <div
    ref={ref}
    className={cn(
      'rounded-xl border bg-card text-card-foreground shadow-sm',
      className
    )}
    {...props}
  />
));
Card.displayName = 'Card';

const CardHeader = React.forwardRef<
  HTMLDivElement,
  React.HTMLAttributes<HTMLDivElement>
>(({ className, ...props }, ref) => (
  <div
    ref={ref}
    className={cn('flex flex-col space-y-1.5 p-6', className)}
    {...props}
  />
));
CardHeader.displayName = 'CardHeader';

const CardTitle = React.forwardRef<
  HTMLDivElement,
  React.HTMLAttributes<HTMLDivElement>
>(({ className, ...props }, ref) => (
  <div
    ref={ref}
    className={cn('font-semibold leading-none tracking-tight', className)}
    {...props}
  />
));
CardTitle.displayName = 'CardTitle';

const CardDescription = React.forwardRef<
  HTMLDivElement,
  React.HTMLAttributes<HTMLDivElement>
>(({ className, ...props }, ref) => (
  <div
    ref={ref}
    className={cn('text-sm text-muted-foreground', className)}
    {...props}
  />
));
CardDescription.displayName = 'CardDescription';

const CardContent = React.forwardRef<
  HTMLDivElement,
  React.HTMLAttributes<HTMLDivElement>
>(({ className, ...props }, ref) => (
  <div ref={ref} className={cn('p-6 pt-0', className)} {...props} />
));
CardContent.displayName = 'CardContent';

const CardFooter = React.forwardRef<
  HTMLDivElement,
  React.HTMLAttributes<HTMLDivElement>
>(({ className, ...props }, ref) => (
  <div
    ref={ref}
    className={cn('flex items-center p-6 pt-0', className)}
    {...props}
  />
));
CardFooter.displayName = 'CardFooter';

export { Card, CardHeader, CardFooter, CardTitle, CardDescription, CardContent };
```

### Interactive Card

```tsx
// components/molecules/interactive-card.tsx
'use client';

import * as React from 'react';
import Link from 'next/link';
import { motion } from 'framer-motion';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { cn } from '@/lib/utils';

interface InteractiveCardProps {
  href?: string;
  title: string;
  description?: string;
  badge?: string;
  image?: string;
  footer?: React.ReactNode;
  className?: string;
  onClick?: () => void;
}

export function InteractiveCard({
  href,
  title,
  description,
  badge,
  image,
  footer,
  className,
  onClick,
}: InteractiveCardProps) {
  const cardContent = (
    <motion.div
      whileHover={{ y: -4 }}
      whileTap={{ scale: 0.98 }}
      transition={{ type: 'spring', stiffness: 400, damping: 25 }}
    >
      <Card
        className={cn(
          'overflow-hidden transition-shadow hover:shadow-lg cursor-pointer',
          'focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring',
          className
        )}
        onClick={onClick}
        tabIndex={href ? -1 : 0}
        role={href ? undefined : 'button'}
      >
        {image && (
          <div className="aspect-video overflow-hidden">
            <img
              src={image}
              alt=""
              className="h-full w-full object-cover transition-transform duration-300 hover:scale-105"
            />
          </div>
        )}
        <CardHeader>
          <div className="flex items-start justify-between gap-2">
            <CardTitle className="text-lg">{title}</CardTitle>
            {badge && (
              <Badge variant="secondary" className="shrink-0">
                {badge}
              </Badge>
            )}
          </div>
          {description && (
            <CardDescription className="line-clamp-2">{description}</CardDescription>
          )}
        </CardHeader>
        {footer && <CardContent className="pt-0">{footer}</CardContent>}
      </Card>
    </motion.div>
  );

  if (href) {
    return (
      <Link href={href} className="block focus-visible:outline-none">
        {cardContent}
      </Link>
    );
  }

  return cardContent;
}
```

### Featured Card

```tsx
// components/molecules/featured-card.tsx
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { ArrowRight } from 'lucide-react';
import { cn } from '@/lib/utils';

interface FeaturedCardProps {
  title: string;
  description: string;
  icon?: React.ReactNode;
  gradient?: string;
  cta?: {
    label: string;
    onClick: () => void;
  };
  className?: string;
}

export function FeaturedCard({
  title,
  description,
  icon,
  gradient = 'from-primary/10 to-primary/5',
  cta,
  className,
}: FeaturedCardProps) {
  return (
    <Card className={cn('relative overflow-hidden', className)}>
      {/* Gradient Background */}
      <div
        className={cn(
          'absolute inset-0 bg-gradient-to-br opacity-50',
          gradient
        )}
        aria-hidden="true"
      />

      <CardHeader className="relative">
        {icon && (
          <div className="mb-4 inline-flex h-12 w-12 items-center justify-center rounded-lg bg-primary/10 text-primary">
            {icon}
          </div>
        )}
        <CardTitle className="text-xl">{title}</CardTitle>
        <CardDescription className="text-base">{description}</CardDescription>
      </CardHeader>

      {cta && (
        <CardContent className="relative pt-0">
          <Button
            variant="ghost"
            className="group -ml-4 text-primary hover:text-primary"
            onClick={cta.onClick}
          >
            {cta.label}
            <ArrowRight className="ml-2 h-4 w-4 transition-transform group-hover:translate-x-1" />
          </Button>
        </CardContent>
      )}
    </Card>
  );
}
```

### Stat Card

```tsx
// components/molecules/stat-card.tsx
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { cn } from '@/lib/utils';
import { TrendingDown, TrendingUp } from 'lucide-react';

interface StatCardProps {
  title: string;
  value: string | number;
  description?: string;
  trend?: {
    value: number;
    label?: string;
  };
  icon?: React.ReactNode;
  className?: string;
}

export function StatCard({
  title,
  value,
  description,
  trend,
  icon,
  className,
}: StatCardProps) {
  const isPositive = trend && trend.value >= 0;

  return (
    <Card className={className}>
      <CardHeader className="flex flex-row items-center justify-between pb-2">
        <CardTitle className="text-sm font-medium text-muted-foreground">
          {title}
        </CardTitle>
        {icon && <div className="text-muted-foreground">{icon}</div>}
      </CardHeader>
      <CardContent>
        <div className="text-2xl font-bold">{value}</div>
        {(description || trend) && (
          <div className="mt-1 flex items-center gap-2">
            {trend && (
              <span
                className={cn(
                  'flex items-center text-xs font-medium',
                  isPositive ? 'text-success' : 'text-destructive'
                )}
              >
                {isPositive ? (
                  <TrendingUp className="mr-0.5 h-3 w-3" />
                ) : (
                  <TrendingDown className="mr-0.5 h-3 w-3" />
                )}
                {Math.abs(trend.value)}%
              </span>
            )}
            <span className="text-xs text-muted-foreground">
              {trend?.label || description}
            </span>
          </div>
        )}
      </CardContent>
    </Card>
  );
}
```

---

## Modal/Dialog Patterns

### Dialog 기본 패턴

```tsx
// components/ui/dialog.tsx (shadcn/ui + 커스텀)
'use client';

import * as React from 'react';
import * as DialogPrimitive from '@radix-ui/react-dialog';
import { X } from 'lucide-react';
import { cn } from '@/lib/utils';

const Dialog = DialogPrimitive.Root;
const DialogTrigger = DialogPrimitive.Trigger;
const DialogPortal = DialogPrimitive.Portal;
const DialogClose = DialogPrimitive.Close;

const DialogOverlay = React.forwardRef<
  React.ElementRef<typeof DialogPrimitive.Overlay>,
  React.ComponentPropsWithoutRef<typeof DialogPrimitive.Overlay>
>(({ className, ...props }, ref) => (
  <DialogPrimitive.Overlay
    ref={ref}
    className={cn(
      'fixed inset-0 z-50 bg-black/80 data-[state=open]:animate-in data-[state=closed]:animate-out data-[state=closed]:fade-out-0 data-[state=open]:fade-in-0',
      className
    )}
    {...props}
  />
));
DialogOverlay.displayName = DialogPrimitive.Overlay.displayName;

const DialogContent = React.forwardRef<
  React.ElementRef<typeof DialogPrimitive.Content>,
  React.ComponentPropsWithoutRef<typeof DialogPrimitive.Content> & {
    size?: 'sm' | 'md' | 'lg' | 'xl' | 'full';
  }
>(({ className, children, size = 'md', ...props }, ref) => {
  const sizeClasses = {
    sm: 'max-w-sm',
    md: 'max-w-lg',
    lg: 'max-w-2xl',
    xl: 'max-w-4xl',
    full: 'max-w-[calc(100vw-2rem)] max-h-[calc(100vh-2rem)]',
  };

  return (
    <DialogPortal>
      <DialogOverlay />
      <DialogPrimitive.Content
        ref={ref}
        className={cn(
          'fixed left-[50%] top-[50%] z-50 grid w-full translate-x-[-50%] translate-y-[-50%] gap-4 border bg-background p-6 shadow-lg duration-200 data-[state=open]:animate-in data-[state=closed]:animate-out data-[state=closed]:fade-out-0 data-[state=open]:fade-in-0 data-[state=closed]:zoom-out-95 data-[state=open]:zoom-in-95 data-[state=closed]:slide-out-to-left-1/2 data-[state=closed]:slide-out-to-top-[48%] data-[state=open]:slide-in-from-left-1/2 data-[state=open]:slide-in-from-top-[48%] sm:rounded-lg',
          sizeClasses[size],
          className
        )}
        {...props}
      >
        {children}
        <DialogPrimitive.Close className="absolute right-4 top-4 rounded-sm opacity-70 ring-offset-background transition-opacity hover:opacity-100 focus:outline-none focus:ring-2 focus:ring-ring focus:ring-offset-2 disabled:pointer-events-none data-[state=open]:bg-accent data-[state=open]:text-muted-foreground">
          <X className="h-4 w-4" />
          <span className="sr-only">닫기</span>
        </DialogPrimitive.Close>
      </DialogPrimitive.Content>
    </DialogPortal>
  );
});
DialogContent.displayName = DialogPrimitive.Content.displayName;

const DialogHeader = ({
  className,
  ...props
}: React.HTMLAttributes<HTMLDivElement>) => (
  <div
    className={cn(
      'flex flex-col space-y-1.5 text-center sm:text-left',
      className
    )}
    {...props}
  />
);
DialogHeader.displayName = 'DialogHeader';

const DialogFooter = ({
  className,
  ...props
}: React.HTMLAttributes<HTMLDivElement>) => (
  <div
    className={cn(
      'flex flex-col-reverse sm:flex-row sm:justify-end sm:space-x-2',
      className
    )}
    {...props}
  />
);
DialogFooter.displayName = 'DialogFooter';

const DialogTitle = React.forwardRef<
  React.ElementRef<typeof DialogPrimitive.Title>,
  React.ComponentPropsWithoutRef<typeof DialogPrimitive.Title>
>(({ className, ...props }, ref) => (
  <DialogPrimitive.Title
    ref={ref}
    className={cn(
      'text-lg font-semibold leading-none tracking-tight',
      className
    )}
    {...props}
  />
));
DialogTitle.displayName = DialogPrimitive.Title.displayName;

const DialogDescription = React.forwardRef<
  React.ElementRef<typeof DialogPrimitive.Description>,
  React.ComponentPropsWithoutRef<typeof DialogPrimitive.Description>
>(({ className, ...props }, ref) => (
  <DialogPrimitive.Description
    ref={ref}
    className={cn('text-sm text-muted-foreground', className)}
    {...props}
  />
));
DialogDescription.displayName = DialogPrimitive.Description.displayName;

export {
  Dialog,
  DialogPortal,
  DialogOverlay,
  DialogTrigger,
  DialogClose,
  DialogContent,
  DialogHeader,
  DialogFooter,
  DialogTitle,
  DialogDescription,
};
```

### Confirmation Dialog

```tsx
// components/organisms/confirmation-dialog.tsx
'use client';

import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
} from '@/components/ui/dialog';
import { Button } from '@/components/ui/button';
import { AlertTriangle, Info, CheckCircle } from 'lucide-react';
import { cn } from '@/lib/utils';

type DialogType = 'info' | 'warning' | 'success' | 'destructive';

interface ConfirmationDialogProps {
  open: boolean;
  onOpenChange: (open: boolean) => void;
  title: string;
  description?: string;
  type?: DialogType;
  confirmLabel?: string;
  cancelLabel?: string;
  onConfirm: () => void | Promise<void>;
  loading?: boolean;
}

const typeConfig: Record<DialogType, { icon: React.ReactNode; buttonVariant: 'default' | 'destructive' }> = {
  info: {
    icon: <Info className="h-6 w-6 text-info" />,
    buttonVariant: 'default',
  },
  warning: {
    icon: <AlertTriangle className="h-6 w-6 text-warning" />,
    buttonVariant: 'default',
  },
  success: {
    icon: <CheckCircle className="h-6 w-6 text-success" />,
    buttonVariant: 'default',
  },
  destructive: {
    icon: <AlertTriangle className="h-6 w-6 text-destructive" />,
    buttonVariant: 'destructive',
  },
};

export function ConfirmationDialog({
  open,
  onOpenChange,
  title,
  description,
  type = 'info',
  confirmLabel = '확인',
  cancelLabel = '취소',
  onConfirm,
  loading = false,
}: ConfirmationDialogProps) {
  const config = typeConfig[type];

  const handleConfirm = async () => {
    await onConfirm();
    onOpenChange(false);
  };

  return (
    <Dialog open={open} onOpenChange={onOpenChange}>
      <DialogContent size="sm">
        <DialogHeader>
          <div className="flex items-center gap-3">
            {config.icon}
            <DialogTitle>{title}</DialogTitle>
          </div>
          {description && <DialogDescription>{description}</DialogDescription>}
        </DialogHeader>
        <DialogFooter className="gap-2 sm:gap-0">
          <Button variant="outline" onClick={() => onOpenChange(false)} disabled={loading}>
            {cancelLabel}
          </Button>
          <Button
            variant={config.buttonVariant}
            onClick={handleConfirm}
            loading={loading}
          >
            {confirmLabel}
          </Button>
        </DialogFooter>
      </DialogContent>
    </Dialog>
  );
}
```

---

## Dropdown/Select Patterns

### Dropdown Menu

```tsx
// components/ui/dropdown-menu.tsx (shadcn/ui 기본 + 커스텀)
'use client';

import * as React from 'react';
import * as DropdownMenuPrimitive from '@radix-ui/react-dropdown-menu';
import { Check, ChevronRight, Circle } from 'lucide-react';
import { cn } from '@/lib/utils';

const DropdownMenu = DropdownMenuPrimitive.Root;
const DropdownMenuTrigger = DropdownMenuPrimitive.Trigger;
const DropdownMenuGroup = DropdownMenuPrimitive.Group;
const DropdownMenuPortal = DropdownMenuPrimitive.Portal;
const DropdownMenuSub = DropdownMenuPrimitive.Sub;
const DropdownMenuRadioGroup = DropdownMenuPrimitive.RadioGroup;

const DropdownMenuContent = React.forwardRef<
  React.ElementRef<typeof DropdownMenuPrimitive.Content>,
  React.ComponentPropsWithoutRef<typeof DropdownMenuPrimitive.Content>
>(({ className, sideOffset = 4, ...props }, ref) => (
  <DropdownMenuPrimitive.Portal>
    <DropdownMenuPrimitive.Content
      ref={ref}
      sideOffset={sideOffset}
      className={cn(
        'z-50 min-w-[8rem] overflow-hidden rounded-md border bg-popover p-1 text-popover-foreground shadow-md',
        'data-[state=open]:animate-in data-[state=closed]:animate-out data-[state=closed]:fade-out-0 data-[state=open]:fade-in-0 data-[state=closed]:zoom-out-95 data-[state=open]:zoom-in-95 data-[side=bottom]:slide-in-from-top-2 data-[side=left]:slide-in-from-right-2 data-[side=right]:slide-in-from-left-2 data-[side=top]:slide-in-from-bottom-2',
        className
      )}
      {...props}
    />
  </DropdownMenuPrimitive.Portal>
));
DropdownMenuContent.displayName = DropdownMenuPrimitive.Content.displayName;

const DropdownMenuItem = React.forwardRef<
  React.ElementRef<typeof DropdownMenuPrimitive.Item>,
  React.ComponentPropsWithoutRef<typeof DropdownMenuPrimitive.Item> & {
    inset?: boolean;
    destructive?: boolean;
  }
>(({ className, inset, destructive, ...props }, ref) => (
  <DropdownMenuPrimitive.Item
    ref={ref}
    className={cn(
      'relative flex cursor-default select-none items-center gap-2 rounded-sm px-2 py-1.5 text-sm outline-none transition-colors focus:bg-accent focus:text-accent-foreground data-[disabled]:pointer-events-none data-[disabled]:opacity-50 [&>svg]:size-4 [&>svg]:shrink-0',
      inset && 'pl-8',
      destructive && 'text-destructive focus:bg-destructive/10 focus:text-destructive',
      className
    )}
    {...props}
  />
));
DropdownMenuItem.displayName = DropdownMenuPrimitive.Item.displayName;

const DropdownMenuSeparator = React.forwardRef<
  React.ElementRef<typeof DropdownMenuPrimitive.Separator>,
  React.ComponentPropsWithoutRef<typeof DropdownMenuPrimitive.Separator>
>(({ className, ...props }, ref) => (
  <DropdownMenuPrimitive.Separator
    ref={ref}
    className={cn('-mx-1 my-1 h-px bg-muted', className)}
    {...props}
  />
));
DropdownMenuSeparator.displayName = DropdownMenuPrimitive.Separator.displayName;

const DropdownMenuLabel = React.forwardRef<
  React.ElementRef<typeof DropdownMenuPrimitive.Label>,
  React.ComponentPropsWithoutRef<typeof DropdownMenuPrimitive.Label> & {
    inset?: boolean;
  }
>(({ className, inset, ...props }, ref) => (
  <DropdownMenuPrimitive.Label
    ref={ref}
    className={cn(
      'px-2 py-1.5 text-sm font-semibold',
      inset && 'pl-8',
      className
    )}
    {...props}
  />
));
DropdownMenuLabel.displayName = DropdownMenuPrimitive.Label.displayName;

export {
  DropdownMenu,
  DropdownMenuTrigger,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuSeparator,
  DropdownMenuLabel,
  DropdownMenuGroup,
  DropdownMenuPortal,
  DropdownMenuSub,
  DropdownMenuRadioGroup,
};
```

### User Menu Pattern

```tsx
// components/organisms/user-menu.tsx
'use client';

import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuGroup,
  DropdownMenuItem,
  DropdownMenuLabel,
  DropdownMenuSeparator,
  DropdownMenuTrigger,
} from '@/components/ui/dropdown-menu';
import { Avatar, AvatarFallback, AvatarImage } from '@/components/ui/avatar';
import { Button } from '@/components/ui/button';
import { User, Settings, CreditCard, LogOut, HelpCircle } from 'lucide-react';

interface UserMenuProps {
  user: {
    name: string;
    email: string;
    avatarUrl?: string;
  };
  onLogout: () => void;
}

export function UserMenu({ user, onLogout }: UserMenuProps) {
  const initials = user.name
    .split(' ')
    .map((n) => n[0])
    .join('')
    .toUpperCase()
    .slice(0, 2);

  return (
    <DropdownMenu>
      <DropdownMenuTrigger asChild>
        <Button variant="ghost" className="relative h-8 w-8 rounded-full">
          <Avatar className="h-8 w-8">
            <AvatarImage src={user.avatarUrl} alt={user.name} />
            <AvatarFallback>{initials}</AvatarFallback>
          </Avatar>
        </Button>
      </DropdownMenuTrigger>
      <DropdownMenuContent className="w-56" align="end" forceMount>
        <DropdownMenuLabel className="font-normal">
          <div className="flex flex-col space-y-1">
            <p className="text-sm font-medium leading-none">{user.name}</p>
            <p className="text-xs leading-none text-muted-foreground">{user.email}</p>
          </div>
        </DropdownMenuLabel>
        <DropdownMenuSeparator />
        <DropdownMenuGroup>
          <DropdownMenuItem>
            <User className="mr-2 h-4 w-4" />
            <span>프로필</span>
          </DropdownMenuItem>
          <DropdownMenuItem>
            <CreditCard className="mr-2 h-4 w-4" />
            <span>결제 정보</span>
          </DropdownMenuItem>
          <DropdownMenuItem>
            <Settings className="mr-2 h-4 w-4" />
            <span>설정</span>
          </DropdownMenuItem>
        </DropdownMenuGroup>
        <DropdownMenuSeparator />
        <DropdownMenuItem>
          <HelpCircle className="mr-2 h-4 w-4" />
          <span>도움말</span>
        </DropdownMenuItem>
        <DropdownMenuSeparator />
        <DropdownMenuItem destructive onClick={onLogout}>
          <LogOut className="mr-2 h-4 w-4" />
          <span>로그아웃</span>
        </DropdownMenuItem>
      </DropdownMenuContent>
    </DropdownMenu>
  );
}
```

---

## Navigation Patterns

### Navbar

```tsx
// components/organisms/navbar.tsx
'use client';

import * as React from 'react';
import Link from 'next/link';
import { usePathname } from 'next/navigation';
import { Menu, X } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Sheet, SheetContent, SheetTrigger } from '@/components/ui/sheet';
import { cn } from '@/lib/utils';

interface NavItem {
  label: string;
  href: string;
}

interface NavbarProps {
  logo: React.ReactNode;
  items: NavItem[];
  actions?: React.ReactNode;
}

export function Navbar({ logo, items, actions }: NavbarProps) {
  const pathname = usePathname();
  const [mobileOpen, setMobileOpen] = React.useState(false);

  return (
    <header className="sticky top-0 z-50 w-full border-b bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/60">
      <nav className="container flex h-16 items-center justify-between">
        {/* Logo */}
        <Link href="/" className="flex items-center">
          {logo}
        </Link>

        {/* Desktop Navigation */}
        <div className="hidden md:flex md:items-center md:gap-6">
          {items.map((item) => (
            <Link
              key={item.href}
              href={item.href}
              className={cn(
                'text-sm font-medium transition-colors hover:text-primary',
                pathname === item.href
                  ? 'text-foreground'
                  : 'text-muted-foreground'
              )}
            >
              {item.label}
            </Link>
          ))}
        </div>

        {/* Actions */}
        <div className="flex items-center gap-4">
          <div className="hidden md:flex md:items-center md:gap-2">
            {actions}
          </div>

          {/* Mobile Menu */}
          <Sheet open={mobileOpen} onOpenChange={setMobileOpen}>
            <SheetTrigger asChild className="md:hidden">
              <Button variant="ghost" size="icon">
                <Menu className="h-5 w-5" />
                <span className="sr-only">메뉴 열기</span>
              </Button>
            </SheetTrigger>
            <SheetContent side="right" className="w-[300px] sm:w-[400px]">
              <nav className="flex flex-col gap-4">
                {items.map((item) => (
                  <Link
                    key={item.href}
                    href={item.href}
                    onClick={() => setMobileOpen(false)}
                    className={cn(
                      'block px-2 py-1 text-lg font-medium',
                      pathname === item.href
                        ? 'text-foreground'
                        : 'text-muted-foreground'
                    )}
                  >
                    {item.label}
                  </Link>
                ))}
                <div className="border-t pt-4">{actions}</div>
              </nav>
            </SheetContent>
          </Sheet>
        </div>
      </nav>
    </header>
  );
}
```

### Sidebar Navigation

```tsx
// components/organisms/sidebar.tsx
'use client';

import * as React from 'react';
import Link from 'next/link';
import { usePathname } from 'next/navigation';
import { ChevronDown, ChevronRight, LucideIcon } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { ScrollArea } from '@/components/ui/scroll-area';
import { Collapsible, CollapsibleContent, CollapsibleTrigger } from '@/components/ui/collapsible';
import { cn } from '@/lib/utils';

interface NavGroup {
  label: string;
  items: NavItem[];
}

interface NavItem {
  label: string;
  href: string;
  icon?: LucideIcon;
  badge?: string;
  children?: NavItem[];
}

interface SidebarProps {
  groups: NavGroup[];
  footer?: React.ReactNode;
}

export function Sidebar({ groups, footer }: SidebarProps) {
  const pathname = usePathname();

  return (
    <aside className="fixed inset-y-0 left-0 z-30 hidden w-64 border-r bg-background md:block">
      <ScrollArea className="h-full py-6">
        <div className="space-y-6 px-3">
          {groups.map((group) => (
            <div key={group.label}>
              <h4 className="mb-2 px-4 text-xs font-semibold uppercase tracking-wider text-muted-foreground">
                {group.label}
              </h4>
              <nav className="space-y-1">
                {group.items.map((item) => (
                  <NavLink key={item.href} item={item} pathname={pathname} />
                ))}
              </nav>
            </div>
          ))}
        </div>
      </ScrollArea>
      {footer && (
        <div className="absolute bottom-0 left-0 right-0 border-t p-4">
          {footer}
        </div>
      )}
    </aside>
  );
}

function NavLink({ item, pathname }: { item: NavItem; pathname: string }) {
  const isActive = pathname === item.href || pathname.startsWith(item.href + '/');
  const hasChildren = item.children && item.children.length > 0;
  const [open, setOpen] = React.useState(isActive);

  if (hasChildren) {
    return (
      <Collapsible open={open} onOpenChange={setOpen}>
        <CollapsibleTrigger asChild>
          <Button
            variant="ghost"
            className={cn(
              'w-full justify-between',
              isActive && 'bg-accent'
            )}
          >
            <span className="flex items-center gap-2">
              {item.icon && <item.icon className="h-4 w-4" />}
              {item.label}
            </span>
            {open ? (
              <ChevronDown className="h-4 w-4" />
            ) : (
              <ChevronRight className="h-4 w-4" />
            )}
          </Button>
        </CollapsibleTrigger>
        <CollapsibleContent className="pl-6 pt-1 space-y-1">
          {item.children?.map((child) => (
            <NavLink key={child.href} item={child} pathname={pathname} />
          ))}
        </CollapsibleContent>
      </Collapsible>
    );
  }

  return (
    <Button
      variant="ghost"
      className={cn(
        'w-full justify-start gap-2',
        isActive && 'bg-accent text-accent-foreground'
      )}
      asChild
    >
      <Link href={item.href}>
        {item.icon && <item.icon className="h-4 w-4" />}
        <span className="flex-1 text-left">{item.label}</span>
        {item.badge && (
          <span className="rounded-full bg-primary/10 px-2 py-0.5 text-xs text-primary">
            {item.badge}
          </span>
        )}
      </Link>
    </Button>
  );
}
```

### Tabs Navigation

```tsx
// components/ui/tabs.tsx (shadcn/ui + 커스텀)
'use client';

import * as React from 'react';
import * as TabsPrimitive from '@radix-ui/react-tabs';
import { cn } from '@/lib/utils';

const Tabs = TabsPrimitive.Root;

const TabsList = React.forwardRef<
  React.ElementRef<typeof TabsPrimitive.List>,
  React.ComponentPropsWithoutRef<typeof TabsPrimitive.List> & {
    variant?: 'default' | 'underline' | 'pills';
  }
>(({ className, variant = 'default', ...props }, ref) => (
  <TabsPrimitive.List
    ref={ref}
    className={cn(
      'inline-flex items-center justify-center',
      variant === 'default' && 'h-9 rounded-lg bg-muted p-1 text-muted-foreground',
      variant === 'underline' && 'h-10 border-b gap-4',
      variant === 'pills' && 'gap-2',
      className
    )}
    {...props}
  />
));
TabsList.displayName = TabsPrimitive.List.displayName;

const TabsTrigger = React.forwardRef<
  React.ElementRef<typeof TabsPrimitive.Trigger>,
  React.ComponentPropsWithoutRef<typeof TabsPrimitive.Trigger> & {
    variant?: 'default' | 'underline' | 'pills';
  }
>(({ className, variant = 'default', ...props }, ref) => (
  <TabsPrimitive.Trigger
    ref={ref}
    className={cn(
      'inline-flex items-center justify-center whitespace-nowrap text-sm font-medium ring-offset-background transition-all focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:pointer-events-none disabled:opacity-50',
      variant === 'default' &&
        'rounded-md px-3 py-1 data-[state=active]:bg-background data-[state=active]:text-foreground data-[state=active]:shadow',
      variant === 'underline' &&
        'border-b-2 border-transparent px-4 pb-3 pt-2 data-[state=active]:border-primary data-[state=active]:text-foreground text-muted-foreground',
      variant === 'pills' &&
        'rounded-full border px-4 py-1.5 data-[state=active]:bg-primary data-[state=active]:text-primary-foreground data-[state=active]:border-primary',
      className
    )}
    {...props}
  />
));
TabsTrigger.displayName = TabsPrimitive.Trigger.displayName;

const TabsContent = React.forwardRef<
  React.ElementRef<typeof TabsPrimitive.Content>,
  React.ComponentPropsWithoutRef<typeof TabsPrimitive.Content>
>(({ className, ...props }, ref) => (
  <TabsPrimitive.Content
    ref={ref}
    className={cn(
      'mt-2 ring-offset-background focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2',
      className
    )}
    {...props}
  />
));
TabsContent.displayName = TabsPrimitive.Content.displayName;

export { Tabs, TabsList, TabsTrigger, TabsContent };
```

---

## Form Patterns

### Labeled Input

```tsx
// components/molecules/labeled-input.tsx
import * as React from 'react';
import { Label } from '@/components/ui/label';
import { Input } from '@/components/ui/input';
import { cn } from '@/lib/utils';

interface LabeledInputProps extends React.InputHTMLAttributes<HTMLInputElement> {
  label: string;
  error?: string;
  hint?: string;
  required?: boolean;
}

const LabeledInput = React.forwardRef<HTMLInputElement, LabeledInputProps>(
  ({ label, error, hint, required, className, id, ...props }, ref) => {
    const inputId = id || props.name;
    const errorId = `${inputId}-error`;
    const hintId = `${inputId}-hint`;

    return (
      <div className="space-y-2">
        <Label
          htmlFor={inputId}
          className={cn(error && 'text-destructive')}
        >
          {label}
          {required && <span className="text-destructive ml-1">*</span>}
        </Label>
        <Input
          id={inputId}
          ref={ref}
          className={cn(error && 'border-destructive', className)}
          aria-invalid={!!error}
          aria-describedby={
            error ? errorId : hint ? hintId : undefined
          }
          {...props}
        />
        {hint && !error && (
          <p id={hintId} className="text-sm text-muted-foreground">
            {hint}
          </p>
        )}
        {error && (
          <p id={errorId} className="text-sm text-destructive" role="alert">
            {error}
          </p>
        )}
      </div>
    );
  }
);
LabeledInput.displayName = 'LabeledInput';

export { LabeledInput };
```

### Form Group

```tsx
// components/molecules/form-group.tsx
import { cn } from '@/lib/utils';

interface FormGroupProps {
  children: React.ReactNode;
  label?: string;
  description?: string;
  error?: string;
  className?: string;
}

export function FormGroup({
  children,
  label,
  description,
  error,
  className,
}: FormGroupProps) {
  return (
    <fieldset className={cn('space-y-3', className)}>
      {label && (
        <legend className="text-base font-medium">{label}</legend>
      )}
      {description && (
        <p className="text-sm text-muted-foreground">{description}</p>
      )}
      <div className="space-y-4">{children}</div>
      {error && (
        <p className="text-sm text-destructive" role="alert">
          {error}
        </p>
      )}
    </fieldset>
  );
}
```

---

## Data Display Patterns

### Data Table

```tsx
// components/organisms/data-table.tsx
'use client';

import * as React from 'react';
import {
  ColumnDef,
  flexRender,
  getCoreRowModel,
  useReactTable,
  getPaginationRowModel,
  getSortedRowModel,
  SortingState,
  getFilteredRowModel,
  ColumnFiltersState,
} from '@tanstack/react-table';
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from '@/components/ui/table';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { ChevronLeft, ChevronRight, Search } from 'lucide-react';

interface DataTableProps<TData, TValue> {
  columns: ColumnDef<TData, TValue>[];
  data: TData[];
  searchKey?: string;
  searchPlaceholder?: string;
}

export function DataTable<TData, TValue>({
  columns,
  data,
  searchKey,
  searchPlaceholder = '검색...',
}: DataTableProps<TData, TValue>) {
  const [sorting, setSorting] = React.useState<SortingState>([]);
  const [columnFilters, setColumnFilters] = React.useState<ColumnFiltersState>([]);

  const table = useReactTable({
    data,
    columns,
    getCoreRowModel: getCoreRowModel(),
    getPaginationRowModel: getPaginationRowModel(),
    onSortingChange: setSorting,
    getSortedRowModel: getSortedRowModel(),
    onColumnFiltersChange: setColumnFilters,
    getFilteredRowModel: getFilteredRowModel(),
    state: {
      sorting,
      columnFilters,
    },
  });

  return (
    <div className="space-y-4">
      {/* Toolbar */}
      {searchKey && (
        <div className="flex items-center gap-2">
          <div className="relative flex-1 max-w-sm">
            <Search className="absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-muted-foreground" />
            <Input
              placeholder={searchPlaceholder}
              value={(table.getColumn(searchKey)?.getFilterValue() as string) ?? ''}
              onChange={(event) =>
                table.getColumn(searchKey)?.setFilterValue(event.target.value)
              }
              className="pl-9"
            />
          </div>
        </div>
      )}

      {/* Table */}
      <div className="rounded-md border">
        <Table>
          <TableHeader>
            {table.getHeaderGroups().map((headerGroup) => (
              <TableRow key={headerGroup.id}>
                {headerGroup.headers.map((header) => (
                  <TableHead key={header.id}>
                    {header.isPlaceholder
                      ? null
                      : flexRender(
                          header.column.columnDef.header,
                          header.getContext()
                        )}
                  </TableHead>
                ))}
              </TableRow>
            ))}
          </TableHeader>
          <TableBody>
            {table.getRowModel().rows?.length ? (
              table.getRowModel().rows.map((row) => (
                <TableRow
                  key={row.id}
                  data-state={row.getIsSelected() && 'selected'}
                >
                  {row.getVisibleCells().map((cell) => (
                    <TableCell key={cell.id}>
                      {flexRender(cell.column.columnDef.cell, cell.getContext())}
                    </TableCell>
                  ))}
                </TableRow>
              ))
            ) : (
              <TableRow>
                <TableCell colSpan={columns.length} className="h-24 text-center">
                  데이터가 없습니다.
                </TableCell>
              </TableRow>
            )}
          </TableBody>
        </Table>
      </div>

      {/* Pagination */}
      <div className="flex items-center justify-between">
        <p className="text-sm text-muted-foreground">
          총 {table.getFilteredRowModel().rows.length}개 중{' '}
          {table.getState().pagination.pageIndex * table.getState().pagination.pageSize + 1}-
          {Math.min(
            (table.getState().pagination.pageIndex + 1) * table.getState().pagination.pageSize,
            table.getFilteredRowModel().rows.length
          )}
          개 표시
        </p>
        <div className="flex items-center gap-2">
          <Button
            variant="outline"
            size="sm"
            onClick={() => table.previousPage()}
            disabled={!table.getCanPreviousPage()}
          >
            <ChevronLeft className="h-4 w-4" />
            이전
          </Button>
          <Button
            variant="outline"
            size="sm"
            onClick={() => table.nextPage()}
            disabled={!table.getCanNextPage()}
          >
            다음
            <ChevronRight className="h-4 w-4" />
          </Button>
        </div>
      </div>
    </div>
  );
}
```

### List Component

```tsx
// components/molecules/item-list.tsx
import * as React from 'react';
import { cn } from '@/lib/utils';

interface ListProps<T> {
  items: T[];
  renderItem: (item: T, index: number) => React.ReactNode;
  keyExtractor: (item: T, index: number) => string;
  emptyState?: React.ReactNode;
  className?: string;
  divided?: boolean;
}

export function ItemList<T>({
  items,
  renderItem,
  keyExtractor,
  emptyState,
  className,
  divided = false,
}: ListProps<T>) {
  if (items.length === 0 && emptyState) {
    return <>{emptyState}</>;
  }

  return (
    <ul className={cn(divided && 'divide-y', className)} role="list">
      {items.map((item, index) => (
        <li key={keyExtractor(item, index)}>{renderItem(item, index)}</li>
      ))}
    </ul>
  );
}
```

### Grid Layout

```tsx
// components/molecules/responsive-grid.tsx
import { cn } from '@/lib/utils';

interface ResponsiveGridProps {
  children: React.ReactNode;
  columns?: {
    default?: number;
    sm?: number;
    md?: number;
    lg?: number;
    xl?: number;
  };
  gap?: 'none' | 'sm' | 'md' | 'lg';
  className?: string;
}

export function ResponsiveGrid({
  children,
  columns = { default: 1, sm: 2, lg: 3 },
  gap = 'md',
  className,
}: ResponsiveGridProps) {
  const gapClasses = {
    none: 'gap-0',
    sm: 'gap-2',
    md: 'gap-4',
    lg: 'gap-6',
  };

  const colClasses = [
    columns.default && `grid-cols-${columns.default}`,
    columns.sm && `sm:grid-cols-${columns.sm}`,
    columns.md && `md:grid-cols-${columns.md}`,
    columns.lg && `lg:grid-cols-${columns.lg}`,
    columns.xl && `xl:grid-cols-${columns.xl}`,
  ].filter(Boolean);

  return (
    <div
      className={cn(
        'grid',
        gapClasses[gap],
        ...colClasses,
        className
      )}
    >
      {children}
    </div>
  );
}
```

---

## Accessibility Considerations

### Dialog 접근성

```tsx
// Dialog 필수 패턴
<Dialog>
  <DialogTrigger>열기</DialogTrigger>
  <DialogContent>
    <DialogHeader>
      <DialogTitle>제목 필수</DialogTitle>  {/* aria-labelledby 연결 */}
      <DialogDescription>설명 권장</DialogDescription>  {/* aria-describedby 연결 */}
    </DialogHeader>
    {/* 내용 */}
  </DialogContent>
</Dialog>
```

### Navigation 접근성

```tsx
// 현재 페이지 표시
<Link
  href="/dashboard"
  aria-current={pathname === '/dashboard' ? 'page' : undefined}
>
  대시보드
</Link>

// 모바일 메뉴 상태
<Button
  aria-expanded={isOpen}
  aria-controls="mobile-menu"
  aria-label="메뉴 열기"
>
  <Menu />
</Button>
```

---

## Anti-Patterns

### 1. 중첩 버튼

```tsx
// ❌ Bad: 버튼 안에 버튼 (접근성 위반)
<Button>
  외부 버튼
  <button onClick={handleInner}>내부 버튼</button>
</Button>

// ✅ Good: 별도 배치
<div className="flex gap-2">
  <Button>외부 버튼</Button>
  <Button onClick={handleInner}>내부 버튼</Button>
</div>
```

### 2. 제목 없는 Dialog

```tsx
// ❌ Bad: DialogTitle 누락
<DialogContent>
  <p>내용만 있음</p>
</DialogContent>

// ✅ Good: 제목 포함
<DialogContent>
  <DialogHeader>
    <DialogTitle>알림</DialogTitle>
  </DialogHeader>
  <p>내용</p>
</DialogContent>
```

### 3. 키보드 트랩

```tsx
// ❌ Bad: ESC로 닫을 수 없는 모달
<Dialog open={true} onOpenChange={() => {}}>
  {/* 닫기 불가 */}
</Dialog>

// ✅ Good: ESC, 배경 클릭, 닫기 버튼 모두 작동
<Dialog open={open} onOpenChange={setOpen}>
  {/* 자연스러운 닫기 */}
</Dialog>
```

---

## References

- `_references/COMPONENT-PATTERN.md`
- `8-primitives/SKILL.md` (Atoms 컴포넌트)
- shadcn/ui 공식 문서: https://ui.shadcn.com/
- Radix UI Primitives: https://www.radix-ui.com/
