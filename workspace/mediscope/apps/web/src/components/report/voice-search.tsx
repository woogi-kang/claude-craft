"use client";

import { Mic } from "lucide-react";

interface CheckItem {
  status: "pass" | "warn" | "fail";
  description: string;
  count?: number;
}

interface Recommendation {
  priority: string;
  message: string;
}

interface VoiceSearchData {
  overall_score: number;
  checks: Record<string, CheckItem>;
  pass_count: number;
  total_checks: number;
  recommendations: Recommendation[];
}

interface VoiceSearchProps {
  data: VoiceSearchData;
}

const CHECK_LABELS: Record<string, string> = {
  faq_schema: "FAQ 구조화 데이터",
  question_headings: "질문형 헤딩",
  featured_snippet: "Featured Snippet 적합성",
  local_business: "LocalBusiness Schema",
  page_speed: "페이지 로딩 속도",
  mobile: "모바일 최적화",
  howto_schema: "HowTo Schema",
  long_tail: "장문 키워드 콘텐츠",
};

const CHECK_ORDER = [
  "faq_schema",
  "question_headings",
  "featured_snippet",
  "local_business",
  "page_speed",
  "mobile",
  "howto_schema",
  "long_tail",
];

function StatusIcon({ status }: { status: string }) {
  if (status === "pass") {
    return (
      <span className="inline-flex h-6 w-6 items-center justify-center rounded-full bg-green-100 text-green-600 shrink-0">
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
  if (status === "warn") {
    return (
      <span className="inline-flex h-6 w-6 items-center justify-center rounded-full bg-yellow-100 text-yellow-600 shrink-0">
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
    <span className="inline-flex h-6 w-6 items-center justify-center rounded-full bg-red-100 text-red-400 shrink-0">
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

export function VoiceSearch({ data }: VoiceSearchProps) {
  const checkEntries = CHECK_ORDER.filter((key) => key in data.checks).map(
    (key) => ({ key, label: CHECK_LABELS[key] ?? key, ...data.checks[key] }),
  );

  return (
    <section className="mt-10">
      <div className="flex items-center gap-2 mb-4">
        <Mic className="h-5 w-5 text-slate-600" aria-hidden="true" />
        <h2 className="text-lg font-bold text-slate-900">음성 검색 최적화</h2>
      </div>
      <div className="rounded-xl border border-slate-200 bg-white p-5 sm:p-6">
        {/* Overall score */}
        <div className="flex items-center gap-3 mb-6">
          <ScoreCircle score={data.overall_score} />
          <div>
            <p className="text-sm font-semibold text-slate-900">
              음성 검색 준비도 점수
            </p>
            <p className="text-xs text-slate-500">
              {data.pass_count}/{data.total_checks} 항목 통과
            </p>
          </div>
        </div>

        {/* Checklist */}
        <div className="space-y-2.5 mb-6">
          {checkEntries.map((check) => (
            <div
              key={check.key}
              className="flex items-center gap-3 rounded-lg border border-slate-100 bg-slate-50 px-3 py-2.5"
            >
              <StatusIcon status={check.status} />
              <div className="flex-1 min-w-0">
                <span className="text-sm font-medium text-slate-700">
                  {check.label}
                </span>
                <p className="text-xs text-slate-500 truncate">
                  {check.description}
                </p>
              </div>
            </div>
          ))}
        </div>

        {/* Insight */}
        <div className="rounded-lg border border-indigo-100 bg-indigo-50 p-3 mb-6">
          <p className="text-xs text-indigo-700">
            <span className="font-semibold">Insight:</span> 음성 검색의 70%는
            자연어 질문 형태입니다. FAQ와 질문형 헤딩을 추가하면 음성 검색 노출
            가능성이 크게 향상됩니다.
          </p>
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
