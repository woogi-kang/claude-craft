export const SUPPORTED_LANGS = ["ko", "en", "ja", "zh"] as const;
export type Lang = (typeof SUPPORTED_LANGS)[number];

export function isValidLang(lang: string): lang is Lang {
  return SUPPORTED_LANGS.includes(lang as Lang);
}

export const LANG_LABELS: Record<Lang, string> = {
  ko: "한국어",
  en: "English",
  ja: "日本語",
  zh: "中文",
};

export const LANG_LOCALE: Record<Lang, string> = {
  ko: "ko_KR",
  en: "en_US",
  ja: "ja_JP",
  zh: "zh_CN",
};

export const GUIDE_UI: Record<
  Lang,
  {
    title: string;
    subtitle: string;
    procedureCount: string;
    avgDiscount: string;
    viewAll: string;
    backToGuide: string;
    priceCompare: string;
    relatedProcedures: string;
    recommendedClinics: string;
    recoveryDays: string;
    priceRange: string;
    koreaPrice: string;
    savings: string;
  }
> = {
  ko: {
    title: "한국 의료관광 시술 가이드",
    subtitle: "한국에서 받을 수 있는 미용 시술을 카테고리별로 확인하세요",
    procedureCount: "개 시술",
    avgDiscount: "평균 할인율",
    viewAll: "전체 보기",
    backToGuide: "가이드로 돌아가기",
    priceCompare: "국가별 가격 비교",
    relatedProcedures: "관련 시술",
    recommendedClinics: "추천 병원",
    recoveryDays: "회복 기간",
    priceRange: "가격 범위",
    koreaPrice: "한국 가격",
    savings: "절감 효과",
  },
  en: {
    title: "Korea Medical Tourism Procedure Guide",
    subtitle: "Explore cosmetic procedures available in Korea by category",
    procedureCount: " procedures",
    avgDiscount: "Avg. discount",
    viewAll: "View all",
    backToGuide: "Back to guide",
    priceCompare: "Price comparison by country",
    relatedProcedures: "Related procedures",
    recommendedClinics: "Recommended clinics",
    recoveryDays: "Recovery period",
    priceRange: "Price range",
    koreaPrice: "Korea price",
    savings: "Savings",
  },
  ja: {
    title: "韓国医療観光施術ガイド",
    subtitle: "韓国で受けられる美容施術をカテゴリー別にご覧ください",
    procedureCount: "件の施術",
    avgDiscount: "平均割引率",
    viewAll: "すべて見る",
    backToGuide: "ガイドに戻る",
    priceCompare: "国別価格比較",
    relatedProcedures: "関連施術",
    recommendedClinics: "おすすめクリニック",
    recoveryDays: "回復期間",
    priceRange: "価格帯",
    koreaPrice: "韓国価格",
    savings: "節約額",
  },
  zh: {
    title: "韩国医疗旅游手术指南",
    subtitle: "按类别浏览韩国可接受的美容手术",
    procedureCount: "项手术",
    avgDiscount: "平均折扣",
    viewAll: "查看全部",
    backToGuide: "返回指南",
    priceCompare: "各国价格对比",
    relatedProcedures: "相关手术",
    recommendedClinics: "推荐医院",
    recoveryDays: "恢复期",
    priceRange: "价格范围",
    koreaPrice: "韩国价格",
    savings: "节省金额",
  },
};
