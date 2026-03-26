import { describe, it, expect, vi, beforeEach } from "vitest";

const mockFrom = vi.fn();

vi.mock("@/lib/supabase/admin", () => ({
  createAdminClient: vi.fn(() => ({ from: mockFrom })),
}));

import { PATCH } from "@/app/api/projects/[id]/tasks/route";

function makeParams(id: string) {
  return { params: Promise.resolve({ id }) };
}

function makeRequest(id: string, body: unknown) {
  return new Request(`http://localhost/api/projects/${id}/tasks`, {
    method: "PATCH",
    body: JSON.stringify(body),
    headers: { "Content-Type": "application/json" },
  }) as any;
}

const existingPlan = {
  tasks: [
    { id: "task-1", title: "Existing Task", priority: "medium", done: false },
  ],
};

describe("PATCH /api/projects/[id]/tasks", () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  it('should add a task (action: "add")', async () => {
    mockFrom.mockImplementation((table: string) => {
      if (table === "projects") {
        return {
          select: vi.fn().mockReturnValue({
            eq: vi.fn().mockReturnValue({
              single: vi.fn().mockResolvedValue({
                data: { plan: { tasks: [] } },
                error: null,
              }),
            }),
          }),
          update: vi.fn().mockReturnValue({
            eq: vi.fn().mockResolvedValue({ error: null }),
          }),
        };
      }
      return {};
    });

    const req = makeRequest("p1", {
      action: "add",
      data: { title: "New Task", category: "seo" },
    });

    const res = await PATCH(req, makeParams("p1"));
    const data = await res.json();

    expect(res.status).toBe(200);
    expect(data.tasks).toHaveLength(1);
    expect(data.tasks[0].title).toBe("New Task");
    expect(data.task).toBeDefined();
    expect(data.task.id).toBeDefined();
  });

  it('should update a task (action: "update")', async () => {
    mockFrom.mockImplementation((table: string) => {
      if (table === "projects") {
        return {
          select: vi.fn().mockReturnValue({
            eq: vi.fn().mockReturnValue({
              single: vi.fn().mockResolvedValue({
                data: { plan: existingPlan },
                error: null,
              }),
            }),
          }),
          update: vi.fn().mockReturnValue({
            eq: vi.fn().mockResolvedValue({ error: null }),
          }),
        };
      }
      return {};
    });

    const req = makeRequest("p1", {
      action: "update",
      taskId: "task-1",
      data: { done: true },
    });

    const res = await PATCH(req, makeParams("p1"));
    const data = await res.json();

    expect(res.status).toBe(200);
    expect(data.tasks[0].done).toBe(true);
  });

  it('should remove a task (action: "remove")', async () => {
    mockFrom.mockImplementation((table: string) => {
      if (table === "projects") {
        return {
          select: vi.fn().mockReturnValue({
            eq: vi.fn().mockReturnValue({
              single: vi.fn().mockResolvedValue({
                data: { plan: existingPlan },
                error: null,
              }),
            }),
          }),
          update: vi.fn().mockReturnValue({
            eq: vi.fn().mockResolvedValue({ error: null }),
          }),
        };
      }
      return {};
    });

    const req = makeRequest("p1", {
      action: "remove",
      taskId: "task-1",
    });

    const res = await PATCH(req, makeParams("p1"));
    const data = await res.json();

    expect(res.status).toBe(200);
    expect(data.tasks).toHaveLength(0);
  });

  it("should return 400 for invalid action", async () => {
    mockFrom.mockImplementation((table: string) => {
      if (table === "projects") {
        return {
          select: vi.fn().mockReturnValue({
            eq: vi.fn().mockReturnValue({
              single: vi.fn().mockResolvedValue({
                data: { plan: { tasks: [] } },
                error: null,
              }),
            }),
          }),
        };
      }
      return {};
    });

    const req = makeRequest("p1", { action: "invalid" });

    const res = await PATCH(req, makeParams("p1"));
    expect(res.status).toBe(400);
    const data = await res.json();
    expect(data.error).toBe("잘못된 요청");
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

    const req = makeRequest("nonexistent", {
      action: "add",
      data: { title: "Task" },
    });

    const res = await PATCH(req, makeParams("nonexistent"));
    expect(res.status).toBe(404);
  });
});
