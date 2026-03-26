"use client";

import { use } from "react";
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
import {
  ArrowLeft,
  Clock,
  Zap,
  AlertTriangle,
  Shield,
  Scissors,
} from "lucide-react";
import Link from "next/link";
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { BEAUTY_CATEGORIES, COUNTRY_COLORS } from "@/lib/types/beauty";
import type {
  Procedure,
  ProcedureDetail,
  PriceComparison,
} from "@/lib/types/beauty";

interface ProcedureResponse {
  procedure: Procedure;
  details: ProcedureDetail[];
  price_comparison: PriceComparison | null;
}

const LANG_LABELS: Record<string, string> = {
  ko: "한국어",
  ja: "日本語",
  zh: "中文",
  en: "English",
};

function InfoItem({
  icon,
  label,
  value,
}: {
  icon: React.ReactNode;
  label: string;
  value: string | null;
}) {
  if (!value) return null;
  return (
    <div className="flex items-start gap-3 rounded-lg border p-3">
      <div className="mt-0.5 text-muted-foreground">{icon}</div>
      <div>
        <p className="text-xs font-medium text-muted-foreground">{label}</p>
        <p className="text-sm">{value}</p>
      </div>
    </div>
  );
}

function PriceSection({ price }: { price: PriceComparison }) {
  const chartData = [
    {
      country: "한국",
      code: "KR",
      avg: Math.round((price.korea_min_usd + price.korea_max_usd) / 2),
    },
    price.japan_min_usd != null
      ? {
          country: "일본",
          code: "JP",
          avg: Math.round(
            ((price.japan_min_usd ?? 0) + (price.japan_max_usd ?? 0)) / 2,
          ),
        }
      : null,
    price.china_min_usd != null
      ? {
          country: "중국",
          code: "CN",
          avg: Math.round(
            ((price.china_min_usd ?? 0) + (price.china_max_usd ?? 0)) / 2,
          ),
        }
      : null,
  ].filter(Boolean) as { country: string; code: string; avg: number }[];

  return (
    <Card>
      <CardHeader>
        <CardTitle className="text-lg">가격비교</CardTitle>
        <CardDescription>국가별 평균 가격 (USD)</CardDescription>
      </CardHeader>
      <CardContent>
        <ResponsiveContainer width="100%" height={200}>
          <BarChart
            data={chartData}
            layout="vertical"
            margin={{ left: 20, right: 30 }}
          >
            <CartesianGrid strokeDasharray="3 3" horizontal={false} />
            <XAxis
              type="number"
              tickFormatter={(v) => `$${v.toLocaleString()}`}
              fontSize={12}
            />
            <YAxis type="category" dataKey="country" width={50} fontSize={14} />
            <Tooltip
              formatter={(value: number) => [
                `$${value.toLocaleString()}`,
                "평균",
              ]}
            />
            <Bar dataKey="avg" radius={[0, 6, 6, 0]} barSize={28}>
              {chartData.map((entry) => (
                <Cell
                  key={entry.code}
                  fill={COUNTRY_COLORS[entry.code] ?? "#94A3B8"}
                  opacity={entry.code === "KR" ? 1 : 0.7}
                />
              ))}
            </Bar>
          </BarChart>
        </ResponsiveContainer>

        <div className="mt-4 flex gap-3 flex-wrap">
          {price.savings_vs_japan_pct != null && (
            <Badge variant="success">
              일본 대비 {price.savings_vs_japan_pct}% 절약
            </Badge>
          )}
          {price.savings_vs_china_pct != null && (
            <Badge variant="warning">
              중국 대비 {price.savings_vs_china_pct}% 절약
            </Badge>
          )}
        </div>

        <div className="mt-4">
          <Link
            href="/prices"
            className="text-sm text-blue-600 hover:underline"
          >
            전체 가격비교 보기 &rarr;
          </Link>
        </div>
      </CardContent>
    </Card>
  );
}

export default function ProcedureDetailPage({
  params,
}: {
  params: Promise<{ id: string }>;
}) {
  const { id } = use(params);

  const { data, isLoading, error } = useQuery<ProcedureResponse>({
    queryKey: ["procedure", id],
    queryFn: () => fetch(`/api/procedures/${id}`).then((r) => r.json()),
  });

  if (isLoading) {
    return (
      <div className="flex min-h-screen items-center justify-center">
        <div className="h-8 w-8 animate-spin rounded-full border-4 border-blue-500 border-t-transparent" />
      </div>
    );
  }

  if (error || !data?.procedure) {
    return (
      <div className="mx-auto max-w-4xl px-4 py-8">
        <Link
          href="/procedures"
          className="mb-6 inline-flex items-center gap-1 text-sm text-muted-foreground hover:text-foreground"
        >
          <ArrowLeft className="h-4 w-4" />
          시술 목록
        </Link>
        <Card>
          <CardContent className="py-10 text-center text-muted-foreground">
            시술 정보를 찾을 수 없습니다.
          </CardContent>
        </Card>
      </div>
    );
  }

  const { procedure, details, price_comparison } = data;
  const koDetail = details.find((d) => d.lang === "ko");
  const availableLangs = details.map((d) => d.lang);

  return (
    <div className="min-h-screen bg-gradient-to-b from-blue-50 to-white">
      <div className="mx-auto max-w-4xl px-4 py-8">
        <Link
          href="/procedures"
          className="mb-6 inline-flex items-center gap-1 text-sm text-muted-foreground hover:text-foreground"
        >
          <ArrowLeft className="h-4 w-4" />
          시술 목록
        </Link>

        <div className="mb-6">
          <div className="flex items-center gap-3">
            <h1 className="text-3xl font-bold tracking-tight">
              {procedure.name_ko}
            </h1>
            <Badge variant="secondary">
              {BEAUTY_CATEGORIES[procedure.category] ?? procedure.category}
            </Badge>
          </div>
          {procedure.name_en && (
            <p className="mt-1 text-lg text-muted-foreground">
              {procedure.name_en}
            </p>
          )}
          {procedure.description_ko && (
            <p className="mt-3 text-muted-foreground">
              {procedure.description_ko}
            </p>
          )}
        </div>

        {/* Quick Info Grid */}
        {koDetail && (
          <div className="mb-6 grid gap-3 sm:grid-cols-2">
            <InfoItem
              icon={<Scissors className="h-4 w-4" />}
              label="시술 시간"
              value={koDetail.duration}
            />
            <InfoItem
              icon={<Shield className="h-4 w-4" />}
              label="마취"
              value={koDetail.anesthesia}
            />
            <InfoItem
              icon={<Zap className="h-4 w-4" />}
              label="통증 레벨"
              value={koDetail.pain_level}
            />
            <InfoItem
              icon={<Clock className="h-4 w-4" />}
              label="다운타임"
              value={koDetail.downtime}
            />
          </div>
        )}

        {/* Multilingual Tabs */}
        {details.length > 0 && (
          <Card className="mb-6">
            <Tabs
              defaultValue={
                availableLangs.includes("ko") ? "ko" : availableLangs[0]
              }
            >
              <CardHeader>
                <div className="flex items-center justify-between">
                  <CardTitle className="text-lg">상세 정보</CardTitle>
                  <TabsList>
                    {availableLangs.map((lang) => (
                      <TabsTrigger key={lang} value={lang}>
                        {LANG_LABELS[lang] ?? lang}
                      </TabsTrigger>
                    ))}
                  </TabsList>
                </div>
              </CardHeader>
              <CardContent>
                {details.map((detail) => (
                  <TabsContent key={detail.lang} value={detail.lang}>
                    <div className="space-y-4">
                      {detail.principle && (
                        <div>
                          <h3 className="mb-1 font-semibold">원리</h3>
                          <p className="text-sm text-muted-foreground whitespace-pre-line">
                            {detail.principle}
                          </p>
                        </div>
                      )}
                      {detail.effects && (
                        <div>
                          <h3 className="mb-1 font-semibold">효과</h3>
                          <p className="text-sm text-muted-foreground whitespace-pre-line">
                            {detail.effects}
                          </p>
                        </div>
                      )}
                      {detail.side_effects && (
                        <div>
                          <h3 className="mb-1 flex items-center gap-1 font-semibold">
                            <AlertTriangle className="h-4 w-4 text-amber-500" />
                            부작용
                          </h3>
                          <p className="text-sm text-muted-foreground whitespace-pre-line">
                            {detail.side_effects}
                          </p>
                        </div>
                      )}
                      {detail.recovery && (
                        <div>
                          <h3 className="mb-1 font-semibold">회복</h3>
                          <p className="text-sm text-muted-foreground whitespace-pre-line">
                            {detail.recovery}
                          </p>
                        </div>
                      )}
                    </div>
                  </TabsContent>
                ))}
              </CardContent>
            </Tabs>
          </Card>
        )}

        {/* Price Comparison Section */}
        {price_comparison && <PriceSection price={price_comparison} />}
      </div>
    </div>
  );
}
