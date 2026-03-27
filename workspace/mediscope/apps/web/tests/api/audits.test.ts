import { describe, it, expect, vi, beforeEach } from "vitest";

vi.mock("@/lib/supabase/admin", () => ({
  createAdminClient: vi.fn(() => ({ from: mockFrom })),
}));

vi.mock("@/lib/rate-limit", () => ({
  checkRateLimit: vi.fn(() => ({ allowed: true })),
}));

const mockFrom = vi.fn();

import { POST } from "@/app/api/audits/route";

function makeRequest(body: unknown) {
  return new Request("http://localhost/api/audits", {
    method: "POST",
    body: JSON.stringify(body),
    headers: { "Content-Type": "application/json" },
  });
}

// Helper: create a chainable mock that resolves at the end
function makeChain(resolveValue: { data: unknown; error: unknown }) {
  const chain: Record<string, unknown> = {};
  const handler = {
    get(_: unknown, prop: string) {
      if (["single", "maybeSingle"].includes(prop)) {
        return () => Promise.resolve(resolveValue);
      }
      if (prop === "then") return undefined; // not a thenable
      return (..._args: unknown[]) => new Proxy({}, handler);
    },
  };
  return new Proxy(chain, handler);
}

describe("POST /api/audits", () => {
  beforeEach(() => {
    vi.clearAllMocks();

    // Default mock: no cache, no existing hospital, successful inserts
    mockFrom.mockImplementation((table: string) => {
      if (table === "audits") {
        return {
          // Cache check (select chain)
          select: () => makeChain({ data: null, error: null }),
          // Insert
          insert: () => ({
            select: () => ({
              single: () =>
                Promise.resolve({
                  data: {
                    id: "audit-123",
                    status: "pending",
                    created_at: "2026-03-27T00:00:00Z",
                  },
                  error: null,
                }),
            }),
          }),
        };
      }
      if (table === "hospitals") {
        return {
          select: () => makeChain({ data: null, error: null }),
          insert: () => ({
            select: () => ({
              single: () =>
                Promise.resolve({
                  data: { id: "hospital-1" },
                  error: null,
                }),
            }),
          }),
        };
      }
      return makeChain({ data: null, error: null });
    });
  });

  it("should return 202 with audit ID for a valid URL", async () => {
    const req = makeRequest({ url: "https://example.com" });
    const res = await POST(req as any);
    const data = await res.json();

    expect(res.status).toBe(202);
    expect(data.id).toBe("audit-123");
    expect(data.status).toBe("pending");
  });

  it("should return 400 when URL is missing", async () => {
    const req = makeRequest({});
    const res = await POST(req as any);
    expect(res.status).toBe(400);
  });

  it("should return 400 for an invalid URL", async () => {
    const req = makeRequest({ url: "not-a-url" });
    const res = await POST(req as any);
    expect(res.status).toBe(400);
  });

  it("should return 500 when audit insert fails", async () => {
    mockFrom.mockImplementation((table: string) => {
      if (table === "hospitals") {
        return {
          select: () => makeChain({ data: { id: "hospital-1" }, error: null }),
        };
      }
      if (table === "audits") {
        return {
          select: () => makeChain({ data: null, error: null }),
          insert: () => ({
            select: () => ({
              single: () =>
                Promise.resolve({
                  data: null,
                  error: { message: "insert error" },
                }),
            }),
          }),
        };
      }
      return makeChain({ data: null, error: null });
    });

    const req = makeRequest({ url: "https://example.com" });
    const res = await POST(req as any);
    expect(res.status).toBe(500);
  });

  it("should use existing hospital if found", async () => {
    const hospitalInsert = vi.fn();
    mockFrom.mockImplementation((table: string) => {
      if (table === "hospitals") {
        return {
          select: () =>
            makeChain({ data: { id: "existing-hospital" }, error: null }),
          insert: hospitalInsert,
        };
      }
      if (table === "audits") {
        return {
          select: () => makeChain({ data: null, error: null }),
          insert: () => ({
            select: () => ({
              single: () =>
                Promise.resolve({
                  data: {
                    id: "audit-456",
                    status: "pending",
                    created_at: "2026-03-27",
                  },
                  error: null,
                }),
            }),
          }),
        };
      }
      return makeChain({ data: null, error: null });
    });

    const req = makeRequest({ url: "https://example.com" });
    const res = await POST(req as any);
    expect(res.status).toBe(202);
    expect(hospitalInsert).not.toHaveBeenCalled();
  });
});
