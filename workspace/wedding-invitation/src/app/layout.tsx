import type { Metadata, Viewport } from 'next';
import { Noto_Serif_KR, Noto_Sans_KR } from 'next/font/google';
import { Toaster } from 'sonner';
import { OG_METADATA } from '@/lib/constants';
import './globals.css';

const notoSerifKR = Noto_Serif_KR({
  subsets: ['latin'],
  weight: ['400', '500', '600', '700'],
  variable: '--font-serif',
  display: 'swap',
});

const notoSansKR = Noto_Sans_KR({
  subsets: ['latin'],
  weight: ['300', '400', '500', '700'],
  variable: '--font-sans',
  display: 'swap',
});

export const viewport: Viewport = {
  width: 'device-width',
  initialScale: 1,
  maximumScale: 1,
  userScalable: false,
  themeColor: '#FFFCF9',
};

export const metadata: Metadata = {
  metadataBase: new URL(OG_METADATA.url),
  title: OG_METADATA.title,
  description: OG_METADATA.description,
  openGraph: {
    type: 'website',
    title: OG_METADATA.title,
    description: OG_METADATA.description,
    images: [
      {
        url: OG_METADATA.image,
        width: 800,
        height: 400,
        alt: OG_METADATA.title,
      },
    ],
    url: OG_METADATA.url,
  },
  twitter: {
    card: 'summary_large_image',
    title: OG_METADATA.title,
    description: OG_METADATA.description,
    images: [OG_METADATA.image],
  },
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="ko">
      <head>
        <link rel="icon" href="/favicon.ico" />
        <meta name="format-detection" content="telephone=no" />
      </head>
      <body
        className={`${notoSerifKR.variable} ${notoSansKR.variable} font-sans antialiased`}
      >
        {children}
        <Toaster position="bottom-center" richColors />
      </body>
    </html>
  );
}
