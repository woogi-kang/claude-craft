import { NextRequest, NextResponse } from "next/server";
import { z } from "zod";
import { createAdminClient } from "@/lib/supabase/admin";

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

    const supabase = createAdminClient();

    // 1. Find or create hospital
    const { data: existingHospital } = await supabase
      .from("hospitals")
      .select("id")
      .eq("url", parsed.data.url)
      .single();

    let hospitalId = existingHospital?.id;
    if (!hospitalId) {
      const { data: newHospital } = await supabase
        .from("hospitals")
        .insert({
          name: new URL(parsed.data.url).hostname,
          url: parsed.data.url,
          specialty: parsed.data.specialty,
        })
        .select("id")
        .single();
      hospitalId = newHospital?.id;
    }

    // 2. Create audit record
    const { data: audit, error } = await supabase
      .from("audits")
      .insert({
        hospital_id: hospitalId,
        url: parsed.data.url,
        status: "pending",
      })
      .select("id, status, created_at")
      .single();

    if (error) {
      return NextResponse.json(
        { error: "진단을 생성할 수 없습니다" },
        { status: 500 },
      );
    }

    // 3. Trigger worker scan (fire-and-forget)
    const workerUrl = process.env.WORKER_URL;
    if (workerUrl) {
      fetch(`${workerUrl}/worker/scan`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${process.env.WORKER_API_KEY}`,
        },
        body: JSON.stringify({ audit_id: audit.id, url: parsed.data.url }),
      }).catch(() => {});
    }

    return NextResponse.json(
      { id: audit.id, status: "pending", estimated_time_seconds: 60 },
      { status: 202 },
    );
  } catch {
    return NextResponse.json(
      { error: "서버 오류가 발생했습니다" },
      { status: 500 },
    );
  }
}
