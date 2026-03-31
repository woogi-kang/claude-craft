"use client";

import {
  MousePointerClick,
  Phone,
  MessageCircle,
  FileText,
  DollarSign,
  Globe,
  Check,
  X,
  AlertTriangle,
  ChevronDown,
  ChevronUp,
} from "lucide-react";
import { useState } from "react";

interface ConversionData {
  cta_main: boolean;
  cta_procedure_pages: { total: number; with_cta: number };
  phone_clickable: boolean;
  phone_tel_links: number;
  phone_numbers_in_text: number;
  messengers: Record<string, boolean>;
  form_exists: boolean;
  form_fields: number;
  form_multilingual: boolean;
  price_visible: boolean;
  elements_found: string[];
  elements_missing: string[];
  score_breakdown: Record<string, number>;
}

interface ConversionAnalysisProps {
  data: ConversionData;
  score: number;
}

const ELEMENT_CONFIG: {
  key: string;
  label: string;
  icon: typeof Check;
  description: string;
}[] = [
  {
    key: "cta_main",
    label: "메인 CTA 버튼",
    icon: MousePointerClick,
    description: "예약/상담/문의 버튼",
  },
  {
    key: "phone_clickable",
    label: "전화번호 tel: 링크",
    icon: Phone,
    description: "모바일 클릭 통화 가능",
  },
  {
    key: "kakao",
    label: "카카오톡",
    icon: MessageCircle,
    description: "카카오톡 채널/플러스친구",
  },
  {
    key: "line",
    label: "LINE",
    icon: MessageCircle,
    description: "일본 환자 필수 메신저",
  },
  {
    key: "wechat",
    label: "WeChat",
    icon: MessageCircle,
    description: "중국 환자 필수 메신저",
  },
  {
    key: "chat_widget",
    label: "채팅 위젯",
    icon: MessageCircle,
    description: "Channel.io, Zendesk 등",
  },
  {
    key: "form",
    label: "예약/문의 폼",
    icon: FileText,
    description: "온라인 예약 양식",
  },
  {
    key: "form_multilingual",
    label: "폼 다국어 지원",
    icon: Globe,
    description: "외국어 placeholder/label",
  },
  {
    key: "price",
    label: "가격 정보 표시",
    icon: DollarSign,
    description: "시술 비용 정보 공개",
  },
];

function StatusBadge({ present }: { present: boolean }) {
  if (present) {
    return (
      <span className="inline-flex items-center gap-1 rounded-full bg-green-100 px-2 py-0.5 text-xs font-medium text-green-700">
        <Check className="h-3 w-3" />
        있음
      </span>
    );
  }
  return (
    <span className="inline-flex items-center gap-1 rounded-full bg-red-100 px-2 py-0.5 text-xs font-medium text-red-700">
      <X className="h-3 w-3" />
      없음
    </span>
  );
}

function ScoreBar({ score }: { score: number }) {
  const color =
    score >= 80
      ? "bg-green-500"
      : score >= 60
        ? "bg-blue-500"
        : score >= 40
          ? "bg-yellow-500"
          : "bg-red-500";

  return (
    <div className="flex items-center gap-3">
      <div className="h-2.5 flex-1 rounded-full bg-slate-100">
        <div
          className={`h-full rounded-full transition-all ${color}`}
          style={{ width: `${score}%` }}
        />
      </div>
      <span className="text-sm font-bold tabular-nums text-slate-900">
        {score}
      </span>
    </div>
  );
}

export function ConversionAnalysis({ data, score }: ConversionAnalysisProps) {
  const [showDetails, setShowDetails] = useState(false);

  if (!data) return null;

  const foundCount = data.elements_found?.length ?? 0;
  const totalCount = foundCount + (data.elements_missing?.length ?? 0);
  const messengerCount = Object.values(data.messengers ?? {}).filter(
    Boolean,
  ).length;

  // Build presence map
  const presenceMap: Record<string, boolean> = {};
  for (const el of data.elements_found ?? []) presenceMap[el] = true;
  for (const el of data.elements_missing ?? []) presenceMap[el] = false;

  // Recommendations based on missing elements
  const recommendations: string[] = [];
  if (!data.cta_main) {
    recommendations.push(
      "메인 페이지에 눈에 띄는 '예약하기' 또는 '상담 문의' CTA 버튼을 추가하세요",
    );
  }
  if (!data.phone_clickable) {
    recommendations.push(
      '전화번호를 <a href="tel:..."> 형식으로 변경하여 모바일에서 클릭 통화가 가능하게 하세요',
    );
  }
  if (messengerCount === 0) {
    recommendations.push(
      "카카오톡 채널, LINE, WeChat 중 타겟 환자 국가에 맞는 메신저를 연결하세요",
    );
  }
  if (!data.form_exists) {
    recommendations.push(
      "간단한 예약/문의 폼(이름, 연락처, 시술 종류)을 추가하세요",
    );
  } else if (data.form_fields > 5) {
    recommendations.push(
      `폼 입력 필드를 ${data.form_fields}개에서 5개 이하로 줄여 전환율을 높이세요`,
    );
  }
  if (!data.price_visible) {
    recommendations.push(
      "대표 시술의 가격 범위를 공개하여 환자의 의사결정을 도와주세요",
    );
  }
  if (!data.form_multilingual) {
    recommendations.push(
      "예약 폼의 placeholder와 label을 영어/일본어/중국어로도 제공하세요",
    );
  }

  return (
    <section className="mt-10">
      <div className="mb-4">
        <h2 className="text-lg font-bold text-slate-900">전환 퍼널 분석</h2>
        <p className="mt-1 text-sm text-slate-500">
          환자가 웹사이트를 방문한 후 예약으로 전환되기 위해 필요한 요소 점검
        </p>
      </div>

      <div className="rounded-xl border border-slate-200 bg-white p-5 sm:p-6">
        {/* Score overview */}
        <div className="mb-5">
          <div className="flex items-center justify-between mb-2">
            <span className="text-sm font-medium text-slate-600">
              전환 요소 점수
            </span>
            <span className="text-xs text-slate-400">
              {foundCount}/{totalCount} 요소 갖춤
            </span>
          </div>
          <ScoreBar score={score} />
        </div>

        {/* Checklist grid */}
        <div className="grid gap-2 sm:grid-cols-2">
          {ELEMENT_CONFIG.map(({ key, label, icon: Icon, description }) => {
            const present = presenceMap[key] ?? false;
            return (
              <div
                key={key}
                className={`flex items-center gap-3 rounded-lg border p-3 ${
                  present
                    ? "border-green-200 bg-green-50/50"
                    : "border-slate-200 bg-slate-50/50"
                }`}
              >
                <Icon
                  className={`h-4 w-4 flex-shrink-0 ${present ? "text-green-600" : "text-slate-400"}`}
                />
                <div className="min-w-0 flex-1">
                  <p
                    className={`text-sm font-medium ${present ? "text-green-800" : "text-slate-600"}`}
                  >
                    {label}
                  </p>
                  <p className="text-xs text-slate-400 truncate">
                    {description}
                  </p>
                </div>
                <StatusBadge present={present} />
              </div>
            );
          })}
        </div>

        {/* Procedure CTA coverage */}
        {data.cta_procedure_pages && data.cta_procedure_pages.total > 0 && (
          <div className="mt-4 rounded-lg bg-slate-50 p-3">
            <div className="flex items-center justify-between">
              <span className="text-sm text-slate-600">
                시술 페이지 CTA 커버리지
              </span>
              <span className="text-sm font-bold tabular-nums text-slate-900">
                {data.cta_procedure_pages.with_cta}/
                {data.cta_procedure_pages.total} 페이지
              </span>
            </div>
            <div className="mt-1.5 h-1.5 rounded-full bg-slate-200">
              <div
                className="h-full rounded-full bg-slate-600"
                style={{
                  width: `${(data.cta_procedure_pages.with_cta / data.cta_procedure_pages.total) * 100}%`,
                }}
              />
            </div>
          </div>
        )}

        {/* Form details */}
        {data.form_exists && (
          <div className="mt-4 flex items-center gap-4 rounded-lg bg-slate-50 p-3">
            <div className="flex items-center gap-2">
              <FileText className="h-4 w-4 text-slate-500" />
              <span className="text-sm text-slate-600">폼 필드 수</span>
            </div>
            <span
              className={`text-sm font-bold tabular-nums ${data.form_fields <= 5 ? "text-green-700" : "text-orange-700"}`}
            >
              {data.form_fields}개
            </span>
            {data.form_fields <= 5 ? (
              <span className="text-xs text-green-600">✓ 권장 기준 충족</span>
            ) : (
              <span className="text-xs text-orange-600">⚠ 5개 이하 권장</span>
            )}
          </div>
        )}

        {/* Recommendations */}
        {recommendations.length > 0 && (
          <div className="mt-5">
            <button
              onClick={() => setShowDetails(!showDetails)}
              className="flex w-full items-center justify-between rounded-lg bg-amber-50 px-4 py-2.5 text-left"
            >
              <div className="flex items-center gap-2">
                <AlertTriangle className="h-4 w-4 text-amber-500" />
                <span className="text-sm font-medium text-amber-800">
                  개선 추천사항 ({recommendations.length}건)
                </span>
              </div>
              {showDetails ? (
                <ChevronUp className="h-4 w-4 text-amber-500" />
              ) : (
                <ChevronDown className="h-4 w-4 text-amber-500" />
              )}
            </button>
            {showDetails && (
              <ul className="mt-2 space-y-2 px-1">
                {recommendations.map((rec, i) => (
                  <li
                    key={i}
                    className="flex items-start gap-2 text-sm text-slate-700"
                  >
                    <span className="mt-0.5 flex h-5 w-5 flex-shrink-0 items-center justify-center rounded-full bg-amber-100 text-xs font-bold text-amber-700">
                      {i + 1}
                    </span>
                    {rec}
                  </li>
                ))}
              </ul>
            )}
          </div>
        )}
      </div>
    </section>
  );
}
