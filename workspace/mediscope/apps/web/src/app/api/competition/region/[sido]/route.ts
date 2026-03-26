import { NextRequest, NextResponse } from "next/server";
import { createAdminClient } from "@/lib/supabase/admin";

export async function GET(
  _request: NextRequest,
  { params }: { params: Promise<{ sido: string }> },
) {
  const { sido } = await params;
  const decodedSido = decodeURIComponent(sido);
  const supabase = createAdminClient();

  const { data: clinics, error } = await supabase
    .from("beauty_clinics")
    .select("id, name, sido, sggu, website, is_foreign_patient_facilitator")
    .eq("sido", decodedSido);

  if (error) {
    return NextResponse.json({ error: "데이터 조회 실패" }, { status: 500 });
  }

  const allClinics = clinics ?? [];

  // Group by sggu
  const sgguMap: Record<
    string,
    { total: number; withWebsite: number; foreignFacilitator: number }
  > = {};

  for (const clinic of allClinics) {
    const key = clinic.sggu ?? "기타";
    if (!sgguMap[key]) {
      sgguMap[key] = { total: 0, withWebsite: 0, foreignFacilitator: 0 };
    }
    sgguMap[key].total += 1;
    if (clinic.website) sgguMap[key].withWebsite += 1;
    if (clinic.is_foreign_patient_facilitator)
      sgguMap[key].foreignFacilitator += 1;
  }

  const distribution = Object.entries(sgguMap)
    .map(([sggu, stats]) => ({
      sggu,
      ...stats,
      websiteRate:
        stats.total > 0
          ? Math.round((stats.withWebsite / stats.total) * 100)
          : 0,
      foreignRate:
        stats.total > 0
          ? Math.round((stats.foreignFacilitator / stats.total) * 100)
          : 0,
    }))
    .sort((a, b) => b.total - a.total);

  const totalWithWebsite = allClinics.filter((c) => c.website).length;
  const totalForeignFacilitator = allClinics.filter(
    (c) => c.is_foreign_patient_facilitator,
  ).length;

  return NextResponse.json({
    sido: decodedSido,
    total_clinics: allClinics.length,
    website_count: totalWithWebsite,
    website_rate:
      allClinics.length > 0
        ? Math.round((totalWithWebsite / allClinics.length) * 100)
        : 0,
    foreign_patient_facilitators: totalForeignFacilitator,
    foreign_patient_rate:
      allClinics.length > 0
        ? Math.round((totalForeignFacilitator / allClinics.length) * 100)
        : 0,
    distribution,
  });
}
