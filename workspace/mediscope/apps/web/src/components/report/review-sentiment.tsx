"use client";

import { MessageSquare } from "lucide-react";

interface SentimentDistribution {
  positive: number;
  neutral: number;
  negative: number;
}

interface KeywordItem {
  keyword: string;
  count: number;
}

interface ProcedureSentiment {
  name: string;
  positive: number;
  neutral: number;
  negative: number;
  review_count: number;
}

interface Recommendation {
  priority: string;
  message: string;
}

interface ReviewSentimentData {
  reviews_found: number;
  has_review_section: boolean;
  has_star_ratings: boolean;
  average_rating: number | null;
  overall_sentiment: SentimentDistribution;
  top_positive_keywords: KeywordItem[];
  top_negative_keywords: KeywordItem[];
  by_procedure: Record<string, ProcedureSentiment>;
  sentiment_score: number;
  recommendations: Recommendation[];
}

interface ReviewSentimentProps {
  data: ReviewSentimentData;
}

function ScoreCircle({ score }: { score: number }) {
  const color =
    score >= 70
      ? "text-green-600"
      : score >= 40
        ? "text-yellow-600"
        : "text-red-600";
  const bgColor =
    score >= 70 ? "bg-green-50" : score >= 40 ? "bg-yellow-50" : "bg-red-50";

  return (
    <div
      className={`flex h-14 w-14 items-center justify-center rounded-xl ${bgColor}`}
    >
      <span className={`text-xl font-bold tabular-nums ${color}`}>{score}</span>
    </div>
  );
}

function SentimentBar({ data }: { data: SentimentDistribution }) {
  const total = data.positive + data.neutral + data.negative;
  if (total === 0) {
    return <div className="h-3 w-full rounded-full bg-slate-100" />;
  }

  return (
    <div className="flex h-3 w-full overflow-hidden rounded-full">
      {data.positive > 0 && (
        <div
          className="bg-green-500 transition-all"
          style={{ width: `${data.positive}%` }}
        />
      )}
      {data.neutral > 0 && (
        <div
          className="bg-slate-300 transition-all"
          style={{ width: `${data.neutral}%` }}
        />
      )}
      {data.negative > 0 && (
        <div
          className="bg-red-400 transition-all"
          style={{ width: `${data.negative}%` }}
        />
      )}
    </div>
  );
}

function SentimentLegend({ data }: { data: SentimentDistribution }) {
  return (
    <div className="flex items-center gap-4 text-xs text-slate-600">
      <span className="flex items-center gap-1.5">
        <span className="inline-block h-2.5 w-2.5 rounded-full bg-green-500" />
        긍정 {data.positive}%
      </span>
      <span className="flex items-center gap-1.5">
        <span className="inline-block h-2.5 w-2.5 rounded-full bg-slate-300" />
        중립 {data.neutral}%
      </span>
      <span className="flex items-center gap-1.5">
        <span className="inline-block h-2.5 w-2.5 rounded-full bg-red-400" />
        부정 {data.negative}%
      </span>
    </div>
  );
}

function StarRating({ rating }: { rating: number }) {
  const full = Math.floor(rating);
  const hasHalf = rating - full >= 0.3;
  const stars = [];
  for (let i = 0; i < 5; i++) {
    if (i < full) {
      stars.push(
        <span key={i} className="text-yellow-400">
          ★
        </span>,
      );
    } else if (i === full && hasHalf) {
      stars.push(
        <span key={i} className="text-yellow-400 opacity-50">
          ★
        </span>,
      );
    } else {
      stars.push(
        <span key={i} className="text-slate-200">
          ★
        </span>,
      );
    }
  }
  return <span className="text-lg">{stars}</span>;
}

function KeywordTags({
  keywords,
  variant,
}: {
  keywords: KeywordItem[];
  variant: "positive" | "negative";
}) {
  if (keywords.length === 0) return null;
  const styles =
    variant === "positive"
      ? "bg-green-50 text-green-700 border-green-200"
      : "bg-red-50 text-red-700 border-red-200";

  return (
    <div className="flex flex-wrap gap-1.5">
      {keywords.map((kw) => (
        <span
          key={kw.keyword}
          className={`inline-flex items-center gap-1 rounded-md border px-2 py-0.5 text-xs font-medium ${styles}`}
        >
          {kw.keyword}
          <span className="text-[10px] opacity-60">{kw.count}</span>
        </span>
      ))}
    </div>
  );
}

function PriorityBadge({ priority }: { priority: string }) {
  const styles =
    priority === "high"
      ? "bg-red-50 text-red-700 border-red-200"
      : priority === "medium"
        ? "bg-yellow-50 text-yellow-700 border-yellow-200"
        : "bg-slate-50 text-slate-600 border-slate-200";
  const label =
    priority === "high" ? "높음" : priority === "medium" ? "중간" : "낮음";

  return (
    <span
      className={`inline-flex items-center rounded-md border px-1.5 py-0.5 text-xs font-medium ${styles}`}
    >
      {label}
    </span>
  );
}

export function ReviewSentiment({ data }: ReviewSentimentProps) {
  const procedures = Object.entries(data.by_procedure);

  return (
    <section className="mt-10">
      <div className="flex items-center gap-2 mb-4">
        <MessageSquare className="h-5 w-5 text-slate-600" aria-hidden="true" />
        <h2 className="text-lg font-bold text-slate-900">리뷰 감성 분석</h2>
      </div>
      <div className="rounded-xl border border-slate-200 bg-white p-5 sm:p-6">
        {/* Overall score + review count */}
        <div className="flex items-center gap-3 mb-6">
          <ScoreCircle score={data.sentiment_score} />
          <div>
            <p className="text-sm font-semibold text-slate-900">
              리뷰 감성 점수
            </p>
            <p className="text-xs text-slate-500">
              {data.reviews_found}개 리뷰 분석
              {data.has_star_ratings && data.average_rating != null && (
                <span className="ml-2">· 평균 {data.average_rating}점</span>
              )}
            </p>
          </div>
        </div>

        {/* Star rating display */}
        {data.has_star_ratings && data.average_rating != null && (
          <div className="flex items-center gap-2 mb-4">
            <StarRating rating={data.average_rating} />
            <span className="text-sm font-semibold text-slate-700 tabular-nums">
              {data.average_rating} / 5.0
            </span>
          </div>
        )}

        {/* Overall sentiment bar */}
        {data.reviews_found > 0 && (
          <div className="mb-6">
            <p className="text-sm font-medium text-slate-700 mb-2">
              전체 감성 분포
            </p>
            <SentimentBar data={data.overall_sentiment} />
            <div className="mt-2">
              <SentimentLegend data={data.overall_sentiment} />
            </div>
          </div>
        )}

        {/* Keywords */}
        {(data.top_positive_keywords.length > 0 ||
          data.top_negative_keywords.length > 0) && (
          <div className="mb-6 space-y-3">
            {data.top_positive_keywords.length > 0 && (
              <div>
                <p className="text-xs font-medium text-slate-500 mb-1.5">
                  긍정 키워드
                </p>
                <KeywordTags
                  keywords={data.top_positive_keywords}
                  variant="positive"
                />
              </div>
            )}
            {data.top_negative_keywords.length > 0 && (
              <div>
                <p className="text-xs font-medium text-slate-500 mb-1.5">
                  부정 키워드
                </p>
                <KeywordTags
                  keywords={data.top_negative_keywords}
                  variant="negative"
                />
              </div>
            )}
          </div>
        )}

        {/* Procedure breakdown */}
        {procedures.length > 0 && (
          <div className="mb-6">
            <p className="text-sm font-semibold text-slate-900 mb-3">
              시술별 감성 비교
            </p>
            <div className="space-y-3">
              {procedures.map(([key, proc]) => (
                <div
                  key={key}
                  className="rounded-lg border border-slate-100 bg-slate-50 p-3"
                >
                  <div className="flex items-center justify-between mb-1.5">
                    <span className="text-sm font-medium text-slate-700">
                      {proc.name}
                    </span>
                    <span className="text-xs text-slate-500">
                      {proc.review_count}건
                    </span>
                  </div>
                  <SentimentBar data={proc} />
                  <div className="mt-1.5">
                    <SentimentLegend data={proc} />
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* Insight */}
        <div className="rounded-lg border border-indigo-100 bg-indigo-50 p-3 mb-6">
          <p className="text-xs text-indigo-700">
            <span className="font-semibold">Insight:</span>{" "}
            {data.reviews_found === 0
              ? "환자 후기는 신규 환자의 의사결정에 가장 큰 영향을 미칩니다. 리뷰 섹션을 추가하세요."
              : data.overall_sentiment.positive >= 70
                ? "긍정적 리뷰가 많습니다. Google 리뷰와 연동하면 검색 노출이 향상됩니다."
                : "부정적 리뷰에 대한 공개 응대는 오히려 신뢰도를 높일 수 있습니다."}
          </p>
        </div>

        {/* Recommendations */}
        {data.recommendations.length > 0 && (
          <div>
            <h3 className="text-sm font-semibold text-slate-900 mb-3">
              개선 권장사항
            </h3>
            <div className="space-y-2">
              {data.recommendations.map((rec, idx) => (
                <div
                  key={idx}
                  className="flex items-start gap-2.5 rounded-lg border border-slate-100 bg-slate-50 p-3"
                >
                  <PriorityBadge priority={rec.priority} />
                  <p className="text-sm text-slate-700">{rec.message}</p>
                </div>
              ))}
            </div>
          </div>
        )}
      </div>
    </section>
  );
}
