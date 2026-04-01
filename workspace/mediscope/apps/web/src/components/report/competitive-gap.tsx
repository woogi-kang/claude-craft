"use client";

interface GapItem {
  area: string;
  your_status: "present" | "missing" | "weak";
  competitor_rate: number;
  priority: "high" | "medium" | "low";
  recommendation: string;
}

interface CompetitiveGapData {
  gaps: GapItem[];
  overall_gap_score: number;
}

interface CompetitiveGapProps {
  data: CompetitiveGapData;
}

const STATUS_CONFIG: Record<
  string,
  { icon: string; label: string; iconClass: string }
> = {
  present: {
    icon: "✓",
    label: "보유",
    iconClass: "bg-green-100 text-green-600",
  },
  missing: {
    icon: "✗",
    label: "미보유",
    iconClass: "bg-red-100 text-red-600",
  },
  weak: {
    icon: "⚠",
    label: "부족",
    iconClass: "bg-yellow-100 text-yellow-600",
  },
};

const PRIORITY_STYLES: Record<string, string> = {
  high: "bg-red-50 text-red-700 border-red-200",
  medium: "bg-yellow-50 text-yellow-700 border-yellow-200",
  low: "bg-slate-50 text-slate-600 border-slate-200",
};

const PRIORITY_LABELS: Record<string, string> = {
  high: "높음",
  medium: "중간",
  low: "낮음",
};

function GapScoreRing({ score }: { score: number }) {
  const colorClass =
    score >= 80
      ? "text-green-600"
      : score >= 60
        ? "text-yellow-600"
        : score >= 40
          ? "text-orange-600"
          : "text-red-600";

  return (
    <div className="flex h-14 w-14 items-center justify-center rounded-xl bg-slate-100">
      <span className={`text-xl font-bold tabular-nums ${colorClass}`}>
        {score}
      </span>
    </div>
  );
}

export function CompetitiveGap({ data }: CompetitiveGapProps) {
  if (data.gaps.length === 0) return null;

  return (
    <section className="mt-10">
      <div className="flex items-center gap-2 mb-4">
        <h2 className="text-lg font-bold text-slate-900">경쟁 갭 분석</h2>
      </div>

      <div className="rounded-xl border border-slate-200 bg-white p-5 sm:p-6">
        {/* Overall gap score */}
        <div className="flex items-center gap-3 mb-6">
          <GapScoreRing score={data.overall_gap_score} />
          <div>
            <p className="text-sm font-semibold text-slate-900">
              경쟁력 갭 점수
            </p>
            <p className="text-xs text-slate-500">
              점수가 높을수록 경쟁사 대비 격차가 적음
            </p>
          </div>
        </div>

        {/* Gap items */}
        <div className="space-y-3">
          {data.gaps.map((gap, idx) => {
            const status =
              STATUS_CONFIG[gap.your_status] ?? STATUS_CONFIG.missing;

            return (
              <div
                key={idx}
                className="rounded-lg border border-slate-100 bg-slate-50 p-4"
              >
                <div className="flex items-start gap-3">
                  {/* Status icon */}
                  <span
                    className={`inline-flex h-7 w-7 shrink-0 items-center justify-center rounded-full text-sm font-bold ${status.iconClass}`}
                  >
                    {status.icon}
                  </span>

                  <div className="min-w-0 flex-1">
                    <div className="flex items-center gap-2 mb-1">
                      <span className="text-sm font-semibold text-slate-900">
                        {gap.area}
                      </span>
                      <span
                        className={`inline-flex items-center rounded-md border px-1.5 py-0.5 text-xs font-medium ${PRIORITY_STYLES[gap.priority] ?? PRIORITY_STYLES.low}`}
                      >
                        {PRIORITY_LABELS[gap.priority] ?? "낮음"}
                      </span>
                    </div>

                    {/* Competitor rate bar */}
                    <div className="mb-2">
                      <div className="flex items-center gap-2">
                        <div className="flex-1 h-2 rounded-full bg-slate-200 overflow-hidden">
                          <div
                            className="h-full rounded-full bg-slate-400 transition-all"
                            style={{
                              width: `${Math.min(100, gap.competitor_rate)}%`,
                            }}
                          />
                        </div>
                        <span className="text-xs font-medium tabular-nums text-slate-500 shrink-0">
                          경쟁사 {gap.competitor_rate}% 보유
                        </span>
                      </div>
                    </div>

                    {/* Recommendation */}
                    <p className="text-xs text-slate-600 leading-relaxed">
                      {gap.recommendation}
                    </p>
                  </div>
                </div>
              </div>
            );
          })}
        </div>

        {/* Legend */}
        <div className="flex items-center gap-4 mt-4 text-xs text-slate-400">
          <span className="flex items-center gap-1">
            <span className="inline-flex h-4 w-4 items-center justify-center rounded-full bg-green-100 text-green-600 text-[10px] font-bold">
              ✓
            </span>
            보유
          </span>
          <span className="flex items-center gap-1">
            <span className="inline-flex h-4 w-4 items-center justify-center rounded-full bg-yellow-100 text-yellow-600 text-[10px] font-bold">
              ⚠
            </span>
            부족
          </span>
          <span className="flex items-center gap-1">
            <span className="inline-flex h-4 w-4 items-center justify-center rounded-full bg-red-100 text-red-600 text-[10px] font-bold">
              ✗
            </span>
            미보유
          </span>
        </div>
      </div>
    </section>
  );
}
