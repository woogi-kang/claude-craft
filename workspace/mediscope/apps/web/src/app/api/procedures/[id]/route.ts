import { NextRequest, NextResponse } from "next/server";
import { createAdminClient } from "@/lib/supabase/admin";

export async function GET(
  _request: NextRequest,
  { params }: { params: Promise<{ id: string }> },
) {
  try {
    const { id } = await params;
    const supabase = createAdminClient();

    // Fetch procedure and details in parallel
    const [procedureResult, detailsResult, priceResult] = await Promise.all([
      supabase.from("procedures").select("*").eq("id", id).single(),
      supabase
        .from("procedure_details")
        .select("*")
        .eq("procedure_id", id)
        .order("lang"),
      supabase
        .from("price_comparison")
        .select("*")
        .eq("procedure_id", id)
        .maybeSingle(),
    ]);

    if (procedureResult.error || !procedureResult.data) {
      return NextResponse.json(
        { error: "시술을 찾을 수 없습니다" },
        { status: 404 },
      );
    }

    return NextResponse.json({
      procedure: procedureResult.data,
      details: detailsResult.data ?? [],
      price_comparison: priceResult.data,
    });
  } catch {
    return NextResponse.json(
      { error: "서버 오류가 발생했습니다" },
      { status: 500 },
    );
  }
}
