import { NextRequest, NextResponse } from "next/server";
import { createHash } from "crypto";
import { createAdminClient } from "@/lib/supabase/admin";

const WECHAT_TOKEN = process.env.WECHAT_TOKEN ?? "";
const WECHAT_APP_ID = process.env.WECHAT_APP_ID ?? "";

function verifySignature(
  signature: string,
  timestamp: string,
  nonce: string,
): boolean {
  if (!WECHAT_TOKEN) return false;
  const sorted = [WECHAT_TOKEN, timestamp, nonce].sort().join("");
  const hash = createHash("sha1").update(sorted).digest("hex");
  return hash === signature;
}

function parseXmlValue(xml: string, tag: string): string {
  const match = xml.match(
    new RegExp(`<${tag}><!\\[CDATA\\[(.+?)\\]\\]></${tag}>`),
  );
  if (match) return match[1];
  const simple = xml.match(new RegExp(`<${tag}>(.+?)</${tag}>`));
  return simple?.[1] ?? "";
}

function buildXmlReply(
  toUser: string,
  fromUser: string,
  content: string,
): string {
  const timestamp = Math.floor(Date.now() / 1000);
  return `<xml>
<ToUserName><![CDATA[${toUser}]]></ToUserName>
<FromUserName><![CDATA[${fromUser}]]></FromUserName>
<CreateTime>${timestamp}</CreateTime>
<MsgType><![CDATA[text]]></MsgType>
<Content><![CDATA[${content}]]></Content>
</xml>`;
}

async function generateChatResponse(message: string): Promise<string> {
  if (
    message.includes("咨询") ||
    message.includes("预约") ||
    message.includes("상담")
  ) {
    return "您好！欢迎使用CheckYourHospital医疗旅游咨询服务。专业顾问将尽快与您联系，请留下您的问题。";
  }
  return "您好！欢迎使用CheckYourHospital。如需医疗旅游咨询，请输入'咨询'。";
}

export async function GET(request: NextRequest) {
  if (!WECHAT_TOKEN) {
    return new NextResponse("WeChat integration not configured", {
      status: 503,
    });
  }

  const { searchParams } = request.nextUrl;
  const signature = searchParams.get("signature") ?? "";
  const timestamp = searchParams.get("timestamp") ?? "";
  const nonce = searchParams.get("nonce") ?? "";
  const echostr = searchParams.get("echostr") ?? "";

  if (!verifySignature(signature, timestamp, nonce)) {
    return new NextResponse("Invalid signature", { status: 403 });
  }

  return new NextResponse(echostr, {
    headers: { "Content-Type": "text/plain" },
  });
}

export async function POST(request: NextRequest) {
  if (!WECHAT_TOKEN) {
    return new NextResponse("WeChat integration not configured", {
      status: 503,
    });
  }

  const { searchParams } = request.nextUrl;
  const signature = searchParams.get("signature") ?? "";
  const timestamp = searchParams.get("timestamp") ?? "";
  const nonce = searchParams.get("nonce") ?? "";

  if (!verifySignature(signature, timestamp, nonce)) {
    return new NextResponse("Invalid signature", { status: 403 });
  }

  try {
    const body = await request.text();

    const msgType = parseXmlValue(body, "MsgType");
    const fromUser = parseXmlValue(body, "FromUserName");
    const toUser = parseXmlValue(body, "ToUserName");

    // Save lead
    const supabase = createAdminClient();
    await supabase.from("leads").upsert(
      {
        name: `WeChat_${fromUser.slice(0, 8)}`,
        email: `${fromUser}@wechat.messenger`,
        source: "wechat",
        source_id: fromUser,
      },
      { onConflict: "source,source_id", ignoreDuplicates: true },
    );

    // Handle text messages with passive reply
    if (msgType === "text") {
      const content = parseXmlValue(body, "Content");
      const reply = await generateChatResponse(content);
      const xml = buildXmlReply(fromUser, toUser, reply);

      return new NextResponse(xml, {
        headers: { "Content-Type": "application/xml" },
      });
    }

    // Non-text messages: return success (empty response = no reply)
    return new NextResponse("success", {
      headers: { "Content-Type": "text/plain" },
    });
  } catch {
    return new NextResponse("success", {
      headers: { "Content-Type": "text/plain" },
    });
  }
}
