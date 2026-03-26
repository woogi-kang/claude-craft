import { createAdminClient } from "@/lib/supabase/admin";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { CancelSubscriptionButton } from "./cancel-button";

const FREQUENCY_LABEL: Record<string, string> = {
  weekly: "주간",
  biweekly: "격주",
  monthly: "월간",
};

const STATUS_BADGE: Record<
  string,
  {
    label: string;
    variant: "default" | "secondary" | "success" | "destructive";
  }
> = {
  active: { label: "활성", variant: "success" },
  paused: { label: "일시중지", variant: "secondary" },
  cancelled: { label: "해지", variant: "destructive" },
};

interface Subscription {
  id: string;
  audit_id: string;
  email: string;
  frequency: string;
  status: string;
  last_scan_at: string | null;
  next_scan_at: string | null;
  created_at: string;
  audits: { url: string; hospital_name: string | null } | null;
}

export const dynamic = "force-dynamic";

export default async function AdminSubscriptionsPage() {
  const supabase = createAdminClient();

  const { data: subscriptions, error } = await supabase
    .from("subscriptions")
    .select(
      "id, audit_id, email, frequency, status, last_scan_at, next_scan_at, created_at, audits(url, hospital_name)",
    )
    .order("created_at", { ascending: false });

  if (error) {
    return (
      <div>
        <h1 className="mb-6 text-2xl font-bold">구독 관리</h1>
        <p className="text-destructive">데이터를 불러올 수 없습니다.</p>
      </div>
    );
  }

  const items = (subscriptions ?? []) as unknown as Subscription[];

  return (
    <div>
      <h1 className="mb-6 text-2xl font-bold">구독 관리</h1>
      <Card>
        <CardHeader>
          <CardTitle className="text-lg">
            구독 목록{" "}
            <span className="text-muted-foreground font-normal">
              ({items.length}건)
            </span>
          </CardTitle>
        </CardHeader>
        <CardContent>
          {!items.length ? (
            <p className="text-muted-foreground">등록된 구독이 없습니다.</p>
          ) : (
            <div className="overflow-x-auto">
              <table className="w-full text-sm">
                <thead>
                  <tr className="border-b text-left">
                    <th className="pb-3 pr-4 font-medium">병원/URL</th>
                    <th className="pb-3 pr-4 font-medium">이메일</th>
                    <th className="pb-3 pr-4 font-medium">빈도</th>
                    <th className="pb-3 pr-4 font-medium">마지막 스캔</th>
                    <th className="pb-3 pr-4 font-medium">다음 스캔</th>
                    <th className="pb-3 pr-4 font-medium">상태</th>
                    <th className="pb-3 font-medium">작업</th>
                  </tr>
                </thead>
                <tbody>
                  {items.map((sub) => {
                    const badge =
                      STATUS_BADGE[sub.status] ?? STATUS_BADGE.active;
                    return (
                      <tr key={sub.id} className="border-b last:border-0">
                        <td className="py-3 pr-4">
                          {sub.audits?.hospital_name ?? sub.audits?.url ?? "-"}
                        </td>
                        <td className="py-3 pr-4 text-muted-foreground">
                          {sub.email}
                        </td>
                        <td className="py-3 pr-4">
                          {FREQUENCY_LABEL[sub.frequency] ?? sub.frequency}
                        </td>
                        <td className="py-3 pr-4 text-muted-foreground">
                          {sub.last_scan_at
                            ? new Date(sub.last_scan_at).toLocaleDateString(
                                "ko-KR",
                              )
                            : "-"}
                        </td>
                        <td className="py-3 pr-4 text-muted-foreground">
                          {sub.next_scan_at
                            ? new Date(sub.next_scan_at).toLocaleDateString(
                                "ko-KR",
                              )
                            : "-"}
                        </td>
                        <td className="py-3 pr-4">
                          <Badge variant={badge.variant}>{badge.label}</Badge>
                        </td>
                        <td className="py-3">
                          {sub.status === "active" && (
                            <CancelSubscriptionButton subscriptionId={sub.id} />
                          )}
                        </td>
                      </tr>
                    );
                  })}
                </tbody>
              </table>
            </div>
          )}
        </CardContent>
      </Card>
    </div>
  );
}
