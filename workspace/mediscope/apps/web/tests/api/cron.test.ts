import { describe, it, expect, vi, beforeEach } from "vitest";

// Mock supabase admin for follow-up route
const mockFrom = vi.fn();
vi.mock("@/lib/supabase/admin", () => ({
  createAdminClient: vi.fn(() => ({ from: mockFrom })),
}));

vi.mock("@/lib/resend", () => ({
  sendReportEmail: vi.fn().mockResolvedValue({ id: "mock-email-id" }),
  sendFollowUpEmail: vi.fn().mockResolvedValue({ id: "mock-email-id" }),
}));

import { POST as followUpPOST } from "@/app/api/cron/follow-up/route";
import { POST as rescanPOST } from "@/app/api/cron/rescan/route";

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

function makeFollowUpRequest(secret?: string) {
  const headers: Record<string, string> = {
    "Content-Type": "application/json",
  };
  if (secret) {
    headers["authorization"] = `Bearer ${secret}`;
  }
  return new Request("http://localhost/api/cron/follow-up", {
    method: "POST",
    headers,
  });
}

function makeRescanRequest(secret?: string) {
  const headers: Record<string, string> = {
    "Content-Type": "application/json",
  };
  if (secret) {
    headers["authorization"] = `Bearer ${secret}`;
  }
  return new Request("http://localhost/api/cron/rescan", {
    method: "POST",
    headers,
  });
}

describe("POST /api/cron/follow-up", () => {
  beforeEach(() => {
    vi.clearAllMocks();
    // No leads found by default
    mockFrom.mockReturnValue(makeChain([]));
  });

  it("should return 401 with wrong secret", async () => {
    const req = makeFollowUpRequest("wrong-secret");
    const res = await followUpPOST(req as any);

    expect(res.status).toBe(401);
  });

  it("should return 200 with correct secret", async () => {
    const req = makeFollowUpRequest("test-cron-secret");
    const res = await followUpPOST(req as any);
    const data = await res.json();

    expect(res.status).toBe(200);
    expect(data.ok).toBe(true);
    expect(typeof data.sent).toBe("number");
    expect(typeof data.skipped).toBe("number");
  });

  it("should return 401 with no authorization header", async () => {
    const req = makeFollowUpRequest();
    const res = await followUpPOST(req as any);

    expect(res.status).toBe(401);
  });
});

describe("POST /api/cron/rescan", () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  it("should return 401 with wrong secret", async () => {
    const req = makeRescanRequest("wrong-secret");
    const res = await rescanPOST(req as any);

    expect(res.status).toBe(401);
  });

  it("should return 200 with correct secret and worker success", async () => {
    vi.stubGlobal(
      "fetch",
      vi.fn().mockResolvedValue({
        ok: true,
        status: 200,
        json: vi.fn().mockResolvedValue({ processed: 3 }),
      }),
    );

    const req = makeRescanRequest("test-cron-secret");
    const res = await rescanPOST(req as any);
    const data = await res.json();

    expect(res.status).toBe(200);
    expect(data.ok).toBe(true);
  });

  it("should forward worker error", async () => {
    vi.stubGlobal(
      "fetch",
      vi.fn().mockResolvedValue({
        ok: false,
        status: 502,
        json: vi.fn().mockResolvedValue({ error: "worker down" }),
      }),
    );

    const req = makeRescanRequest("test-cron-secret");
    const res = await rescanPOST(req as any);

    expect(res.status).toBe(502);
  });
});
