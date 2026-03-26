import { NextRequest, NextResponse } from "next/server";
import { createAdminClient } from "@/lib/supabase/admin";

export async function GET(
  _request: NextRequest,
  { params }: { params: Promise<{ id: string }> },
) {
  try {
    const { id } = await params;
    const supabase = createAdminClient();

    const { data: project, error } = await supabase
      .from("projects")
      .select(
        `
        *,
        hospitals:hospital_id (id, name, url, latest_score),
        leads:lead_id (id, name, email, hospital_name)
      `,
      )
      .eq("id", id)
      .single();

    if (error || !project) {
      return NextResponse.json(
        { error: "프로젝트를 찾을 수 없습니다" },
        { status: 404 },
      );
    }

    return NextResponse.json(project);
  } catch {
    return NextResponse.json({ error: "서버 오류" }, { status: 500 });
  }
}

export async function PATCH(
  request: NextRequest,
  { params }: { params: Promise<{ id: string }> },
) {
  try {
    const { id } = await params;
    const body = await request.json();
    const supabase = createAdminClient();

    const allowedFields = [
      "status",
      "name",
      "contract_amount",
      "start_date",
      "end_date",
      "plan",
      "before_audit_id",
      "latest_audit_id",
    ];
    const updates: Record<string, unknown> = {};
    for (const key of allowedFields) {
      if (key in body) {
        updates[key] = body[key];
      }
    }

    const { data: project, error } = await supabase
      .from("projects")
      .update(updates)
      .eq("id", id)
      .select("*")
      .single();

    if (error) {
      return NextResponse.json({ error: "수정 실패" }, { status: 500 });
    }

    return NextResponse.json(project);
  } catch {
    return NextResponse.json({ error: "서버 오류" }, { status: 500 });
  }
}
