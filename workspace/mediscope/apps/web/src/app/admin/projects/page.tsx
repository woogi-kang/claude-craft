"use client";

import { useQuery } from "@tanstack/react-query";
import Link from "next/link";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { ProgressRing } from "@/components/progress-ring";

interface Project {
  id: string;
  name: string | null;
  status: string;
  start_date: string | null;
  end_date: string | null;
  contract_amount: number | null;
  plan: { tasks?: Array<{ done: boolean }> } | null;
  hospitals: {
    id: string;
    name: string;
    url: string;
    latest_score: number | null;
  } | null;
  leads: { id: string; name: string; hospital_name: string | null } | null;
  created_at: string;
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

function getProgress(plan: Project["plan"]): number {
  const tasks = plan?.tasks ?? [];
  if (tasks.length === 0) return 0;
  const done = tasks.filter((t) => t.done).length;
  return Math.round((done / tasks.length) * 100);
}

export default function AdminProjectsPage() {
  const { data: projects, isLoading } = useQuery<Project[]>({
    queryKey: ["admin-projects"],
    queryFn: async () => {
      const res = await fetch("/api/projects");
      if (!res.ok) throw new Error("Failed");
      return res.json();
    },
  });

  return (
    <div>
      <div className="mb-6 flex items-center justify-between">
        <h1 className="text-2xl font-bold">프로젝트</h1>
        <Link href="/admin/projects/new">
          <Button>새 프로젝트</Button>
        </Link>
      </div>

      {isLoading ? (
        <p className="text-muted-foreground">로딩 중...</p>
      ) : !projects?.length ? (
        <Card>
          <CardContent className="p-8 text-center text-muted-foreground">
            등록된 프로젝트가 없습니다.
          </CardContent>
        </Card>
      ) : (
        <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
          {projects.map((project) => {
            const badge = STATUS_BADGE[project.status] ?? STATUS_BADGE.planning;
            const progress = getProgress(project.plan);
            return (
              <Link key={project.id} href={`/admin/projects/${project.id}`}>
                <Card className="hover:bg-accent/50 transition-colors">
                  <CardHeader className="pb-3">
                    <div className="flex items-center justify-between">
                      <CardTitle className="text-base">
                        {project.name ?? project.hospitals?.name ?? "프로젝트"}
                      </CardTitle>
                      <Badge variant={badge.variant}>{badge.label}</Badge>
                    </div>
                    <p className="text-sm text-muted-foreground">
                      {project.hospitals?.name ??
                        project.leads?.hospital_name ??
                        "-"}
                    </p>
                  </CardHeader>
                  <CardContent>
                    <div className="flex items-center justify-between">
                      <div className="space-y-1 text-sm">
                        {project.start_date && project.end_date && (
                          <p className="text-muted-foreground">
                            {project.start_date} ~ {project.end_date}
                          </p>
                        )}
                        {project.hospitals?.latest_score !== null &&
                          project.hospitals?.latest_score !== undefined && (
                            <p>
                              현재 점수:{" "}
                              <span className="font-medium">
                                {project.hospitals.latest_score}점
                              </span>
                            </p>
                          )}
                      </div>
                      <ProgressRing value={progress} size={64} />
                    </div>
                  </CardContent>
                </Card>
              </Link>
            );
          })}
        </div>
      )}
    </div>
  );
}
