"use client";

import { Search, Zap, ShieldCheck, Globe, Bot } from "lucide-react";
import type { CheckItemData } from "@/lib/report-config";
import {
  REPORT_CATEGORIES,
  computeCategoryScore,
  getScoreStatus,
} from "@/lib/report-config";

const ICON_MAP: Record<string, typeof Search> = {
  Search,
  Zap,
  ShieldCheck,
  Globe,
  Bot,
};

interface CategorySummaryProps {
  categoryScores: Record<string, CheckItemData>;
}

export function CategorySummary({ categoryScores }: CategorySummaryProps) {
  return (
    <section className="mt-8">
      <h2 className="mb-4 text-lg font-bold text-slate-900">카테고리별 점수</h2>
      <div className="grid grid-cols-2 gap-3 sm:grid-cols-5">
        {REPORT_CATEGORIES.map((cat) => {
          const Icon = ICON_MAP[cat.icon] ?? Search;
          const { score } = computeCategoryScore(cat.items, categoryScores);
          const status = getScoreStatus(score);

          return (
            <div
              key={cat.key}
              className={`rounded-xl border p-4 text-center ${status.borderClass} ${status.bgClass}`}
            >
              <div
                className={`mx-auto flex h-9 w-9 items-center justify-center rounded-lg bg-white/60`}
              >
                <Icon
                  className={`h-5 w-5 ${status.colorClass}`}
                  aria-hidden="true"
                />
              </div>
              <p className="mt-2 text-xs font-medium text-slate-700 leading-tight">
                {cat.label}
              </p>
              <p
                className={`mt-1 text-xl font-bold tabular-nums ${status.colorClass}`}
              >
                {score}
                <span className="text-xs font-normal text-slate-400">점</span>
              </p>
              <div className="mt-2 h-1.5 w-full rounded-full bg-white/60">
                <div
                  className={`h-full rounded-full transition-all duration-700 ${status.barClass}`}
                  style={{
                    width: `${Math.min(100, Math.max(0, score))}%`,
                  }}
                />
              </div>
            </div>
          );
        })}
      </div>
    </section>
  );
}
