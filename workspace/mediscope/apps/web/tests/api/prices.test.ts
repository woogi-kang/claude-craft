import { describe, it, expect, vi, beforeEach } from "vitest";

const mockFrom = vi.fn();

vi.mock("@/lib/supabase/admin", () => ({
  createAdminClient: vi.fn(() => ({ from: mockFrom })),
}));

import { GET } from "@/app/api/prices/compare/route";

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

describe("GET /api/prices/compare", () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  it("should return grouped price comparison data", async () => {
    mockFrom.mockImplementation((table: string) => {
      if (table === "price_comparison") {
        return makeChain([
          {
            id: 1,
            therapy_id: 10,
            price_min: 50000,
            price_max: 150000,
            currency: "KRW",
            country: "KR",
            condition_note: null,
          },
          {
            id: 2,
            therapy_id: 10,
            price_min: 200,
            price_max: 500,
            currency: "USD",
            country: "US",
            condition_note: null,
          },
        ]);
      }
      if (table === "beauty_std_procedures") {
        return makeChain([{ id: 10, name: "보톡스" }]);
      }
      if (table === "intl_prices") {
        return makeChain([]);
      }
      return makeChain([]);
    });

    const req = new Request("http://localhost/api/prices/compare", {
      method: "GET",
    });
    const res = await GET();
    const data = await res.json();

    expect(res.status).toBe(200);
    expect(Array.isArray(data)).toBe(true);
    if (data.length > 0) {
      expect(data[0].procedure_id).toBeDefined();
      expect(data[0].procedure_name).toBeDefined();
      expect(data[0].prices).toBeDefined();
    }
  });

  it("should return empty array when no prices exist", async () => {
    mockFrom.mockImplementation((table: string) => {
      if (table === "price_comparison") return makeChain([]);
      if (table === "beauty_std_procedures") return makeChain([]);
      if (table === "intl_prices") return makeChain([]);
      return makeChain([]);
    });

    const res = await GET();
    const data = await res.json();

    expect(res.status).toBe(200);
    expect(data).toEqual([]);
  });

  it("should return 500 on error", async () => {
    mockFrom.mockImplementation((table: string) => {
      if (table === "price_comparison")
        return makeChain(null, { message: "db error" });
      return makeChain([]);
    });

    const res = await GET();

    expect(res.status).toBe(500);
  });
});
