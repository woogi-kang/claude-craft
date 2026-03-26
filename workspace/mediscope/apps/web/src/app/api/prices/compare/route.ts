import { NextResponse } from "next/server";
import { createAdminClient } from "@/lib/supabase/admin";

export async function GET() {
  try {
    const supabase = createAdminClient();

    // Fetch price_comparison with procedure name
    const { data: prices, error } = await supabase
      .from("price_comparison")
      .select(
        "id, therapy_id, price_min, price_max, currency, country, condition_note",
      )
      .order("therapy_id");

    if (error) {
      return NextResponse.json({ error: error.message }, { status: 500 });
    }

    // Fetch procedure names
    const therapyIds = [...new Set(prices?.map((p) => p.therapy_id) ?? [])];
    const { data: procedures } = await supabase
      .from("beauty_std_procedures")
      .select("id, name")
      .in("id", therapyIds);

    const procMap = new Map(procedures?.map((p) => [p.id, p.name]) ?? []);

    // Also fetch intl_prices
    const { data: intlPrices } = await supabase
      .from("intl_prices")
      .select("top_procedure_id, country_code, currency, price, price_unit");

    // Group by procedure
    const grouped = new Map<
      number,
      {
        name: string;
        prices: Array<{
          country: string;
          currency: string;
          price_min: number | null;
          price_max: number | null;
        }>;
      }
    >();

    for (const p of prices ?? []) {
      if (!grouped.has(p.therapy_id)) {
        grouped.set(p.therapy_id, {
          name: procMap.get(p.therapy_id) ?? `시술 ${p.therapy_id}`,
          prices: [],
        });
      }
      grouped.get(p.therapy_id)!.prices.push({
        country: p.country,
        currency: p.currency,
        price_min: p.price_min,
        price_max: p.price_max,
      });
    }

    const results = [...grouped.entries()].map(([id, data]) => ({
      procedure_id: id,
      procedure_name: data.name,
      prices: data.prices,
    }));

    return NextResponse.json(results);
  } catch {
    return NextResponse.json({ error: "서버 오류" }, { status: 500 });
  }
}
