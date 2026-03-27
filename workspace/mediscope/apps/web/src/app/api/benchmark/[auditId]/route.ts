import { NextRequest, NextResponse } from "next/server";
import { createAdminClient } from "@/lib/supabase/admin";

/** Medical tourism region mapping (mirrors worker regions.py) */
const MEDICAL_REGIONS: Record<string, Set<string>> = {
  "강남/서초": new Set(["강남구", "서초구"]),
  "홍대/마포": new Set(["마포구"]),
  "명동/을지": new Set(["중구"]),
  "신촌/연남": new Set(["서대문구"]),
  "잠실/송파": new Set(["송파구", "강동구"]),
  "건대/성수": new Set(["광진구", "성동구"]),
  "압구정/청담": new Set(["강남구"]),
  "영등포/여의도": new Set(["영등포구"]),
  "부산 서면": new Set(["부산진구", "연제구"]),
  "부산 해운대": new Set(["해운대구", "수영구"]),
  "대구 수성": new Set(["수성구"]),
  제주: new Set(["제주시", "서귀포시"]),
};

function getRegionName(sido: string, sggu: string): string {
  for (const [name, sggus] of Object.entries(MEDICAL_REGIONS)) {
    if (sggus.has(sggu)) return name;
  }
  return `${sido} ${sggu}`;
}

function getRegionSggus(regionName: string): string[] {
  const sggus = MEDICAL_REGIONS[regionName];
  return sggus ? Array.from(sggus) : [];
}

function buildDistribution(
  scores: number[],
): { range: string; count: number }[] {
  const bins = Array.from({ length: 10 }, (_, i) => ({
    range: `${i * 10}-${i * 10 + 9}`,
    count: 0,
  }));
  for (const s of scores) {
    const idx = Math.min(Math.floor(s / 10), 9);
    bins[idx].count += 1;
  }
  return bins;
}

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

  // Resolve medical tourism region
  const regionName =
    sido && sggu ? getRegionName(sido, sggu) : sido ? `${sido}` : "";
  const regionSggus = regionName ? getRegionSggus(regionName) : [];

  // Query beauty_clinics with latest_score for the same region
  let query = supabase
    .from("beauty_clinics")
    .select("latest_score")
    .not("latest_score", "is", null);

  if (regionSggus.length > 0) {
    query = query.in("sggu", regionSggus);
    if (sido) query = query.eq("sido", sido);
  } else {
    if (sido) query = query.eq("sido", sido);
    if (sggu) query = query.eq("sggu", sggu);
  }

  const { data: clinics } = await query;
  const scores = (clinics ?? [])
    .map((c) => c.latest_score as number)
    .filter((s) => s != null)
    .sort((a, b) => a - b);

  if (scores.length === 0) {
    return NextResponse.json({
      audit_id: auditId,
      region: sido ? { sido, sggu } : null,
      region_name: regionName,
      top_25_avg: 0,
      median: 0,
      bottom_25_avg: 0,
      total_count: 0,
      your_score: audit.total_score,
      your_percentile: null,
      distribution: [],
      rank: null,
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

  // Distribution histogram (actual data, not estimated)
  const distribution = buildDistribution(scores);

  // Percentile and rank
  let yourPercentile: number | null = null;
  let rank: number | null = null;
  if (audit.total_score != null) {
    const lowerCount = scores.filter((s) => s < audit.total_score!).length;
    yourPercentile = Math.round((lowerCount / n) * 100);
    const higherCount = scores.filter((s) => s > audit.total_score!).length;
    rank = higherCount + 1;
  }

  return NextResponse.json({
    audit_id: auditId,
    region: sido ? { sido, sggu } : null,
    region_name: regionName,
    top_25_avg: Math.round(avg(topScores) * 10) / 10,
    median: Math.round(median * 10) / 10,
    bottom_25_avg: Math.round(avg(bottomScores) * 10) / 10,
    total_count: n,
    your_score: audit.total_score,
    your_percentile: yourPercentile,
    distribution,
    rank,
  });
}
