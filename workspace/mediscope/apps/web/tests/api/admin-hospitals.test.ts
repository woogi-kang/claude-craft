import { describe, it, expect, vi, beforeEach } from "vitest";

const mockFrom = vi.fn();

vi.mock("@/lib/supabase/admin", () => ({
  createAdminClient: vi.fn(() => ({ from: mockFrom })),
}));

import { GET } from "@/app/api/admin/hospitals/route";
import { GET as GET_DETAIL } from "@/app/api/admin/hospitals/[id]/route";

describe("GET /api/admin/hospitals", () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  it("should return hospital list", async () => {
    const hospitals = [
      { id: "h1", name: "Hospital A", region: "Seoul" },
      { id: "h2", name: "Hospital B", region: "Busan" },
    ];
    mockFrom.mockReturnValue({
      select: vi.fn().mockReturnValue({
        order: vi.fn().mockResolvedValue({ data: hospitals, error: null }),
      }),
    });

    const res = await GET();
    const data = await res.json();

    expect(res.status).toBe(200);
    expect(data).toHaveLength(2);
    expect(data[0].name).toBe("Hospital A");
    expect(mockFrom).toHaveBeenCalledWith("hospitals");
  });

  it("should return 500 on Supabase error", async () => {
    mockFrom.mockReturnValue({
      select: vi.fn().mockReturnValue({
        order: vi
          .fn()
          .mockResolvedValue({ data: null, error: { message: "db error" } }),
      }),
    });

    const res = await GET();
    expect(res.status).toBe(500);
  });
});

describe("GET /api/admin/hospitals/[id]", () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  it("should return hospital detail", async () => {
    const hospital = {
      id: "h1",
      name: "Hospital A",
      url: "https://hospital-a.com",
      specialty: "dermatology",
    };
    mockFrom.mockReturnValue({
      select: vi.fn().mockReturnValue({
        eq: vi.fn().mockReturnValue({
          single: vi.fn().mockResolvedValue({ data: hospital, error: null }),
        }),
      }),
    });

    const req = new Request("http://localhost/api/admin/hospitals/h1") as any;
    const params = { params: Promise.resolve({ id: "h1" }) };
    const res = await GET_DETAIL(req, params);
    const data = await res.json();

    expect(res.status).toBe(200);
    expect(data.name).toBe("Hospital A");
    expect(mockFrom).toHaveBeenCalledWith("hospitals");
  });

  it("should return 404 when hospital not found", async () => {
    mockFrom.mockReturnValue({
      select: vi.fn().mockReturnValue({
        eq: vi.fn().mockReturnValue({
          single: vi.fn().mockResolvedValue({
            data: null,
            error: { message: "not found" },
          }),
        }),
      }),
    });

    const req = new Request(
      "http://localhost/api/admin/hospitals/nonexistent",
    ) as any;
    const params = { params: Promise.resolve({ id: "nonexistent" }) };
    const res = await GET_DETAIL(req, params);

    expect(res.status).toBe(404);
    const data = await res.json();
    expect(data.error).toBe("병원을 찾을 수 없습니다");
  });
});
