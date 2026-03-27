"""Benchmark service: compute score distributions for beauty_clinics."""

import statistics

from ..db.supabase import get_supabase_client
from .regions import get_region_name, get_region_sggus


class BenchmarkStats:
    def __init__(
        self,
        top_25_avg: float,
        median: float,
        bottom_25_avg: float,
        total_count: int,
        your_percentile: float | None = None,
        region_name: str = "",
        distribution: list[dict] | None = None,
        rank: int | None = None,
    ):
        self.top_25_avg = top_25_avg
        self.median = median
        self.bottom_25_avg = bottom_25_avg
        self.total_count = total_count
        self.your_percentile = your_percentile
        self.region_name = region_name
        self.distribution = distribution or []
        self.rank = rank

    def to_dict(self) -> dict:
        return {
            "top_25_avg": round(self.top_25_avg, 1),
            "median": round(self.median, 1),
            "bottom_25_avg": round(self.bottom_25_avg, 1),
            "total_count": self.total_count,
            "your_percentile": (
                round(self.your_percentile, 1) if self.your_percentile is not None else None
            ),
            "region_name": self.region_name,
            "distribution": self.distribution,
            "rank": self.rank,
        }


def _build_distribution(scores: list[float]) -> list[dict]:
    """Build 10-point histogram bins from scores."""
    bins = [{"range": f"{i * 10}-{i * 10 + 9}", "count": 0} for i in range(10)]
    for s in scores:
        idx = min(int(s // 10), 9)
        bins[idx]["count"] += 1
    return bins


async def compute_benchmark(
    sido: str | None = None,
    sggu: str | None = None,
    region_name: str | None = None,
    your_score: float | None = None,
) -> BenchmarkStats | None:
    """Compute benchmark stats from beauty_clinics latest_score.

    Filters by sido/sggu if provided, or by region_name (medical tourism region).
    If your_score is given, computes what percentile it falls in.
    """
    sb = get_supabase_client()
    if sb is None:
        return None

    # Resolve region_name to sggu set for querying
    resolved_region_name = ""
    filter_sggus: set[str] | None = None

    if region_name:
        filter_sggus = get_region_sggus(region_name)
        resolved_region_name = region_name
    elif sido and sggu:
        resolved_region_name = get_region_name(sido, sggu)
        # Get all sggus in same region for broader comparison
        filter_sggus = get_region_sggus(resolved_region_name)

    try:
        query = sb.table("beauty_clinics").select("latest_score")

        if filter_sggus:
            # Filter by all sggus in the region
            query = query.in_("sggu", list(filter_sggus))
            if sido:
                query = query.eq("sido", sido)
        else:
            if sido:
                query = query.eq("sido", sido)
            if sggu:
                query = query.eq("sggu", sggu)

        query = query.not_.is_("latest_score", "null")

        result = query.execute()
        rows = result.data or []
    except Exception:
        return None

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

    # Distribution histogram
    distribution = _build_distribution(scores)

    # Percentile and rank
    percentile = None
    rank = None
    if your_score is not None and n > 0:
        lower_count = sum(1 for s in scores if s < your_score)
        percentile = (lower_count / n) * 100
        # Rank: how many score higher + 1
        higher_count = sum(1 for s in scores if s > your_score)
        rank = higher_count + 1

    return BenchmarkStats(
        top_25_avg=top_25_avg,
        median=median_val,
        bottom_25_avg=bottom_25_avg,
        total_count=n,
        your_percentile=percentile,
        region_name=resolved_region_name,
        distribution=distribution,
        rank=rank,
    )
