"use client";

import { useState } from "react";
import { useParams, useRouter } from "next/navigation";
import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import Link from "next/link";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import type { LeadStatus, Grade } from "@/lib/types";

const STATUS_BADGE: Record<
  string,
  {
    label: string;
    variant: "default" | "secondary" | "success" | "warning" | "destructive";
  }
> = {
  new: { label: "신규", variant: "default" },
  contacted: { label: "연락완료", variant: "secondary" },
  consulting: { label: "상담중", variant: "warning" },
  proposal_sent: { label: "제안서발송", variant: "secondary" },
  contracted: { label: "계약", variant: "success" },
  active: { label: "활성", variant: "success" },
  churned: { label: "이탈", variant: "destructive" },
};

const STATUS_OPTIONS: { value: LeadStatus; label: string }[] = [
  { value: "new", label: "신규" },
  { value: "contacted", label: "연락완료" },
  { value: "consulting", label: "상담중" },
  { value: "proposal_sent", label: "제안서발송" },
  { value: "contracted", label: "계약" },
  { value: "active", label: "활성" },
  { value: "churned", label: "이탈" },
];

interface LeadDetail {
  id: string;
  name: string;
  email: string;
  hospital_name: string | null;
  phone: string | null;
  specialty: string | null;
  status: LeadStatus;
  notes: Array<{ date: string; content: string; author: string }> | null;
  emails_sent: number;
  last_email_at: string | null;
  audit_id: string | null;
  created_at: string;
  updated_at: string;
  audit: {
    id: string;
    url: string;
    total_score: number | null;
    grade: Grade | null;
    report_url: string | null;
    created_at: string;
  } | null;
}

export default function AdminLeadDetailPage() {
  const { id } = useParams<{ id: string }>();
  const router = useRouter();
  const queryClient = useQueryClient();
  const [noteContent, setNoteContent] = useState("");
  const [isResending, setIsResending] = useState(false);

  const { data: lead, isLoading } = useQuery<LeadDetail>({
    queryKey: ["admin-lead", id],
    queryFn: async () => {
      const res = await fetch(`/api/admin/leads/${id}`);
      if (!res.ok) throw new Error("Failed");
      return res.json();
    },
  });

  const mutation = useMutation({
    mutationFn: async (body: Record<string, unknown>) => {
      const res = await fetch(`/api/admin/leads/${id}`, {
        method: "PATCH",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(body),
      });
      if (!res.ok) throw new Error("Failed");
      return res.json();
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["admin-lead", id] });
      queryClient.invalidateQueries({ queryKey: ["admin-leads"] });
    },
  });

  const handleAddNote = () => {
    if (!noteContent.trim()) return;
    mutation.mutate(
      { note: { content: noteContent.trim(), author: "관리자" } },
      { onSuccess: () => setNoteContent("") },
    );
  };

  const handleStatusChange = (status: LeadStatus) => {
    mutation.mutate({ status });
  };

  const handleResendReport = async () => {
    setIsResending(true);
    try {
      await mutation.mutateAsync({ resend_report: true });
    } finally {
      setIsResending(false);
    }
  };

  if (isLoading) {
    return (
      <div>
        <p className="text-muted-foreground">로딩 중...</p>
      </div>
    );
  }

  if (!lead) {
    return (
      <div>
        <p className="text-destructive">리드를 찾을 수 없습니다.</p>
      </div>
    );
  }

  const badge = STATUS_BADGE[lead.status] ?? STATUS_BADGE.new;
  const notes = Array.isArray(lead.notes) ? lead.notes : [];

  return (
    <div>
      <div className="mb-6 flex items-center gap-4">
        <Button variant="outline" size="sm" onClick={() => router.back()}>
          &larr; 목록
        </Button>
        <h1 className="text-2xl font-bold">리드 상세</h1>
      </div>

      {/* Lead Info */}
      <Card className="mb-6">
        <CardHeader>
          <div className="flex items-center justify-between">
            <CardTitle className="text-lg">{lead.name}</CardTitle>
            <Badge variant={badge.variant}>{badge.label}</Badge>
          </div>
        </CardHeader>
        <CardContent>
          <dl className="grid gap-3 sm:grid-cols-2">
            <div>
              <dt className="text-sm text-muted-foreground">이메일</dt>
              <dd className="font-medium">{lead.email}</dd>
            </div>
            <div>
              <dt className="text-sm text-muted-foreground">병원명</dt>
              <dd className="font-medium">{lead.hospital_name ?? "-"}</dd>
            </div>
            <div>
              <dt className="text-sm text-muted-foreground">전화</dt>
              <dd className="font-medium">{lead.phone ?? "-"}</dd>
            </div>
            <div>
              <dt className="text-sm text-muted-foreground">진료과</dt>
              <dd className="font-medium">{lead.specialty ?? "-"}</dd>
            </div>
            <div>
              <dt className="text-sm text-muted-foreground">발송 이메일</dt>
              <dd className="font-medium">{lead.emails_sent}건</dd>
            </div>
            <div>
              <dt className="text-sm text-muted-foreground">등록일</dt>
              <dd className="font-medium">
                {new Date(lead.created_at).toLocaleDateString("ko-KR")}
              </dd>
            </div>
          </dl>

          {/* Status change */}
          <div className="mt-4 flex flex-wrap items-center gap-2">
            <span className="text-sm text-muted-foreground">상태 변경:</span>
            {STATUS_OPTIONS.map((opt) => (
              <Button
                key={opt.value}
                variant={lead.status === opt.value ? "default" : "outline"}
                size="sm"
                disabled={lead.status === opt.value || mutation.isPending}
                onClick={() => handleStatusChange(opt.value)}
              >
                {opt.label}
              </Button>
            ))}
          </div>
        </CardContent>
      </Card>

      {/* Linked Audit */}
      {lead.audit && (
        <Card className="mb-6">
          <CardHeader>
            <div className="flex items-center justify-between">
              <CardTitle className="text-lg">연결된 진단</CardTitle>
              <Button
                variant="outline"
                size="sm"
                disabled={isResending}
                onClick={handleResendReport}
              >
                {isResending ? "발송 중..." : "리포트 재발송"}
              </Button>
            </div>
          </CardHeader>
          <CardContent>
            <dl className="grid gap-3 sm:grid-cols-2">
              <div>
                <dt className="text-sm text-muted-foreground">URL</dt>
                <dd className="font-medium truncate">{lead.audit.url}</dd>
              </div>
              <div>
                <dt className="text-sm text-muted-foreground">점수 / 등급</dt>
                <dd className="font-medium">
                  {lead.audit.total_score ?? "-"}점 / {lead.audit.grade ?? "-"}
                  등급
                </dd>
              </div>
              <div>
                <dt className="text-sm text-muted-foreground">진단일</dt>
                <dd className="font-medium">
                  {new Date(lead.audit.created_at).toLocaleDateString("ko-KR")}
                </dd>
              </div>
              <div>
                <dt className="text-sm text-muted-foreground">리포트</dt>
                <dd>
                  <Link
                    href={`/report/${lead.audit.id}`}
                    className="text-sm text-primary underline"
                  >
                    리포트 보기
                  </Link>
                </dd>
              </div>
            </dl>
          </CardContent>
        </Card>
      )}

      {/* Consultation Notes */}
      <Card>
        <CardHeader>
          <CardTitle className="text-lg">상담 메모</CardTitle>
        </CardHeader>
        <CardContent>
          {/* Note list */}
          {notes.length === 0 ? (
            <p className="mb-4 text-sm text-muted-foreground">
              등록된 메모가 없습니다.
            </p>
          ) : (
            <div className="mb-4 space-y-3">
              {notes.map((note, i) => (
                <div key={i} className="rounded-lg border p-3">
                  <div className="mb-1 flex items-center justify-between">
                    <span className="text-xs font-medium text-muted-foreground">
                      {note.author}
                    </span>
                    <span className="text-xs text-muted-foreground">
                      {new Date(note.date).toLocaleString("ko-KR")}
                    </span>
                  </div>
                  <p className="text-sm whitespace-pre-wrap">{note.content}</p>
                </div>
              ))}
            </div>
          )}

          {/* Add note */}
          <div className="flex gap-2">
            <Input
              placeholder="상담 메모를 입력하세요..."
              value={noteContent}
              onChange={(e) => setNoteContent(e.target.value)}
              onKeyDown={(e) => {
                if (e.key === "Enter" && !e.shiftKey) {
                  e.preventDefault();
                  handleAddNote();
                }
              }}
            />
            <Button
              onClick={handleAddNote}
              disabled={!noteContent.trim() || mutation.isPending}
            >
              {mutation.isPending ? "저장 중..." : "저장"}
            </Button>
          </div>
        </CardContent>
      </Card>
    </div>
  );
}
