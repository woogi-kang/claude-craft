import { NextRequest, NextResponse } from "next/server";
import { createAdminClient } from "@/lib/supabase/admin";

export async function GET(
  _request: NextRequest,
  { params }: { params: Promise<{ id: string }> },
) {
  try {
    const { id } = await params;
    const supabase = createAdminClient();

    const { data: hospital, error } = await supabase
      .from("hospitals")
      .select("*")
      .eq("id", id)
      .single();

    if (error || !hospital) {
      return NextResponse.json(
        { error: "병원을 찾을 수 없습니다" },
        { status: 404 },
      );
    }

    return NextResponse.json(hospital);
  } catch {
    return NextResponse.json({ error: "서버 오류" }, { status: 500 });
  }
}
