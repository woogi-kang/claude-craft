import { describe, it, expect, vi, beforeEach } from "vitest";

const mockFrom = vi.fn();

vi.mock("@/lib/supabase/admin", () => ({
  createAdminClient: vi.fn(() => ({ from: mockFrom })),
}));

import { POST } from "@/app/api/chat/route";

function makeRequest(body: unknown) {
  return new Request("http://localhost/api/chat", {
    method: "POST",
    body: JSON.stringify(body),
    headers: { "Content-Type": "application/json" },
  });
}

// Helper: create a chain that resolves to given data
function makeChain(data: unknown = [], error: unknown = null) {
  const chain: Record<string, unknown> = {};
  const proxy = new Proxy(chain, {
    get(_target, prop) {
      if (prop === "then") {
        return (resolve: (v: unknown) => void) => resolve({ data, error });
      }
      return vi.fn().mockReturnValue(proxy);
    },
  });
  return proxy;
}

describe("POST /api/chat", () => {
  beforeEach(() => {
    vi.clearAllMocks();
    mockFrom.mockReturnValue(makeChain([]));
  });

  it("should return greeting response for hello message", async () => {
    const req = makeRequest({ message: "안녕하세요" });
    const res = await POST(req as any);
    const data = await res.json();

    expect(res.status).toBe(200);
    expect(data.reply).toContain("MediScope");
    expect(data.suggestions).toBeDefined();
  });

  it("should return greeting response for 'hi'", async () => {
    const req = makeRequest({ message: "hi" });
    const res = await POST(req as any);
    const data = await res.json();

    expect(res.status).toBe(200);
    expect(data.reply).toContain("MediScope");
  });

  it("should return 400 when message is missing", async () => {
    const req = makeRequest({});
    const res = await POST(req as any);

    expect(res.status).toBe(400);
  });

  it("should return 400 when message is empty", async () => {
    const req = makeRequest({ message: "  " });
    const res = await POST(req as any);

    expect(res.status).toBe(400);
  });

  it("should handle procedure keyword and query supabase", async () => {
    // "시술" triggers procedure intent
    mockFrom.mockImplementation((table: string) => {
      if (table === "search_dict") {
        return makeChain([{ procedure_id: 1 }]);
      }
      if (table === "procedures") {
        return makeChain([{ id: 1, name: "보톡스", primary_category_id: 1 }]);
      }
      if (table === "procedure_details") {
        return makeChain({
          procedure_name: "보톡스",
          effect: "주름 개선",
          method: "주사",
          duration_of_procedure: "10분",
          pain_level: 2,
          pain_description: "약간의 따끔함",
          downtime: "없음",
          average_price: "10만원",
        });
      }
      return makeChain([]);
    });

    const req = makeRequest({ message: "보톡스 시술 알려줘" });
    const res = await POST(req as any);
    const data = await res.json();

    expect(res.status).toBe(200);
    expect(data.reply).toBeDefined();
  });

  it("should handle price keyword", async () => {
    mockFrom.mockImplementation((table: string) => {
      if (table === "beauty_std_procedures") {
        return makeChain([{ id: 1, name: "보톡스" }]);
      }
      if (table === "price_comparison") {
        return makeChain([
          {
            country: "KR",
            currency: "KRW",
            price_min: 50000,
            price_max: 150000,
          },
        ]);
      }
      if (table === "intl_prices") {
        return makeChain([]);
      }
      return makeChain([]);
    });

    const req = makeRequest({ message: "보톡스 가격 알려줘" });
    const res = await POST(req as any);
    const data = await res.json();

    expect(res.status).toBe(200);
    expect(data.reply).toBeDefined();
  });

  it("should handle clinic/hospital keyword", async () => {
    mockFrom.mockImplementation((table: string) => {
      if (table === "recommended_clinics") {
        return makeChain([]);
      }
      if (table === "beauty_clinics") {
        return makeChain([
          {
            id: 1,
            name: "Test Clinic",
            sido: "서울",
            sggu: "강남",
            website: null,
            is_foreign_patient_facilitator: true,
          },
        ]);
      }
      return makeChain([]);
    });

    const req = makeRequest({ message: "강남 병원 추천해줘" });
    const res = await POST(req as any);
    const data = await res.json();

    expect(res.status).toBe(200);
    expect(data.reply).toBeDefined();
  });

  it("should handle unknown messages with fallback", async () => {
    // Unknown message with no procedure match
    mockFrom.mockImplementation((table: string) => {
      if (table === "search_dict") return makeChain([]);
      if (table === "procedures") return makeChain([]);
      if (table === "procedure_categories") return makeChain([]);
      return makeChain([]);
    });

    const req = makeRequest({ message: "abcxyz123" });
    const res = await POST(req as any);
    const data = await res.json();

    expect(res.status).toBe(200);
    expect(data.reply).toBeDefined();
    expect(data.suggestions).toBeDefined();
  });
});
