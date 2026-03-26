import { NextRequest, NextResponse } from "next/server";
import { createAdminClient } from "@/lib/supabase/admin";

export async function GET(
  _request: NextRequest,
  { params }: { params: Promise<{ id: string }> },
) {
  try {
    const { id } = await params;
    const supabase = createAdminClient();

    const [procedureResult, detailsResult, translationsResult] =
      await Promise.all([
        supabase.from("procedures").select("*").eq("id", id).single(),
        supabase
          .from("procedure_details")
          .select("*")
          .eq("procedure_id", id)
          .single(),
        supabase
          .from("procedure_intl")
          .select("*")
          .eq("procedure_id", id)
          .order("language_code"),
      ]);

    if (procedureResult.error || !procedureResult.data) {
      return NextResponse.json(
        { error: "시술을 찾을 수 없습니다" },
        { status: 404 },
      );
    }

    return NextResponse.json({
      procedure: procedureResult.data,
      details: detailsResult.data,
      translations: translationsResult.data ?? [],
      prices: [],
    });
  } catch {
    return NextResponse.json({ error: "서버 오류" }, { status: 500 });
  }
}
