import { describe, it, expect, vi, beforeEach } from "vitest";

vi.mock("@/lib/supabase/admin", () => ({
  createAdminClient: vi.fn(() => ({})),
}));

import { POST, GET } from "@/app/api/subscriptions/route";
import { createNextRequest } from "../helpers";

function makePostRequest(body: unknown) {
  return createNextRequest("http://localhost/api/subscriptions", {
    method: "POST",
    body: JSON.stringify(body),
    headers: { "Content-Type": "application/json" },
  });
}

function makeGetRequest(email?: string) {
  const url = email
    ? `http://localhost/api/subscriptions?email=${encodeURIComponent(email)}`
    : "http://localhost/api/subscriptions";
  return createNextRequest(url, { method: "GET" });
}

describe("POST /api/subscriptions", () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  it("should return 201 when worker returns success", async () => {
    vi.stubGlobal(
      "fetch",
      vi.fn().mockResolvedValue({
        ok: true,
        status: 201,
        json: vi.fn().mockResolvedValue({ id: "sub-1" }),
      }),
    );

    const req = makePostRequest({
      audit_id: "550e8400-e29b-41d4-a716-446655440000",
      email: "test@example.com",
      frequency: "weekly",
    });
    const res = await POST(req as any);
    const data = await res.json();

    expect(res.status).toBe(201);
    expect(data.id).toBe("sub-1");
  });

  it("should return 400 for missing email", async () => {
    const req = makePostRequest({
      audit_id: "550e8400-e29b-41d4-a716-446655440000",
      frequency: "weekly",
    });
    const res = await POST(req as any);

    expect(res.status).toBe(400);
  });

  it("should return 400 for invalid frequency", async () => {
    const req = makePostRequest({
      audit_id: "550e8400-e29b-41d4-a716-446655440000",
      email: "test@example.com",
      frequency: "daily",
    });
    const res = await POST(req as any);

    expect(res.status).toBe(400);
  });

  it("should forward worker error status", async () => {
    vi.stubGlobal(
      "fetch",
      vi.fn().mockResolvedValue({
        ok: false,
        status: 422,
        json: vi.fn().mockResolvedValue({ error: "duplicate" }),
      }),
    );

    const req = makePostRequest({
      audit_id: "550e8400-e29b-41d4-a716-446655440000",
      email: "test@example.com",
      frequency: "monthly",
    });
    const res = await POST(req as any);

    expect(res.status).toBe(422);
  });
});

describe("GET /api/subscriptions", () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  it("should return subscriptions for given email", async () => {
    vi.stubGlobal(
      "fetch",
      vi.fn().mockResolvedValue({
        ok: true,
        status: 200,
        json: vi.fn().mockResolvedValue([{ id: "sub-1", frequency: "weekly" }]),
      }),
    );

    const req = makeGetRequest("test@example.com");
    const res = await GET(req as any);
    const data = await res.json();

    expect(res.status).toBe(200);
    expect(Array.isArray(data)).toBe(true);
  });

  it("should return 400 when email is missing", async () => {
    const req = makeGetRequest();
    const res = await GET(req as any);

    expect(res.status).toBe(400);
  });

  it("should forward worker error", async () => {
    vi.stubGlobal(
      "fetch",
      vi.fn().mockResolvedValue({
        ok: false,
        status: 500,
        json: vi.fn().mockResolvedValue({}),
      }),
    );

    const req = makeGetRequest("test@example.com");
    const res = await GET(req as any);

    expect(res.status).toBe(500);
  });
});
