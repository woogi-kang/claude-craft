"use client";

import { useParams } from "next/navigation";
import { useQuery } from "@tanstack/react-query";
import { useState } from "react";
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  Cell,
} from "recharts";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Badge } from "@/components/ui/badge";
import type { Audit, Category } from "@/lib/types";
import { CATEGORY_LABELS, GRADE_COLORS, getGrade } from "@/lib/types";

const BAR_COLORS = ["#4f46e5", "#0ea5e9", "#8b5cf6", "#f59e0b", "#10b981"];

function ScoreGauge({ score, grade }: { score: number; grade: string }) {
  return (
    <div className="flex flex-col items-center">
      <div className="relative flex h-32 w-32 items-center justify-center rounded-full border-8 border-muted">
        <div className="text-center">
          <div className="text-4xl font-bold">{score}</div>
          <div className="text-sm text-muted-foreground">/100</div>
        </div>
      </div>
      <Badge
        className={`mt-3 text-lg ${GRADE_COLORS[grade as keyof typeof GRADE_COLORS] ?? ""}`}
        variant="outline"
      >
        등급: {grade}
      </Badge>
    </div>
  );
}

export default function ReportPage() {
  const { id } = useParams<{ id: string }>();
  const [leadForm, setLeadForm] = useState({
    email: "",
    name: "",
    hospital_name: "",
    phone: "",
  });
  const [leadSubmitted, setLeadSubmitted] = useState(false);
  const [leadError, setLeadError] = useState("");

  const { data: audit, isLoading } = useQuery<Audit>({
    queryKey: ["audit", id],
    queryFn: async () => {
      const res = await fetch(`/api/audits/${id}`);
      if (!res.ok) throw new Error("Failed to fetch");
      return res.json();
    },
  });

  async function handleLeadSubmit(e: React.FormEvent) {
    e.preventDefault();
    setLeadError("");

    if (!leadForm.email || !leadForm.name) {
      setLeadError("이메일과 이름은 필수입니다.");
      return;
    }

    try {
      const res = await fetch("/api/leads", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ audit_id: id, ...leadForm }),
      });
      if (!res.ok) throw new Error("제출 실패");
      setLeadSubmitted(true);
    } catch {
      setLeadError("제출에 실패했습니다. 다시 시도해주세요.");
    }
  }

  if (isLoading) {
    return (
      <div className="flex min-h-screen items-center justify-center">
        <p className="text-muted-foreground">리포트 로딩 중...</p>
      </div>
    );
  }

  if (!audit) {
    return (
      <div className="flex min-h-screen items-center justify-center">
        <p className="text-destructive">리포트를 찾을 수 없습니다.</p>
      </div>
    );
  }

  const scores = audit.scores;
  const chartData = (Object.entries(scores) as [Category, number][]).map(
    ([key, value], i) => ({
      name: CATEGORY_LABELS[key] ?? key,
      score: value,
      fill: BAR_COLORS[i % BAR_COLORS.length],
    }),
  );

  const totalScore = audit.total_score ?? 0;
  const grade = audit.grade ?? getGrade(totalScore);

  return (
    <div className="mx-auto max-w-4xl px-4 py-12">
      <h1 className="mb-2 text-3xl font-bold">진단 리포트</h1>
      <p className="mb-8 text-muted-foreground">{audit.url}</p>

      <div className="grid gap-6 md:grid-cols-[1fr_2fr]">
        {/* Score Summary */}
        <Card>
          <CardHeader>
            <CardTitle className="text-lg">종합 점수</CardTitle>
          </CardHeader>
          <CardContent className="flex justify-center">
            <ScoreGauge score={totalScore} grade={grade} />
          </CardContent>
        </Card>

        {/* Bar Chart */}
        <Card>
          <CardHeader>
            <CardTitle className="text-lg">카테고리별 점수</CardTitle>
          </CardHeader>
          <CardContent>
            <ResponsiveContainer width="100%" height={250}>
              <BarChart data={chartData} layout="vertical">
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis type="number" domain={[0, 100]} />
                <YAxis
                  type="category"
                  dataKey="name"
                  width={80}
                  tick={{ fontSize: 12 }}
                />
                <Tooltip />
                <Bar dataKey="score" radius={[0, 4, 4, 0]}>
                  {chartData.map((entry, i) => (
                    <Cell key={i} fill={entry.fill} />
                  ))}
                </Bar>
              </BarChart>
            </ResponsiveContainer>
          </CardContent>
        </Card>
      </div>

      {/* Lead Collection Form */}
      <Card className="mt-8">
        <CardHeader>
          <CardTitle className="text-lg">상세 리포트를 받아보세요</CardTitle>
          <p className="text-sm text-muted-foreground">
            정보를 입력하시면 PDF 상세 리포트를 이메일로 보내드립니다.
          </p>
        </CardHeader>
        <CardContent>
          {leadSubmitted ? (
            <div className="rounded-lg bg-green-50 p-4 text-center text-green-800">
              신청이 완료되었습니다. 이메일로 상세 리포트를 보내드리겠습니다.
            </div>
          ) : (
            <form onSubmit={handleLeadSubmit} className="space-y-4">
              <div className="grid gap-4 sm:grid-cols-2">
                <div className="space-y-2">
                  <Label htmlFor="email">이메일 *</Label>
                  <Input
                    id="email"
                    type="email"
                    placeholder="you@hospital.kr"
                    value={leadForm.email}
                    onChange={(e) =>
                      setLeadForm((p) => ({ ...p, email: e.target.value }))
                    }
                    required
                  />
                </div>
                <div className="space-y-2">
                  <Label htmlFor="name">담당자명 *</Label>
                  <Input
                    id="name"
                    placeholder="홍길동"
                    value={leadForm.name}
                    onChange={(e) =>
                      setLeadForm((p) => ({ ...p, name: e.target.value }))
                    }
                    required
                  />
                </div>
                <div className="space-y-2">
                  <Label htmlFor="hospital_name">병원명</Label>
                  <Input
                    id="hospital_name"
                    placeholder="OO병원"
                    value={leadForm.hospital_name}
                    onChange={(e) =>
                      setLeadForm((p) => ({
                        ...p,
                        hospital_name: e.target.value,
                      }))
                    }
                  />
                </div>
                <div className="space-y-2">
                  <Label htmlFor="phone">전화번호</Label>
                  <Input
                    id="phone"
                    type="tel"
                    placeholder="02-1234-5678"
                    value={leadForm.phone}
                    onChange={(e) =>
                      setLeadForm((p) => ({ ...p, phone: e.target.value }))
                    }
                  />
                </div>
              </div>
              {leadError && (
                <p className="text-sm text-destructive">{leadError}</p>
              )}
              <Button type="submit" className="w-full">
                무료 상세 리포트 받기
              </Button>
            </form>
          )}
        </CardContent>
      </Card>
    </div>
  );
}
