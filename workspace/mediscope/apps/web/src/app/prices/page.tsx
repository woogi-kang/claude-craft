"use client";

import { useState } from "react";
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
} from "recharts";
import { ArrowLeft } from "lucide-react";
import Link from "next/link";
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import { COUNTRY_LABELS, COUNTRY_COLORS } from "@/lib/types/beauty";

interface PriceData {
  procedure_id: number;
  procedure_name: string;
  prices: Array<{
    country: string;
    currency: string;
    price_min: number | null;
    price_max: number | null;
  }>;
}

function PriceChart({ data }: { data: PriceData }) {
  const chartData = data.prices
    .filter((p) => p.price_min != null)
    .map((p) => ({
      country: COUNTRY_LABELS[p.country] ?? p.country,
      countryCode: p.country,
      avg: Math.round(((p.price_min ?? 0) + (p.price_max ?? 0)) / 2),
    }))
    .sort((a, b) => b.avg - a.avg);

  return (
    <ResponsiveContainer
      width="100%"
      height={Math.max(200, chartData.length * 60)}
    >
      <BarChart
        data={chartData}
        layout="vertical"
        margin={{ left: 20, right: 30 }}
      >
        <CartesianGrid strokeDasharray="3 3" horizontal={false} />
        <XAxis
          type="number"
          tickFormatter={(v) => v.toLocaleString()}
          fontSize={12}
        />
        <YAxis type="category" dataKey="country" width={80} fontSize={14} />
        <Tooltip
          formatter={(value: number) => [value.toLocaleString(), "평균 가격"]}
          contentStyle={{ borderRadius: 8 }}
        />
        <Bar dataKey="avg" radius={[0, 6, 6, 0]} barSize={32}>
          {chartData.map((entry) => (
            <Cell
              key={entry.countryCode}
              fill={COUNTRY_COLORS[entry.countryCode] ?? "#94A3B8"}
              opacity={entry.countryCode === "KR" ? 1 : 0.7}
            />
          ))}
        </Bar>
      </BarChart>
    </ResponsiveContainer>
  );
}

export default function PricesPage() {
  const [selectedIdx, setSelectedIdx] = useState<string>("0");

  const { data, isLoading, error } = useQuery<PriceData[]>({
    queryKey: ["prices-compare"],
    queryFn: () => fetch("/api/prices/compare").then((r) => r.json()),
  });

  const selected = data?.[parseInt(selectedIdx)];

  return (
    <div className="min-h-screen bg-gradient-to-b from-blue-50 to-white">
      <div className="mx-auto max-w-4xl px-4 py-8">
        <Link
          href="/"
          className="mb-6 inline-flex items-center gap-1 text-sm text-muted-foreground hover:text-foreground"
        >
          <ArrowLeft className="h-4 w-4" /> 홈으로
        </Link>

        <div className="mb-8">
          <h1 className="text-3xl font-bold tracking-tight">
            한국 미용시술 가격비교
          </h1>
          <p className="mt-2 text-muted-foreground">
            한국, 일본, 중국의 주요 미용시술 가격을 비교해보세요.
          </p>
        </div>

        {isLoading && (
          <div className="flex items-center justify-center py-20">
            <div className="h-8 w-8 animate-spin rounded-full border-4 border-blue-500 border-t-transparent" />
          </div>
        )}

        {error && (
          <Card>
            <CardContent className="py-10 text-center text-muted-foreground">
              데이터를 불러오는 중 오류가 발생했습니다.
            </CardContent>
          </Card>
        )}

        {data && data.length > 0 && (
          <>
            <Card className="mb-6">
              <CardHeader>
                <CardTitle className="text-lg">시술 선택</CardTitle>
                <CardDescription>비교할 시술을 선택하세요</CardDescription>
              </CardHeader>
              <CardContent>
                <Select value={selectedIdx} onValueChange={setSelectedIdx}>
                  <SelectTrigger className="w-full max-w-md">
                    <SelectValue placeholder="시술을 선택하세요" />
                  </SelectTrigger>
                  <SelectContent>
                    {data.map((item, idx) => (
                      <SelectItem key={idx} value={String(idx)}>
                        {item.procedure_name}
                      </SelectItem>
                    ))}
                  </SelectContent>
                </Select>
              </CardContent>
            </Card>

            {selected && (
              <>
                <Card className="mb-6">
                  <CardHeader>
                    <CardTitle>{selected.procedure_name}</CardTitle>
                    <CardDescription>
                      국가별 가격 비교 (현지 통화 기준)
                    </CardDescription>
                  </CardHeader>
                  <CardContent>
                    <PriceChart data={selected} />
                  </CardContent>
                </Card>

                <Card>
                  <CardHeader>
                    <CardTitle className="text-lg">상세 가격표</CardTitle>
                  </CardHeader>
                  <CardContent>
                    <div className="overflow-x-auto">
                      <table className="w-full text-sm">
                        <thead>
                          <tr className="border-b text-left">
                            <th className="pb-2 font-medium">국가</th>
                            <th className="pb-2 font-medium">최저가</th>
                            <th className="pb-2 font-medium">최고가</th>
                            <th className="pb-2 font-medium">통화</th>
                          </tr>
                        </thead>
                        <tbody>
                          {selected.prices.map((p) => (
                            <tr
                              key={p.country}
                              className="border-b last:border-0"
                            >
                              <td className="py-3">
                                <div className="flex items-center gap-2">
                                  <div
                                    className="h-3 w-3 rounded-full"
                                    style={{
                                      backgroundColor:
                                        COUNTRY_COLORS[p.country] ?? "#94A3B8",
                                    }}
                                  />
                                  {COUNTRY_LABELS[p.country] ?? p.country}
                                </div>
                              </td>
                              <td className="py-3">
                                {p.price_min?.toLocaleString() ?? "-"}
                              </td>
                              <td className="py-3">
                                {p.price_max?.toLocaleString() ?? "-"}
                              </td>
                              <td className="py-3 font-medium">{p.currency}</td>
                            </tr>
                          ))}
                        </tbody>
                      </table>
                    </div>
                  </CardContent>
                </Card>
              </>
            )}
          </>
        )}

        {data && data.length === 0 && (
          <Card>
            <CardContent className="py-10 text-center text-muted-foreground">
              가격비교 데이터가 없습니다.
            </CardContent>
          </Card>
        )}
      </div>
    </div>
  );
}
