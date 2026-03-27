"use client";

import { useState } from "react";
import {
  Search,
  Zap,
  ShieldCheck,
  Globe,
  Bot,
  ChevronDown,
  ChevronUp,
} from "lucide-react";
import type { CheckItemData } from "@/lib/report-config";
import {
  REPORT_CATEGORIES,
  computeCategoryScore,
  getScoreStatus,
} from "@/lib/report-config";
import { CheckItemCard } from "./check-item-card";

const ICON_MAP: Record<string, typeof Search> = {
  Search,
  Zap,
  ShieldCheck,
  Globe,
  Bot,
};

interface CategoryAccordionProps {
  categoryScores: Record<string, CheckItemData>;
  /** Index of the first category to be open by default (e.g. worst) */
  defaultOpenIndex?: number;
}

export function CategoryAccordion({
  categoryScores,
  defaultOpenIndex = 0,
}: CategoryAccordionProps) {
  const [openIndices, setOpenIndices] = useState<Set<number>>(
    new Set([defaultOpenIndex]),
  );

  function toggleCategory(idx: number) {
    setOpenIndices((prev) => {
      const next = new Set(prev);
      if (next.has(idx)) next.delete(idx);
      else next.add(idx);
      return next;
    });
  }

  return (
    <section className="mt-10">
      <h2 className="text-lg font-bold text-slate-900 mb-4">
        카테고리별 상세 진단
      </h2>
      <div className="space-y-3">
        {REPORT_CATEGORIES.map((cat, idx) => {
          const Icon = ICON_MAP[cat.icon] ?? Search;
          const { score, measured, total } = computeCategoryScore(
            cat.items,
            categoryScores,
          );
          const status = getScoreStatus(score);
          const isOpen = openIndices.has(idx);
          const unmeasured = total - measured;

          return (
            <div
              key={cat.key}
              className="rounded-xl border border-slate-200 bg-white overflow-hidden"
            >
              <button
                type="button"
                onClick={() => toggleCategory(idx)}
                className="flex w-full items-center gap-3 p-4 sm:p-5 text-left hover:bg-slate-50 transition-colors focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-slate-500"
                aria-expanded={isOpen}
              >
                <div
                  className={`flex h-9 w-9 shrink-0 items-center justify-center rounded-lg ${status.bgClass}`}
                >
                  <Icon
                    className={`h-5 w-5 ${status.colorClass}`}
                    aria-hidden="true"
                  />
                </div>
                <div className="flex-1 min-w-0">
                  <div className="flex items-center gap-2">
                    <span className="font-semibold text-slate-900">
                      {cat.label}
                    </span>
                    {unmeasured > 0 && (
                      <span className="text-xs text-slate-400">
                        ({unmeasured}/{total} 측정불가)
                      </span>
                    )}
                  </div>
                  <div className="flex items-center gap-3 mt-1.5">
                    <div className="flex-1 h-2 rounded-full bg-slate-100">
                      <div
                        className={`h-full rounded-full transition-all duration-500 ${status.barClass}`}
                        style={{
                          width: `${Math.min(100, Math.max(0, score))}%`,
                        }}
                      />
                    </div>
                    <span
                      className={`text-sm font-bold tabular-nums shrink-0 ${status.colorClass}`}
                    >
                      {score}점
                    </span>
                  </div>
                </div>
                <div className="shrink-0 ml-2">
                  {isOpen ? (
                    <ChevronUp
                      className="h-5 w-5 text-slate-400"
                      aria-hidden="true"
                    />
                  ) : (
                    <ChevronDown
                      className="h-5 w-5 text-slate-400"
                      aria-hidden="true"
                    />
                  )}
                </div>
              </button>
              {isOpen && (
                <div className="border-t border-slate-100 bg-slate-50/50 p-4 sm:p-5">
                  <p className="text-sm text-slate-500 mb-4">
                    {cat.description}
                  </p>
                  <div className="space-y-2">
                    {cat.items.map((itemKey) => {
                      const item = categoryScores[itemKey];
                      if (!item) return null;
                      return (
                        <CheckItemCard
                          key={itemKey}
                          itemKey={itemKey}
                          data={item}
                        />
                      );
                    })}
                  </div>
                </div>
              )}
            </div>
          );
        })}
      </div>
    </section>
  );
}
