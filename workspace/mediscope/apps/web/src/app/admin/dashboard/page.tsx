"use client";

import { useQuery } from "@tanstack/react-query";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { FileSearch, Users, MessageSquare, FileCheck } from "lucide-react";
import Link from "next/link";

interface Stats {
  audits: number;
  leads: number;
  consulting: number;
  contracted: number;
}

interface RecentAudit {
  id: string;
  url: string;
  total_score: number | null;
  status: string;
  created_at: string;
}

export default function AdminDashboardPage() {
  const { data: stats } = useQuery<Stats>({
    queryKey: ["admin-stats"],
    queryFn: async () => {
      const res = await fetch("/api/admin/stats");
      if (!res.ok) throw new Error("Failed");
      return res.json();
    },
  });

  const { data: recentAudits } = useQuery<RecentAudit[]>({
    queryKey: ["admin-recent-audits"],
    queryFn: async () => {
      const res = await fetch("/api/admin/audits?limit=5");
      if (!res.ok) throw new Error("Failed");
      return res.json();
    },
  });

  const cards = [
    {
      label: "진단",
      value: stats?.audits ?? 0,
      icon: FileSearch,
      color: "text-blue-600",
    },
    {
      label: "리드",
      value: stats?.leads ?? 0,
      icon: Users,
      color: "text-green-600",
    },
    {
      label: "상담 중",
      value: stats?.consulting ?? 0,
      icon: MessageSquare,
      color: "text-yellow-600",
    },
    {
      label: "계약",
      value: stats?.contracted ?? 0,
      icon: FileCheck,
      color: "text-purple-600",
    },
  ];

  function timeAgo(dateStr: string) {
    const diff = Date.now() - new Date(dateStr).getTime();
    const hours = Math.floor(diff / 3600000);
    if (hours < 1) return "방금 전";
    if (hours < 24) return `${hours}시간 전`;
    return `${Math.floor(hours / 24)}일 전`;
  }

  return (
    <div>
      <h1 className="mb-6 text-2xl font-bold">대시보드</h1>

      <div className="mb-8 grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
        {cards.map((stat) => (
          <Card key={stat.label}>
            <CardHeader className="flex flex-row items-center justify-between pb-2">
              <CardTitle className="text-sm font-medium text-muted-foreground">
                {stat.label}
              </CardTitle>
              <stat.icon className={`h-5 w-5 ${stat.color}`} />
            </CardHeader>
            <CardContent>
              <div className="text-3xl font-bold">{stat.value}</div>
            </CardContent>
          </Card>
        ))}
      </div>

      <Card>
        <CardHeader>
          <CardTitle className="text-lg">최근 진단</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="space-y-3">
            {recentAudits?.map((audit) => (
              <Link
                key={audit.id}
                href={`/report/${audit.id}`}
                className="flex items-center justify-between rounded-lg border p-3 hover:bg-accent/50"
              >
                <div>
                  <span className="font-medium font-mono text-sm">
                    {audit.url}
                  </span>
                  {audit.total_score !== null && (
                    <span className="ml-3 text-sm text-muted-foreground">
                      {audit.total_score}점
                    </span>
                  )}
                </div>
                <div className="flex items-center gap-3 text-sm text-muted-foreground">
                  <Badge
                    variant={
                      audit.status === "completed" ? "success" : "secondary"
                    }
                  >
                    {audit.status}
                  </Badge>
                  <span>{timeAgo(audit.created_at)}</span>
                </div>
              </Link>
            )) ?? (
              <p className="text-muted-foreground">진단 데이터가 없습니다.</p>
            )}
          </div>
        </CardContent>
      </Card>
    </div>
  );
}
