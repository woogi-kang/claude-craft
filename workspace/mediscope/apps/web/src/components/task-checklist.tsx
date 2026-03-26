"use client";

import { useState } from "react";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";

interface Task {
  id: string;
  title: string;
  category?: string;
  priority?: "high" | "medium" | "low";
  done: boolean;
}

interface TaskChecklistProps {
  projectId: string;
  tasks: Task[];
  readOnly?: boolean;
}

const PRIORITY_COLORS: Record<string, string> = {
  high: "destructive",
  medium: "warning",
  low: "secondary",
};

export function TaskChecklist({
  projectId,
  tasks: initialTasks,
  readOnly = false,
}: TaskChecklistProps) {
  const [tasks, setTasks] = useState<Task[]>(initialTasks);
  const [newTitle, setNewTitle] = useState("");
  const [loading, setLoading] = useState<string | null>(null);

  async function handleToggle(taskId: string, done: boolean) {
    setLoading(taskId);
    try {
      const res = await fetch(`/api/projects/${projectId}/tasks`, {
        method: "PATCH",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ action: "update", taskId, data: { done } }),
      });
      if (res.ok) {
        setTasks((prev) =>
          prev.map((t) => (t.id === taskId ? { ...t, done } : t)),
        );
      }
    } finally {
      setLoading(null);
    }
  }

  async function handleAdd() {
    if (!newTitle.trim()) return;
    setLoading("add");
    try {
      const res = await fetch(`/api/projects/${projectId}/tasks`, {
        method: "PATCH",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          action: "add",
          data: { title: newTitle.trim(), priority: "medium" },
        }),
      });
      if (res.ok) {
        const { task } = await res.json();
        setTasks((prev) => [...prev, task]);
        setNewTitle("");
      }
    } finally {
      setLoading(null);
    }
  }

  async function handleRemove(taskId: string) {
    setLoading(taskId);
    try {
      const res = await fetch(`/api/projects/${projectId}/tasks`, {
        method: "PATCH",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ action: "remove", taskId }),
      });
      if (res.ok) {
        setTasks((prev) => prev.filter((t) => t.id !== taskId));
      }
    } finally {
      setLoading(null);
    }
  }

  return (
    <div className="space-y-2">
      {tasks.map((task) => (
        <div
          key={task.id}
          className="flex items-center gap-3 rounded-lg border p-3"
        >
          <input
            type="checkbox"
            checked={task.done}
            disabled={readOnly || loading === task.id}
            onChange={(e) => handleToggle(task.id, e.target.checked)}
            className="h-4 w-4 rounded border-gray-300"
          />
          <span
            className={task.done ? "line-through text-muted-foreground" : ""}
          >
            {task.title}
          </span>
          {task.category && (
            <Badge variant="outline" className="text-xs">
              {task.category}
            </Badge>
          )}
          {task.priority && (
            <Badge
              variant={
                (PRIORITY_COLORS[task.priority] ?? "secondary") as
                  | "destructive"
                  | "warning"
                  | "secondary"
              }
              className="text-xs"
            >
              {task.priority}
            </Badge>
          )}
          {!readOnly && (
            <Button
              variant="ghost"
              size="sm"
              className="ml-auto h-6 w-6 p-0 text-muted-foreground hover:text-destructive"
              onClick={() => handleRemove(task.id)}
              disabled={loading === task.id}
            >
              x
            </Button>
          )}
        </div>
      ))}
      {!readOnly && (
        <div className="flex gap-2 pt-2">
          <Input
            placeholder="새 작업 추가..."
            value={newTitle}
            onChange={(e) => setNewTitle(e.target.value)}
            onKeyDown={(e) => e.key === "Enter" && handleAdd()}
          />
          <Button onClick={handleAdd} disabled={loading === "add"} size="sm">
            추가
          </Button>
        </div>
      )}
    </div>
  );
}
