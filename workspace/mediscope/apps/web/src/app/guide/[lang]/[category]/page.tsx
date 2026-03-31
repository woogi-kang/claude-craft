import { Metadata } from "next";
import Link from "next/link";
import { ArrowLeft, ArrowRight, TrendingDown, Hospital } from "lucide-react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { createAdminClient } from "@/lib/supabase/admin";
import {
  SUPPORTED_LANGS,
  LANG_LABELS,
  LANG_LOCALE,
  GUIDE_UI,
  isValidLang,
  type Lang,
} from "@/lib/i18n";
import { BEAUTY_CATEGORIES } from "@/lib/types/beauty";

interface PageParams {
  lang: string;
  category: string;
}

interface ProcedureWithPrice {
  id: number;
  name: string;
  name_intl: string | null;
  kr_price_min: number | null;
  kr_price_max: number | null;
  intl_avg_price: number | null;
  discount_pct: number | null;
  clinic_count: number;
}

interface CategoryInfo {
  id: number;
  name_ko: string;
  name_en: string;
  slug: string;
}

async function getCategoryData(
  lang: Lang,
  categorySlug: string,
): Promise<{
  category: CategoryInfo | null;
  procedures: ProcedureWithPrice[];
  allCategories: CategoryInfo[];
}> {
  try {
    const supabase = createAdminClient();

    const [catResult, allCatResult] = await Promise.all([
      supabase
        .from("procedure_categories")
        .select("id, name_ko, name_en, slug")
        .eq("slug", categorySlug)
        .single(),
      supabase
        .from("procedure_categories")
        .select("id, name_ko, name_en, slug")
        .order("id"),
    ]);

    if (catResult.error || !catResult.data) {
      return {
        category: null,
        procedures: [],
        allCategories: allCatResult.data ?? [],
      };
    }

    const category = catResult.data;

    const { data: procedures } = await supabase
      .from("procedures")
      .select("id, name, grade, primary_category_id")
      .eq("primary_category_id", category.id)
      .order("grade", { ascending: false })
      .order("name");

    const procedureIds = (procedures ?? []).map((p) => p.id);

    const [translationsResult, pricesResult, clinicsResult] = await Promise.all(
      [
        lang !== "ko" && procedureIds.length > 0
          ? supabase
              .from("procedure_intl")
              .select("procedure_id, translated_name")
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
              .select("procedure_id, clinic_id")
              .in("procedure_id", procedureIds)
          : Promise.resolve({ data: [] }),
      ],
    );

    const translationMap = new Map<number, string>();
    for (const t of translationsResult.data ?? []) {
      if (t.translated_name)
        translationMap.set(t.procedure_id, t.translated_name);
    }

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

    const clinicCountMap = new Map<number, number>();
    for (const c of clinicsResult.data ?? []) {
      clinicCountMap.set(
        c.procedure_id,
        (clinicCountMap.get(c.procedure_id) ?? 0) + 1,
      );
    }

    const result: ProcedureWithPrice[] = (procedures ?? []).map((proc) => {
      const prices = priceMap.get(proc.id);
      const krAvg = prices ? (prices.kr_min + prices.kr_max) / 2 : 0;
      const discount =
        prices && prices.intl_avg > 0 && krAvg > 0
          ? Math.round(((prices.intl_avg - krAvg) / prices.intl_avg) * 100)
          : null;

      return {
        id: proc.id,
        name: proc.name,
        name_intl: translationMap.get(proc.id) ?? null,
        kr_price_min: prices?.kr_min ?? null,
        kr_price_max: prices?.kr_max ?? null,
        intl_avg_price: prices?.intl_avg ?? null,
        discount_pct: discount,
        clinic_count: clinicCountMap.get(proc.id) ?? 0,
      };
    });

    return {
      category,
      procedures: result,
      allCategories: allCatResult.data ?? [],
    };
  } catch {
    return { category: null, procedures: [], allCategories: [] };
  }
}

export async function generateMetadata({
  params,
}: {
  params: Promise<PageParams>;
}): Promise<Metadata> {
  const { lang, category } = await params;
  if (!isValidLang(lang)) return {};

  const supabase = createAdminClient();
  const { data: cat } = await supabase
    .from("procedure_categories")
    .select("name_ko, name_en, slug")
    .eq("slug", category)
    .single();

  if (!cat) return {};

  const catName = lang === "ko" ? cat.name_ko : cat.name_en;
  const ui = GUIDE_UI[lang];

  const title = `${catName} - ${ui.title} | CheckYourHospital`;
  const description =
    lang === "ko"
      ? `${cat.name_ko} 시술 가이드 - 한국 의료관광 가격 비교, 추천 병원 정보`
      : `${cat.name_en} procedure guide - Korea medical tourism price comparison`;

  const alternates: Record<string, string> = {};
  for (const l of SUPPORTED_LANGS) {
    alternates[l] = `/guide/${l}/${category}`;
  }

  return {
    title,
    description,
    openGraph: {
      title,
      description,
      type: "website",
      locale: LANG_LOCALE[lang],
    },
    alternates: {
      languages: alternates,
    },
  };
}

function formatPrice(min: number | null, max: number | null): string {
  if (min == null && max == null) return "-";
  if (min != null && max != null && min !== max) {
    return `$${min.toLocaleString()} - $${max.toLocaleString()}`;
  }
  return `$${(min ?? max ?? 0).toLocaleString()}`;
}

export default async function GuideCategoryPage({
  params,
}: {
  params: Promise<PageParams>;
}) {
  const { lang: langParam, category: categorySlug } = await params;
  const lang: Lang = isValidLang(langParam) ? langParam : "ko";
  const ui = GUIDE_UI[lang];

  const { category, procedures, allCategories } = await getCategoryData(
    lang,
    categorySlug,
  );

  if (!category) {
    return (
      <div className="mx-auto max-w-4xl px-4 py-8">
        <Link
          href="/guide"
          className="mb-6 inline-flex items-center gap-1 text-sm text-muted-foreground hover:text-foreground"
        >
          <ArrowLeft className="h-4 w-4" />
          {ui.backToGuide}
        </Link>
        <Card>
          <CardContent className="py-10 text-center text-muted-foreground">
            카테고리를 찾을 수 없습니다.
          </CardContent>
        </Card>
      </div>
    );
  }

  const catInfo = BEAUTY_CATEGORIES[category.id];
  const catName = lang === "ko" ? category.name_ko : category.name_en;
  const avgDiscount =
    procedures.filter((p) => p.discount_pct != null && p.discount_pct > 0)
      .length > 0
      ? Math.round(
          procedures
            .filter((p) => p.discount_pct != null && p.discount_pct > 0)
            .reduce((sum, p) => sum + (p.discount_pct ?? 0), 0) /
            procedures.filter(
              (p) => p.discount_pct != null && p.discount_pct > 0,
            ).length,
        )
      : null;

  const jsonLd = {
    "@context": "https://schema.org",
    "@type": "MedicalWebPage",
    name: `${catName} - ${ui.title}`,
    description: `${catName} procedure guide for Korea medical tourism`,
    url: `https://checkyourhospital.kr/guide/${lang}/${categorySlug}`,
    inLanguage: lang,
    about: {
      "@type": "MedicalSpecialty",
      name: category.name_en,
    },
    mainEntity: {
      "@type": "ItemList",
      numberOfItems: procedures.length,
      itemListElement: procedures.slice(0, 10).map((proc, idx) => ({
        "@type": "ListItem",
        position: idx + 1,
        item: {
          "@type": "MedicalProcedure",
          name: proc.name_intl ?? proc.name,
          url: `https://checkyourhospital.kr/guide/${lang}/procedure/${proc.id}`,
        },
      })),
    },
  };

  return (
    <div className="min-h-screen bg-gradient-to-b from-blue-50 to-white">
      <div className="mx-auto max-w-6xl px-4 py-8">
        <Link
          href="/guide"
          className="mb-6 inline-flex items-center gap-1 text-sm text-muted-foreground hover:text-foreground"
        >
          <ArrowLeft className="h-4 w-4" />
          {ui.backToGuide}
        </Link>

        {/* Category Header */}
        <div className="mb-8">
          <div className="flex items-center gap-3">
            <span className="text-3xl">{catInfo?.icon ?? "💊"}</span>
            <div>
              <h1 className="text-3xl font-bold tracking-tight">{catName}</h1>
              <p className="mt-1 text-muted-foreground">
                {procedures.length}
                {ui.procedureCount}
                {avgDiscount != null && (
                  <span className="ml-3">
                    {ui.avgDiscount}: -{avgDiscount}%
                  </span>
                )}
              </p>
            </div>
          </div>

          {/* Language Switcher */}
          <div className="mt-4 flex gap-2">
            {SUPPORTED_LANGS.map((l) => (
              <Link
                key={l}
                href={`/guide/${l}/${categorySlug}`}
                className={`rounded-full px-3 py-1 text-sm transition-colors ${
                  l === lang
                    ? "bg-blue-600 text-white"
                    : "bg-gray-100 text-gray-600 hover:bg-gray-200"
                }`}
              >
                {LANG_LABELS[l]}
              </Link>
            ))}
          </div>
        </div>

        {/* Category Navigation */}
        <div className="mb-8 flex gap-2 overflow-x-auto pb-2">
          {allCategories.map((cat) => (
            <Link
              key={cat.id}
              href={`/guide/${lang}/${cat.slug}`}
              className={`whitespace-nowrap rounded-lg border px-3 py-1.5 text-sm transition-colors ${
                cat.slug === categorySlug
                  ? "border-blue-500 bg-blue-50 text-blue-700"
                  : "border-gray-200 hover:border-blue-300"
              }`}
            >
              {lang === "ko" ? cat.name_ko : cat.name_en}
            </Link>
          ))}
        </div>

        {/* Procedure List */}
        <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
          {procedures.map((proc) => (
            <Link key={proc.id} href={`/guide/${lang}/procedure/${proc.id}`}>
              <Card className="h-full transition-all hover:shadow-md hover:-translate-y-0.5">
                <CardHeader className="pb-2">
                  <CardTitle className="text-base">
                    {proc.name_intl ?? proc.name}
                  </CardTitle>
                  {proc.name_intl && (
                    <p className="text-xs text-muted-foreground">{proc.name}</p>
                  )}
                </CardHeader>
                <CardContent>
                  <div className="flex flex-wrap items-center gap-2">
                    {proc.kr_price_min != null && (
                      <Badge variant="secondary" className="text-xs">
                        {formatPrice(proc.kr_price_min, proc.kr_price_max)}
                      </Badge>
                    )}
                    {proc.discount_pct != null && proc.discount_pct > 0 && (
                      <Badge className="bg-green-100 text-green-700 text-xs">
                        <TrendingDown className="mr-1 h-3 w-3" />-
                        {proc.discount_pct}%
                      </Badge>
                    )}
                    {proc.clinic_count > 0 && (
                      <Badge variant="outline" className="text-xs">
                        <Hospital className="mr-1 h-3 w-3" />
                        {proc.clinic_count}
                      </Badge>
                    )}
                  </div>
                  <div className="mt-3 flex items-center text-sm text-blue-600">
                    {ui.viewAll}
                    <ArrowRight className="ml-1 h-3 w-3" />
                  </div>
                </CardContent>
              </Card>
            </Link>
          ))}
        </div>

        {procedures.length === 0 && (
          <Card>
            <CardContent className="py-10 text-center text-muted-foreground">
              이 카테고리에 등록된 시술이 없습니다.
            </CardContent>
          </Card>
        )}

        <script
          type="application/ld+json"
          dangerouslySetInnerHTML={{ __html: JSON.stringify(jsonLd) }}
        />
      </div>
    </div>
  );
}
