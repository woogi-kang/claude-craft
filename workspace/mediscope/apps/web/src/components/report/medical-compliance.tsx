"use client";

import { Shield } from "lucide-react";

interface Violation {
  severity: string;
  rule: string;
  text: string;
  url: string;
  law: string;
  description: string;
}

interface Warning {
  severity: string;
  rule: string;
  text: string;
  url: string;
  law: string;
  description: string;
}

interface CompliantItem {
  rule: string;
  message: string;
  url?: string;
}

interface CountryScore {
  score: number;
  violations: number;
  warnings: number;
}

interface Recommendation {
  priority: string;
  message: string;
}

interface MedicalComplianceData {
  overall_score: number;
  violations: Violation[];
  warnings: Warning[];
  compliant_items: CompliantItem[];
  by_country: {
    kr: CountryScore;
    jp: CountryScore;
    global: CountryScore;
  };
  recommendations: Recommendation[];
}

interface MedicalComplianceProps {
  data: MedicalComplianceData;
}

const COUNTRY_LABELS: Record<string, { label: string; flag: string }> = {
  kr: { label: "한국 의료법", flag: "🇰🇷" },
  jp: { label: "일본 医療法", flag: "🇯🇵" },
  global: { label: "글로벌 규정", flag: "🌐" },
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

function CountryScoreCard({
  code,
  data,
}: {
  code: string;
  data: CountryScore;
}) {
  const info = COUNTRY_LABELS[code] ?? { label: code, flag: "" };
  const borderColor =
    data.score >= 70
      ? "border-green-200"
      : data.score >= 40
        ? "border-yellow-200"
        : "border-red-200";
  const bgColor =
    data.score >= 70
      ? "bg-green-50"
      : data.score >= 40
        ? "bg-yellow-50"
        : "bg-red-50";
  const scoreColor =
    data.score >= 70
      ? "text-green-700"
      : data.score >= 40
        ? "text-yellow-700"
        : "text-red-700";

  return (
    <div
      className={`rounded-lg border ${borderColor} ${bgColor} p-4 text-center`}
    >
      <div className="text-sm text-slate-500 mb-1">
        {info.flag} {info.label}
      </div>
      <div className={`text-3xl font-bold tabular-nums ${scoreColor}`}>
        {data.score}
      </div>
      <div className="mt-1 flex justify-center gap-3 text-xs">
        {data.violations > 0 && (
          <span className="text-red-600">위반 {data.violations}</span>
        )}
        {data.warnings > 0 && (
          <span className="text-yellow-600">주의 {data.warnings}</span>
        )}
        {data.violations === 0 && data.warnings === 0 && (
          <span className="text-green-600">준수</span>
        )}
      </div>
    </div>
  );
}

function SeverityBadge({ severity }: { severity: string }) {
  const styles =
    severity === "high"
      ? "bg-red-100 text-red-800 border-red-200"
      : severity === "medium"
        ? "bg-yellow-100 text-yellow-800 border-yellow-200"
        : "bg-slate-100 text-slate-600 border-slate-200";
  const label =
    severity === "high" ? "높음" : severity === "medium" ? "중간" : "낮음";

  return (
    <span
      className={`inline-flex items-center rounded-md border px-1.5 py-0.5 text-xs font-medium ${styles}`}
    >
      {label}
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

function truncateUrl(url: string, maxLen: number = 60): string {
  if (url.length <= maxLen) return url;
  return url.slice(0, maxLen - 3) + "...";
}

export function MedicalCompliance({ data }: MedicalComplianceProps) {
  const countries = Object.entries(data.by_country) as [string, CountryScore][];

  return (
    <section className="mt-10">
      <div className="flex items-center gap-2 mb-4">
        <Shield className="h-5 w-5 text-slate-600" aria-hidden="true" />
        <h2 className="text-lg font-bold text-slate-900">의료광고 규정 준수</h2>
      </div>
      <div className="rounded-xl border border-slate-200 bg-white p-5 sm:p-6">
        {/* Overall score */}
        <div className="flex items-center gap-3 mb-6">
          <ScoreCircle score={data.overall_score} />
          <div>
            <p className="text-sm font-semibold text-slate-900">
              규정 준수 점수
            </p>
            <p className="text-xs text-slate-500">
              위반 {data.violations.length}건 &middot; 주의{" "}
              {data.warnings.length}건 &middot; 준수{" "}
              {data.compliant_items.length}건
            </p>
          </div>
        </div>

        {/* Country scores */}
        <div className="grid gap-3 sm:grid-cols-3 mb-6">
          {countries.map(([code, countryData]) => (
            <CountryScoreCard key={code} code={code} data={countryData} />
          ))}
        </div>

        {/* Violations */}
        {data.violations.length > 0 && (
          <div className="mb-6">
            <h3 className="text-sm font-semibold text-red-700 mb-3">
              위반 항목
            </h3>
            <div className="space-y-2">
              {data.violations.map((v, idx) => (
                <div
                  key={idx}
                  className="rounded-lg border border-red-100 bg-red-50/50 p-3"
                >
                  <div className="flex items-start gap-2.5">
                    <SeverityBadge severity={v.severity} />
                    <div className="flex-1 min-w-0">
                      <p className="text-sm font-medium text-slate-900">
                        {v.description}
                      </p>
                      <p className="text-xs text-slate-600 mt-0.5 break-all">
                        &ldquo;{v.text}&rdquo;
                      </p>
                      <div className="flex flex-wrap gap-x-3 mt-1.5">
                        <span className="text-xs text-slate-400">{v.law}</span>
                        <a
                          href={v.url}
                          target="_blank"
                          rel="noopener noreferrer"
                          className="text-xs text-blue-500 hover:underline truncate max-w-[200px]"
                        >
                          {truncateUrl(v.url)}
                        </a>
                      </div>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* Warnings */}
        {data.warnings.length > 0 && (
          <div className="mb-6">
            <h3 className="text-sm font-semibold text-yellow-700 mb-3">
              주의 항목
            </h3>
            <div className="space-y-2">
              {data.warnings.map((w, idx) => (
                <div
                  key={idx}
                  className="rounded-lg border border-yellow-100 bg-yellow-50/50 p-3"
                >
                  <div className="flex items-start gap-2.5">
                    <SeverityBadge severity={w.severity} />
                    <div className="flex-1 min-w-0">
                      <p className="text-sm font-medium text-slate-900">
                        {w.description}
                      </p>
                      <p className="text-xs text-slate-600 mt-0.5 break-all">
                        &ldquo;{w.text}&rdquo;
                      </p>
                      <div className="flex flex-wrap gap-x-3 mt-1.5">
                        <span className="text-xs text-slate-400">{w.law}</span>
                        <a
                          href={w.url}
                          target="_blank"
                          rel="noopener noreferrer"
                          className="text-xs text-blue-500 hover:underline truncate max-w-[200px]"
                        >
                          {truncateUrl(w.url)}
                        </a>
                      </div>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* Compliant items */}
        {data.compliant_items.length > 0 && (
          <div className="mb-6">
            <h3 className="text-sm font-semibold text-green-700 mb-3">
              준수 항목
            </h3>
            <div className="space-y-1.5">
              {data.compliant_items.map((item, idx) => (
                <div
                  key={idx}
                  className="flex items-center gap-2 rounded-lg border border-green-100 bg-green-50/50 px-3 py-2"
                >
                  <span className="text-green-600 text-sm">&#10003;</span>
                  <span className="text-sm text-slate-700">{item.message}</span>
                </div>
              ))}
            </div>
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
