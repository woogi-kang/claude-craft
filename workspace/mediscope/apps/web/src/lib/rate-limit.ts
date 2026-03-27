/**
 * In-memory rate limiter (IP-based).
 *
 * Limits:
 *   - 5 requests per hour per IP
 *   - 20 requests per day per IP
 *
 * Note: This resets on server restart and is per-instance.
 * For production multi-instance deployments, replace with Redis-backed limiter.
 */

interface RateLimitEntry {
  timestamps: number[];
}

const store = new Map<string, RateLimitEntry>();

const HOUR_MS = 60 * 60 * 1000;
const DAY_MS = 24 * HOUR_MS;
const HOURLY_LIMIT = 5;
const DAILY_LIMIT = 20;

// Periodic cleanup to prevent memory leak (every 10 minutes)
const CLEANUP_INTERVAL = 10 * 60 * 1000;
let lastCleanup = Date.now();

function cleanup() {
  const now = Date.now();
  if (now - lastCleanup < CLEANUP_INTERVAL) return;
  lastCleanup = now;

  const cutoff = now - DAY_MS;
  for (const [key, entry] of store) {
    entry.timestamps = entry.timestamps.filter((t) => t > cutoff);
    if (entry.timestamps.length === 0) {
      store.delete(key);
    }
  }
}

export interface RateLimitResult {
  allowed: boolean;
  reason?: string;
  retryAfterSeconds?: number;
}

export function checkRateLimit(ip: string): RateLimitResult {
  cleanup();

  const now = Date.now();
  const entry = store.get(ip) ?? { timestamps: [] };

  // Prune timestamps older than 24h
  entry.timestamps = entry.timestamps.filter((t) => t > now - DAY_MS);

  const hourlyCount = entry.timestamps.filter((t) => t > now - HOUR_MS).length;
  const dailyCount = entry.timestamps.length;

  if (hourlyCount >= HOURLY_LIMIT) {
    const oldestInHour = entry.timestamps.filter((t) => t > now - HOUR_MS)[0];
    const retryAfter = Math.ceil((oldestInHour + HOUR_MS - now) / 1000);
    return {
      allowed: false,
      reason: `시간당 ${HOURLY_LIMIT}회 제한을 초과했습니다`,
      retryAfterSeconds: retryAfter,
    };
  }

  if (dailyCount >= DAILY_LIMIT) {
    const oldestInDay = entry.timestamps[0];
    const retryAfter = Math.ceil((oldestInDay + DAY_MS - now) / 1000);
    return {
      allowed: false,
      reason: `일일 ${DAILY_LIMIT}회 제한을 초과했습니다`,
      retryAfterSeconds: retryAfter,
    };
  }

  entry.timestamps.push(now);
  store.set(ip, entry);

  return { allowed: true };
}
