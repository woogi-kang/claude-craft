"use client";

import { useQuery } from "@tanstack/react-query";
import { BarChart3 } from "lucide-react";

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

interface BenchmarkSectionProps {
  auditId: string;
  enabled: boolean;
}

export function BenchmarkSection({ auditId, enabled }: BenchmarkSectionProps) {
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

  const regionLabel = benchmark.region
    ? `${benchmark.region.sido} ${benchmark.region.sggu ?? ""}`.trim()
    : "전체";

  return (
    <section className="mt-10">
      <div className="flex items-center gap-2 mb-4">
        <BarChart3 className="h-5 w-5 text-slate-600" aria-hidden="true" />
        <h2 className="text-lg font-bold text-slate-900">경쟁사 벤치마크</h2>
      </div>
      <div className="rounded-xl border border-slate-200 bg-white p-5 sm:p-6">
        <p className="text-sm text-slate-500 mb-4">
          {regionLabel} 지역 {benchmark.total_count}개 병원 대비 위치
        </p>

        {benchmark.your_percentile !== null && (
          <div className="mb-6 rounded-lg bg-slate-50 border border-slate-200 p-4 text-center">
            <p className="text-sm text-slate-500 mb-1">
              동일 지역 {benchmark.total_count}개 병원 대비
            </p>
            <p className="text-lg font-semibold text-slate-900">
              귀원은 상위{" "}
              <span className="text-2xl font-bold tabular-nums text-primary">
                {Math.max(1, 100 - benchmark.your_percentile)}%
              </span>
              에 위치합니다
            </p>
          </div>
        )}

        {/* Distribution bar */}
        <div className="space-y-2">
          <div className="flex justify-between text-xs text-slate-400">
            <span>하위</span>
            <span>상위</span>
          </div>
          <div className="relative h-10 w-full overflow-hidden rounded-lg bg-slate-100">
            <div
              className="absolute inset-y-0 left-0 bg-red-200/80"
              style={{ width: "25%" }}
            />
            <div
              className="absolute inset-y-0 bg-yellow-200/80"
              style={{ left: "25%", width: "50%" }}
            />
            <div
              className="absolute inset-y-0 right-0 bg-green-200/80"
              style={{ width: "25%" }}
            />
            {/* Labels inside zones */}
            <span className="absolute inset-y-0 left-[12.5%] -translate-x-1/2 flex items-center text-[10px] font-medium text-red-700/60">
              하위 25%
            </span>
            <span className="absolute inset-y-0 left-[50%] -translate-x-1/2 flex items-center text-[10px] font-medium text-yellow-700/60">
              중간
            </span>
            <span className="absolute inset-y-0 left-[87.5%] -translate-x-1/2 flex items-center text-[10px] font-medium text-green-700/60">
              상위 25%
            </span>
            {/* Position marker */}
            {benchmark.your_percentile !== null && (
              <div
                className="absolute inset-y-0 w-0.5 bg-slate-900 shadow-lg"
                style={{
                  left: `${Math.min(99, Math.max(1, benchmark.your_percentile))}%`,
                }}
              >
                <div className="absolute -top-7 left-1/2 -translate-x-1/2 whitespace-nowrap rounded-md bg-slate-900 px-2 py-1 text-xs font-bold text-white">
                  {benchmark.your_score}점
                  <div className="absolute top-full left-1/2 -translate-x-1/2 border-4 border-transparent border-t-slate-900" />
                </div>
              </div>
            )}
          </div>
        </div>

        {/* Stats grid */}
        <div className="mt-5 grid grid-cols-2 gap-3 sm:grid-cols-4">
          <div className="rounded-lg border border-green-200 bg-green-50 p-3 text-center">
            <div className="text-lg font-bold tabular-nums text-green-700">
              {benchmark.top_25_avg}점
            </div>
            <div className="text-xs text-green-600">상위 25% 평균</div>
          </div>
          <div className="rounded-lg border border-yellow-200 bg-yellow-50 p-3 text-center">
            <div className="text-lg font-bold tabular-nums text-yellow-700">
              {benchmark.median}점
            </div>
            <div className="text-xs text-yellow-600">중위값</div>
          </div>
          <div className="rounded-lg border border-red-200 bg-red-50 p-3 text-center">
            <div className="text-lg font-bold tabular-nums text-red-700">
              {benchmark.bottom_25_avg}점
            </div>
            <div className="text-xs text-red-600">하위 25% 평균</div>
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
      </div>
    </section>
  );
}
