import { NextRequest, NextResponse } from "next/server";
import { z } from "zod";

const createLeadSchema = z.object({
  audit_id: z.string().uuid(),
  email: z.string().email("올바른 이메일을 입력해주세요"),
  name: z.string().min(1, "이름을 입력해주세요"),
  hospital_name: z.string().optional(),
  phone: z.string().optional(),
  specialty: z.string().optional(),
});

export async function POST(request: NextRequest) {
  try {
    const body = await request.json();
    const parsed = createLeadSchema.safeParse(body);

    if (!parsed.success) {
      return NextResponse.json(
        { error: parsed.error.issues[0]?.message ?? "잘못된 요청입니다" },
        { status: 400 },
      );
    }

    // TODO: Supabase insert + email trigger
    const id = crypto.randomUUID();

    return NextResponse.json({ id, status: "new" }, { status: 201 });
  } catch {
    return NextResponse.json(
      { error: "서버 오류가 발생했습니다" },
      { status: 500 },
    );
  }
}
