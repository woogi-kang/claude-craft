import { Metadata } from "next";
import Link from "next/link";
import { Globe, ArrowRight } from "lucide-react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { createAdminClient } from "@/lib/supabase/admin";
import { SUPPORTED_LANGS, LANG_LABELS, GUIDE_UI } from "@/lib/i18n";
import { BEAUTY_CATEGORIES } from "@/lib/types/beauty";

export const metadata: Metadata = {
  title: "한국 의료관광 시술 가이드 | CheckYourHospital",
  description:
    "한국에서 받을 수 있는 미용 시술을 언어별, 카테고리별로 확인하세요. 가격 비교와 추천 병원 정보를 제공합니다.",
  openGraph: {
    title: "한국 의료관광 시술 가이드 | CheckYourHospital",
    description: "한국 미용 시술 가이드 - 가격 비교, 추천 병원, 다국어 지원",
    type: "website",
  },
};

interface CategoryWithStats {
  id: number;
  name_ko: string;
  name_en: string;
  slug: string;
  procedure_count: number;
}

async function getCategories(): Promise<CategoryWithStats[]> {
  try {
    const supabase = createAdminClient();

    const { data: categories } = await supabase
      .from("procedure_categories")
      .select("id, name_ko, name_en, slug")
      .order("id");

    if (!categories) return [];

    const { data: procedures } = await supabase
      .from("procedures")
      .select("id, primary_category_id");

    const countMap = new Map<number, number>();
    for (const p of procedures ?? []) {
      countMap.set(
        p.primary_category_id,
        (countMap.get(p.primary_category_id) ?? 0) + 1,
      );
    }

    return categories.map((cat) => ({
      ...cat,
      procedure_count: countMap.get(cat.id) ?? 0,
    }));
  } catch {
    return [];
  }
}

export default async function GuideLandingPage() {
  const categories = await getCategories();

  return (
    <div className="min-h-screen bg-gradient-to-b from-blue-50 to-white">
      <div className="mx-auto max-w-6xl px-4 py-12">
        {/* Hero */}
        <div className="mb-12 text-center">
          <div className="mb-4 inline-flex items-center gap-2 rounded-full bg-blue-100 px-4 py-2 text-sm font-medium text-blue-700">
            <Globe className="h-4 w-4" />
            4개 언어 지원
          </div>
          <h1 className="text-4xl font-bold tracking-tight sm:text-5xl">
            한국 의료관광 시술 가이드
          </h1>
          <p className="mt-4 text-lg text-muted-foreground">
            한국에서 받을 수 있는 미용 시술을 카테고리별로 확인하세요.
            <br />
            국가별 가격 비교와 추천 병원 정보를 제공합니다.
          </p>
        </div>

        {/* Language Selection */}
        <div className="mb-12">
          <h2 className="mb-4 text-center text-lg font-semibold text-muted-foreground">
            언어를 선택하세요
          </h2>
          <div className="mx-auto grid max-w-2xl grid-cols-2 gap-3 sm:grid-cols-4">
            {SUPPORTED_LANGS.map((lang) => (
              <Link
                key={lang}
                href={`/guide/${lang}/${categories[0]?.slug ?? ""}`}
              >
                <Card className="h-full cursor-pointer transition-shadow hover:shadow-md">
                  <CardContent className="flex flex-col items-center justify-center py-6">
                    <span className="text-2xl font-bold">
                      {lang.toUpperCase()}
                    </span>
                    <span className="mt-1 text-sm text-muted-foreground">
                      {LANG_LABELS[lang]}
                    </span>
                  </CardContent>
                </Card>
              </Link>
            ))}
          </div>
        </div>

        {/* Category Grid */}
        <h2 className="mb-6 text-2xl font-bold">카테고리</h2>
        <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
          {categories.map((cat) => {
            const catInfo = BEAUTY_CATEGORIES[cat.id];
            return (
              <Link key={cat.id} href={`/guide/ko/${cat.slug}`}>
                <Card className="h-full cursor-pointer transition-all hover:shadow-md hover:-translate-y-0.5">
                  <CardHeader className="pb-2">
                    <div className="flex items-center justify-between">
                      <span className="text-2xl">{catInfo?.icon ?? "💊"}</span>
                      <Badge variant="secondary">
                        {cat.procedure_count}
                        {GUIDE_UI.ko.procedureCount}
                      </Badge>
                    </div>
                    <CardTitle className="text-lg">{cat.name_ko}</CardTitle>
                  </CardHeader>
                  <CardContent>
                    <p className="text-sm text-muted-foreground">
                      {cat.name_en}
                    </p>
                    <div className="mt-3 flex items-center text-sm text-blue-600">
                      자세히 보기
                      <ArrowRight className="ml-1 h-3 w-3" />
                    </div>
                  </CardContent>
                </Card>
              </Link>
            );
          })}
        </div>

        {/* JSON-LD */}
        <script
          type="application/ld+json"
          dangerouslySetInnerHTML={{
            __html: JSON.stringify({
              "@context": "https://schema.org",
              "@type": "MedicalWebPage",
              name: "한국 의료관광 시술 가이드",
              description:
                "한국에서 받을 수 있는 미용 시술 가이드 - 가격 비교, 추천 병원",
              url: "https://checkyourhospital.kr/guide",
              inLanguage: ["ko", "en", "ja", "zh"],
              about: {
                "@type": "MedicalSpecialty",
                name: "Dermatology",
              },
            }),
          }}
        />
      </div>
    </div>
  );
}
