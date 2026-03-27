"use client";

import { Globe } from "lucide-react";

interface IntlSearchResult {
  rank: number | null;
  score: number;
  query: string;
  error?: string;
}

interface IntlSearchData {
  engines_checked: number;
  engines_available: number;
  results: Record<string, IntlSearchResult>;
  summary: string;
}

interface IntlSearchSectionProps {
  data: IntlSearchData;
}

const COUNTRY_FLAGS: Record<string, { flag: string; name: string }> = {
  google_jp: { flag: "\u{1F1EF}\u{1F1F5}", name: "일본 Google" },
  google_tw: { flag: "\u{1F1F9}\u{1F1FC}", name: "대만 Google" },
  google_sg: { flag: "\u{1F1F8}\u{1F1EC}", name: "싱가포르 Google" },
  google_my: { flag: "\u{1F1F2}\u{1F1FE}", name: "말레이시아 Google" },
  google_th: { flag: "\u{1F1F9}\u{1F1ED}", name: "태국 Google" },
  google_vn: { flag: "\u{1F1FB}\u{1F1F3}", name: "베트남 Google" },
  naver: { flag: "\u{1F1F0}\u{1F1F7}", name: "네이버" },
  baidu: { flag: "\u{1F1E8}\u{1F1F3}", name: "바이두" },
};

function getStatusBadge(result: IntlSearchResult) {
  if (result.error) {
    return {
      label: "미확인",
      colorClass: "text-slate-500 bg-slate-100 border-slate-200",
      barColor: "bg-slate-300",
    };
  }
  if (result.rank === null || result.rank > 30) {
    return {
      label: "미노출",
      colorClass: "text-red-600 bg-red-50 border-red-200",
      barColor: "bg-red-400",
    };
  }
  if (result.rank <= 10) {
    return {
      label: `${result.rank}위`,
      colorClass: "text-green-600 bg-green-50 border-green-200",
      barColor: "bg-green-500",
    };
  }
  return {
    label: `${result.rank}위`,
    colorClass: "text-yellow-600 bg-yellow-50 border-yellow-200",
    barColor: "bg-yellow-500",
  };
}

export function IntlSearchSection({ data }: IntlSearchSectionProps) {
  const exposedCount = Object.values(data.results).filter(
    (r) => !r.error && r.rank !== null && r.rank <= 30,
  ).length;

  return (
    <section className="mt-10">
      <div className="flex items-center gap-2 mb-4">
        <Globe className="h-5 w-5 text-slate-600" aria-hidden="true" />
        <h2 className="text-lg font-bold text-slate-900">
          해외 검색 노출 현황
        </h2>
      </div>
      <div className="rounded-xl border border-slate-200 bg-white p-5 sm:p-6">
        <p className="text-sm text-slate-500 mb-4">
          {data.engines_available}개 검색엔진 중 {data.engines_checked}개 체크,{" "}
          {exposedCount}개에서 노출 확인
        </p>
        <div className="space-y-3">
          {Object.entries(data.results).map(([engineKey, result]) => {
            const country = COUNTRY_FLAGS[engineKey] ?? {
              flag: "\u{1F310}",
              name: engineKey,
            };
            const status = getStatusBadge(result);
            const scorePercent = Math.round(result.score * 100);

            return (
              <div key={engineKey} className="flex items-center gap-3">
                <span className="text-lg w-7 text-center shrink-0">
                  {country.flag}
                </span>
                <span className="text-sm font-medium w-32 shrink-0 text-slate-700">
                  {country.name}
                </span>
                <span
                  className={`inline-flex items-center rounded-md border px-2 py-0.5 text-xs font-semibold w-16 justify-center shrink-0 ${status.colorClass}`}
                >
                  {status.label}
                </span>
                <div className="flex-1 h-2 rounded-full bg-slate-100 overflow-hidden">
                  <div
                    className={`h-full rounded-full transition-all ${status.barColor}`}
                    style={{ width: `${scorePercent}%` }}
                  />
                </div>
                <span className="text-xs text-slate-400 w-10 text-right shrink-0 tabular-nums">
                  {result.error ? "" : `${scorePercent}%`}
                </span>
              </div>
            );
          })}
        </div>

        {data.summary && (
          <div className="mt-5 rounded-lg bg-blue-50 border border-blue-200 p-3.5 text-sm text-blue-800">
            <span className="font-semibold">권장:</span> {data.summary}
          </div>
        )}
      </div>
    </section>
  );
}
