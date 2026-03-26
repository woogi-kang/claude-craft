import { vi } from "vitest";

// Environment variables
process.env.NEXT_PUBLIC_SUPABASE_URL = "https://test.supabase.co";
process.env.SUPABASE_URL = "https://test.supabase.co";
process.env.SUPABASE_SECRET_KEY = "test-secret-key";
process.env.NEXT_PUBLIC_SUPABASE_PUBLISHABLE_KEY = "test-publishable-key";
process.env.RESEND_API_KEY = "test-resend-key";
process.env.WORKER_URL = "https://test-worker.example.com";
process.env.WORKER_API_KEY = "test-worker-api-key";
process.env.CRON_SECRET = "test-cron-secret";
process.env.LINE_CHANNEL_SECRET = "test-line-secret";
process.env.LINE_CHANNEL_ACCESS_TOKEN = "test-line-token";
process.env.WECHAT_TOKEN = "test-wechat-token";
process.env.WECHAT_APP_ID = "test-wechat-app-id";

// Global mock for Supabase browser client
vi.mock("@/lib/supabase/client", () => ({
  createClient: vi.fn(() => ({})),
}));

// Global mock for Resend
vi.mock("@/lib/resend", () => ({
  sendReportEmail: vi.fn().mockResolvedValue({ id: "mock-email-id" }),
  sendFollowUpEmail: vi.fn().mockResolvedValue({ id: "mock-email-id" }),
}));

// Reset mocks between tests
beforeEach(() => {
  vi.clearAllMocks();
});
