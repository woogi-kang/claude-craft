import { describe, it, expect, vi, beforeEach } from "vitest";

const mockFrom = vi.fn();

vi.mock("@/lib/supabase/admin", () => ({
  createAdminClient: vi.fn(() => ({ from: mockFrom })),
}));

import { GET } from "@/app/api/guide/[lang]/[category]/route";

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

function makeRequest(lang: string, category: string) {
  return new Request(`http://localhost/api/guide/${lang}/${category}`, {
    method: "GET",
  });
}

describe("GET /api/guide/[lang]/[category]", () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  it("should return 400 for unsupported language", async () => {
    const req = makeRequest("fr", "skincare");
    const res = await GET(req as any, {
      params: Promise.resolve({ lang: "fr", category: "skincare" }),
    });

    expect(res.status).toBe(400);
  });

  it("should return 404 for non-existent category", async () => {
    mockFrom.mockImplementation((table: string) => {
      if (table === "procedure_categories") {
        return makeChain(null, { message: "not found" });
      }
      return makeChain([]);
    });

    const req = makeRequest("ko", "nonexistent");
    const res = await GET(req as any, {
      params: Promise.resolve({ lang: "ko", category: "nonexistent" }),
    });

    expect(res.status).toBe(404);
  });

  it("should return procedures for valid lang and category", async () => {
    mockFrom.mockImplementation((table: string) => {
      if (table === "procedure_categories") {
        return makeChain({
          id: 1,
          name_ko: "피부관리",
          name_en: "Skin Care",
          slug: "skincare",
        });
      }
      if (table === "procedures") {
        return makeChain([
          {
            id: 1,
            name: "보톡스",
            grade: 5,
            primary_category_id: 1,
            is_leaf: true,
          },
        ]);
      }
      if (table === "procedure_intl") {
        return makeChain([]);
      }
      if (table === "price_comparison") {
        return makeChain([]);
      }
      if (table === "recommended_clinics") {
        return makeChain([]);
      }
      return makeChain([]);
    });

    const req = makeRequest("ko", "skincare");
    const res = await GET(req as any, {
      params: Promise.resolve({ lang: "ko", category: "skincare" }),
    });
    const data = await res.json();

    expect(res.status).toBe(200);
    expect(data.category).toBeDefined();
    expect(data.procedures).toBeDefined();
    expect(data.lang).toBe("ko");
  });

  it("should fetch translations for non-ko languages", async () => {
    mockFrom.mockImplementation((table: string) => {
      if (table === "procedure_categories") {
        return makeChain({
          id: 1,
          name_ko: "피부관리",
          name_en: "Skin Care",
          slug: "skincare",
        });
      }
      if (table === "procedures") {
        return makeChain([
          {
            id: 1,
            name: "보톡스",
            grade: 5,
            primary_category_id: 1,
            is_leaf: true,
          },
        ]);
      }
      if (table === "procedure_intl") {
        return makeChain([
          {
            procedure_id: 1,
            translated_name: "Botox",
            principle: "Botulinum toxin",
            method: "Injection",
          },
        ]);
      }
      if (table === "price_comparison") {
        return makeChain([]);
      }
      if (table === "recommended_clinics") {
        return makeChain([]);
      }
      return makeChain([]);
    });

    const req = makeRequest("en", "skincare");
    const res = await GET(req as any, {
      params: Promise.resolve({ lang: "en", category: "skincare" }),
    });
    const data = await res.json();

    expect(res.status).toBe(200);
    expect(data.lang).toBe("en");
  });
});
