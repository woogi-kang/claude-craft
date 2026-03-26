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
  PieChart,
  Pie,
} from "recharts";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Badge } from "@/components/ui/badge";
import type { Audit, Category } from "@/lib/types";
import { CATEGORY_LABELS, GRADE_COLORS, getGrade } from "@/lib/types";

const BAR_COLORS = ["#4f46e5", "#0ea5e9", "#8b5cf6", "#f59e0b", "#10b981"];
const PIE_COLORS = ["#4f46e5", "#e5e7eb"];

interface BenchmarkData {
  audit_id: string;
  region: { sido: string; sggu: string } | null;
  top_25_avg: number;
  median: number;
  bottom_25_avg: number;
  total_count: number;
  your_score: number | null;
  your_percentile: number | null;
}

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

  const { data: benchmark } = useQuery<BenchmarkData>({
    queryKey: ["benchmark", id],
    queryFn: async () => {
      const res = await fetch(`/api/benchmark/${id}`);
      if (!res.ok) return null;
      return res.json();
    },
    enabled: !!audit,
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

  const chartData = Object.entries(categoryScores).map(
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
        <a
          href={`/api/reports/${id}`}
          target="_blank"
          rel="noopener noreferrer"
          className="inline-flex items-center gap-2 rounded-md bg-primary px-4 py-2 text-sm font-medium text-primary-foreground hover:bg-primary/90"
        >
          상세 리포트 보기 / 인쇄
        </a>
      </div>
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
      {benchmark && benchmark.total_count > 0 && (
        <Card className="mt-8">
          <CardHeader>
            <CardTitle className="text-lg">지역 벤치마크</CardTitle>
            <p className="text-sm text-muted-foreground">
              {benchmark.region
                ? `${benchmark.region.sido} ${benchmark.region.sggu ?? ""} 지역`
                : "전체"}{" "}
              {benchmark.total_count}개 병원 대비 위치
            </p>
          </CardHeader>
          <CardContent>
            {benchmark.your_percentile !== null && (
              <div className="mb-6 rounded-lg bg-primary/5 p-4 text-center">
                <p className="text-lg font-semibold text-primary">
                  귀원은 동일 지역 상위{" "}
                  <span className="text-2xl">
                    {Math.max(1, 100 - benchmark.your_percentile)}%
                  </span>
                  에 위치합니다
                </p>
              </div>
            )}
            <div className="space-y-3">
              {/* Distribution bar */}
              <div className="space-y-2">
                <div className="flex justify-between text-sm text-muted-foreground">
                  <span>하위 25% 평균: {benchmark.bottom_25_avg}점</span>
                  <span>중위값: {benchmark.median}점</span>
                  <span>상위 25% 평균: {benchmark.top_25_avg}점</span>
                </div>
                <div className="relative h-8 w-full overflow-hidden rounded-full bg-muted">
                  {/* Bottom 25% zone */}
                  <div
                    className="absolute inset-y-0 left-0 bg-red-200"
                    style={{ width: "25%" }}
                  />
                  {/* Middle 50% zone */}
                  <div
                    className="absolute inset-y-0 bg-yellow-200"
                    style={{ left: "25%", width: "50%" }}
                  />
                  {/* Top 25% zone */}
                  <div
                    className="absolute inset-y-0 right-0 bg-green-200"
                    style={{ width: "25%" }}
                  />
                  {/* Your position marker */}
                  {benchmark.your_percentile !== null && (
                    <div
                      className="absolute inset-y-0 w-1 bg-primary shadow-md"
                      style={{
                        left: `${Math.min(99, Math.max(1, benchmark.your_percentile))}%`,
                      }}
                    >
                      <div className="absolute -top-6 left-1/2 -translate-x-1/2 whitespace-nowrap rounded bg-primary px-2 py-0.5 text-xs text-primary-foreground">
                        {benchmark.your_score}점
                      </div>
                    </div>
                  )}
                </div>
              </div>
            </div>
          </CardContent>
        </Card>
      )}

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
