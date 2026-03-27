"use client";

import { CheckCircle, AlertTriangle, XCircle } from "lucide-react";
import type { Grade } from "@/lib/types";
import {
  GRADE_SUMMARIES,
  GRADE_BG_COLORS,
  GRADE_RING_COLORS,
  GRADE_TEXT_COLORS,
  GRADE_BADGE_COLORS,
} from "@/lib/report-config";

interface ScoreHeroProps {
  totalScore: number;
  grade: Grade;
  passCount: number;
  warnCount: number;
  failCount: number;
}

function ScoreGauge({ score, grade }: { score: number; grade: Grade }) {
  const circumference = 2 * Math.PI * 54;
  const offset = circumference - (score / 100) * circumference;

  return (
    <div className="relative flex h-40 w-40 items-center justify-center">
      <svg
        className="-rotate-90"
        width="160"
        height="160"
        viewBox="0 0 120 120"
        aria-hidden="true"
      >
        <circle
          cx="60"
          cy="60"
          r="54"
          fill="none"
          stroke="currentColor"
          strokeWidth="8"
          className="text-slate-100"
        />
        <circle
          cx="60"
          cy="60"
          r="54"
          fill="none"
          strokeWidth="8"
          strokeLinecap="round"
          strokeDasharray={circumference}
          strokeDashoffset={offset}
          className={`${GRADE_RING_COLORS[grade]} transition-[stroke-dashoffset] duration-1000 ease-out`}
        />
      </svg>
      <div className="absolute inset-0 flex flex-col items-center justify-center">
        <span
          className={`text-5xl font-extrabold tabular-nums tracking-tight ${GRADE_TEXT_COLORS[grade]}`}
        >
          {score}
        </span>
        <span className="text-xs text-slate-400 mt-0.5">/100</span>
      </div>
    </div>
  );
}

function StatusCounter({
  icon: Icon,
  count,
  label,
  colorClass,
}: {
  icon: typeof CheckCircle;
  count: number;
  label: string;
  colorClass: string;
}) {
  return (
    <div className="flex items-center gap-2">
      <Icon className={`h-5 w-5 ${colorClass}`} aria-hidden="true" />
      <div>
        <span className="text-lg font-bold tabular-nums">{count}</span>
        <span className="text-sm text-slate-500 ml-1">{label}</span>
      </div>
    </div>
  );
}

export function ScoreHero({
  totalScore,
  grade,
  passCount,
  warnCount,
  failCount,
}: ScoreHeroProps) {
  return (
    <div
      className={`rounded-2xl border-2 p-6 sm:p-8 ${GRADE_BG_COLORS[grade]}`}
    >
      <div className="flex flex-col sm:flex-row items-center gap-6 sm:gap-10">
        <ScoreGauge score={totalScore} grade={grade} />
        <div className="flex-1 text-center sm:text-left">
          <div className="flex items-center justify-center sm:justify-start gap-3 mb-3">
            <h2 className="text-xl font-bold text-slate-900">종합 점수</h2>
            <span
              className={`inline-flex items-center rounded-md border px-3 py-1 text-sm font-bold ${GRADE_BADGE_COLORS[grade]}`}
            >
              {grade}등급
            </span>
          </div>
          <p
            className={`text-base font-medium mb-5 ${GRADE_TEXT_COLORS[grade]}`}
          >
            {GRADE_SUMMARIES[grade]}
          </p>
          <div className="flex items-center justify-center sm:justify-start gap-6">
            <StatusCounter
              icon={CheckCircle}
              count={passCount}
              label="양호"
              colorClass="text-green-500"
            />
            <StatusCounter
              icon={AlertTriangle}
              count={warnCount}
              label="주의"
              colorClass="text-yellow-500"
            />
            <StatusCounter
              icon={XCircle}
              count={failCount}
              label="심각"
              colorClass="text-red-500"
            />
          </div>
        </div>
      </div>
    </div>
  );
}
