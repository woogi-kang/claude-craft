import { NextRequest, NextResponse } from "next/server";
import { createAdminClient } from "@/lib/supabase/admin";

export async function GET(
  _request: NextRequest,
  { params }: { params: Promise<{ hospitalId: string }> },
) {
  try {
    const { hospitalId } = await params;
    const supabase = createAdminClient();

    const { data: history, error } = await supabase
      .from("score_history")
      .select("total_score, category_scores, created_at")
      .eq("hospital_id", hospitalId)
      .order("created_at", { ascending: true });

    if (error) {
      return NextResponse.json({ error: "조회 실패" }, { status: 500 });
    }

    const formatted = (history ?? []).map((h) => ({
      date: h.created_at,
      total_score: h.total_score,
      category_scores: h.category_scores,
    }));

    const before = formatted.length > 0 ? formatted[0].category_scores : {};
    const current =
      formatted.length > 0
        ? formatted[formatted.length - 1].category_scores
        : {};

    return NextResponse.json({
      history: formatted,
      before,
      current,
    });
  } catch {
    return NextResponse.json({ error: "서버 오류" }, { status: 500 });
  }
}
