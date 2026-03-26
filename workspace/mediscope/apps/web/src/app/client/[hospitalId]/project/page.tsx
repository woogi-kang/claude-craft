import { createAdminClient } from "@/lib/supabase/admin";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { ProgressRing } from "@/components/progress-ring";

interface Task {
  id: string;
  title: string;
  category?: string;
  priority?: "high" | "medium" | "low";
  done: boolean;
}

interface Props {
  params: Promise<{ hospitalId: string }>;
  searchParams: Promise<{ token?: string }>;
}

const STATUS_LABELS: Record<string, string> = {
  planning: "기획",
  in_progress: "진행중",
  completed: "완료",
  cancelled: "취소",
};

export default async function ClientProjectPage({
  params,
  searchParams,
}: Props) {
  const { hospitalId } = await params;
  const { token } = await searchParams;

  if (!token) {
    return (
      <div className="flex min-h-screen items-center justify-center">
        <Card className="max-w-md">
          <CardContent className="p-8 text-center">
            <h1 className="mb-2 text-xl font-bold text-destructive">
              접근 불가
            </h1>
            <p className="text-muted-foreground">
              유효한 토큰이 필요합니다. 관리자에게 문의하세요.
            </p>
          </CardContent>
        </Card>
      </div>
    );
  }

  const supabase = createAdminClient();

  const { data: project } = await supabase
    .from("projects")
    .select(
      `
      id, name, status, start_date, end_date, plan,
      hospitals:hospital_id (name, url)
    `,
    )
    .eq("hospital_id", hospitalId)
    .eq("client_token", token)
    .single();

  if (!project) {
    return (
      <div className="flex min-h-screen items-center justify-center">
        <Card className="max-w-md">
          <CardContent className="p-8 text-center">
            <h1 className="mb-2 text-xl font-bold text-destructive">
              접근 불가
            </h1>
            <p className="text-muted-foreground">유효하지 않은 토큰입니다.</p>
          </CardContent>
        </Card>
      </div>
    );
  }

  const plan = project.plan as { tasks?: Task[] } | null;
  const tasks: Task[] = plan?.tasks ?? [];
  const doneCount = tasks.filter((t) => t.done).length;
  const progress =
    tasks.length > 0 ? Math.round((doneCount / tasks.length) * 100) : 0;
  const hospitalsRaw = project.hospitals as
    | { name: string; url: string }
    | { name: string; url: string }[]
    | null;
  const hospital = Array.isArray(hospitalsRaw)
    ? (hospitalsRaw[0] ?? null)
    : hospitalsRaw;

  return (
    <div className="mx-auto max-w-3xl px-4 py-12">
      <h1 className="mb-2 text-3xl font-bold">
        {(project.name as string) ?? "프로젝트"}
      </h1>
      <p className="mb-8 text-muted-foreground">
        {hospital?.name} &middot;{" "}
        {STATUS_LABELS[project.status as string] ?? project.status}
      </p>

      <div className="mb-8 flex items-center gap-6">
        <ProgressRing value={progress} size={100} />
        <div>
          <p className="text-lg font-bold">
            {doneCount}/{tasks.length} 작업 완료
          </p>
          {project.start_date && project.end_date && (
            <p className="text-sm text-muted-foreground">
              {project.start_date as string} ~ {project.end_date as string}
            </p>
          )}
        </div>
      </div>

      <Card>
        <CardHeader>
          <CardTitle className="text-lg">작업 진행 현황</CardTitle>
        </CardHeader>
        <CardContent>
          {tasks.length === 0 ? (
            <p className="text-muted-foreground">등록된 작업이 없습니다.</p>
          ) : (
            <div className="space-y-2">
              {tasks.map((task) => (
                <div
                  key={task.id}
                  className="flex items-center gap-3 rounded-lg border p-3"
                >
                  <div
                    className={`h-4 w-4 rounded-full border-2 ${
                      task.done
                        ? "border-green-500 bg-green-500"
                        : "border-gray-300"
                    }`}
                  />
                  <span
                    className={
                      task.done ? "line-through text-muted-foreground" : ""
                    }
                  >
                    {task.title}
                  </span>
                  {task.category && (
                    <Badge variant="outline" className="text-xs">
                      {task.category}
                    </Badge>
                  )}
                </div>
              ))}
            </div>
          )}
        </CardContent>
      </Card>
    </div>
  );
}
