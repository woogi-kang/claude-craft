import { Printer, FileDown, ExternalLink } from "lucide-react";
import { Button } from "@/components/ui/button";

interface ReportHeaderProps {
  url: string;
  createdAt: string;
  reportUrl: string | null;
  auditId: string;
}

export function ReportHeader({
  url,
  createdAt,
  reportUrl,
  auditId,
}: ReportHeaderProps) {
  const formattedDate = new Date(createdAt).toLocaleDateString("ko-KR", {
    year: "numeric",
    month: "long",
    day: "numeric",
    hour: "2-digit",
    minute: "2-digit",
  });

  return (
    <header className="border-b border-slate-200 pb-6 mb-8">
      <div className="flex items-start justify-between gap-4 flex-wrap">
        <div>
          <div className="flex items-center gap-2 mb-3">
            <div className="flex h-8 w-8 items-center justify-center rounded-lg bg-slate-900">
              <span className="text-sm font-bold text-white tracking-tight">
                C
              </span>
            </div>
            <span className="text-lg font-semibold tracking-tight text-slate-900">
              CheckYourHospital
            </span>
          </div>
          <h1 className="text-2xl font-bold text-slate-900 mb-1">
            SEO 진단 리포트
          </h1>
          <div className="flex items-center gap-2 text-sm text-slate-500">
            <ExternalLink className="h-3.5 w-3.5" aria-hidden="true" />
            <a
              href={url}
              target="_blank"
              rel="noopener noreferrer"
              className="hover:text-slate-700 underline underline-offset-2 break-all"
            >
              {url}
            </a>
          </div>
          <p className="text-sm text-slate-400 mt-1">진단일: {formattedDate}</p>
        </div>
        <div className="flex items-center gap-2 shrink-0">
          {reportUrl && (
            <Button variant="outline" size="sm" asChild>
              <a href={reportUrl} target="_blank" rel="noopener noreferrer">
                <FileDown className="h-4 w-4" aria-hidden="true" />
                PDF
              </a>
            </Button>
          )}
          <Button variant="outline" size="sm" asChild>
            <a
              href={`/api/reports/${auditId}`}
              target="_blank"
              rel="noopener noreferrer"
            >
              <Printer className="h-4 w-4" aria-hidden="true" />
              인쇄
            </a>
          </Button>
        </div>
      </div>
    </header>
  );
}
