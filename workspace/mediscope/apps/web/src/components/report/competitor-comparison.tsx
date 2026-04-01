"use client";

import type { Grade } from "@/lib/types";
import { GRADE_BADGE_COLORS } from "@/lib/report-config";

interface TopCompetitor {
  name: string;
  score: number | null;
  grade: string | null;
  domain: string | null;
}

interface PortalComparison {
  your: number;
  avg: number;
  top3_avg: number;
  gap: number;
}

interface CompetitorComparisonData {
  region_name: string;
  your_score: number | null;
  your_rank: number | null;
  total_competitors: number;
  competitors_with_score: number;
  regional_avg_score: number;
  top3_avg_score: number;
  top_competitors: TopCompetitor[];
  portal_comparison: Record<string, PortalComparison>;
  percentile: number;
  insight: string;
}

interface CompetitorComparisonProps {
  data: CompetitorComparisonData;
}

const PORTAL_LABELS: Record<string, string> = {
  google: "Google",
  naver: "Naver",
  baidu: "Baidu",
  yahoo_jp: "Yahoo! JP",
  ai_search: "AI 검색",
};

const PORTAL_ICON_COLORS: Record<string, string> = {
  google: "bg-blue-100 text-blue-700",
  naver: "bg-green-100 text-green-700",
  baidu: "bg-red-100 text-red-700",
  yahoo_jp: "bg-purple-100 text-purple-700",
  ai_search: "bg-slate-100 text-slate-700",
};

const PORTAL_ICONS: Record<string, string> = {
  google: "G",
  naver: "N",
  baidu: "B",
  yahoo_jp: "Y",
  ai_search: "AI",
};

const PORTAL_BAR_COLORS: Record<
  string,
  { your: string; avg: string; top3: string }
> = {
  google: { your: "bg-blue-500", avg: "bg-blue-200", top3: "bg-blue-300" },
  naver: { your: "bg-green-500", avg: "bg-green-200", top3: "bg-green-300" },
  baidu: { your: "bg-red-500", avg: "bg-red-200", top3: "bg-red-300" },
  yahoo_jp: {
    your: "bg-purple-500",
    avg: "bg-purple-200",
    top3: "bg-purple-300",
  },
  ai_search: {
    your: "bg-slate-500",
    avg: "bg-slate-200",
    top3: "bg-slate-300",
  },
};

function ScoreBar({
  score,
  maxScore = 100,
}: {
  score: number | null;
  maxScore?: number;
}) {
  if (score === null)
    return <div className="h-2 w-full rounded-full bg-slate-100" />;
  const pct = Math.min(100, Math.max(0, (score / maxScore) * 100));
  const colorClass =
    score >= 80
      ? "bg-green-500"
      : score >= 60
        ? "bg-yellow-500"
        : score >= 40
          ? "bg-orange-500"
          : "bg-red-500";

  return (
    <div className="h-2 w-full rounded-full bg-slate-100 overflow-hidden">
      <div
        className={`h-full rounded-full transition-all ${colorClass}`}
        style={{ width: `${pct}%` }}
      />
    </div>
  );
}

export function CompetitorComparison({ data }: CompetitorComparisonProps) {
  const portalKeys = Object.keys(data.portal_comparison);

  return (
    <section className="mt-10">
      <div className="flex items-center gap-2 mb-4">
        <h2 className="text-lg font-bold text-slate-900">
          {data.region_name} 경쟁 현황
        </h2>
        {data.your_rank !== null && (
          <span className="inline-flex items-center rounded-md border border-slate-300 bg-slate-50 px-2 py-0.5 text-xs font-bold text-slate-700">
            {data.total_competitors}곳 중 {data.your_rank}위
          </span>
        )}
      </div>

      <div className="rounded-xl border border-slate-200 bg-white p-5 sm:p-6">
        {/* Rank card + percentile */}
        <div className="flex items-center gap-4 mb-6">
          <div className="flex h-16 w-20 flex-col items-center justify-center rounded-xl bg-slate-100">
            <span className="text-2xl font-bold tabular-nums text-slate-900">
              {data.your_rank ?? "-"}
              <span className="text-sm font-normal text-slate-400">위</span>
            </span>
            <span className="text-xs text-slate-500">
              / {data.total_competitors}곳
            </span>
          </div>
          <div className="flex-1">
            <p className="text-sm font-medium text-slate-700 mb-1">
              상위 {Math.round(100 - data.percentile)}%
            </p>
            <div className="h-3 w-full rounded-full bg-slate-100 overflow-hidden">
              <div
                className="h-full rounded-full bg-slate-700 transition-all"
                style={{ width: `${data.percentile}%` }}
              />
            </div>
            <div className="flex justify-between mt-1">
              <span className="text-xs text-slate-400">하위</span>
              <span className="text-xs text-slate-400">상위</span>
            </div>
          </div>
        </div>

        {/* Score comparison row */}
        <div className="grid gap-3 sm:grid-cols-3 mb-6">
          <div className="rounded-lg border border-slate-200 bg-slate-50 p-3 text-center">
            <div className="text-2xl font-bold tabular-nums text-slate-900">
              {data.your_score ?? "-"}
            </div>
            <div className="text-xs text-slate-500 mt-0.5">귀원 점수</div>
          </div>
          <div className="rounded-lg border border-slate-200 bg-slate-50 p-3 text-center">
            <div className="text-2xl font-bold tabular-nums text-slate-500">
              {data.regional_avg_score}
            </div>
            <div className="text-xs text-slate-500 mt-0.5">지역 평균</div>
          </div>
          <div className="rounded-lg border border-slate-200 bg-slate-50 p-3 text-center">
            <div className="text-2xl font-bold tabular-nums text-slate-500">
              {data.top3_avg_score}
            </div>
            <div className="text-xs text-slate-500 mt-0.5">상위 3곳 평균</div>
          </div>
        </div>

        {/* Competitor table */}
        {data.top_competitors.length > 0 && (
          <div className="mb-6">
            <h3 className="text-sm font-semibold text-slate-900 mb-3">
              경쟁사 순위
            </h3>
            <div className="overflow-x-auto">
              <table className="w-full text-sm">
                <thead>
                  <tr className="border-b border-slate-200">
                    <th className="py-2 pr-2 text-left font-medium text-slate-500 w-10">
                      순위
                    </th>
                    <th className="py-2 px-2 text-left font-medium text-slate-500">
                      병원명
                    </th>
                    <th className="py-2 px-2 text-right font-medium text-slate-500 w-14">
                      점수
                    </th>
                    <th className="py-2 px-2 text-center font-medium text-slate-500 w-12">
                      등급
                    </th>
                    <th className="py-2 pl-2 font-medium text-slate-500 w-24"></th>
                  </tr>
                </thead>
                <tbody>
                  {data.top_competitors.map((comp, idx) => {
                    const isYou =
                      data.your_score !== null &&
                      comp.score === data.your_score &&
                      idx + 1 === data.your_rank;

                    return (
                      <tr
                        key={idx}
                        className={`border-b border-slate-100 last:border-0 ${isYou ? "bg-blue-50" : ""}`}
                      >
                        <td className="py-2.5 pr-2 tabular-nums text-slate-600 font-medium">
                          {idx + 1}
                        </td>
                        <td className="py-2.5 px-2 text-slate-700 font-medium truncate max-w-[180px]">
                          {comp.name}
                          {isYou && (
                            <span className="ml-1.5 text-xs text-blue-600 font-bold">
                              ← 귀원
                            </span>
                          )}
                        </td>
                        <td className="py-2.5 px-2 text-right tabular-nums text-slate-700 font-semibold">
                          {comp.score ?? "-"}
                        </td>
                        <td className="py-2.5 px-2 text-center">
                          {comp.grade && (
                            <span
                              className={`inline-flex items-center rounded-md border px-1.5 py-0.5 text-xs font-bold ${GRADE_BADGE_COLORS[comp.grade as Grade] ?? "bg-slate-100 text-slate-600 border-slate-300"}`}
                            >
                              {comp.grade}
                            </span>
                          )}
                        </td>
                        <td className="py-2.5 pl-2">
                          <ScoreBar score={comp.score} />
                        </td>
                      </tr>
                    );
                  })}
                </tbody>
              </table>
            </div>
          </div>
        )}

        {/* Portal comparison bars */}
        {portalKeys.length > 0 && (
          <div className="mb-6">
            <h3 className="text-sm font-semibold text-slate-900 mb-3">
              포털별 비교
            </h3>
            <div className="space-y-4">
              {portalKeys.map((portal) => {
                const pc = data.portal_comparison[portal];
                const maxVal = Math.max(pc.your, pc.avg, pc.top3_avg, 1);
                const colors = PORTAL_BAR_COLORS[portal] ?? {
                  your: "bg-slate-500",
                  avg: "bg-slate-200",
                  top3: "bg-slate-300",
                };

                return (
                  <div key={portal}>
                    <div className="flex items-center gap-2 mb-1.5">
                      <div
                        className={`flex h-6 w-6 shrink-0 items-center justify-center rounded text-xs font-bold ${PORTAL_ICON_COLORS[portal] ?? "bg-slate-100 text-slate-700"}`}
                      >
                        {PORTAL_ICONS[portal] ?? portal[0].toUpperCase()}
                      </div>
                      <span className="text-sm font-medium text-slate-700">
                        {PORTAL_LABELS[portal] ?? portal}
                      </span>
                    </div>
                    <div className="space-y-1 pl-8">
                      <div className="flex items-center gap-2">
                        <span className="text-xs text-slate-500 w-14 shrink-0">
                          귀원
                        </span>
                        <div className="flex-1 h-2.5 rounded-full bg-slate-50 overflow-hidden">
                          <div
                            className={`h-full rounded-full ${colors.your}`}
                            style={{ width: `${(pc.your / maxVal) * 100}%` }}
                          />
                        </div>
                        <span className="text-xs font-semibold tabular-nums text-slate-700 w-8 text-right">
                          {pc.your}
                        </span>
                      </div>
                      <div className="flex items-center gap-2">
                        <span className="text-xs text-slate-500 w-14 shrink-0">
                          평균
                        </span>
                        <div className="flex-1 h-2.5 rounded-full bg-slate-50 overflow-hidden">
                          <div
                            className={`h-full rounded-full ${colors.avg}`}
                            style={{ width: `${(pc.avg / maxVal) * 100}%` }}
                          />
                        </div>
                        <span className="text-xs font-semibold tabular-nums text-slate-500 w-8 text-right">
                          {pc.avg}
                        </span>
                      </div>
                      <div className="flex items-center gap-2">
                        <span className="text-xs text-slate-500 w-14 shrink-0">
                          상위3
                        </span>
                        <div className="flex-1 h-2.5 rounded-full bg-slate-50 overflow-hidden">
                          <div
                            className={`h-full rounded-full ${colors.top3}`}
                            style={{
                              width: `${(pc.top3_avg / maxVal) * 100}%`,
                            }}
                          />
                        </div>
                        <span className="text-xs font-semibold tabular-nums text-slate-500 w-8 text-right">
                          {pc.top3_avg}
                        </span>
                      </div>
                    </div>
                  </div>
                );
              })}
            </div>

            {/* Legend */}
            <div className="flex items-center gap-4 mt-3 pl-8 text-xs text-slate-400">
              <span className="flex items-center gap-1">
                <span className="inline-block h-2 w-4 rounded bg-slate-500" />
                귀원
              </span>
              <span className="flex items-center gap-1">
                <span className="inline-block h-2 w-4 rounded bg-slate-200" />
                지역 평균
              </span>
              <span className="flex items-center gap-1">
                <span className="inline-block h-2 w-4 rounded bg-slate-300" />
                상위 3곳
              </span>
            </div>
          </div>
        )}

        {/* Insight */}
        {data.insight && (
          <div className="rounded-lg border border-blue-100 bg-blue-50 p-3">
            <p className="text-sm text-blue-800">{data.insight}</p>
          </div>
        )}
      </div>
    </section>
  );
}
