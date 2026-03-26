import { describe, it, expect, vi, beforeEach } from "vitest";

const mockFrom = vi.fn();

vi.mock("@/lib/supabase/admin", () => ({
  createAdminClient: vi.fn(() => ({ from: mockFrom })),
}));

import { GET, PATCH } from "@/app/api/projects/[id]/route";

function makeParams(id: string) {
  return { params: Promise.resolve({ id }) };
}

describe("GET /api/projects/[id]", () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  it("should return project detail", async () => {
    const project = {
      id: "p1",
      name: "Project A",
      status: "active",
      hospitals: { id: "h1", name: "Hospital A" },
    };
    mockFrom.mockReturnValue({
      select: vi.fn().mockReturnValue({
        eq: vi.fn().mockReturnValue({
          single: vi.fn().mockResolvedValue({ data: project, error: null }),
        }),
      }),
    });

    const req = new Request("http://localhost/api/projects/p1") as any;
    const res = await GET(req, makeParams("p1"));
    const data = await res.json();

    expect(res.status).toBe(200);
    expect(data.name).toBe("Project A");
    expect(mockFrom).toHaveBeenCalledWith("projects");
  });

  it("should return 404 when project not found", async () => {
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

    const req = new Request("http://localhost/api/projects/nonexistent") as any;
    const res = await GET(req, makeParams("nonexistent"));

    expect(res.status).toBe(404);
    const data = await res.json();
    expect(data.error).toBe("프로젝트를 찾을 수 없습니다");
  });
});

describe("PATCH /api/projects/[id]", () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  it("should update project fields", async () => {
    const updated = { id: "p1", name: "Updated", status: "active" };
    mockFrom.mockReturnValue({
      update: vi.fn().mockReturnValue({
        eq: vi.fn().mockReturnValue({
          select: vi.fn().mockReturnValue({
            single: vi.fn().mockResolvedValue({ data: updated, error: null }),
          }),
        }),
      }),
    });

    const req = new Request("http://localhost/api/projects/p1", {
      method: "PATCH",
      body: JSON.stringify({ name: "Updated", status: "active" }),
      headers: { "Content-Type": "application/json" },
    }) as any;

    const res = await PATCH(req, makeParams("p1"));
    const data = await res.json();

    expect(res.status).toBe(200);
    expect(data.name).toBe("Updated");
  });

  it("should return 500 on update error", async () => {
    mockFrom.mockReturnValue({
      update: vi.fn().mockReturnValue({
        eq: vi.fn().mockReturnValue({
          select: vi.fn().mockReturnValue({
            single: vi.fn().mockResolvedValue({
              data: null,
              error: { message: "update failed" },
            }),
          }),
        }),
      }),
    });

    const req = new Request("http://localhost/api/projects/p1", {
      method: "PATCH",
      body: JSON.stringify({ status: "completed" }),
      headers: { "Content-Type": "application/json" },
    }) as any;

    const res = await PATCH(req, makeParams("p1"));
    expect(res.status).toBe(500);
  });
});
