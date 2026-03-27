import { NextRequest, NextResponse } from "next/server";
import { z } from "zod";
import { createAdminClient } from "@/lib/supabase/admin";
import { sendReportEmail } from "@/lib/resend";

const patchSchema = z.object({
  status: z
    .enum([
      "new",
      "contacted",
      "consulting",
      "proposal_sent",
      "contracted",
      "active",
      "churned",
    ])
    .optional(),
  note: z
    .object({
      content: z.string().min(1),
      author: z.string().min(1),
    })
    .optional(),
  resend_report: z.boolean().optional(),
});

export async function GET(
  _request: NextRequest,
  { params }: { params: Promise<{ id: string }> },
) {
  const { id } = await params;
  const supabase = createAdminClient();

  const { data: lead, error } = await supabase
    .from("leads")
    .select(
      "id, name, email, hospital_name, phone, specialty, status, notes, emails_sent, last_email_at, audit_id, created_at, updated_at",
    )
    .eq("id", id)
    .single();

  if (error || !lead) {
    return NextResponse.json(
      { error: "리드를 찾을 수 없습니다" },
      { status: 404 },
    );
  }

  // Fetch linked audit summary
  let audit = null;
  if (lead.audit_id) {
    const { data } = await supabase
      .from("audits")
      .select("id, url, total_score, grade, report_url, created_at")
      .eq("id", lead.audit_id)
      .single();
    audit = data;
  }

  return NextResponse.json({ ...lead, audit });
}

export async function PATCH(
  request: NextRequest,
  { params }: { params: Promise<{ id: string }> },
) {
  const { id } = await params;
  const body = await request.json();
  const parsed = patchSchema.safeParse(body);

  if (!parsed.success) {
    return NextResponse.json(
      { error: parsed.error.issues[0]?.message ?? "잘못된 요청입니다" },
      { status: 400 },
    );
  }

  const supabase = createAdminClient();

  // Fetch current lead
  const { data: lead, error: fetchError } = await supabase
    .from("leads")
    .select("id, name, email, hospital_name, status, notes, audit_id")
    .eq("id", id)
    .single();

  if (fetchError || !lead) {
    return NextResponse.json(
      { error: "리드를 찾을 수 없습니다" },
      { status: 404 },
    );
  }

  const updates: Record<string, unknown> = {
    updated_at: new Date().toISOString(),
  };

  // Status change
  if (parsed.data.status) {
    updates.status = parsed.data.status;
  }

  // Append note
  if (parsed.data.note) {
    const currentNotes = Array.isArray(lead.notes) ? lead.notes : [];
    updates.notes = [
      ...currentNotes,
      {
        date: new Date().toISOString(),
        content: parsed.data.note.content,
        author: parsed.data.note.author,
      },
    ];
  }

  const { data: updated, error: updateError } = await supabase
    .from("leads")
    .update(updates)
    .eq("id", id)
    .select(
      "id, name, email, hospital_name, phone, specialty, status, notes, emails_sent, last_email_at, audit_id, created_at, updated_at",
    )
    .single();

  if (updateError) {
    return NextResponse.json(
      { error: "업데이트에 실패했습니다" },
      { status: 500 },
    );
  }

  // Resend report email
  if (parsed.data.resend_report && lead.audit_id) {
    const { data: audit } = await supabase
      .from("audits")
      .select("url, total_score, grade, report_url")
      .eq("id", lead.audit_id)
      .single();

    if (audit) {
      const origin = request.nextUrl.origin;
      sendReportEmail({
        to: lead.email,
        name: lead.name,
        hospitalName: lead.hospital_name ?? "",
        auditUrl: audit.url,
        totalScore: audit.total_score ?? 0,
        grade: audit.grade ?? "F",
        reportUrl: `${origin}/api/reports/${lead.audit_id}`,
        pdfUrl: audit.report_url ?? undefined,
      }).catch(() => {});

      // Log and increment
      await supabase.from("email_logs").insert({
        lead_id: id,
        template: "report_resend",
      });

      await supabase
        .from("leads")
        .update({
          emails_sent: (updated?.emails_sent ?? 0) + 1,
          last_email_at: new Date().toISOString(),
        })
        .eq("id", id);
    }
  }

  return NextResponse.json(updated);
}
