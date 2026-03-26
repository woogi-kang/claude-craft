import { describe, it, expect, vi, beforeEach } from "vitest";

// Mock createAdminClient before importing the route
const mockSingle = vi.fn();
const mockInsertSelectSingle = vi.fn();
const mockInsertSelect = vi
  .fn()
  .mockReturnValue({ single: mockInsertSelectSingle });
const mockInsert = vi.fn().mockReturnValue({ select: mockInsertSelect });
const mockSelectEqSingle = vi.fn();
const mockSelectEq = vi.fn().mockReturnValue({ single: mockSelectEqSingle });
const mockSelect = vi.fn().mockReturnValue({ eq: mockSelectEq });
const mockFrom = vi.fn().mockReturnValue({
  select: mockSelect,
  insert: mockInsert,
});

vi.mock("@/lib/supabase/admin", () => ({
  createAdminClient: vi.fn(() => ({ from: mockFrom })),
}));

import { POST } from "@/app/api/audits/route";

function makeRequest(body: unknown) {
  return new Request("http://localhost/api/audits", {
    method: "POST",
    body: JSON.stringify(body),
    headers: { "Content-Type": "application/json" },
  });
}

describe("POST /api/audits", () => {
  beforeEach(() => {
    vi.clearAllMocks();

    // Default: no existing hospital, successful insert
    mockFrom.mockImplementation((table: string) => {
      if (table === "hospitals") {
        return {
          select: vi.fn().mockReturnValue({
            eq: vi.fn().mockReturnValue({
              single: vi.fn().mockResolvedValue({ data: null, error: null }),
            }),
          }),
          insert: vi.fn().mockReturnValue({
            select: vi.fn().mockReturnValue({
              single: vi.fn().mockResolvedValue({
                data: { id: "hospital-1" },
                error: null,
              }),
            }),
          }),
        };
      }
      if (table === "audits") {
        return {
          insert: vi.fn().mockReturnValue({
            select: vi.fn().mockReturnValue({
              single: vi.fn().mockResolvedValue({
                data: {
                  id: "audit-123",
                  status: "pending",
                  created_at: "2026-03-27T00:00:00Z",
                },
                error: null,
              }),
            }),
          }),
        };
      }
      return {
        select: vi.fn().mockReturnThis(),
        insert: vi.fn().mockReturnThis(),
      };
    });
  });

  it("should return 202 with audit ID for a valid URL", async () => {
    const req = makeRequest({ url: "https://example.com" });
    const res = await POST(req as any);
    const data = await res.json();

    expect(res.status).toBe(202);
    expect(data.id).toBe("audit-123");
    expect(data.status).toBe("pending");
  });

  it("should return 400 when URL is missing", async () => {
    const req = makeRequest({});
    const res = await POST(req as any);

    expect(res.status).toBe(400);
  });

  it("should return 400 for an invalid URL", async () => {
    const req = makeRequest({ url: "not-a-url" });
    const res = await POST(req as any);

    expect(res.status).toBe(400);
  });

  it("should return 500 when audit insert fails", async () => {
    mockFrom.mockImplementation((table: string) => {
      if (table === "hospitals") {
        return {
          select: vi.fn().mockReturnValue({
            eq: vi.fn().mockReturnValue({
              single: vi.fn().mockResolvedValue({
                data: { id: "hospital-1" },
                error: null,
              }),
            }),
          }),
        };
      }
      if (table === "audits") {
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

    const req = makeRequest({ url: "https://example.com" });
    const res = await POST(req as any);

    expect(res.status).toBe(500);
  });

  it("should use existing hospital if found", async () => {
    const hospitalInsert = vi.fn();
    mockFrom.mockImplementation((table: string) => {
      if (table === "hospitals") {
        return {
          select: vi.fn().mockReturnValue({
            eq: vi.fn().mockReturnValue({
              single: vi.fn().mockResolvedValue({
                data: { id: "existing-hospital" },
                error: null,
              }),
            }),
          }),
          insert: hospitalInsert,
        };
      }
      if (table === "audits") {
        return {
          insert: vi.fn().mockReturnValue({
            select: vi.fn().mockReturnValue({
              single: vi.fn().mockResolvedValue({
                data: {
                  id: "audit-456",
                  status: "pending",
                  created_at: "2026-03-27",
                },
                error: null,
              }),
            }),
          }),
        };
      }
      return {};
    });

    const req = makeRequest({ url: "https://example.com" });
    const res = await POST(req as any);

    expect(res.status).toBe(202);
    // Hospital insert should NOT be called since existing hospital was found
    expect(hospitalInsert).not.toHaveBeenCalled();
  });
});
