import { NextResponse } from "next/server";
import { createAdminClient } from "@/lib/supabase/admin";

export async function GET() {
  const supabase = createAdminClient();

  const [auditsRes, leadsRes, consultingRes, contractedRes] = await Promise.all(
    [
      supabase.from("audits").select("id", { count: "exact", head: true }),
      supabase.from("leads").select("id", { count: "exact", head: true }),
      supabase
        .from("leads")
        .select("id", { count: "exact", head: true })
        .eq("status", "consulting"),
      supabase
        .from("leads")
        .select("id", { count: "exact", head: true })
        .eq("status", "contracted"),
    ],
  );

  return NextResponse.json({
    audits: auditsRes.count ?? 0,
    leads: leadsRes.count ?? 0,
    consulting: consultingRes.count ?? 0,
    contracted: contractedRes.count ?? 0,
  });
}
