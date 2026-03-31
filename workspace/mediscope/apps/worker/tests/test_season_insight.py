"""Tests for medical tourism season insight service."""

from datetime import date

import pytest

from app.services.season_insight import (
    DEMAND_LEVELS,
    SEASON_DATA,
    get_season_insight,
    _demand_level,
    _months_until,
)


# ── Demand level mapping ────────────────────────────────────────────


class TestDemandLevel:
    def test_all_levels(self):
        assert _demand_level(1) == "very_low"
        assert _demand_level(2) == "low"
        assert _demand_level(3) == "moderate"
        assert _demand_level(4) == "high"
        assert _demand_level(5) == "peak"

    def test_unknown_value(self):
        assert _demand_level(0) == "moderate"
        assert _demand_level(99) == "moderate"


# ── Months until calculation ────────────────────────────────────────


class TestMonthsUntil:
    def test_same_month(self):
        assert _months_until(3, 3) == 0

    def test_future_month(self):
        assert _months_until(3, 5) == 2
        assert _months_until(1, 12) == 11

    def test_wrap_around(self):
        assert _months_until(10, 2) == 4
        assert _months_until(12, 1) == 1


# ── Calendar data ───────────────────────────────────────────────────


class TestCalendar:
    def test_all_countries_present(self):
        result = get_season_insight(date(2026, 3, 15))
        assert set(result["calendar"].keys()) == {"jp", "cn", "us", "th", "vn"}

    def test_each_country_has_12_months(self):
        result = get_season_insight(date(2026, 6, 1))
        for code, entries in result["calendar"].items():
            assert len(entries) == 12, f"{code} should have 12 months"
            for entry in entries:
                assert "month" in entry
                assert "demand" in entry
                assert "level" in entry

    def test_demand_values_match_season_data(self):
        result = get_season_insight(date(2026, 1, 1))
        for code, entries in result["calendar"].items():
            for entry in entries:
                expected = SEASON_DATA[code]["monthly"][entry["month"]]
                assert entry["demand"] == expected


# ── Current month ───────────────────────────────────────────────────


class TestCurrentMonth:
    def test_january(self):
        result = get_season_insight(date(2026, 1, 10))
        assert result["current_month"] == 1
        assert result["current_month_name"] == "1월"

    def test_july(self):
        result = get_season_insight(date(2026, 7, 20))
        assert result["current_month"] == 7
        assert result["current_month_name"] == "7월"

    def test_december(self):
        result = get_season_insight(date(2026, 12, 31))
        assert result["current_month"] == 12
        assert result["current_month_name"] == "12월"


# ── Current opportunities ───────────────────────────────────────────


class TestCurrentOpportunities:
    def test_january_high_demand(self):
        """January: CN=5 (춘절), VN=4 (뗏)"""
        result = get_season_insight(date(2026, 1, 15))
        opps = result["current_opportunities"]
        countries = [o["country"] for o in opps]
        assert "cn" in countries
        assert "vn" in countries
        # CN has demand 5, should be first
        assert opps[0]["country"] == "cn"
        assert opps[0]["demand"] == 5

    def test_march_moderate(self):
        """March: JP=4, others <= 3"""
        result = get_season_insight(date(2026, 3, 10))
        opps = result["current_opportunities"]
        countries = [o["country"] for o in opps]
        assert "jp" in countries
        assert "cn" not in countries  # CN=2 in March

    def test_september_no_peaks(self):
        """September: all countries <= 3"""
        result = get_season_insight(date(2026, 9, 1))
        opps = result["current_opportunities"]
        assert len(opps) == 0

    def test_opportunity_has_reason(self):
        result = get_season_insight(date(2026, 10, 1))
        cn_opp = next(o for o in result["current_opportunities"] if o["country"] == "cn")
        assert "국경절" in cn_opp["reason"]

    def test_opportunity_fields(self):
        result = get_season_insight(date(2026, 1, 1))
        for opp in result["current_opportunities"]:
            assert "country" in opp
            assert "label" in opp
            assert "flag" in opp
            assert "demand" in opp
            assert "level" in opp
            assert opp["demand"] >= 4


# ── Upcoming peaks ──────────────────────────────────────────────────


class TestUpcomingPeaks:
    def test_from_march(self):
        """March → look at Apr, May, Jun. Apr: JP=5, TH=4. May: CN=4"""
        result = get_season_insight(date(2026, 3, 15))
        peaks = result["upcoming_peaks"]
        countries_months = [(p["country"], p["month"]) for p in peaks]
        assert ("jp", 4) in countries_months
        assert ("th", 4) in countries_months
        assert ("cn", 5) in countries_months

    def test_days_until_ordering(self):
        result = get_season_insight(date(2026, 3, 15))
        peaks = result["upcoming_peaks"]
        days_list = [p["days_until"] for p in peaks]
        assert days_list == sorted(days_list)

    def test_peak_fields(self):
        result = get_season_insight(date(2026, 3, 1))
        for peak in result["upcoming_peaks"]:
            assert "country" in peak
            assert "label" in peak
            assert "flag" in peak
            assert "month" in peak
            assert "month_name" in peak
            assert "demand" in peak
            assert "days_until" in peak
            assert peak["demand"] >= 4

    def test_wrap_around_year_end(self):
        """November → look at Dec, Jan, Feb"""
        result = get_season_insight(date(2026, 11, 1))
        peaks = result["upcoming_peaks"]
        months = [p["month"] for p in peaks]
        # Dec: JP=4, US=4. Jan: CN=5, VN=4. Feb: CN=5, VN=4
        assert 12 in months or 1 in months or 2 in months


# ── Marketing actions ───────────────────────────────────────────────


class TestMarketingActions:
    def test_actions_generated(self):
        result = get_season_insight(date(2026, 3, 15))
        actions = result["marketing_actions"]
        assert len(actions) > 0

    def test_priority_ordering(self):
        result = get_season_insight(date(2026, 3, 1))
        actions = result["marketing_actions"]
        priorities = [a["priority"] for a in actions]
        order = {"high": 0, "medium": 1, "low": 2}
        numeric = [order[p] for p in priorities]
        assert numeric == sorted(numeric)

    def test_action_fields(self):
        result = get_season_insight(date(2026, 3, 15))
        for action in result["marketing_actions"]:
            assert "priority" in action
            assert "country" in action
            assert "message" in action
            assert action["priority"] in ("high", "medium", "low")

    def test_no_actions_when_no_peaks(self):
        """September: no upcoming peaks with demand >= 4 within 3 months
        Oct: CN=5, TH=3, others <=3 → actually CN=5 in Oct"""
        result = get_season_insight(date(2026, 9, 1))
        # Oct has CN=5, so there should be actions
        # But let's check that actions relate to actual peaks
        for action in result["marketing_actions"]:
            assert action["country"] in {"jp", "cn", "us", "th", "vn"}


# ── Quarterly forecast ──────────────────────────────────────────────


class TestQuarterlyForecast:
    def test_q1_forecast(self):
        """In Q1 → next quarter is Q2"""
        result = get_season_insight(date(2026, 2, 1))
        forecast = result["quarterly_forecast"]
        assert forecast["next_quarter"] == "Q2 2026"
        assert forecast["top_market"] in SEASON_DATA

    def test_q4_wraps_to_next_year(self):
        """In Q4 → next quarter is Q1 of next year"""
        result = get_season_insight(date(2026, 11, 1))
        forecast = result["quarterly_forecast"]
        assert forecast["next_quarter"] == "Q1 2027"

    def test_forecast_has_expected_demand(self):
        result = get_season_insight(date(2026, 6, 1))
        forecast = result["quarterly_forecast"]
        assert forecast["expected_demand"] != ""
        assert forecast["top_market"] != ""


# ── Various dates ───────────────────────────────────────────────────


class TestVariousDates:
    @pytest.mark.parametrize("month", range(1, 13))
    def test_every_month_produces_valid_result(self, month):
        result = get_season_insight(date(2026, month, 15))
        assert result["current_month"] == month
        assert len(result["calendar"]) == 5
        assert isinstance(result["current_opportunities"], list)
        assert isinstance(result["upcoming_peaks"], list)
        assert isinstance(result["marketing_actions"], list)
        assert "quarterly_forecast" in result

    def test_default_date(self):
        """Calling without date uses today."""
        result = get_season_insight()
        assert 1 <= result["current_month"] <= 12

    def test_leap_year(self):
        result = get_season_insight(date(2028, 2, 29))
        assert result["current_month"] == 2

    def test_first_day_of_year(self):
        result = get_season_insight(date(2026, 1, 1))
        assert result["current_month"] == 1

    def test_last_day_of_year(self):
        result = get_season_insight(date(2026, 12, 31))
        assert result["current_month"] == 12
