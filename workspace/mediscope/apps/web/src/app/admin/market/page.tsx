"use client";

import { useQuery } from "@tanstack/react-query";
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  Cell,
  PieChart,
  Pie,
} from "recharts";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";

const SIDOS = [
  "서울",
  "경기",
  "부산",
  "인천",
  "대구",
  "대전",
  "광주",
  "울산",
  "세종",
  "강원",
  "충북",
  "충남",
  "전북",
  "전남",
  "경북",
  "경남",
  "제주",
];

const BAR_COLORS = [
  "#4f46e5",
  "#0ea5e9",
  "#8b5cf6",
  "#f59e0b",
  "#10b981",
  "#ef4444",
  "#6366f1",
  "#14b8a6",
  "#f97316",
  "#a855f7",
  "#ec4899",
  "#06b6d4",
  "#84cc16",
  "#eab308",
  "#3b82f6",
  "#8b5cf6",
  "#22c55e",
];

const PIE_COLORS = ["#4f46e5", "#e5e7eb"];

interface RegionData {
  sido: string;
  total_clinics: number;
  website_count: number;
  website_rate: number;
  foreign_patient_facilitators: number;
  foreign_patient_rate: number;
  distribution: {
    sggu: string;
    total: number;
    withWebsite: number;
    foreignFacilitator: number;
  }[];
}

export default function MarketPage() {
  const { data: regionsData, isLoading } = useQuery<RegionData[]>({
    queryKey: ["market-overview"],
    queryFn: async () => {
      const results = await Promise.all(
        SIDOS.map(async (sido) => {
          const res = await fetch(
            `/api/competition/region/${encodeURIComponent(sido)}`,
          );
          if (!res.ok) return null;
          return res.json();
        }),
      );
      return results.filter(
        (r): r is RegionData => r !== null && r.total_clinics > 0,
      );
    },
  });

  if (isLoading) {
    return (
      <div className="flex items-center justify-center py-12">
        <p className="text-muted-foreground">시장 현황 로딩 중...</p>
      </div>
    );
  }

  const regions = regionsData ?? [];
  const totalClinics = regions.reduce((sum, r) => sum + r.total_clinics, 0);
  const totalWebsite = regions.reduce((sum, r) => sum + r.website_count, 0);
  const totalForeign = regions.reduce(
    (sum, r) => sum + r.foreign_patient_facilitators,
    0,
  );

  const barData = regions
    .map((r) => ({
      name: r.sido,
      count: r.total_clinics,
    }))
    .sort((a, b) => b.count - a.count);

  // Find 강남/서초 concentration
  const seoul = regions.find((r) => r.sido === "서울");
  const gangnamSeocho = (seoul?.distribution ?? []).filter((d) =>
    ["강남구", "서초구"].includes(d.sggu),
  );
  const gangnamSeochoCount = gangnamSeocho.reduce((sum, d) => sum + d.total, 0);

  return (
    <div>
      <h1 className="mb-6 text-2xl font-bold">전국 시장 현황</h1>

      {/* Stats Cards */}
      <div className="mb-8 grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
        <Card>
          <CardHeader className="pb-2">
            <CardTitle className="text-sm text-muted-foreground">
              전국 피부과
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="text-3xl font-bold">
              {totalClinics.toLocaleString()}
            </div>
            <p className="text-xs text-muted-foreground">
              {regions.length}개 시도
            </p>
          </CardContent>
        </Card>
        <Card>
          <CardHeader className="pb-2">
            <CardTitle className="text-sm text-muted-foreground">
              웹사이트 보유
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="text-3xl font-bold text-blue-600">
              {totalWebsite.toLocaleString()}
            </div>
            <p className="text-xs text-muted-foreground">
              {totalClinics > 0
                ? Math.round((totalWebsite / totalClinics) * 100)
                : 0}
              % 보유율
            </p>
          </CardContent>
        </Card>
        <Card>
          <CardHeader className="pb-2">
            <CardTitle className="text-sm text-muted-foreground">
              외국인유치기관
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="text-3xl font-bold text-orange-600">
              {totalForeign.toLocaleString()}
            </div>
            <p className="text-xs text-muted-foreground">
              {totalClinics > 0
                ? Math.round((totalForeign / totalClinics) * 100)
                : 0}
              % 비율
            </p>
          </CardContent>
        </Card>
        <Card>
          <CardHeader className="pb-2">
            <CardTitle className="text-sm text-muted-foreground">
              강남/서초 집중도
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="text-3xl font-bold text-purple-600">
              {gangnamSeochoCount.toLocaleString()}
            </div>
            <p className="text-xs text-muted-foreground">
              전체의{" "}
              {totalClinics > 0
                ? Math.round((gangnamSeochoCount / totalClinics) * 100)
                : 0}
              %
            </p>
          </CardContent>
        </Card>
      </div>

      {/* Bar Chart: Clinics by Sido */}
      <div className="mb-8 grid gap-6 lg:grid-cols-2">
        <Card>
          <CardHeader>
            <CardTitle className="text-lg">시도별 피부과 수</CardTitle>
          </CardHeader>
          <CardContent>
            <ResponsiveContainer width="100%" height={400}>
              <BarChart data={barData} layout="vertical">
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis type="number" />
                <YAxis
                  type="category"
                  dataKey="name"
                  width={50}
                  tick={{ fontSize: 12 }}
                />
                <Tooltip />
                <Bar dataKey="count" radius={[0, 4, 4, 0]}>
                  {barData.map((_, i) => (
                    <Cell key={i} fill={BAR_COLORS[i % BAR_COLORS.length]} />
                  ))}
                </Bar>
              </BarChart>
            </ResponsiveContainer>
          </CardContent>
        </Card>

        {/* Pie Charts */}
        <div className="space-y-6">
          <Card>
            <CardHeader>
              <CardTitle className="text-lg">웹사이트 보유율</CardTitle>
            </CardHeader>
            <CardContent>
              <ResponsiveContainer width="100%" height={180}>
                <PieChart>
                  <Pie
                    data={[
                      { name: "보유", value: totalWebsite },
                      { name: "미보유", value: totalClinics - totalWebsite },
                    ]}
                    cx="50%"
                    cy="50%"
                    innerRadius={50}
                    outerRadius={70}
                    dataKey="value"
                    label={({ name, percent }) =>
                      `${name} ${(percent * 100).toFixed(0)}%`
                    }
                  >
                    <Cell fill={PIE_COLORS[0]} />
                    <Cell fill={PIE_COLORS[1]} />
                  </Pie>
                  <Tooltip />
                </PieChart>
              </ResponsiveContainer>
            </CardContent>
          </Card>
          <Card>
            <CardHeader>
              <CardTitle className="text-lg">외국인유치기관 비율</CardTitle>
            </CardHeader>
            <CardContent>
              <ResponsiveContainer width="100%" height={180}>
                <PieChart>
                  <Pie
                    data={[
                      { name: "유치기관", value: totalForeign },
                      { name: "일반", value: totalClinics - totalForeign },
                    ]}
                    cx="50%"
                    cy="50%"
                    innerRadius={50}
                    outerRadius={70}
                    dataKey="value"
                    label={({ name, percent }) =>
                      `${name} ${(percent * 100).toFixed(0)}%`
                    }
                  >
                    <Cell fill="#f59e0b" />
                    <Cell fill={PIE_COLORS[1]} />
                  </Pie>
                  <Tooltip />
                </PieChart>
              </ResponsiveContainer>
            </CardContent>
          </Card>
        </div>
      </div>
    </div>
  );
}
