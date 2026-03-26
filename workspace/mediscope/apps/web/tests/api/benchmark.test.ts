import { describe, it, expect, vi, beforeEach } from "vitest";

const mockFrom = vi.fn();

vi.mock("@/lib/supabase/admin", () => ({
  createAdminClient: vi.fn(() => ({ from: mockFrom })),
}));

import { GET } from "@/app/api/benchmark/[auditId]/route";

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

function makeRequest(auditId: string) {
  return new Request(`http://localhost/api/benchmark/${auditId}`, {
    method: "GET",
  });
}

describe("GET /api/benchmark/[auditId]", () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  it("should return benchmark data for valid audit", async () => {
    mockFrom.mockImplementation((table: string) => {
      if (table === "audits") {
        return makeChain({
          id: "audit-1",
          url: "https://example.com",
          total_score: 72,
          details: { sido: "서울", sggu: "강남" },
        });
      }
      if (table === "beauty_clinics") {
        return makeChain([
          { latest_score: 60 },
          { latest_score: 70 },
          { latest_score: 80 },
          { latest_score: 90 },
        ]);
      }
      return makeChain([]);
    });

    const req = makeRequest("audit-1");
    const res = await GET(req as any, {
      params: Promise.resolve({ auditId: "audit-1" }),
    });
    const data = await res.json();

    expect(res.status).toBe(200);
    expect(data.audit_id).toBe("audit-1");
    expect(data.your_score).toBe(72);
    expect(data.total_count).toBe(4);
    expect(data.your_percentile).toBeDefined();
    expect(typeof data.median).toBe("number");
    expect(typeof data.top_25_avg).toBe("number");
    expect(typeof data.bottom_25_avg).toBe("number");
  });

  it("should return 404 for non-existent audit", async () => {
    mockFrom.mockImplementation((table: string) => {
      if (table === "audits") {
        return makeChain(null, { message: "not found" });
      }
      return makeChain([]);
    });

    const req = makeRequest("nonexistent");
    const res = await GET(req as any, {
      params: Promise.resolve({ auditId: "nonexistent" }),
    });

    expect(res.status).toBe(404);
  });

  it("should handle zero clinics gracefully", async () => {
    mockFrom.mockImplementation((table: string) => {
      if (table === "audits") {
        return makeChain({
          id: "audit-2",
          url: "https://example.com",
          total_score: 50,
          details: {},
        });
      }
      if (table === "beauty_clinics") {
        return makeChain([]);
      }
      return makeChain([]);
    });

    const req = makeRequest("audit-2");
    const res = await GET(req as any, {
      params: Promise.resolve({ auditId: "audit-2" }),
    });
    const data = await res.json();

    expect(res.status).toBe(200);
    expect(data.total_count).toBe(0);
    expect(data.your_percentile).toBeNull();
  });
});
