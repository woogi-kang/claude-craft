"use client";

import { useQuery } from "@tanstack/react-query";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";

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

  return (
    <Card className="mt-8">
      <CardHeader>
        <CardTitle className="text-lg">경쟁사 벤치마크</CardTitle>
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
            <p className="text-sm text-muted-foreground mb-1">
              동일 지역 {benchmark.total_count}개 병원 대비
            </p>
            <p className="text-lg font-semibold text-primary">
              귀원은 상위{" "}
              <span className="text-2xl">
                {Math.max(1, 100 - benchmark.your_percentile)}%
              </span>
              에 위치합니다
            </p>
          </div>
        )}

        {/* Percentile bar */}
        <div className="space-y-2">
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

        {/* Stats */}
        <div className="mt-4 grid grid-cols-2 gap-3 sm:grid-cols-4">
          <div className="rounded-lg border p-3 text-center">
            <div className="text-lg font-bold text-green-600">
              {benchmark.top_25_avg}점
            </div>
            <div className="text-xs text-muted-foreground">상위 25% 평균</div>
          </div>
          <div className="rounded-lg border p-3 text-center">
            <div className="text-lg font-bold text-yellow-600">
              {benchmark.median}점
            </div>
            <div className="text-xs text-muted-foreground">중위값</div>
          </div>
          <div className="rounded-lg border p-3 text-center">
            <div className="text-lg font-bold text-red-600">
              {benchmark.bottom_25_avg}점
            </div>
            <div className="text-xs text-muted-foreground">하위 25% 평균</div>
          </div>
          {benchmark.your_score !== null && (
            <div className="rounded-lg border border-primary/30 bg-primary/5 p-3 text-center">
              <div className="text-lg font-bold text-primary">
                {benchmark.your_score}점
              </div>
              <div className="text-xs text-muted-foreground">귀원</div>
            </div>
          )}
        </div>
      </CardContent>
    </Card>
  );
}
