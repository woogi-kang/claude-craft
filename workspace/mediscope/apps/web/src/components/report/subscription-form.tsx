"use client";

import { useState } from "react";
import { Bell } from "lucide-react";
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

export function SubscriptionForm({ auditId }: { auditId: string }) {
  const [email, setEmail] = useState("");
  const [frequency, setFrequency] = useState("monthly");
  const [submitted, setSubmitted] = useState(false);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    setError("");

    if (!email) {
      setError("이메일을 입력해주세요.");
      return;
    }

    setLoading(true);
    try {
      const res = await fetch("/api/subscriptions", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          audit_id: auditId,
          email,
          frequency,
        }),
      });
      if (!res.ok) {
        const data = await res.json().catch(() => ({}));
        throw new Error((data as { error?: string }).error ?? "구독 실패");
      }
      setSubmitted(true);
    } catch (err) {
      setError(
        err instanceof Error
          ? err.message
          : "구독에 실패했습니다. 다시 시도해주세요.",
      );
    } finally {
      setLoading(false);
    }
  }

  return (
    <section className="mt-6">
      <div className="rounded-xl border border-slate-200 bg-white p-5 sm:p-6">
        <div className="flex items-center gap-2 mb-1">
          <Bell className="h-4 w-4 text-slate-500" aria-hidden="true" />
          <h3 className="text-base font-semibold text-slate-900">
            모니터링 구독
          </h3>
        </div>
        <p className="text-sm text-slate-500 mb-4">
          정기적으로 사이트를 재진단하여 점수 변동 알림을 받아보세요.
        </p>

        {submitted ? (
          <div className="rounded-lg bg-green-50 border border-green-200 p-4 text-center text-green-800">
            구독이 완료되었습니다. 점수 변동 시 이메일로 알림을 보내드립니다.
          </div>
        ) : (
          <form
            onSubmit={handleSubmit}
            className="flex flex-col sm:flex-row gap-3"
          >
            <div className="flex-1 space-y-1">
              <Label htmlFor="sub-email" className="sr-only">
                이메일
              </Label>
              <Input
                id="sub-email"
                type="email"
                placeholder="이메일 주소를 입력하세요"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                required
              />
            </div>
            <div className="w-full sm:w-28 space-y-1">
              <Label htmlFor="sub-frequency" className="sr-only">
                진단 빈도
              </Label>
              <Select value={frequency} onValueChange={setFrequency}>
                <SelectTrigger id="sub-frequency">
                  <SelectValue />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="weekly">주간</SelectItem>
                  <SelectItem value="biweekly">격주</SelectItem>
                  <SelectItem value="monthly">월간</SelectItem>
                </SelectContent>
              </Select>
            </div>
            <Button
              type="submit"
              variant="outline"
              disabled={loading}
              className="shrink-0"
            >
              {loading ? "처리중..." : "알림 받기"}
            </Button>
          </form>
        )}
        {error && <p className="mt-2 text-sm text-destructive">{error}</p>}
      </div>
    </section>
  );
}
