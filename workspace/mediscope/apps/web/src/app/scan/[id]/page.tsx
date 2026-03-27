"use client";

import { useEffect, useRef, useState } from "react";
import { useParams, useRouter } from "next/navigation";
import { useQuery } from "@tanstack/react-query";
import { motion, AnimatePresence } from "framer-motion";
import {
  CheckCircle2,
  AlertCircle,
  ArrowRight,
  Globe,
  Gauge,
  Search,
  Languages,
  BarChart3,
} from "lucide-react";
import type { Audit, AuditStatus, Category, Grade } from "@/lib/types";
import { getGrade, CATEGORY_LABELS } from "@/lib/types";

/* ────────────────────────────────────────────
 * Scan phases — 24 check items grouped into 5 stages
 * ──────────────────────────────────────────── */

interface ScanPhase {
  key: Category;
  label: string;
  icon: typeof Globe;
  items: string[];
}

const SCAN_PHASES: ScanPhase[] = [
  {
    key: "technical_seo",
    label: "기술 SEO 분석",
    icon: Globe,
    items: [
      "robots_txt",
      "sitemap",
      "meta_tags",
      "headings",
      "canonical",
      "url_structure",
      "images_alt",
      "links",
      "errors_404",
      "https",
    ],
  },
  {
    key: "performance",
    label: "성능 측정",
    icon: Gauge,
    items: ["lcp", "inp", "cls", "performance_score", "mobile"],
  },
  {
    key: "geo_aeo",
    label: "GEO/AEO 진단",
    icon: Search,
    items: [
      "structured_data",
      "faq_content",
      "eeat_signals",
      "content_clarity",
      "ai_search_mention",
    ],
  },
  {
    key: "multilingual",
    label: "다국어 지원 확인",
    icon: Languages,
    items: ["multilingual_pages", "hreflang", "overseas_channels"],
  },
  {
    key: "competitiveness",
    label: "해외 검색 벤치마크",
    icon: BarChart3,
    items: ["international_search"],
  },
];

const TOTAL_ITEMS = SCAN_PHASES.reduce((s, p) => s + p.items.length, 0);

/* ────────────────────────────────────────────
 * Scan log item labels
 * ──────────────────────────────────────────── */

const LOG_LABELS: Record<string, string> = {
  robots_txt: "robots.txt 확인",
  sitemap: "sitemap.xml 분석",
  meta_tags: "메타 태그 분석",
  headings: "Heading 구조 분석",
  canonical: "Canonical URL 확인",
  url_structure: "URL 구조 분석",
  images_alt: "이미지 ALT 속성 확인",
  links: "내부 링크 분석",
  errors_404: "404/리다이렉트 확인",
  https: "HTTPS 보안 확인",
  lcp: "LCP 측정",
  inp: "INP 측정",
  cls: "CLS 측정",
  performance_score: "종합 성능 점수 계산",
  mobile: "모바일 반응형 확인",
  structured_data: "구조화 데이터 확인",
  faq_content: "FAQ 콘텐츠 분석",
  eeat_signals: "E-E-A-T 신호 분석",
  content_clarity: "콘텐츠 명확성 검증",
  ai_search_mention: "AI 검색 노출 확인",
  multilingual_pages: "다국어 페이지 확인",
  hreflang: "hreflang 태그 분석",
  overseas_channels: "해외 채널 확인",
  international_search: "국제 검색 노출 벤치마크",
};

/* ────────────────────────────────────────────
 * Utility: progress from scores
 * ──────────────────────────────────────────── */

function getProgress(status: AuditStatus, scores: Record<string, number>) {
  if (status === "completed") return 100;
  if (status === "failed") return 0;
  const completed = Object.keys(scores).length;
  return Math.min(95, (completed / SCAN_PHASES.length) * 90 + 5);
}

/* ────────────────────────────────────────────
 * Hook: simulate scan log entries from score changes
 * ──────────────────────────────────────────── */

interface LogEntry {
  key: string;
  label: string;
  status: "done" | "active" | "pending";
  elapsed?: string;
}

function useScanLog(
  scores: Record<string, number>,
  status: AuditStatus,
): LogEntry[] {
  const [entries, setEntries] = useState<LogEntry[]>([]);
  const prevScoresRef = useRef<Set<string>>(new Set());
  const timersRef = useRef<Map<string, number>>(new Map());

  useEffect(() => {
    const allItems = SCAN_PHASES.flatMap((p) => p.items);
    const prevKeys = prevScoresRef.current;

    // Find the current phase based on completed scores
    let currentPhaseIdx = 0;
    for (let i = 0; i < SCAN_PHASES.length; i++) {
      if (scores[SCAN_PHASES[i].key] !== undefined) {
        currentPhaseIdx = i + 1;
      }
    }

    // Build log entries
    const newEntries: LogEntry[] = [];
    let foundActive = false;

    for (const item of allItems) {
      const phaseIdx = SCAN_PHASES.findIndex((p) => p.items.includes(item));
      const phaseCompleted = scores[SCAN_PHASES[phaseIdx].key] !== undefined;

      if (phaseCompleted) {
        // Track elapsed time for newly completed items
        if (
          !prevKeys.has(SCAN_PHASES[phaseIdx].key) &&
          !timersRef.current.has(item)
        ) {
          timersRef.current.set(item, 0.1 + Math.random() * 0.8);
        }
        newEntries.push({
          key: item,
          label: LOG_LABELS[item] ?? item,
          status: "done",
          elapsed: `${(timersRef.current.get(item) ?? 0.3).toFixed(1)}s`,
        });
      } else if (
        phaseIdx === currentPhaseIdx &&
        !foundActive &&
        status === "scanning"
      ) {
        // First item in the active phase
        newEntries.push({
          key: item,
          label: LOG_LABELS[item] ?? item,
          status: "active",
        });
        foundActive = true;
      } else if (phaseIdx >= currentPhaseIdx) {
        newEntries.push({
          key: item,
          label: LOG_LABELS[item] ?? item,
          status: "pending",
        });
      }
    }

    prevScoresRef.current = new Set(Object.keys(scores));
    setEntries(newEntries);
  }, [scores, status]);

  return entries;
}

/* ────────────────────────────────────────────
 * Hook: animated counter
 * ──────────────────────────────────────────── */

function useAnimatedNumber(target: number, duration = 1200) {
  const [value, setValue] = useState(0);
  const frameRef = useRef<number>(0);

  useEffect(() => {
    const start = value;
    const diff = target - start;
    if (diff === 0) return;

    const startTime = performance.now();
    function animate(now: number) {
      const elapsed = now - startTime;
      const t = Math.min(elapsed / duration, 1);
      // Ease-out cubic
      const eased = 1 - Math.pow(1 - t, 3);
      setValue(Math.round(start + diff * eased));
      if (t < 1) frameRef.current = requestAnimationFrame(animate);
    }
    frameRef.current = requestAnimationFrame(animate);
    return () => {
      if (frameRef.current) cancelAnimationFrame(frameRef.current);
    };
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [target, duration]);

  return value;
}

/* ────────────────────────────────────────────
 * Circular Scan Gauge (SVG)
 * ──────────────────────────────────────────── */

function ScanGauge({
  progress,
  status,
  finalScore,
  grade,
}: {
  progress: number;
  status: AuditStatus;
  finalScore: number | null;
  grade: Grade | null;
}) {
  const size = 220;
  const strokeWidth = 6;
  const radius = (size - strokeWidth * 2 - 20) / 2;
  const circumference = 2 * Math.PI * radius;
  const displayValue = useAnimatedNumber(
    status === "completed" && finalScore !== null
      ? finalScore
      : Math.round(progress),
    status === "completed" ? 2000 : 800,
  );
  const offset = circumference - (displayValue / 100) * circumference;

  const outerRadius = radius + 14;

  const gradeColors: Record<Grade, string> = {
    A: "#22c55e",
    B: "#3b82f6",
    C: "#eab308",
    D: "#f97316",
    F: "#ef4444",
  };

  const accentColor =
    status === "completed" && grade ? gradeColors[grade] : "#38bdf8";

  return (
    <div className="relative flex items-center justify-center">
      {/* Pulse rings */}
      {status === "scanning" && (
        <>
          <div
            className="scan-pulse-ring absolute rounded-full"
            style={{ width: size + 40, height: size + 40 }}
          />
          <div
            className="scan-pulse-ring absolute rounded-full"
            style={{
              width: size + 70,
              height: size + 70,
              animationDelay: "0.6s",
            }}
          />
        </>
      )}

      <svg
        width={size}
        height={size}
        className="drop-shadow-lg"
        role="img"
        aria-label={`스캔 진행률 ${displayValue}%`}
      >
        {/* Outer rotating dashed ring */}
        {status === "scanning" && (
          <circle
            cx={size / 2}
            cy={size / 2}
            r={outerRadius}
            fill="none"
            stroke="#38bdf8"
            strokeWidth={1.5}
            strokeDasharray="4 8"
            opacity={0.4}
            className="scan-rotate-ring"
          />
        )}

        {/* Background track */}
        <circle
          cx={size / 2}
          cy={size / 2}
          r={radius}
          fill="none"
          stroke="currentColor"
          strokeWidth={strokeWidth}
          className="text-slate-700/50"
        />

        {/* Progress arc */}
        <circle
          cx={size / 2}
          cy={size / 2}
          r={radius}
          fill="none"
          stroke={accentColor}
          strokeWidth={strokeWidth + 1}
          strokeDasharray={circumference}
          strokeDashoffset={offset}
          strokeLinecap="round"
          transform={`rotate(-90 ${size / 2} ${size / 2})`}
          className="transition-[stroke-dashoffset] duration-700 ease-out"
          style={{ filter: `drop-shadow(0 0 6px ${accentColor}60)` }}
        />

        {/* Glow dot at arc tip */}
        {status === "scanning" && (
          <circle
            cx={
              size / 2 +
              radius *
                Math.cos(((displayValue / 100) * 360 - 90) * (Math.PI / 180))
            }
            cy={
              size / 2 +
              radius *
                Math.sin(((displayValue / 100) * 360 - 90) * (Math.PI / 180))
            }
            r={4}
            fill="#38bdf8"
            className="scan-glow-dot"
          />
        )}
      </svg>

      {/* Center text */}
      <div className="absolute flex flex-col items-center justify-center">
        {status === "completed" && grade ? (
          <motion.div
            initial={{ scale: 0, opacity: 0 }}
            animate={{ scale: 1, opacity: 1 }}
            transition={{
              type: "spring",
              stiffness: 200,
              damping: 15,
              delay: 0.3,
            }}
            className="flex flex-col items-center"
          >
            <span
              className="font-scan-display text-5xl font-black tracking-tight"
              style={{ color: accentColor }}
            >
              {displayValue}
            </span>
            <span
              className="mt-1 rounded-md px-3 py-0.5 text-xs font-bold tracking-widest"
              style={{
                backgroundColor: `${accentColor}20`,
                color: accentColor,
              }}
            >
              Grade {grade}
            </span>
          </motion.div>
        ) : (
          <>
            <span className="font-scan-display text-4xl font-black tracking-tight text-slate-100">
              {displayValue}
              <span className="text-lg text-slate-400">%</span>
            </span>
            <span className="mt-1 text-xs font-medium tracking-wider text-slate-500 uppercase">
              {status === "scanning" ? "scanning" : "preparing"}
            </span>
          </>
        )}
      </div>
    </div>
  );
}

/* ────────────────────────────────────────────
 * Step Indicator (horizontal / vertical on mobile)
 * ──────────────────────────────────────────── */

function StepIndicator({
  scores,
  status,
}: {
  scores: Record<string, number>;
  status: AuditStatus;
}) {
  // Determine phase states
  const phases = SCAN_PHASES.map((phase, i) => {
    const done = scores[phase.key] !== undefined;
    const prevDone = i === 0 || scores[SCAN_PHASES[i - 1].key] !== undefined;
    const active = !done && prevDone && status === "scanning";
    return { ...phase, done, active };
  });

  return (
    <div className="w-full">
      {/* Desktop: horizontal */}
      <div
        className="hidden items-center justify-between sm:flex"
        role="list"
        aria-label="스캔 진행 단계"
      >
        {phases.map((phase, i) => {
          const Icon = phase.icon;
          return (
            <div key={phase.key} className="flex items-center" role="listitem">
              {/* Step circle */}
              <div className="flex flex-col items-center gap-1.5">
                <div
                  className={`relative flex h-10 w-10 items-center justify-center rounded-full border-2 transition-all duration-500 ${
                    phase.done
                      ? "border-cyan-400 bg-cyan-400/10"
                      : phase.active
                        ? "border-cyan-400/60 bg-cyan-400/5"
                        : "border-slate-700 bg-slate-800/50"
                  }`}
                >
                  {phase.active && (
                    <span className="absolute inset-0 rounded-full border-2 border-cyan-400/40 scan-step-pulse" />
                  )}
                  <Icon
                    className={`h-4 w-4 ${
                      phase.done
                        ? "text-cyan-400"
                        : phase.active
                          ? "text-cyan-300"
                          : "text-slate-600"
                    }`}
                  />
                </div>
                <span
                  className={`text-[11px] font-medium ${
                    phase.done
                      ? "text-slate-300"
                      : phase.active
                        ? "text-cyan-300"
                        : "text-slate-600"
                  }`}
                >
                  {CATEGORY_LABELS[phase.key]}
                </span>
              </div>

              {/* Connector line */}
              {i < phases.length - 1 && (
                <div className="mx-2 h-[2px] w-8 lg:w-14">
                  <div
                    className={`h-full transition-all duration-700 ${
                      phases[i + 1].done || phases[i + 1].active
                        ? "bg-cyan-400/50"
                        : "bg-slate-700"
                    }`}
                    style={{
                      backgroundImage:
                        !phases[i + 1].done && !phases[i + 1].active
                          ? "repeating-linear-gradient(90deg, transparent, transparent 3px, var(--color-slate-700, #334155) 3px, var(--color-slate-700, #334155) 7px)"
                          : undefined,
                    }}
                  />
                </div>
              )}
            </div>
          );
        })}
      </div>

      {/* Mobile: vertical */}
      <div
        className="flex flex-col gap-3 sm:hidden"
        role="list"
        aria-label="스캔 진행 단계"
      >
        {phases.map((phase) => {
          const Icon = phase.icon;
          return (
            <div
              key={phase.key}
              className="flex items-center gap-3"
              role="listitem"
            >
              <div
                className={`flex h-8 w-8 items-center justify-center rounded-full border-2 transition-all duration-500 ${
                  phase.done
                    ? "border-cyan-400 bg-cyan-400/10"
                    : phase.active
                      ? "border-cyan-400/60 bg-cyan-400/5"
                      : "border-slate-700 bg-slate-800/50"
                }`}
              >
                {phase.active && (
                  <span className="absolute h-8 w-8 rounded-full border-2 border-cyan-400/40 scan-step-pulse" />
                )}
                <Icon
                  className={`h-3.5 w-3.5 ${
                    phase.done
                      ? "text-cyan-400"
                      : phase.active
                        ? "text-cyan-300"
                        : "text-slate-600"
                  }`}
                />
              </div>
              <span
                className={`text-sm font-medium ${
                  phase.done
                    ? "text-slate-300"
                    : phase.active
                      ? "text-cyan-300"
                      : "text-slate-600"
                }`}
              >
                {phase.label}
              </span>
              {phase.done && (
                <CheckCircle2 className="ml-auto h-4 w-4 text-emerald-400" />
              )}
            </div>
          );
        })}
      </div>
    </div>
  );
}

/* ────────────────────────────────────────────
 * Terminal-style Scan Log
 * ──────────────────────────────────────────── */

function ScanLog({ entries }: { entries: LogEntry[] }) {
  const scrollRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (scrollRef.current) {
      scrollRef.current.scrollTop = scrollRef.current.scrollHeight;
    }
  }, [entries]);

  const visibleEntries = entries
    .filter((e) => e.status !== "pending")
    .slice(-10);
  const pendingCount = entries.filter((e) => e.status === "pending").length;

  return (
    <div className="w-full overflow-hidden rounded-lg border border-slate-700/60 bg-slate-900/80 backdrop-blur">
      {/* Terminal header */}
      <div className="flex items-center gap-1.5 border-b border-slate-700/60 px-3 py-2">
        <span className="h-2.5 w-2.5 rounded-full bg-red-500/70" />
        <span className="h-2.5 w-2.5 rounded-full bg-yellow-500/70" />
        <span className="h-2.5 w-2.5 rounded-full bg-green-500/70" />
        <span className="ml-2 text-[10px] font-medium tracking-wider text-slate-500 uppercase">
          scan log
        </span>
      </div>

      {/* Log entries */}
      <div
        ref={scrollRef}
        className="max-h-52 overflow-y-auto px-3 py-2 font-mono text-[13px] leading-relaxed sm:max-h-64"
      >
        <AnimatePresence mode="popLayout">
          {visibleEntries.map((entry) => (
            <motion.div
              key={entry.key}
              initial={{ opacity: 0, x: -8 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ duration: 0.3 }}
              className="flex items-center gap-2 py-0.5"
            >
              {entry.status === "done" ? (
                <span className="text-emerald-400">&#10003;</span>
              ) : (
                <span className="text-cyan-400 scan-blink">&#9656;</span>
              )}
              <span
                className={
                  entry.status === "done" ? "text-slate-400" : "text-slate-200"
                }
              >
                {entry.label}
                {entry.status === "active" && (
                  <span className="text-cyan-400">...</span>
                )}
              </span>
              {entry.elapsed && (
                <span className="ml-auto tabular-nums text-slate-600">
                  {entry.elapsed}
                </span>
              )}
            </motion.div>
          ))}
        </AnimatePresence>

        {pendingCount > 0 && (
          <div className="mt-1 text-slate-600">
            <span className="mr-2">░</span>
            {pendingCount}개 항목 대기 중
          </div>
        )}
      </div>
    </div>
  );
}

/* ────────────────────────────────────────────
 * Stats Counter Cards
 * ──────────────────────────────────────────── */

function StatsCounters({ scores }: { scores: Record<string, number> }) {
  const completedPhases = Object.keys(scores).length;
  const completedItems = SCAN_PHASES.reduce((count, phase) => {
    if (scores[phase.key] !== undefined) return count + phase.items.length;
    return count;
  }, 0);

  const issueCount = Object.values(scores).filter((s) => s < 60).length;

  const stats = [
    {
      label: "분석 항목",
      value: useAnimatedNumber(completedItems, 600),
      suffix: `/${TOTAL_ITEMS}`,
    },
    {
      label: "발견 이슈",
      value: useAnimatedNumber(issueCount, 600),
      suffix: "개",
      warn: issueCount > 0,
    },
    {
      label: "완료 단계",
      value: useAnimatedNumber(completedPhases, 600),
      suffix: `/${SCAN_PHASES.length}`,
    },
  ];

  return (
    <div className="grid w-full grid-cols-3 gap-3">
      {stats.map((stat) => (
        <div
          key={stat.label}
          className="rounded-lg border border-slate-700/50 bg-slate-800/40 px-3 py-3 text-center backdrop-blur"
        >
          <div className="text-[11px] font-medium tracking-wider text-slate-500 uppercase">
            {stat.label}
          </div>
          <div className="mt-1 font-scan-display text-xl font-bold tabular-nums text-slate-200">
            <motion.span
              key={stat.value}
              initial={{ opacity: 0, y: 6 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.3 }}
              className={stat.warn ? "text-amber-400" : ""}
            >
              {stat.value}
            </motion.span>
            <span className="text-sm text-slate-600">{stat.suffix}</span>
          </div>
        </div>
      ))}
    </div>
  );
}

/* ────────────────────────────────────────────
 * Completion Overlay
 * ──────────────────────────────────────────── */

function CompletionOverlay({
  totalScore,
  grade,
  id,
}: {
  totalScore: number;
  grade: Grade;
  id: string;
}) {
  const router = useRouter();
  const gradeColors: Record<Grade, string> = {
    A: "#22c55e",
    B: "#3b82f6",
    C: "#eab308",
    D: "#f97316",
    F: "#ef4444",
  };
  const color = gradeColors[grade];

  return (
    <motion.div
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      className="fixed inset-0 z-50 flex items-center justify-center bg-slate-950/80 backdrop-blur-sm"
    >
      <motion.div
        initial={{ scale: 0.8, opacity: 0 }}
        animate={{ scale: 1, opacity: 1 }}
        transition={{ type: "spring", stiffness: 180, damping: 18, delay: 0.2 }}
        className="flex flex-col items-center gap-4 rounded-2xl border border-slate-700/50 bg-slate-900/90 px-10 py-10 backdrop-blur"
      >
        <p className="text-sm font-medium tracking-wider text-slate-400 uppercase">
          분석 완료
        </p>
        <div
          className="font-scan-display text-6xl font-black"
          style={{ color }}
        >
          {totalScore}
        </div>
        <motion.span
          initial={{ scale: 0 }}
          animate={{ scale: 1 }}
          transition={{ delay: 0.6, type: "spring", stiffness: 300 }}
          className="rounded-lg px-5 py-1.5 text-lg font-bold tracking-widest"
          style={{ backgroundColor: `${color}20`, color }}
        >
          Grade {grade}
        </motion.span>
        <button
          onClick={() => router.replace(`/report/${id}`)}
          className="mt-4 flex items-center gap-2 rounded-lg bg-cyan-500 px-6 py-2.5 text-sm font-semibold text-white transition-colors hover:bg-cyan-400 focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-cyan-400"
          aria-label="리포트 보기"
        >
          리포트 보기
          <ArrowRight className="h-4 w-4" />
        </button>
      </motion.div>
    </motion.div>
  );
}

/* ────────────────────────────────────────────
 * Main Page Component
 * ──────────────────────────────────────────── */

export default function ScanPage() {
  const { id } = useParams<{ id: string }>();
  const router = useRouter();
  const [showCompletion, setShowCompletion] = useState(false);

  const { data: audit } = useQuery<Audit>({
    queryKey: ["audit", id],
    queryFn: async () => {
      const res = await fetch(`/api/audits/${id}`);
      if (!res.ok) throw new Error("Failed to fetch audit");
      return res.json();
    },
    refetchInterval: (query) => {
      const s = query.state.data?.status;
      if (s === "completed" || s === "failed") return false;
      return 2000;
    },
  });

  const status = audit?.status ?? "pending";
  const scores = (audit?.scores ?? {}) as Record<string, number>;
  const progress = getProgress(status, scores);
  const logEntries = useScanLog(scores, status);

  // Handle completion
  useEffect(() => {
    if (status === "completed" && audit) {
      setShowCompletion(true);
      const timer = setTimeout(() => {
        router.replace(`/report/${id}`);
      }, 4000);
      return () => clearTimeout(timer);
    }
  }, [status, audit, router, id]);

  const totalScore = audit?.total_score ?? 0;
  const grade =
    audit?.grade ?? (status === "completed" ? getGrade(totalScore) : null);

  return (
    <div className="scan-page-bg relative flex min-h-screen items-center justify-center overflow-hidden px-4 py-8">
      {/* Ambient background effects */}
      <div
        className="pointer-events-none absolute inset-0 overflow-hidden"
        aria-hidden="true"
      >
        <div className="scan-ambient-orb absolute -left-32 top-1/4 h-96 w-96 rounded-full bg-cyan-500/5 blur-3xl" />
        <div
          className="scan-ambient-orb absolute -right-32 bottom-1/4 h-96 w-96 rounded-full bg-indigo-500/5 blur-3xl"
          style={{ animationDelay: "3s" }}
        />
      </div>

      <div className="relative z-10 flex w-full max-w-xl flex-col items-center gap-8">
        {/* Header */}
        <div className="text-center">
          <h1 className="font-scan-display text-xl font-bold tracking-tight text-slate-100 sm:text-2xl">
            {status === "failed" ? "진단 실패" : "사이트 진단 진행 중"}
          </h1>
          {audit?.url && (
            <p className="mt-1.5 truncate text-sm text-slate-500">
              {audit.url}
            </p>
          )}
        </div>

        {/* Circular Gauge */}
        <ScanGauge
          progress={progress}
          status={status}
          finalScore={totalScore}
          grade={grade}
        />

        {/* Step Indicator */}
        <StepIndicator scores={scores} status={status} />

        {/* Stats Counters */}
        <StatsCounters scores={scores} />

        {/* Scan Log */}
        {status === "scanning" && <ScanLog entries={logEntries} />}

        {/* Error state */}
        {status === "failed" && (
          <div className="flex items-center gap-2 rounded-lg border border-red-900/40 bg-red-950/30 px-4 py-3 text-sm text-red-400">
            <AlertCircle className="h-4 w-4 shrink-0" />
            진단 중 오류가 발생했습니다. 다시 시도해주세요.
          </div>
        )}
      </div>

      {/* Completion overlay */}
      <AnimatePresence>
        {showCompletion && audit && grade && (
          <CompletionOverlay totalScore={totalScore} grade={grade} id={id} />
        )}
      </AnimatePresence>
    </div>
  );
}
