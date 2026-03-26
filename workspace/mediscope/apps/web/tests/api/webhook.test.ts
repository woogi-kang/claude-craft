import { describe, it, expect, vi, beforeEach } from "vitest";
import { createHmac, createHash } from "crypto";
import { createNextRequest } from "../helpers";

const mockFrom = vi.fn();

vi.mock("@/lib/supabase/admin", () => ({
  createAdminClient: vi.fn(() => ({ from: mockFrom })),
}));

import { GET as lineGET, POST as linePOST } from "@/app/api/webhook/line/route";
import {
  GET as wechatGET,
  POST as wechatPOST,
} from "@/app/api/webhook/wechat/route";

function makeChain(data: unknown = [], error: unknown = null) {
  const chain: Record<string, unknown> = {};
  const proxy = new Proxy(chain, {
    get(_target, prop) {
      if (prop === "then") {
        return (resolve: (v: unknown) => void) => resolve({ data, error });
      }
      return vi.fn().mockReturnValue(proxy);
    },
  });
  return proxy;
}

describe("LINE webhook", () => {
  beforeEach(() => {
    vi.clearAllMocks();
    mockFrom.mockReturnValue(makeChain([]));

    // Mock fetch for LINE API calls
    vi.stubGlobal(
      "fetch",
      vi.fn().mockResolvedValue({
        ok: true,
        status: 200,
        json: vi.fn().mockResolvedValue({ displayName: "TestUser" }),
      }),
    );
  });

  it("GET should return 200", async () => {
    const res = await lineGET();

    expect(res.status).toBe(200);
    const data = await res.json();
    expect(data.status).toBe("ok");
  });

  it("POST should return 200 with valid signature", async () => {
    const body = JSON.stringify({
      events: [
        {
          type: "message",
          replyToken: "test-reply-token",
          source: { userId: "user123456", type: "user" },
          message: { type: "text", text: "안녕하세요" },
        },
      ],
    });

    const signature = createHmac("SHA256", "test-line-secret")
      .update(body)
      .digest("base64");

    const req = createNextRequest("http://localhost/api/webhook/line", {
      method: "POST",
      body,
      headers: {
        "Content-Type": "application/json",
        "x-line-signature": signature,
      },
    });

    const res = await linePOST(req as any);

    expect(res.status).toBe(200);
  });

  it("POST should return 403 with invalid signature", async () => {
    const body = JSON.stringify({ events: [] });

    const req = createNextRequest("http://localhost/api/webhook/line", {
      method: "POST",
      body,
      headers: {
        "Content-Type": "application/json",
        "x-line-signature": "invalid-signature",
      },
    });

    const res = await linePOST(req as any);

    expect(res.status).toBe(403);
  });
});

describe("WeChat webhook", () => {
  beforeEach(() => {
    vi.clearAllMocks();
    mockFrom.mockReturnValue(makeChain([]));
  });

  function generateWechatSignature(timestamp: string, nonce: string): string {
    const token = "test-wechat-token";
    const sorted = [token, timestamp, nonce].sort().join("");
    return createHash("sha1").update(sorted).digest("hex");
  }

  it("GET should return echostr with valid signature", async () => {
    const timestamp = "1234567890";
    const nonce = "nonce123";
    const echostr = "echo_test_string";
    const signature = generateWechatSignature(timestamp, nonce);

    const url = `http://localhost/api/webhook/wechat?signature=${signature}&timestamp=${timestamp}&nonce=${nonce}&echostr=${echostr}`;
    const req = createNextRequest(url, { method: "GET" });

    const res = await wechatGET(req as any);
    const text = await res.text();

    expect(res.status).toBe(200);
    expect(text).toBe(echostr);
  });

  it("GET should return 403 with invalid signature", async () => {
    const url = `http://localhost/api/webhook/wechat?signature=invalid&timestamp=123&nonce=abc&echostr=test`;
    const req = createNextRequest(url, { method: "GET" });

    const res = await wechatGET(req as any);

    expect(res.status).toBe(403);
  });

  it("POST should return XML response for text message", async () => {
    const timestamp = "1234567890";
    const nonce = "nonce123";
    const signature = generateWechatSignature(timestamp, nonce);

    const xmlBody = `<xml>
      <ToUserName><![CDATA[gh_test]]></ToUserName>
      <FromUserName><![CDATA[user123]]></FromUserName>
      <CreateTime>1234567890</CreateTime>
      <MsgType><![CDATA[text]]></MsgType>
      <Content><![CDATA[咨询]]></Content>
      <MsgId>12345</MsgId>
    </xml>`;

    const url = `http://localhost/api/webhook/wechat?signature=${signature}&timestamp=${timestamp}&nonce=${nonce}`;
    const req = createNextRequest(url, {
      method: "POST",
      body: xmlBody,
      headers: { "Content-Type": "application/xml" },
    });

    const res = await wechatPOST(req as any);
    const text = await res.text();

    expect(res.status).toBe(200);
    expect(text).toContain("<xml>");
    expect(text).toContain("<MsgType><![CDATA[text]]></MsgType>");
    expect(text).toContain("MediScope");
  });

  it("POST should return 403 with invalid signature", async () => {
    const url = `http://localhost/api/webhook/wechat?signature=invalid&timestamp=123&nonce=abc`;
    const req = createNextRequest(url, {
      method: "POST",
      body: "<xml></xml>",
      headers: { "Content-Type": "application/xml" },
    });

    const res = await wechatPOST(req as any);

    expect(res.status).toBe(403);
  });

  it("POST should return success for non-text message", async () => {
    const timestamp = "1234567890";
    const nonce = "nonce123";
    const signature = generateWechatSignature(timestamp, nonce);

    const xmlBody = `<xml>
      <ToUserName><![CDATA[gh_test]]></ToUserName>
      <FromUserName><![CDATA[user123]]></FromUserName>
      <CreateTime>1234567890</CreateTime>
      <MsgType><![CDATA[image]]></MsgType>
      <PicUrl><![CDATA[http://example.com/img.jpg]]></PicUrl>
      <MsgId>12345</MsgId>
    </xml>`;

    const url = `http://localhost/api/webhook/wechat?signature=${signature}&timestamp=${timestamp}&nonce=${nonce}`;
    const req = createNextRequest(url, {
      method: "POST",
      body: xmlBody,
      headers: { "Content-Type": "application/xml" },
    });

    const res = await wechatPOST(req as any);
    const text = await res.text();

    expect(res.status).toBe(200);
    expect(text).toBe("success");
  });
});
