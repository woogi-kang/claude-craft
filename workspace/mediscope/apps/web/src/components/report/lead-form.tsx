"use client";

import { useState } from "react";
import { MessageSquareHeart, Send } from "lucide-react";
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
    <section className="mt-10">
      <div className="rounded-2xl border-2 border-primary/20 bg-gradient-to-br from-slate-50 to-blue-50/40 p-6 sm:p-8">
        <div className="flex items-center gap-3 mb-2">
          <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-primary/10">
            <MessageSquareHeart
              className="h-5 w-5 text-primary"
              aria-hidden="true"
            />
          </div>
          <div>
            <h2 className="text-lg font-bold text-slate-900">
              전문가의 도움이 필요하신가요?
            </h2>
            <p className="text-sm text-slate-500">
              정보를 입력하시면 맞춤 개선안을 이메일로 보내드립니다
            </p>
          </div>
        </div>

        {submitted ? (
          <div className="mt-4 rounded-xl bg-green-50 border border-green-200 p-5 text-center">
            <p className="text-green-800 font-medium">신청이 완료되었습니다.</p>
            <p className="text-sm text-green-600 mt-1">
              이메일로 맞춤 개선안을 보내드리겠습니다.
            </p>
          </div>
        ) : (
          <form onSubmit={handleSubmit} className="mt-5 space-y-4">
            <div className="grid gap-4 sm:grid-cols-2">
              <div className="space-y-1.5">
                <Label
                  htmlFor="lead-email"
                  className="text-sm font-medium text-slate-700"
                >
                  이메일 *
                </Label>
                <Input
                  id="lead-email"
                  type="email"
                  placeholder="you@hospital.kr"
                  value={form.email}
                  onChange={(e) =>
                    setForm((p) => ({ ...p, email: e.target.value }))
                  }
                  required
                  className="bg-white"
                />
              </div>
              <div className="space-y-1.5">
                <Label
                  htmlFor="lead-name"
                  className="text-sm font-medium text-slate-700"
                >
                  담당자명 *
                </Label>
                <Input
                  id="lead-name"
                  placeholder="홍길동"
                  value={form.name}
                  onChange={(e) =>
                    setForm((p) => ({ ...p, name: e.target.value }))
                  }
                  required
                  className="bg-white"
                />
              </div>
              <div className="space-y-1.5">
                <Label
                  htmlFor="lead-hospital"
                  className="text-sm font-medium text-slate-700"
                >
                  병원명
                </Label>
                <Input
                  id="lead-hospital"
                  placeholder="OO병원"
                  value={form.hospital_name}
                  onChange={(e) =>
                    setForm((p) => ({
                      ...p,
                      hospital_name: e.target.value,
                    }))
                  }
                  className="bg-white"
                />
              </div>
              <div className="space-y-1.5">
                <Label
                  htmlFor="lead-phone"
                  className="text-sm font-medium text-slate-700"
                >
                  전화번호
                </Label>
                <Input
                  id="lead-phone"
                  type="tel"
                  placeholder="02-1234-5678"
                  value={form.phone}
                  onChange={(e) =>
                    setForm((p) => ({ ...p, phone: e.target.value }))
                  }
                  className="bg-white"
                />
              </div>
            </div>
            {error && <p className="text-sm text-destructive">{error}</p>}
            <Button type="submit" size="lg" className="w-full text-base">
              <Send className="h-4 w-4" aria-hidden="true" />
              무료 상담 받기
            </Button>
          </form>
        )}
      </div>
    </section>
  );
}
