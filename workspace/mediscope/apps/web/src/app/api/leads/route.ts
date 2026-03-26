import { NextRequest, NextResponse } from "next/server";
import { z } from "zod";
import { createAdminClient } from "@/lib/supabase/admin";
import { sendReportEmail } from "@/lib/resend";

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

    // 1. Create lead
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

    // 2. Fetch audit data for email
    const { data: audit } = await supabase
      .from("audits")
      .select("url, total_score, grade, report_url")
      .eq("id", parsed.data.audit_id)
      .single();

    // 3. Send report email (fire-and-forget)
    if (audit) {
      const origin = request.nextUrl.origin;
      sendReportEmail({
        to: parsed.data.email,
        name: parsed.data.name,
        hospitalName: parsed.data.hospital_name ?? "",
        auditUrl: audit.url,
        totalScore: audit.total_score ?? 0,
        grade: audit.grade ?? "F",
        reportUrl: `${origin}/api/reports/${parsed.data.audit_id}`,
        pdfUrl: audit.report_url ?? undefined,
      }).catch(() => {});

      // Log email sent
      await supabase.from("email_logs").insert({
        lead_id: lead.id,
        template: "report_delivery",
      });

      await supabase
        .from("leads")
        .update({ emails_sent: 1, last_email_at: new Date().toISOString() })
        .eq("id", lead.id);
    }

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
