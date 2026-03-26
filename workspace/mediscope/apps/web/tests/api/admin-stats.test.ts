import { describe, it, expect, vi, beforeEach } from "vitest";

const mockFrom = vi.fn();

vi.mock("@/lib/supabase/admin", () => ({
  createAdminClient: vi.fn(() => ({ from: mockFrom })),
}));

import { GET } from "@/app/api/admin/stats/route";

describe("GET /api/admin/stats", () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  it("should return stats counts", async () => {
    mockFrom.mockImplementation((table: string) => {
      // All calls use .select('id', { count: 'exact', head: true })
      // which returns { count, error }
      const baseCounts: Record<string, number> = {
        audits: 42,
        leads: 15,
      };

      return {
        select: vi.fn(
          (_col: string, opts?: { count?: string; head?: boolean }) => {
            if (opts?.count === "exact" && opts?.head) {
              // leads table may have .eq('status', ...) chained
              const result = { count: baseCounts[table] ?? 0, error: null };
              return {
                ...result,
                eq: vi.fn((_field: string, value: string) => {
                  if (value === "consulting") return { count: 5, error: null };
                  if (value === "contracted") return { count: 3, error: null };
                  return { count: 0, error: null };
                }),
              };
            }
            return { eq: vi.fn().mockReturnThis() };
          },
        ),
      };
    });

    const res = await GET();
    const data = await res.json();

    expect(res.status).toBe(200);
    expect(typeof data.audits).toBe("number");
    expect(typeof data.leads).toBe("number");
    expect(typeof data.consulting).toBe("number");
    expect(typeof data.contracted).toBe("number");
  });
});
