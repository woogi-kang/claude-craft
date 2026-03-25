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
  new: { label: "신규", variant: "default" },
  contacted: { label: "연락완료", variant: "secondary" },
  consulting: { label: "상담중", variant: "warning" },
  proposal_sent: { label: "제안서발송", variant: "secondary" },
  contracted: { label: "계약", variant: "success" },
  active: { label: "활성", variant: "success" },
  churned: { label: "이탈", variant: "destructive" },
};

const MOCK_LEADS = [
  {
    id: "1",
    name: "박지현",
    email: "park@gangnam-skin.kr",
    hospital_name: "강남피부과",
    status: "new",
    created_at: "2026-03-25",
  },
  {
    id: "2",
    name: "이수진",
    email: "lee@seoul-ps.com",
    hospital_name: "서울성형외과",
    status: "consulting",
    created_at: "2026-03-24",
  },
  {
    id: "3",
    name: "김태호",
    email: "kim@yeoksam-dental.kr",
    hospital_name: "역삼치과",
    status: "contacted",
    created_at: "2026-03-23",
  },
];

export default function AdminLeadsPage() {
  return (
    <div>
      <h1 className="mb-6 text-2xl font-bold">리드 관리</h1>
      <Card>
        <CardHeader>
          <CardTitle className="text-lg">리드 목록</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="overflow-x-auto">
            <table className="w-full text-sm">
              <thead>
                <tr className="border-b text-left">
                  <th className="pb-3 pr-4 font-medium">담당자</th>
                  <th className="pb-3 pr-4 font-medium">이메일</th>
                  <th className="pb-3 pr-4 font-medium">병원명</th>
                  <th className="pb-3 pr-4 font-medium">상태</th>
                  <th className="pb-3 font-medium">등록일</th>
                </tr>
              </thead>
              <tbody>
                {MOCK_LEADS.map((lead) => {
                  const badge = STATUS_BADGE[lead.status] ?? STATUS_BADGE.new;
                  return (
                    <tr key={lead.id} className="border-b last:border-0">
                      <td className="py-3 pr-4">{lead.name}</td>
                      <td className="py-3 pr-4 text-muted-foreground">
                        {lead.email}
                      </td>
                      <td className="py-3 pr-4">{lead.hospital_name}</td>
                      <td className="py-3 pr-4">
                        <Badge variant={badge.variant}>{badge.label}</Badge>
                      </td>
                      <td className="py-3 text-muted-foreground">
                        {lead.created_at}
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
