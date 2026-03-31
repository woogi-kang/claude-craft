"use client";

import {
  Globe,
  Phone,
  Clock,
  DollarSign,
  Languages,
  Plane,
  Building,
  CreditCard,
  Type,
  Image,
  Check,
  X,
  AlertTriangle,
  ChevronDown,
  ChevronUp,
} from "lucide-react";
import { useState } from "react";

interface CheckItem {
  status: "pass" | "warn" | "fail";
  detail: string;
}

interface Recommendation {
  priority: string;
  check: string;
  message: string;
}

interface InternationalUsabilityData {
  overall_score: number;
  checks: Record<string, CheckItem>;
  pass_count: number;
  warn_count: number;
  fail_count: number;
  recommendations: Recommendation[];
}

interface InternationalUsabilityProps {
  data: InternationalUsabilityData;
}

const CHECK_CONFIG: {
  key: string;
  label: string;
  icon: typeof Globe;
  description: string;
}[] = [
  {
    key: "lang_switcher",
    label: "언어 전환 버튼",
    icon: Globe,
    description: "메인 네비게이션 언어 스위처",
  },
  {
    key: "intl_phone",
    label: "국제 전화번호",
    icon: Phone,
    description: "+82 국가코드 포함 여부",
  },
  {
    key: "timezone",
    label: "시간대 표시",
    icon: Clock,
    description: "KST/UTC 등 시간대 명시",
  },
  {
    key: "currency",
    label: "다중 통화 표시",
    icon: DollarSign,
    description: "USD/JPY/CNY 등 환산 표기",
  },
  {
    key: "google_translate",
    label: "번역 위젯",
    icon: Languages,
    description: "Google Translate 위젯",
  },
  {
    key: "visa_info",
    label: "비자/입국 안내",
    icon: Plane,
    description: "의료관광 비자 정보",
  },
  {
    key: "travel_support",
    label: "공항 픽업/숙소",
    icon: Building,
    description: "교통/숙박 지원 안내",
  },
  {
    key: "payment_methods",
    label: "해외 결제수단",
    icon: CreditCard,
    description: "Alipay, WeChat Pay, PayPal 등",
  },
  {
    key: "multilingual_fonts",
    label: "다국어 폰트",
    icon: Type,
    description: "CJK 웹폰트 지원",
  },
  {
    key: "alt_multilingual",
    label: "이미지 alt 다국어",
    icon: Image,
    description: "외국어 alt 텍스트",
  },
];

function StatusBadge({ status }: { status: string }) {
  if (status === "pass") {
    return (
      <span className="inline-flex items-center gap-1 rounded-full bg-green-100 px-2 py-0.5 text-xs font-medium text-green-700">
        <Check className="h-3 w-3" />
        충족
      </span>
    );
  }
  if (status === "warn") {
    return (
      <span className="inline-flex items-center gap-1 rounded-full bg-yellow-100 px-2 py-0.5 text-xs font-medium text-yellow-700">
        <AlertTriangle className="h-3 w-3" />
        부분
      </span>
    );
  }
  return (
    <span className="inline-flex items-center gap-1 rounded-full bg-red-100 px-2 py-0.5 text-xs font-medium text-red-700">
      <X className="h-3 w-3" />
      미충족
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

function GradeLabel({ score }: { score: number }) {
  if (score >= 80)
    return <span className="text-green-600 font-bold">우수</span>;
  if (score >= 60) return <span className="text-blue-600 font-bold">양호</span>;
  if (score >= 40)
    return <span className="text-yellow-600 font-bold">보통</span>;
  return <span className="text-red-600 font-bold">미흡</span>;
}

export function InternationalUsability({ data }: InternationalUsabilityProps) {
  const [showRecs, setShowRecs] = useState(false);

  if (!data) return null;

  const totalChecks = data.pass_count + data.warn_count + data.fail_count;

  return (
    <section className="mt-10">
      <div className="mb-4">
        <h2 className="text-lg font-bold text-slate-900">
          해외 환자 사용성 분석
        </h2>
        <p className="mt-1 text-sm text-slate-500">
          외국인 환자가 실제로 사이트를 이용할 수 있는지 UX 관점에서 점검
        </p>
      </div>

      <div className="rounded-xl border border-slate-200 bg-white p-5 sm:p-6">
        {/* Score overview */}
        <div className="mb-5">
          <div className="flex items-center justify-between mb-2">
            <div className="flex items-center gap-2">
              <span className="text-sm font-medium text-slate-600">
                해외 환자 사용성 점수
              </span>
              <GradeLabel score={data.overall_score} />
            </div>
            <span className="text-xs text-slate-400">
              {data.pass_count}/{totalChecks} 항목 충족
            </span>
          </div>
          <ScoreBar score={data.overall_score} />
        </div>

        {/* Status summary pills */}
        <div className="mb-4 flex gap-2 flex-wrap">
          {data.pass_count > 0 && (
            <span className="inline-flex items-center gap-1 rounded-full bg-green-50 border border-green-200 px-3 py-1 text-xs text-green-700">
              <Check className="h-3 w-3" /> 충족 {data.pass_count}
            </span>
          )}
          {data.warn_count > 0 && (
            <span className="inline-flex items-center gap-1 rounded-full bg-yellow-50 border border-yellow-200 px-3 py-1 text-xs text-yellow-700">
              <AlertTriangle className="h-3 w-3" /> 부분 {data.warn_count}
            </span>
          )}
          {data.fail_count > 0 && (
            <span className="inline-flex items-center gap-1 rounded-full bg-red-50 border border-red-200 px-3 py-1 text-xs text-red-700">
              <X className="h-3 w-3" /> 미충족 {data.fail_count}
            </span>
          )}
        </div>

        {/* Checklist */}
        <div className="grid gap-2 sm:grid-cols-2">
          {CHECK_CONFIG.map(({ key, label, icon: Icon, description }) => {
            const check = data.checks[key];
            if (!check) return null;
            const { status, detail } = check;
            const borderColor =
              status === "pass"
                ? "border-green-200 bg-green-50/50"
                : status === "warn"
                  ? "border-yellow-200 bg-yellow-50/50"
                  : "border-slate-200 bg-slate-50/50";
            const iconColor =
              status === "pass"
                ? "text-green-600"
                : status === "warn"
                  ? "text-yellow-600"
                  : "text-slate-400";
            const textColor =
              status === "pass"
                ? "text-green-800"
                : status === "warn"
                  ? "text-yellow-800"
                  : "text-slate-600";

            return (
              <div
                key={key}
                className={`flex items-center gap-3 rounded-lg border p-3 ${borderColor}`}
                title={detail}
              >
                <Icon className={`h-4 w-4 flex-shrink-0 ${iconColor}`} />
                <div className="min-w-0 flex-1">
                  <p className={`text-sm font-medium ${textColor}`}>{label}</p>
                  <p className="text-xs text-slate-400 truncate">
                    {detail || description}
                  </p>
                </div>
                <StatusBadge status={status} />
              </div>
            );
          })}
        </div>

        {/* Recommendations */}
        {data.recommendations && data.recommendations.length > 0 && (
          <div className="mt-5">
            <button
              onClick={() => setShowRecs(!showRecs)}
              className="flex w-full items-center justify-between rounded-lg bg-amber-50 px-4 py-2.5 text-left"
            >
              <div className="flex items-center gap-2">
                <AlertTriangle className="h-4 w-4 text-amber-500" />
                <span className="text-sm font-medium text-amber-800">
                  개선 추천사항 ({data.recommendations.length}건)
                </span>
              </div>
              {showRecs ? (
                <ChevronUp className="h-4 w-4 text-amber-500" />
              ) : (
                <ChevronDown className="h-4 w-4 text-amber-500" />
              )}
            </button>
            {showRecs && (
              <ul className="mt-2 space-y-2 px-1">
                {data.recommendations.map((rec, i) => (
                  <li
                    key={i}
                    className="flex items-start gap-2 text-sm text-slate-700"
                  >
                    <span
                      className={`mt-0.5 flex h-5 w-5 flex-shrink-0 items-center justify-center rounded-full text-xs font-bold ${
                        rec.priority === "high"
                          ? "bg-red-100 text-red-700"
                          : "bg-amber-100 text-amber-700"
                      }`}
                    >
                      {i + 1}
                    </span>
                    {rec.message}
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
