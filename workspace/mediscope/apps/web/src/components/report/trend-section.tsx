"use client";

import { useState } from "react";
import { useQuery } from "@tanstack/react-query";
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  Tooltip as RechartsTooltip,
  ResponsiveContainer,
  CartesianGrid,
} from "recharts";
import {
  TrendingUp,
  TrendingDown,
  Minus,
  CheckCircle,
  Circle,
} from "lucide-react";
import { CATEGORY_LABELS } from "@/lib/types";
import type { Grade } from "@/lib/types";
import { GRADE_BADGE_COLORS } from "@/lib/report-config";

const PERIODS = [
  { label: "30일", value: "30d" },
  { label: "90일", value: "90d" },
  { label: "180일", value: "180d" },
  { label: "1년", value: "1y" },
] as const;

const CATEGORY_COLORS: Record<string, string> = {
  technical_seo: "#6366f1",
  performance: "#f59e0b",
  geo_aeo: "#10b981",
  multilingual: "#ec4899",
  competitiveness: "#8b5cf6",
};

interface TrendHistoryEntry {
  scanned_at: string;
  total_score: number;
  grade: Grade;
  category_scores: Record<string, number>;
}

interface TrendChanges {
  total: {
    current: number;
    previous: number;
    delta: number;
    direction: "up" | "down" | "same";
  };
  by_category: Record<
    string,
    { current: number; previous: number; delta: number }
  >;
}

interface TrendData {
  hospital_id: string;
  history: TrendHistoryEntry[];
  changes: TrendChanges | null;
  improved_items: string[];
  declined_items: string[];
  unchanged_items: string[];
}

interface TrendSectionProps {
  hospitalId: string;
  enabled: boolean;
}

function formatDate(iso: string) {
  const d = new Date(iso);
  return `${d.getMonth() + 1}/${d.getDate()}`;
}

function formatFullDate(iso: string) {
  const d = new Date(iso);
  return `${d.getFullYear()}.${String(d.getMonth() + 1).padStart(2, "0")}.${String(d.getDate()).padStart(2, "0")}`;
}

function DeltaBadge({ delta }: { delta: number }) {
  if (delta > 0) {
    return (
      <span className="inline-flex items-center gap-0.5 text-sm font-semibold text-green-600">
        <TrendingUp className="h-4 w-4" />+{delta}
      </span>
    );
  }
  if (delta < 0) {
    return (
      <span className="inline-flex items-center gap-0.5 text-sm font-semibold text-red-600">
        <TrendingDown className="h-4 w-4" />
        {delta}
      </span>
    );
  }
  return (
    <span className="inline-flex items-center gap-0.5 text-sm font-semibold text-slate-400">
      <Minus className="h-4 w-4" />0
    </span>
  );
}

// eslint-disable-next-line @typescript-eslint/no-explicit-any
function CustomTooltip({ active, payload, label }: any) {
  if (!active || !payload?.length) return null;
  return (
    <div className="rounded-lg border border-slate-200 bg-white p-3 shadow-lg">
      <p className="text-xs font-medium text-slate-500 mb-1.5">
        {formatFullDate(label)}
      </p>
      {payload.map((p: { name: string; value: number; color: string }) => (
        <div key={p.name} className="flex items-center gap-2 text-sm">
          <span
            className="h-2 w-2 rounded-full"
            style={{ backgroundColor: p.color }}
          />
          <span className="text-slate-600">{p.name}</span>
          <span className="ml-auto font-semibold tabular-nums">{p.value}</span>
        </div>
      ))}
    </div>
  );
}

export function TrendSection({ hospitalId, enabled }: TrendSectionProps) {
  const [period, setPeriod] = useState("90d");
  const [visibleCategories, setVisibleCategories] = useState<Set<string>>(
    new Set(),
  );

  const { data: trend } = useQuery<TrendData>({
    queryKey: ["trend", hospitalId, period],
    queryFn: async () => {
      const res = await fetch(`/api/trend/${hospitalId}?period=${period}`);
      if (!res.ok) throw new Error("Failed to fetch trend");
      return res.json();
    },
    enabled,
  });

  // Don't render if less than 2 data points
  if (!trend || trend.history.length < 2) return null;

  const chartData = trend.history.map((entry) => {
    const point: Record<string, string | number> = {
      date: entry.scanned_at,
      종합: entry.total_score,
    };
    for (const cat of visibleCategories) {
      const label = CATEGORY_LABELS[cat as keyof typeof CATEGORY_LABELS] ?? cat;
      point[label] = entry.category_scores[cat] ?? 0;
    }
    return point;
  });

  const toggleCategory = (cat: string) => {
    setVisibleCategories((prev) => {
      const next = new Set(prev);
      if (next.has(cat)) next.delete(cat);
      else next.add(cat);
      return next;
    });
  };

  const allCategories = Object.keys(
    trend.history[trend.history.length - 1].category_scores,
  );

  return (
    <section className="mt-10">
      <div className="flex items-center justify-between mb-4">
        <h2 className="text-lg font-bold text-slate-900">점수 변화 추이</h2>
        <div className="flex gap-1 rounded-lg border border-slate-200 bg-white p-0.5">
          {PERIODS.map((p) => (
            <button
              key={p.value}
              onClick={() => setPeriod(p.value)}
              className={`rounded-md px-2.5 py-1 text-xs font-medium transition-colors ${
                period === p.value
                  ? "bg-slate-900 text-white"
                  : "text-slate-500 hover:text-slate-700"
              }`}
            >
              {p.label}
            </button>
          ))}
        </div>
      </div>

      <div className="rounded-xl border border-slate-200 bg-white p-5 sm:p-6">
        {/* Chart */}
        <ResponsiveContainer width="100%" height={260}>
          <LineChart data={chartData}>
            <CartesianGrid strokeDasharray="3 3" stroke="#f1f5f9" />
            <XAxis
              dataKey="date"
              tickFormatter={formatDate}
              tick={{ fontSize: 12, fill: "#94a3b8" }}
              axisLine={false}
              tickLine={false}
            />
            <YAxis
              domain={[0, 100]}
              tick={{ fontSize: 12, fill: "#94a3b8" }}
              axisLine={false}
              tickLine={false}
              width={32}
            />
            <RechartsTooltip content={<CustomTooltip />} />
            <Line
              type="monotone"
              dataKey="종합"
              stroke="#334155"
              strokeWidth={2.5}
              dot={{ fill: "#334155", r: 3 }}
              activeDot={{ r: 5 }}
            />
            {allCategories
              .filter((cat) => visibleCategories.has(cat))
              .map((cat) => {
                const label =
                  CATEGORY_LABELS[cat as keyof typeof CATEGORY_LABELS] ?? cat;
                return (
                  <Line
                    key={cat}
                    type="monotone"
                    dataKey={label}
                    stroke={CATEGORY_COLORS[cat] ?? "#94a3b8"}
                    strokeWidth={1.5}
                    strokeDasharray="4 2"
                    dot={false}
                  />
                );
              })}
          </LineChart>
        </ResponsiveContainer>

        {/* Category toggles */}
        <div className="mt-4 flex flex-wrap gap-2">
          {allCategories.map((cat) => {
            const label =
              CATEGORY_LABELS[cat as keyof typeof CATEGORY_LABELS] ?? cat;
            const active = visibleCategories.has(cat);
            return (
              <button
                key={cat}
                onClick={() => toggleCategory(cat)}
                className={`inline-flex items-center gap-1.5 rounded-full border px-3 py-1 text-xs font-medium transition-colors ${
                  active
                    ? "border-slate-300 bg-slate-100 text-slate-700"
                    : "border-slate-200 bg-white text-slate-400 hover:text-slate-600"
                }`}
              >
                <span
                  className="h-2 w-2 rounded-full"
                  style={{
                    backgroundColor: active
                      ? (CATEGORY_COLORS[cat] ?? "#94a3b8")
                      : "#cbd5e1",
                  }}
                />
                {label}
              </button>
            );
          })}
        </div>

        {/* Changes summary */}
        {trend.changes && (
          <div className="mt-6 grid gap-4 sm:grid-cols-2">
            {/* Score change card */}
            <div className="rounded-lg border border-slate-200 bg-slate-50 p-4">
              <p className="text-sm font-medium text-slate-500 mb-2">
                이전 스캔 대비
              </p>
              <div className="flex items-baseline gap-3">
                <span className="text-3xl font-bold tabular-nums text-slate-900">
                  {trend.changes.total.current}
                </span>
                <DeltaBadge delta={trend.changes.total.delta} />
              </div>
              <div className="mt-1 text-xs text-slate-400">
                이전: {trend.changes.total.previous}점
                {trend.history.length >= 2 && (
                  <>
                    {" "}
                    &middot;{" "}
                    {(() => {
                      const prevEntry = trend.history[trend.history.length - 2];
                      const currEntry = trend.history[trend.history.length - 1];
                      const prevGrade = prevEntry.grade;
                      const currGrade = currEntry.grade;
                      if (prevGrade !== currGrade) {
                        return `${prevGrade}→${currGrade} 등급 변화`;
                      }
                      return `${currGrade}등급 유지`;
                    })()}
                  </>
                )}
              </div>
              {/* Per-category deltas */}
              <div className="mt-3 space-y-1">
                {Object.entries(trend.changes.by_category).map(([key, val]) => {
                  const label =
                    CATEGORY_LABELS[key as keyof typeof CATEGORY_LABELS] ?? key;
                  return (
                    <div
                      key={key}
                      className="flex items-center justify-between text-xs"
                    >
                      <span className="text-slate-500">{label}</span>
                      <DeltaBadge delta={val.delta} />
                    </div>
                  );
                })}
              </div>
            </div>

            {/* Improved / unchanged items */}
            <div className="rounded-lg border border-slate-200 bg-slate-50 p-4">
              <p className="text-sm font-medium text-slate-500 mb-2">
                변화 항목
              </p>
              {trend.improved_items.length > 0 && (
                <div className="mb-2">
                  <p className="text-xs font-medium text-green-600 mb-1">
                    개선됨
                  </p>
                  {trend.improved_items.map((item) => (
                    <div
                      key={item}
                      className="flex items-center gap-1.5 text-xs text-slate-600"
                    >
                      <CheckCircle className="h-3 w-3 text-green-500" />
                      {CATEGORY_LABELS[item as keyof typeof CATEGORY_LABELS] ??
                        item}
                    </div>
                  ))}
                </div>
              )}
              {trend.declined_items.length > 0 && (
                <div className="mb-2">
                  <p className="text-xs font-medium text-red-600 mb-1">하락</p>
                  {trend.declined_items.map((item) => (
                    <div
                      key={item}
                      className="flex items-center gap-1.5 text-xs text-slate-600"
                    >
                      <TrendingDown className="h-3 w-3 text-red-500" />
                      {CATEGORY_LABELS[item as keyof typeof CATEGORY_LABELS] ??
                        item}
                    </div>
                  ))}
                </div>
              )}
              {trend.unchanged_items.length > 0 && (
                <div>
                  <p className="text-xs font-medium text-slate-400 mb-1">
                    변화 없음
                  </p>
                  {trend.unchanged_items.map((item) => (
                    <div
                      key={item}
                      className="flex items-center gap-1.5 text-xs text-slate-400"
                    >
                      <Circle className="h-3 w-3" />
                      {CATEGORY_LABELS[item as keyof typeof CATEGORY_LABELS] ??
                        item}
                    </div>
                  ))}
                </div>
              )}
              {trend.improved_items.length === 0 &&
                trend.declined_items.length === 0 &&
                trend.unchanged_items.length === 0 && (
                  <p className="text-xs text-slate-400">변화 항목이 없습니다</p>
                )}
            </div>
          </div>
        )}
      </div>
    </section>
  );
}
