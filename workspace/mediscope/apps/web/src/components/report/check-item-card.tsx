"use client";

import { useState } from "react";
import {
  CheckCircle,
  AlertTriangle,
  XCircle,
  MinusCircle,
  ChevronDown,
  ChevronUp,
} from "lucide-react";
import type { CheckItemData } from "@/lib/report-config";
import { getScoreStatus } from "@/lib/report-config";

interface CheckItemCardProps {
  itemKey: string;
  data: CheckItemData;
}

function getStatusIcon(score: number, failType: string) {
  if (failType === "system_limit" || failType === "api_error")
    return { Icon: MinusCircle, color: "text-slate-400" };
  if (score >= 80) return { Icon: CheckCircle, color: "text-green-500" };
  if (score >= 60) return { Icon: AlertTriangle, color: "text-yellow-500" };
  if (score >= 40) return { Icon: AlertTriangle, color: "text-orange-500" };
  return { Icon: XCircle, color: "text-red-500" };
}

function ScoreRing({
  score,
  status,
}: {
  score: number;
  status: ReturnType<typeof getScoreStatus>;
}) {
  const radius = 18;
  const circumference = 2 * Math.PI * radius;
  const offset = circumference - (score / 100) * circumference;

  return (
    <div className="relative flex h-12 w-12 shrink-0 items-center justify-center">
      <svg
        className="-rotate-90"
        width="48"
        height="48"
        viewBox="0 0 48 48"
        aria-hidden="true"
      >
        <circle
          cx="24"
          cy="24"
          r={radius}
          fill="none"
          stroke="currentColor"
          strokeWidth="3"
          className="text-slate-100"
        />
        <circle
          cx="24"
          cy="24"
          r={radius}
          fill="none"
          strokeWidth="3"
          strokeLinecap="round"
          strokeDasharray={circumference}
          strokeDashoffset={offset}
          className={`${status.barClass.replace("bg-", "stroke-")} transition-[stroke-dashoffset] duration-700`}
        />
      </svg>
      <span className="absolute text-xs font-bold tabular-nums text-slate-700">
        {score}
      </span>
    </div>
  );
}

export function CheckItemCard({ data }: CheckItemCardProps) {
  const [showRec, setShowRec] = useState(false);

  const isUnavailable =
    data.fail_type === "system_limit" || data.fail_type === "api_error";
  const isNotApplicable = data.fail_type === "not_applicable";

  const { Icon, color } = getStatusIcon(data.score, data.fail_type);
  const status = getScoreStatus(data.score);

  if (isUnavailable) {
    return (
      <div className="rounded-lg border border-slate-200 bg-slate-50 p-4">
        <div className="flex items-start gap-3">
          <MinusCircle
            className="h-5 w-5 shrink-0 text-slate-400 mt-0.5"
            aria-hidden="true"
          />
          <div className="flex-1 min-w-0">
            <div className="flex items-center justify-between gap-2">
              <h4 className="font-medium text-slate-500">
                {data.display_name}
              </h4>
              <span className="text-xs font-medium text-slate-400 shrink-0">
                측정 불가
              </span>
            </div>
            <p className="text-sm text-slate-400 mt-1">
              {data.fail_type === "system_limit"
                ? "이 항목은 추가 정보가 필요하여 측정하지 못했습니다. 병원명을 입력하시면 다시 측정할 수 있습니다."
                : "외부 서비스 연결 문제로 일시적으로 측정하지 못했습니다. 나중에 다시 확인해 드립니다."}
            </p>
          </div>
        </div>
      </div>
    );
  }

  if (isNotApplicable) {
    return (
      <div className="rounded-lg border border-slate-100 bg-slate-50/50 p-4">
        <div className="flex items-start gap-3">
          <MinusCircle
            className="h-5 w-5 shrink-0 text-slate-300 mt-0.5"
            aria-hidden="true"
          />
          <div className="flex-1 min-w-0">
            <h4 className="font-medium text-slate-400">{data.display_name}</h4>
            <p className="text-xs text-slate-400 mt-0.5">
              현재 단계에서는 참고 사항입니다.
            </p>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div
      className={`rounded-lg border p-4 transition-colors ${status.borderClass} ${status.bgClass}`}
    >
      <div className="flex items-start gap-3">
        <ScoreRing score={data.score} status={status} />
        <div className="flex-1 min-w-0">
          <div className="flex items-center justify-between gap-2 mb-1">
            <div className="flex items-center gap-2">
              <Icon
                className={`h-4 w-4 shrink-0 ${color}`}
                aria-hidden="true"
              />
              <h4 className="font-medium text-slate-900">
                {data.display_name}
              </h4>
            </div>
            <span
              className={`text-xs font-semibold shrink-0 ${status.colorClass}`}
            >
              {status.label}
            </span>
          </div>
          <p className="text-sm text-slate-600">{data.description}</p>
          {data.issues.length > 0 && (
            <ul className="mt-2 space-y-0.5">
              {data.issues.map((issue, i) => (
                <li
                  key={i}
                  className="flex items-start gap-1.5 text-xs text-red-600"
                >
                  <XCircle
                    className="h-3 w-3 shrink-0 mt-0.5"
                    aria-hidden="true"
                  />
                  <span>{issue}</span>
                </li>
              ))}
            </ul>
          )}
          {data.recommendation && (
            <>
              <button
                type="button"
                onClick={() => setShowRec(!showRec)}
                className="mt-2 inline-flex items-center gap-1 text-xs font-medium text-slate-500 hover:text-slate-800 focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-slate-500 rounded"
              >
                {showRec ? (
                  <>
                    접기 <ChevronUp className="h-3 w-3" aria-hidden="true" />
                  </>
                ) : (
                  <>
                    개선 방법 보기{" "}
                    <ChevronDown className="h-3 w-3" aria-hidden="true" />
                  </>
                )}
              </button>
              {showRec && (
                <div className="mt-2 rounded-md bg-white p-3 text-sm text-slate-700 border border-slate-200">
                  {data.recommendation}
                </div>
              )}
            </>
          )}
        </div>
      </div>
    </div>
  );
}
