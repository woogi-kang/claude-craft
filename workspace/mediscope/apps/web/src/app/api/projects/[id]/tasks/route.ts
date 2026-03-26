import { NextRequest, NextResponse } from "next/server";
import { createAdminClient } from "@/lib/supabase/admin";

interface Task {
  id: string;
  title: string;
  category?: string;
  priority?: "high" | "medium" | "low";
  done: boolean;
}

export async function PATCH(
  request: NextRequest,
  { params }: { params: Promise<{ id: string }> },
) {
  try {
    const { id } = await params;
    const body = await request.json();
    const { action, taskId, data } = body as {
      action: "add" | "update" | "remove";
      taskId?: string;
      data?: Partial<Task>;
    };

    const supabase = createAdminClient();

    const { data: project, error: fetchError } = await supabase
      .from("projects")
      .select("plan")
      .eq("id", id)
      .single();

    if (fetchError || !project) {
      return NextResponse.json(
        { error: "프로젝트를 찾을 수 없습니다" },
        { status: 404 },
      );
    }

    const plan = (project.plan as { tasks?: Task[] }) ?? { tasks: [] };
    const tasks: Task[] = plan.tasks ?? [];

    let newTask: Task | undefined;

    if (action === "add" && data) {
      newTask = {
        id: crypto.randomUUID(),
        title: data.title ?? "",
        category: data.category,
        priority: data.priority ?? "medium",
        done: false,
      };
      tasks.push(newTask);
    } else if (action === "update" && taskId && data) {
      const idx = tasks.findIndex((t) => t.id === taskId);
      if (idx >= 0) {
        tasks[idx] = { ...tasks[idx], ...data };
      }
    } else if (action === "remove" && taskId) {
      const idx = tasks.findIndex((t) => t.id === taskId);
      if (idx >= 0) tasks.splice(idx, 1);
    } else {
      return NextResponse.json({ error: "잘못된 요청" }, { status: 400 });
    }

    const { error: updateError } = await supabase
      .from("projects")
      .update({ plan: { ...plan, tasks } })
      .eq("id", id);

    if (updateError) {
      return NextResponse.json({ error: "수정 실패" }, { status: 500 });
    }

    return NextResponse.json({ tasks, task: newTask });
  } catch {
    return NextResponse.json({ error: "서버 오류" }, { status: 500 });
  }
}
