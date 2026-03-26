"use client";

import { useState } from "react";
import { useRouter, useSearchParams } from "next/navigation";
import { useQuery } from "@tanstack/react-query";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";

interface Lead {
  id: string;
  name: string;
  email: string;
  hospital_name: string | null;
  audit_id: string | null;
  status: string;
}

interface Audit {
  id: string;
  hospital_id: string | null;
}

export default function NewProjectPage() {
  const router = useRouter();
  const searchParams = useSearchParams();
  const preselectedLeadId = searchParams.get("lead_id") ?? "";

  const [form, setForm] = useState({
    lead_id: preselectedLeadId,
    name: "",
    contract_amount: "",
    start_date: "",
    end_date: "",
  });
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  const { data: leads } = useQuery<Lead[]>({
    queryKey: ["admin-leads"],
    queryFn: async () => {
      const res = await fetch("/api/admin/leads");
      if (!res.ok) throw new Error("Failed");
      return res.json();
    },
  });

  const selectedLead = leads?.find((l) => l.id === form.lead_id);

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    setError("");

    if (!form.lead_id || !form.name) {
      setError("리드와 프로젝트 이름은 필수입니다.");
      return;
    }

    setLoading(true);
    try {
      let hospitalId: string | null = null;

      if (selectedLead?.audit_id) {
        const auditRes = await fetch(`/api/audits/${selectedLead.audit_id}`);
        if (auditRes.ok) {
          const audit: Audit = await auditRes.json();
          hospitalId = audit.hospital_id;
        }
      }

      if (!hospitalId) {
        setError("연결된 병원을 찾을 수 없습니다. 리드에 진단이 필요합니다.");
        return;
      }

      const res = await fetch("/api/projects", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          lead_id: form.lead_id,
          hospital_id: hospitalId,
          name: form.name,
          contract_amount: form.contract_amount
            ? parseInt(form.contract_amount, 10)
            : undefined,
          start_date: form.start_date || undefined,
          end_date: form.end_date || undefined,
        }),
      });

      if (!res.ok) {
        const data = await res.json().catch(() => ({}));
        throw new Error(
          (data as { error?: string }).error ?? "프로젝트 생성 실패",
        );
      }

      const project = await res.json();
      router.push(`/admin/projects/${project.id}`);
    } catch (err) {
      setError(
        err instanceof Error ? err.message : "프로젝트 생성에 실패했습니다.",
      );
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="mx-auto max-w-2xl">
      <h1 className="mb-6 text-2xl font-bold">새 프로젝트</h1>

      <Card>
        <CardHeader>
          <CardTitle className="text-lg">프로젝트 정보</CardTitle>
        </CardHeader>
        <CardContent>
          <form onSubmit={handleSubmit} className="space-y-4">
            <div className="space-y-2">
              <Label htmlFor="lead">리드 선택 *</Label>
              <Select
                value={form.lead_id}
                onValueChange={(v) => setForm((p) => ({ ...p, lead_id: v }))}
              >
                <SelectTrigger id="lead">
                  <SelectValue placeholder="리드를 선택하세요" />
                </SelectTrigger>
                <SelectContent>
                  {leads?.map((lead) => (
                    <SelectItem key={lead.id} value={lead.id}>
                      {lead.name} - {lead.hospital_name ?? lead.email}
                    </SelectItem>
                  ))}
                </SelectContent>
              </Select>
              {selectedLead && (
                <p className="text-sm text-muted-foreground">
                  병원: {selectedLead.hospital_name ?? "미지정"} &middot;{" "}
                  {selectedLead.email}
                </p>
              )}
            </div>

            <div className="space-y-2">
              <Label htmlFor="name">프로젝트 이름 *</Label>
              <Input
                id="name"
                placeholder="SEO 최적화 프로젝트"
                value={form.name}
                onChange={(e) =>
                  setForm((p) => ({ ...p, name: e.target.value }))
                }
                required
              />
            </div>

            <div className="space-y-2">
              <Label htmlFor="contract_amount">계약 금액 (원)</Label>
              <Input
                id="contract_amount"
                type="number"
                placeholder="5000000"
                value={form.contract_amount}
                onChange={(e) =>
                  setForm((p) => ({ ...p, contract_amount: e.target.value }))
                }
              />
            </div>

            <div className="grid gap-4 sm:grid-cols-2">
              <div className="space-y-2">
                <Label htmlFor="start_date">시작일</Label>
                <Input
                  id="start_date"
                  type="date"
                  value={form.start_date}
                  onChange={(e) =>
                    setForm((p) => ({ ...p, start_date: e.target.value }))
                  }
                />
              </div>
              <div className="space-y-2">
                <Label htmlFor="end_date">종료일</Label>
                <Input
                  id="end_date"
                  type="date"
                  value={form.end_date}
                  onChange={(e) =>
                    setForm((p) => ({ ...p, end_date: e.target.value }))
                  }
                />
              </div>
            </div>

            {error && <p className="text-sm text-destructive">{error}</p>}

            <Button type="submit" className="w-full" disabled={loading}>
              {loading ? "생성 중..." : "프로젝트 생성"}
            </Button>
          </form>
        </CardContent>
      </Card>
    </div>
  );
}
