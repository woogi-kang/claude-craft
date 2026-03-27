"""Benchmark API routes."""

from fastapi import APIRouter, Query

from ..services.benchmark import compute_benchmark

router = APIRouter(tags=["benchmark"])


@router.get("/benchmark")
async def get_benchmark(
    sido: str | None = Query(None, description="시/도 필터"),
    sggu: str | None = Query(None, description="시/군/구 필터"),
    region_name: str | None = Query(None, description="의료관광 권역명 필터"),
    your_score: float | None = Query(None, description="비교할 점수"),
):
    """Get benchmark statistics for beauty clinics."""
    stats = await compute_benchmark(
        sido=sido, sggu=sggu, region_name=region_name, your_score=your_score
    )
    if stats is None:
        return {"error": "No benchmark data available", "data": None}
    return {"data": stats.to_dict()}
