import { NextRequest, NextResponse } from "next/server";
import { createAdminClient } from "@/lib/supabase/admin";
import { isValidLang } from "@/lib/i18n";

export async function GET(
  _request: NextRequest,
  { params }: { params: Promise<{ lang: string; category: string }> },
) {
  try {
    const { lang, category } = await params;

    if (!isValidLang(lang)) {
      return NextResponse.json(
        { error: "지원하지 않는 언어입니다" },
        { status: 400 },
      );
    }

    const supabase = createAdminClient();

    // 카테고리 조회
    const { data: categoryData, error: catError } = await supabase
      .from("procedure_categories")
      .select("id, name_ko, name_en, slug")
      .eq("slug", category)
      .single();

    if (catError || !categoryData) {
      return NextResponse.json(
        { error: "카테고리를 찾을 수 없습니다" },
        { status: 404 },
      );
    }

    // 해당 카테고리의 시술 목록
    const { data: procedures } = await supabase
      .from("procedures")
      .select("id, name, grade, primary_category_id, is_leaf")
      .eq("primary_category_id", categoryData.id)
      .order("grade", { ascending: false })
      .order("name");

    const procedureIds = (procedures ?? []).map((p) => p.id);

    // 번역, 가격 비교, 추천 병원을 병렬로 조회
    const [translationsResult, pricesResult, clinicsResult] = await Promise.all(
      [
        lang !== "ko" && procedureIds.length > 0
          ? supabase
              .from("procedure_intl")
              .select("procedure_id, translated_name, principle, method")
              .eq("language_code", lang)
              .in("procedure_id", procedureIds)
          : Promise.resolve({ data: [] }),
        procedureIds.length > 0
          ? supabase
              .from("price_comparison")
              .select("procedure_id, country, price_usd_min, price_usd_max")
              .in("procedure_id", procedureIds)
          : Promise.resolve({ data: [] }),
        procedureIds.length > 0
          ? supabase
              .from("recommended_clinics")
              .select("procedure_id, clinic_id, rank")
              .in("procedure_id", procedureIds)
              .order("rank")
              .limit(30)
          : Promise.resolve({ data: [] }),
      ],
    );

    // 번역 맵 생성
    const translationMap = new Map<
      number,
      { name: string; description: string }
    >();
    for (const t of translationsResult.data ?? []) {
      translationMap.set(t.procedure_id, {
        name: t.translated_name ?? "",
        description: t.principle ?? "",
      });
    }

    // 가격 맵 생성 (한국 vs 다른 나라)
    const priceMap = new Map<
      number,
      { kr_min: number; kr_max: number; intl_avg: number }
    >();
    for (const p of pricesResult.data ?? []) {
      const existing = priceMap.get(p.procedure_id) ?? {
        kr_min: 0,
        kr_max: 0,
        intl_avg: 0,
      };
      if (p.country === "KR") {
        existing.kr_min = p.price_usd_min ?? 0;
        existing.kr_max = p.price_usd_max ?? 0;
      } else {
        const avg =
          ((p.price_usd_min ?? 0) + (p.price_usd_max ?? p.price_usd_min ?? 0)) /
          2;
        if (avg > 0) {
          existing.intl_avg =
            existing.intl_avg > 0 ? (existing.intl_avg + avg) / 2 : avg;
        }
      }
      priceMap.set(p.procedure_id, existing);
    }

    // 응답 조립
    const result = (procedures ?? []).map((proc) => {
      const translation = translationMap.get(proc.id);
      const prices = priceMap.get(proc.id);
      const discount =
        prices && prices.intl_avg > 0 && prices.kr_max > 0
          ? Math.round(
              ((prices.intl_avg - (prices.kr_min + prices.kr_max) / 2) /
                prices.intl_avg) *
                100,
            )
          : null;

      return {
        id: proc.id,
        name_ko: proc.name,
        name_intl: translation?.name ?? null,
        description_intl: translation?.description ?? null,
        kr_price_min: prices?.kr_min ?? null,
        kr_price_max: prices?.kr_max ?? null,
        intl_avg_price: prices?.intl_avg ?? null,
        discount_pct: discount,
        clinic_count: (clinicsResult.data ?? []).filter(
          (c) => c.procedure_id === proc.id,
        ).length,
      };
    });

    return NextResponse.json({
      category: categoryData,
      procedures: result,
      lang,
    });
  } catch {
    return NextResponse.json({ error: "서버 오류" }, { status: 500 });
  }
}
