import { NextRequest, NextResponse } from "next/server";
import { createAdminClient } from "@/lib/supabase/admin";

export async function GET(request: NextRequest) {
  try {
    const supabase = createAdminClient();
    const category = request.nextUrl.searchParams.get("category");

    let query = supabase
      .from("procedures")
      .select(
        "id, category, name_ko, name_en, name_ja, name_zh, description_ko",
      )
      .order("category")
      .order("name_ko");

    if (category) {
      query = query.eq("category", category);
    }

    const { data, error } = await query;

    if (error) {
      return NextResponse.json(
        { error: "시술 목록을 불러올 수 없습니다" },
        { status: 500 },
      );
    }

    return NextResponse.json(data ?? []);
  } catch {
    return NextResponse.json(
      { error: "서버 오류가 발생했습니다" },
      { status: 500 },
    );
  }
}
