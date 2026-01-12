# Dashboard Design Skill

대시보드 및 SaaS 관리자 UI 디자인을 위한 종합 스킬입니다.

## Triggers

- "대시보드", "dashboard", "SaaS", "관리자", "admin", "백오피스"

---

## Input

| 항목 | 필수 | 설명 |
|------|------|------|
| `appType` | ✅ | 애플리케이션 유형 (analytics, crm, project, ecommerce) |
| `brand` | ✅ | 브랜드 정보 (colors, fonts) |
| `features` | ❌ | 필요한 기능 목록 |

---

## Dashboard Layout Structure

### 기본 레이아웃 구조

```
┌────────────────────────────────────────────────────────────────────────┐
│  Header (fixed)                                            [User Menu] │
├──────────────┬─────────────────────────────────────────────────────────┤
│              │                                                         │
│   Sidebar    │   Main Content Area                                     │
│   (fixed)    │   ┌─────────────────────────────────────────────────┐   │
│              │   │  Page Header / Breadcrumb                       │   │
│   - Nav      │   ├─────────────────────────────────────────────────┤   │
│   - Submenu  │   │                                                 │   │
│   - Footer   │   │  Content                                        │   │
│              │   │  (Stats, Tables, Charts, etc.)                  │   │
│              │   │                                                 │   │
│              │   │                                                 │   │
│              │   └─────────────────────────────────────────────────┘   │
│              │                                                         │
└──────────────┴─────────────────────────────────────────────────────────┘
```

---

## Layout Component

### 전체 대시보드 레이아웃

```tsx
// components/layouts/dashboard-layout.tsx
"use client";

import { useState } from "react";
import { cn } from "@/lib/utils";
import { DashboardSidebar } from "./dashboard-sidebar";
import { DashboardHeader } from "./dashboard-header";

interface DashboardLayoutProps {
  children: React.ReactNode;
}

export function DashboardLayout({ children }: DashboardLayoutProps) {
  const [sidebarCollapsed, setSidebarCollapsed] = useState(false);
  const [mobileSidebarOpen, setMobileSidebarOpen] = useState(false);

  return (
    <div className="min-h-screen bg-muted/30">
      {/* Sidebar */}
      <DashboardSidebar
        collapsed={sidebarCollapsed}
        onCollapse={setSidebarCollapsed}
        mobileOpen={mobileSidebarOpen}
        onMobileClose={() => setMobileSidebarOpen(false)}
      />

      {/* Main Area */}
      <div
        className={cn(
          "transition-all duration-300",
          sidebarCollapsed ? "lg:pl-[72px]" : "lg:pl-64"
        )}
      >
        {/* Header */}
        <DashboardHeader
          onMenuClick={() => setMobileSidebarOpen(true)}
        />

        {/* Content */}
        <main className="p-4 lg:p-6">
          {children}
        </main>
      </div>

      {/* Mobile Overlay */}
      {mobileSidebarOpen && (
        <div
          className="fixed inset-0 bg-black/50 z-40 lg:hidden"
          onClick={() => setMobileSidebarOpen(false)}
        />
      )}
    </div>
  );
}
```

---

## Sidebar Navigation

### 사이드바 컴포넌트

```tsx
// components/layouts/dashboard-sidebar.tsx
"use client";

import { useState } from "react";
import Link from "next/link";
import { usePathname } from "next/navigation";
import { cn } from "@/lib/utils";
import {
  ChevronLeft,
  ChevronRight,
  Home,
  BarChart3,
  Users,
  Settings,
  FileText,
  CreditCard,
  HelpCircle,
  LogOut,
  ChevronDown,
} from "lucide-react";
import {
  Tooltip,
  TooltipContent,
  TooltipTrigger,
} from "@/components/ui/tooltip";

interface NavItem {
  label: string;
  href?: string;
  icon: React.ComponentType<{ className?: string }>;
  badge?: string | number;
  children?: NavItem[];
}

interface DashboardSidebarProps {
  collapsed: boolean;
  onCollapse: (collapsed: boolean) => void;
  mobileOpen: boolean;
  onMobileClose: () => void;
}

const navItems: NavItem[] = [
  { label: "대시보드", href: "/dashboard", icon: Home },
  { label: "분석", href: "/dashboard/analytics", icon: BarChart3 },
  {
    label: "사용자",
    icon: Users,
    children: [
      { label: "목록", href: "/dashboard/users", icon: Users },
      { label: "권한 관리", href: "/dashboard/users/roles", icon: Users },
    ],
  },
  { label: "문서", href: "/dashboard/documents", icon: FileText },
  { label: "결제", href: "/dashboard/billing", icon: CreditCard, badge: "New" },
];

const bottomNavItems: NavItem[] = [
  { label: "설정", href: "/dashboard/settings", icon: Settings },
  { label: "도움말", href: "/help", icon: HelpCircle },
];

export function DashboardSidebar({
  collapsed,
  onCollapse,
  mobileOpen,
  onMobileClose,
}: DashboardSidebarProps) {
  const pathname = usePathname();
  const [expandedItems, setExpandedItems] = useState<string[]>([]);

  const toggleExpanded = (label: string) => {
    setExpandedItems((prev) =>
      prev.includes(label)
        ? prev.filter((item) => item !== label)
        : [...prev, label]
    );
  };

  const isActive = (href?: string) => {
    if (!href) return false;
    return pathname === href || pathname.startsWith(href + "/");
  };

  const renderNavItem = (item: NavItem, index: number) => {
    const hasChildren = item.children && item.children.length > 0;
    const isExpanded = expandedItems.includes(item.label);
    const active = isActive(item.href);

    const itemContent = (
      <div
        className={cn(
          "flex items-center gap-3 px-3 py-2.5 rounded-lg transition-colors cursor-pointer",
          active
            ? "bg-primary text-primary-foreground"
            : "text-muted-foreground hover:text-foreground hover:bg-muted"
        )}
      >
        <item.icon className="h-5 w-5 flex-shrink-0" />

        {!collapsed && (
          <>
            <span className="flex-1 text-sm font-medium truncate">
              {item.label}
            </span>

            {item.badge && (
              <span className="px-2 py-0.5 text-xs font-medium bg-primary/10 text-primary rounded-full">
                {item.badge}
              </span>
            )}

            {hasChildren && (
              <ChevronDown
                className={cn(
                  "h-4 w-4 transition-transform",
                  isExpanded && "rotate-180"
                )}
              />
            )}
          </>
        )}
      </div>
    );

    if (collapsed) {
      return (
        <Tooltip key={index} delayDuration={0}>
          <TooltipTrigger asChild>
            {item.href ? (
              <Link href={item.href}>{itemContent}</Link>
            ) : (
              <div onClick={() => hasChildren && onCollapse(false)}>
                {itemContent}
              </div>
            )}
          </TooltipTrigger>
          <TooltipContent side="right" className="flex items-center gap-2">
            {item.label}
            {item.badge && (
              <span className="px-1.5 py-0.5 text-xs bg-primary text-primary-foreground rounded">
                {item.badge}
              </span>
            )}
          </TooltipContent>
        </Tooltip>
      );
    }

    if (hasChildren) {
      return (
        <div key={index}>
          <div onClick={() => toggleExpanded(item.label)}>{itemContent}</div>
          {isExpanded && (
            <div className="ml-4 mt-1 space-y-1 border-l border-border pl-3">
              {item.children!.map((child, childIndex) => (
                <Link
                  key={childIndex}
                  href={child.href!}
                  className={cn(
                    "flex items-center gap-2 px-3 py-2 rounded-lg text-sm transition-colors",
                    isActive(child.href)
                      ? "bg-primary/10 text-primary font-medium"
                      : "text-muted-foreground hover:text-foreground hover:bg-muted"
                  )}
                >
                  {child.label}
                </Link>
              ))}
            </div>
          )}
        </div>
      );
    }

    return (
      <Link key={index} href={item.href!}>
        {itemContent}
      </Link>
    );
  };

  return (
    <aside
      className={cn(
        "fixed top-0 left-0 z-50 h-full bg-card border-r border-border flex flex-col transition-all duration-300",
        collapsed ? "w-[72px]" : "w-64",
        mobileOpen ? "translate-x-0" : "-translate-x-full lg:translate-x-0"
      )}
    >
      {/* Logo */}
      <div className="h-16 flex items-center justify-between px-4 border-b border-border">
        {!collapsed && (
          <Link href="/dashboard" className="flex items-center gap-2">
            <div className="w-8 h-8 rounded-lg bg-primary flex items-center justify-center">
              <span className="text-primary-foreground font-bold text-sm">A</span>
            </div>
            <span className="font-semibold text-foreground">AppName</span>
          </Link>
        )}
        {collapsed && (
          <div className="w-10 h-10 rounded-lg bg-primary flex items-center justify-center mx-auto">
            <span className="text-primary-foreground font-bold">A</span>
          </div>
        )}
      </div>

      {/* Navigation */}
      <nav className="flex-1 overflow-y-auto p-3 space-y-1">
        {navItems.map(renderNavItem)}
      </nav>

      {/* Bottom Navigation */}
      <div className="p-3 space-y-1 border-t border-border">
        {bottomNavItems.map(renderNavItem)}

        {/* Logout Button */}
        <button
          className={cn(
            "w-full flex items-center gap-3 px-3 py-2.5 rounded-lg transition-colors text-muted-foreground hover:text-foreground hover:bg-muted"
          )}
        >
          <LogOut className="h-5 w-5 flex-shrink-0" />
          {!collapsed && <span className="text-sm font-medium">로그아웃</span>}
        </button>
      </div>

      {/* Collapse Toggle */}
      <button
        onClick={() => onCollapse(!collapsed)}
        className="hidden lg:flex absolute -right-3 top-20 w-6 h-6 rounded-full bg-card border border-border items-center justify-center hover:bg-muted transition-colors"
      >
        {collapsed ? (
          <ChevronRight className="h-4 w-4" />
        ) : (
          <ChevronLeft className="h-4 w-4" />
        )}
      </button>
    </aside>
  );
}
```

---

## Header Component

```tsx
// components/layouts/dashboard-header.tsx
"use client";

import { useState } from "react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuLabel,
  DropdownMenuSeparator,
  DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu";
import {
  Menu,
  Search,
  Bell,
  Settings,
  User,
  LogOut,
  Moon,
  Sun,
} from "lucide-react";
import { useTheme } from "next-themes";

interface DashboardHeaderProps {
  onMenuClick: () => void;
}

export function DashboardHeader({ onMenuClick }: DashboardHeaderProps) {
  const { theme, setTheme } = useTheme();
  const [notifications] = useState([
    { id: 1, title: "새로운 가입자", message: "김철수님이 가입했습니다.", time: "5분 전" },
    { id: 2, title: "결제 완료", message: "Pro 플랜 결제가 완료되었습니다.", time: "1시간 전" },
  ]);

  return (
    <header className="sticky top-0 z-30 h-16 bg-card/80 backdrop-blur-md border-b border-border">
      <div className="flex items-center justify-between h-full px-4 lg:px-6">
        {/* Left: Mobile Menu & Search */}
        <div className="flex items-center gap-4">
          <Button
            variant="ghost"
            size="icon"
            className="lg:hidden"
            onClick={onMenuClick}
          >
            <Menu className="h-5 w-5" />
          </Button>

          {/* Search */}
          <div className="hidden md:flex items-center">
            <div className="relative">
              <Search className="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-muted-foreground" />
              <Input
                type="search"
                placeholder="검색..."
                className="w-64 pl-9 bg-muted/50 border-0 focus-visible:ring-1"
              />
              <kbd className="absolute right-3 top-1/2 -translate-y-1/2 pointer-events-none hidden sm:inline-flex h-5 select-none items-center gap-1 rounded border bg-muted px-1.5 font-mono text-[10px] font-medium text-muted-foreground">
                <span className="text-xs">⌘</span>K
              </kbd>
            </div>
          </div>
        </div>

        {/* Right: Actions */}
        <div className="flex items-center gap-2">
          {/* Theme Toggle */}
          <Button
            variant="ghost"
            size="icon"
            onClick={() => setTheme(theme === "dark" ? "light" : "dark")}
          >
            <Sun className="h-5 w-5 rotate-0 scale-100 transition-transform dark:-rotate-90 dark:scale-0" />
            <Moon className="absolute h-5 w-5 rotate-90 scale-0 transition-transform dark:rotate-0 dark:scale-100" />
            <span className="sr-only">테마 변경</span>
          </Button>

          {/* Notifications */}
          <DropdownMenu>
            <DropdownMenuTrigger asChild>
              <Button variant="ghost" size="icon" className="relative">
                <Bell className="h-5 w-5" />
                <span className="absolute top-1 right-1 w-2 h-2 bg-red-500 rounded-full" />
                <span className="sr-only">알림</span>
              </Button>
            </DropdownMenuTrigger>
            <DropdownMenuContent align="end" className="w-80">
              <DropdownMenuLabel className="flex items-center justify-between">
                알림
                <Button variant="ghost" size="sm" className="h-auto p-0 text-xs text-primary">
                  모두 읽음
                </Button>
              </DropdownMenuLabel>
              <DropdownMenuSeparator />
              {notifications.map((notification) => (
                <DropdownMenuItem
                  key={notification.id}
                  className="flex flex-col items-start gap-1 p-3"
                >
                  <div className="font-medium">{notification.title}</div>
                  <div className="text-sm text-muted-foreground">
                    {notification.message}
                  </div>
                  <div className="text-xs text-muted-foreground">
                    {notification.time}
                  </div>
                </DropdownMenuItem>
              ))}
              <DropdownMenuSeparator />
              <DropdownMenuItem className="justify-center text-primary">
                모든 알림 보기
              </DropdownMenuItem>
            </DropdownMenuContent>
          </DropdownMenu>

          {/* User Menu */}
          <DropdownMenu>
            <DropdownMenuTrigger asChild>
              <Button variant="ghost" className="gap-2 px-2">
                <div className="w-8 h-8 rounded-full bg-gradient-to-br from-primary to-primary/60 flex items-center justify-center text-primary-foreground font-medium text-sm">
                  JD
                </div>
                <span className="hidden md:inline-block text-sm font-medium">
                  John Doe
                </span>
              </Button>
            </DropdownMenuTrigger>
            <DropdownMenuContent align="end" className="w-56">
              <DropdownMenuLabel>
                <div className="flex flex-col">
                  <span>John Doe</span>
                  <span className="text-xs font-normal text-muted-foreground">
                    john@example.com
                  </span>
                </div>
              </DropdownMenuLabel>
              <DropdownMenuSeparator />
              <DropdownMenuItem>
                <User className="mr-2 h-4 w-4" />
                프로필
              </DropdownMenuItem>
              <DropdownMenuItem>
                <Settings className="mr-2 h-4 w-4" />
                설정
              </DropdownMenuItem>
              <DropdownMenuSeparator />
              <DropdownMenuItem className="text-red-600">
                <LogOut className="mr-2 h-4 w-4" />
                로그아웃
              </DropdownMenuItem>
            </DropdownMenuContent>
          </DropdownMenu>
        </div>
      </div>
    </header>
  );
}
```

---

## Stat Cards & KPI Displays

### 기본 통계 카드

```tsx
// components/dashboard/stat-card.tsx
import { cn } from "@/lib/utils";
import { LucideIcon, TrendingUp, TrendingDown } from "lucide-react";

interface StatCardProps {
  title: string;
  value: string | number;
  change?: {
    value: number;
    type: "increase" | "decrease";
  };
  icon: LucideIcon;
  description?: string;
  className?: string;
}

export function StatCard({
  title,
  value,
  change,
  icon: Icon,
  description,
  className,
}: StatCardProps) {
  return (
    <div
      className={cn(
        "p-6 rounded-xl border border-border bg-card",
        className
      )}
    >
      <div className="flex items-start justify-between">
        <div>
          <p className="text-sm font-medium text-muted-foreground">{title}</p>
          <p className="text-2xl lg:text-3xl font-bold text-foreground mt-2">
            {typeof value === "number" ? value.toLocaleString() : value}
          </p>

          {change && (
            <div className="flex items-center gap-1 mt-2">
              {change.type === "increase" ? (
                <TrendingUp className="h-4 w-4 text-green-500" />
              ) : (
                <TrendingDown className="h-4 w-4 text-red-500" />
              )}
              <span
                className={cn(
                  "text-sm font-medium",
                  change.type === "increase" ? "text-green-500" : "text-red-500"
                )}
              >
                {change.value}%
              </span>
              <span className="text-sm text-muted-foreground">
                전월 대비
              </span>
            </div>
          )}

          {description && (
            <p className="text-sm text-muted-foreground mt-2">
              {description}
            </p>
          )}
        </div>

        <div className="p-3 rounded-lg bg-primary/10">
          <Icon className="h-6 w-6 text-primary" />
        </div>
      </div>
    </div>
  );
}

// 사용 예시
import { Users, DollarSign, ShoppingCart, Activity } from "lucide-react";

function StatsGrid() {
  return (
    <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
      <StatCard
        title="총 사용자"
        value={12847}
        change={{ value: 12.5, type: "increase" }}
        icon={Users}
      />
      <StatCard
        title="월 매출"
        value="₩24,500,000"
        change={{ value: 8.2, type: "increase" }}
        icon={DollarSign}
      />
      <StatCard
        title="주문 수"
        value={1429}
        change={{ value: 3.1, type: "decrease" }}
        icon={ShoppingCart}
      />
      <StatCard
        title="전환율"
        value="3.2%"
        change={{ value: 0.5, type: "increase" }}
        icon={Activity}
      />
    </div>
  );
}
```

### 상세 KPI 카드

```tsx
// components/dashboard/kpi-card.tsx
import { cn } from "@/lib/utils";
import { Progress } from "@/components/ui/progress";

interface KPICardProps {
  title: string;
  current: number;
  target: number;
  unit?: string;
  trend?: { value: number; direction: "up" | "down" };
  sparklineData?: number[];
}

export function KPICard({
  title,
  current,
  target,
  unit = "",
  trend,
  sparklineData,
}: KPICardProps) {
  const progress = Math.min((current / target) * 100, 100);
  const isAchieved = current >= target;

  return (
    <div className="p-6 rounded-xl border border-border bg-card">
      <div className="flex items-center justify-between mb-4">
        <h3 className="text-sm font-medium text-muted-foreground">{title}</h3>
        {trend && (
          <span
            className={cn(
              "text-xs font-medium px-2 py-1 rounded-full",
              trend.direction === "up"
                ? "bg-green-100 text-green-700 dark:bg-green-900/30 dark:text-green-400"
                : "bg-red-100 text-red-700 dark:bg-red-900/30 dark:text-red-400"
            )}
          >
            {trend.direction === "up" ? "+" : "-"}{trend.value}%
          </span>
        )}
      </div>

      <div className="flex items-end gap-4 mb-4">
        <div>
          <span className="text-3xl font-bold text-foreground">
            {current.toLocaleString()}
          </span>
          <span className="text-sm text-muted-foreground ml-1">{unit}</span>
        </div>
        <span className="text-sm text-muted-foreground mb-1">
          / {target.toLocaleString()} {unit}
        </span>
      </div>

      {/* Progress Bar */}
      <div className="space-y-2">
        <Progress
          value={progress}
          className={cn(
            "h-2",
            isAchieved && "[&>div]:bg-green-500"
          )}
        />
        <div className="flex justify-between text-xs text-muted-foreground">
          <span>{progress.toFixed(1)}% 달성</span>
          <span>
            {isAchieved ? "목표 달성!" : `${(target - current).toLocaleString()} ${unit} 남음`}
          </span>
        </div>
      </div>

      {/* Mini Sparkline (optional) */}
      {sparklineData && (
        <div className="mt-4 h-10 flex items-end gap-0.5">
          {sparklineData.map((value, index) => {
            const height = (value / Math.max(...sparklineData)) * 100;
            return (
              <div
                key={index}
                className="flex-1 bg-primary/20 rounded-t transition-all hover:bg-primary/40"
                style={{ height: `${height}%` }}
              />
            );
          })}
        </div>
      )}
    </div>
  );
}
```

---

## Data Tables

### 기능이 포함된 데이터 테이블

```tsx
// components/dashboard/data-table.tsx
"use client";

import { useState } from "react";
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Checkbox } from "@/components/ui/checkbox";
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu";
import {
  Search,
  Filter,
  Download,
  MoreHorizontal,
  ChevronLeft,
  ChevronRight,
  ArrowUpDown,
} from "lucide-react";
import { cn } from "@/lib/utils";

interface Column<T> {
  key: keyof T | string;
  header: string;
  sortable?: boolean;
  render?: (row: T) => React.ReactNode;
  className?: string;
}

interface DataTableProps<T> {
  data: T[];
  columns: Column<T>[];
  searchPlaceholder?: string;
  searchKey?: keyof T;
  onRowClick?: (row: T) => void;
  selectable?: boolean;
  pageSize?: number;
}

export function DataTable<T extends { id: string | number }>({
  data,
  columns,
  searchPlaceholder = "검색...",
  searchKey,
  onRowClick,
  selectable = false,
  pageSize = 10,
}: DataTableProps<T>) {
  const [search, setSearch] = useState("");
  const [sortKey, setSortKey] = useState<string | null>(null);
  const [sortDirection, setSortDirection] = useState<"asc" | "desc">("asc");
  const [selectedRows, setSelectedRows] = useState<Set<string | number>>(new Set());
  const [currentPage, setCurrentPage] = useState(1);

  // Filter & Sort
  const filteredData = data.filter((row) => {
    if (!search || !searchKey) return true;
    const value = String(row[searchKey]).toLowerCase();
    return value.includes(search.toLowerCase());
  });

  const sortedData = [...filteredData].sort((a, b) => {
    if (!sortKey) return 0;
    const aVal = String(a[sortKey as keyof T]);
    const bVal = String(b[sortKey as keyof T]);
    const comparison = aVal.localeCompare(bVal);
    return sortDirection === "asc" ? comparison : -comparison;
  });

  // Pagination
  const totalPages = Math.ceil(sortedData.length / pageSize);
  const paginatedData = sortedData.slice(
    (currentPage - 1) * pageSize,
    currentPage * pageSize
  );

  const handleSort = (key: string) => {
    if (sortKey === key) {
      setSortDirection(sortDirection === "asc" ? "desc" : "asc");
    } else {
      setSortKey(key);
      setSortDirection("asc");
    }
  };

  const handleSelectAll = (checked: boolean) => {
    if (checked) {
      setSelectedRows(new Set(paginatedData.map((row) => row.id)));
    } else {
      setSelectedRows(new Set());
    }
  };

  const handleSelectRow = (id: string | number, checked: boolean) => {
    const newSelected = new Set(selectedRows);
    if (checked) {
      newSelected.add(id);
    } else {
      newSelected.delete(id);
    }
    setSelectedRows(newSelected);
  };

  return (
    <div className="rounded-xl border border-border bg-card">
      {/* Toolbar */}
      <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4 p-4 border-b border-border">
        <div className="flex items-center gap-2 w-full sm:w-auto">
          <div className="relative flex-1 sm:flex-initial">
            <Search className="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-muted-foreground" />
            <Input
              placeholder={searchPlaceholder}
              value={search}
              onChange={(e) => setSearch(e.target.value)}
              className="pl-9 w-full sm:w-64"
            />
          </div>
          <Button variant="outline" size="icon">
            <Filter className="h-4 w-4" />
          </Button>
        </div>

        <div className="flex items-center gap-2">
          {selectedRows.size > 0 && (
            <span className="text-sm text-muted-foreground">
              {selectedRows.size}개 선택됨
            </span>
          )}
          <Button variant="outline" size="sm">
            <Download className="h-4 w-4 mr-2" />
            내보내기
          </Button>
        </div>
      </div>

      {/* Table */}
      <div className="overflow-x-auto">
        <Table>
          <TableHeader>
            <TableRow className="hover:bg-transparent">
              {selectable && (
                <TableHead className="w-12">
                  <Checkbox
                    checked={
                      paginatedData.length > 0 &&
                      paginatedData.every((row) => selectedRows.has(row.id))
                    }
                    onCheckedChange={handleSelectAll}
                  />
                </TableHead>
              )}
              {columns.map((column) => (
                <TableHead
                  key={String(column.key)}
                  className={cn(column.className)}
                >
                  {column.sortable ? (
                    <Button
                      variant="ghost"
                      size="sm"
                      className="-ml-3 h-8 hover:bg-transparent"
                      onClick={() => handleSort(String(column.key))}
                    >
                      {column.header}
                      <ArrowUpDown className="ml-2 h-4 w-4" />
                    </Button>
                  ) : (
                    column.header
                  )}
                </TableHead>
              ))}
              <TableHead className="w-12" />
            </TableRow>
          </TableHeader>
          <TableBody>
            {paginatedData.length === 0 ? (
              <TableRow>
                <TableCell
                  colSpan={columns.length + (selectable ? 2 : 1)}
                  className="h-32 text-center text-muted-foreground"
                >
                  데이터가 없습니다.
                </TableCell>
              </TableRow>
            ) : (
              paginatedData.map((row) => (
                <TableRow
                  key={String(row.id)}
                  className={cn(
                    onRowClick && "cursor-pointer",
                    selectedRows.has(row.id) && "bg-muted/50"
                  )}
                  onClick={() => onRowClick?.(row)}
                >
                  {selectable && (
                    <TableCell onClick={(e) => e.stopPropagation()}>
                      <Checkbox
                        checked={selectedRows.has(row.id)}
                        onCheckedChange={(checked) =>
                          handleSelectRow(row.id, checked as boolean)
                        }
                      />
                    </TableCell>
                  )}
                  {columns.map((column) => (
                    <TableCell
                      key={String(column.key)}
                      className={cn(column.className)}
                    >
                      {column.render
                        ? column.render(row)
                        : String(row[column.key as keyof T])}
                    </TableCell>
                  ))}
                  <TableCell onClick={(e) => e.stopPropagation()}>
                    <DropdownMenu>
                      <DropdownMenuTrigger asChild>
                        <Button variant="ghost" size="icon" className="h-8 w-8">
                          <MoreHorizontal className="h-4 w-4" />
                        </Button>
                      </DropdownMenuTrigger>
                      <DropdownMenuContent align="end">
                        <DropdownMenuItem>보기</DropdownMenuItem>
                        <DropdownMenuItem>수정</DropdownMenuItem>
                        <DropdownMenuItem className="text-red-600">
                          삭제
                        </DropdownMenuItem>
                      </DropdownMenuContent>
                    </DropdownMenu>
                  </TableCell>
                </TableRow>
              ))
            )}
          </TableBody>
        </Table>
      </div>

      {/* Pagination */}
      <div className="flex items-center justify-between p-4 border-t border-border">
        <p className="text-sm text-muted-foreground">
          전체 {sortedData.length}개 중 {(currentPage - 1) * pageSize + 1}-
          {Math.min(currentPage * pageSize, sortedData.length)}개 표시
        </p>
        <div className="flex items-center gap-2">
          <Button
            variant="outline"
            size="icon"
            className="h-8 w-8"
            onClick={() => setCurrentPage(currentPage - 1)}
            disabled={currentPage === 1}
          >
            <ChevronLeft className="h-4 w-4" />
          </Button>
          <span className="text-sm">
            {currentPage} / {totalPages}
          </span>
          <Button
            variant="outline"
            size="icon"
            className="h-8 w-8"
            onClick={() => setCurrentPage(currentPage + 1)}
            disabled={currentPage === totalPages}
          >
            <ChevronRight className="h-4 w-4" />
          </Button>
        </div>
      </div>
    </div>
  );
}
```

### 사용 예시

```tsx
// 사용 예시
interface User {
  id: string;
  name: string;
  email: string;
  role: string;
  status: "active" | "inactive";
  createdAt: string;
}

const columns: Column<User>[] = [
  {
    key: "name",
    header: "이름",
    sortable: true,
    render: (row) => (
      <div className="flex items-center gap-3">
        <div className="w-8 h-8 rounded-full bg-primary/10 flex items-center justify-center">
          <span className="text-sm font-medium text-primary">
            {row.name[0]}
          </span>
        </div>
        <span className="font-medium">{row.name}</span>
      </div>
    ),
  },
  { key: "email", header: "이메일", sortable: true },
  { key: "role", header: "역할" },
  {
    key: "status",
    header: "상태",
    render: (row) => (
      <span
        className={cn(
          "px-2 py-1 text-xs font-medium rounded-full",
          row.status === "active"
            ? "bg-green-100 text-green-700 dark:bg-green-900/30 dark:text-green-400"
            : "bg-gray-100 text-gray-700 dark:bg-gray-800 dark:text-gray-400"
        )}
      >
        {row.status === "active" ? "활성" : "비활성"}
      </span>
    ),
  },
  { key: "createdAt", header: "가입일", sortable: true },
];

function UsersPage() {
  return (
    <DataTable
      data={users}
      columns={columns}
      searchKey="name"
      searchPlaceholder="이름으로 검색..."
      selectable
      pageSize={10}
    />
  );
}
```

---

## Chart Containers

```tsx
// components/dashboard/chart-container.tsx
import { cn } from "@/lib/utils";
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu";
import { Button } from "@/components/ui/button";
import { MoreHorizontal, Download, Maximize2 } from "lucide-react";

interface ChartContainerProps {
  title: string;
  description?: string;
  children: React.ReactNode;
  actions?: React.ReactNode;
  className?: string;
}

export function ChartContainer({
  title,
  description,
  children,
  actions,
  className,
}: ChartContainerProps) {
  return (
    <div
      className={cn(
        "rounded-xl border border-border bg-card p-6",
        className
      )}
    >
      {/* Header */}
      <div className="flex items-start justify-between mb-6">
        <div>
          <h3 className="text-lg font-semibold text-foreground">{title}</h3>
          {description && (
            <p className="text-sm text-muted-foreground mt-1">{description}</p>
          )}
        </div>

        <div className="flex items-center gap-2">
          {actions}
          <DropdownMenu>
            <DropdownMenuTrigger asChild>
              <Button variant="ghost" size="icon" className="h-8 w-8">
                <MoreHorizontal className="h-4 w-4" />
              </Button>
            </DropdownMenuTrigger>
            <DropdownMenuContent align="end">
              <DropdownMenuItem>
                <Download className="h-4 w-4 mr-2" />
                이미지 다운로드
              </DropdownMenuItem>
              <DropdownMenuItem>
                <Download className="h-4 w-4 mr-2" />
                CSV 다운로드
              </DropdownMenuItem>
              <DropdownMenuItem>
                <Maximize2 className="h-4 w-4 mr-2" />
                전체 화면
              </DropdownMenuItem>
            </DropdownMenuContent>
          </DropdownMenu>
        </div>
      </div>

      {/* Chart */}
      <div className="h-[300px]">{children}</div>
    </div>
  );
}

// 기간 선택 탭
export function ChartPeriodTabs({
  value,
  onChange,
}: {
  value: string;
  onChange: (value: string) => void;
}) {
  const periods = [
    { label: "7일", value: "7d" },
    { label: "30일", value: "30d" },
    { label: "90일", value: "90d" },
    { label: "1년", value: "1y" },
  ];

  return (
    <div className="flex items-center gap-1 p-1 bg-muted rounded-lg">
      {periods.map((period) => (
        <button
          key={period.value}
          onClick={() => onChange(period.value)}
          className={cn(
            "px-3 py-1.5 text-sm font-medium rounded-md transition-colors",
            value === period.value
              ? "bg-background text-foreground shadow-sm"
              : "text-muted-foreground hover:text-foreground"
          )}
        >
          {period.label}
        </button>
      ))}
    </div>
  );
}
```

---

## Empty States

```tsx
// components/dashboard/empty-state.tsx
import { Button } from "@/components/ui/button";
import { LucideIcon } from "lucide-react";

interface EmptyStateProps {
  icon: LucideIcon;
  title: string;
  description: string;
  action?: {
    label: string;
    onClick: () => void;
  };
}

export function EmptyState({
  icon: Icon,
  title,
  description,
  action,
}: EmptyStateProps) {
  return (
    <div className="flex flex-col items-center justify-center py-16 px-4 text-center">
      <div className="w-16 h-16 rounded-full bg-muted flex items-center justify-center mb-6">
        <Icon className="h-8 w-8 text-muted-foreground" />
      </div>
      <h3 className="text-lg font-semibold text-foreground mb-2">{title}</h3>
      <p className="text-sm text-muted-foreground max-w-sm mb-6">
        {description}
      </p>
      {action && (
        <Button onClick={action.onClick}>{action.label}</Button>
      )}
    </div>
  );
}

// 검색 결과 없음
import { SearchX } from "lucide-react";

function NoSearchResults() {
  return (
    <EmptyState
      icon={SearchX}
      title="검색 결과가 없습니다"
      description="다른 검색어를 입력하거나 필터를 조정해보세요."
    />
  );
}

// 데이터 없음
import { FolderOpen } from "lucide-react";

function NoData() {
  return (
    <EmptyState
      icon={FolderOpen}
      title="아직 데이터가 없습니다"
      description="첫 번째 항목을 추가하여 시작하세요."
      action={{
        label: "새로 만들기",
        onClick: () => {},
      }}
    />
  );
}
```

---

## Notification Patterns

```tsx
// components/dashboard/notification-center.tsx
import { useState } from "react";
import { cn } from "@/lib/utils";
import { Button } from "@/components/ui/button";
import {
  Sheet,
  SheetContent,
  SheetHeader,
  SheetTitle,
  SheetTrigger,
} from "@/components/ui/sheet";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { Bell, Check, Trash2, Settings } from "lucide-react";

interface Notification {
  id: string;
  type: "info" | "success" | "warning" | "error";
  title: string;
  message: string;
  time: string;
  read: boolean;
}

interface NotificationCenterProps {
  notifications: Notification[];
  onMarkAsRead: (id: string) => void;
  onMarkAllAsRead: () => void;
  onDelete: (id: string) => void;
}

export function NotificationCenter({
  notifications,
  onMarkAsRead,
  onMarkAllAsRead,
  onDelete,
}: NotificationCenterProps) {
  const unreadCount = notifications.filter((n) => !n.read).length;

  const typeStyles = {
    info: "bg-blue-500",
    success: "bg-green-500",
    warning: "bg-yellow-500",
    error: "bg-red-500",
  };

  return (
    <Sheet>
      <SheetTrigger asChild>
        <Button variant="ghost" size="icon" className="relative">
          <Bell className="h-5 w-5" />
          {unreadCount > 0 && (
            <span className="absolute -top-1 -right-1 w-5 h-5 bg-red-500 text-white text-xs font-medium rounded-full flex items-center justify-center">
              {unreadCount > 9 ? "9+" : unreadCount}
            </span>
          )}
        </Button>
      </SheetTrigger>
      <SheetContent className="w-full sm:max-w-md">
        <SheetHeader className="pb-4 border-b">
          <div className="flex items-center justify-between">
            <SheetTitle>알림</SheetTitle>
            <div className="flex items-center gap-2">
              <Button
                variant="ghost"
                size="sm"
                onClick={onMarkAllAsRead}
                disabled={unreadCount === 0}
              >
                <Check className="h-4 w-4 mr-1" />
                모두 읽음
              </Button>
              <Button variant="ghost" size="icon" className="h-8 w-8">
                <Settings className="h-4 w-4" />
              </Button>
            </div>
          </div>
        </SheetHeader>

        <Tabs defaultValue="all" className="mt-4">
          <TabsList className="w-full">
            <TabsTrigger value="all" className="flex-1">
              전체
            </TabsTrigger>
            <TabsTrigger value="unread" className="flex-1">
              읽지 않음 ({unreadCount})
            </TabsTrigger>
          </TabsList>

          <TabsContent value="all" className="mt-4 space-y-2">
            {notifications.length === 0 ? (
              <div className="py-12 text-center text-muted-foreground">
                알림이 없습니다
              </div>
            ) : (
              notifications.map((notification) => (
                <NotificationItem
                  key={notification.id}
                  notification={notification}
                  onMarkAsRead={onMarkAsRead}
                  onDelete={onDelete}
                  typeStyles={typeStyles}
                />
              ))
            )}
          </TabsContent>

          <TabsContent value="unread" className="mt-4 space-y-2">
            {notifications
              .filter((n) => !n.read)
              .map((notification) => (
                <NotificationItem
                  key={notification.id}
                  notification={notification}
                  onMarkAsRead={onMarkAsRead}
                  onDelete={onDelete}
                  typeStyles={typeStyles}
                />
              ))}
          </TabsContent>
        </Tabs>
      </SheetContent>
    </Sheet>
  );
}

function NotificationItem({
  notification,
  onMarkAsRead,
  onDelete,
  typeStyles,
}: {
  notification: Notification;
  onMarkAsRead: (id: string) => void;
  onDelete: (id: string) => void;
  typeStyles: Record<string, string>;
}) {
  return (
    <div
      className={cn(
        "relative p-4 rounded-lg border transition-colors",
        notification.read
          ? "bg-background border-border"
          : "bg-muted/50 border-primary/20"
      )}
    >
      <div className="flex gap-3">
        <div
          className={cn(
            "w-2 h-2 rounded-full mt-2 flex-shrink-0",
            typeStyles[notification.type]
          )}
        />
        <div className="flex-1 min-w-0">
          <div className="flex items-start justify-between gap-2">
            <p className="font-medium text-foreground truncate">
              {notification.title}
            </p>
            <span className="text-xs text-muted-foreground whitespace-nowrap">
              {notification.time}
            </span>
          </div>
          <p className="text-sm text-muted-foreground mt-1 line-clamp-2">
            {notification.message}
          </p>
          <div className="flex items-center gap-2 mt-3">
            {!notification.read && (
              <Button
                variant="ghost"
                size="sm"
                className="h-7 text-xs"
                onClick={() => onMarkAsRead(notification.id)}
              >
                <Check className="h-3 w-3 mr-1" />
                읽음 처리
              </Button>
            )}
            <Button
              variant="ghost"
              size="sm"
              className="h-7 text-xs text-muted-foreground hover:text-red-600"
              onClick={() => onDelete(notification.id)}
            >
              <Trash2 className="h-3 w-3 mr-1" />
              삭제
            </Button>
          </div>
        </div>
      </div>
    </div>
  );
}
```

---

## Settings Page

```tsx
// app/dashboard/settings/page.tsx
"use client";

import { useState } from "react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Switch } from "@/components/ui/switch";
import { Separator } from "@/components/ui/separator";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { User, Bell, Lock, Palette, CreditCard } from "lucide-react";

export default function SettingsPage() {
  return (
    <div className="max-w-4xl mx-auto">
      <div className="mb-8">
        <h1 className="text-2xl font-bold text-foreground">설정</h1>
        <p className="text-muted-foreground mt-1">
          계정 및 앱 환경설정을 관리합니다.
        </p>
      </div>

      <Tabs defaultValue="profile" className="space-y-6">
        <TabsList className="grid w-full grid-cols-5">
          <TabsTrigger value="profile" className="gap-2">
            <User className="h-4 w-4" />
            <span className="hidden sm:inline">프로필</span>
          </TabsTrigger>
          <TabsTrigger value="notifications" className="gap-2">
            <Bell className="h-4 w-4" />
            <span className="hidden sm:inline">알림</span>
          </TabsTrigger>
          <TabsTrigger value="security" className="gap-2">
            <Lock className="h-4 w-4" />
            <span className="hidden sm:inline">보안</span>
          </TabsTrigger>
          <TabsTrigger value="appearance" className="gap-2">
            <Palette className="h-4 w-4" />
            <span className="hidden sm:inline">외관</span>
          </TabsTrigger>
          <TabsTrigger value="billing" className="gap-2">
            <CreditCard className="h-4 w-4" />
            <span className="hidden sm:inline">결제</span>
          </TabsTrigger>
        </TabsList>

        {/* Profile Tab */}
        <TabsContent value="profile">
          <Card>
            <CardHeader>
              <CardTitle>프로필</CardTitle>
              <CardDescription>
                다른 사용자에게 표시되는 정보입니다.
              </CardDescription>
            </CardHeader>
            <CardContent className="space-y-6">
              {/* Avatar */}
              <div className="flex items-center gap-6">
                <div className="w-20 h-20 rounded-full bg-gradient-to-br from-primary to-primary/60 flex items-center justify-center text-primary-foreground text-2xl font-bold">
                  JD
                </div>
                <div>
                  <Button variant="outline" size="sm">
                    이미지 변경
                  </Button>
                  <p className="text-xs text-muted-foreground mt-2">
                    JPG, PNG 또는 GIF. 최대 2MB.
                  </p>
                </div>
              </div>

              <Separator />

              {/* Form Fields */}
              <div className="grid gap-4 md:grid-cols-2">
                <div className="space-y-2">
                  <Label htmlFor="name">이름</Label>
                  <Input id="name" defaultValue="John Doe" />
                </div>
                <div className="space-y-2">
                  <Label htmlFor="username">사용자명</Label>
                  <Input id="username" defaultValue="johndoe" />
                </div>
                <div className="space-y-2 md:col-span-2">
                  <Label htmlFor="email">이메일</Label>
                  <Input
                    id="email"
                    type="email"
                    defaultValue="john@example.com"
                  />
                </div>
                <div className="space-y-2 md:col-span-2">
                  <Label htmlFor="bio">소개</Label>
                  <textarea
                    id="bio"
                    className="w-full min-h-[100px] px-3 py-2 text-sm rounded-md border border-input bg-background resize-none focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring"
                    placeholder="자기소개를 입력하세요..."
                  />
                </div>
              </div>

              <div className="flex justify-end">
                <Button>저장</Button>
              </div>
            </CardContent>
          </Card>
        </TabsContent>

        {/* Notifications Tab */}
        <TabsContent value="notifications">
          <Card>
            <CardHeader>
              <CardTitle>알림 설정</CardTitle>
              <CardDescription>
                알림을 받는 방법과 시기를 설정합니다.
              </CardDescription>
            </CardHeader>
            <CardContent className="space-y-6">
              {[
                {
                  title: "이메일 알림",
                  description: "중요한 업데이트를 이메일로 받습니다.",
                  defaultChecked: true,
                },
                {
                  title: "푸시 알림",
                  description: "브라우저 푸시 알림을 활성화합니다.",
                  defaultChecked: false,
                },
                {
                  title: "마케팅 이메일",
                  description: "제품 업데이트 및 프로모션 정보를 받습니다.",
                  defaultChecked: false,
                },
                {
                  title: "보안 알림",
                  description: "계정 보안 관련 알림은 항상 발송됩니다.",
                  defaultChecked: true,
                  disabled: true,
                },
              ].map((item, index) => (
                <div key={index} className="flex items-center justify-between">
                  <div>
                    <p className="font-medium text-foreground">{item.title}</p>
                    <p className="text-sm text-muted-foreground">
                      {item.description}
                    </p>
                  </div>
                  <Switch
                    defaultChecked={item.defaultChecked}
                    disabled={item.disabled}
                  />
                </div>
              ))}
            </CardContent>
          </Card>
        </TabsContent>

        {/* Security Tab */}
        <TabsContent value="security">
          <div className="space-y-6">
            <Card>
              <CardHeader>
                <CardTitle>비밀번호 변경</CardTitle>
              </CardHeader>
              <CardContent className="space-y-4">
                <div className="space-y-2">
                  <Label htmlFor="current">현재 비밀번호</Label>
                  <Input id="current" type="password" />
                </div>
                <div className="space-y-2">
                  <Label htmlFor="new">새 비밀번호</Label>
                  <Input id="new" type="password" />
                </div>
                <div className="space-y-2">
                  <Label htmlFor="confirm">비밀번호 확인</Label>
                  <Input id="confirm" type="password" />
                </div>
                <Button>비밀번호 변경</Button>
              </CardContent>
            </Card>

            <Card>
              <CardHeader>
                <CardTitle>2단계 인증</CardTitle>
                <CardDescription>
                  계정 보안을 강화하기 위해 2단계 인증을 활성화하세요.
                </CardDescription>
              </CardHeader>
              <CardContent>
                <Button variant="outline">2단계 인증 설정</Button>
              </CardContent>
            </Card>

            <Card className="border-red-200 dark:border-red-900">
              <CardHeader>
                <CardTitle className="text-red-600">위험 구역</CardTitle>
                <CardDescription>
                  이 작업은 되돌릴 수 없습니다.
                </CardDescription>
              </CardHeader>
              <CardContent>
                <Button variant="destructive">계정 삭제</Button>
              </CardContent>
            </Card>
          </div>
        </TabsContent>

        {/* Appearance Tab */}
        <TabsContent value="appearance">
          <Card>
            <CardHeader>
              <CardTitle>외관</CardTitle>
              <CardDescription>
                앱의 외관을 사용자화합니다.
              </CardDescription>
            </CardHeader>
            <CardContent className="space-y-6">
              <div>
                <Label className="mb-3 block">테마</Label>
                <div className="grid grid-cols-3 gap-4">
                  {["light", "dark", "system"].map((theme) => (
                    <button
                      key={theme}
                      className="flex flex-col items-center gap-2 p-4 rounded-lg border border-border hover:border-primary transition-colors"
                    >
                      <div
                        className={cn(
                          "w-full aspect-video rounded-md",
                          theme === "light" && "bg-white border",
                          theme === "dark" && "bg-zinc-900",
                          theme === "system" &&
                            "bg-gradient-to-r from-white to-zinc-900"
                        )}
                      />
                      <span className="text-sm font-medium capitalize">
                        {theme === "system" ? "시스템" : theme === "light" ? "라이트" : "다크"}
                      </span>
                    </button>
                  ))}
                </div>
              </div>

              <Separator />

              <div className="flex items-center justify-between">
                <div>
                  <p className="font-medium">사이드바 축소</p>
                  <p className="text-sm text-muted-foreground">
                    기본적으로 사이드바를 축소합니다.
                  </p>
                </div>
                <Switch />
              </div>
            </CardContent>
          </Card>
        </TabsContent>

        {/* Billing Tab */}
        <TabsContent value="billing">
          <div className="space-y-6">
            <Card>
              <CardHeader>
                <CardTitle>현재 플랜</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="flex items-center justify-between p-4 rounded-lg bg-primary/5 border border-primary/20">
                  <div>
                    <p className="font-semibold text-foreground">Pro 플랜</p>
                    <p className="text-sm text-muted-foreground">
                      ₩49,000/월 (연간 결제)
                    </p>
                  </div>
                  <Button variant="outline">플랜 변경</Button>
                </div>
              </CardContent>
            </Card>

            <Card>
              <CardHeader>
                <CardTitle>결제 수단</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="flex items-center justify-between p-4 rounded-lg border">
                  <div className="flex items-center gap-4">
                    <div className="w-12 h-8 bg-gradient-to-r from-blue-600 to-blue-400 rounded flex items-center justify-center text-white text-xs font-bold">
                      VISA
                    </div>
                    <div>
                      <p className="font-medium">**** **** **** 4242</p>
                      <p className="text-sm text-muted-foreground">
                        만료: 12/2025
                      </p>
                    </div>
                  </div>
                  <Button variant="ghost" size="sm">
                    수정
                  </Button>
                </div>
                <Button variant="outline" className="mt-4">
                  결제 수단 추가
                </Button>
              </CardContent>
            </Card>
          </div>
        </TabsContent>
      </Tabs>
    </div>
  );
}
```

---

## Full Dashboard Composition

```tsx
// app/dashboard/page.tsx
import { StatCard } from "@/components/dashboard/stat-card";
import { KPICard } from "@/components/dashboard/kpi-card";
import { DataTable } from "@/components/dashboard/data-table";
import { ChartContainer, ChartPeriodTabs } from "@/components/dashboard/chart-container";
import { Users, DollarSign, ShoppingCart, Activity } from "lucide-react";

export default function DashboardPage() {
  return (
    <div className="space-y-6">
      {/* Page Header */}
      <div>
        <h1 className="text-2xl font-bold text-foreground">대시보드</h1>
        <p className="text-muted-foreground mt-1">
          비즈니스 핵심 지표를 한눈에 확인하세요.
        </p>
      </div>

      {/* Stats Overview */}
      <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
        <StatCard
          title="총 사용자"
          value={12847}
          change={{ value: 12.5, type: "increase" }}
          icon={Users}
        />
        <StatCard
          title="월 매출"
          value="₩24,500,000"
          change={{ value: 8.2, type: "increase" }}
          icon={DollarSign}
        />
        <StatCard
          title="주문 수"
          value={1429}
          change={{ value: 3.1, type: "decrease" }}
          icon={ShoppingCart}
        />
        <StatCard
          title="전환율"
          value="3.2%"
          change={{ value: 0.5, type: "increase" }}
          icon={Activity}
        />
      </div>

      {/* Charts Row */}
      <div className="grid gap-6 lg:grid-cols-2">
        <ChartContainer
          title="매출 추이"
          description="최근 매출 현황"
          actions={<ChartPeriodTabs value="30d" onChange={() => {}} />}
        >
          {/* Chart Component Here (e.g., Recharts, Chart.js) */}
          <div className="flex items-center justify-center h-full text-muted-foreground">
            매출 차트 영역
          </div>
        </ChartContainer>

        <ChartContainer
          title="사용자 분포"
          description="플랜별 사용자 현황"
        >
          {/* Chart Component Here */}
          <div className="flex items-center justify-center h-full text-muted-foreground">
            파이 차트 영역
          </div>
        </ChartContainer>
      </div>

      {/* KPI Cards */}
      <div className="grid gap-4 md:grid-cols-3">
        <KPICard
          title="월간 활성 사용자"
          current={8500}
          target={10000}
          unit="명"
          trend={{ value: 12, direction: "up" }}
          sparklineData={[65, 72, 78, 74, 80, 85, 89]}
        />
        <KPICard
          title="고객 만족도"
          current={4.5}
          target={4.8}
          unit="점"
          trend={{ value: 2, direction: "up" }}
        />
        <KPICard
          title="평균 응답 시간"
          current={2.3}
          target={2.0}
          unit="초"
          trend={{ value: 5, direction: "down" }}
        />
      </div>

      {/* Recent Activity Table */}
      <div>
        <h2 className="text-lg font-semibold text-foreground mb-4">
          최근 활동
        </h2>
        <DataTable
          data={recentActivities}
          columns={activityColumns}
          searchKey="user"
          searchPlaceholder="사용자 검색..."
          pageSize={5}
        />
      </div>
    </div>
  );
}
```

---

## 접근성 요구사항

```markdown
## Dashboard 접근성 체크리스트

### 네비게이션
- [ ] 키보드로 모든 메뉴 항목 접근 가능
- [ ] 현재 페이지 표시 (aria-current="page")
- [ ] Skip navigation 링크 제공
- [ ] Focus trap (모달, 드롭다운)

### 데이터 테이블
- [ ] 테이블 caption 또는 aria-label
- [ ] 정렬 상태 aria-sort 표시
- [ ] 선택 상태 aria-selected 표시

### 차트/그래프
- [ ] 텍스트 대안 제공 (aria-label, 데이터 테이블)
- [ ] 색상만으로 정보 전달하지 않음
- [ ] 마우스 오버/포커스 시 상세 정보 제공

### 알림
- [ ] 새 알림 aria-live로 공지
- [ ] 알림 개수 스크린 리더 접근 가능
```

---

## 반응형 고려사항

```markdown
## Dashboard 반응형 Breakpoints

### Mobile (< 768px)
- 사이드바: 햄버거 메뉴로 숨김
- 통계 카드: 1열 (세로 스크롤)
- 테이블: 가로 스크롤 또는 카드 형태
- 헤더: 검색창 아이콘화

### Tablet (768px - 1024px)
- 사이드바: 아이콘만 표시 (collapsed)
- 통계 카드: 2열
- 테이블: 주요 컬럼만 표시

### Desktop (> 1024px)
- 사이드바: 펼침 상태 유지
- 통계 카드: 4열
- 테이블: 전체 컬럼 표시
```

---

## References

- `_references/COMPONENT-PATTERN.md`
- `9-patterns/SKILL.md`
- `8-primitives/SKILL.md`
