"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { Search, Shield, Globe, BarChart3, Zap } from "lucide-react";

export default function LandingPage() {
  const [url, setUrl] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const router = useRouter();

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    setError("");

    if (!url.trim()) {
      setError("URL을 입력해주세요.");
      return;
    }

    try {
      new URL(url.startsWith("http") ? url : `https://${url}`);
    } catch {
      setError("올바른 URL을 입력해주세요.");
      return;
    }

    setLoading(true);
    try {
      const res = await fetch("/api/audits", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          url: url.startsWith("http") ? url : `https://${url}`,
        }),
      });

      if (!res.ok) {
        const data = await res.json();
        throw new Error(data.error || "진단 요청에 실패했습니다.");
      }

      const data = await res.json();
      router.push(`/scan/${data.id}`);
    } catch (err) {
      setError(
        err instanceof Error ? err.message : "진단 요청에 실패했습니다.",
      );
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="flex min-h-screen flex-col">
      {/* Hero Section */}
      <header className="border-b">
        <div className="mx-auto flex h-16 max-w-6xl items-center justify-between px-4">
          <h1 className="text-xl font-bold text-primary">CheckYourHospital</h1>
          <nav className="flex gap-4">
            <a
              href="#features"
              className="text-sm text-muted-foreground hover:text-foreground"
            >
              기능
            </a>
            <a
              href="#how-it-works"
              className="text-sm text-muted-foreground hover:text-foreground"
            >
              진단 방법
            </a>
          </nav>
        </div>
      </header>

      <main className="flex-1">
        {/* Hero */}
        <section className="flex flex-col items-center justify-center px-4 py-24 text-center">
          <h2 className="mb-4 max-w-3xl text-4xl font-bold tracking-tight sm:text-5xl">
            당신의 병원, 외국인 환자가
            <br />
            <span className="text-primary">검색으로 찾을 수 있나요?</span>
          </h2>
          <p className="mb-8 max-w-2xl text-lg text-muted-foreground">
            병원 홈페이지 URL을 입력하면 AI가 SEO/GEO/AEO를 종합 진단하여 해외
            환자가 검색으로 찾을 수 있는 상태인지 즉시 리포트를 제공합니다.
          </p>

          {/* URL Input Form */}
          <form
            onSubmit={handleSubmit}
            className="flex w-full max-w-xl flex-col gap-3 sm:flex-row"
          >
            <div className="relative flex-1">
              <Search className="absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-muted-foreground" />
              <Input
                type="text"
                placeholder="병원 홈페이지 URL 입력 (예: hospital.co.kr)"
                value={url}
                onChange={(e) => setUrl(e.target.value)}
                className="h-12 pl-10 text-base"
                disabled={loading}
              />
            </div>
            <Button type="submit" size="lg" disabled={loading} className="h-12">
              {loading ? "분석 중..." : "무료 진단 시작"}
            </Button>
          </form>
          {error && <p className="mt-2 text-sm text-destructive">{error}</p>}
          <p className="mt-3 text-xs text-muted-foreground">
            무료로 15개 항목을 진단합니다. 이메일 불필요.
          </p>
        </section>

        {/* Features */}
        <section id="features" className="border-t bg-muted/50 px-4 py-20">
          <div className="mx-auto max-w-6xl">
            <h3 className="mb-12 text-center text-3xl font-bold">
              종합 진단 항목
            </h3>
            <div className="grid gap-6 sm:grid-cols-2 lg:grid-cols-4">
              {[
                {
                  icon: Shield,
                  title: "기술 SEO",
                  desc: "robots.txt, sitemap, meta tags, 구조화 데이터 등 10개 항목 분석",
                },
                {
                  icon: Zap,
                  title: "성능 분석",
                  desc: "Core Web Vitals (LCP, CLS, INP) 및 모바일 반응형 점검",
                },
                {
                  icon: Globe,
                  title: "GEO/AEO",
                  desc: "AI 검색(ChatGPT, Perplexity) 노출 여부 및 구조화 데이터 진단",
                },
                {
                  icon: BarChart3,
                  title: "경쟁력 벤치마크",
                  desc: "동일 진료과 분포 기반 비교 분석으로 현재 위치 파악",
                },
              ].map((f) => (
                <Card key={f.title}>
                  <CardHeader>
                    <f.icon className="mb-2 h-8 w-8 text-primary" />
                    <CardTitle className="text-lg">{f.title}</CardTitle>
                  </CardHeader>
                  <CardContent>
                    <CardDescription>{f.desc}</CardDescription>
                  </CardContent>
                </Card>
              ))}
            </div>
          </div>
        </section>

        {/* How it works */}
        <section id="how-it-works" className="px-4 py-20">
          <div className="mx-auto max-w-4xl">
            <h3 className="mb-12 text-center text-3xl font-bold">
              진단 프로세스
            </h3>
            <div className="grid gap-8 sm:grid-cols-3">
              {[
                {
                  step: "1",
                  title: "URL 입력",
                  desc: "병원 홈페이지 주소를 입력하세요",
                },
                {
                  step: "2",
                  title: "AI 분석",
                  desc: "15개 항목을 자동으로 분석합니다",
                },
                {
                  step: "3",
                  title: "리포트 확인",
                  desc: "종합 점수와 개선 방안을 확인하세요",
                },
              ].map((s) => (
                <div key={s.step} className="text-center">
                  <div className="mx-auto mb-4 flex h-12 w-12 items-center justify-center rounded-full bg-primary text-lg font-bold text-primary-foreground">
                    {s.step}
                  </div>
                  <h4 className="mb-2 font-semibold">{s.title}</h4>
                  <p className="text-sm text-muted-foreground">{s.desc}</p>
                </div>
              ))}
            </div>
          </div>
        </section>
      </main>

      <footer className="border-t py-8 text-center text-sm text-muted-foreground">
        &copy; 2026 CheckYourHospital. All rights reserved.
      </footer>
    </div>
  );
}
