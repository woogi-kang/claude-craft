"use client";

import { useState } from "react";
import { Lock, ArrowRight } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";

interface GateOverlayProps {
  auditId: string;
  totalItems: number;
  failCount: number;
  onUnlock: () => void;
}

export function GateOverlay({
  auditId,
  totalItems,
  failCount,
  onUnlock,
}: GateOverlayProps) {
  const [email, setEmail] = useState("");
  const [name, setName] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    setError("");

    if (!email || !name) {
      setError("이메일과 이름은 필수입니다.");
      return;
    }

    setLoading(true);
    try {
      const res = await fetch("/api/leads", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ audit_id: auditId, email, name }),
      });
      if (!res.ok) throw new Error("제출 실패");
      onUnlock();
    } catch {
      setError("제출에 실패했습니다. 다시 시도해주세요.");
    } finally {
      setLoading(false);
    }
  }

  return (
    <section className="relative mt-10 print:hidden">
      {/* Blurred background hint */}
      <div className="pointer-events-none select-none" aria-hidden="true">
        <div className="space-y-3 blur-sm opacity-50">
          {[1, 2, 3].map((i) => (
            <div
              key={i}
              className="rounded-xl border border-slate-200 bg-white p-5"
            >
              <div className="flex items-center gap-3">
                <div className="h-9 w-9 rounded-lg bg-slate-100" />
                <div className="flex-1 space-y-2">
                  <div className="h-4 w-40 rounded bg-slate-100" />
                  <div className="h-2 w-full rounded-full bg-slate-100" />
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Overlay form */}
      <div className="absolute inset-0 flex items-center justify-center">
        <div className="mx-4 w-full max-w-md rounded-2xl border-2 border-slate-200 bg-white/95 p-6 shadow-xl backdrop-blur-md sm:p-8">
          <div className="mb-4 flex items-center justify-center gap-2">
            <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-slate-100">
              <Lock className="h-5 w-5 text-slate-600" aria-hidden="true" />
            </div>
          </div>
          <h3 className="mb-1 text-center text-lg font-bold text-slate-900">
            상세 진단 결과 확인하기
          </h3>
          <p className="mb-5 text-center text-sm text-slate-500">
            이메일을 입력하면 {totalItems}개 항목의 상세 분석과
            <br />
            개선 가이드를 무료로 확인할 수 있습니다
          </p>
          {failCount > 0 && (
            <p className="mb-4 text-center text-xs font-medium text-red-600">
              {totalItems}개 항목 중 {failCount}개 심각 - 지금 바로 확인하세요
            </p>
          )}

          <form onSubmit={handleSubmit} className="space-y-3">
            <div className="grid gap-3 sm:grid-cols-2">
              <div className="space-y-1.5">
                <Label
                  htmlFor="gate-email"
                  className="text-sm font-medium text-slate-700"
                >
                  이메일 *
                </Label>
                <Input
                  id="gate-email"
                  type="email"
                  placeholder="you@hospital.kr"
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  required
                />
              </div>
              <div className="space-y-1.5">
                <Label
                  htmlFor="gate-name"
                  className="text-sm font-medium text-slate-700"
                >
                  담당자명 *
                </Label>
                <Input
                  id="gate-name"
                  placeholder="홍길동"
                  value={name}
                  onChange={(e) => setName(e.target.value)}
                  required
                />
              </div>
            </div>
            {error && <p className="text-sm text-destructive">{error}</p>}
            <Button
              type="submit"
              size="lg"
              className="w-full text-base"
              disabled={loading}
            >
              {loading ? (
                "처리중..."
              ) : (
                <>
                  상세 리포트 받기
                  <ArrowRight className="ml-1 h-4 w-4" aria-hidden="true" />
                </>
              )}
            </Button>
          </form>
          <p className="mt-3 text-center text-[11px] text-slate-400">
            입력하신 정보는 리포트 발송 목적으로만 사용됩니다
          </p>
        </div>
      </div>
    </section>
  );
}
