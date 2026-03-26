import { createAdminClient } from "@/lib/supabase/admin";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { ScoreTrendChart } from "@/components/score-trend-chart";
import { BeforeAfterTable } from "@/components/before-after-table";
import type { Category } from "@/lib/types";

type CategoryScores = Partial<Record<Category, number>>;

interface Props {
  params: Promise<{ hospitalId: string }>;
  searchParams: Promise<{ token?: string }>;
}

export default async function ClientHospitalPage({
  params,
  searchParams,
}: Props) {
  const { hospitalId } = await params;
  const { token } = await searchParams;

  if (!token) {
    return (
      <div className="flex min-h-screen items-center justify-center">
        <Card className="max-w-md">
          <CardContent className="p-8 text-center">
            <h1 className="mb-2 text-xl font-bold text-destructive">
              접근 불가
            </h1>
            <p className="text-muted-foreground">
              유효한 토큰이 필요합니다. 관리자에게 문의하세요.
            </p>
          </CardContent>
        </Card>
      </div>
    );
  }

  const supabase = createAdminClient();

  const { data: project } = await supabase
    .from("projects")
    .select("id, client_token, hospital_id")
    .eq("hospital_id", hospitalId)
    .eq("client_token", token)
    .single();

  if (!project) {
    return (
      <div className="flex min-h-screen items-center justify-center">
        <Card className="max-w-md">
          <CardContent className="p-8 text-center">
            <h1 className="mb-2 text-xl font-bold text-destructive">
              접근 불가
            </h1>
            <p className="text-muted-foreground">유효하지 않은 토큰입니다.</p>
          </CardContent>
        </Card>
      </div>
    );
  }

  const { data: hospital } = await supabase
    .from("hospitals")
    .select("name, url")
    .eq("id", hospitalId)
    .single();

  const { data: history } = await supabase
    .from("score_history")
    .select("total_score, category_scores, created_at")
    .eq("hospital_id", hospitalId)
    .order("created_at", { ascending: true });

  const formatted = (history ?? []).map((h) => ({
    date: h.created_at as string,
    total_score: h.total_score as number,
    category_scores: h.category_scores as CategoryScores,
  }));

  const before: CategoryScores =
    formatted.length > 0 ? formatted[0].category_scores : {};
  const current: CategoryScores =
    formatted.length > 0 ? formatted[formatted.length - 1].category_scores : {};

  return (
    <div className="mx-auto max-w-4xl px-4 py-12">
      <h1 className="mb-2 text-3xl font-bold">
        {hospital?.name ?? "병원"} 진단 현황
      </h1>
      <p className="mb-8 text-muted-foreground">{hospital?.url}</p>

      <div className="grid gap-6">
        <Card>
          <CardHeader>
            <CardTitle className="text-lg">점수 추이</CardTitle>
          </CardHeader>
          <CardContent>
            {formatted.length > 1 ? (
              <ScoreTrendChart history={formatted} target={80} />
            ) : (
              <p className="text-muted-foreground">
                추이 데이터가 부족합니다. (최소 2회 진단 필요)
              </p>
            )}
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle className="text-lg">Before / After 비교</CardTitle>
          </CardHeader>
          <CardContent>
            <BeforeAfterTable before={before} current={current} />
          </CardContent>
        </Card>
      </div>
    </div>
  );
}
