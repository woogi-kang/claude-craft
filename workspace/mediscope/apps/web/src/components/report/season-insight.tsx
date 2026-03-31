"use client";

import { CalendarDays } from "lucide-react";

interface CalendarEntry {
  month: number;
  demand: number;
  level: string;
}

interface Opportunity {
  country: string;
  label: string;
  flag: string;
  demand: number;
  level: string;
  reason: string;
}

interface UpcomingPeak {
  country: string;
  label: string;
  flag: string;
  month: number;
  month_name: string;
  demand: number;
  level: string;
  reason: string;
  days_until: number;
}

interface MarketingAction {
  priority: string;
  country: string;
  message: string;
}

interface QuarterlyForecast {
  next_quarter: string;
  top_market: string;
  expected_demand: string;
}

interface SeasonInsightData {
  current_month: number;
  current_month_name: string;
  calendar: Record<string, CalendarEntry[]>;
  current_opportunities: Opportunity[];
  upcoming_peaks: UpcomingPeak[];
  marketing_actions: MarketingAction[];
  quarterly_forecast: QuarterlyForecast;
}

interface SeasonInsightProps {
  data: SeasonInsightData;
}

const DEMAND_COLORS: Record<string, string> = {
  very_low: "bg-slate-100 text-slate-400",
  low: "bg-blue-50 text-blue-400",
  moderate: "bg-yellow-50 text-yellow-600",
  high: "bg-orange-100 text-orange-600",
  peak: "bg-red-100 text-red-600 font-bold",
};

const DEMAND_BG_ONLY: Record<string, string> = {
  very_low: "bg-slate-100",
  low: "bg-blue-50",
  moderate: "bg-yellow-100",
  high: "bg-orange-200",
  peak: "bg-red-300",
};

const MONTH_LABELS = [
  "1",
  "2",
  "3",
  "4",
  "5",
  "6",
  "7",
  "8",
  "9",
  "10",
  "11",
  "12",
];

function PriorityBadge({ priority }: { priority: string }) {
  const styles =
    priority === "high"
      ? "bg-red-50 text-red-700 border-red-200"
      : priority === "medium"
        ? "bg-yellow-50 text-yellow-700 border-yellow-200"
        : "bg-slate-50 text-slate-600 border-slate-200";
  const label =
    priority === "high" ? "높음" : priority === "medium" ? "중간" : "낮음";

  return (
    <span
      className={`inline-flex items-center rounded-md border px-1.5 py-0.5 text-xs font-medium ${styles}`}
    >
      {label}
    </span>
  );
}

function DemandBar({ demand }: { demand: number }) {
  return (
    <div className="flex gap-0.5">
      {[1, 2, 3, 4, 5].map((i) => (
        <div
          key={i}
          className={`h-2 w-3 rounded-sm ${
            i <= demand
              ? demand >= 5
                ? "bg-red-400"
                : demand >= 4
                  ? "bg-orange-400"
                  : demand >= 3
                    ? "bg-yellow-400"
                    : "bg-blue-300"
              : "bg-slate-200"
          }`}
        />
      ))}
    </div>
  );
}

export function SeasonInsight({ data }: SeasonInsightProps) {
  const countryEntries = Object.entries(data.calendar);

  return (
    <section className="mt-10">
      <div className="flex items-center gap-2 mb-4">
        <CalendarDays className="h-5 w-5 text-slate-600" aria-hidden="true" />
        <h2 className="text-lg font-bold text-slate-900">
          의료관광 시즌 인사이트
        </h2>
      </div>
      <div className="rounded-xl border border-slate-200 bg-white p-5 sm:p-6">
        {/* Heatmap Table */}
        <div className="mb-6">
          <h3 className="text-sm font-semibold text-slate-900 mb-3">
            국가별 월별 수요 히트맵
          </h3>
          <div className="overflow-x-auto">
            <table className="w-full text-xs">
              <thead>
                <tr>
                  <th className="text-left py-1.5 px-2 text-slate-500 font-medium w-20">
                    국가
                  </th>
                  {MONTH_LABELS.map((label, idx) => (
                    <th
                      key={idx}
                      className={`py-1.5 px-1 text-center font-medium w-8 ${
                        idx + 1 === data.current_month
                          ? "text-blue-700 bg-blue-50 rounded-t-md"
                          : "text-slate-500"
                      }`}
                    >
                      {label}월
                    </th>
                  ))}
                </tr>
              </thead>
              <tbody>
                {countryEntries.map(([code, months]) => {
                  const info = months;
                  const countryData =
                    data.current_opportunities.find(
                      (o) => o.country === code,
                    ) ?? data.upcoming_peaks.find((p) => p.country === code);
                  const flag =
                    countryData?.flag ??
                    { jp: "🇯🇵", cn: "🇨🇳", us: "🇺🇸", th: "🇹🇭", vn: "🇻🇳" }[
                      code
                    ] ??
                    "";
                  const label =
                    countryData?.label ??
                    {
                      jp: "일본",
                      cn: "중국",
                      us: "미국",
                      th: "태국",
                      vn: "베트남",
                    }[code] ??
                    code;

                  return (
                    <tr key={code} className="border-t border-slate-100">
                      <td className="py-1.5 px-2 text-slate-700 font-medium whitespace-nowrap">
                        {flag} {label}
                      </td>
                      {info.map((entry, idx) => (
                        <td
                          key={idx}
                          className={`py-1.5 px-1 text-center ${
                            idx + 1 === data.current_month
                              ? "bg-blue-50 border-x border-blue-200"
                              : ""
                          }`}
                        >
                          <span
                            className={`inline-flex items-center justify-center h-6 w-6 rounded text-xs ${
                              DEMAND_COLORS[entry.level] ??
                              "bg-slate-100 text-slate-400"
                            }`}
                          >
                            {entry.demand}
                          </span>
                        </td>
                      ))}
                    </tr>
                  );
                })}
              </tbody>
            </table>
          </div>
          <div className="flex items-center gap-3 mt-2 text-xs text-slate-500">
            <span>수요:</span>
            {[
              { level: "very_low", label: "1 매우 낮음" },
              { level: "low", label: "2 낮음" },
              { level: "moderate", label: "3 보통" },
              { level: "high", label: "4 높음" },
              { level: "peak", label: "5 성수기" },
            ].map(({ level, label }) => (
              <span key={level} className="flex items-center gap-1">
                <span
                  className={`inline-block h-3 w-3 rounded ${
                    DEMAND_BG_ONLY[level] ?? "bg-slate-100"
                  }`}
                />
                {label}
              </span>
            ))}
          </div>
        </div>

        {/* Current Opportunities */}
        {data.current_opportunities.length > 0 && (
          <div className="mb-6">
            <h3 className="text-sm font-semibold text-slate-900 mb-3">
              지금 기회 ({data.current_month_name})
            </h3>
            <div className="grid gap-2 sm:grid-cols-2">
              {data.current_opportunities.map((opp) => (
                <div
                  key={opp.country}
                  className="flex items-center gap-3 rounded-lg border border-orange-200 bg-orange-50 p-3"
                >
                  <span className="text-2xl">{opp.flag}</span>
                  <div className="flex-1 min-w-0">
                    <div className="flex items-center gap-2">
                      <span className="text-sm font-semibold text-slate-900">
                        {opp.label}
                      </span>
                      <DemandBar demand={opp.demand} />
                    </div>
                    {opp.reason && (
                      <p className="text-xs text-orange-700 mt-0.5">
                        {opp.reason}
                      </p>
                    )}
                  </div>
                  <span
                    className={`text-xs font-medium px-2 py-0.5 rounded-full ${
                      opp.level === "peak"
                        ? "bg-red-100 text-red-700"
                        : "bg-orange-100 text-orange-700"
                    }`}
                  >
                    {opp.level === "peak" ? "성수기" : "높음"}
                  </span>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* Upcoming Peaks */}
        {data.upcoming_peaks.length > 0 && (
          <div className="mb-6">
            <h3 className="text-sm font-semibold text-slate-900 mb-3">
              다가오는 성수기 (3개월 내)
            </h3>
            <div className="space-y-2">
              {data.upcoming_peaks.map((peak, idx) => (
                <div
                  key={`${peak.country}-${peak.month}-${idx}`}
                  className="flex items-center gap-3 rounded-lg border border-slate-100 bg-slate-50 p-3"
                >
                  <span className="text-lg">{peak.flag}</span>
                  <div className="flex-1 min-w-0">
                    <div className="flex items-center gap-2">
                      <span className="text-sm font-medium text-slate-700">
                        {peak.label}
                      </span>
                      <span className="text-xs text-slate-500">
                        {peak.month_name}
                      </span>
                      <DemandBar demand={peak.demand} />
                    </div>
                    {peak.reason && (
                      <p className="text-xs text-slate-500 mt-0.5">
                        {peak.reason}
                      </p>
                    )}
                  </div>
                  <span className="text-xs font-medium text-blue-600 bg-blue-50 px-2 py-0.5 rounded-full whitespace-nowrap">
                    D-{peak.days_until}
                  </span>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* Marketing Actions */}
        {data.marketing_actions.length > 0 && (
          <div className="mb-6">
            <h3 className="text-sm font-semibold text-slate-900 mb-3">
              마케팅 액션 플랜
            </h3>
            <div className="space-y-2">
              {data.marketing_actions.map((action, idx) => (
                <div
                  key={idx}
                  className="flex items-start gap-2.5 rounded-lg border border-slate-100 bg-slate-50 p-3"
                >
                  <PriorityBadge priority={action.priority} />
                  <p className="text-sm text-slate-700">{action.message}</p>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* Quarterly Forecast */}
        {data.quarterly_forecast.top_market && (
          <div className="rounded-lg border border-indigo-100 bg-indigo-50 p-3">
            <p className="text-xs text-indigo-700">
              <span className="font-semibold">
                {data.quarterly_forecast.next_quarter} 전망:
              </span>{" "}
              {data.quarterly_forecast.expected_demand}
            </p>
          </div>
        )}
      </div>
    </section>
  );
}
