"use client";

import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";

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

const MOCK_AUDITS = [
  {
    id: "1",
    url: "https://gangnam-skin.kr",
    total_score: 38,
    grade: "D",
    status: "completed",
    created_at: "2026-03-25 14:30",
  },
  {
    id: "2",
    url: "https://seoul-ps.com",
    total_score: 52,
    grade: "C",
    status: "completed",
    created_at: "2026-03-25 09:15",
  },
  {
    id: "3",
    url: "https://yeoksam-dental.kr",
    total_score: 21,
    grade: "D",
    status: "completed",
    created_at: "2026-03-24 16:45",
  },
  {
    id: "4",
    url: "https://sinsa-eye.kr",
    total_score: null,
    grade: null,
    status: "scanning",
    created_at: "2026-03-26 10:00",
  },
];

export default function AdminAuditsPage() {
  return (
    <div>
      <h1 className="mb-6 text-2xl font-bold">진단 목록</h1>
      <Card>
        <CardHeader>
          <CardTitle className="text-lg">전체 진단</CardTitle>
        </CardHeader>
        <CardContent>
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
                {MOCK_AUDITS.map((audit) => {
                  const badge =
                    STATUS_BADGE[audit.status] ?? STATUS_BADGE.pending;
                  return (
                    <tr key={audit.id} className="border-b last:border-0">
                      <td className="py-3 pr-4 font-mono text-xs">
                        {audit.url}
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
                        {audit.created_at}
                      </td>
                    </tr>
                  );
                })}
              </tbody>
            </table>
          </div>
        </CardContent>
      </Card>
    </div>
  );
}
