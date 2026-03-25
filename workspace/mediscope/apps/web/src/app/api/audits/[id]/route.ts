import { NextRequest, NextResponse } from "next/server";

export async function GET(
  _request: NextRequest,
  { params }: { params: Promise<{ id: string }> },
) {
  const { id } = await params;

  // TODO: Supabase query
  // For now, return mock data
  const mockAudit = {
    id,
    hospital_id: null,
    url: "https://example-clinic.com",
    status: "completed" as const,
    total_score: 38,
    grade: "D" as const,
    scores: {
      technical_seo: 32,
      performance: 45,
      geo_aeo: 18,
      multilingual: 0,
      competitiveness: 22,
    },
    details: {},
    report_url: null,
    scan_duration_ms: 45000,
    created_at: new Date().toISOString(),
    updated_at: new Date().toISOString(),
  };

  return NextResponse.json(mockAudit);
}
