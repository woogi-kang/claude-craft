"use client";

import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";

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
  google_jp: { flag: "🇯🇵", name: "일본 Google" },
  google_tw: { flag: "🇹🇼", name: "대만 Google" },
  google_sg: { flag: "🇸🇬", name: "싱가포르 Google" },
  google_my: { flag: "🇲🇾", name: "말레이시아 Google" },
  google_th: { flag: "🇹🇭", name: "태국 Google" },
  google_vn: { flag: "🇻🇳", name: "베트남 Google" },
  naver: { flag: "🇰🇷", name: "네이버" },
  baidu: { flag: "🇨🇳", name: "바이두" },
};

function getStatusBadge(result: IntlSearchResult) {
  if (result.error) {
    return {
      icon: "⬜",
      label: "미확인",
      colorClass: "text-gray-500 bg-gray-100",
      barColor: "bg-gray-300",
    };
  }
  if (result.rank === null || result.rank > 30) {
    return {
      icon: "❌",
      label: "미노출",
      colorClass: "text-red-600 bg-red-50",
      barColor: "bg-red-400",
    };
  }
  if (result.rank <= 10) {
    return {
      icon: "✅",
      label: `${result.rank}위`,
      colorClass: "text-green-600 bg-green-50",
      barColor: "bg-green-500",
    };
  }
  return {
    icon: "⚠️",
    label: `${result.rank}위`,
    colorClass: "text-yellow-600 bg-yellow-50",
    barColor: "bg-yellow-500",
  };
}

export function IntlSearchSection({ data }: IntlSearchSectionProps) {
  const exposedCount = Object.values(data.results).filter(
    (r) => !r.error && r.rank !== null && r.rank <= 30,
  ).length;

  return (
    <Card className="mt-8">
      <CardHeader>
        <CardTitle className="text-lg">해외 검색 노출 현황</CardTitle>
        <p className="text-sm text-muted-foreground">
          {data.engines_available}개 검색엔진 중 {data.engines_checked}개 체크,{" "}
          {exposedCount}개에서 노출 확인
        </p>
      </CardHeader>
      <CardContent>
        <div className="space-y-3">
          {Object.entries(data.results).map(([engineKey, result]) => {
            const country = COUNTRY_FLAGS[engineKey] ?? {
              flag: "🌐",
              name: engineKey,
            };
            const status = getStatusBadge(result);
            const scorePercent = Math.round(result.score * 100);

            return (
              <div key={engineKey} className="flex items-center gap-3">
                <span className="text-lg w-7 text-center shrink-0">
                  {country.flag}
                </span>
                <span className="text-sm font-medium w-32 shrink-0">
                  {country.name}
                </span>
                <span
                  className={`inline-flex items-center gap-1 rounded-full px-2.5 py-0.5 text-xs font-semibold w-20 justify-center shrink-0 ${status.colorClass}`}
                >
                  {status.icon} {status.label}
                </span>
                <div className="flex-1 h-2.5 rounded-full bg-muted overflow-hidden">
                  <div
                    className={`h-full rounded-full transition-all ${status.barColor}`}
                    style={{ width: `${scorePercent}%` }}
                  />
                </div>
                <span className="text-xs text-muted-foreground w-10 text-right shrink-0">
                  {result.error ? "" : `${scorePercent}%`}
                </span>
              </div>
            );
          })}
        </div>

        {data.summary && (
          <div className="mt-4 rounded-lg bg-blue-50 p-3 text-sm text-blue-800">
            <span className="font-medium">💡 권장:</span> {data.summary}
          </div>
        )}
      </CardContent>
    </Card>
  );
}
