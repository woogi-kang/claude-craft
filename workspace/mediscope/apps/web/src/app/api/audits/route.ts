import { NextRequest, NextResponse } from "next/server";
import { z } from "zod";

const createAuditSchema = z.object({
  url: z.string().url("올바른 URL을 입력해주세요"),
  specialty: z.string().optional(),
});

export async function POST(request: NextRequest) {
  try {
    const body = await request.json();
    const parsed = createAuditSchema.safeParse(body);

    if (!parsed.success) {
      return NextResponse.json(
        { error: parsed.error.issues[0]?.message ?? "잘못된 요청입니다" },
        { status: 400 },
      );
    }

    // TODO: Supabase insert + worker trigger
    // For now, return a mock response
    const id = crypto.randomUUID();

    return NextResponse.json(
      { id, status: "pending", estimated_time_seconds: 60 },
      { status: 202 },
    );
  } catch {
    return NextResponse.json(
      { error: "서버 오류가 발생했습니다" },
      { status: 500 },
    );
  }
}
