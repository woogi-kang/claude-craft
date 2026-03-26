import { NextRequest, NextResponse } from "next/server";

const WORKER_URL = process.env.WORKER_URL ?? "";
const WORKER_API_KEY = process.env.WORKER_API_KEY ?? "";
const CRON_SECRET = process.env.CRON_SECRET ?? "";

export async function POST(request: NextRequest) {
  // Verify cron secret (Cloud Scheduler auth)
  const authHeader = request.headers.get("authorization");
  if (CRON_SECRET && authHeader !== `Bearer ${CRON_SECRET}`) {
    return NextResponse.json({ error: "Unauthorized" }, { status: 401 });
  }

  try {
    const res = await fetch(`${WORKER_URL}/worker/subscriptions/process-due`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${WORKER_API_KEY}`,
      },
    });

    if (!res.ok) {
      const err = await res.json().catch(() => ({}));
      return NextResponse.json(
        {
          error:
            (err as { error?: string }).error ?? "재스캔 처리에 실패했습니다",
        },
        { status: res.status },
      );
    }

    const data = await res.json();
    return NextResponse.json({
      ok: true,
      ...data,
      timestamp: new Date().toISOString(),
    });
  } catch {
    return NextResponse.json(
      { error: "서버 오류가 발생했습니다" },
      { status: 500 },
    );
  }
}
