"""Tests for benchmark service."""

from unittest.mock import MagicMock, patch

import pytest

from app.services.benchmark import BenchmarkStats, compute_benchmark


class TestBenchmarkStats:
    def test_to_dict(self):
        stats = BenchmarkStats(
            top_25_avg=85.5,
            median=60.0,
            bottom_25_avg=30.123,
            total_count=100,
            your_percentile=75.678,
        )
        d = stats.to_dict()
        assert d["top_25_avg"] == 85.5
        assert d["median"] == 60.0
        assert d["bottom_25_avg"] == 30.1
        assert d["total_count"] == 100
        assert d["your_percentile"] == 75.7

    def test_to_dict_no_percentile(self):
        stats = BenchmarkStats(
            top_25_avg=80, median=50, bottom_25_avg=20, total_count=10
        )
        d = stats.to_dict()
        assert d["your_percentile"] is None


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
        # Chain: table().select().not_.is_().execute()
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
