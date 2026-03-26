import { NextRequest, NextResponse } from "next/server";
import { createAdminClient } from "@/lib/supabase/admin";

export async function POST(request: NextRequest) {
  const supabase = createAdminClient();

  // Fetch beauty_clinics with websites
  const { data: clinics, error } = await supabase
    .from("beauty_clinics")
    .select("id, website")
    .not("website", "is", null)
    .neq("website", "")
    .limit(500);

  if (error) {
    return NextResponse.json(
      { error: "클리닉 데이터 조회 실패" },
      { status: 500 },
    );
  }

  const urls = (clinics ?? [])
    .map((c) => c.website as string)
    .filter((w) => w && (w.startsWith("http://") || w.startsWith("https://")));

  if (urls.length === 0) {
    return NextResponse.json(
      { error: "스캔할 URL이 없습니다" },
      { status: 400 },
    );
  }

  // Call Worker's batch-scan endpoint
  const workerUrl = process.env.WORKER_URL || "http://localhost:8000";
  try {
    const res = await fetch(`${workerUrl}/worker/batch-scan`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ urls, update_db: true }),
    });

    if (!res.ok) {
      const text = await res.text();
      return NextResponse.json(
        { error: `Worker 오류: ${text}` },
        { status: res.status },
      );
    }

    const result = await res.json();
    return NextResponse.json(result);
  } catch (e) {
    return NextResponse.json(
      { error: `Worker 연결 실패: ${String(e)}` },
      { status: 502 },
    );
  }
}
