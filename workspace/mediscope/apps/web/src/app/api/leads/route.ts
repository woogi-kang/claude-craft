import { NextRequest, NextResponse } from "next/server";
import { z } from "zod";
import { createAdminClient } from "@/lib/supabase/admin";

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

    const supabase = createAdminClient();

    const { data: lead, error } = await supabase
      .from("leads")
      .insert({
        audit_id: parsed.data.audit_id,
        email: parsed.data.email,
        name: parsed.data.name,
        hospital_name: parsed.data.hospital_name,
        phone: parsed.data.phone,
        specialty: parsed.data.specialty,
      })
      .select("id, status")
      .single();

    if (error) {
      return NextResponse.json(
        { error: "리드를 생성할 수 없습니다" },
        { status: 500 },
      );
    }

    // TODO: Resend 이메일 발송 트리거

    return NextResponse.json(
      { id: lead.id, status: lead.status },
      { status: 201 },
    );
  } catch {
    return NextResponse.json(
      { error: "서버 오류가 발생했습니다" },
      { status: 500 },
    );
  }
}
