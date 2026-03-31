"use client";

import { useState } from "react";
import { motion, AnimatePresence } from "framer-motion";
import {
  Search,
  Shield,
  Scale,
  CalendarCheck,
  ChevronRight,
  AlertTriangle,
  X,
} from "lucide-react";
import type { Grade } from "@/lib/types";
import { getGrade } from "@/lib/types";

interface JourneyStage {
  score: number;
  grade: string;
  display_name: string;
  icon: string;
  description: string;
  weakest_check: string | null;
  recommendation: string;
}

interface PatientJourneyData {
  stages: Record<string, JourneyStage>;
  weakest_stage: string | null;
  strongest_stage: string | null;
  overall_journey_score: number;
  narrative: string;
}

interface PatientJourneyFunnelProps {
  data: PatientJourneyData;
}

const STAGE_ORDER = ["discovery", "trust", "comparison", "booking"] as const;

const STAGE_ICONS: Record<string, typeof Search> = {
  search: Search,
  shield: Shield,
  scale: Scale,
  calendar: CalendarCheck,
};

function getScoreColor(score: number) {
  if (score >= 80)
    return {
      bg: "bg-green-50",
      border: "border-green-300",
      text: "text-green-700",
      bar: "bg-green-500",
      arrow: "text-green-400",
    };
  if (score >= 60)
    return {
      bg: "bg-blue-50",
      border: "border-blue-300",
      text: "text-blue-700",
      bar: "bg-blue-500",
      arrow: "text-blue-400",
    };
  if (score >= 40)
    return {
      bg: "bg-yellow-50",
      border: "border-yellow-300",
      text: "text-yellow-700",
      bar: "bg-yellow-500",
      arrow: "text-yellow-400",
    };
  if (score >= 20)
    return {
      bg: "bg-orange-50",
      border: "border-orange-300",
      text: "text-orange-700",
      bar: "bg-orange-500",
      arrow: "text-orange-400",
    };
  return {
    bg: "bg-red-50",
    border: "border-red-300",
    text: "text-red-700",
    bar: "bg-red-500",
    arrow: "text-red-400",
  };
}

const GRADE_BADGE: Record<Grade, string> = {
  A: "bg-green-100 text-green-800 border-green-300",
  B: "bg-blue-100 text-blue-800 border-blue-300",
  C: "bg-yellow-100 text-yellow-800 border-yellow-300",
  D: "bg-orange-100 text-orange-800 border-orange-300",
  F: "bg-red-100 text-red-800 border-red-300",
};

function StageCard({
  stage,
  stageKey,
  isWeakest,
  index,
  onSelect,
}: {
  stage: JourneyStage;
  stageKey: string;
  isWeakest: boolean;
  index: number;
  onSelect: () => void;
}) {
  const colors = getScoreColor(stage.score);
  const Icon = STAGE_ICONS[stage.icon] ?? Search;
  const grade = getGrade(stage.score);

  return (
    <motion.button
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ delay: index * 0.1, duration: 0.4 }}
      onClick={onSelect}
      className={`relative flex flex-col items-center rounded-xl border-2 p-4 transition-shadow hover:shadow-md cursor-pointer w-full ${colors.bg} ${isWeakest ? "border-red-400 ring-2 ring-red-200" : colors.border}`}
    >
      {isWeakest && (
        <span className="absolute -top-2.5 left-1/2 -translate-x-1/2 rounded-full bg-red-500 px-2 py-0.5 text-[10px] font-bold text-white whitespace-nowrap">
          가장 취약
        </span>
      )}
      <div
        className={`flex h-10 w-10 items-center justify-center rounded-full ${colors.bg} ${colors.text}`}
      >
        <Icon className="h-5 w-5" />
      </div>
      <p className="mt-2 text-xs font-medium text-slate-500">
        {stage.display_name}
      </p>
      <p className={`mt-1 text-2xl font-bold tabular-nums ${colors.text}`}>
        {stage.score}
      </p>
      <span
        className={`mt-1 inline-flex items-center rounded border px-1.5 py-0.5 text-[10px] font-bold ${GRADE_BADGE[grade]}`}
      >
        {grade}
      </span>
    </motion.button>
  );
}

function StageDetailPopup({
  stage,
  onClose,
}: {
  stage: JourneyStage;
  onClose: () => void;
}) {
  const colors = getScoreColor(stage.score);

  return (
    <motion.div
      initial={{ opacity: 0, y: 10 }}
      animate={{ opacity: 1, y: 0 }}
      exit={{ opacity: 0, y: 10 }}
      className="mt-4 rounded-xl border border-slate-200 bg-white p-5 shadow-lg"
    >
      <div className="flex items-start justify-between">
        <div>
          <h4 className="text-base font-bold text-slate-900">
            {stage.display_name} 단계
          </h4>
          <p className="mt-0.5 text-sm text-slate-500">{stage.description}</p>
        </div>
        <button
          onClick={onClose}
          className="rounded-md p-1 text-slate-400 hover:bg-slate-100 hover:text-slate-600"
        >
          <X className="h-4 w-4" />
        </button>
      </div>

      <div className="mt-4 space-y-3">
        <div>
          <div className="flex items-center justify-between text-sm">
            <span className="text-slate-600">점수</span>
            <span className={`font-bold ${colors.text}`}>
              {stage.score}/100
            </span>
          </div>
          <div className="mt-1 h-2 w-full rounded-full bg-slate-100">
            <motion.div
              initial={{ width: 0 }}
              animate={{ width: `${stage.score}%` }}
              transition={{ duration: 0.6, ease: "easeOut" }}
              className={`h-full rounded-full ${colors.bar}`}
            />
          </div>
        </div>

        {stage.weakest_check && (
          <div className="flex items-start gap-2 rounded-lg bg-amber-50 p-3">
            <AlertTriangle className="mt-0.5 h-4 w-4 flex-shrink-0 text-amber-500" />
            <div>
              <p className="text-xs font-medium text-amber-800">
                가장 취약한 항목
              </p>
              <p className="text-sm text-amber-700">{stage.weakest_check}</p>
            </div>
          </div>
        )}

        <div className="rounded-lg bg-slate-50 p-3">
          <p className="text-xs font-medium text-slate-500 mb-1">추천사항</p>
          <p className="text-sm text-slate-700">{stage.recommendation}</p>
        </div>
      </div>
    </motion.div>
  );
}

export function PatientJourneyFunnel({ data }: PatientJourneyFunnelProps) {
  const [selectedStage, setSelectedStage] = useState<string | null>(null);

  if (!data || !data.stages || Object.keys(data.stages).length === 0) {
    return null;
  }

  const selectedStageData = selectedStage ? data.stages[selectedStage] : null;

  return (
    <section className="mt-10">
      <div className="mb-4">
        <h2 className="text-lg font-bold text-slate-900">환자 여정 분석</h2>
        <p className="mt-1 text-sm text-slate-500">
          환자가 병원을 발견하고 예약하기까지 4단계 여정의 디지털 준비도
        </p>
      </div>

      <div className="rounded-xl border border-slate-200 bg-white p-5 sm:p-6">
        {/* Funnel: horizontal on desktop, vertical on mobile */}
        <div className="flex flex-col sm:flex-row items-center gap-2 sm:gap-0">
          {STAGE_ORDER.map((key, idx) => {
            const stage = data.stages[key];
            if (!stage) return null;
            const isWeakest = data.weakest_stage === key;
            const colors = getScoreColor(stage.score);

            return (
              <div
                key={key}
                className="flex flex-col sm:flex-row items-center w-full sm:w-auto sm:flex-1"
              >
                <StageCard
                  stage={stage}
                  stageKey={key}
                  isWeakest={isWeakest}
                  index={idx}
                  onSelect={() =>
                    setSelectedStage(selectedStage === key ? null : key)
                  }
                />
                {idx < STAGE_ORDER.length - 1 && (
                  <ChevronRight
                    className={`hidden sm:block mx-1 h-5 w-5 flex-shrink-0 ${colors.arrow}`}
                  />
                )}
              </div>
            );
          })}
        </div>

        {/* Overall score + narrative */}
        <div className="mt-5 flex flex-col sm:flex-row items-center gap-3 rounded-lg bg-slate-50 px-4 py-3">
          <div className="flex items-center gap-2">
            <span className="text-sm font-medium text-slate-500">
              여정 종합
            </span>
            <span className="text-xl font-bold tabular-nums text-slate-900">
              {data.overall_journey_score}
            </span>
            <span className="text-xs text-slate-400">/100</span>
          </div>
          <p className="text-sm text-slate-600 text-center sm:text-left">
            {data.narrative}
          </p>
        </div>

        {/* Detail popup */}
        <AnimatePresence>
          {selectedStageData && selectedStage && (
            <StageDetailPopup
              key={selectedStage}
              stage={selectedStageData}
              onClose={() => setSelectedStage(null)}
            />
          )}
        </AnimatePresence>
      </div>
    </section>
  );
}
