import type { Metadata } from "next";
import Script from "next/script";
import { Providers } from "@/components/providers";
import { ChatWidget } from "@/components/chat-widget";
import "./globals.css";

const GA_ID = "G-29ECQ5M1G6";

export const metadata: Metadata = {
  title: "CheckYourHospital - AI 병원 홈페이지 진단",
  description:
    "병원 홈페이지 URL을 입력하면 AI가 SEO/GEO/AEO를 종합 진단하여 해외 환자가 검색으로 찾을 수 있는 상태인지 즉시 리포트를 제공합니다.",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="ko">
      <head>
        <Script
          src={`https://www.googletagmanager.com/gtag/js?id=${GA_ID}`}
          strategy="afterInteractive"
        />
        <Script id="gtag-init" strategy="afterInteractive">
          {`
            window.dataLayer = window.dataLayer || [];
            function gtag(){dataLayer.push(arguments);}
            gtag('js', new Date());
            gtag('config', '${GA_ID}');
          `}
        </Script>
      </head>
      <body className="min-h-screen antialiased">
        <Providers>
          {children}
          <ChatWidget />
        </Providers>
      </body>
    </html>
  );
}
