import { createAdminClient } from "@/lib/supabase/admin";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";

const ALERT_TYPE_LABEL: Record<string, string> = {
  score_change: "점수 변동",
  grade_change: "등급 변동",
  score_drop: "점수 하락",
  score_rise: "점수 상승",
};

interface Alert {
  id: string;
  subscription_id: string;
  alert_type: string;
  previous_score: number | null;
  current_score: number | null;
  message: string | null;
  sent: boolean;
  created_at: string;
  subscriptions: {
    email: string;
    audits: { url: string; hospital_name: string | null } | null;
  } | null;
}

export const dynamic = "force-dynamic";

export default async function AdminAlertsPage() {
  const supabase = createAdminClient();

  const { data: alerts, error } = await supabase
    .from("alerts")
    .select(
      "id, subscription_id, alert_type, previous_score, current_score, message, sent, created_at, subscriptions(email, audits(url, hospital_name))",
    )
    .order("created_at", { ascending: false })
    .limit(100);

  if (error) {
    return (
      <div>
        <h1 className="mb-6 text-2xl font-bold">알림 이력</h1>
        <p className="text-destructive">데이터를 불러올 수 없습니다.</p>
      </div>
    );
  }

  const items = (alerts ?? []) as unknown as Alert[];

  return (
    <div>
      <h1 className="mb-6 text-2xl font-bold">알림 이력</h1>
      <Card>
        <CardHeader>
          <CardTitle className="text-lg">
            알림 목록{" "}
            <span className="text-muted-foreground font-normal">
              ({items.length}건)
            </span>
          </CardTitle>
        </CardHeader>
        <CardContent>
          {!items.length ? (
            <p className="text-muted-foreground">알림 이력이 없습니다.</p>
          ) : (
            <div className="overflow-x-auto">
              <table className="w-full text-sm">
                <thead>
                  <tr className="border-b text-left">
                    <th className="pb-3 pr-4 font-medium">병원/URL</th>
                    <th className="pb-3 pr-4 font-medium">이메일</th>
                    <th className="pb-3 pr-4 font-medium">유형</th>
                    <th className="pb-3 pr-4 font-medium">점수 변동</th>
                    <th className="pb-3 pr-4 font-medium">전송</th>
                    <th className="pb-3 font-medium">일시</th>
                  </tr>
                </thead>
                <tbody>
                  {items.map((alert) => {
                    const scoreDiff =
                      alert.previous_score != null &&
                      alert.current_score != null
                        ? alert.current_score - alert.previous_score
                        : null;

                    return (
                      <tr key={alert.id} className="border-b last:border-0">
                        <td className="py-3 pr-4">
                          {alert.subscriptions?.audits?.hospital_name ??
                            alert.subscriptions?.audits?.url ??
                            "-"}
                        </td>
                        <td className="py-3 pr-4 text-muted-foreground">
                          {alert.subscriptions?.email ?? "-"}
                        </td>
                        <td className="py-3 pr-4">
                          <Badge variant="secondary">
                            {ALERT_TYPE_LABEL[alert.alert_type] ??
                              alert.alert_type}
                          </Badge>
                        </td>
                        <td className="py-3 pr-4">
                          {scoreDiff !== null ? (
                            <span
                              className={
                                scoreDiff > 0
                                  ? "text-green-600 font-medium"
                                  : scoreDiff < 0
                                    ? "text-red-600 font-medium"
                                    : "text-muted-foreground"
                              }
                            >
                              {alert.previous_score} → {alert.current_score} (
                              {scoreDiff > 0 ? "+" : ""}
                              {scoreDiff})
                            </span>
                          ) : (
                            <span className="text-muted-foreground">-</span>
                          )}
                        </td>
                        <td className="py-3 pr-4">
                          <Badge
                            variant={alert.sent ? "success" : "destructive"}
                          >
                            {alert.sent ? "전송됨" : "미전송"}
                          </Badge>
                        </td>
                        <td className="py-3 text-muted-foreground">
                          {new Date(alert.created_at).toLocaleString("ko-KR")}
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
