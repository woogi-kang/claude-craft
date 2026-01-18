import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  output: 'export',
  images: {
    unoptimized: true,
  },
  // GitHub Pages 배포 시 주석 해제
  // basePath: '/wedding-invitation',
};

export default nextConfig;
