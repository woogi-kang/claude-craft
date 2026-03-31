"use client";

import { Video } from "lucide-react";

interface EmbeddedVideo {
  count: number;
  urls: string[];
}

interface SocialProfile {
  found: boolean;
  url: string | null;
  label: string;
}

interface MissingPlatform {
  platform: string;
  reason: string;
  priority: string;
}

interface Recommendation {
  priority: string;
  message: string;
}

interface VideoPresenceData {
  embedded_videos: Record<string, EmbeddedVideo>;
  total_videos: number;
  social_profiles: Record<string, SocialProfile>;
  social_count: number;
  has_video_schema: boolean;
  has_og_video: boolean;
  video_score: number;
  social_score: number;
  overall_score: number;
  missing_platforms: MissingPlatform[];
  recommendations: Recommendation[];
}

interface VideoPresenceProps {
  data: VideoPresenceData;
}

const PLATFORM_META: Record<string, { icon: string }> = {
  youtube: { icon: "▶️" },
  naver_tv: { icon: "📺" },
  vimeo: { icon: "🎬" },
  self_hosted: { icon: "🎥" },
};

const SOCIAL_META: Record<string, { icon: string }> = {
  youtube: { icon: "▶️" },
  instagram: { icon: "📸" },
  tiktok: { icon: "🎵" },
  facebook: { icon: "👤" },
  naver_blog: { icon: "📝" },
  naver_tv: { icon: "📺" },
  kakao_story: { icon: "💬" },
  xiaohongshu: { icon: "📕" },
  twitter: { icon: "🐦" },
};

function ScoreCircle({ score, label }: { score: number; label: string }) {
  const color =
    score >= 70
      ? "text-green-600"
      : score >= 40
        ? "text-yellow-600"
        : "text-red-600";
  const bgColor =
    score >= 70 ? "bg-green-50" : score >= 40 ? "bg-yellow-50" : "bg-red-50";

  return (
    <div className="text-center">
      <div
        className={`flex h-14 w-14 items-center justify-center rounded-xl ${bgColor} mx-auto`}
      >
        <span className={`text-xl font-bold tabular-nums ${color}`}>
          {score}
        </span>
      </div>
      <p className="mt-1.5 text-xs text-slate-500">{label}</p>
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

function SocialProfileCard({
  platform,
  profile,
}: {
  platform: string;
  profile: SocialProfile;
}) {
  const meta = SOCIAL_META[platform] ?? { icon: "🔗" };

  return (
    <div
      className={`flex items-center gap-2 rounded-lg border p-2.5 ${
        profile.found
          ? "border-green-200 bg-green-50"
          : "border-slate-200 bg-slate-50"
      }`}
    >
      <span className="text-base shrink-0" aria-hidden="true">
        {meta.icon}
      </span>
      <div className="flex-1 min-w-0">
        <span className="text-sm font-medium text-slate-800">
          {profile.label}
        </span>
      </div>
      {profile.found ? (
        <span className="inline-flex h-5 w-5 items-center justify-center rounded-full bg-green-500 text-white text-xs shrink-0">
          ✓
        </span>
      ) : (
        <span className="inline-flex h-5 w-5 items-center justify-center rounded-full bg-slate-300 text-white text-xs shrink-0">
          −
        </span>
      )}
    </div>
  );
}

export function VideoPresence({ data }: VideoPresenceProps) {
  const videoPlatforms = Object.entries(data.embedded_videos).filter(
    ([, v]) => v.count > 0,
  );

  const socialOrder = [
    "youtube",
    "instagram",
    "tiktok",
    "facebook",
    "naver_blog",
    "naver_tv",
    "kakao_story",
    "xiaohongshu",
    "twitter",
  ];

  return (
    <section className="mt-10">
      <div className="flex items-center gap-2 mb-4">
        <Video className="h-5 w-5 text-slate-600" aria-hidden="true" />
        <h2 className="text-lg font-bold text-slate-900">
          비디오 & 소셜 프레즌스
        </h2>
        <span className="ml-auto rounded-full bg-slate-100 px-2.5 py-0.5 text-xs font-medium tabular-nums text-slate-600">
          총점 {data.overall_score}
        </span>
      </div>
      <div className="rounded-xl border border-slate-200 bg-white p-5 sm:p-6">
        {/* Score overview */}
        <div className="flex items-center justify-center gap-8 mb-6">
          <ScoreCircle score={data.video_score} label="비디오" />
          <ScoreCircle score={data.overall_score} label="종합" />
          <ScoreCircle score={data.social_score} label="소셜" />
        </div>

        {/* Embedded videos */}
        <div className="mb-6">
          <h3 className="text-sm font-semibold text-slate-900 mb-3">
            임베드 영상{" "}
            <span className="font-normal text-slate-500">
              ({data.total_videos}개)
            </span>
          </h3>
          {videoPlatforms.length > 0 ? (
            <div className="grid gap-2 sm:grid-cols-2">
              {videoPlatforms.map(([platform, info]) => {
                const meta = PLATFORM_META[platform] ?? { icon: "🎬" };
                const label =
                  platform === "youtube"
                    ? "YouTube"
                    : platform === "naver_tv"
                      ? "네이버 TV"
                      : platform === "vimeo"
                        ? "Vimeo"
                        : "자체 호스팅";
                return (
                  <div
                    key={platform}
                    className="flex items-center gap-2 rounded-lg border border-blue-100 bg-blue-50 p-3"
                  >
                    <span className="text-base" aria-hidden="true">
                      {meta.icon}
                    </span>
                    <div className="flex-1">
                      <span className="text-sm font-medium text-blue-900">
                        {label}
                      </span>
                      <span className="ml-2 text-xs text-blue-600">
                        {info.count}개
                      </span>
                    </div>
                  </div>
                );
              })}
            </div>
          ) : (
            <div className="rounded-lg border border-slate-100 bg-slate-50 p-3 text-center">
              <p className="text-sm text-slate-400">
                임베드된 영상이 감지되지 않았습니다
              </p>
            </div>
          )}

          {/* Metadata badges */}
          <div className="mt-3 flex gap-2">
            <span
              className={`inline-flex items-center rounded-md border px-2 py-0.5 text-xs font-medium ${
                data.has_video_schema
                  ? "border-green-200 bg-green-50 text-green-700"
                  : "border-slate-200 bg-slate-50 text-slate-400"
              }`}
            >
              VideoObject Schema {data.has_video_schema ? "✓" : "−"}
            </span>
            <span
              className={`inline-flex items-center rounded-md border px-2 py-0.5 text-xs font-medium ${
                data.has_og_video
                  ? "border-green-200 bg-green-50 text-green-700"
                  : "border-slate-200 bg-slate-50 text-slate-400"
              }`}
            >
              og:video {data.has_og_video ? "✓" : "−"}
            </span>
          </div>
        </div>

        {/* Social profiles */}
        <div className="mb-6">
          <h3 className="text-sm font-semibold text-slate-900 mb-3">
            소셜 미디어 프로필{" "}
            <span className="font-normal text-slate-500">
              ({data.social_count}/{Object.keys(data.social_profiles).length})
            </span>
          </h3>
          <div className="grid gap-2 grid-cols-2 sm:grid-cols-3">
            {socialOrder
              .filter((p) => p in data.social_profiles)
              .map((platform) => (
                <SocialProfileCard
                  key={platform}
                  platform={platform}
                  profile={data.social_profiles[platform]}
                />
              ))}
          </div>
        </div>

        {/* Missing platforms */}
        {data.missing_platforms.filter((p) => p.priority === "high").length >
          0 && (
          <div className="mb-6">
            <h3 className="text-sm font-semibold text-slate-900 mb-3">
              미진출 기회
            </h3>
            <div className="grid gap-2 sm:grid-cols-2">
              {data.missing_platforms
                .filter((p) => p.priority === "high")
                .map((mp) => (
                  <div
                    key={mp.platform}
                    className="flex items-start gap-2 rounded-lg border border-amber-100 bg-amber-50 p-3"
                  >
                    <span className="mt-0.5 text-amber-500 text-sm">💡</span>
                    <div>
                      <p className="text-sm font-medium text-amber-900">
                        {mp.platform}
                      </p>
                      <p className="text-xs text-amber-700">{mp.reason}</p>
                    </div>
                  </div>
                ))}
            </div>
          </div>
        )}

        {/* Insight */}
        <div className="rounded-lg border border-indigo-100 bg-indigo-50 p-3 mb-6">
          <p className="text-xs text-indigo-700">
            <span className="font-semibold">Insight:</span> 병원 마케팅에서 영상
            콘텐츠는 텍스트 대비 3배 높은 전환율을 보입니다. YouTube, TikTok,
            小红书를 활용한 시술 과정 영상은 환자 신뢰도를 크게 향상시킵니다.
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
