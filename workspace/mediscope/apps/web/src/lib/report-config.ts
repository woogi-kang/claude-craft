import type { Grade } from "./types";

/** Individual check item from worker audit.details.category_scores */
export interface CheckItemData {
  score: number;
  grade: string;
  fail_type: "site_issue" | "system_limit" | "api_error" | "not_applicable";
  display_name: string;
  description: string;
  recommendation: string;
  issues: string[];
  weight: number;
}

/** Category definition for the 5-group redesign */
export interface CategoryDef {
  key: string;
  label: string;
  icon: string;
  description: string;
  items: string[];
}

export const REPORT_CATEGORIES: CategoryDef[] = [
  {
    key: "search_basics",
    label: "검색 노출 기본기",
    icon: "Search",
    description:
      "구글, 네이버 같은 검색엔진이 홈페이지를 제대로 읽고 검색 결과에 노출시키기 위한 기본 설정입니다. 이 항목이 낮으면 아무리 좋은 병원이어도 온라인에서 발견되지 않습니다.",
    items: [
      "robots_txt",
      "sitemap",
      "meta_tags",
      "headings",
      "canonical",
      "url_structure",
    ],
  },
  {
    key: "speed_performance",
    label: "사이트 속도/성능",
    icon: "Zap",
    description:
      "환자가 스마트폰으로 홈페이지를 열었을 때 빠르고 편하게 볼 수 있는지 측정합니다. 3초 이상 걸리면 환자의 절반 이상이 다른 병원 사이트로 이동합니다.",
    items: ["lcp", "inp", "cls", "performance_score", "mobile"],
  },
  {
    key: "security_trust",
    label: "보안/신뢰",
    icon: "ShieldCheck",
    description:
      "환자가 홈페이지를 신뢰할 수 있는지 판단하는 요소입니다. 보안 경고, 깨진 페이지, 전문성 정보 부족은 환자 이탈의 주요 원인입니다.",
    items: [
      "https",
      "errors_404",
      "images_alt",
      "links",
      "eeat_signals",
      "structured_data",
    ],
  },
  {
    key: "international",
    label: "해외 환자 유치",
    icon: "Globe",
    description:
      "일본, 중국, 동남아 환자가 자국 검색엔진에서 병원을 찾고, 익숙한 언어와 메신저로 상담할 수 있는지 확인합니다. 의료관광 매출의 핵심 지표입니다.",
    items: [
      "multilingual_pages",
      "hreflang",
      "overseas_channels",
      "international_search",
    ],
  },
  {
    key: "ai_search",
    label: "AI 검색 대비",
    icon: "Bot",
    description:
      "Gemini, ChatGPT, Perplexity 같은 AI 검색에서 병원이 추천되기 위한 콘텐츠 준비도입니다. 2026년 현재 검색의 30%가 AI를 통해 이루어지고 있어 중요성이 급증하고 있습니다.",
    items: ["ai_search_mention", "content_clarity", "faq_content"],
  },
];

export const GRADE_SUMMARIES: Record<Grade, string> = {
  A: "검색엔진에서 잘 노출되고 있는 우수한 상태입니다",
  B: "기본기는 갖추었으나 몇 가지 개선이 필요합니다",
  C: "검색 노출에 여러 문제가 있어 개선이 필요합니다",
  D: "검색엔진에서 잘 보이지 않는 상태입니다",
  F: "홈페이지가 검색엔진에 거의 노출되지 않는 심각한 상태입니다",
};

export const GRADE_BG_COLORS: Record<Grade, string> = {
  A: "bg-green-50 border-green-200",
  B: "bg-blue-50 border-blue-200",
  C: "bg-yellow-50 border-yellow-200",
  D: "bg-orange-50 border-orange-200",
  F: "bg-red-50 border-red-200",
};

export const GRADE_RING_COLORS: Record<Grade, string> = {
  A: "stroke-green-500",
  B: "stroke-blue-500",
  C: "stroke-yellow-500",
  D: "stroke-orange-500",
  F: "stroke-red-500",
};

export const GRADE_TEXT_COLORS: Record<Grade, string> = {
  A: "text-green-700",
  B: "text-blue-700",
  C: "text-yellow-700",
  D: "text-orange-700",
  F: "text-red-700",
};

export const GRADE_BADGE_COLORS: Record<Grade, string> = {
  A: "bg-green-100 text-green-800 border-green-300",
  B: "bg-blue-100 text-blue-800 border-blue-300",
  C: "bg-yellow-100 text-yellow-800 border-yellow-300",
  D: "bg-orange-100 text-orange-800 border-orange-300",
  F: "bg-red-100 text-red-800 border-red-300",
};

/** Roadmap phase definitions */
export const ROADMAP_PHASES = [
  {
    phase: 1,
    label: "즉시 (당일~3일)",
    description: "설정 변경만으로 해결 가능한 항목",
    items: ["https", "mobile", "robots_txt"],
  },
  {
    phase: 2,
    label: "단기 (1~2주)",
    description: "웹 개발자 작업이 필요한 항목",
    items: [
      "meta_tags",
      "sitemap",
      "canonical",
      "headings",
      "images_alt",
      "errors_404",
      "links",
    ],
  },
  {
    phase: 3,
    label: "중기 (1~3개월)",
    description: "콘텐츠 작성/번역/최적화가 필요한 항목",
    items: [
      "structured_data",
      "eeat_signals",
      "faq_content",
      "content_clarity",
      "multilingual_pages",
      "hreflang",
      "overseas_channels",
      "performance_score",
      "lcp",
      "inp",
      "cls",
      "url_structure",
    ],
  },
];

export function getScoreStatus(score: number) {
  if (score >= 80)
    return {
      label: "양호",
      colorClass: "text-green-600",
      bgClass: "bg-green-50",
      barClass: "bg-green-500",
      borderClass: "border-green-200",
    };
  if (score >= 60)
    return {
      label: "개선 필요",
      colorClass: "text-yellow-600",
      bgClass: "bg-yellow-50",
      barClass: "bg-yellow-500",
      borderClass: "border-yellow-200",
    };
  if (score >= 40)
    return {
      label: "주의",
      colorClass: "text-orange-600",
      bgClass: "bg-orange-50",
      barClass: "bg-orange-500",
      borderClass: "border-orange-200",
    };
  return {
    label: "심각",
    colorClass: "text-red-600",
    bgClass: "bg-red-50",
    barClass: "bg-red-500",
    borderClass: "border-red-200",
  };
}

export function getTopIssues(
  categoryScores: Record<string, CheckItemData>,
  n = 3,
) {
  const issues: (CheckItemData & { key: string; impact: number })[] = [];
  for (const [key, data] of Object.entries(categoryScores)) {
    if (
      data.fail_type === "system_limit" ||
      data.fail_type === "api_error" ||
      data.fail_type === "not_applicable"
    )
      continue;
    if (data.score >= 80) continue;
    const impact = data.weight * (100 - data.score);
    issues.push({ key, impact, ...data });
  }
  issues.sort((a, b) => b.impact - a.impact);
  return issues.slice(0, n);
}

export function computeCategoryScore(
  items: string[],
  scores: Record<string, CheckItemData>,
): { score: number; measured: number; total: number } {
  let totalWeight = 0;
  let weightedScore = 0;
  let measured = 0;
  const total = items.length;

  for (const key of items) {
    const item = scores[key];
    if (!item) continue;
    if (
      item.fail_type === "system_limit" ||
      item.fail_type === "api_error" ||
      item.fail_type === "not_applicable"
    )
      continue;
    measured++;
    totalWeight += item.weight;
    weightedScore += item.weight * item.score;
  }

  const score = totalWeight > 0 ? Math.round(weightedScore / totalWeight) : 0;
  return { score, measured, total };
}
