"use client";

import { useParams } from "next/navigation";
import { useQuery } from "@tanstack/react-query";
import { PieChart, Pie, Tooltip, ResponsiveContainer, Cell } from "recharts";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import type { Audit, Category } from "@/lib/types";
import { CATEGORY_LABELS, getGrade } from "@/lib/types";
import { ScoreSection } from "@/components/report/score-section";
import {
  CategoryChart,
  type ChartDataItem,
} from "@/components/report/category-chart";
import { BenchmarkSection } from "@/components/report/benchmark-section";
import { LeadForm } from "@/components/report/lead-form";
import { SubscriptionForm } from "@/components/report/subscription-form";

const BAR_COLORS = ["#4f46e5", "#0ea5e9", "#8b5cf6", "#f59e0b", "#10b981"];
const PIE_COLORS = ["#4f46e5", "#e5e7eb"];

interface CompetitionData {
  audit_id: string;
  region: { sido: string; sggu: string } | null;
  total_clinics: number;
  region_clinics: number;
  foreign_patient_facilitators: number;
  foreign_patient_rate: number;
  website_count: number;
  website_rate: number;
}

export default function ReportPage() {
  const { id } = useParams<{ id: string }>();

  const { data: audit, isLoading } = useQuery<Audit>({
    queryKey: ["audit", id],
    queryFn: async () => {
      const res = await fetch(`/api/audits/${id}`);
      if (!res.ok) throw new Error("Failed to fetch");
      return res.json();
    },
  });

  const { data: competition } = useQuery<CompetitionData>({
    queryKey: ["competition", id],
    queryFn: async () => {
      const res = await fetch(`/api/competition/${id}`);
      if (!res.ok) return null;
      return res.json();
    },
    enabled: !!audit,
  });

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

  const scores = audit.scores ?? {};

  // scores can be either { category: number } or { item_key: { score, weight, grade, ... } }
  // Aggregate by category for the chart
  const CATEGORY_MAP: Record<string, string> = {
    robots_txt: "technical_seo",
    sitemap: "technical_seo",
    meta_tags: "technical_seo",
    headings: "technical_seo",
    images_alt: "technical_seo",
    links: "technical_seo",
    https: "technical_seo",
    canonical: "technical_seo",
    url_structure: "technical_seo",
    errors_404: "technical_seo",
    lcp: "performance",
    inp: "performance",
    cls: "performance",
    performance_score: "performance",
    mobile: "performance",
  };

  const categoryScores: Record<string, { total: number; count: number }> = {};
  for (const [key, val] of Object.entries(scores)) {
    const cat = CATEGORY_MAP[key] ?? key;
    const numScore =
      typeof val === "number" ? val : ((val as { score?: number })?.score ?? 0);
    if (!categoryScores[cat]) categoryScores[cat] = { total: 0, count: 0 };
    categoryScores[cat].total += numScore;
    categoryScores[cat].count += 1;
  }

  const chartData: ChartDataItem[] = Object.entries(categoryScores).map(
    ([key, { total, count }], i) => ({
      name: CATEGORY_LABELS[key as Category] ?? key,
      score: Math.round(count > 0 ? total / count : 0),
      fill: BAR_COLORS[i % BAR_COLORS.length],
    }),
  );

  const totalScore = audit.total_score ?? 0;
  const grade = audit.grade ?? getGrade(totalScore);

  return (
    <div className="mx-auto max-w-4xl px-4 py-12">
      <div className="flex items-center justify-between mb-2">
        <h1 className="text-3xl font-bold">진단 리포트</h1>
        <div className="flex items-center gap-2">
          {audit.report_url && (
            <a
              href={audit.report_url}
              target="_blank"
              rel="noopener noreferrer"
              className="inline-flex items-center gap-2 rounded-md bg-green-600 px-4 py-2 text-sm font-medium text-white hover:bg-green-700"
            >
              PDF 다운로드
            </a>
          )}
          <a
            href={`/api/reports/${id}`}
            target="_blank"
            rel="noopener noreferrer"
            className="inline-flex items-center gap-2 rounded-md bg-primary px-4 py-2 text-sm font-medium text-primary-foreground hover:bg-primary/90"
          >
            상세 리포트 보기 / 인쇄
          </a>
        </div>
      </div>
      <p className="mb-8 text-muted-foreground">{audit.url}</p>

      <div className="grid gap-6 md:grid-cols-[1fr_2fr]">
        <ScoreSection totalScore={totalScore} grade={grade} />
        <CategoryChart data={chartData} />
      </div>

      {/* Competition Analysis */}
      {competition && competition.region_clinics > 0 && (
        <Card className="mt-8">
          <CardHeader>
            <CardTitle className="text-lg">경쟁 분석</CardTitle>
            <p className="text-sm text-muted-foreground">
              {competition.region
                ? `${competition.region.sido} ${competition.region.sggu ?? ""} 지역`
                : "전체"}{" "}
              피부과 현황
            </p>
          </CardHeader>
          <CardContent>
            <div className="grid gap-4 sm:grid-cols-3">
              <div className="rounded-lg border p-4 text-center">
                <div className="text-3xl font-bold text-primary">
                  {competition.region_clinics}
                </div>
                <div className="mt-1 text-sm text-muted-foreground">
                  같은 지역 피부과
                </div>
              </div>
              <div className="rounded-lg border p-4 text-center">
                <div className="text-3xl font-bold text-orange-600">
                  {competition.foreign_patient_rate}%
                </div>
                <div className="mt-1 text-sm text-muted-foreground">
                  외국인유치기관 비율
                </div>
              </div>
              <div className="rounded-lg border p-4 text-center">
                <div className="text-3xl font-bold text-blue-600">
                  {competition.website_rate}%
                </div>
                <div className="mt-1 text-sm text-muted-foreground">
                  웹사이트 보유율
                </div>
              </div>
            </div>
            <div className="mt-6 grid gap-4 sm:grid-cols-2">
              <div>
                <p className="mb-2 text-sm font-medium">웹사이트 보유</p>
                <ResponsiveContainer width="100%" height={160}>
                  <PieChart>
                    <Pie
                      data={[
                        { name: "보유", value: competition.website_count },
                        {
                          name: "미보유",
                          value:
                            competition.region_clinics -
                            competition.website_count,
                        },
                      ]}
                      cx="50%"
                      cy="50%"
                      innerRadius={40}
                      outerRadius={60}
                      dataKey="value"
                      label={({ name, percent }) =>
                        `${name} ${(percent * 100).toFixed(0)}%`
                      }
                    >
                      <Cell fill={PIE_COLORS[0]} />
                      <Cell fill={PIE_COLORS[1]} />
                    </Pie>
                    <Tooltip />
                  </PieChart>
                </ResponsiveContainer>
              </div>
              <div>
                <p className="mb-2 text-sm font-medium">외국인유치기관</p>
                <ResponsiveContainer width="100%" height={160}>
                  <PieChart>
                    <Pie
                      data={[
                        {
                          name: "유치기관",
                          value: competition.foreign_patient_facilitators,
                        },
                        {
                          name: "일반",
                          value:
                            competition.region_clinics -
                            competition.foreign_patient_facilitators,
                        },
                      ]}
                      cx="50%"
                      cy="50%"
                      innerRadius={40}
                      outerRadius={60}
                      dataKey="value"
                      label={({ name, percent }) =>
                        `${name} ${(percent * 100).toFixed(0)}%`
                      }
                    >
                      <Cell fill="#f59e0b" />
                      <Cell fill={PIE_COLORS[1]} />
                    </Pie>
                    <Tooltip />
                  </PieChart>
                </ResponsiveContainer>
              </div>
            </div>
          </CardContent>
        </Card>
      )}

      {/* Benchmark Section */}
      <BenchmarkSection auditId={id} enabled={!!audit} />

      <LeadForm auditId={id} />
      <SubscriptionForm auditId={id} />
    </div>
  );
}
