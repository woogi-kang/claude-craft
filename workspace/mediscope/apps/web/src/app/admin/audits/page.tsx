"use client";

import { useQuery } from "@tanstack/react-query";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import Link from "next/link";

const STATUS_BADGE: Record<
  string,
  {
    label: string;
    variant: "default" | "secondary" | "success" | "warning" | "destructive";
  }
> = {
  pending: { label: "대기", variant: "secondary" },
  scanning: { label: "스캔중", variant: "warning" },
  completed: { label: "완료", variant: "success" },
  failed: { label: "실패", variant: "destructive" },
};

interface Audit {
  id: string;
  url: string;
  total_score: number | null;
  grade: string | null;
  status: string;
  created_at: string;
}

export default function AdminAuditsPage() {
  const { data: audits, isLoading } = useQuery<Audit[]>({
    queryKey: ["admin-audits"],
    queryFn: async () => {
      const res = await fetch("/api/admin/audits");
      if (!res.ok) throw new Error("Failed");
      return res.json();
    },
  });

  return (
    <div>
      <h1 className="mb-6 text-2xl font-bold">진단 목록</h1>
      <Card>
        <CardHeader>
          <CardTitle className="text-lg">
            전체 진단{" "}
            {audits && (
              <span className="text-muted-foreground font-normal">
                ({audits.length}건)
              </span>
            )}
          </CardTitle>
        </CardHeader>
        <CardContent>
          {isLoading ? (
            <p className="text-muted-foreground">로딩 중...</p>
          ) : !audits?.length ? (
            <p className="text-muted-foreground">진단 데이터가 없습니다.</p>
          ) : (
            <div className="overflow-x-auto">
              <table className="w-full text-sm">
                <thead>
                  <tr className="border-b text-left">
                    <th className="pb-3 pr-4 font-medium">URL</th>
                    <th className="pb-3 pr-4 font-medium">점수</th>
                    <th className="pb-3 pr-4 font-medium">등급</th>
                    <th className="pb-3 pr-4 font-medium">상태</th>
                    <th className="pb-3 font-medium">일시</th>
                  </tr>
                </thead>
                <tbody>
                  {audits.map((audit) => {
                    const badge =
                      STATUS_BADGE[audit.status] ?? STATUS_BADGE.pending;
                    return (
                      <tr key={audit.id} className="border-b last:border-0">
                        <td className="py-3 pr-4">
                          <Link
                            href={`/report/${audit.id}`}
                            className="font-mono text-xs hover:underline"
                          >
                            {audit.url}
                          </Link>
                        </td>
                        <td className="py-3 pr-4 font-medium">
                          {audit.total_score !== null
                            ? `${audit.total_score}점`
                            : "-"}
                        </td>
                        <td className="py-3 pr-4 font-bold">
                          {audit.grade ?? "-"}
                        </td>
                        <td className="py-3 pr-4">
                          <Badge variant={badge.variant}>{badge.label}</Badge>
                        </td>
                        <td className="py-3 text-muted-foreground">
                          {new Date(audit.created_at).toLocaleString("ko-KR")}
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
