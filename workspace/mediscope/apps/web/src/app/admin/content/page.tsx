"use client";

import * as React from "react";
import { useMutation } from "@tanstack/react-query";
import { Bot } from "lucide-react";
import {
  ContentGeneratorForm,
  type GenerateFormData,
} from "@/components/admin/content-generator-form";
import { ContentResult } from "@/components/admin/content-result";
import { ImageGallery } from "@/components/admin/image-gallery";

interface ContentItem {
  content_type: string;
  title: string;
  body: string;
  word_count: number;
  seo_score?: number;
  warnings?: string[];
}

interface GeneratedImage {
  id: string;
  label: string;
  url: string;
}

interface GenerateResponse {
  contents: ContentItem[];
  images: GeneratedImage[];
}

export default function AdminContentPage() {
  const [results, setResults] = React.useState<ContentItem[]>([]);
  const [images, setImages] = React.useState<GeneratedImage[]>([]);

  const mutation = useMutation({
    mutationFn: async (data: GenerateFormData): Promise<GenerateResponse> => {
      const requests = data.content_types.map((ct) =>
        fetch("/api/content/generate", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            content_type: ct,
            procedure_name: data.procedure_name,
            hospital_name: data.hospital_name,
            target_language: data.target_language,
            target_keywords: data.target_keywords,
          }),
        }).then((res) => {
          if (!res.ok) throw new Error(`Failed to generate ${ct}`);
          return res.json();
        }),
      );

      const responses = await Promise.all(requests);

      const contents: ContentItem[] = responses.map((r, i) => ({
        content_type: data.content_types[i],
        title: r.title ?? `${data.content_types[i]} 콘텐츠`,
        body: r.body ?? r.content ?? "",
        word_count: r.word_count ?? (r.body ?? r.content ?? "").length,
        seo_score: r.seo_score,
        warnings: r.warnings ?? [],
      }));

      const allImages: GeneratedImage[] = responses.flatMap(
        (r) => r.images ?? [],
      );

      return { contents, images: allImages };
    },
    onSuccess: (data) => {
      setResults(data.contents);
      setImages(data.images);
    },
  });

  async function handleDownloadAll() {
    if (images.length === 0) return;
    const res = await fetch("/api/content/image", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ image_ids: images.map((img) => img.id) }),
    });
    if (!res.ok) return;
    const blob = await res.blob();
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = "content-images.zip";
    a.click();
    URL.revokeObjectURL(url);
  }

  return (
    <div>
      <div className="mb-6 flex items-center gap-2">
        <Bot className="h-6 w-6 text-primary" />
        <h1 className="text-2xl font-bold">AI 콘텐츠 생성</h1>
      </div>

      <div className="grid gap-6 lg:grid-cols-[380px_1fr]">
        <div>
          <ContentGeneratorForm
            onSubmit={(data) => mutation.mutate(data)}
            isLoading={mutation.isPending}
          />
        </div>

        <div className="space-y-6">
          {mutation.isPending && (
            <div className="flex flex-col items-center justify-center rounded-lg border border-dashed py-16 text-muted-foreground">
              <div className="mb-3 h-8 w-8 animate-spin rounded-full border-4 border-primary border-t-transparent" />
              <p className="text-sm">AI가 콘텐츠를 생성하고 있습니다...</p>
              <p className="mt-1 text-xs">
                선택한 유형에 따라 1~3분 소요될 수 있습니다
              </p>
            </div>
          )}

          {mutation.isError && (
            <div className="rounded-md border border-red-200 bg-red-50 p-4 text-sm text-red-800">
              콘텐츠 생성에 실패했습니다. 다시 시도해주세요.
            </div>
          )}

          {results.length > 0 && !mutation.isPending && (
            <ContentResult results={results} />
          )}

          {images.length > 0 && !mutation.isPending && (
            <ImageGallery images={images} onDownloadAll={handleDownloadAll} />
          )}

          {!mutation.isPending && results.length === 0 && (
            <div className="flex flex-col items-center justify-center rounded-lg border border-dashed py-16 text-muted-foreground">
              <Bot className="mb-3 h-10 w-10" />
              <p className="text-sm">
                시술과 콘텐츠 유형을 선택한 후 생성 버튼을 클릭하세요
              </p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
