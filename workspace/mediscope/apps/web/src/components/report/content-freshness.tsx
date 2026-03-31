"use client";

import { Clock } from "lucide-react";

interface TypeInfo {
  count: number;
  newest: string | null;
  freshness: string;
  pages_with_date: number;
}

interface Recommendation {
  priority: string;
  message: string;
}

interface ContentFreshnessData {
  overall_freshness_score: number;
  total_pages: number;
  pages_with_date: number;
  recent_6months: number;
  by_type: Record<string, TypeInfo>;
  freshness_rating: {
    good: number;
    moderate: number;
    stale: number;
    unknown: number;
  };
  recommendations: Recommendation[];
}

interface ContentFreshnessProps {
  data: ContentFreshnessData;
}

const TYPE_LABELS: Record<string, string> = {
  blog: "블로그/뉴스",
  procedure: "시술 소개",
  doctor: "의사 소개",
  price: "가격/비용",
  booking: "예약/상담",
  review: "후기/리뷰",
  event: "이벤트/프로모션",
  main: "메인 페이지",
  other: "기타",
};

const FRESHNESS_STYLES: Record<
  string,
  { bg: string; text: string; label: string; dot: string }
> = {
  good: {
    bg: "bg-green-50",
    text: "text-green-700",
    label: "최신",
    dot: "bg-green-500",
  },
  moderate: {
    bg: "bg-yellow-50",
    text: "text-yellow-700",
    label: "보통",
    dot: "bg-yellow-500",
  },
  stale: {
    bg: "bg-red-50",
    text: "text-red-700",
    label: "오래됨",
    dot: "bg-red-500",
  },
  unknown: {
    bg: "bg-slate-50",
    text: "text-slate-500",
    label: "불명",
    dot: "bg-slate-300",
  },
};

function ScoreCircle({ score }: { score: number }) {
  const color =
    score >= 70
      ? "text-green-600"
      : score >= 40
        ? "text-yellow-600"
        : "text-red-600";
  const bgColor =
    score >= 70 ? "bg-green-50" : score >= 40 ? "bg-yellow-50" : "bg-red-50";

  return (
    <div
      className={`flex h-14 w-14 items-center justify-center rounded-xl ${bgColor}`}
    >
      <span className={`text-xl font-bold tabular-nums ${color}`}>{score}</span>
    </div>
  );
}

function FreshnessBadge({ freshness }: { freshness: string }) {
  const style = FRESHNESS_STYLES[freshness] ?? FRESHNESS_STYLES.unknown;
  return (
    <span
      className={`inline-flex items-center gap-1.5 rounded-md px-2 py-0.5 text-xs font-medium ${style.bg} ${style.text}`}
    >
      <span className={`h-1.5 w-1.5 rounded-full ${style.dot}`} />
      {style.label}
    </span>
  );
}

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

function RatingBar({
  rating,
}: {
  rating: ContentFreshnessData["freshness_rating"];
}) {
  const total = rating.good + rating.moderate + rating.stale + rating.unknown;
  if (total === 0) return null;

  const segments = [
    { key: "good", count: rating.good, color: "bg-green-500" },
    { key: "moderate", count: rating.moderate, color: "bg-yellow-500" },
    { key: "stale", count: rating.stale, color: "bg-red-500" },
    { key: "unknown", count: rating.unknown, color: "bg-slate-300" },
  ];

  return (
    <div>
      <div className="flex h-3 w-full overflow-hidden rounded-full bg-slate-100">
        {segments.map(
          (seg) =>
            seg.count > 0 && (
              <div
                key={seg.key}
                className={`${seg.color} transition-all`}
                style={{ width: `${(seg.count / total) * 100}%` }}
              />
            ),
        )}
      </div>
      <div className="mt-2 flex flex-wrap gap-x-4 gap-y-1">
        {segments.map((seg) => (
          <div key={seg.key} className="flex items-center gap-1.5 text-xs">
            <span className={`h-2 w-2 rounded-full ${seg.color}`} />
            <span className="text-slate-600">
              {FRESHNESS_STYLES[seg.key]?.label ?? seg.key}
            </span>
            <span className="font-medium tabular-nums text-slate-900">
              {seg.count}
            </span>
          </div>
        ))}
      </div>
    </div>
  );
}

export function ContentFreshness({ data }: ContentFreshnessProps) {
  const typeEntries = Object.entries(data.by_type).sort(
    (a, b) => b[1].count - a[1].count,
  );

  return (
    <section className="mt-10">
      <div className="flex items-center gap-2 mb-4">
        <Clock className="h-5 w-5 text-slate-600" aria-hidden="true" />
        <h2 className="text-lg font-bold text-slate-900">콘텐츠 신선도</h2>
      </div>
      <div className="rounded-xl border border-slate-200 bg-white p-5 sm:p-6">
        {/* Overall score */}
        <div className="flex items-center gap-3 mb-6">
          <ScoreCircle score={data.overall_freshness_score} />
          <div>
            <p className="text-sm font-semibold text-slate-900">
              콘텐츠 신선도 점수
            </p>
            <p className="text-xs text-slate-500">
              {data.pages_with_date}/{data.total_pages} 페이지에서 날짜 감지
              &middot; 최근 6개월 이내 {data.recent_6months}개
            </p>
          </div>
        </div>

        {/* Rating distribution bar */}
        <div className="mb-6">
          <RatingBar rating={data.freshness_rating} />
        </div>

        {/* By-type table */}
        {typeEntries.length > 0 && (
          <div className="overflow-x-auto mb-6">
            <table className="w-full text-sm">
              <thead>
                <tr className="border-b border-slate-200">
                  <th className="py-2 pr-3 text-left font-medium text-slate-500">
                    페이지 유형
                  </th>
                  <th className="py-2 px-2 text-center font-medium text-slate-500">
                    수량
                  </th>
                  <th className="py-2 px-2 text-center font-medium text-slate-500">
                    최근 수정일
                  </th>
                  <th className="py-2 px-2 text-center font-medium text-slate-500">
                    상태
                  </th>
                </tr>
              </thead>
              <tbody>
                {typeEntries.map(([ptype, info]) => (
                  <tr
                    key={ptype}
                    className="border-b border-slate-100 last:border-0"
                  >
                    <td className="py-2.5 pr-3 text-slate-700">
                      {TYPE_LABELS[ptype] ?? ptype}
                    </td>
                    <td className="py-2.5 px-2 text-center tabular-nums text-slate-700">
                      {info.count}
                    </td>
                    <td className="py-2.5 px-2 text-center tabular-nums text-slate-500">
                      {info.newest ?? "-"}
                    </td>
                    <td className="py-2.5 px-2 text-center">
                      <FreshnessBadge freshness={info.freshness} />
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}

        {/* Recommendations */}
        {data.recommendations.length > 0 && (
          <div>
            <h3 className="text-sm font-semibold text-slate-900 mb-3">
              개선 권장사항
            </h3>
            <div className="space-y-2">
              {data.recommendations.map((rec, idx) => (
                <div
                  key={idx}
                  className="flex items-start gap-2.5 rounded-lg border border-slate-100 bg-slate-50 p-3"
                >
                  <PriorityBadge priority={rec.priority} />
                  <p className="text-sm text-slate-700">{rec.message}</p>
                </div>
              ))}
            </div>
          </div>
        )}
      </div>
    </section>
  );
}
