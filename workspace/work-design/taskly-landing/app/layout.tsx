import type { Metadata } from 'next';
import './globals.css';

export const metadata: Metadata = {
  title: 'Taskly - AI-Powered Task Management',
  description: 'Stop managing tasks. Start completing them. AI that prioritizes what matters.',
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <head>
        <link rel="preconnect" href="https://fonts.googleapis.com" />
        <link rel="preconnect" href="https://fonts.gstatic.com" crossOrigin="anonymous" />
        <link
          href="https://fonts.googleapis.com/css2?family=Albert+Sans:wght@100..900&family=DM+Sans:opsz,wght@9..40,100..1000&display=swap"
          rel="stylesheet"
        />
      </head>
      <body className="antialiased">
        {children}
      </body>
    </html>
  );
}
