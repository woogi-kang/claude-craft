import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "그럼AI - 건강 AI 상담 서비스",
  description: "증상, 음식, 약 무엇이든 물어보세요! AI 기반 건강 상담 서비스",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="ko">
      <head>
        <link
          rel="stylesheet"
          href="https://cdn.jsdelivr.net/gh/orioncactus/pretendard@v1.3.9/dist/web/variable/pretendardvariable-dynamic-subset.min.css"
        />
      </head>
      <body className="font-sans antialiased">
        {children}
      </body>
    </html>
  );
}
