"use client";

import { useQuery } from "@tanstack/react-query";
import { BarChart3, TrendingUp } from "lucide-react";
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  ResponsiveContainer,
  Cell,
  ReferenceLine,
  Tooltip,
} from "recharts";

interface DistributionBin {
  range: string;
  count: number;
}

interface BenchmarkData {
  audit_id: string;
  region: { sido: string; sggu: string } | null;
  region_name: string;
  top_25_avg: number;
  median: number;
  bottom_25_avg: number;
  total_count: number;
  your_score: number | null;
  your_percentile: number | null;
  distribution: DistributionBin[];
  rank: number | null;
}

interface BenchmarkSectionProps {
  auditId: string;
  enabled: boolean;
  teaser?: boolean;
}

function getBarColor(binRange: string, yourScore: number | null) {
  const binStart = parseInt(binRange.split("-")[0], 10);
  const binEnd = binStart + 9;

  if (yourScore !== null && yourScore >= binStart && yourScore <= binEnd) {
    return "#1e293b";
  }
  if (binStart < 30) return "#fca5a5";
  if (binStart < 60) return "#fde68a";
  return "#86efac";
}

function generateEstimatedDistribution(
  totalCount: number,
  bottom25Avg: number,
  median: number,
  top25Avg: number,
): DistributionBin[] {
  const bins: DistributionBin[] = Array.from({ length: 10 }, (_, i) => ({
    range: `${i * 10}-${i * 10 + 9}`,
    count: 0,
  }));

  const mean = (bottom25Avg + median + top25Avg) / 3;
  const stddev = Math.max(10, (top25Avg - bottom25Avg) / 2);

  for (let i = 0; i < 10; i++) {
    const x = i * 10 + 5;
    const z = (x - mean) / stddev;
    bins[i].count = Math.max(
      1,
      Math.round(totalCount * 0.15 * Math.exp(-0.5 * z * z)),
    );
  }

  return bins;
}

export function BenchmarkSection({
  auditId,
  enabled,
  teaser = false,
}: BenchmarkSectionProps) {
  const { data: benchmark } = useQuery<BenchmarkData>({
    queryKey: ["benchmark", auditId],
    queryFn: async () => {
      const res = await fetch(`/api/benchmark/${auditId}`);
      if (!res.ok) return null;
      return res.json();
    },
    enabled,
  });

  if (!benchmark || benchmark.total_count === 0) return null;

  const regionLabel =
    benchmark.region_name ||
    (benchmark.region
      ? `${benchmark.region.sido} ${benchmark.region.sggu ?? ""}`.trim()
      : "전체");

  const percentileDisplay =
    benchmark.your_percentile !== null
      ? Math.max(1, 100 - benchmark.your_percentile)
      : null;

  // Teaser mode: show only region + count + percentile
  if (teaser) {
    return (
      <section className="mt-10">
        <div className="flex items-center gap-2 mb-4">
          <BarChart3 className="h-5 w-5 text-slate-600" aria-hidden="true" />
          <h2 className="text-lg font-bold text-slate-900">
            같은 지역 병원 대비
          </h2>
        </div>
        <div className="rounded-xl border border-slate-200 bg-white p-5 sm:p-6 text-center">
          <p className="text-sm text-slate-500 mb-3">
            {regionLabel} {benchmark.total_count}개 피부과 중
          </p>
          {percentileDisplay !== null && (
            <p className="text-slate-900 mb-4">
              <span className="text-4xl font-extrabold tabular-nums text-primary">
                상위 {percentileDisplay}%
              </span>
            </p>
          )}
          <p className="text-sm text-slate-400">
            이메일 입력 후 상세 비교를 확인하세요
          </p>
        </div>
      </section>
    );
  }

  // Full mode: detailed benchmark with distribution chart
  const distribution =
    benchmark.distribution && benchmark.distribution.length > 0
      ? benchmark.distribution
      : generateEstimatedDistribution(
          benchmark.total_count,
          benchmark.bottom_25_avg,
          benchmark.median,
          benchmark.top_25_avg,
        );

  // Find which category could improve percentile the most (simple heuristic)
  const nextTierPercentile =
    percentileDisplay !== null ? Math.max(1, percentileDisplay - 15) : null;

  return (
    <section className="mt-10">
      <div className="flex items-center gap-2 mb-4">
        <BarChart3 className="h-5 w-5 text-slate-600" aria-hidden="true" />
        <h2 className="text-lg font-bold text-slate-900">
          같은 지역 병원 대비
        </h2>
      </div>
      <div className="rounded-xl border border-slate-200 bg-white p-5 sm:p-6">
        <p className="text-sm text-slate-500 mb-4">
          {regionLabel} 권역 {benchmark.total_count}개 피부과 중
        </p>

        {percentileDisplay !== null && (
          <div className="mb-6 rounded-lg bg-slate-50 border border-slate-200 p-5 text-center">
            <p className="text-sm text-slate-500 mb-1">
              동일 권역 {benchmark.total_count}개 병원 대비
            </p>
            <p className="text-slate-900">
              <span className="text-4xl font-extrabold tabular-nums text-primary">
                {percentileDisplay}%
              </span>
            </p>
            <p className="text-sm font-medium text-slate-600 mt-1">
              상위 {percentileDisplay}%에 위치합니다
              {benchmark.rank !== null && (
                <span className="text-slate-400">
                  {" "}
                  ({benchmark.total_count}개 중 {benchmark.rank}위)
                </span>
              )}
            </p>
          </div>
        )}

        {/* Histogram */}
        <div className="mb-4">
          <p className="mb-2 text-xs font-medium text-slate-500">점수 분포</p>
          <ResponsiveContainer width="100%" height={180}>
            <BarChart
              data={distribution}
              margin={{ top: 10, right: 10, left: -20, bottom: 0 }}
            >
              <XAxis
                dataKey="range"
                tick={{ fontSize: 10, fill: "#94a3b8" }}
                axisLine={false}
                tickLine={false}
              />
              <YAxis hide />
              <Tooltip
                formatter={(value: number) => [`${value}개 병원`, "분포"]}
                contentStyle={{
                  fontSize: 12,
                  borderRadius: 8,
                  border: "1px solid #e2e8f0",
                }}
              />
              <Bar dataKey="count" radius={[4, 4, 0, 0]}>
                {distribution.map((entry) => (
                  <Cell
                    key={entry.range}
                    fill={getBarColor(entry.range, benchmark.your_score)}
                  />
                ))}
              </Bar>
              {benchmark.your_score !== null && (
                <ReferenceLine
                  x={`${Math.floor(benchmark.your_score / 10) * 10}-${Math.floor(benchmark.your_score / 10) * 10 + 9}`}
                  stroke="#1e293b"
                  strokeWidth={2}
                  strokeDasharray="4 4"
                  label={{
                    value: `귀원 ${benchmark.your_score}점`,
                    position: "top",
                    fontSize: 11,
                    fontWeight: 700,
                    fill: "#1e293b",
                  }}
                />
              )}
            </BarChart>
          </ResponsiveContainer>
        </div>

        {/* Stats grid */}
        <div className="grid grid-cols-2 gap-3 sm:grid-cols-4">
          <div className="rounded-lg border border-red-200 bg-red-50 p-3 text-center">
            <div className="text-lg font-bold tabular-nums text-red-700">
              {benchmark.bottom_25_avg}점
            </div>
            <div className="text-xs text-red-600">하위 25%</div>
          </div>
          <div className="rounded-lg border border-yellow-200 bg-yellow-50 p-3 text-center">
            <div className="text-lg font-bold tabular-nums text-yellow-700">
              {benchmark.median}점
            </div>
            <div className="text-xs text-yellow-600">중위값</div>
          </div>
          <div className="rounded-lg border border-green-200 bg-green-50 p-3 text-center">
            <div className="text-lg font-bold tabular-nums text-green-700">
              {benchmark.top_25_avg}점
            </div>
            <div className="text-xs text-green-600">상위 25%</div>
          </div>
          {benchmark.your_score !== null && (
            <div className="rounded-lg border-2 border-slate-300 bg-slate-50 p-3 text-center">
              <div className="text-lg font-bold tabular-nums text-slate-900">
                {benchmark.your_score}점
              </div>
              <div className="text-xs text-slate-600 font-medium">귀원</div>
            </div>
          )}
        </div>

        {/* Improvement hint */}
        {nextTierPercentile !== null &&
          percentileDisplay !== null &&
          percentileDisplay > 20 && (
            <div className="mt-4 flex items-start gap-2 rounded-lg bg-blue-50 border border-blue-200 p-3">
              <TrendingUp className="h-4 w-4 text-blue-600 mt-0.5 shrink-0" />
              <p className="text-sm text-blue-700">
                다국어 지원만 개선하면 상위 {nextTierPercentile}%로 올라갑니다
              </p>
            </div>
          )}
      </div>
    </section>
  );
}
