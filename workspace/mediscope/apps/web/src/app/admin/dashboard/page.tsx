"use client";

import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { FileSearch, Users, MessageSquare, FileCheck } from "lucide-react";

const stats = [
  { label: "진단", value: "23", icon: FileSearch, color: "text-blue-600" },
  { label: "리드", value: "8", icon: Users, color: "text-green-600" },
  {
    label: "상담 중",
    value: "3",
    icon: MessageSquare,
    color: "text-yellow-600",
  },
  { label: "계약", value: "1", icon: FileCheck, color: "text-purple-600" },
];

export default function AdminDashboardPage() {
  return (
    <div>
      <h1 className="mb-6 text-2xl font-bold">대시보드</h1>

      {/* Stats Cards */}
      <div className="mb-8 grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
        {stats.map((stat) => (
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

      {/* Recent Audits */}
      <Card>
        <CardHeader>
          <CardTitle className="text-lg">최근 진단</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="space-y-3">
            {[
              {
                name: "강남피부과",
                score: 38,
                status: "리드수집완료",
                time: "2h ago",
              },
              {
                name: "서울성형외과",
                score: 52,
                status: "상담예약",
                time: "5h ago",
              },
              { name: "역삼치과", score: 21, status: "미전환", time: "1d ago" },
            ].map((item) => (
              <div
                key={item.name}
                className="flex items-center justify-between rounded-lg border p-3"
              >
                <div>
                  <span className="font-medium">{item.name}</span>
                  <span className="ml-3 text-sm text-muted-foreground">
                    {item.score}점
                  </span>
                </div>
                <div className="flex items-center gap-3 text-sm text-muted-foreground">
                  <span>{item.status}</span>
                  <span>{item.time}</span>
                </div>
              </div>
            ))}
          </div>
        </CardContent>
      </Card>
    </div>
  );
}
