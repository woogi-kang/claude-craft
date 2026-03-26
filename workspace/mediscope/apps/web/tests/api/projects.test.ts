import { describe, it, expect, vi, beforeEach } from "vitest";

const mockFrom = vi.fn();

vi.mock("@/lib/supabase/admin", () => ({
  createAdminClient: vi.fn(() => ({ from: mockFrom })),
}));

import { GET, POST } from "@/app/api/projects/route";

describe("GET /api/projects", () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  it("should return project list", async () => {
    const projects = [
      { id: "p1", name: "Project A", status: "planning" },
      { id: "p2", name: "Project B", status: "active" },
    ];
    mockFrom.mockReturnValue({
      select: vi.fn().mockReturnValue({
        order: vi.fn().mockResolvedValue({ data: projects, error: null }),
      }),
    });

    const res = await GET();
    const data = await res.json();

    expect(res.status).toBe(200);
    expect(data).toHaveLength(2);
    expect(data[0].name).toBe("Project A");
    expect(mockFrom).toHaveBeenCalledWith("projects");
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

describe("POST /api/projects", () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  it("should create a new project and return 201", async () => {
    const createdProject = {
      id: "new-p",
      name: "New Project",
      status: "planning",
      client_token: "some-uuid",
    };
    mockFrom.mockReturnValue({
      insert: vi.fn().mockReturnValue({
        select: vi.fn().mockReturnValue({
          single: vi
            .fn()
            .mockResolvedValue({ data: createdProject, error: null }),
        }),
      }),
    });

    const req = new Request("http://localhost/api/projects", {
      method: "POST",
      body: JSON.stringify({
        lead_id: "00000000-0000-0000-0000-000000000001",
        hospital_id: "00000000-0000-0000-0000-000000000002",
        name: "New Project",
      }),
      headers: { "Content-Type": "application/json" },
    });

    const res = await POST(req as any);
    const data = await res.json();

    expect(res.status).toBe(201);
    expect(data.name).toBe("New Project");
    expect(mockFrom).toHaveBeenCalledWith("projects");
  });

  it("should return 400 when required fields are missing", async () => {
    const req = new Request("http://localhost/api/projects", {
      method: "POST",
      body: JSON.stringify({ name: "No IDs" }),
      headers: { "Content-Type": "application/json" },
    });

    const res = await POST(req as any);
    expect(res.status).toBe(400);
  });

  it("should auto-generate client_token", async () => {
    const insertFn = vi.fn().mockReturnValue({
      select: vi.fn().mockReturnValue({
        single: vi.fn().mockResolvedValue({
          data: { id: "p-new", client_token: "generated-uuid" },
          error: null,
        }),
      }),
    });
    mockFrom.mockReturnValue({ insert: insertFn });

    const req = new Request("http://localhost/api/projects", {
      method: "POST",
      body: JSON.stringify({
        lead_id: "00000000-0000-0000-0000-000000000001",
        hospital_id: "00000000-0000-0000-0000-000000000002",
        name: "Token Test",
      }),
      headers: { "Content-Type": "application/json" },
    });

    await POST(req as any);

    const insertedData = insertFn.mock.calls[0][0];
    expect(insertedData.client_token).toBeDefined();
    expect(insertedData.client_token).toMatch(
      /^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$/,
    );
  });
});
