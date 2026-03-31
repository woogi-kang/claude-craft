"use client";

import { Cpu } from "lucide-react";

interface DetectedTech {
  label: string;
  category: string;
  found_on: string[];
}

interface MissingRecommended {
  tech: string;
  reason: string;
}

interface Recommendation {
  priority: string;
  message: string;
}

interface TechStackData {
  detected: Record<string, DetectedTech>;
  by_category: Record<string, string[]>;
  missing_recommended: MissingRecommended[];
  total_detected: number;
  recommendations: Recommendation[];
}

interface TechStackProps {
  data: TechStackData;
}

const CATEGORY_META: Record<string, { label: string; icon: string }> = {
  analytics: { label: "웹 분석", icon: "📊" },
  ads: { label: "광고 추적", icon: "📣" },
  chat: { label: "채팅/CRM", icon: "💬" },
  cms: { label: "CMS/빌더", icon: "🏗️" },
  cdn: { label: "CDN", icon: "🌐" },
  booking: { label: "예약 시스템", icon: "📅" },
  seo: { label: "SEO", icon: "🔍" },
};

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

function CategoryCard({
  category,
  techs,
}: {
  category: string;
  techs: string[];
}) {
  const meta = CATEGORY_META[category] ?? { label: category, icon: "⚙️" };
  const detected = techs.length > 0;

  return (
    <div
      className={`rounded-lg border p-3 ${
        detected
          ? "border-green-200 bg-green-50"
          : "border-slate-200 bg-slate-50"
      }`}
    >
      <div className="flex items-center gap-2 mb-1.5">
        <span className="text-base" aria-hidden="true">
          {meta.icon}
        </span>
        <span className="text-sm font-medium text-slate-900">{meta.label}</span>
        {detected ? (
          <span className="ml-auto inline-flex h-5 w-5 items-center justify-center rounded-full bg-green-500 text-white text-xs">
            ✓
          </span>
        ) : (
          <span className="ml-auto inline-flex h-5 w-5 items-center justify-center rounded-full bg-slate-300 text-white text-xs">
            −
          </span>
        )}
      </div>
      {detected ? (
        <div className="flex flex-wrap gap-1">
          {techs.map((tech) => (
            <span
              key={tech}
              className="inline-flex items-center rounded-md bg-green-100 px-2 py-0.5 text-xs font-medium text-green-800"
            >
              {tech}
            </span>
          ))}
        </div>
      ) : (
        <p className="text-xs text-slate-400">미감지</p>
      )}
    </div>
  );
}

export function TechStack({ data }: TechStackProps) {
  const categories = Object.keys(CATEGORY_META);

  return (
    <section className="mt-10">
      <div className="flex items-center gap-2 mb-4">
        <Cpu className="h-5 w-5 text-slate-600" aria-hidden="true" />
        <h2 className="text-lg font-bold text-slate-900">기술 스택 분석</h2>
        <span className="ml-auto rounded-full bg-slate-100 px-2.5 py-0.5 text-xs font-medium tabular-nums text-slate-600">
          {data.total_detected}개 감지
        </span>
      </div>
      <div className="rounded-xl border border-slate-200 bg-white p-5 sm:p-6">
        {/* Category grid */}
        <div className="grid gap-3 sm:grid-cols-2 lg:grid-cols-3 mb-6">
          {categories.map((cat) => (
            <CategoryCard
              key={cat}
              category={cat}
              techs={data.by_category[cat] ?? []}
            />
          ))}
        </div>

        {/* Missing recommended */}
        {data.missing_recommended.length > 0 && (
          <div className="mb-6">
            <h3 className="text-sm font-semibold text-slate-900 mb-3">
              추천 기술
            </h3>
            <div className="grid gap-2 sm:grid-cols-2">
              {data.missing_recommended.map((item) => (
                <div
                  key={item.tech}
                  className="flex items-start gap-2 rounded-lg border border-amber-100 bg-amber-50 p-3"
                >
                  <span className="mt-0.5 text-amber-500 text-sm">💡</span>
                  <div>
                    <p className="text-sm font-medium text-amber-900">
                      {item.tech}
                    </p>
                    <p className="text-xs text-amber-700">{item.reason}</p>
                  </div>
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
