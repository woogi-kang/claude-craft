"use client";

import * as React from "react";
import { useQuery } from "@tanstack/react-query";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import { Loader2 } from "lucide-react";

interface Procedure {
  id: string;
  name: string;
  name_ko: string;
}

const CONTENT_TYPES = [
  { id: "blog_post", label: "블로그 포스트" },
  { id: "procedure_intro", label: "시술 소개 페이지" },
  { id: "faq", label: "FAQ" },
  { id: "medical_tourism_guide", label: "의료관광 가이드" },
  { id: "sns_set", label: "SNS 세트" },
  { id: "infographic", label: "인포그래픽" },
] as const;

const LANGUAGES = [
  { value: "ko", label: "한국어" },
  { value: "en", label: "English" },
  { value: "ja", label: "日本語" },
  { value: "zh", label: "中文" },
] as const;

export interface GenerateFormData {
  procedure_name: string;
  content_types: string[];
  target_language: string;
  hospital_name: string;
  target_keywords: string[];
}

interface ContentGeneratorFormProps {
  onSubmit: (data: GenerateFormData) => void;
  isLoading: boolean;
}

export function ContentGeneratorForm({
  onSubmit,
  isLoading,
}: ContentGeneratorFormProps) {
  const [procedure, setProcedure] = React.useState("");
  const [selectedTypes, setSelectedTypes] = React.useState<string[]>([
    "blog_post",
    "faq",
    "sns_set",
  ]);
  const [language, setLanguage] = React.useState("ko");
  const [hospitalName, setHospitalName] = React.useState("");
  const [keywords, setKeywords] = React.useState("");

  const { data: procedures } = useQuery<Procedure[]>({
    queryKey: ["content-procedures"],
    queryFn: async () => {
      const res = await fetch("/api/content/procedures");
      if (!res.ok) throw new Error("Failed");
      return res.json();
    },
  });

  function toggleType(typeId: string) {
    setSelectedTypes((prev) =>
      prev.includes(typeId)
        ? prev.filter((t) => t !== typeId)
        : [...prev, typeId],
    );
  }

  function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    if (!procedure || selectedTypes.length === 0) return;

    onSubmit({
      procedure_name: procedure,
      content_types: selectedTypes,
      target_language: language,
      hospital_name: hospitalName,
      target_keywords: keywords
        .split(",")
        .map((k) => k.trim())
        .filter(Boolean),
    });
  }

  return (
    <Card>
      <CardHeader>
        <CardTitle className="text-lg">콘텐츠 설정</CardTitle>
      </CardHeader>
      <CardContent>
        <form onSubmit={handleSubmit} className="space-y-5">
          <div className="space-y-2">
            <Label>시술 선택</Label>
            <Select value={procedure} onValueChange={setProcedure}>
              <SelectTrigger>
                <SelectValue placeholder="시술을 선택하세요" />
              </SelectTrigger>
              <SelectContent>
                {procedures?.map((p) => (
                  <SelectItem key={p.id} value={p.name}>
                    {p.name_ko}
                  </SelectItem>
                ))}
              </SelectContent>
            </Select>
          </div>

          <div className="space-y-2">
            <Label>콘텐츠 유형</Label>
            <div className="grid grid-cols-2 gap-2">
              {CONTENT_TYPES.map((type) => (
                <label
                  key={type.id}
                  className="flex cursor-pointer items-center gap-2 rounded-md border px-3 py-2 text-sm hover:bg-accent/50"
                >
                  <input
                    type="checkbox"
                    checked={selectedTypes.includes(type.id)}
                    onChange={() => toggleType(type.id)}
                    className="h-4 w-4 rounded border-gray-300"
                  />
                  {type.label}
                </label>
              ))}
            </div>
          </div>

          <div className="space-y-2">
            <Label>언어</Label>
            <Select value={language} onValueChange={setLanguage}>
              <SelectTrigger>
                <SelectValue />
              </SelectTrigger>
              <SelectContent>
                {LANGUAGES.map((lang) => (
                  <SelectItem key={lang.value} value={lang.value}>
                    {lang.label}
                  </SelectItem>
                ))}
              </SelectContent>
            </Select>
          </div>

          <div className="space-y-2">
            <Label>병원명</Label>
            <Input
              value={hospitalName}
              onChange={(e) => setHospitalName(e.target.value)}
              placeholder="예: 강남 A피부과"
            />
          </div>

          <div className="space-y-2">
            <Label>타겟 키워드 (쉼표 구분)</Label>
            <Input
              value={keywords}
              onChange={(e) => setKeywords(e.target.value)}
              placeholder="예: 포텐자 강남, 포텐자 시술"
            />
          </div>

          <Button
            type="submit"
            className="w-full"
            disabled={isLoading || !procedure || selectedTypes.length === 0}
          >
            {isLoading ? (
              <>
                <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                생성 중...
              </>
            ) : (
              "AI 콘텐츠 생성"
            )}
          </Button>
        </form>
      </CardContent>
    </Card>
  );
}
