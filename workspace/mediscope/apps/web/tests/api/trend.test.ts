import { describe, it, expect, vi, beforeEach } from "vitest";

const mockOrder = vi.fn();
const mockGte = vi.fn().mockReturnValue({ order: mockOrder });
const mockEq = vi.fn().mockReturnValue({ gte: mockGte });
const mockSelect = vi.fn().mockReturnValue({ eq: mockEq });
const mockFrom = vi.fn().mockReturnValue({ select: mockSelect });

vi.mock("@/lib/supabase/admin", () => ({
  createAdminClient: vi.fn(() => ({ from: mockFrom })),
}));

import { GET } from "@/app/api/trend/[hospitalId]/route";

function makeRequest(hospitalId: string, period?: string) {
  const url = period
    ? `http://localhost/api/trend/${hospitalId}?period=${period}`
    : `http://localhost/api/trend/${hospitalId}`;
  const req = new Request(url) as any;
  req.nextUrl = new URL(url);
  return {
    request: req,
    params: { params: Promise.resolve({ hospitalId }) },
  };
}

const historyData = [
  {
    total_score: 52,
    grade: "D",
    category_scores: { technical_seo: 60, performance: 45, geo_aeo: 30 },
    created_at: "2026-03-01T00:00:00Z",
  },
  {
    total_score: 78,
    grade: "B",
    category_scores: { technical_seo: 85, performance: 70, geo_aeo: 30 },
    created_at: "2026-03-15T00:00:00Z",
  },
];

describe("GET /api/trend/[hospitalId]", () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  it("should return trend data with changes when history has 2+ entries", async () => {
    mockOrder.mockResolvedValue({ data: historyData, error: null });

    const { request, params } = makeRequest("hospital-1");
    const res = await GET(request, params);
    const data = await res.json();

    expect(res.status).toBe(200);
    expect(data.hospital_id).toBe("hospital-1");
    expect(data.history).toHaveLength(2);
    expect(data.history[0].scanned_at).toBe("2026-03-01T00:00:00Z");
    expect(data.history[1].total_score).toBe(78);

    // Changes
    expect(data.changes).not.toBeNull();
    expect(data.changes.total.current).toBe(78);
    expect(data.changes.total.previous).toBe(52);
    expect(data.changes.total.delta).toBe(26);
    expect(data.changes.total.direction).toBe("up");

    // Category changes
    expect(data.changes.by_category.technical_seo.delta).toBe(25);
    expect(data.changes.by_category.performance.delta).toBe(25);
    expect(data.changes.by_category.geo_aeo.delta).toBe(0);

    // Improved items
    expect(data.improved_items).toContain("technical_seo");
    expect(data.improved_items).toContain("performance");
    expect(data.unchanged_items).toContain("geo_aeo");
    expect(data.declined_items).toEqual([]);
  });

  it("should return empty result when no history", async () => {
    mockOrder.mockResolvedValue({ data: [], error: null });

    const { request, params } = makeRequest("hospital-empty");
    const res = await GET(request, params);
    const data = await res.json();

    expect(res.status).toBe(200);
    expect(data.history).toEqual([]);
    expect(data.changes).toBeNull();
  });

  it("should return null changes when only one entry", async () => {
    mockOrder.mockResolvedValue({
      data: [historyData[0]],
      error: null,
    });

    const { request, params } = makeRequest("hospital-single");
    const res = await GET(request, params);
    const data = await res.json();

    expect(res.status).toBe(200);
    expect(data.history).toHaveLength(1);
    expect(data.changes).toBeNull();
  });

  it("should accept period parameter", async () => {
    mockOrder.mockResolvedValue({ data: historyData, error: null });

    const { request, params } = makeRequest("hospital-1", "30d");
    await GET(request, params);

    // Verify gte was called with a date within ~30 days
    expect(mockGte).toHaveBeenCalledWith("created_at", expect.any(String));
  });

  it("should return 500 on database error", async () => {
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

  it("should detect declined items", async () => {
    const declineData = [
      {
        total_score: 80,
        grade: "A",
        category_scores: { technical_seo: 90, performance: 80 },
        created_at: "2026-03-01T00:00:00Z",
      },
      {
        total_score: 60,
        grade: "B",
        category_scores: { technical_seo: 70, performance: 50 },
        created_at: "2026-03-15T00:00:00Z",
      },
    ];
    mockOrder.mockResolvedValue({ data: declineData, error: null });

    const { request, params } = makeRequest("hospital-decline");
    const res = await GET(request, params);
    const data = await res.json();

    expect(data.changes.total.direction).toBe("down");
    expect(data.declined_items).toContain("technical_seo");
    expect(data.declined_items).toContain("performance");
    expect(data.improved_items).toEqual([]);
  });
});
