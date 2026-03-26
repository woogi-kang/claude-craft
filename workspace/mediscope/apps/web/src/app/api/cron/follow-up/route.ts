import { NextRequest, NextResponse } from "next/server";
import { createAdminClient } from "@/lib/supabase/admin";
import { sendFollowUpEmail } from "@/lib/resend";

const CRON_SECRET = process.env.CRON_SECRET ?? "";

// Follow-up schedule: days since lead creation → email template
const FOLLOW_UP_SCHEDULE = [
  { days: 3, template: "followup_1", subject: "리포트 확인하셨나요?" },
  { days: 7, template: "followup_2", subject: "무료 30분 상담을 제안드립니다" },
  {
    days: 14,
    template: "followup_3",
    subject: "경쟁 병원은 이미 시작했습니다",
  },
  {
    days: 30,
    template: "rediagnose",
    subject: "한 달이 지났습니다. 다시 진단해보세요",
  },
];

export async function POST(request: NextRequest) {
  // Verify cron secret (Cloud Scheduler auth)
  const authHeader = request.headers.get("authorization");
  if (CRON_SECRET && authHeader !== `Bearer ${CRON_SECRET}`) {
    return NextResponse.json({ error: "Unauthorized" }, { status: 401 });
  }

  const supabase = createAdminClient();
  const now = new Date();
  let sent = 0;
  let skipped = 0;

  for (const schedule of FOLLOW_UP_SCHEDULE) {
    // Find leads created exactly N days ago that haven't received this template
    const targetDate = new Date(now);
    targetDate.setDate(targetDate.getDate() - schedule.days);
    const dateStr = targetDate.toISOString().split("T")[0];

    // Get leads created on target date, status is 'new' or 'contacted'
    const { data: leads } = await supabase
      .from("leads")
      .select("id, email, name, hospital_name, audit_id, emails_sent, status")
      .gte("created_at", `${dateStr}T00:00:00`)
      .lt("created_at", `${dateStr}T23:59:59`)
      .in("status", ["new", "contacted"])
      .lt(
        "emails_sent",
        schedule.days === 3
          ? 2
          : schedule.days === 7
            ? 3
            : schedule.days === 14
              ? 4
              : 5,
      );

    if (!leads?.length) {
      skipped += 1;
      continue;
    }

    for (const lead of leads) {
      // Check if this template was already sent
      const { data: existingLog } = await supabase
        .from("email_logs")
        .select("id")
        .eq("lead_id", lead.id)
        .eq("template", schedule.template)
        .limit(1);

      if (existingLog?.length) continue;

      // Get audit score for email content
      const { data: audit } = await supabase
        .from("audits")
        .select("total_score")
        .eq("id", lead.audit_id)
        .single();

      try {
        await sendFollowUpEmail({
          to: lead.email,
          name: lead.name,
          hospitalName: lead.hospital_name ?? "",
          totalScore: audit?.total_score ?? 0,
          template: schedule.template,
        });

        // Log email
        await supabase.from("email_logs").insert({
          lead_id: lead.id,
          template: schedule.template,
        });

        // Update lead
        await supabase
          .from("leads")
          .update({
            emails_sent: lead.emails_sent + 1,
            last_email_at: now.toISOString(),
            status: lead.status === "new" ? "contacted" : lead.status,
          })
          .eq("id", lead.id);

        sent += 1;
      } catch {
        // Skip failed sends
      }
    }
  }

  return NextResponse.json({
    ok: true,
    sent,
    skipped,
    timestamp: now.toISOString(),
  });
}
