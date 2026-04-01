"use client";

interface KeywordResult {
  keyword: string;
  language: string;
  naver: { rank: number | null; cached: boolean } | null;
  google: { rank: number | null; cached: boolean } | null;
}

interface KeywordSummary {
  naver_avg_rank: number | null;
  google_avg_rank: number | null;
  keywords_found_naver: number;
  keywords_found_google: number;
  keywords_total: number;
  best_keyword: { keyword: string; portal: string; rank: number } | null;
  worst_keyword: {
    keyword: string;
    portal: string;
    rank: number | null;
  } | null;
}

interface SerpCompetitor {
  domain: string;
  name: string;
  appearances: number;
  avg_rank: number;
}

interface KeywordRankingsData {
  results: KeywordResult[];
  summary: KeywordSummary;
  competitors_in_serp: SerpCompetitor[];
}

interface KeywordRankingsProps {
  data: KeywordRankingsData;
}

const LANG_FLAGS: Record<string, string> = {
  ko: "\uD83C\uDDF0\uD83C\uDDF7",
  en: "\uD83C\uDDFA\uD83C\uDDF8",
  ja: "\uD83C\uDDEF\uD83C\uDDF5",
  zh: "\uD83C\uDDE8\uD83C\uDDF3",
};

function RankBadge({
  rank,
}: {
  rank: number | null | undefined;
  portalAvailable?: boolean;
}) {
  if (rank === undefined) {
    return <span className="text-xs text-slate-300">-</span>;
  }
  if (rank === null) {
    return (
      <span className="inline-flex items-center rounded-md border border-slate-200 bg-slate-50 px-2 py-0.5 text-xs font-medium text-slate-400">
        미노출
      </span>
    );
  }
  if (rank <= 3) {
    return (
      <span className="inline-flex items-center rounded-md border border-green-300 bg-green-100 px-2 py-0.5 text-xs font-bold text-green-800">
        {rank}위
      </span>
    );
  }
  if (rank <= 10) {
    return (
      <span className="inline-flex items-center rounded-md border border-yellow-300 bg-yellow-100 px-2 py-0.5 text-xs font-bold text-yellow-800">
        {rank}위
      </span>
    );
  }
  if (rank <= 20) {
    return (
      <span className="inline-flex items-center rounded-md border border-orange-300 bg-orange-100 px-2 py-0.5 text-xs font-bold text-orange-800">
        {rank}위
      </span>
    );
  }
  return (
    <span className="inline-flex items-center rounded-md border border-red-300 bg-red-100 px-2 py-0.5 text-xs font-bold text-red-800">
      20+
    </span>
  );
}

export function KeywordRankings({ data }: KeywordRankingsProps) {
  const { results, summary, competitors_in_serp } = data;

  if (results.length === 0) return null;

  return (
    <section className="mt-10">
      <div className="flex items-center gap-2 mb-4">
        <h2 className="text-lg font-bold text-slate-900">키워드 검색 순위</h2>
      </div>

      <div className="rounded-xl border border-slate-200 bg-white p-5 sm:p-6">
        {/* Summary cards */}
        <div className="grid gap-3 sm:grid-cols-2 mb-6">
          <div className="rounded-lg border border-green-200 bg-green-50 p-4 text-center">
            <div className="flex items-center justify-center gap-1.5 mb-1">
              <span className="flex h-6 w-6 items-center justify-center rounded bg-green-100 text-xs font-bold text-green-700">
                N
              </span>
              <span className="text-sm font-medium text-green-700">Naver</span>
            </div>
            <div className="text-2xl font-bold tabular-nums text-green-800">
              {summary.naver_avg_rank !== null
                ? `${summary.naver_avg_rank.toFixed(1)}위`
                : "-"}
            </div>
            <div className="text-xs text-green-600 mt-0.5">
              {summary.keywords_found_naver}/{summary.keywords_total} 키워드
              노출
            </div>
          </div>
          <div className="rounded-lg border border-blue-200 bg-blue-50 p-4 text-center">
            <div className="flex items-center justify-center gap-1.5 mb-1">
              <span className="flex h-6 w-6 items-center justify-center rounded bg-blue-100 text-xs font-bold text-blue-700">
                G
              </span>
              <span className="text-sm font-medium text-blue-700">Google</span>
            </div>
            <div className="text-2xl font-bold tabular-nums text-blue-800">
              {summary.google_avg_rank !== null
                ? `${summary.google_avg_rank.toFixed(1)}위`
                : "-"}
            </div>
            <div className="text-xs text-blue-600 mt-0.5">
              {summary.keywords_found_google}/{summary.keywords_total} 키워드
              노출
            </div>
          </div>
        </div>

        {/* Best/Worst keyword */}
        {(summary.best_keyword || summary.worst_keyword) && (
          <div className="grid gap-3 sm:grid-cols-2 mb-6">
            {summary.best_keyword && (
              <div className="flex items-center gap-2 rounded-lg border border-slate-100 bg-slate-50 p-3">
                <span className="text-xs text-slate-500">최고</span>
                <span className="text-sm font-medium text-slate-700 truncate">
                  {summary.best_keyword.keyword}
                </span>
                <RankBadge rank={summary.best_keyword.rank} />
              </div>
            )}
            {summary.worst_keyword && (
              <div className="flex items-center gap-2 rounded-lg border border-slate-100 bg-slate-50 p-3">
                <span className="text-xs text-slate-500">최저</span>
                <span className="text-sm font-medium text-slate-700 truncate">
                  {summary.worst_keyword.keyword}
                </span>
                <RankBadge rank={summary.worst_keyword.rank} />
              </div>
            )}
          </div>
        )}

        {/* Matrix table */}
        <div className="overflow-x-auto mb-6">
          <table className="w-full text-sm">
            <thead>
              <tr className="border-b border-slate-200">
                <th className="py-2 pr-3 text-left font-medium text-slate-500">
                  키워드
                </th>
                <th className="py-2 px-2 text-center font-medium text-slate-500">
                  <span className="flex items-center justify-center gap-1">
                    <span className="flex h-5 w-5 items-center justify-center rounded bg-green-100 text-xs font-bold text-green-700">
                      N
                    </span>
                  </span>
                </th>
                <th className="py-2 px-2 text-center font-medium text-slate-500">
                  <span className="flex items-center justify-center gap-1">
                    <span className="flex h-5 w-5 items-center justify-center rounded bg-blue-100 text-xs font-bold text-blue-700">
                      G
                    </span>
                  </span>
                </th>
              </tr>
            </thead>
            <tbody>
              {results.map((result, idx) => (
                <tr
                  key={idx}
                  className="border-b border-slate-100 last:border-0"
                >
                  <td className="py-2.5 pr-3 text-slate-700 font-medium">
                    <span className="mr-1.5">
                      {LANG_FLAGS[result.language] ?? ""}
                    </span>
                    {result.keyword}
                  </td>
                  <td className="py-2.5 px-2 text-center">
                    <RankBadge
                      rank={
                        result.naver === null ? undefined : result.naver.rank
                      }
                    />
                  </td>
                  <td className="py-2.5 px-2 text-center">
                    <RankBadge
                      rank={
                        result.google === null ? undefined : result.google.rank
                      }
                    />
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>

        {/* Legend */}
        <div className="flex flex-wrap items-center gap-3 mb-6 text-xs text-slate-400">
          <span className="flex items-center gap-1">
            <span className="inline-block h-3 w-6 rounded bg-green-100 border border-green-300" />
            1-3위
          </span>
          <span className="flex items-center gap-1">
            <span className="inline-block h-3 w-6 rounded bg-yellow-100 border border-yellow-300" />
            4-10위
          </span>
          <span className="flex items-center gap-1">
            <span className="inline-block h-3 w-6 rounded bg-orange-100 border border-orange-300" />
            11-20위
          </span>
          <span className="flex items-center gap-1">
            <span className="inline-block h-3 w-6 rounded bg-red-100 border border-red-300" />
            20위+
          </span>
          <span className="flex items-center gap-1">
            <span className="inline-block h-3 w-6 rounded bg-slate-50 border border-slate-200" />
            미노출
          </span>
        </div>

        {/* SERP Competitors */}
        {competitors_in_serp.length > 0 && (
          <div>
            <h3 className="text-sm font-semibold text-slate-900 mb-3">
              SERP에서 만나는 경쟁사
            </h3>
            <div className="space-y-2">
              {competitors_in_serp.map((comp, idx) => (
                <div
                  key={idx}
                  className="flex items-center gap-3 rounded-lg border border-slate-100 bg-slate-50 p-3"
                >
                  <div className="min-w-0 flex-1">
                    <p className="text-sm font-medium text-slate-700 truncate">
                      {comp.name}
                    </p>
                    <p className="text-xs text-slate-400 truncate">
                      {comp.domain}
                    </p>
                  </div>
                  <div className="flex items-center gap-3 shrink-0">
                    <div className="text-center">
                      <div className="text-sm font-bold tabular-nums text-slate-700">
                        {comp.appearances}
                      </div>
                      <div className="text-xs text-slate-400">키워드</div>
                    </div>
                    <div className="text-center">
                      <div className="text-sm font-bold tabular-nums text-slate-700">
                        {comp.avg_rank.toFixed(1)}
                      </div>
                      <div className="text-xs text-slate-400">평균순위</div>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}
      </div>
    </section>
  );
}
