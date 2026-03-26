export interface Procedure {
  id: number;
  name: string;
  grade: number;
  primary_category_id: number;
  thumbnail_url?: string;
  is_leaf: boolean;
  thumbnail_alt?: string;
}

export interface PriceComparison {
  procedure_id: number;
  procedure_name: string;
  prices: CountryPrice[];
}

export interface CountryPrice {
  country: string;
  currency: string;
  price_min: number | null;
  price_max: number | null;
  price_unit?: string;
}

export interface PriceCompareResponse {
  procedure_id: number;
  procedure_name: string;
  prices: CountryPrice[];
}

export interface ProcedureCategory {
  id: number;
  name: string;
  name_en: string;
  icon?: string;
  description?: string;
}

export interface ProcedureDetail {
  id: number;
  procedure_id: number;
  procedure_name: string;
  alias?: string;
  target?: string;
  effect?: string;
  principle: string;
  mechanism_detail: string;
  method: string;
  duration_of_procedure?: string;
  duration?: string;
  recommended_cycle?: string;
  pain_level?: number;
  pain_description?: string;
  downtime?: string;
  side_effects?: string;
  post_care?: string;
  average_price?: string;
}

export interface ProcedureTranslation {
  language_code: string;
  translated_name?: string;
  principle?: string;
  method?: string;
  pain_description?: string;
  downtime?: string;
  post_care?: string;
}

export const BEAUTY_CATEGORIES: Record<
  number,
  { name: string; name_en: string; icon: string }
> = {
  1: { name: "피부관리", name_en: "Skin Care", icon: "💆" },
  2: { name: "제모", name_en: "Hair Removal", icon: "✨" },
  3: { name: "피부톤/색소", name_en: "Skin Tone", icon: "🎨" },
  4: { name: "기타", name_en: "Others", icon: "📋" },
  5: { name: "윤곽/볼륨", name_en: "Contouring", icon: "💎" },
  6: { name: "바디", name_en: "Body", icon: "🏋️" },
  7: { name: "안티에이징", name_en: "Anti-aging", icon: "⏳" },
  8: { name: "피부결/트러블", name_en: "Skin Texture", icon: "🔬" },
};

export const COUNTRY_LABELS: Record<string, string> = {
  KR: "한국 🇰🇷",
  JP: "일본 🇯🇵",
  CN: "중국 🇨🇳",
  TW: "대만 🇹🇼",
  TH: "태국 🇹🇭",
  VN: "베트남 🇻🇳",
};

export const COUNTRY_COLORS: Record<string, string> = {
  KR: "#3b82f6",
  JP: "#ef4444",
  CN: "#f59e0b",
  TW: "#10b981",
  TH: "#8b5cf6",
  VN: "#06b6d4",
};
