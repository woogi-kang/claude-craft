import { NextRequest, NextResponse } from "next/server";
import { z } from "zod";

const WORKER_URL = process.env.WORKER_URL ?? "";
const WORKER_API_KEY = process.env.WORKER_API_KEY ?? "";

const createSubscriptionSchema = z.object({
  audit_id: z.string().uuid(),
  email: z.string().email("올바른 이메일을 입력해주세요"),
  frequency: z.enum(["weekly", "biweekly", "monthly"], {
    message: "빈도는 weekly, biweekly, monthly 중 하나여야 합니다",
  }),
});

export async function POST(request: NextRequest) {
  try {
    const body = await request.json();
    const parsed = createSubscriptionSchema.safeParse(body);

    if (!parsed.success) {
      return NextResponse.json(
        { error: parsed.error.issues[0]?.message ?? "잘못된 요청입니다" },
        { status: 400 },
      );
    }

    const res = await fetch(`${WORKER_URL}/worker/subscriptions`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${WORKER_API_KEY}`,
      },
      body: JSON.stringify(parsed.data),
    });

    if (!res.ok) {
      const err = await res.json().catch(() => ({}));
      return NextResponse.json(
        {
          error:
            (err as { error?: string }).error ?? "구독 생성에 실패했습니다",
        },
        { status: res.status },
      );
    }

    const data = await res.json();
    return NextResponse.json(data, { status: 201 });
  } catch {
    return NextResponse.json(
      { error: "서버 오류가 발생했습니다" },
      { status: 500 },
    );
  }
}

export async function GET(request: NextRequest) {
  try {
    const email = request.nextUrl.searchParams.get("email");

    if (!email) {
      return NextResponse.json(
        { error: "이메일 파라미터가 필요합니다" },
        { status: 400 },
      );
    }

    const res = await fetch(
      `${WORKER_URL}/worker/subscriptions?email=${encodeURIComponent(email)}`,
      {
        headers: {
          Authorization: `Bearer ${WORKER_API_KEY}`,
        },
      },
    );

    if (!res.ok) {
      return NextResponse.json(
        { error: "구독 조회에 실패했습니다" },
        { status: res.status },
      );
    }

    const data = await res.json();
    return NextResponse.json(data);
  } catch {
    return NextResponse.json(
      { error: "서버 오류가 발생했습니다" },
      { status: 500 },
    );
  }
}
