"use client";

import { useState } from "react";
import { useQuery } from "@tanstack/react-query";
import { ArrowLeft, Search } from "lucide-react";
import Link from "next/link";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Input } from "@/components/ui/input";
import { BEAUTY_CATEGORIES } from "@/lib/types/beauty";

interface ProcedureItem {
  id: string;
  category: string;
  name_ko: string;
  name_en: string | null;
  description_ko: string | null;
}

const CATEGORY_ICONS: Record<string, string> = {
  eyes: "👁",
  nose: "👃",
  face: "🧑",
  breast: "💎",
  body: "🏋️",
  skin: "✨",
  anti_aging: "⏳",
  hair: "💇",
};

export default function ProceduresPage() {
  const [selectedCategory, setSelectedCategory] = useState<string | null>(null);
  const [search, setSearch] = useState("");

  const { data, isLoading } = useQuery<ProcedureItem[]>({
    queryKey: ["procedures"],
    queryFn: () => fetch("/api/procedures").then((r) => r.json()),
  });

  const filtered = data?.filter((p) => {
    if (selectedCategory && p.category !== selectedCategory) return false;
    if (search) {
      const q = search.toLowerCase();
      return (
        p.name_ko.toLowerCase().includes(q) ||
        p.name_en?.toLowerCase().includes(q) ||
        p.description_ko?.toLowerCase().includes(q)
      );
    }
    return true;
  });

  const grouped = new Map<string, ProcedureItem[]>();
  for (const p of filtered ?? []) {
    const existing = grouped.get(p.category) ?? [];
    existing.push(p);
    grouped.set(p.category, existing);
  }

  return (
    <div className="min-h-screen bg-gradient-to-b from-blue-50 to-white">
      <div className="mx-auto max-w-6xl px-4 py-8">
        <Link
          href="/"
          className="mb-6 inline-flex items-center gap-1 text-sm text-muted-foreground hover:text-foreground"
        >
          <ArrowLeft className="h-4 w-4" />
          홈으로
        </Link>

        <div className="mb-8">
          <h1 className="text-3xl font-bold tracking-tight">시술 정보</h1>
          <p className="mt-2 text-muted-foreground">
            324개 미용시술의 상세 정보를 확인하세요. 원리, 효과, 부작용,
            다운타임까지 한눈에.
          </p>
        </div>

        {/* Category Grid */}
        <div className="mb-8 grid grid-cols-2 gap-3 sm:grid-cols-4">
          <button
            onClick={() => setSelectedCategory(null)}
            className={`rounded-lg border p-3 text-center transition-colors ${
              selectedCategory === null
                ? "border-blue-500 bg-blue-50 text-blue-700"
                : "border-gray-200 hover:border-blue-300 hover:bg-blue-50/50"
            }`}
          >
            <span className="text-xl">📋</span>
            <p className="mt-1 text-sm font-medium">전체</p>
            <p className="text-xs text-muted-foreground">
              {data?.length ?? 0}개
            </p>
          </button>
          {Object.entries(BEAUTY_CATEGORIES).map(([key, cat]) => {
            const count = data?.filter((p) => p.category === key).length ?? 0;
            return (
              <button
                key={key}
                onClick={() =>
                  setSelectedCategory(selectedCategory === key ? null : key)
                }
                className={`rounded-lg border p-3 text-center transition-colors ${
                  selectedCategory === key
                    ? "border-blue-500 bg-blue-50 text-blue-700"
                    : "border-gray-200 hover:border-blue-300 hover:bg-blue-50/50"
                }`}
              >
                <span className="text-xl">
                  {CATEGORY_ICONS[key] ?? cat.icon ?? "💊"}
                </span>
                <p className="mt-1 text-sm font-medium">{cat.name}</p>
                <p className="text-xs text-muted-foreground">{count}개</p>
              </button>
            );
          })}
        </div>

        {/* Search */}
        <div className="relative mb-6">
          <Search className="absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-muted-foreground" />
          <Input
            placeholder="시술명으로 검색..."
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            className="pl-10"
          />
        </div>

        {isLoading && (
          <div className="flex items-center justify-center py-20">
            <div className="h-8 w-8 animate-spin rounded-full border-4 border-blue-500 border-t-transparent" />
          </div>
        )}

        {/* Procedure List */}
        {[...grouped.entries()].map(([category, procedures]) => (
          <div key={category} className="mb-8">
            <h2 className="mb-4 flex items-center gap-2 text-xl font-semibold">
              <span>{CATEGORY_ICONS[category] ?? "💊"}</span>
              {BEAUTY_CATEGORIES[Number(category)]?.name ?? category}
              <Badge variant="secondary">{procedures.length}</Badge>
            </h2>
            <div className="grid gap-3 sm:grid-cols-2 lg:grid-cols-3">
              {procedures.map((p) => (
                <Link key={p.id} href={`/procedures/${p.id}`}>
                  <Card className="h-full transition-shadow hover:shadow-md">
                    <CardHeader className="pb-2">
                      <CardTitle className="text-base">{p.name_ko}</CardTitle>
                      {p.name_en && (
                        <p className="text-xs text-muted-foreground">
                          {p.name_en}
                        </p>
                      )}
                    </CardHeader>
                    {p.description_ko && (
                      <CardContent>
                        <p className="line-clamp-2 text-sm text-muted-foreground">
                          {p.description_ko}
                        </p>
                      </CardContent>
                    )}
                  </Card>
                </Link>
              ))}
            </div>
          </div>
        ))}

        {filtered?.length === 0 && !isLoading && (
          <Card>
            <CardContent className="py-10 text-center text-muted-foreground">
              검색 결과가 없습니다.
            </CardContent>
          </Card>
        )}
      </div>
    </div>
  );
}
