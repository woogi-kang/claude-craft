import { NextRequest, NextResponse } from "next/server";
import { createAdminClient } from "@/lib/supabase/admin";
import type { PriceCompareResponse, CountryPrice } from "@/lib/types/beauty";

export async function GET(request: NextRequest) {
  try {
    const supabase = createAdminClient();
    const procedureId = request.nextUrl.searchParams.get("procedure_id");

    // Fetch price_comparison data
    let query = supabase.from("price_comparison").select("*");
    if (procedureId) {
      query = query.eq("procedure_id", procedureId);
    }
    const { data: comparisons, error: compError } =
      await query.order("procedure_name_ko");

    if (compError) {
      return NextResponse.json(
        { error: "가격 데이터를 불러올 수 없습니다" },
        { status: 500 },
      );
    }

    // Also fetch intl_prices for richer data
    const procedureIds = [
      ...new Set(comparisons?.map((c) => c.procedure_id) ?? []),
    ];
    const { data: intlPrices } = procedureIds.length
      ? await supabase
          .from("intl_prices")
          .select("*")
          .in("std_procedure_id", procedureIds)
      : { data: [] };

    // Build response
    const intlByProcedure = new Map<string, typeof intlPrices>();
    for (const ip of intlPrices ?? []) {
      const existing = intlByProcedure.get(ip.std_procedure_id) ?? [];
      existing.push(ip);
      intlByProcedure.set(ip.std_procedure_id, existing);
    }

    const results: PriceCompareResponse[] = (comparisons ?? []).map((comp) => {
      const prices: CountryPrice[] = [];

      // Korea price (always present)
      prices.push({
        country: "KR",
        currency: "KRW",
        price_min: comp.korea_min_krw,
        price_max: comp.korea_max_krw,
        price_usd_min: comp.korea_min_usd,
        price_usd_max: comp.korea_max_usd,
      });

      // Japan price
      if (comp.japan_min_jpy != null) {
        prices.push({
          country: "JP",
          currency: "JPY",
          price_min: comp.japan_min_jpy,
          price_max: comp.japan_max_jpy,
          price_usd_min: comp.japan_min_usd,
          price_usd_max: comp.japan_max_usd,
        });
      }

      // China price
      if (comp.china_min_cny != null) {
        prices.push({
          country: "CN",
          currency: "CNY",
          price_min: comp.china_min_cny,
          price_max: comp.china_max_cny,
          price_usd_min: comp.china_min_usd,
          price_usd_max: comp.china_max_usd,
        });
      }

      // Add additional intl prices if available
      const extras = intlByProcedure.get(comp.procedure_id) ?? [];
      for (const ip of extras) {
        if (!prices.some((p) => p.country === ip.country_code)) {
          prices.push({
            country: ip.country_code,
            currency: ip.currency,
            price_min: ip.price_min,
            price_max: ip.price_max,
            price_usd_min: ip.price_usd_min ?? 0,
            price_usd_max: ip.price_usd_max ?? 0,
          });
        }
      }

      return {
        procedure_name: comp.procedure_name_ko,
        procedure_name_en: comp.procedure_name_en,
        prices,
        savings_vs_japan_pct: comp.savings_vs_japan_pct,
        savings_vs_china_pct: comp.savings_vs_china_pct,
      };
    });

    return NextResponse.json(results);
  } catch {
    return NextResponse.json(
      { error: "서버 오류가 발생했습니다" },
      { status: 500 },
    );
  }
}
