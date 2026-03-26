"use client";

import { useEffect } from "react";
import { useParams, useRouter } from "next/navigation";
import { useQuery } from "@tanstack/react-query";
import { Progress } from "@/components/ui/progress";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { CheckCircle2, Circle, Loader2 } from "lucide-react";
import type { Audit, AuditStatus } from "@/lib/types";

const SCAN_STEPS = [
  { key: "technical_seo", label: "기술 SEO 분석" },
  { key: "performance", label: "성능 측정" },
  { key: "geo_aeo", label: "GEO/AEO 진단" },
  { key: "multilingual", label: "다국어 지원 확인" },
  { key: "competitiveness", label: "경쟁사 벤치마크" },
];

function getProgress(status: AuditStatus, scores: Record<string, number>) {
  if (status === "completed") return 100;
  if (status === "failed") return 0;
  const completed = Object.keys(scores).length;
  return Math.min(90, (completed / SCAN_STEPS.length) * 90 + 10);
}

function StepIcon({ done, active }: { done: boolean; active: boolean }) {
  if (done) return <CheckCircle2 className="h-5 w-5 text-green-600" />;
  if (active) return <Loader2 className="h-5 w-5 animate-spin text-primary" />;
  return <Circle className="h-5 w-5 text-muted-foreground" />;
}

export default function ScanPage() {
  const { id } = useParams<{ id: string }>();
  const router = useRouter();

  const { data: audit } = useQuery<Audit>({
    queryKey: ["audit", id],
    queryFn: async () => {
      const res = await fetch(`/api/audits/${id}`);
      if (!res.ok) throw new Error("Failed to fetch audit");
      return res.json();
    },
    refetchInterval: (query) => {
      const status = query.state.data?.status;
      if (status === "completed" || status === "failed") return false;
      return 2000;
    },
  });

  const status = audit?.status ?? "pending";
  const scores = audit?.scores ?? {};
  const progress = getProgress(status, scores);

  useEffect(() => {
    if (status === "completed" && audit) {
      router.replace(`/report/${id}`);
    }
  }, [status, audit, router, id]);

  return (
    <div className="flex min-h-screen items-center justify-center px-4">
      <Card className="w-full max-w-lg">
        <CardHeader className="text-center">
          <CardTitle>
            {status === "failed" ? "진단 실패" : "진단 진행 중..."}
          </CardTitle>
          {audit?.url && (
            <p className="text-sm text-muted-foreground">{audit.url}</p>
          )}
        </CardHeader>
        <CardContent className="space-y-6">
          <div className="space-y-2">
            <div className="flex items-center justify-between text-sm">
              <span>진행률</span>
              <span className="font-medium">{Math.round(progress)}%</span>
            </div>
            <Progress value={progress} />
          </div>

          <div className="space-y-3">
            {SCAN_STEPS.map((step, i) => {
              const done =
                scores[step.key as keyof typeof scores] !== undefined;
              const prevDone =
                i === 0 ||
                scores[SCAN_STEPS[i - 1].key as keyof typeof scores] !==
                  undefined;
              const active = !done && prevDone && status === "scanning";

              return (
                <div key={step.key} className="flex items-center gap-3">
                  <StepIcon done={done} active={active} />
                  <span
                    className={
                      done ? "text-foreground" : "text-muted-foreground"
                    }
                  >
                    {step.label}
                  </span>
                  {done && (
                    <Badge variant="success" className="ml-auto">
                      완료
                    </Badge>
                  )}
                </div>
              );
            })}
          </div>

          {status === "failed" && (
            <p className="text-center text-sm text-destructive">
              진단 중 오류가 발생했습니다. 다시 시도해주세요.
            </p>
          )}
        </CardContent>
      </Card>
    </div>
  );
}
