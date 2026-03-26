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
import { ArrowLeft, Clock, Zap, AlertTriangle, Scissors } from "lucide-react";
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
import {
  BEAUTY_CATEGORIES,
  COUNTRY_COLORS,
  COUNTRY_LABELS,
} from "@/lib/types/beauty";
import type {
  Procedure,
  ProcedureDetail,
  ProcedureTranslation,
  CountryPrice,
} from "@/lib/types/beauty";

interface ProcedureResponse {
  procedure: Procedure;
  details: ProcedureDetail;
  translations: ProcedureTranslation[];
  prices: CountryPrice[];
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
  value: string | number | null | undefined;
}) {
  if (value == null) return null;
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

function PriceSection({ prices }: { prices: CountryPrice[] }) {
  const chartData = prices
    .filter((p) => p.price_min != null || p.price_max != null)
    .map((p) => ({
      country: COUNTRY_LABELS[p.country] ?? p.country,
      code: p.country,
      avg: Math.round(
        ((p.price_min ?? 0) + (p.price_max ?? p.price_min ?? 0)) / 2,
      ),
      currency: p.currency,
    }));

  if (chartData.length === 0) return null;

  return (
    <Card>
      <CardHeader>
        <CardTitle className="text-lg">가격비교</CardTitle>
        <CardDescription>국가별 평균 가격</CardDescription>
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
              tickFormatter={(v) => v.toLocaleString()}
              fontSize={12}
            />
            <YAxis type="category" dataKey="country" width={80} fontSize={12} />
            <Tooltip
              formatter={(
                value: number,
                _name: string,
                props: { payload?: { currency?: string } },
              ) => [
                `${value.toLocaleString()} ${props.payload?.currency ?? ""}`,
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

  const { procedure, details, translations, prices } = data;
  const categoryInfo = BEAUTY_CATEGORIES[procedure.primary_category_id];

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
              {procedure.name}
            </h1>
            {categoryInfo && (
              <Badge variant="secondary">
                {categoryInfo.icon} {categoryInfo.name}
              </Badge>
            )}
          </div>
          {details?.alias && (
            <p className="mt-1 text-lg text-muted-foreground">
              {details.alias}
            </p>
          )}
        </div>

        {/* Quick Info Grid */}
        {details && (
          <div className="mb-6 grid gap-3 sm:grid-cols-2">
            <InfoItem
              icon={<Scissors className="h-4 w-4" />}
              label="시술 시간"
              value={details.duration_of_procedure ?? details.duration}
            />
            <InfoItem
              icon={<Zap className="h-4 w-4" />}
              label="통증 레벨"
              value={details.pain_level}
            />
            <InfoItem
              icon={<Clock className="h-4 w-4" />}
              label="다운타임"
              value={details.downtime}
            />
            <InfoItem
              icon={<Clock className="h-4 w-4" />}
              label="권장 주기"
              value={details.recommended_cycle}
            />
          </div>
        )}

        {/* Detail Tabs: Korean details + multilingual translations */}
        <Card className="mb-6">
          <Tabs defaultValue="ko">
            <CardHeader>
              <div className="flex items-center justify-between">
                <CardTitle className="text-lg">상세 정보</CardTitle>
                <TabsList>
                  <TabsTrigger value="ko">{LANG_LABELS.ko}</TabsTrigger>
                  {translations.map((t) => (
                    <TabsTrigger key={t.language_code} value={t.language_code}>
                      {LANG_LABELS[t.language_code] ?? t.language_code}
                    </TabsTrigger>
                  ))}
                </TabsList>
              </div>
            </CardHeader>
            <CardContent>
              {/* Korean tab: from procedure_details */}
              <TabsContent value="ko">
                <div className="space-y-4">
                  {details?.principle && (
                    <div>
                      <h3 className="mb-1 font-semibold">원리</h3>
                      <p className="text-sm text-muted-foreground whitespace-pre-line">
                        {details.principle}
                      </p>
                    </div>
                  )}
                  {details?.effect && (
                    <div>
                      <h3 className="mb-1 font-semibold">효과</h3>
                      <p className="text-sm text-muted-foreground whitespace-pre-line">
                        {details.effect}
                      </p>
                    </div>
                  )}
                  {details?.target && (
                    <div>
                      <h3 className="mb-1 font-semibold">대상</h3>
                      <p className="text-sm text-muted-foreground whitespace-pre-line">
                        {details.target}
                      </p>
                    </div>
                  )}
                  {details?.side_effects && (
                    <div>
                      <h3 className="mb-1 flex items-center gap-1 font-semibold">
                        <AlertTriangle className="h-4 w-4 text-amber-500" />
                        부작용
                      </h3>
                      <p className="text-sm text-muted-foreground whitespace-pre-line">
                        {details.side_effects}
                      </p>
                    </div>
                  )}
                  {details?.post_care && (
                    <div>
                      <h3 className="mb-1 font-semibold">사후 관리</h3>
                      <p className="text-sm text-muted-foreground whitespace-pre-line">
                        {details.post_care}
                      </p>
                    </div>
                  )}
                </div>
              </TabsContent>

              {/* Translation tabs: from procedure_intl */}
              {translations.map((t) => (
                <TabsContent key={t.language_code} value={t.language_code}>
                  <div className="space-y-4">
                    {t.principle && (
                      <div>
                        <h3 className="mb-1 font-semibold">原理 / Principle</h3>
                        <p className="text-sm text-muted-foreground whitespace-pre-line">
                          {t.principle}
                        </p>
                      </div>
                    )}
                    {t.method && (
                      <div>
                        <h3 className="mb-1 font-semibold">方法 / Method</h3>
                        <p className="text-sm text-muted-foreground whitespace-pre-line">
                          {t.method}
                        </p>
                      </div>
                    )}
                    {t.downtime && (
                      <div>
                        <h3 className="mb-1 font-semibold">
                          ダウンタイム / Downtime
                        </h3>
                        <p className="text-sm text-muted-foreground whitespace-pre-line">
                          {t.downtime}
                        </p>
                      </div>
                    )}
                    {t.post_care && (
                      <div>
                        <h3 className="mb-1 font-semibold">
                          アフターケア / Post Care
                        </h3>
                        <p className="text-sm text-muted-foreground whitespace-pre-line">
                          {t.post_care}
                        </p>
                      </div>
                    )}
                  </div>
                </TabsContent>
              ))}
            </CardContent>
          </Tabs>
        </Card>

        {/* Price Comparison Section */}
        {prices && prices.length > 0 && <PriceSection prices={prices} />}
      </div>
    </div>
  );
}
