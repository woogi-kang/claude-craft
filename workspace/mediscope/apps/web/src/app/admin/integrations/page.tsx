"use client";

import { useQuery } from "@tanstack/react-query";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";

interface IntegrationStats {
  line: { configured: boolean; leadCount: number };
  wechat: { configured: boolean; leadCount: number };
}

export default function AdminIntegrationsPage() {
  const { data, isLoading } = useQuery<IntegrationStats>({
    queryKey: ["admin-integrations"],
    queryFn: async () => {
      const res = await fetch("/api/admin/integrations");
      if (!res.ok) throw new Error("Failed");
      return res.json();
    },
  });

  const webhookBase =
    typeof window !== "undefined" ? window.location.origin : "";

  return (
    <div>
      <h1 className="mb-6 text-2xl font-bold">메신저 연동</h1>

      {isLoading ? (
        <p className="text-muted-foreground">로딩 중...</p>
      ) : (
        <div className="grid gap-6 md:grid-cols-2">
          {/* LINE */}
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center gap-2 text-lg">
                LINE
                <Badge
                  variant={data?.line.configured ? "success" : "secondary"}
                >
                  {data?.line.configured ? "설정됨" : "미설정"}
                </Badge>
              </CardTitle>
            </CardHeader>
            <CardContent className="space-y-3">
              <div>
                <p className="text-sm font-medium text-muted-foreground">
                  Webhook URL
                </p>
                <code className="mt-1 block rounded bg-muted px-3 py-2 text-xs break-all">
                  {webhookBase}/api/webhook/line
                </code>
              </div>
              <div>
                <p className="text-sm font-medium text-muted-foreground">
                  필요한 환경변수
                </p>
                <ul className="mt-1 space-y-1 text-xs text-muted-foreground">
                  <li>
                    <code>LINE_CHANNEL_SECRET</code>
                  </li>
                  <li>
                    <code>LINE_CHANNEL_ACCESS_TOKEN</code>
                  </li>
                </ul>
              </div>
              <div>
                <p className="text-sm font-medium text-muted-foreground">
                  수신 메시지 (리드)
                </p>
                <p className="mt-1 text-2xl font-bold">
                  {data?.line.leadCount ?? 0}
                  <span className="text-sm font-normal text-muted-foreground">
                    건
                  </span>
                </p>
              </div>
            </CardContent>
          </Card>

          {/* WeChat */}
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center gap-2 text-lg">
                WeChat
                <Badge
                  variant={data?.wechat.configured ? "success" : "secondary"}
                >
                  {data?.wechat.configured ? "설정됨" : "미설정"}
                </Badge>
              </CardTitle>
            </CardHeader>
            <CardContent className="space-y-3">
              <div>
                <p className="text-sm font-medium text-muted-foreground">
                  Webhook URL
                </p>
                <code className="mt-1 block rounded bg-muted px-3 py-2 text-xs break-all">
                  {webhookBase}/api/webhook/wechat
                </code>
              </div>
              <div>
                <p className="text-sm font-medium text-muted-foreground">
                  필요한 환경변수
                </p>
                <ul className="mt-1 space-y-1 text-xs text-muted-foreground">
                  <li>
                    <code>WECHAT_TOKEN</code>
                  </li>
                  <li>
                    <code>WECHAT_APP_ID</code>
                  </li>
                  <li>
                    <code>WECHAT_APP_SECRET</code>
                  </li>
                </ul>
              </div>
              <div>
                <p className="text-sm font-medium text-muted-foreground">
                  수신 메시지 (리드)
                </p>
                <p className="mt-1 text-2xl font-bold">
                  {data?.wechat.leadCount ?? 0}
                  <span className="text-sm font-normal text-muted-foreground">
                    건
                  </span>
                </p>
              </div>
            </CardContent>
          </Card>
        </div>
      )}
    </div>
  );
}
