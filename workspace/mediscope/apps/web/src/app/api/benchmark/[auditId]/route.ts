import { NextRequest, NextResponse } from "next/server";
import { createAdminClient } from "@/lib/supabase/admin";

export async function GET(
  _request: NextRequest,
  { params }: { params: Promise<{ auditId: string }> },
) {
  const { auditId } = await params;
  const supabase = createAdminClient();

  // Fetch audit to get score and location
  const { data: audit, error: auditError } = await supabase
    .from("audits")
    .select("id, url, total_score, details")
    .eq("id", auditId)
    .single();

  if (auditError || !audit) {
    return NextResponse.json(
      { error: "진단을 찾을 수 없습니다" },
      { status: 404 },
    );
  }

  const details = (audit.details ?? {}) as Record<string, unknown>;
  const sido = details.sido as string | undefined;
  const sggu = details.sggu as string | undefined;

  // Query beauty_clinics with latest_score for the same region
  let query = supabase
    .from("beauty_clinics")
    .select("latest_score")
    .not("latest_score", "is", null);

  if (sido) query = query.eq("sido", sido);
  if (sggu) query = query.eq("sggu", sggu);

  const { data: clinics } = await query;
  const scores = (clinics ?? [])
    .map((c) => c.latest_score as number)
    .filter((s) => s != null)
    .sort((a, b) => a - b);

  if (scores.length === 0) {
    return NextResponse.json({
      audit_id: auditId,
      region: sido ? { sido, sggu } : null,
      top_25_avg: 0,
      median: 0,
      bottom_25_avg: 0,
      total_count: 0,
      your_score: audit.total_score,
      your_percentile: null,
    });
  }

  const n = scores.length;
  const topStart = Math.max(0, n - Math.floor(n / 4));
  const topScores = scores.slice(topStart);
  const bottomEnd = Math.floor(n / 4) || 1;
  const bottomScores = scores.slice(0, bottomEnd);

  const avg = (arr: number[]) =>
    arr.length > 0 ? arr.reduce((a, b) => a + b, 0) / arr.length : 0;
  const median =
    n % 2 === 0
      ? (scores[n / 2 - 1] + scores[n / 2]) / 2
      : scores[Math.floor(n / 2)];

  // Percentile: % of clinics with lower score
  let yourPercentile: number | null = null;
  if (audit.total_score != null) {
    const lowerCount = scores.filter((s) => s < audit.total_score!).length;
    yourPercentile = Math.round((lowerCount / n) * 100);
  }

  return NextResponse.json({
    audit_id: auditId,
    region: sido ? { sido, sggu } : null,
    top_25_avg: Math.round(avg(topScores) * 10) / 10,
    median: Math.round(median * 10) / 10,
    bottom_25_avg: Math.round(avg(bottomScores) * 10) / 10,
    total_count: n,
    your_score: audit.total_score,
    your_percentile: yourPercentile,
  });
}
