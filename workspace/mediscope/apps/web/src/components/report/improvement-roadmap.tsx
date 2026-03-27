import { Clock, CalendarDays, CalendarRange, ArrowRight } from "lucide-react";
import type { CheckItemData } from "@/lib/report-config";
import { ROADMAP_PHASES } from "@/lib/report-config";

interface ImprovementRoadmapProps {
  categoryScores: Record<string, CheckItemData>;
}

const PHASE_ICONS = [Clock, CalendarDays, CalendarRange];
const PHASE_COLORS = [
  {
    bg: "bg-red-50",
    border: "border-red-200",
    badge: "bg-red-100 text-red-700",
    dot: "bg-red-400",
  },
  {
    bg: "bg-yellow-50",
    border: "border-yellow-200",
    badge: "bg-yellow-100 text-yellow-700",
    dot: "bg-yellow-400",
  },
  {
    bg: "bg-blue-50",
    border: "border-blue-200",
    badge: "bg-blue-100 text-blue-700",
    dot: "bg-blue-400",
  },
];

export function ImprovementRoadmap({
  categoryScores,
}: ImprovementRoadmapProps) {
  const phases = ROADMAP_PHASES.map((phase, idx) => {
    const actionItems = phase.items.filter((key) => {
      const item = categoryScores[key];
      if (!item) return false;
      if (
        item.fail_type === "system_limit" ||
        item.fail_type === "api_error" ||
        item.fail_type === "not_applicable"
      )
        return false;
      return item.score < 80;
    });

    return {
      ...phase,
      actionItems,
      displayNames: actionItems.map(
        (key) => categoryScores[key]?.display_name ?? key,
      ),
      idx,
    };
  }).filter((p) => p.actionItems.length > 0);

  if (phases.length === 0) return null;

  return (
    <section className="mt-10">
      <div className="flex items-center gap-2 mb-4">
        <ArrowRight className="h-5 w-5 text-slate-600" aria-hidden="true" />
        <h2 className="text-lg font-bold text-slate-900">3단계 개선 로드맵</h2>
      </div>
      <div className="grid gap-4 sm:grid-cols-3">
        {phases.map((phase) => {
          const Icon = PHASE_ICONS[phase.idx];
          const colors = PHASE_COLORS[phase.idx];
          return (
            <div
              key={phase.phase}
              className={`rounded-xl border-2 ${colors.border} ${colors.bg} p-5`}
            >
              <div className="flex items-center gap-2 mb-3">
                <Icon className="h-5 w-5 text-slate-600" aria-hidden="true" />
                <span
                  className={`text-xs font-bold rounded-full px-2.5 py-0.5 ${colors.badge}`}
                >
                  Phase {phase.phase}
                </span>
              </div>
              <h3 className="font-semibold text-slate-900 mb-1">
                {phase.label}
              </h3>
              <p className="text-xs text-slate-500 mb-3">{phase.description}</p>
              <ul className="space-y-1.5">
                {phase.displayNames.map((name, i) => (
                  <li key={i} className="flex items-center gap-2 text-sm">
                    <span
                      className={`h-1.5 w-1.5 rounded-full shrink-0 ${colors.dot}`}
                      aria-hidden="true"
                    />
                    <span className="text-slate-700">{name}</span>
                  </li>
                ))}
              </ul>
              <div className="mt-3 pt-3 border-t border-slate-200/60">
                <span className="text-xs text-slate-500">
                  {phase.actionItems.length}개 항목 개선 필요
                </span>
              </div>
            </div>
          );
        })}
      </div>
    </section>
  );
}
