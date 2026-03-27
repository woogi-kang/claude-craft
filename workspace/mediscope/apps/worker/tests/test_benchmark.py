"""Tests for benchmark service."""

from unittest.mock import MagicMock, patch

import pytest

from app.services.benchmark import BenchmarkStats, compute_benchmark, _build_distribution
from app.services.regions import get_region_name, get_region_sggus


class TestBenchmarkStats:
    def test_to_dict(self):
        stats = BenchmarkStats(
            top_25_avg=85.5,
            median=60.0,
            bottom_25_avg=30.123,
            total_count=100,
            your_percentile=75.678,
            region_name="강남/서초",
            distribution=[{"range": "0-9", "count": 5}],
            rank=25,
        )
        d = stats.to_dict()
        assert d["top_25_avg"] == 85.5
        assert d["median"] == 60.0
        assert d["bottom_25_avg"] == 30.1
        assert d["total_count"] == 100
        assert d["your_percentile"] == 75.7
        assert d["region_name"] == "강남/서초"
        assert d["distribution"] == [{"range": "0-9", "count": 5}]
        assert d["rank"] == 25

    def test_to_dict_no_percentile(self):
        stats = BenchmarkStats(
            top_25_avg=80, median=50, bottom_25_avg=20, total_count=10
        )
        d = stats.to_dict()
        assert d["your_percentile"] is None
        assert d["region_name"] == ""
        assert d["distribution"] == []
        assert d["rank"] is None


class TestBuildDistribution:
    def test_basic(self):
        scores = [5, 15, 25, 35, 45, 55, 65, 75, 85, 95]
        dist = _build_distribution(scores)
        assert len(dist) == 10
        for b in dist:
            assert b["count"] == 1

    def test_all_same_bin(self):
        scores = [50, 51, 52, 53]
        dist = _build_distribution(scores)
        assert dist[5]["count"] == 4
        assert sum(b["count"] for b in dist) == 4

    def test_score_100(self):
        scores = [100]
        dist = _build_distribution(scores)
        assert dist[9]["count"] == 1  # 100 goes to last bin


class TestRegions:
    def test_known_region(self):
        assert get_region_name("서울특별시", "강남구") == "강남/서초"
        assert get_region_name("서울특별시", "서초구") == "강남/서초"
        assert get_region_name("서울특별시", "마포구") == "홍대/마포"

    def test_unknown_region(self):
        assert get_region_name("인천광역시", "남동구") == "인천광역시 남동구"

    def test_get_region_sggus(self):
        sggus = get_region_sggus("강남/서초")
        assert sggus == {"강남구", "서초구"}

    def test_get_region_sggus_unknown(self):
        assert get_region_sggus("unknown") == set()


@pytest.mark.asyncio
class TestComputeBenchmark:
    async def test_returns_none_without_supabase(self):
        with patch(
            "app.services.benchmark.get_supabase_client", return_value=None
        ):
            result = await compute_benchmark()
        assert result is None

    async def test_returns_stats_with_data(self):
        mock_client = MagicMock()
        mock_query = MagicMock()
        mock_client.table.return_value = mock_query
        mock_query.select.return_value = mock_query
        mock_query.not_ = MagicMock()
        mock_query.not_.is_.return_value = mock_query
        mock_query.not_.is_.return_value.execute.return_value = MagicMock(
            data=[
                {"latest_score": 30},
                {"latest_score": 50},
                {"latest_score": 70},
                {"latest_score": 90},
            ]
        )

        with patch(
            "app.services.benchmark.get_supabase_client", return_value=mock_client
        ):
            result = await compute_benchmark(your_score=60)

        assert result is not None
        assert result.total_count == 4
        assert result.median == 60.0  # median of [30,50,70,90]
        assert result.your_percentile == 50.0  # 2 out of 4 are below 60
        # scores > 60 are 70, 90 → higher_count=2 → rank=3
        assert result.rank == 3
        assert len(result.distribution) == 10
        assert result.distribution[3]["count"] == 1  # 30 → bin 30-39
        assert result.distribution[5]["count"] == 1  # 50 → bin 50-59

    async def test_returns_none_with_empty_data(self):
        mock_client = MagicMock()
        mock_query = MagicMock()
        mock_client.table.return_value = mock_query
        mock_query.select.return_value = mock_query
        mock_query.not_ = MagicMock()
        mock_query.not_.is_.return_value = mock_query
        mock_query.not_.is_.return_value.execute.return_value = MagicMock(data=[])

        with patch(
            "app.services.benchmark.get_supabase_client", return_value=mock_client
        ):
            result = await compute_benchmark()
        assert result is None

    async def test_region_name_resolved(self):
        mock_client = MagicMock()
        mock_query = MagicMock()
        mock_client.table.return_value = mock_query
        mock_query.select.return_value = mock_query
        mock_query.in_.return_value = mock_query
        mock_query.eq.return_value = mock_query
        mock_query.not_ = MagicMock()
        mock_query.not_.is_.return_value = mock_query
        mock_query.not_.is_.return_value.execute.return_value = MagicMock(
            data=[{"latest_score": 50}, {"latest_score": 80}]
        )

        with patch(
            "app.services.benchmark.get_supabase_client", return_value=mock_client
        ):
            result = await compute_benchmark(sido="서울특별시", sggu="강남구")

        assert result is not None
        assert result.region_name == "강남/서초"

    async def test_region_name_param(self):
        mock_client = MagicMock()
        mock_query = MagicMock()
        mock_client.table.return_value = mock_query
        mock_query.select.return_value = mock_query
        mock_query.in_.return_value = mock_query
        mock_query.not_ = MagicMock()
        mock_query.not_.is_.return_value = mock_query
        mock_query.not_.is_.return_value.execute.return_value = MagicMock(
            data=[{"latest_score": 40}]
        )

        with patch(
            "app.services.benchmark.get_supabase_client", return_value=mock_client
        ):
            result = await compute_benchmark(region_name="강남/서초")

        assert result is not None
        assert result.region_name == "강남/서초"
