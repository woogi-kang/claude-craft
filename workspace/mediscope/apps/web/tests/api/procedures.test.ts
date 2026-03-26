import { describe, it, expect, vi, beforeEach } from "vitest";

const mockFrom = vi.fn();

vi.mock("@/lib/supabase/admin", () => ({
  createAdminClient: vi.fn(() => ({ from: mockFrom })),
}));

import { GET } from "@/app/api/procedures/route";
import { createNextRequest } from "../helpers";

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

describe("GET /api/procedures", () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  it("should return procedure list", async () => {
    mockFrom.mockReturnValue(
      makeChain([
        {
          id: 1,
          name: "보톡스",
          grade: 5,
          primary_category_id: 1,
          thumbnail_url: null,
          is_leaf: true,
        },
        {
          id: 2,
          name: "필러",
          grade: 4,
          primary_category_id: 1,
          thumbnail_url: null,
          is_leaf: true,
        },
      ]),
    );

    const req = createNextRequest("http://localhost/api/procedures", {
      method: "GET",
    });
    const res = await GET(req as any);
    const data = await res.json();

    expect(res.status).toBe(200);
    expect(Array.isArray(data)).toBe(true);
    expect(data.length).toBe(2);
    expect(data[0].name).toBe("보톡스");
  });

  it("should filter by category_id", async () => {
    mockFrom.mockReturnValue(
      makeChain([
        {
          id: 3,
          name: "레이저 토닝",
          grade: 3,
          primary_category_id: 3,
          thumbnail_url: null,
          is_leaf: true,
        },
      ]),
    );

    const req = createNextRequest(
      "http://localhost/api/procedures?category_id=3",
      {
        method: "GET",
      },
    );
    const res = await GET(req as any);
    const data = await res.json();

    expect(res.status).toBe(200);
    expect(Array.isArray(data)).toBe(true);
  });

  it("should return 500 on supabase error", async () => {
    mockFrom.mockReturnValue(makeChain(null, { message: "db error" }));

    const req = createNextRequest("http://localhost/api/procedures", {
      method: "GET",
    });
    const res = await GET(req as any);

    expect(res.status).toBe(500);
  });
});
