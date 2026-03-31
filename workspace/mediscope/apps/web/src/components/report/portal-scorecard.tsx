"use client";

import type { Grade } from "@/lib/types";
import { GRADE_BADGE_COLORS, getScoreStatus } from "@/lib/report-config";

interface PortalScore {
  score: number;
  grade: string;
  label: string;
  issues: string[];
  checks_measured: number;
  checks_total: number;
}

interface PortalScorecardProps {
  portalScores: Record<string, PortalScore>;
}

const PORTAL_ORDER = ["google", "naver", "baidu", "yahoo_jp", "ai_search"];

const PORTAL_ICONS: Record<string, string> = {
  google: "G",
  naver: "N",
  baidu: "B",
  yahoo_jp: "Y",
  ai_search: "AI",
};

const PORTAL_ICON_COLORS: Record<string, string> = {
  google: "bg-blue-100 text-blue-700",
  naver: "bg-green-100 text-green-700",
  baidu: "bg-red-100 text-red-700",
  yahoo_jp: "bg-purple-100 text-purple-700",
  ai_search: "bg-slate-100 text-slate-700",
};

export function PortalScorecard({ portalScores }: PortalScorecardProps) {
  if (!portalScores || Object.keys(portalScores).length === 0) return null;

  const portals = PORTAL_ORDER.filter((key) => portalScores[key]);

  return (
    <section className="mt-8">
      <h2 className="mb-4 text-lg font-bold text-slate-900">포털별 SEO 점수</h2>
      <div className="space-y-3">
        {portals.map((key) => {
          const portal = portalScores[key];
          const grade = portal.grade as Grade;
          const status = getScoreStatus(portal.score);

          return (
            <div
              key={key}
              className={`rounded-xl border p-4 sm:p-5 ${status.borderClass} ${status.bgClass}`}
            >
              <div className="flex items-center gap-3 sm:gap-4">
                {/* Portal icon */}
                <div
                  className={`flex h-10 w-10 shrink-0 items-center justify-center rounded-lg text-sm font-bold ${PORTAL_ICON_COLORS[key]}`}
                >
                  {PORTAL_ICONS[key]}
                </div>

                {/* Name + score bar */}
                <div className="min-w-0 flex-1">
                  <div className="flex items-center justify-between gap-2">
                    <span className="text-sm font-semibold text-slate-900 truncate">
                      {portal.label}
                    </span>
                    <div className="flex items-center gap-2 shrink-0">
                      <span
                        className={`text-lg font-bold tabular-nums ${status.colorClass}`}
                      >
                        {portal.score}
                        <span className="text-xs font-normal text-slate-400">
                          /100
                        </span>
                      </span>
                      <span
                        className={`inline-flex items-center rounded-md border px-2 py-0.5 text-xs font-bold ${GRADE_BADGE_COLORS[grade] ?? "bg-slate-100 text-slate-600 border-slate-300"}`}
                      >
                        {grade}
                      </span>
                    </div>
                  </div>

                  {/* Progress bar */}
                  <div className="mt-2 h-2 w-full rounded-full bg-white/60">
                    <div
                      className={`h-full rounded-full transition-all duration-700 ${status.barClass}`}
                      style={{
                        width: `${Math.min(100, Math.max(0, portal.score))}%`,
                      }}
                    />
                  </div>

                  {/* Issues */}
                  {portal.issues.length > 0 && (
                    <div className="mt-2 space-y-0.5">
                      {portal.issues.map((issue, i) => (
                        <p
                          key={i}
                          className="text-xs text-slate-500 leading-relaxed truncate"
                        >
                          {issue}
                        </p>
                      ))}
                    </div>
                  )}
                </div>
              </div>
            </div>
          );
        })}
      </div>
    </section>
  );
}
