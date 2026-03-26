"use client";

import { useParams } from "next/navigation";
import { useQuery } from "@tanstack/react-query";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { ScoreTrendChart } from "@/components/score-trend-chart";
import { BeforeAfterTable } from "@/components/before-after-table";
import { TaskChecklist } from "@/components/task-checklist";
import { ProgressRing } from "@/components/progress-ring";
import type { Category } from "@/lib/types";

type CategoryScores = Partial<Record<Category, number>>;

interface Task {
  id: string;
  title: string;
  category?: string;
  priority?: "high" | "medium" | "low";
  done: boolean;
}

interface Project {
  id: string;
  name: string | null;
  status: string;
  start_date: string | null;
  end_date: string | null;
  contract_amount: number | null;
  client_token: string | null;
  plan: { tasks?: Task[] } | null;
  hospitals: {
    id: string;
    name: string;
    url: string;
    latest_score: number | null;
  } | null;
  leads: { id: string; name: string; email: string } | null;
}

interface ScoreHistoryResponse {
  history: Array<{
    date: string;
    total_score: number;
    category_scores: CategoryScores;
  }>;
  before: CategoryScores;
  current: CategoryScores;
}

const STATUS_BADGE: Record<
  string,
  {
    label: string;
    variant: "default" | "secondary" | "success" | "warning" | "destructive";
  }
> = {
  planning: { label: "기획", variant: "default" },
  in_progress: { label: "진행중", variant: "warning" },
  completed: { label: "완료", variant: "success" },
  cancelled: { label: "취소", variant: "destructive" },
};

export default function AdminProjectDetailPage() {
  const { id } = useParams<{ id: string }>();

  const { data: project } = useQuery<Project>({
    queryKey: ["project", id],
    queryFn: async () => {
      const res = await fetch(`/api/projects/${id}`);
      if (!res.ok) throw new Error("Failed");
      return res.json();
    },
  });

  const hospitalId = project?.hospitals?.id;

  const { data: scoreData } = useQuery<ScoreHistoryResponse>({
    queryKey: ["score-history", hospitalId],
    queryFn: async () => {
      const res = await fetch(`/api/score-history/${hospitalId}`);
      if (!res.ok) throw new Error("Failed");
      return res.json();
    },
    enabled: !!hospitalId,
  });

  if (!project) {
    return <p className="text-muted-foreground">로딩 중...</p>;
  }

  const tasks: Task[] = project.plan?.tasks ?? [];
  const doneCount = tasks.filter((t) => t.done).length;
  const progress =
    tasks.length > 0 ? Math.round((doneCount / tasks.length) * 100) : 0;
  const badge = STATUS_BADGE[project.status] ?? STATUS_BADGE.planning;

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-start justify-between">
        <div>
          <h1 className="text-2xl font-bold">{project.name ?? "프로젝트"}</h1>
          <p className="text-sm text-muted-foreground">
            {project.hospitals?.name} &middot; {project.leads?.name}
          </p>
        </div>
        <div className="flex items-center gap-3">
          <Badge variant={badge.variant}>{badge.label}</Badge>
          <ProgressRing value={progress} size={64} />
        </div>
      </div>

      {/* Project Info */}
      <Card>
        <CardHeader>
          <CardTitle className="text-lg">프로젝트 정보</CardTitle>
        </CardHeader>
        <CardContent>
          <dl className="grid grid-cols-2 gap-4 text-sm sm:grid-cols-4">
            <div>
              <dt className="text-muted-foreground">기간</dt>
              <dd className="font-medium">
                {project.start_date && project.end_date
                  ? `${project.start_date} ~ ${project.end_date}`
                  : "미정"}
              </dd>
            </div>
            <div>
              <dt className="text-muted-foreground">계약금액</dt>
              <dd className="font-medium">
                {project.contract_amount
                  ? `${project.contract_amount.toLocaleString()}원`
                  : "미정"}
              </dd>
            </div>
            <div>
              <dt className="text-muted-foreground">진행률</dt>
              <dd className="font-medium">
                {doneCount}/{tasks.length} ({progress}%)
              </dd>
            </div>
            <div>
              <dt className="text-muted-foreground">고객 링크</dt>
              <dd className="font-medium">
                {project.client_token ? (
                  <a
                    href={`/client/${hospitalId}?token=${project.client_token}`}
                    className="text-primary underline"
                    target="_blank"
                    rel="noopener noreferrer"
                  >
                    공유 링크
                  </a>
                ) : (
                  "-"
                )}
              </dd>
            </div>
          </dl>
        </CardContent>
      </Card>

      {/* Score Trend */}
      <Card>
        <CardHeader>
          <CardTitle className="text-lg">점수 추이</CardTitle>
        </CardHeader>
        <CardContent>
          {scoreData && scoreData.history.length > 1 ? (
            <ScoreTrendChart history={scoreData.history} target={80} />
          ) : (
            <p className="text-muted-foreground">
              추이 데이터가 부족합니다. (최소 2회 진단 필요)
            </p>
          )}
        </CardContent>
      </Card>

      {/* Before/After */}
      {scoreData && Object.keys(scoreData.before).length > 0 && (
        <Card>
          <CardHeader>
            <CardTitle className="text-lg">Before / After 비교</CardTitle>
          </CardHeader>
          <CardContent>
            <BeforeAfterTable
              before={scoreData.before}
              current={scoreData.current}
            />
          </CardContent>
        </Card>
      )}

      {/* Task Checklist */}
      <Card>
        <CardHeader>
          <CardTitle className="text-lg">작업 체크리스트</CardTitle>
        </CardHeader>
        <CardContent>
          <TaskChecklist projectId={project.id} tasks={tasks} />
        </CardContent>
      </Card>
    </div>
  );
}
