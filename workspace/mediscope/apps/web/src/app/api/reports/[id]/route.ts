import { NextRequest, NextResponse } from "next/server";
import { createAdminClient } from "@/lib/supabase/admin";

function generateReportHtml(audit: {
  url: string;
  total_score: number;
  grade: string;
  scores: Record<string, unknown>;
}) {
  const CATEGORY_LABELS: Record<string, string> = {
    robots_txt: "Robots.txt",
    sitemap: "Sitemap",
    meta_tags: "Meta Tags",
    headings: "Heading 구조",
    images_alt: "이미지 ALT",
    links: "내부 링크",
    https: "HTTPS",
    canonical: "Canonical",
    url_structure: "URL 구조",
    errors_404: "404/리다이렉트",
    lcp: "LCP",
    inp: "INP",
    cls: "CLS",
    performance_score: "성능 점수",
    mobile: "모바일 반응형",
  };

  const gradeColor =
    audit.grade === "A"
      ? "#166534"
      : audit.grade === "B"
        ? "#1e40af"
        : audit.grade === "C"
          ? "#854d0e"
          : "#991b1b";

  const gradeBg =
    audit.grade === "A"
      ? "#dcfce7"
      : audit.grade === "B"
        ? "#dbeafe"
        : audit.grade === "C"
          ? "#fef9c3"
          : "#fee2e2";

  const items = Object.entries(audit.scores).map(([key, val]) => {
    const v = val as { score?: number; grade?: string; issues?: string[] };
    const label = CATEGORY_LABELS[key] ?? key;
    const score = v?.score ?? 0;
    const grade = v?.grade ?? "skip";
    const issues = v?.issues ?? [];
    return { key, label, score, grade, issues };
  });

  const passCount = items.filter((i) => i.grade === "pass").length;
  const warnCount = items.filter((i) => i.grade === "warn").length;
  const failCount = items.filter((i) => i.grade === "fail").length;

  return `<!DOCTYPE html>
<html lang="ko">
<head>
  <meta charset="utf-8"/>
  <title>CheckYourHospital 진단 리포트</title>
  <style>
    * { margin: 0; padding: 0; box-sizing: border-box; }
    body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif; color: #1e293b; padding: 48px; max-width: 800px; margin: 0 auto; }
    .header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 40px; padding-bottom: 20px; border-bottom: 2px solid #e2e8f0; }
    .logo { font-size: 24px; font-weight: bold; color: #2563eb; }
    .date { color: #64748b; font-size: 14px; }
    .summary { text-align: center; margin: 40px 0; }
    .score-circle { display: inline-flex; align-items: center; justify-content: center; width: 120px; height: 120px; border-radius: 50%; border: 6px solid #e2e8f0; }
    .score-num { font-size: 42px; font-weight: bold; }
    .score-sub { color: #64748b; font-size: 14px; }
    .grade-badge { display: inline-block; margin-top: 12px; padding: 4px 20px; border-radius: 20px; font-weight: bold; font-size: 18px; background: ${gradeBg}; color: ${gradeColor}; }
    .stats { display: flex; gap: 24px; justify-content: center; margin: 24px 0; }
    .stat { text-align: center; }
    .stat-num { font-size: 24px; font-weight: bold; }
    .stat-label { font-size: 12px; color: #64748b; }
    .items-table { width: 100%; border-collapse: collapse; margin: 32px 0; }
    .items-table th, .items-table td { padding: 12px 16px; text-align: left; border-bottom: 1px solid #e2e8f0; }
    .items-table th { background: #f8fafc; font-weight: 600; font-size: 13px; color: #64748b; text-transform: uppercase; }
    .badge { display: inline-block; padding: 2px 10px; border-radius: 12px; font-size: 12px; font-weight: 600; }
    .badge-pass { background: #dcfce7; color: #166534; }
    .badge-warn { background: #fef9c3; color: #854d0e; }
    .badge-fail { background: #fee2e2; color: #991b1b; }
    .issue { color: #64748b; font-size: 13px; margin-top: 4px; }
    .footer { margin-top: 48px; padding-top: 20px; border-top: 1px solid #e2e8f0; color: #94a3b8; font-size: 12px; text-align: center; }
    .url { color: #64748b; font-size: 16px; margin-top: 8px; }
    .bar { height: 8px; border-radius: 4px; background: #e2e8f0; margin-top: 4px; }
    .bar-fill { height: 100%; border-radius: 4px; }
    @media print { body { padding: 24px; } }
  </style>
</head>
<body>
  <div class="header">
    <div class="logo">CheckYourHospital</div>
    <div class="date">${new Date().toLocaleDateString("ko-KR", { year: "numeric", month: "long", day: "numeric" })}</div>
  </div>

  <h1 style="font-size: 28px; margin-bottom: 4px;">홈페이지 진단 리포트</h1>
  <p class="url">${audit.url}</p>

  <div class="summary">
    <div class="score-circle">
      <div>
        <div class="score-num">${audit.total_score}</div>
        <div class="score-sub">/100</div>
      </div>
    </div>
    <br/>
    <div class="grade-badge">등급: ${audit.grade}</div>
  </div>

  <div class="stats">
    <div class="stat"><div class="stat-num" style="color:#166534">${passCount}</div><div class="stat-label">통과</div></div>
    <div class="stat"><div class="stat-num" style="color:#854d0e">${warnCount}</div><div class="stat-label">주의</div></div>
    <div class="stat"><div class="stat-num" style="color:#991b1b">${failCount}</div><div class="stat-label">실패</div></div>
  </div>

  <table class="items-table">
    <thead>
      <tr><th>항목</th><th>점수</th><th>상태</th><th>개선 사항</th></tr>
    </thead>
    <tbody>
      ${items
        .map(
          (item) => `
        <tr>
          <td><strong>${item.label}</strong></td>
          <td>
            ${Math.round(item.score)}/100
            <div class="bar"><div class="bar-fill" style="width:${item.score}%; background:${item.grade === "pass" ? "#22c55e" : item.grade === "warn" ? "#eab308" : "#ef4444"}"></div></div>
          </td>
          <td><span class="badge badge-${item.grade}">${item.grade === "pass" ? "통과" : item.grade === "warn" ? "주의" : "실패"}</span></td>
          <td class="issue">${item.issues.length > 0 ? item.issues[0] : "—"}</td>
        </tr>
      `,
        )
        .join("")}
    </tbody>
  </table>

  <div class="footer">
    <p>이 리포트는 CheckYourHospital AI 진단 시스템에 의해 자동 생성되었습니다.</p>
    <p style="margin-top: 4px;">© 2026 CheckYourHospital. All rights reserved.</p>
  </div>
</body>
</html>`;
}

export async function GET(
  _request: NextRequest,
  { params }: { params: Promise<{ id: string }> },
) {
  const { id } = await params;
  const supabase = createAdminClient();

  const { data: audit, error } = await supabase
    .from("audits")
    .select("url, total_score, grade, scores")
    .eq("id", id)
    .single();

  if (error || !audit) {
    return NextResponse.json(
      { error: "리포트를 찾을 수 없습니다" },
      { status: 404 },
    );
  }

  const html = generateReportHtml(audit);

  return new NextResponse(html, {
    headers: {
      "Content-Type": "text/html; charset=utf-8",
    },
  });
}
