"use client";

import { Languages } from "lucide-react";

interface LanguageInfo {
  code: string;
  label: string;
  flag: string;
  page_count: number;
}

interface Recommendation {
  priority: string;
  category: string;
  lang?: string;
  message: string;
}

interface MultilingualReadinessData {
  languages: Record<string, LanguageInfo>;
  page_types: Record<string, { name: string; languages: string[] }>;
  matrix: Record<string, Record<string, boolean>>;
  readiness_scores: Record<string, number>;
  overall_score: number;
  hreflang_tags: { lang: string; hreflang: string; href: string }[];
  recommendations: Recommendation[];
}

interface MultilingualReadinessProps {
  data: MultilingualReadinessData;
}

const TARGET_LANGS = ["ko", "en", "ja", "zh"];
const LANG_LABELS: Record<string, string> = {
  ko: "KO",
  en: "EN",
  ja: "JA",
  zh: "ZH",
};
const LANG_FLAGS: Record<string, string> = {
  ko: "\u{1F1F0}\u{1F1F7}",
  en: "\u{1F1FA}\u{1F1F8}",
  ja: "\u{1F1EF}\u{1F1F5}",
  zh: "\u{1F1E8}\u{1F1F3}",
};
const PAGE_TYPE_LABELS: Record<string, string> = {
  main: "메인",
  procedure: "시술 소개",
  doctor: "의료진",
  price: "가격/비용",
  booking: "예약/상담",
  review: "후기/리뷰",
  other: "기타",
};

function MatrixIcon({ exists }: { exists: boolean }) {
  if (exists) {
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

function ScoreBar({ score, lang }: { score: number; lang: string }) {
  const colorClass =
    score >= 80
      ? "bg-green-500"
      : score >= 40
        ? "bg-yellow-500"
        : score > 0
          ? "bg-orange-500"
          : "bg-slate-200";

  return (
    <div className="flex items-center gap-3">
      <span className="text-lg w-7 text-center shrink-0">
        {LANG_FLAGS[lang]}
      </span>
      <span className="text-sm font-medium w-10 shrink-0 text-slate-700">
        {LANG_LABELS[lang]}
      </span>
      <div className="flex-1 h-2.5 rounded-full bg-slate-100 overflow-hidden">
        <div
          className={`h-full rounded-full transition-all ${colorClass}`}
          style={{ width: `${Math.max(score, 2)}%` }}
        />
      </div>
      <span className="text-sm font-semibold w-12 text-right shrink-0 tabular-nums text-slate-700">
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

export function MultilingualReadiness({ data }: MultilingualReadinessProps) {
  const pageTypes = Object.keys(data.matrix);

  return (
    <section className="mt-10">
      <div className="flex items-center gap-2 mb-4">
        <Languages className="h-5 w-5 text-slate-600" aria-hidden="true" />
        <h2 className="text-lg font-bold text-slate-900">다국어 준비도</h2>
      </div>
      <div className="rounded-xl border border-slate-200 bg-white p-5 sm:p-6">
        {/* Overall score */}
        <div className="flex items-center gap-3 mb-6">
          <div className="flex h-14 w-14 items-center justify-center rounded-xl bg-slate-100">
            <span className="text-xl font-bold tabular-nums text-slate-900">
              {data.overall_score}
            </span>
          </div>
          <div>
            <p className="text-sm font-semibold text-slate-900">
              해외 환자 언어 대응 점수
            </p>
            <p className="text-xs text-slate-500">
              영어·일본어·중국어 페이지 커버리지 평균
            </p>
          </div>
        </div>

        {/* Language readiness bars */}
        <div className="space-y-2.5 mb-6">
          {TARGET_LANGS.map((lang) => (
            <ScoreBar
              key={lang}
              lang={lang}
              score={data.readiness_scores[lang] ?? 0}
            />
          ))}
        </div>

        {/* Matrix table */}
        {pageTypes.length > 0 && (
          <div className="overflow-x-auto mb-6">
            <table className="w-full text-sm">
              <thead>
                <tr className="border-b border-slate-200">
                  <th className="py-2 pr-3 text-left font-medium text-slate-500">
                    페이지 유형
                  </th>
                  {TARGET_LANGS.map((lang) => (
                    <th
                      key={lang}
                      className="py-2 px-2 text-center font-medium text-slate-500"
                    >
                      <span className="text-base">{LANG_FLAGS[lang]}</span>
                      <br />
                      <span className="text-xs">{LANG_LABELS[lang]}</span>
                    </th>
                  ))}
                </tr>
              </thead>
              <tbody>
                {pageTypes.map((pt) => (
                  <tr
                    key={pt}
                    className="border-b border-slate-100 last:border-0"
                  >
                    <td className="py-2.5 pr-3 text-slate-700">
                      {PAGE_TYPE_LABELS[pt] ?? pt}
                    </td>
                    {TARGET_LANGS.map((lang) => (
                      <td key={lang} className="py-2.5 px-2 text-center">
                        <MatrixIcon exists={data.matrix[pt]?.[lang] ?? false} />
                      </td>
                    ))}
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}

        {/* Hreflang info */}
        {data.hreflang_tags.length > 0 && (
          <div className="mb-6 rounded-lg bg-green-50 border border-green-200 p-3.5 text-sm text-green-800">
            <span className="font-semibold">hreflang 태그 감지:</span>{" "}
            {data.hreflang_tags.map((t) => t.hreflang).join(", ")}
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
