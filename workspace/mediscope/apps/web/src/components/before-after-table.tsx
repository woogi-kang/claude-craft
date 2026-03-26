import type { Category } from "@/lib/types";
import { CATEGORY_LABELS } from "@/lib/types";

type CategoryScores = Partial<Record<Category, number>>;

interface BeforeAfterTableProps {
  before: CategoryScores;
  current: CategoryScores;
  target?: CategoryScores;
}

const CATEGORIES: Category[] = [
  "technical_seo",
  "performance",
  "geo_aeo",
  "multilingual",
  "competitiveness",
];

function DeltaIndicator({ before, now }: { before: number; now: number }) {
  const diff = now - before;
  if (diff === 0) return <span className="text-muted-foreground">-</span>;
  if (diff > 0) {
    return <span className="text-green-600 font-medium">+{diff} ↑</span>;
  }
  return <span className="text-red-600 font-medium">{diff} ↓</span>;
}

export function BeforeAfterTable({
  before,
  current,
  target,
}: BeforeAfterTableProps) {
  const beforeTotal = CATEGORIES.reduce((s, c) => s + (before[c] ?? 0), 0);
  const currentTotal = CATEGORIES.reduce((s, c) => s + (current[c] ?? 0), 0);
  const targetTotal = target
    ? CATEGORIES.reduce((s, c) => s + (target[c] ?? 0), 0)
    : undefined;

  return (
    <div className="overflow-x-auto">
      <table className="w-full text-sm">
        <thead>
          <tr className="border-b text-left">
            <th className="pb-3 pr-4 font-medium">카테고리</th>
            <th className="pb-3 pr-4 font-medium text-center">Before</th>
            <th className="pb-3 pr-4 font-medium text-center">Now</th>
            <th className="pb-3 pr-4 font-medium text-center">변동</th>
            {target && <th className="pb-3 font-medium text-center">Target</th>}
          </tr>
        </thead>
        <tbody>
          {CATEGORIES.map((cat) => {
            const b = before[cat] ?? 0;
            const c = current[cat] ?? 0;
            return (
              <tr key={cat} className="border-b last:border-0">
                <td className="py-3 pr-4">{CATEGORY_LABELS[cat]}</td>
                <td className="py-3 pr-4 text-center text-muted-foreground">
                  {b}
                </td>
                <td className="py-3 pr-4 text-center font-medium">{c}</td>
                <td className="py-3 pr-4 text-center">
                  <DeltaIndicator before={b} now={c} />
                </td>
                {target && (
                  <td className="py-3 text-center text-muted-foreground">
                    {target[cat] ?? "-"}
                  </td>
                )}
              </tr>
            );
          })}
          <tr className="border-t-2 font-bold">
            <td className="py-3 pr-4">종합</td>
            <td className="py-3 pr-4 text-center text-muted-foreground">
              {beforeTotal}
            </td>
            <td className="py-3 pr-4 text-center">{currentTotal}</td>
            <td className="py-3 pr-4 text-center">
              <DeltaIndicator before={beforeTotal} now={currentTotal} />
            </td>
            {target && (
              <td className="py-3 text-center text-muted-foreground">
                {targetTotal}
              </td>
            )}
          </tr>
        </tbody>
      </table>
    </div>
  );
}
