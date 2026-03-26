import { describe, it, expect, vi, beforeEach } from "vitest";

const mockOrder = vi.fn();
const mockEq = vi.fn().mockReturnValue({ order: mockOrder });
const mockSelect = vi.fn().mockReturnValue({ eq: mockEq });
const mockFrom = vi.fn().mockReturnValue({ select: mockSelect });

vi.mock("@/lib/supabase/admin", () => ({
  createAdminClient: vi.fn(() => ({ from: mockFrom })),
}));

import { GET } from "@/app/api/score-history/[hospitalId]/route";

function makeRequest(hospitalId: string) {
  const req = new Request(
    `http://localhost/api/score-history/${hospitalId}`,
  ) as any;
  return {
    request: req,
    params: { params: Promise.resolve({ hospitalId }) },
  };
}

describe("GET /api/score-history/[hospitalId]", () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  it("should return score history for a hospital", async () => {
    const historyData = [
      {
        total_score: 60,
        category_scores: { seo: 50, performance: 70 },
        created_at: "2026-03-01T00:00:00Z",
      },
      {
        total_score: 80,
        category_scores: { seo: 75, performance: 85 },
        created_at: "2026-03-15T00:00:00Z",
      },
    ];
    mockOrder.mockResolvedValue({ data: historyData, error: null });

    const { request, params } = makeRequest("hospital-1");
    const res = await GET(request, params);
    const data = await res.json();

    expect(res.status).toBe(200);
    expect(data.history).toHaveLength(2);
    expect(data.before).toEqual({ seo: 50, performance: 70 });
    expect(data.current).toEqual({ seo: 75, performance: 85 });
    expect(mockFrom).toHaveBeenCalledWith("score_history");
  });

  it("should return empty array when no history exists", async () => {
    mockOrder.mockResolvedValue({ data: [], error: null });

    const { request, params } = makeRequest("hospital-no-history");
    const res = await GET(request, params);
    const data = await res.json();

    expect(res.status).toBe(200);
    expect(data.history).toEqual([]);
    expect(data.before).toEqual({});
    expect(data.current).toEqual({});
  });

  it("should return 500 on Supabase error", async () => {
    mockOrder.mockResolvedValue({
      data: null,
      error: { message: "db error" },
    });

    const { request, params } = makeRequest("hospital-err");
    const res = await GET(request, params);

    expect(res.status).toBe(500);
    const data = await res.json();
    expect(data.error).toBe("조회 실패");
  });
});
