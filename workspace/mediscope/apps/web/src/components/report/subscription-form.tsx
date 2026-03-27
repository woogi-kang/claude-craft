"use client";

import { useState } from "react";
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
    <Card className="mt-8">
      <CardHeader>
        <CardTitle className="text-lg">모니터링 구독</CardTitle>
        <p className="text-sm text-muted-foreground">
          정기적으로 사이트를 재진단하여 점수 변동 알림을 받아보세요.
        </p>
      </CardHeader>
      <CardContent>
        {submitted ? (
          <div className="rounded-lg bg-green-50 p-4 text-center text-green-800">
            구독이 완료되었습니다. 점수 변동 시 이메일로 알림을 보내드립니다.
          </div>
        ) : (
          <form onSubmit={handleSubmit} className="space-y-4">
            <div className="grid gap-4 sm:grid-cols-2">
              <div className="space-y-2">
                <Label htmlFor="sub-email">이메일 *</Label>
                <Input
                  id="sub-email"
                  type="email"
                  placeholder="you@hospital.kr"
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  required
                />
              </div>
              <div className="space-y-2">
                <Label htmlFor="sub-frequency">진단 빈도</Label>
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
            </div>
            {error && <p className="text-sm text-destructive">{error}</p>}
            <Button
              type="submit"
              variant="outline"
              className="w-full"
              disabled={loading}
            >
              {loading ? "처리중..." : "점수 변동 알림 받기"}
            </Button>
          </form>
        )}
      </CardContent>
    </Card>
  );
}
