"use client";

import { ClipboardCheck } from "lucide-react";

interface ProcedureInfo {
  name: string;
  pages_found: number;
  sections: Record<string, boolean>;
  partial_sections: string[];
  completeness: number;
  content_length: number;
}

interface Recommendation {
  procedure: string;
  procedure_name: string;
  missing: string[];
  priority: string;
  message: string;
}

interface ProcedureCompletenessData {
  procedures: Record<string, ProcedureInfo>;
  overall_completeness: number;
  best_procedure: string | null;
  worst_procedure: string | null;
  recommendations: Recommendation[];
}

interface ProcedureCompletenessProps {
  data: ProcedureCompletenessData;
}

const SECTION_LABELS: Record<string, string> = {
  description: "설명",
  process: "과정",
  price: "가격",
  review: "후기",
  before_after: "전후",
  faq: "FAQ",
};

const SECTION_KEYS = [
  "description",
  "process",
  "price",
  "review",
  "before_after",
  "faq",
];

function SectionIcon({
  present,
  partial,
}: {
  present: boolean;
  partial: boolean;
}) {
  if (present && !partial) {
    return (
      <span className="inline-flex h-6 w-6 items-center justify-center rounded-full bg-green-100 text-green-600">
        <svg
          className="h-3.5 w-3.5"
          fill="none"
          viewBox="0 0 24 24"
          stroke="currentColor"
          strokeWidth={3}
        >
          <path
            strokeLinecap="round"
            strokeLinejoin="round"
            d="M5 13l4 4L19 7"
          />
        </svg>
      </span>
    );
  }
  if (present && partial) {
    return (
      <span className="inline-flex h-6 w-6 items-center justify-center rounded-full bg-yellow-100 text-yellow-600">
        <svg
          className="h-3.5 w-3.5"
          fill="none"
          viewBox="0 0 24 24"
          stroke="currentColor"
          strokeWidth={3}
        >
          <path
            strokeLinecap="round"
            strokeLinejoin="round"
            d="M12 9v3m0 4h.01"
          />
        </svg>
      </span>
    );
  }
  return (
    <span className="inline-flex h-6 w-6 items-center justify-center rounded-full bg-red-100 text-red-400">
      <svg
        className="h-3.5 w-3.5"
        fill="none"
        viewBox="0 0 24 24"
        stroke="currentColor"
        strokeWidth={3}
      >
        <path
          strokeLinecap="round"
          strokeLinejoin="round"
          d="M6 18L18 6M6 6l12 12"
        />
      </svg>
    </span>
  );
}

function CompletenessBar({ score }: { score: number }) {
  const colorClass =
    score >= 80
      ? "bg-green-500"
      : score >= 50
        ? "bg-yellow-500"
        : score > 0
          ? "bg-orange-500"
          : "bg-slate-200";

  return (
    <div className="flex items-center gap-2">
      <div className="flex-1 h-2 rounded-full bg-slate-100 overflow-hidden">
        <div
          className={`h-full rounded-full transition-all ${colorClass}`}
          style={{ width: `${Math.max(score, 2)}%` }}
        />
      </div>
      <span className="text-xs font-semibold w-9 text-right shrink-0 tabular-nums text-slate-600">
        {score}%
      </span>
    </div>
  );
}

function PriorityBadge({ priority }: { priority: string }) {
  const styles =
    priority === "high"
      ? "bg-red-50 text-red-700 border-red-200"
      : priority === "medium"
        ? "bg-yellow-50 text-yellow-700 border-yellow-200"
        : priority === "info"
          ? "bg-blue-50 text-blue-700 border-blue-200"
          : "bg-slate-50 text-slate-600 border-slate-200";
  const label =
    priority === "high"
      ? "높음"
      : priority === "medium"
        ? "중간"
        : priority === "info"
          ? "참고"
          : "낮음";

  return (
    <span
      className={`inline-flex items-center rounded-md border px-1.5 py-0.5 text-xs font-medium ${styles}`}
    >
      {label}
    </span>
  );
}

export function ProcedureCompleteness({ data }: ProcedureCompletenessProps) {
  const procedures = Object.entries(data.procedures);

  if (procedures.length === 0) {
    return null;
  }

  // Sort by completeness ascending (worst first)
  const sorted = [...procedures].sort(
    (a, b) => a[1].completeness - b[1].completeness,
  );

  return (
    <section className="mt-10">
      <div className="flex items-center gap-2 mb-4">
        <ClipboardCheck className="h-5 w-5 text-slate-600" aria-hidden="true" />
        <h2 className="text-lg font-bold text-slate-900">
          시술별 콘텐츠 완성도
        </h2>
      </div>
      <div className="rounded-xl border border-slate-200 bg-white p-5 sm:p-6">
        {/* Overall score */}
        <div className="flex items-center gap-3 mb-6">
          <div className="flex h-14 w-14 items-center justify-center rounded-xl bg-slate-100">
            <span className="text-xl font-bold tabular-nums text-slate-900">
              {data.overall_completeness}
            </span>
          </div>
          <div>
            <p className="text-sm font-semibold text-slate-900">
              전체 콘텐츠 완성도
            </p>
            <p className="text-xs text-slate-500">
              {procedures.length}개 시술 &middot; 6가지 콘텐츠 유형 기준
            </p>
          </div>
        </div>

        {/* Completeness bars per procedure */}
        <div className="space-y-2.5 mb-6">
          {sorted.map(([key, proc]) => (
            <div key={key} className="flex items-center gap-3">
              <span className="text-sm font-medium w-16 shrink-0 text-slate-700 truncate">
                {proc.name}
              </span>
              <div className="flex-1">
                <CompletenessBar score={proc.completeness} />
              </div>
            </div>
          ))}
        </div>

        {/* Matrix table */}
        <div className="overflow-x-auto mb-6">
          <table className="w-full text-sm">
            <thead>
              <tr className="border-b border-slate-200">
                <th className="py-2 pr-3 text-left font-medium text-slate-500">
                  시술
                </th>
                {SECTION_KEYS.map((key) => (
                  <th
                    key={key}
                    className="py-2 px-2 text-center font-medium text-slate-500"
                  >
                    <span className="text-xs">{SECTION_LABELS[key]}</span>
                  </th>
                ))}
              </tr>
            </thead>
            <tbody>
              {sorted.map(([key, proc]) => (
                <tr
                  key={key}
                  className="border-b border-slate-100 last:border-0"
                >
                  <td className="py-2.5 pr-3 text-slate-700 font-medium">
                    {proc.name}
                  </td>
                  {SECTION_KEYS.map((sKey) => (
                    <td key={sKey} className="py-2.5 px-2 text-center">
                      <SectionIcon
                        present={proc.sections[sKey] ?? false}
                        partial={proc.partial_sections.includes(sKey)}
                      />
                    </td>
                  ))}
                </tr>
              ))}
            </tbody>
          </table>
        </div>

        {/* Legend */}
        <div className="flex items-center gap-4 mb-6 text-xs text-slate-500">
          <span className="flex items-center gap-1">
            <span className="inline-block h-3 w-3 rounded-full bg-green-100 border border-green-300" />
            있음
          </span>
          <span className="flex items-center gap-1">
            <span className="inline-block h-3 w-3 rounded-full bg-yellow-100 border border-yellow-300" />
            부족
          </span>
          <span className="flex items-center gap-1">
            <span className="inline-block h-3 w-3 rounded-full bg-red-100 border border-red-300" />
            없음
          </span>
        </div>

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
