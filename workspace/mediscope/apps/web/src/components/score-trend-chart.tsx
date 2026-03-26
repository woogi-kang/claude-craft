"use client";

import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ReferenceLine,
  ResponsiveContainer,
} from "recharts";

interface ScorePoint {
  date: string;
  total_score: number;
}

interface ScoreTrendChartProps {
  history: ScorePoint[];
  target?: number;
}

export function ScoreTrendChart({ history, target }: ScoreTrendChartProps) {
  const data = history.map((h) => ({
    date: new Date(h.date).toLocaleDateString("ko-KR", {
      month: "short",
      day: "numeric",
    }),
    score: h.total_score,
  }));

  return (
    <ResponsiveContainer width="100%" height={300}>
      <LineChart data={data}>
        <CartesianGrid strokeDasharray="3 3" />
        <XAxis dataKey="date" tick={{ fontSize: 12 }} />
        <YAxis domain={[0, 100]} tick={{ fontSize: 12 }} />
        <Tooltip
          formatter={(value: number) => [`${value}점`, "점수"]}
          labelFormatter={(label: string) => `날짜: ${label}`}
        />
        <Line
          type="monotone"
          dataKey="score"
          stroke="#4f46e5"
          strokeWidth={2}
          dot={{ r: 4 }}
          activeDot={{ r: 6 }}
        />
        {target && (
          <ReferenceLine
            y={target}
            stroke="#ef4444"
            strokeDasharray="5 5"
            label={{ value: `목표 ${target}`, position: "right", fontSize: 12 }}
          />
        )}
      </LineChart>
    </ResponsiveContainer>
  );
}
