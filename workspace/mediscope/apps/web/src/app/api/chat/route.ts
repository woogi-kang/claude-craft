import { NextRequest, NextResponse } from "next/server";
import { createAdminClient } from "@/lib/supabase/admin";

interface ChatRequest {
  message: string;
  sessionId?: string;
}

interface ChatResponse {
  reply: string;
  suggestions?: string[];
  data?: unknown;
}

type Intent = "procedure" | "price" | "clinic" | "greeting" | "unknown";

const GREETING_PATTERNS = [
  /^(안녕|하이|헬로|hi|hello|hey|반가)/i,
  /^(도움|help|뭐|무엇|어떤.*할 수)/i,
];

const PRICE_KEYWORDS = [
  "가격",
  "비용",
  "얼마",
  "price",
  "cost",
  "how much",
  "비교",
  "저렴",
  "싼",
  "expensive",
  "cheap",
];

const CLINIC_KEYWORDS = [
  "병원",
  "추천",
  "clinic",
  "hospital",
  "어디",
  "where",
  "좋은",
  "best",
  "의원",
  "피부과",
];

const PROCEDURE_KEYWORDS = [
  "시술",
  "치료",
  "procedure",
  "treatment",
  "뭐가",
  "종류",
  "효과",
  "부작용",
  "통증",
  "다운타임",
];

function detectIntent(message: string): Intent {
  const lower = message.toLowerCase().trim();

  for (const pattern of GREETING_PATTERNS) {
    if (pattern.test(lower)) return "greeting";
  }

  if (PRICE_KEYWORDS.some((k) => lower.includes(k))) return "price";
  if (CLINIC_KEYWORDS.some((k) => lower.includes(k))) return "clinic";
  if (PROCEDURE_KEYWORDS.some((k) => lower.includes(k))) return "procedure";

  return "unknown";
}

function extractKeywords(message: string): string[] {
  const stopWords = new Set([
    "에",
    "대해",
    "알려줘",
    "알려주세요",
    "해줘",
    "해주세요",
    "뭐",
    "좀",
    "는",
    "은",
    "이",
    "가",
    "을",
    "를",
    "의",
    "로",
    "으로",
    "에서",
    "도",
    "와",
    "과",
    "하고",
    "이랑",
    "요",
    "이요",
    "있나요",
    "있어요",
    "할",
    "수",
    "있",
    "어떤",
    "어떻게",
    "what",
    "is",
    "the",
    "a",
    "an",
    "about",
    "tell",
    "me",
    "please",
    "can",
    "you",
    ...PRICE_KEYWORDS,
    ...CLINIC_KEYWORDS,
    ...PROCEDURE_KEYWORDS,
  ]);

  return message
    .replace(/[?!.,;:'"]/g, "")
    .split(/\s+/)
    .filter((w) => w.length > 1 && !stopWords.has(w.toLowerCase()));
}

async function handleProcedure(message: string): Promise<ChatResponse> {
  const supabase = createAdminClient();
  const keywords = extractKeywords(message);

  // Try search_dict first for better matching
  const procedureIds: number[] = [];
  if (keywords.length > 0) {
    for (const keyword of keywords) {
      const { data: dictResults } = await supabase
        .from("search_dict")
        .select("procedure_id")
        .ilike("term", `%${keyword}%`)
        .limit(10);

      if (dictResults?.length) {
        procedureIds.push(
          ...dictResults
            .map((d) => d.procedure_id)
            .filter((id): id is number => id !== null),
        );
      }
    }
  }

  // Also search procedures directly by name
  let procedures: Array<{
    id: number;
    name: string;
    primary_category_id: number;
  }> = [];

  if (procedureIds.length > 0) {
    const uniqueIds = [...new Set(procedureIds)].slice(0, 10);
    const { data } = await supabase
      .from("procedures")
      .select("id, name, primary_category_id")
      .in("id", uniqueIds);
    if (data) procedures = data;
  }

  // Fallback: direct name search
  if (procedures.length === 0 && keywords.length > 0) {
    for (const keyword of keywords) {
      const { data } = await supabase
        .from("procedures")
        .select("id, name, primary_category_id")
        .ilike("name", `%${keyword}%`)
        .limit(5);
      if (data?.length) {
        procedures.push(...data);
        break;
      }
    }
  }

  if (procedures.length === 0) {
    // If no match, suggest categories
    const { data: categories } = await supabase
      .from("procedure_categories")
      .select("name, name_en")
      .eq("level", 1)
      .order("display_order")
      .limit(8);

    const categoryList =
      categories?.map((c) => `${c.name} (${c.name_en})`).join(", ") ?? "";

    return {
      reply: `죄송합니다, 관련 시술을 찾지 못했어요. 다음 카테고리에서 찾아보실 수 있어요:\n\n${categoryList}\n\n구체적인 시술명이나 카테고리를 말씀해주세요!`,
      suggestions: ["피부관리 시술 종류", "안티에이징 추천", "보톡스 효과"],
    };
  }

  // Deduplicate
  const uniqueProcs = Array.from(
    new Map(procedures.map((p) => [p.id, p])).values(),
  ).slice(0, 5);

  // Fetch details for the first procedure
  const { data: detail } = await supabase
    .from("procedure_details")
    .select(
      "procedure_name, effect, method, duration_of_procedure, pain_level, pain_description, downtime, average_price",
    )
    .eq("procedure_id", uniqueProcs[0].id)
    .single();

  let reply = "";
  if (detail) {
    reply = `**${detail.procedure_name}**\n\n`;
    if (detail.effect) reply += `효과: ${detail.effect}\n`;
    if (detail.method) reply += `방법: ${detail.method}\n`;
    if (detail.duration_of_procedure)
      reply += `소요시간: ${detail.duration_of_procedure}\n`;
    if (detail.pain_level !== null && detail.pain_level !== undefined)
      reply += `통증: ${detail.pain_level}/10${detail.pain_description ? ` (${detail.pain_description})` : ""}\n`;
    if (detail.downtime) reply += `다운타임: ${detail.downtime}\n`;
    if (detail.average_price) reply += `평균가격: ${detail.average_price}\n`;
  } else {
    reply = `**${uniqueProcs[0].name}** 시술을 찾았어요!`;
  }

  if (uniqueProcs.length > 1) {
    reply += `\n\n관련 시술: ${uniqueProcs
      .slice(1)
      .map((p) => p.name)
      .join(", ")}`;
  }

  return {
    reply,
    suggestions: [
      `${uniqueProcs[0].name} 가격 비교`,
      `${uniqueProcs[0].name} 병원 추천`,
      "다른 시술 검색",
    ],
    data: { procedures: uniqueProcs, detail },
  };
}

async function handlePrice(message: string): Promise<ChatResponse> {
  const supabase = createAdminClient();
  const keywords = extractKeywords(message);

  // Try to find matching procedure for price comparison
  let therapyId: number | null = null;
  let procedureName = "";

  if (keywords.length > 0) {
    for (const keyword of keywords) {
      const { data } = await supabase
        .from("beauty_std_procedures")
        .select("id, name")
        .ilike("name", `%${keyword}%`)
        .limit(1);
      if (data?.length) {
        therapyId = data[0].id;
        procedureName = data[0].name;
        break;
      }
    }

    // Fallback to procedures table
    if (!therapyId) {
      for (const keyword of keywords) {
        const { data } = await supabase
          .from("procedures")
          .select("id, name")
          .ilike("name", `%${keyword}%`)
          .limit(1);
        if (data?.length) {
          procedureName = data[0].name;
          // Try to find matching therapy
          const { data: therapy } = await supabase
            .from("beauty_std_procedures")
            .select("id, name")
            .ilike("name", `%${keyword}%`)
            .limit(1);
          if (therapy?.length) {
            therapyId = therapy[0].id;
          }
          break;
        }
      }
    }
  }

  if (therapyId) {
    // Fetch KR prices
    const { data: krPrices } = await supabase
      .from("price_comparison")
      .select("country, currency, price_min, price_max")
      .eq("therapy_id", therapyId);

    // Fetch international prices
    const { data: intlPrices } = await supabase
      .from("intl_prices")
      .select("country_code, currency, price, price_unit")
      .eq("top_procedure_id", therapyId);

    let reply = `**${procedureName} 가격 비교**\n\n`;

    if (krPrices?.length) {
      for (const p of krPrices) {
        const min = p.price_min?.toLocaleString() ?? "-";
        const max = p.price_max?.toLocaleString() ?? "-";
        reply += `${p.country}: ${min} ~ ${max} ${p.currency}\n`;
      }
    }

    if (intlPrices?.length) {
      reply += "\n해외 가격:\n";
      for (const p of intlPrices) {
        reply += `${p.country_code}: ${p.price?.toLocaleString() ?? "-"} ${p.currency}${p.price_unit ? ` (${p.price_unit})` : ""}\n`;
      }
    }

    if (!krPrices?.length && !intlPrices?.length) {
      reply += "아직 가격 정보가 등록되지 않은 시술이에요.";
    }

    return {
      reply,
      suggestions: [
        `${procedureName} 시술 정보`,
        `${procedureName} 병원 추천`,
        "다른 시술 가격",
      ],
      data: { krPrices, intlPrices },
    };
  }

  // No specific procedure matched - show popular comparisons
  const { data: prices } = await supabase
    .from("price_comparison")
    .select("therapy_id")
    .eq("country", "KR")
    .limit(5);

  if (prices?.length) {
    const ids = [...new Set(prices.map((p) => p.therapy_id))];
    const { data: procs } = await supabase
      .from("beauty_std_procedures")
      .select("id, name")
      .in("id", ids);

    const procNames = procs?.map((p) => p.name).join(", ") ?? "";

    return {
      reply: `어떤 시술의 가격을 비교해 드릴까요?\n\n가격 비교 가능한 시술: ${procNames}\n\n시술명을 포함해서 다시 질문해주세요!`,
      suggestions: procs?.slice(0, 3).map((p) => `${p.name} 가격 비교`) ?? [],
    };
  }

  return {
    reply:
      "가격 비교 정보를 불러오는 데 실패했어요. 시술명을 포함해서 다시 질문해주세요!",
    suggestions: ["보톡스 가격", "필러 가격 비교", "레이저 시술 비용"],
  };
}

async function handleClinic(message: string): Promise<ChatResponse> {
  const supabase = createAdminClient();
  const keywords = extractKeywords(message);

  // Check for region keywords
  const regionKeywords = [
    "서울",
    "강남",
    "부산",
    "대구",
    "인천",
    "광주",
    "대전",
    "울산",
    "제주",
    "경기",
  ];
  const matchedRegion = regionKeywords.find((r) => message.includes(r));

  // First check recommended_clinics
  const { data: recommended } = await supabase
    .from("recommended_clinics")
    .select(
      "id, hospital_id, region, target_procedures, interpreter_languages, consultation_level",
    )
    .limit(10);

  // Get clinic details from beauty_clinics
  let clinicQuery = supabase
    .from("beauty_clinics")
    .select("id, name, sido, sggu, website, is_foreign_patient_facilitator")
    .eq("is_foreign_patient_facilitator", true)
    .limit(10);

  if (matchedRegion) {
    clinicQuery = clinicQuery.ilike("sido", `%${matchedRegion}%`);
  }

  const { data: clinics } = await clinicQuery;

  let reply = "";

  if (recommended?.length) {
    // Get hospital names for recommended clinics
    const hospitalIds = recommended
      .map((r) => r.hospital_id)
      .filter((id): id is number => id !== null);
    const { data: hospitals } = await supabase
      .from("beauty_clinics")
      .select("id, name, sido, sggu, website")
      .in("id", hospitalIds);

    reply = "**추천 병원**\n\n";
    for (const rec of recommended.slice(0, 5)) {
      const hospital = hospitals?.find((h) => h.id === rec.hospital_id);
      if (hospital) {
        reply += `- **${hospital.name}** (${hospital.sido ?? ""} ${hospital.sggu ?? ""})\n`;
        if (rec.target_procedures?.length) {
          reply += `  주요 시술: ${rec.target_procedures.join(", ")}\n`;
        }
        if (rec.interpreter_languages?.length) {
          reply += `  통역 가능: ${rec.interpreter_languages.join(", ")}\n`;
        }
      }
    }
  } else if (clinics?.length) {
    reply = matchedRegion
      ? `**${matchedRegion} 지역 외국인환자 유치 의료기관**\n\n`
      : "**외국인환자 유치 의료기관**\n\n";

    for (const c of clinics.slice(0, 5)) {
      reply += `- **${c.name}** (${c.sido ?? ""} ${c.sggu ?? ""})`;
      if (c.website) reply += ` [홈페이지](${c.website})`;
      reply += "\n";
    }
  } else {
    reply =
      "현재 조건에 맞는 병원을 찾지 못했어요. 지역이나 시술명을 포함해서 다시 질문해주세요!";
  }

  return {
    reply,
    suggestions: [
      "서울 강남 병원 추천",
      "보톡스 잘하는 병원",
      "시술 가격 비교",
    ],
    data: { recommended, clinics },
  };
}

function handleGreeting(): ChatResponse {
  return {
    reply:
      "안녕하세요! MediScope AI 상담 챗봇이에요.\n\n다음과 같은 질문에 답변해 드릴 수 있어요:\n\n- 시술 정보 (효과, 방법, 다운타임 등)\n- 가격 비교 (한국 vs 해외)\n- 병원 추천 (지역별, 시술별)\n\n궁금한 것을 물어보세요!",
    suggestions: ["인기 시술 추천", "보톡스 가격 비교", "강남 병원 추천"],
  };
}

function handleUnknown(message: string): ChatResponse {
  return {
    reply: `"${message}"에 대해 정확한 답변을 드리기 어려워요.\n\n시술명, 가격, 병원에 대해 구체적으로 질문해주시면 더 정확한 정보를 드릴 수 있어요!`,
    suggestions: ["시술 종류 알려줘", "가격 비교해줘", "병원 추천해줘"],
  };
}

export async function POST(request: NextRequest) {
  try {
    const body = (await request.json()) as ChatRequest;
    const { message } = body;

    if (!message?.trim()) {
      return NextResponse.json(
        { error: "메시지를 입력해주세요" },
        { status: 400 },
      );
    }

    const intent = detectIntent(message);

    let response: ChatResponse;
    switch (intent) {
      case "greeting":
        response = handleGreeting();
        break;
      case "procedure":
        response = await handleProcedure(message);
        break;
      case "price":
        response = await handlePrice(message);
        break;
      case "clinic":
        response = await handleClinic(message);
        break;
      default:
        // Try procedure search as fallback before returning unknown
        response = await handleProcedure(message);
        if (
          response.reply.includes("찾지 못했") ||
          response.reply.includes("카테고리에서")
        ) {
          response = handleUnknown(message);
        }
    }

    return NextResponse.json(response);
  } catch {
    return NextResponse.json({ error: "서버 오류" }, { status: 500 });
  }
}
