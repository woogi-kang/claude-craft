import { NextResponse } from "next/server";
import { createAdminClient } from "@/lib/supabase/admin";

export async function GET() {
  const supabase = createAdminClient();

  const [lineResult, wechatResult] = await Promise.all([
    supabase
      .from("leads")
      .select("id", { count: "exact", head: true })
      .eq("source", "line"),
    supabase
      .from("leads")
      .select("id", { count: "exact", head: true })
      .eq("source", "wechat"),
  ]);

  return NextResponse.json({
    line: {
      configured: !!(
        process.env.LINE_CHANNEL_SECRET && process.env.LINE_CHANNEL_ACCESS_TOKEN
      ),
      leadCount: lineResult.count ?? 0,
    },
    wechat: {
      configured: !!(process.env.WECHAT_TOKEN && process.env.WECHAT_APP_ID),
      leadCount: wechatResult.count ?? 0,
    },
  });
}
