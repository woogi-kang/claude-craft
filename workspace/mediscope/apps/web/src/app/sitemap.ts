import { MetadataRoute } from "next";
import { createAdminClient } from "@/lib/supabase/admin";
import { SUPPORTED_LANGS } from "@/lib/i18n";

export default async function sitemap(): Promise<MetadataRoute.Sitemap> {
  const entries: MetadataRoute.Sitemap = [];
  const baseUrl = "https://checkyourhospital.kr";

  // 정적 페이지
  entries.push({
    url: `${baseUrl}`,
    lastModified: new Date(),
    changeFrequency: "daily",
    priority: 1.0,
  });

  entries.push({
    url: `${baseUrl}/guide`,
    lastModified: new Date(),
    changeFrequency: "weekly",
    priority: 0.9,
  });

  try {
    const supabase = createAdminClient();

    const [categoriesResult, proceduresResult] = await Promise.all([
      supabase.from("procedure_categories").select("id, slug").order("id"),
      supabase.from("procedures").select("id").order("id"),
    ]);

    const categories = categoriesResult.data ?? [];
    const procedures = proceduresResult.data ?? [];

    // 카테고리별 가이드 페이지 (언어 x 카테고리)
    for (const cat of categories) {
      for (const lang of SUPPORTED_LANGS) {
        const alternates: Record<string, string> = {};
        for (const l of SUPPORTED_LANGS) {
          alternates[l] = `${baseUrl}/guide/${l}/${cat.slug}`;
        }

        entries.push({
          url: `${baseUrl}/guide/${lang}/${cat.slug}`,
          lastModified: new Date(),
          changeFrequency: "weekly",
          priority: 0.8,
          alternates: {
            languages: alternates,
          },
        });
      }
    }

    // 시술 상세 페이지 (언어 x 시술)
    for (const proc of procedures) {
      for (const lang of SUPPORTED_LANGS) {
        const alternates: Record<string, string> = {};
        for (const l of SUPPORTED_LANGS) {
          alternates[l] = `${baseUrl}/guide/${l}/procedure/${proc.id}`;
        }

        entries.push({
          url: `${baseUrl}/guide/${lang}/procedure/${proc.id}`,
          lastModified: new Date(),
          changeFrequency: "monthly",
          priority: 0.7,
          alternates: {
            languages: alternates,
          },
        });
      }
    }
  } catch {
    // Supabase 연결 실패 시 정적 페이지만 반환
  }

  return entries;
}
