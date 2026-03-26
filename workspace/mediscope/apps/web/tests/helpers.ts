import { vi } from "vitest";

/**
 * Creates a Request-like object with nextUrl support (mimics NextRequest).
 * This avoids importing NextRequest which requires the full Next.js runtime.
 */
export function createNextRequest(
  url: string,
  init?: RequestInit,
): Request & { nextUrl: URL } {
  const req = new Request(url, init);
  const parsedUrl = new URL(url);
  return Object.assign(req, { nextUrl: parsedUrl });
}
