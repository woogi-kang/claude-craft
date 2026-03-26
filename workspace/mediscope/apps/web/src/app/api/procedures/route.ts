import { NextRequest, NextResponse } from "next/server";
import { createAdminClient } from "@/lib/supabase/admin";

export async function GET(request: NextRequest) {
  try {
    const supabase = createAdminClient();
    const categoryId = request.nextUrl.searchParams.get("category_id");

    let query = supabase
      .from("procedures")
      .select("id, name, grade, primary_category_id, thumbnail_url, is_leaf")
      .order("primary_category_id")
      .order("name");

    if (categoryId) {
      query = query.eq("primary_category_id", categoryId);
    }

    const { data, error } = await query;

    if (error) {
      return NextResponse.json({ error: error.message }, { status: 500 });
    }

    return NextResponse.json(data ?? []);
  } catch {
    return NextResponse.json({ error: "서버 오류" }, { status: 500 });
  }
}
