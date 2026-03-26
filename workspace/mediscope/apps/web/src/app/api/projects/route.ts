import { NextRequest, NextResponse } from "next/server";
import { z } from "zod";
import { createAdminClient } from "@/lib/supabase/admin";

const createProjectSchema = z.object({
  lead_id: z.string().uuid(),
  hospital_id: z.string().uuid(),
  name: z.string().min(1),
  contract_amount: z.number().int().optional(),
  start_date: z.string().optional(),
  end_date: z.string().optional(),
});

export async function GET() {
  try {
    const supabase = createAdminClient();

    const { data: projects, error } = await supabase
      .from("projects")
      .select(
        `
        *,
        hospitals:hospital_id (id, name, url, latest_score),
        leads:lead_id (id, name, email, hospital_name)
      `,
      )
      .order("created_at", { ascending: false });

    if (error) {
      return NextResponse.json({ error: "조회 실패" }, { status: 500 });
    }

    return NextResponse.json(projects ?? []);
  } catch {
    return NextResponse.json({ error: "서버 오류" }, { status: 500 });
  }
}

export async function POST(request: NextRequest) {
  try {
    const body = await request.json();
    const parsed = createProjectSchema.safeParse(body);

    if (!parsed.success) {
      return NextResponse.json(
        { error: parsed.error.issues[0]?.message ?? "잘못된 요청" },
        { status: 400 },
      );
    }

    const supabase = createAdminClient();
    const clientToken = crypto.randomUUID();

    const { data: project, error } = await supabase
      .from("projects")
      .insert({
        lead_id: parsed.data.lead_id,
        hospital_id: parsed.data.hospital_id,
        name: parsed.data.name,
        contract_amount: parsed.data.contract_amount,
        start_date: parsed.data.start_date,
        end_date: parsed.data.end_date,
        client_token: clientToken,
        status: "planning",
        plan: { tasks: [] },
      })
      .select("*")
      .single();

    if (error) {
      return NextResponse.json(
        { error: "프로젝트 생성 실패" },
        { status: 500 },
      );
    }

    return NextResponse.json(project, { status: 201 });
  } catch {
    return NextResponse.json({ error: "서버 오류" }, { status: 500 });
  }
}
