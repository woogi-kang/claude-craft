"use client";

import { useState } from "react";
import { AlertTriangle, XCircle, ChevronDown, ChevronUp } from "lucide-react";
import type { CheckItemData } from "@/lib/report-config";

interface TopIssuesProps {
  issues: (CheckItemData & { key: string; impact: number })[];
}

function IssueCard({
  issue,
  index,
}: {
  issue: CheckItemData & { key: string; impact: number };
  index: number;
}) {
  const [expanded, setExpanded] = useState(false);
  const isUrgent = issue.score < 40;
  const borderColor = isUrgent ? "border-red-300" : "border-orange-300";
  const bgColor = isUrgent ? "bg-red-50" : "bg-orange-50";
  const iconColor = isUrgent ? "text-red-500" : "text-orange-500";
  const Icon = isUrgent ? XCircle : AlertTriangle;

  return (
    <div className={`rounded-xl border-2 ${borderColor} ${bgColor} p-4 sm:p-5`}>
      <div className="flex items-start gap-3">
        <div className="flex h-8 w-8 shrink-0 items-center justify-center rounded-full bg-white shadow-sm">
          <span className="text-sm font-bold text-slate-700">{index + 1}</span>
        </div>
        <div className="flex-1 min-w-0">
          <div className="flex items-center gap-2 mb-1">
            <Icon
              className={`h-4 w-4 shrink-0 ${iconColor}`}
              aria-hidden="true"
            />
            <h3 className="font-semibold text-slate-900 text-sm sm:text-base">
              {issue.display_name}
            </h3>
            <span className="ml-auto text-xs font-bold tabular-nums text-slate-500">
              {issue.score}점
            </span>
          </div>
          <p className="text-sm text-slate-600 mb-2">{issue.description}</p>
          {issue.issues.length > 0 && (
            <ul className="mb-2 space-y-1">
              {issue.issues.map((iss, i) => (
                <li
                  key={i}
                  className={`text-xs ${isUrgent ? "text-red-700" : "text-orange-700"}`}
                >
                  - {iss}
                </li>
              ))}
            </ul>
          )}
          <button
            type="button"
            onClick={() => setExpanded(!expanded)}
            className="inline-flex items-center gap-1 text-xs font-medium text-slate-600 hover:text-slate-900 focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-slate-500 rounded"
          >
            {expanded ? (
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
          {expanded && (
            <div className="mt-2 rounded-lg bg-white/80 p-3 text-sm text-slate-700">
              {issue.recommendation}
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

export function TopIssues({ issues }: TopIssuesProps) {
  if (issues.length === 0) return null;

  return (
    <section className="mt-8">
      <div className="flex items-center gap-2 mb-4">
        <AlertTriangle className="h-5 w-5 text-red-500" aria-hidden="true" />
        <h2 className="text-lg font-bold text-slate-900">
          핵심 문제 Top {issues.length}
        </h2>
      </div>
      <div className="grid gap-3">
        {issues.map((issue, i) => (
          <IssueCard key={issue.key} issue={issue} index={i} />
        ))}
      </div>
      <p className="mt-3 text-center text-sm font-medium text-slate-500">
        이 {issues.length}가지만 해결해도 점수가 크게 올라갑니다
      </p>
    </section>
  );
}
