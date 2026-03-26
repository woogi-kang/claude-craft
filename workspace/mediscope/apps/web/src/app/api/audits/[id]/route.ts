import { NextRequest, NextResponse } from "next/server";
import { createAdminClient } from "@/lib/supabase/admin";

export async function GET(
  _request: NextRequest,
  { params }: { params: Promise<{ id: string }> },
) {
  const { id } = await params;
  const supabase = createAdminClient();

  const { data: audit, error } = await supabase
    .from("audits")
    .select(
      "id, hospital_id, url, status, total_score, grade, scores, details, report_url, scan_duration_ms, created_at, updated_at",
    )
    .eq("id", id)
    .single();

  if (error || !audit) {
    return NextResponse.json(
      { error: "진단을 찾을 수 없습니다" },
      { status: 404 },
    );
  }

  return NextResponse.json(audit);
}
