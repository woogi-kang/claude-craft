"use client";

import {
  Radar,
  RadarChart as RechartsRadarChart,
  PolarGrid,
  PolarAngleAxis,
  PolarRadiusAxis,
  ResponsiveContainer,
} from "recharts";

interface CategoryScore {
  label: string;
  score: number;
}

interface RadarChartProps {
  categories: CategoryScore[];
}

function CustomTick({
  x,
  y,
  payload,
  categories,
}: {
  x: number;
  y: number;
  payload: { value: string };
  categories: CategoryScore[];
}) {
  const cat = categories.find((c) => c.label === payload.value);
  const score = cat?.score ?? 0;

  return (
    <g transform={`translate(${x},${y})`}>
      <text
        textAnchor="middle"
        dy={-6}
        className="fill-slate-700 text-[11px] font-medium sm:text-xs"
      >
        {payload.value}
      </text>
      <text
        textAnchor="middle"
        dy={10}
        className="fill-slate-500 text-[10px] font-bold tabular-nums sm:text-[11px]"
      >
        {score}점
      </text>
    </g>
  );
}

export function RadarChart({ categories }: RadarChartProps) {
  const data = categories.map((cat) => ({
    subject: cat.label,
    score: cat.score,
    fullMark: 100,
  }));

  return (
    <section className="mt-8">
      <h2 className="mb-4 text-lg font-bold text-slate-900">
        카테고리별 진단 현황
      </h2>
      <div className="rounded-xl border border-slate-200 bg-white p-4 sm:p-6">
        <ResponsiveContainer width="100%" height={320}>
          <RechartsRadarChart cx="50%" cy="50%" outerRadius="70%" data={data}>
            <PolarGrid stroke="#e2e8f0" />
            <PolarAngleAxis
              dataKey="subject"
              tick={(props: {
                x: number;
                y: number;
                payload: { value: string };
              }) => <CustomTick {...props} categories={categories} />}
            />
            <PolarRadiusAxis
              angle={90}
              domain={[0, 100]}
              tick={false}
              axisLine={false}
            />
            <Radar
              name="점수"
              dataKey="score"
              stroke="#3b82f6"
              fill="#3b82f6"
              fillOpacity={0.15}
              strokeWidth={2}
            />
          </RechartsRadarChart>
        </ResponsiveContainer>
      </div>
    </section>
  );
}
