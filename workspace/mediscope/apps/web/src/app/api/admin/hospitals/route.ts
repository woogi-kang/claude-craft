import { NextResponse } from "next/server";
import { createAdminClient } from "@/lib/supabase/admin";

export async function GET() {
  try {
    const supabase = createAdminClient();

    const { data: hospitals, error } = await supabase
      .from("hospitals")
      .select("id, name, url, specialty, region, latest_score, created_at")
      .order("created_at", { ascending: false });

    if (error) {
      return NextResponse.json({ error: "조회 실패" }, { status: 500 });
    }

    return NextResponse.json(hospitals ?? []);
  } catch {
    return NextResponse.json({ error: "서버 오류" }, { status: 500 });
  }
}
