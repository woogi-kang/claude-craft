"use client";

import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { GRADE_COLORS } from "@/lib/types";

function ScoreGauge({ score, grade }: { score: number; grade: string }) {
  return (
    <div className="flex flex-col items-center">
      <div className="relative flex h-32 w-32 items-center justify-center rounded-full border-8 border-muted">
        <div className="text-center">
          <div className="text-4xl font-bold">{score}</div>
          <div className="text-sm text-muted-foreground">/100</div>
        </div>
      </div>
      <Badge
        className={`mt-3 text-lg ${GRADE_COLORS[grade as keyof typeof GRADE_COLORS] ?? ""}`}
        variant="outline"
      >
        등급: {grade}
      </Badge>
    </div>
  );
}

export function ScoreSection({
  totalScore,
  grade,
}: {
  totalScore: number;
  grade: string;
}) {
  return (
    <Card>
      <CardHeader>
        <CardTitle className="text-lg">종합 점수</CardTitle>
      </CardHeader>
      <CardContent className="flex justify-center">
        <ScoreGauge score={totalScore} grade={grade} />
      </CardContent>
    </Card>
  );
}
