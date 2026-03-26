import { NextRequest, NextResponse } from "next/server";
import { createAdminClient } from "@/lib/supabase/admin";

export async function GET(
  _request: NextRequest,
  { params }: { params: Promise<{ auditId: string }> },
) {
  const { auditId } = await params;
  const supabase = createAdminClient();

  // Fetch the audit to get the URL/location context
  const { data: audit, error: auditError } = await supabase
    .from("audits")
    .select("id, url, total_score, scores, details")
    .eq("id", auditId)
    .single();

  if (auditError || !audit) {
    return NextResponse.json(
      { error: "진단을 찾을 수 없습니다" },
      { status: 404 },
    );
  }

  // Extract sido/sggu from audit details if available
  const sido = (audit.details as Record<string, unknown>)?.sido as
    | string
    | undefined;
  const sggu = (audit.details as Record<string, unknown>)?.sggu as
    | string
    | undefined;

  if (!sido) {
    // If no location info, return basic competition data for 서울 as default
    const { count: totalClinics } = await supabase
      .from("beauty_clinics")
      .select("*", { count: "exact", head: true });

    return NextResponse.json({
      audit_id: auditId,
      audit_url: audit.url,
      total_score: audit.total_score,
      region: null,
      total_clinics: totalClinics ?? 0,
      region_clinics: 0,
      foreign_patient_facilitators: 0,
      website_count: 0,
      website_rate: 0,
    });
  }

  // Get clinics in the same sido
  const { data: regionClinics, error: regionError } = await supabase
    .from("beauty_clinics")
    .select("id, name, sido, sggu, website, is_foreign_patient_facilitator")
    .eq("sido", sido);

  if (regionError) {
    return NextResponse.json(
      { error: "경쟁 데이터 조회 실패" },
      { status: 500 },
    );
  }

  const clinics = regionClinics ?? [];
  const sgguClinics = sggu ? clinics.filter((c) => c.sggu === sggu) : clinics;

  const withWebsite = sgguClinics.filter((c) => c.website);
  const foreignFacilitators = sgguClinics.filter(
    (c) => c.is_foreign_patient_facilitator,
  );

  return NextResponse.json({
    audit_id: auditId,
    audit_url: audit.url,
    total_score: audit.total_score,
    region: { sido, sggu },
    total_clinics: clinics.length,
    region_clinics: sgguClinics.length,
    foreign_patient_facilitators: foreignFacilitators.length,
    foreign_patient_rate:
      sgguClinics.length > 0
        ? Math.round((foreignFacilitators.length / sgguClinics.length) * 100)
        : 0,
    website_count: withWebsite.length,
    website_rate:
      sgguClinics.length > 0
        ? Math.round((withWebsite.length / sgguClinics.length) * 100)
        : 0,
    top_competitors: withWebsite.slice(0, 10).map((c) => ({
      name: c.name,
      sggu: c.sggu,
      has_website: !!c.website,
      is_foreign_patient_facilitator: c.is_foreign_patient_facilitator,
    })),
  });
}
