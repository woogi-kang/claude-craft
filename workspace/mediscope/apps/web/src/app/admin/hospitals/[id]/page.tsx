"use client";

import { useParams } from "next/navigation";
import { useQuery } from "@tanstack/react-query";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { ScoreTrendChart } from "@/components/score-trend-chart";
import { BeforeAfterTable } from "@/components/before-after-table";
import type { Category } from "@/lib/types";

type CategoryScores = Partial<Record<Category, number>>;

interface Hospital {
  id: string;
  name: string;
  url: string;
  specialty: string | null;
  region: string | null;
  latest_score: number | null;
}

interface ScoreHistoryResponse {
  history: Array<{
    date: string;
    total_score: number;
    category_scores: CategoryScores;
  }>;
  before: CategoryScores;
  current: CategoryScores;
}

export default function AdminHospitalDetailPage() {
  const { id } = useParams<{ id: string }>();

  const { data: hospital } = useQuery<Hospital>({
    queryKey: ["admin-hospital", id],
    queryFn: async () => {
      const res = await fetch(`/api/admin/hospitals/${id}`);
      if (!res.ok) throw new Error("Failed");
      return res.json();
    },
  });

  const { data: scoreData } = useQuery<ScoreHistoryResponse>({
    queryKey: ["score-history", id],
    queryFn: async () => {
      const res = await fetch(`/api/score-history/${id}`);
      if (!res.ok) throw new Error("Failed");
      return res.json();
    },
  });

  async function handleRescan() {
    if (!hospital) return;
    await fetch("/api/audits", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ url: hospital.url }),
    });
    alert("재스캔이 요청되었습니다.");
  }

  return (
    <div>
      <div className="mb-6 flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold">
            {hospital?.name ?? "로딩 중..."}
          </h1>
          {hospital && (
            <p className="text-sm text-muted-foreground">{hospital.url}</p>
          )}
        </div>
        <div className="flex items-center gap-3">
          {hospital?.latest_score !== null &&
            hospital?.latest_score !== undefined && (
              <Badge variant="outline" className="text-lg">
                {hospital.latest_score}점
              </Badge>
            )}
          <Button onClick={handleRescan} disabled={!hospital}>
            재스캔
          </Button>
        </div>
      </div>

      <div className="grid gap-6">
        {hospital && (
          <Card>
            <CardHeader>
              <CardTitle className="text-lg">병원 정보</CardTitle>
            </CardHeader>
            <CardContent>
              <dl className="grid grid-cols-2 gap-4 text-sm">
                <div>
                  <dt className="text-muted-foreground">전문 분야</dt>
                  <dd className="font-medium">
                    {hospital.specialty ?? "미지정"}
                  </dd>
                </div>
                <div>
                  <dt className="text-muted-foreground">지역</dt>
                  <dd className="font-medium">{hospital.region ?? "미지정"}</dd>
                </div>
              </dl>
            </CardContent>
          </Card>
        )}

        <Card>
          <CardHeader>
            <CardTitle className="text-lg">점수 추이</CardTitle>
          </CardHeader>
          <CardContent>
            {scoreData && scoreData.history.length > 1 ? (
              <ScoreTrendChart history={scoreData.history} target={80} />
            ) : (
              <p className="text-muted-foreground">
                추이 데이터가 부족합니다. (최소 2회 진단 필요)
              </p>
            )}
          </CardContent>
        </Card>

        {scoreData && Object.keys(scoreData.before).length > 0 && (
          <Card>
            <CardHeader>
              <CardTitle className="text-lg">Before / After 비교</CardTitle>
            </CardHeader>
            <CardContent>
              <BeforeAfterTable
                before={scoreData.before}
                current={scoreData.current}
              />
            </CardContent>
          </Card>
        )}
      </div>
    </div>
  );
}
