"""Benchmark service: compute score distributions for beauty_clinics."""

import statistics

from ..db.supabase import get_supabase_client


class BenchmarkStats:
    def __init__(
        self,
        top_25_avg: float,
        median: float,
        bottom_25_avg: float,
        total_count: int,
        your_percentile: float | None = None,
    ):
        self.top_25_avg = top_25_avg
        self.median = median
        self.bottom_25_avg = bottom_25_avg
        self.total_count = total_count
        self.your_percentile = your_percentile

    def to_dict(self) -> dict:
        return {
            "top_25_avg": round(self.top_25_avg, 1),
            "median": round(self.median, 1),
            "bottom_25_avg": round(self.bottom_25_avg, 1),
            "total_count": self.total_count,
            "your_percentile": (
                round(self.your_percentile, 1) if self.your_percentile is not None else None
            ),
        }


async def compute_benchmark(
    sido: str | None = None,
    sggu: str | None = None,
    your_score: float | None = None,
) -> BenchmarkStats | None:
    """Compute benchmark stats from beauty_clinics latest_score.

    Filters by sido/sggu if provided.
    If your_score is given, computes what percentile it falls in.
    """
    sb = get_supabase_client()
    if sb is None:
        return None

    query = sb.table("beauty_clinics").select("latest_score")

    if sido:
        query = query.eq("sido", sido)
    if sggu:
        query = query.eq("sggu", sggu)

    # Only include clinics that have been scanned (non-null score)
    query = query.not_.is_("latest_score", "null")

    result = query.execute()
    rows = result.data or []

    if not rows:
        return None

    scores = sorted([r["latest_score"] for r in rows if r["latest_score"] is not None])
    if not scores:
        return None

    n = len(scores)

    # Top 25% (highest scores)
    top_start = max(0, n - n // 4)
    top_25 = scores[top_start:]
    top_25_avg = statistics.mean(top_25) if top_25 else 0

    # Bottom 25% (lowest scores)
    bottom_end = n // 4 or 1
    bottom_25 = scores[:bottom_end]
    bottom_25_avg = statistics.mean(bottom_25) if bottom_25 else 0

    median_val = statistics.median(scores)

    # Percentile: % of clinics scoring lower than your_score
    percentile = None
    if your_score is not None and n > 0:
        lower_count = sum(1 for s in scores if s < your_score)
        percentile = (lower_count / n) * 100

    return BenchmarkStats(
        top_25_avg=top_25_avg,
        median=median_val,
        bottom_25_avg=bottom_25_avg,
        total_count=n,
        your_percentile=percentile,
    )
