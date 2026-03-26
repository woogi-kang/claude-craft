"use client";

import { useQuery } from "@tanstack/react-query";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";

const STATUS_BADGE: Record<
  string,
  {
    label: string;
    variant: "default" | "secondary" | "success" | "warning" | "destructive";
  }
> = {
  new: { label: "신규", variant: "default" },
  contacted: { label: "연락완료", variant: "secondary" },
  consulting: { label: "상담중", variant: "warning" },
  proposal_sent: { label: "제안서발송", variant: "secondary" },
  contracted: { label: "계약", variant: "success" },
  active: { label: "활성", variant: "success" },
  churned: { label: "이탈", variant: "destructive" },
};

interface Lead {
  id: string;
  name: string;
  email: string;
  hospital_name: string | null;
  phone: string | null;
  status: string;
  emails_sent: number;
  created_at: string;
}

export default function AdminLeadsPage() {
  const { data: leads, isLoading } = useQuery<Lead[]>({
    queryKey: ["admin-leads"],
    queryFn: async () => {
      const res = await fetch("/api/admin/leads");
      if (!res.ok) throw new Error("Failed");
      return res.json();
    },
  });

  return (
    <div>
      <h1 className="mb-6 text-2xl font-bold">리드 관리</h1>
      <Card>
        <CardHeader>
          <CardTitle className="text-lg">
            리드 목록{" "}
            {leads && (
              <span className="text-muted-foreground font-normal">
                ({leads.length}건)
              </span>
            )}
          </CardTitle>
        </CardHeader>
        <CardContent>
          {isLoading ? (
            <p className="text-muted-foreground">로딩 중...</p>
          ) : !leads?.length ? (
            <p className="text-muted-foreground">등록된 리드가 없습니다.</p>
          ) : (
            <div className="overflow-x-auto">
              <table className="w-full text-sm">
                <thead>
                  <tr className="border-b text-left">
                    <th className="pb-3 pr-4 font-medium">담당자</th>
                    <th className="pb-3 pr-4 font-medium">이메일</th>
                    <th className="pb-3 pr-4 font-medium">병원명</th>
                    <th className="pb-3 pr-4 font-medium">상태</th>
                    <th className="pb-3 pr-4 font-medium">이메일</th>
                    <th className="pb-3 font-medium">등록일</th>
                  </tr>
                </thead>
                <tbody>
                  {leads.map((lead) => {
                    const badge = STATUS_BADGE[lead.status] ?? STATUS_BADGE.new;
                    return (
                      <tr key={lead.id} className="border-b last:border-0">
                        <td className="py-3 pr-4">{lead.name}</td>
                        <td className="py-3 pr-4 text-muted-foreground">
                          {lead.email}
                        </td>
                        <td className="py-3 pr-4">
                          {lead.hospital_name ?? "-"}
                        </td>
                        <td className="py-3 pr-4">
                          <Badge variant={badge.variant}>{badge.label}</Badge>
                        </td>
                        <td className="py-3 pr-4 text-muted-foreground">
                          {lead.emails_sent}건
                        </td>
                        <td className="py-3 text-muted-foreground">
                          {new Date(lead.created_at).toLocaleDateString(
                            "ko-KR",
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
