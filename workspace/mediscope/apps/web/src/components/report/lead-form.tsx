"use client";

import { useState } from "react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";

export function LeadForm({ auditId }: { auditId: string }) {
  const [form, setForm] = useState({
    email: "",
    name: "",
    hospital_name: "",
    phone: "",
  });
  const [submitted, setSubmitted] = useState(false);
  const [error, setError] = useState("");

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    setError("");

    if (!form.email || !form.name) {
      setError("이메일과 이름은 필수입니다.");
      return;
    }

    try {
      const res = await fetch("/api/leads", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ audit_id: auditId, ...form }),
      });
      if (!res.ok) throw new Error("제출 실패");
      setSubmitted(true);
    } catch {
      setError("제출에 실패했습니다. 다시 시도해주세요.");
    }
  }

  return (
    <Card className="mt-8">
      <CardHeader>
        <CardTitle className="text-lg">상세 리포트를 받아보세요</CardTitle>
        <p className="text-sm text-muted-foreground">
          정보를 입력하시면 PDF 상세 리포트를 이메일로 보내드립니다.
        </p>
      </CardHeader>
      <CardContent>
        {submitted ? (
          <div className="rounded-lg bg-green-50 p-4 text-center text-green-800">
            신청이 완료되었습니다. 이메일로 상세 리포트를 보내드리겠습니다.
          </div>
        ) : (
          <form onSubmit={handleSubmit} className="space-y-4">
            <div className="grid gap-4 sm:grid-cols-2">
              <div className="space-y-2">
                <Label htmlFor="email">이메일 *</Label>
                <Input
                  id="email"
                  type="email"
                  placeholder="you@hospital.kr"
                  value={form.email}
                  onChange={(e) =>
                    setForm((p) => ({ ...p, email: e.target.value }))
                  }
                  required
                />
              </div>
              <div className="space-y-2">
                <Label htmlFor="name">담당자명 *</Label>
                <Input
                  id="name"
                  placeholder="홍길동"
                  value={form.name}
                  onChange={(e) =>
                    setForm((p) => ({ ...p, name: e.target.value }))
                  }
                  required
                />
              </div>
              <div className="space-y-2">
                <Label htmlFor="hospital_name">병원명</Label>
                <Input
                  id="hospital_name"
                  placeholder="OO병원"
                  value={form.hospital_name}
                  onChange={(e) =>
                    setForm((p) => ({
                      ...p,
                      hospital_name: e.target.value,
                    }))
                  }
                />
              </div>
              <div className="space-y-2">
                <Label htmlFor="phone">전화번호</Label>
                <Input
                  id="phone"
                  type="tel"
                  placeholder="02-1234-5678"
                  value={form.phone}
                  onChange={(e) =>
                    setForm((p) => ({ ...p, phone: e.target.value }))
                  }
                />
              </div>
            </div>
            {error && <p className="text-sm text-destructive">{error}</p>}
            <Button type="submit" className="w-full">
              무료 상세 리포트 받기
            </Button>
          </form>
        )}
      </CardContent>
    </Card>
  );
}
