import Link from "next/link";
import { getAdminUser } from "@/lib/auth";
import { AdminLogout } from "@/components/admin-logout";

export default async function AdminLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  const user = await getAdminUser();

  // Login page — render without sidebar
  if (!user) {
    return <>{children}</>;
  }

  return (
    <div className="flex min-h-screen">
      <aside className="flex w-56 flex-col border-r bg-muted/30 p-4">
        <Link
          href="/admin/dashboard"
          className="mb-6 block text-lg font-bold text-primary"
        >
          CYH Admin
        </Link>
        <nav className="flex-1 space-y-1">
          {[
            { href: "/admin/dashboard", label: "대시보드" },
            { href: "/admin/audits", label: "진단 목록" },
            { href: "/admin/leads", label: "리드 관리" },
            { href: "/admin/subscriptions", label: "구독 관리" },
            { href: "/admin/integrations", label: "메신저 연동" },
            { href: "/admin/alerts", label: "알림 이력" },
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
        <AdminLogout email={user.email ?? ""} />
      </aside>
      <main className="flex-1 p-6">{children}</main>
    </div>
  );
}
