import { Metadata } from "next";
import Link from "next/link";
import {
  ArrowLeft,
  Clock,
  Zap,
  AlertTriangle,
  Scissors,
  Hospital,
  TrendingDown,
} from "lucide-react";
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
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
import {
  BEAUTY_CATEGORIES,
  COUNTRY_LABELS,
  type ProcedureDetail,
  type ProcedureTranslation,
  type CountryPrice,
} from "@/lib/types/beauty";

interface PageParams {
  lang: string;
  id: string;
}

interface ProcedureData {
  id: number;
  name: string;
  grade: number;
  primary_category_id: number;
}

interface RelatedProcedure {
  id: number;
  name: string;
  name_intl: string | null;
}

interface ClinicInfo {
  clinic_id: number;
  rank: number;
}

async function getProcedureData(
  lang: Lang,
  procedureId: string,
): Promise<{
  procedure: ProcedureData | null;
  details: ProcedureDetail | null;
  translation: ProcedureTranslation | null;
  prices: CountryPrice[];
  related: RelatedProcedure[];
  clinics: ClinicInfo[];
  categorySlug: string;
}> {
  try {
    const supabase = createAdminClient();

    const { data: procedure, error } = await supabase
      .from("procedures")
      .select("id, name, grade, primary_category_id")
      .eq("id", procedureId)
      .single();

    if (error || !procedure) {
      return {
        procedure: null,
        details: null,
        translation: null,
        prices: [],
        related: [],
        clinics: [],
        categorySlug: "",
      };
    }

    const [
      detailsResult,
      translationResult,
      pricesResult,
      clinicsResult,
      relatedResult,
      categoryResult,
    ] = await Promise.all([
      supabase
        .from("procedure_details")
        .select("*")
        .eq("procedure_id", procedureId)
        .single(),
      lang !== "ko"
        ? supabase
            .from("procedure_intl")
            .select("*")
            .eq("procedure_id", procedureId)
            .eq("language_code", lang)
            .single()
        : Promise.resolve({ data: null }),
      supabase
        .from("price_comparison")
        .select("country, currency, price_usd_min, price_usd_max")
        .eq("procedure_id", procedureId),
      supabase
        .from("recommended_clinics")
        .select("clinic_id, rank")
        .eq("procedure_id", procedureId)
        .order("rank")
        .limit(5),
      supabase
        .from("procedures")
        .select("id, name")
        .eq("primary_category_id", procedure.primary_category_id)
        .neq("id", procedureId)
        .order("grade", { ascending: false })
        .limit(6),
      supabase
        .from("procedure_categories")
        .select("slug")
        .eq("id", procedure.primary_category_id)
        .single(),
    ]);

    // 관련 시술 번역
    const relatedIds = (relatedResult.data ?? []).map((r) => r.id);
    const relatedTranslations = new Map<number, string>();
    if (lang !== "ko" && relatedIds.length > 0) {
      const { data: relTranslations } = await supabase
        .from("procedure_intl")
        .select("procedure_id, translated_name")
        .eq("language_code", lang)
        .in("procedure_id", relatedIds);
      for (const t of relTranslations ?? []) {
        if (t.translated_name)
          relatedTranslations.set(t.procedure_id, t.translated_name);
      }
    }

    return {
      procedure,
      details: detailsResult.data,
      translation: translationResult.data as ProcedureTranslation | null,
      prices: (pricesResult.data ?? []).map((p) => ({
        country: p.country,
        currency: p.currency,
        price_min: p.price_usd_min,
        price_max: p.price_usd_max,
      })),
      related: (relatedResult.data ?? []).map((r) => ({
        id: r.id,
        name: r.name,
        name_intl: relatedTranslations.get(r.id) ?? null,
      })),
      clinics: clinicsResult.data ?? [],
      categorySlug: categoryResult.data?.slug ?? "",
    };
  } catch {
    return {
      procedure: null,
      details: null,
      translation: null,
      prices: [],
      related: [],
      clinics: [],
      categorySlug: "",
    };
  }
}

export async function generateMetadata({
  params,
}: {
  params: Promise<PageParams>;
}): Promise<Metadata> {
  const { lang, id } = await params;
  if (!isValidLang(lang)) return {};

  const supabase = createAdminClient();

  const [procResult, translationResult] = await Promise.all([
    supabase.from("procedures").select("name").eq("id", id).single(),
    lang !== "ko"
      ? supabase
          .from("procedure_intl")
          .select("translated_name")
          .eq("procedure_id", id)
          .eq("language_code", lang)
          .single()
      : Promise.resolve({ data: null }),
  ]);

  if (!procResult.data) return {};

  const name = translationResult.data?.translated_name ?? procResult.data.name;
  const ui = GUIDE_UI[lang];
  const title = `${name} - ${ui.title} | MediScope`;
  const description =
    lang === "ko"
      ? `${name} 시술 정보 - 가격 비교, 회복 기간, 추천 병원`
      : `${name} - Korea medical tourism procedure guide with price comparison`;

  const alternates: Record<string, string> = {};
  for (const l of SUPPORTED_LANGS) {
    alternates[l] = `/guide/${l}/procedure/${id}`;
  }

  return {
    title,
    description,
    openGraph: {
      title,
      description,
      type: "article",
      locale: LANG_LOCALE[lang],
    },
    alternates: {
      languages: alternates,
    },
  };
}

function formatUsd(min: number | null, max: number | null): string {
  if (min == null && max == null) return "-";
  if (min != null && max != null && min !== max) {
    return `$${min.toLocaleString()} - $${max.toLocaleString()}`;
  }
  return `$${(min ?? max ?? 0).toLocaleString()}`;
}

function InfoItem({
  icon,
  label,
  value,
}: {
  icon: React.ReactNode;
  label: string;
  value: string | number | null | undefined;
}) {
  if (value == null) return null;
  return (
    <div className="flex items-start gap-3 rounded-lg border p-3">
      <div className="mt-0.5 text-muted-foreground">{icon}</div>
      <div>
        <p className="text-xs font-medium text-muted-foreground">{label}</p>
        <p className="text-sm">{value}</p>
      </div>
    </div>
  );
}

export default async function GuideProcedureDetailPage({
  params,
}: {
  params: Promise<PageParams>;
}) {
  const { lang: langParam, id } = await params;
  const lang: Lang = isValidLang(langParam) ? langParam : "ko";
  const ui = GUIDE_UI[lang];

  const {
    procedure,
    details,
    translation,
    prices,
    related,
    clinics,
    categorySlug,
  } = await getProcedureData(lang, id);

  if (!procedure) {
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
            시술 정보를 찾을 수 없습니다.
          </CardContent>
        </Card>
      </div>
    );
  }

  const displayName = translation?.translated_name ?? procedure.name;
  const catInfo = BEAUTY_CATEGORIES[procedure.primary_category_id];

  // 한국 가격 추출
  const krPrice = prices.find((p) => p.country === "KR");
  const intlPrices = prices.filter((p) => p.country !== "KR");
  const intlAvg =
    intlPrices.length > 0
      ? Math.round(
          intlPrices.reduce(
            (sum, p) =>
              sum +
              ((p.price_min ?? 0) + (p.price_max ?? p.price_min ?? 0)) / 2,
            0,
          ) / intlPrices.length,
        )
      : null;
  const krAvg =
    krPrice && krPrice.price_min != null
      ? Math.round(
          ((krPrice.price_min ?? 0) +
            (krPrice.price_max ?? krPrice.price_min ?? 0)) /
            2,
        )
      : null;
  const savingsPct =
    intlAvg && krAvg && intlAvg > 0
      ? Math.round(((intlAvg - krAvg) / intlAvg) * 100)
      : null;

  // 시술 설명: 번역이 있으면 번역, 없으면 한국어
  const description =
    lang !== "ko" && translation?.principle
      ? translation.principle
      : (details?.principle ?? null);

  const jsonLd = {
    "@context": "https://schema.org",
    "@type": "MedicalWebPage",
    name: displayName,
    description: description?.slice(0, 200) ?? `${displayName} procedure guide`,
    url: `https://mediscope.kr/guide/${lang}/procedure/${id}`,
    inLanguage: lang,
    about: {
      "@type": "MedicalProcedure",
      name: displayName,
      procedureType: catInfo?.name_en ?? "Cosmetic Procedure",
    },
    ...(krAvg
      ? {
          offers: {
            "@type": "AggregateOffer",
            priceCurrency: "USD",
            lowPrice: krPrice?.price_min ?? krAvg,
            highPrice: krPrice?.price_max ?? krAvg,
            offerCount: clinics.length || 1,
          },
        }
      : {}),
  };

  return (
    <div className="min-h-screen bg-gradient-to-b from-blue-50 to-white">
      <div className="mx-auto max-w-4xl px-4 py-8">
        <Link
          href={categorySlug ? `/guide/${lang}/${categorySlug}` : "/guide"}
          className="mb-6 inline-flex items-center gap-1 text-sm text-muted-foreground hover:text-foreground"
        >
          <ArrowLeft className="h-4 w-4" />
          {ui.backToGuide}
        </Link>

        {/* Header */}
        <div className="mb-6">
          <div className="flex items-center gap-3">
            <h1 className="text-3xl font-bold tracking-tight">{displayName}</h1>
            {catInfo && (
              <Badge variant="secondary">
                {catInfo.icon} {lang === "ko" ? catInfo.name : catInfo.name_en}
              </Badge>
            )}
          </div>
          {translation?.translated_name && (
            <p className="mt-1 text-lg text-muted-foreground">
              {procedure.name}
            </p>
          )}

          {/* Language Switcher */}
          <div className="mt-4 flex gap-2">
            {SUPPORTED_LANGS.map((l) => (
              <Link
                key={l}
                href={`/guide/${l}/procedure/${id}`}
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

        {/* Quick Info */}
        {details && (
          <div className="mb-6 grid gap-3 sm:grid-cols-2">
            <InfoItem
              icon={<Scissors className="h-4 w-4" />}
              label={lang === "ko" ? "시술 시간" : "Duration"}
              value={details.duration_of_procedure ?? details.duration}
            />
            <InfoItem
              icon={<Zap className="h-4 w-4" />}
              label={lang === "ko" ? "통증 레벨" : "Pain Level"}
              value={details.pain_level}
            />
            <InfoItem
              icon={<Clock className="h-4 w-4" />}
              label={ui.recoveryDays}
              value={
                lang !== "ko" && translation?.downtime
                  ? translation.downtime
                  : details.downtime
              }
            />
            <InfoItem
              icon={<Clock className="h-4 w-4" />}
              label={lang === "ko" ? "권장 주기" : "Recommended Cycle"}
              value={details.recommended_cycle}
            />
          </div>
        )}

        {/* Price Savings Summary */}
        {savingsPct != null && savingsPct > 0 && (
          <Card className="mb-6 border-green-200 bg-green-50">
            <CardContent className="flex items-center gap-4 py-4">
              <TrendingDown className="h-8 w-8 text-green-600" />
              <div>
                <p className="text-lg font-bold text-green-700">
                  {ui.savings}: {savingsPct}%
                </p>
                <p className="text-sm text-green-600">
                  {ui.koreaPrice}:{" "}
                  {formatUsd(
                    krPrice?.price_min ?? null,
                    krPrice?.price_max ?? null,
                  )}
                </p>
              </div>
            </CardContent>
          </Card>
        )}

        {/* Description */}
        {description && (
          <Card className="mb-6">
            <CardHeader>
              <CardTitle className="text-lg">
                {lang === "ko" ? "원리" : "Principle"}
              </CardTitle>
            </CardHeader>
            <CardContent>
              <p className="whitespace-pre-line text-sm text-muted-foreground">
                {description}
              </p>
            </CardContent>
          </Card>
        )}

        {/* Additional Details */}
        {details && (
          <Card className="mb-6">
            <CardHeader>
              <CardTitle className="text-lg">
                {lang === "ko" ? "상세 정보" : "Details"}
              </CardTitle>
            </CardHeader>
            <CardContent className="space-y-4">
              {details.effect && (
                <div>
                  <h3 className="mb-1 font-semibold">
                    {lang === "ko" ? "효과" : "Effect"}
                  </h3>
                  <p className="whitespace-pre-line text-sm text-muted-foreground">
                    {details.effect}
                  </p>
                </div>
              )}
              {details.target && (
                <div>
                  <h3 className="mb-1 font-semibold">
                    {lang === "ko" ? "대상" : "Target"}
                  </h3>
                  <p className="whitespace-pre-line text-sm text-muted-foreground">
                    {details.target}
                  </p>
                </div>
              )}
              {details.side_effects && (
                <div>
                  <h3 className="mb-1 flex items-center gap-1 font-semibold">
                    <AlertTriangle className="h-4 w-4 text-amber-500" />
                    {lang === "ko" ? "부작용" : "Side Effects"}
                  </h3>
                  <p className="whitespace-pre-line text-sm text-muted-foreground">
                    {details.side_effects}
                  </p>
                </div>
              )}
              {(lang !== "ko" && translation?.post_care
                ? translation.post_care
                : details.post_care) && (
                <div>
                  <h3 className="mb-1 font-semibold">
                    {lang === "ko" ? "사후 관리" : "Post Care"}
                  </h3>
                  <p className="whitespace-pre-line text-sm text-muted-foreground">
                    {lang !== "ko" && translation?.post_care
                      ? translation.post_care
                      : details.post_care}
                  </p>
                </div>
              )}
            </CardContent>
          </Card>
        )}

        {/* Price Comparison */}
        {prices.length > 0 && (
          <Card className="mb-6">
            <CardHeader>
              <CardTitle className="text-lg">{ui.priceCompare}</CardTitle>
              <CardDescription>USD</CardDescription>
            </CardHeader>
            <CardContent>
              <div className="space-y-3">
                {prices.map((p) => {
                  const avg =
                    ((p.price_min ?? 0) + (p.price_max ?? p.price_min ?? 0)) /
                    2;
                  const maxAvg = Math.max(
                    ...prices.map(
                      (pp) =>
                        ((pp.price_min ?? 0) +
                          (pp.price_max ?? pp.price_min ?? 0)) /
                        2,
                    ),
                  );
                  const barWidth = maxAvg > 0 ? (avg / maxAvg) * 100 : 0;

                  return (
                    <div key={p.country} className="flex items-center gap-3">
                      <span className="w-20 text-sm font-medium">
                        {COUNTRY_LABELS[p.country] ?? p.country}
                      </span>
                      <div className="flex-1">
                        <div className="h-6 w-full rounded-full bg-gray-100">
                          <div
                            className={`h-6 rounded-full ${
                              p.country === "KR" ? "bg-blue-500" : "bg-gray-300"
                            }`}
                            style={{ width: `${barWidth}%` }}
                          />
                        </div>
                      </div>
                      <span className="w-32 text-right text-sm">
                        {formatUsd(p.price_min, p.price_max)}
                      </span>
                    </div>
                  );
                })}
              </div>
            </CardContent>
          </Card>
        )}

        {/* Recommended Clinics */}
        {clinics.length > 0 && (
          <Card className="mb-6">
            <CardHeader>
              <CardTitle className="flex items-center gap-2 text-lg">
                <Hospital className="h-5 w-5" />
                {ui.recommendedClinics}
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className="flex flex-wrap gap-2">
                {clinics.map((c) => (
                  <Badge key={c.clinic_id} variant="outline">
                    #{c.rank} Clinic {c.clinic_id}
                  </Badge>
                ))}
              </div>
            </CardContent>
          </Card>
        )}

        {/* Related Procedures */}
        {related.length > 0 && (
          <Card className="mb-6">
            <CardHeader>
              <CardTitle className="text-lg">{ui.relatedProcedures}</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="grid gap-2 sm:grid-cols-2">
                {related.map((r) => (
                  <Link
                    key={r.id}
                    href={`/guide/${lang}/procedure/${r.id}`}
                    className="flex items-center justify-between rounded-lg border p-3 transition-colors hover:bg-gray-50"
                  >
                    <span className="text-sm font-medium">
                      {r.name_intl ?? r.name}
                    </span>
                    <ArrowLeft className="h-3 w-3 rotate-180 text-muted-foreground" />
                  </Link>
                ))}
              </div>
            </CardContent>
          </Card>
        )}

        {/* hreflang links for SEO crawlers (invisible) */}
        {SUPPORTED_LANGS.map((l) => (
          <link
            key={l}
            rel="alternate"
            hrefLang={l}
            href={`https://mediscope.kr/guide/${l}/procedure/${id}`}
          />
        ))}

        <script
          type="application/ld+json"
          dangerouslySetInnerHTML={{ __html: JSON.stringify(jsonLd) }}
        />
      </div>
    </div>
  );
}
