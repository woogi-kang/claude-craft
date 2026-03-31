"use client";

import * as React from "react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Tabs, TabsList, TabsTrigger, TabsContent } from "@/components/ui/tabs";
import { Copy, FileEdit, FileCode, AlertTriangle, Check } from "lucide-react";

interface ContentItem {
  content_type: string;
  title: string;
  body: string;
  word_count: number;
  seo_score?: number;
  warnings?: string[];
}

interface ContentResultProps {
  results: ContentItem[];
}

const TYPE_LABELS: Record<string, string> = {
  blog_post: "블로그",
  procedure_intro: "시술 소개",
  faq: "FAQ",
  medical_tourism_guide: "의료관광 가이드",
  sns_set: "SNS",
  infographic: "인포그래픽",
};

export function ContentResult({ results }: ContentResultProps) {
  const [editingIndex, setEditingIndex] = React.useState<number | null>(null);
  const [editedBodies, setEditedBodies] = React.useState<
    Record<number, string>
  >({});
  const [copiedId, setCopiedId] = React.useState<string | null>(null);

  if (results.length === 0) return null;

  function getBody(index: number) {
    return editedBodies[index] ?? results[index].body;
  }

  async function copyToClipboard(text: string, id: string) {
    await navigator.clipboard.writeText(text);
    setCopiedId(id);
    setTimeout(() => setCopiedId(null), 2000);
  }

  function toHtml(markdown: string) {
    return markdown
      .replace(/^### (.+)$/gm, "<h3>$1</h3>")
      .replace(/^## (.+)$/gm, "<h2>$1</h2>")
      .replace(/^# (.+)$/gm, "<h1>$1</h1>")
      .replace(/\*\*(.+?)\*\*/g, "<strong>$1</strong>")
      .replace(/\n/g, "<br/>");
  }

  return (
    <Card>
      <CardHeader>
        <CardTitle className="text-lg">생성 결과</CardTitle>
      </CardHeader>
      <CardContent>
        <Tabs defaultValue={results[0].content_type}>
          <TabsList className="mb-4">
            {results.map((item) => (
              <TabsTrigger key={item.content_type} value={item.content_type}>
                {TYPE_LABELS[item.content_type] ?? item.content_type}
              </TabsTrigger>
            ))}
          </TabsList>

          {results.map((item, index) => (
            <TabsContent key={item.content_type} value={item.content_type}>
              <div className="space-y-4">
                <div className="flex items-center justify-between">
                  <h3 className="font-semibold">{item.title}</h3>
                  <div className="flex items-center gap-2">
                    <span className="text-sm text-muted-foreground">
                      {item.word_count.toLocaleString()}자
                    </span>
                    {item.seo_score != null && (
                      <Badge
                        variant={item.seo_score >= 80 ? "success" : "warning"}
                      >
                        SEO {item.seo_score}/100
                      </Badge>
                    )}
                  </div>
                </div>

                {editingIndex === index ? (
                  <div className="space-y-2">
                    <textarea
                      className="min-h-[300px] w-full rounded-md border border-input bg-background px-3 py-2 text-sm focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring"
                      value={getBody(index)}
                      onChange={(e) =>
                        setEditedBodies((prev) => ({
                          ...prev,
                          [index]: e.target.value,
                        }))
                      }
                    />
                    <Button
                      size="sm"
                      variant="outline"
                      onClick={() => setEditingIndex(null)}
                    >
                      완료
                    </Button>
                  </div>
                ) : (
                  <div className="max-h-[400px] overflow-y-auto rounded-md border bg-muted/30 p-4 text-sm whitespace-pre-wrap">
                    {getBody(index)}
                  </div>
                )}

                {item.warnings && item.warnings.length > 0 ? (
                  <div className="flex items-start gap-2 rounded-md border border-yellow-200 bg-yellow-50 p-3 text-sm text-yellow-800">
                    <AlertTriangle className="mt-0.5 h-4 w-4 shrink-0" />
                    <div>
                      <p className="font-medium">의료광고법 경고</p>
                      <ul className="mt-1 list-inside list-disc">
                        {item.warnings.map((w, i) => (
                          <li key={i}>{w}</li>
                        ))}
                      </ul>
                    </div>
                  </div>
                ) : (
                  <div className="flex items-center gap-2 text-sm text-green-700">
                    <Check className="h-4 w-4" />
                    의료광고법 경고: 0건
                  </div>
                )}

                <div className="flex gap-2">
                  <Button
                    size="sm"
                    variant="outline"
                    onClick={() => setEditingIndex(index)}
                  >
                    <FileEdit className="mr-1 h-3.5 w-3.5" />
                    편집
                  </Button>
                  <Button
                    size="sm"
                    variant="outline"
                    onClick={() =>
                      copyToClipboard(getBody(index), `md-${index}`)
                    }
                  >
                    {copiedId === `md-${index}` ? (
                      <Check className="mr-1 h-3.5 w-3.5" />
                    ) : (
                      <Copy className="mr-1 h-3.5 w-3.5" />
                    )}
                    마크다운 복사
                  </Button>
                  <Button
                    size="sm"
                    variant="outline"
                    onClick={() =>
                      copyToClipboard(toHtml(getBody(index)), `html-${index}`)
                    }
                  >
                    {copiedId === `html-${index}` ? (
                      <Check className="mr-1 h-3.5 w-3.5" />
                    ) : (
                      <FileCode className="mr-1 h-3.5 w-3.5" />
                    )}
                    HTML 복사
                  </Button>
                </div>
              </div>
            </TabsContent>
          ))}
        </Tabs>
      </CardContent>
    </Card>
  );
}
