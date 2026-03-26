import Link from "next/link";

export default function AdminLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <div className="flex min-h-screen">
      <aside className="w-56 border-r bg-muted/30 p-4">
        <Link
          href="/admin/dashboard"
          className="mb-6 block text-lg font-bold text-primary"
        >
          CYH Admin
        </Link>
        <nav className="space-y-1">
          {[
            { href: "/admin/dashboard", label: "대시보드" },
            { href: "/admin/audits", label: "진단 목록" },
            { href: "/admin/leads", label: "리드 관리" },
            { href: "/admin/market", label: "시장 현황" },
          ].map((item) => (
            <Link
              key={item.href}
              href={item.href}
              className="block rounded-md px-3 py-2 text-sm hover:bg-accent"
            >
              {item.label}
            </Link>
          ))}
        </nav>
      </aside>
      <main className="flex-1 p-6">{children}</main>
    </div>
  );
}
