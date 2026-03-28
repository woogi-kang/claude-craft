/** GA4 event tracking helpers */

type GtagEvent = {
  action: string;
  category: string;
  label?: string;
  value?: number;
};

export function trackEvent({ action, category, label, value }: GtagEvent) {
  if (typeof window === "undefined") return;
  const gtag = (window as unknown as Record<string, unknown>).gtag as
    | ((...args: unknown[]) => void)
    | undefined;
  if (!gtag) return;
  gtag("event", action, {
    event_category: category,
    event_label: label,
    value,
  });
}

// Pre-defined events
export const analytics = {
  scanStarted: (url: string) =>
    trackEvent({ action: "scan_started", category: "scan", label: url }),

  scanCompleted: (url: string, score: number, grade: string) =>
    trackEvent({
      action: "scan_completed",
      category: "scan",
      label: `${url} | ${grade}`,
      value: score,
    }),

  reportViewed: (auditId: string, score: number) =>
    trackEvent({
      action: "report_viewed",
      category: "report",
      label: auditId,
      value: score,
    }),

  gateUnlocked: (auditId: string) =>
    trackEvent({
      action: "gate_unlocked",
      category: "conversion",
      label: auditId,
    }),

  leadSubmitted: (auditId: string) =>
    trackEvent({
      action: "lead_submitted",
      category: "conversion",
      label: auditId,
    }),

  subscriptionCreated: (auditId: string) =>
    trackEvent({
      action: "subscription_created",
      category: "conversion",
      label: auditId,
    }),

  chatOpened: () =>
    trackEvent({ action: "chat_opened", category: "engagement" }),

  pdfDownloaded: (auditId: string) =>
    trackEvent({
      action: "pdf_downloaded",
      category: "engagement",
      label: auditId,
    }),
};
