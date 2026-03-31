import { NextResponse } from "next/server";
import { createServerSupabaseClient } from "@/lib/supabase/server";

const WORKER_URL = process.env.CONTENT_WORKER_URL ?? "";

export async function GET() {
  const supabase = await createServerSupabaseClient();
  const {
    data: { user },
  } = await supabase.auth.getUser();

  if (!user || user.app_metadata?.role !== "admin") {
    return NextResponse.json({ error: "Unauthorized" }, { status: 401 });
  }

  const res = await fetch(`${WORKER_URL}/content/procedures`);
  const data = await res.json();
  return NextResponse.json(data, { status: res.status });
}
