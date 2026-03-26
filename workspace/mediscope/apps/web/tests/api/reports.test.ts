import { describe, it, expect, vi, beforeEach } from "vitest";

const mockFrom = vi.fn();

vi.mock("@/lib/supabase/admin", () => ({
  createAdminClient: vi.fn(() => ({ from: mockFrom })),
}));

import { GET } from "@/app/api/reports/[id]/route";

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

describe("GET /api/reports/[id]", () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  it("should return HTML report for valid audit", async () => {
    mockFrom.mockReturnValue(
      makeChain({
        url: "https://example.com",
        total_score: 85,
        grade: "A",
        scores: {
          robots_txt: { score: 100, grade: "pass", issues: [] },
          sitemap: { score: 80, grade: "pass", issues: [] },
          meta_tags: {
            score: 70,
            grade: "warn",
            issues: ["Missing description"],
          },
        },
      }),
    );

    const req = new Request("http://localhost/api/reports/test-id", {
      method: "GET",
    });
    const res = await GET(req as any, {
      params: Promise.resolve({ id: "test-id" }),
    });

    expect(res.status).toBe(200);
    const text = await res.text();
    expect(text).toContain("<!DOCTYPE html>");
    expect(text).toContain("CheckYourHospital");
    expect(text).toContain("85");
    expect(text).toContain("example.com");
    expect(res.headers.get("Content-Type")).toContain("text/html");
  });

  it("should return 404 for non-existent audit", async () => {
    mockFrom.mockReturnValue(makeChain(null, { message: "not found" }));

    const req = new Request("http://localhost/api/reports/nonexistent", {
      method: "GET",
    });
    const res = await GET(req as any, {
      params: Promise.resolve({ id: "nonexistent" }),
    });

    expect(res.status).toBe(404);
  });
});
