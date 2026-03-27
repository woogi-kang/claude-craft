import { NextRequest, NextResponse } from "next/server";
import { createHmac, timingSafeEqual } from "crypto";
import { createAdminClient } from "@/lib/supabase/admin";

const LINE_CHANNEL_SECRET = process.env.LINE_CHANNEL_SECRET ?? "";
const LINE_CHANNEL_ACCESS_TOKEN = process.env.LINE_CHANNEL_ACCESS_TOKEN ?? "";

interface LineEvent {
  type: string;
  replyToken: string;
  source: { userId: string; type: string };
  message?: { type: string; text?: string };
}

function verifySignature(body: string, signature: string): boolean {
  if (!LINE_CHANNEL_SECRET) return false;
  const hash = createHmac("SHA256", LINE_CHANNEL_SECRET)
    .update(body)
    .digest("base64");
  const hashBuf = Buffer.from(hash);
  const sigBuf = Buffer.from(signature);
  if (hashBuf.length !== sigBuf.length) return false;
  return timingSafeEqual(hashBuf, sigBuf);
}

async function replyToLine(replyToken: string, text: string): Promise<void> {
  await fetch("https://api.line.me/v2/bot/message/reply", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      Authorization: `Bearer ${LINE_CHANNEL_ACCESS_TOKEN}`,
    },
    body: JSON.stringify({
      replyToken,
      messages: [{ type: "text", text }],
    }),
  });
}

async function getLineProfile(
  userId: string,
): Promise<{ displayName: string } | null> {
  try {
    const res = await fetch(`https://api.line.me/v2/bot/profile/${userId}`, {
      headers: { Authorization: `Bearer ${LINE_CHANNEL_ACCESS_TOKEN}` },
    });
    if (!res.ok) return null;
    return res.json();
  } catch {
    return null;
  }
}

async function generateChatResponse(message: string): Promise<string> {
  // TODO: 챗봇 API가 준비되면 연동. 현재는 기본 응답.
  if (
    message.includes("상담") ||
    message.includes("예약") ||
    message.includes("문의")
  ) {
    return "안녕하세요! MediScope 의료관광 상담 서비스입니다. 전문 상담사가 곧 연락드리겠습니다. 궁금하신 사항을 남겨주세요.";
  }
  return "안녕하세요! MediScope입니다. 의료관광 상담을 원하시면 '상담'이라고 입력해주세요.";
}

export async function GET() {
  // LINE webhook verification - just return 200
  return NextResponse.json({ status: "ok" });
}

export async function POST(request: NextRequest) {
  if (!LINE_CHANNEL_SECRET || !LINE_CHANNEL_ACCESS_TOKEN) {
    return NextResponse.json(
      { error: "LINE integration not configured" },
      { status: 503 },
    );
  }

  try {
    const body = await request.text();
    const signature = request.headers.get("x-line-signature") ?? "";

    if (!verifySignature(body, signature)) {
      return NextResponse.json({ error: "Invalid signature" }, { status: 403 });
    }

    const payload = JSON.parse(body) as { events: LineEvent[] };
    const supabase = createAdminClient();

    for (const event of payload.events) {
      if (event.type !== "message" || !event.message) continue;

      const userId = event.source.userId;

      // Save lead
      const profile = await getLineProfile(userId);
      const displayName = profile?.displayName ?? `LINE_${userId.slice(0, 8)}`;

      await supabase.from("leads").upsert(
        {
          name: displayName,
          email: `${userId}@line.messenger`,
          source: "line",
          source_id: userId,
        },
        { onConflict: "source,source_id", ignoreDuplicates: true },
      );

      // Handle text messages
      if (event.message.type === "text" && event.message.text) {
        const reply = await generateChatResponse(event.message.text);
        await replyToLine(event.replyToken, reply);
      }
    }

    return NextResponse.json({ status: "ok" });
  } catch {
    return NextResponse.json(
      { error: "서버 오류가 발생했습니다" },
      { status: 500 },
    );
  }
}
