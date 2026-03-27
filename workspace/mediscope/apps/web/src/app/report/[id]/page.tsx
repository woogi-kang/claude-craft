"use client";

import { useState } from "react";
import { useParams } from "next/navigation";
import { useQuery } from "@tanstack/react-query";
import { PieChart, Pie, Tooltip, ResponsiveContainer, Cell } from "recharts";
import type { Audit } from "@/lib/types";
import { getGrade } from "@/lib/types";
import type { CheckItemData } from "@/lib/report-config";
import {
  getTopIssues,
  REPORT_CATEGORIES,
  computeCategoryScore,
} from "@/lib/report-config";
import { ReportHeader } from "@/components/report/report-header";
import { ScoreHero } from "@/components/report/score-hero";
import { RadarChart } from "@/components/report/radar-chart";
import { CategorySummary } from "@/components/report/category-summary";
import { TopIssues } from "@/components/report/top-issues";
import { GateOverlay } from "@/components/report/gate-overlay";
import { CategoryAccordion } from "@/components/report/category-accordion";
import { BenchmarkSection } from "@/components/report/benchmark-section";
import { IntlSearchSection } from "@/components/report/intl-search-section";
import { ImprovementRoadmap } from "@/components/report/improvement-roadmap";
import { LeadForm } from "@/components/report/lead-form";
import { SubscriptionForm } from "@/components/report/subscription-form";

const PIE_COLORS = ["#334155", "#e2e8f0"];

interface CompetitionData {
  audit_id: string;
  region: { sido: string; sggu: string } | null;
  total_clinics: number;
  region_clinics: number;
  foreign_patient_facilitators: number;
  foreign_patient_rate: number;
  website_count: number;
  website_rate: number;
}

export default function ReportPage() {
  const { id } = useParams<{ id: string }>();
  const [isUnlocked, setIsUnlocked] = useState(false);

  const { data: audit, isLoading } = useQuery<Audit>({
    queryKey: ["audit", id],
    queryFn: async () => {
      const res = await fetch(`/api/audits/${id}`);
      if (!res.ok) throw new Error("Failed to fetch");
      return res.json();
    },
  });

  const { data: competition } = useQuery<CompetitionData>({
    queryKey: ["competition", id],
    queryFn: async () => {
      const res = await fetch(`/api/competition/${id}`);
      if (!res.ok) return null;
      return res.json();
    },
    enabled: !!audit,
  });

  if (isLoading) {
    return (
      <div className="flex min-h-screen items-center justify-center bg-slate-50">
        <div className="text-center">
          <div className="mx-auto h-10 w-10 animate-spin rounded-full border-4 border-slate-200 border-t-slate-600" />
          <p className="mt-4 text-sm text-slate-500">리포트를 불러오는 중...</p>
        </div>
      </div>
    );
  }

  if (!audit) {
    return (
      <div className="flex min-h-screen items-center justify-center bg-slate-50">
        <div className="text-center">
          <p className="text-lg font-semibold text-slate-900">
            리포트를 찾을 수 없습니다
          </p>
          <p className="mt-1 text-sm text-slate-500">
            URL을 확인하고 다시 시도해주세요.
          </p>
        </div>
      </div>
    );
  }

  const totalScore = audit.total_score ?? 0;
  const grade = audit.grade ?? getGrade(totalScore);

  // Extract check item data from scores (Worker saves enriched data here)
  const rawScores = (audit as unknown as Record<string, unknown>).scores as
    | Record<string, CheckItemData>
    | undefined;
  const detailScores = (audit.details as Record<string, unknown>)
    ?.category_scores as Record<string, CheckItemData> | undefined;

  const categoryScores: Record<string, CheckItemData> = (() => {
    if (rawScores && typeof rawScores === "object") {
      const firstVal = Object.values(rawScores)[0];
      if (
        firstVal &&
        typeof firstVal === "object" &&
        "display_name" in firstVal
      ) {
        return rawScores;
      }
    }
    if (detailScores && typeof detailScores === "object") {
      return detailScores;
    }
    return {};
  })();

  // Compute pass/warn/fail counts
  let passCount = 0;
  let warnCount = 0;
  let failCount = 0;
  for (const item of Object.values(categoryScores)) {
    if (
      item.fail_type === "system_limit" ||
      item.fail_type === "api_error" ||
      item.fail_type === "not_applicable"
    )
      continue;
    if (item.score >= 80) passCount++;
    else if (item.score >= 40) warnCount++;
    else failCount++;
  }

  const totalMeasured = passCount + warnCount + failCount;
  const topIssues = getTopIssues(categoryScores);

  // Radar chart data
  const radarCategories = REPORT_CATEGORIES.map((cat) => {
    const { score } = computeCategoryScore(cat.items, categoryScores);
    return { label: cat.label, score };
  });

  // Find worst category to open by default
  let worstCategoryIdx = 0;
  let worstScore = 101;
  REPORT_CATEGORIES.forEach((cat, idx) => {
    const { score } = computeCategoryScore(cat.items, categoryScores);
    if (score < worstScore) {
      worstScore = score;
      worstCategoryIdx = idx;
    }
  });

  return (
    <div className="min-h-screen bg-slate-50 print:bg-white">
      <div className="mx-auto max-w-3xl px-4 py-8 sm:py-12 print:px-0">
        <ReportHeader
          url={audit.url}
          createdAt={audit.created_at}
          reportUrl={audit.report_url}
          auditId={id}
        />

        {/* === Gate 전: 항상 표시 === */}
        <ScoreHero
          totalScore={totalScore}
          grade={grade}
          passCount={passCount}
          warnCount={warnCount}
          failCount={failCount}
        />

        <RadarChart categories={radarCategories} />

        <CategorySummary categoryScores={categoryScores} />

        <TopIssues issues={topIssues} blurred={!isUnlocked} />

        {/* === Gate 전: 벤치마크 티저 === */}
        {!isUnlocked && (
          <BenchmarkSection auditId={id} enabled={!!audit} teaser />
        )}

        {/* === Gate: 이메일 입력 폼 === */}
        {!isUnlocked && (
          <GateOverlay
            auditId={id}
            totalItems={totalMeasured}
            failCount={failCount}
            onUnlock={() => setIsUnlocked(true)}
          />
        )}

        {/* === Gate 후: 이메일 입력 완료 시 표시 === */}
        {isUnlocked && (
          <>
            <CategoryAccordion
              categoryScores={categoryScores}
              defaultOpenIndex={worstCategoryIdx}
            />

            {/* Competition Analysis */}
            {competition && competition.region_clinics > 0 && (
              <section className="mt-10">
                <div className="flex items-center gap-2 mb-4">
                  <h2 className="text-lg font-bold text-slate-900">
                    경쟁 분석
                  </h2>
                </div>
                <div className="rounded-xl border border-slate-200 bg-white p-5 sm:p-6">
                  <p className="text-sm text-slate-500 mb-4">
                    {competition.region
                      ? `${competition.region.sido} ${competition.region.sggu ?? ""}`
                      : "전체"}{" "}
                    지역 피부과 현황
                  </p>
                  <div className="grid gap-4 sm:grid-cols-3">
                    <div className="rounded-lg border border-slate-200 bg-slate-50 p-4 text-center">
                      <div className="text-3xl font-bold tabular-nums text-slate-900">
                        {competition.region_clinics}
                      </div>
                      <div className="mt-1 text-sm text-slate-500">
                        같은 지역 피부과
                      </div>
                    </div>
                    <div className="rounded-lg border border-orange-200 bg-orange-50 p-4 text-center">
                      <div className="text-3xl font-bold tabular-nums text-orange-700">
                        {competition.foreign_patient_rate}%
                      </div>
                      <div className="mt-1 text-sm text-orange-600">
                        외국인유치기관 비율
                      </div>
                    </div>
                    <div className="rounded-lg border border-blue-200 bg-blue-50 p-4 text-center">
                      <div className="text-3xl font-bold tabular-nums text-blue-700">
                        {competition.website_rate}%
                      </div>
                      <div className="mt-1 text-sm text-blue-600">
                        웹사이트 보유율
                      </div>
                    </div>
                  </div>
                  <div className="mt-6 grid gap-4 sm:grid-cols-2">
                    <div>
                      <p className="mb-2 text-sm font-medium text-slate-700">
                        웹사이트 보유
                      </p>
                      <ResponsiveContainer width="100%" height={160}>
                        <PieChart>
                          <Pie
                            data={[
                              {
                                name: "보유",
                                value: competition.website_count,
                              },
                              {
                                name: "미보유",
                                value:
                                  competition.region_clinics -
                                  competition.website_count,
                              },
                            ]}
                            cx="50%"
                            cy="50%"
                            innerRadius={40}
                            outerRadius={60}
                            dataKey="value"
                            label={({ name, percent }) =>
                              `${name} ${(percent * 100).toFixed(0)}%`
                            }
                          >
                            <Cell fill={PIE_COLORS[0]} />
                            <Cell fill={PIE_COLORS[1]} />
                          </Pie>
                          <Tooltip />
                        </PieChart>
                      </ResponsiveContainer>
                    </div>
                    <div>
                      <p className="mb-2 text-sm font-medium text-slate-700">
                        외국인유치기관
                      </p>
                      <ResponsiveContainer width="100%" height={160}>
                        <PieChart>
                          <Pie
                            data={[
                              {
                                name: "유치기관",
                                value: competition.foreign_patient_facilitators,
                              },
                              {
                                name: "일반",
                                value:
                                  competition.region_clinics -
                                  competition.foreign_patient_facilitators,
                              },
                            ]}
                            cx="50%"
                            cy="50%"
                            innerRadius={40}
                            outerRadius={60}
                            dataKey="value"
                            label={({ name, percent }) =>
                              `${name} ${(percent * 100).toFixed(0)}%`
                            }
                          >
                            <Cell fill="#c2410c" />
                            <Cell fill={PIE_COLORS[1]} />
                          </Pie>
                          <Tooltip />
                        </PieChart>
                      </ResponsiveContainer>
                    </div>
                  </div>
                </div>
              </section>
            )}

            <BenchmarkSection auditId={id} enabled={!!audit} teaser={false} />

            {!!audit.details?.international_search && (
              <IntlSearchSection
                data={
                  audit.details.international_search as {
                    engines_checked: number;
                    engines_available: number;
                    results: Record<
                      string,
                      {
                        rank: number | null;
                        score: number;
                        query: string;
                        error?: string;
                      }
                    >;
                    summary: string;
                  }
                }
              />
            )}

            <ImprovementRoadmap categoryScores={categoryScores} />

            <LeadForm auditId={id} />
            <SubscriptionForm auditId={id} />
          </>
        )}

        {/* Footer */}
        <footer className="mt-12 pt-6 border-t border-slate-200 text-center print:mt-8">
          <p className="text-xs text-slate-400">
            CheckYourHospital by MediScope &middot; 본 리포트는 자동화된 진단
            결과이며, 실제 검색 순위와 차이가 있을 수 있습니다.
          </p>
        </footer>
      </div>
    </div>
  );
}
