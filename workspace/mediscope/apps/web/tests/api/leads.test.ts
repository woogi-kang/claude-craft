import { describe, it, expect, vi, beforeEach } from "vitest";

const mockFrom = vi.fn();

vi.mock("@/lib/supabase/admin", () => ({
  createAdminClient: vi.fn(() => ({ from: mockFrom })),
}));

vi.mock("@/lib/resend", () => ({
  sendReportEmail: vi.fn().mockResolvedValue({ id: "mock-email-id" }),
  sendFollowUpEmail: vi.fn().mockResolvedValue({ id: "mock-email-id" }),
}));

import { POST } from "@/app/api/leads/route";
import { createNextRequest } from "../helpers";

function makeRequest(body: unknown) {
  return createNextRequest("http://localhost/api/leads", {
    method: "POST",
    body: JSON.stringify(body),
    headers: { "Content-Type": "application/json" },
  });
}

describe("POST /api/leads", () => {
  beforeEach(() => {
    vi.clearAllMocks();

    mockFrom.mockImplementation((table: string) => {
      if (table === "leads") {
        return {
          insert: vi.fn().mockReturnValue({
            select: vi.fn().mockReturnValue({
              single: vi.fn().mockResolvedValue({
                data: { id: "lead-1", status: "new" },
                error: null,
              }),
            }),
          }),
          update: vi.fn().mockReturnValue({
            eq: vi.fn().mockResolvedValue({ data: null, error: null }),
          }),
        };
      }
      if (table === "audits") {
        return {
          select: vi.fn().mockReturnValue({
            eq: vi.fn().mockReturnValue({
              single: vi.fn().mockResolvedValue({
                data: {
                  url: "https://example.com",
                  total_score: 75,
                  grade: "B",
                },
                error: null,
              }),
            }),
          }),
        };
      }
      if (table === "email_logs") {
        return {
          insert: vi.fn().mockResolvedValue({ data: null, error: null }),
        };
      }
      return {};
    });
  });

  it("should return 201 with lead ID for valid data", async () => {
    const req = makeRequest({
      audit_id: "550e8400-e29b-41d4-a716-446655440000",
      email: "test@example.com",
      name: "Test User",
    });
    const res = await POST(req as any);
    const data = await res.json();

    expect(res.status).toBe(201);
    expect(data.id).toBe("lead-1");
    expect(data.status).toBe("new");
  });

  it("should return 400 when email is missing", async () => {
    const req = makeRequest({
      audit_id: "550e8400-e29b-41d4-a716-446655440000",
      name: "Test User",
    });
    const res = await POST(req as any);

    expect(res.status).toBe(400);
  });

  it("should return 400 when name is missing", async () => {
    const req = makeRequest({
      audit_id: "550e8400-e29b-41d4-a716-446655440000",
      email: "test@example.com",
    });
    const res = await POST(req as any);

    expect(res.status).toBe(400);
  });

  it("should return 400 when audit_id is not a valid UUID", async () => {
    const req = makeRequest({
      audit_id: "not-a-uuid",
      email: "test@example.com",
      name: "Test User",
    });
    const res = await POST(req as any);

    expect(res.status).toBe(400);
  });

  it("should return 500 when lead insert fails", async () => {
    mockFrom.mockImplementation((table: string) => {
      if (table === "leads") {
        return {
          insert: vi.fn().mockReturnValue({
            select: vi.fn().mockReturnValue({
              single: vi.fn().mockResolvedValue({
                data: null,
                error: { message: "insert error" },
              }),
            }),
          }),
        };
      }
      return {};
    });

    const req = makeRequest({
      audit_id: "550e8400-e29b-41d4-a716-446655440000",
      email: "test@example.com",
      name: "Test User",
    });
    const res = await POST(req as any);

    expect(res.status).toBe(500);
  });
});
