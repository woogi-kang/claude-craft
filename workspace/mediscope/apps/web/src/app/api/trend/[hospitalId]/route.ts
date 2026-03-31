import { NextRequest, NextResponse } from "next/server";
import { createAdminClient } from "@/lib/supabase/admin";
import { getGrade } from "@/lib/types";

const PERIOD_DAYS: Record<string, number> = {
  "30d": 30,
  "90d": 90,
  "180d": 180,
  "1y": 365,
};

export async function GET(
  request: NextRequest,
  { params }: { params: Promise<{ hospitalId: string }> },
) {
  try {
    const { hospitalId } = await params;
    const period = request.nextUrl.searchParams.get("period") ?? "90d";
    const days = PERIOD_DAYS[period] ?? 90;

    const supabase = createAdminClient();

    const since = new Date();
    since.setDate(since.getDate() - days);

    const { data: history, error } = await supabase
      .from("score_history")
      .select("total_score, grade, category_scores, created_at")
      .eq("hospital_id", hospitalId)
      .gte("created_at", since.toISOString())
      .order("created_at", { ascending: true });

    if (error) {
      return NextResponse.json({ error: "조회 실패" }, { status: 500 });
    }

    const records = history ?? [];

    if (records.length === 0) {
      return NextResponse.json({
        hospital_id: hospitalId,
        history: [],
        changes: null,
        improved_items: [],
        declined_items: [],
        unchanged_items: [],
      });
    }

    const formatted = records.map((h) => ({
      scanned_at: h.created_at,
      total_score: h.total_score,
      grade: h.grade ?? getGrade(h.total_score ?? 0),
      category_scores: h.category_scores ?? {},
    }));

    const current = formatted[formatted.length - 1];
    const previous =
      formatted.length >= 2 ? formatted[formatted.length - 2] : null;

    // Compute changes
    let changes: Record<string, unknown> | null = null;
    const improvedItems: string[] = [];
    const declinedItems: string[] = [];
    const unchangedItems: string[] = [];

    if (previous) {
      const totalDelta =
        (current.total_score ?? 0) - (previous.total_score ?? 0);
      const byCategory: Record<
        string,
        { current: number; previous: number; delta: number }
      > = {};

      const currentCat = (current.category_scores ?? {}) as Record<
        string,
        number
      >;
      const prevCat = (previous.category_scores ?? {}) as Record<
        string,
        number
      >;

      const allKeys = new Set([
        ...Object.keys(currentCat),
        ...Object.keys(prevCat),
      ]);
      for (const key of allKeys) {
        const cur = currentCat[key] ?? 0;
        const prev = prevCat[key] ?? 0;
        const delta = cur - prev;
        byCategory[key] = { current: cur, previous: prev, delta };

        if (delta > 0) improvedItems.push(key);
        else if (delta < 0) declinedItems.push(key);
        else unchangedItems.push(key);
      }

      changes = {
        total: {
          current: current.total_score ?? 0,
          previous: previous.total_score ?? 0,
          delta: totalDelta,
          direction: totalDelta > 0 ? "up" : totalDelta < 0 ? "down" : "same",
        },
        by_category: byCategory,
      };
    }

    return NextResponse.json({
      hospital_id: hospitalId,
      history: formatted,
      changes,
      improved_items: improvedItems,
      declined_items: declinedItems,
      unchanged_items: unchangedItems,
    });
  } catch {
    return NextResponse.json({ error: "서버 오류" }, { status: 500 });
  }
}
