"""Tests for configuration validation."""
from __future__ import annotations

import pytest
from pydantic import ValidationError

from src.config import (
    ClassifierConfig,
    RateLimitConfig,
    SchedulingConfig,
)


class TestRateLimitConfigValidation:
    def test_valid_config(self):
        config = RateLimitConfig(max_responses_per_hour=30, max_responses_per_day=200)
        assert config.max_responses_per_hour == 30

    def test_invalid_hourly_limit(self):
        with pytest.raises(ValidationError):
            RateLimitConfig(max_responses_per_hour=0)

    def test_invalid_daily_limit(self):
        with pytest.raises(ValidationError):
            RateLimitConfig(max_responses_per_day=0)


class TestSchedulingConfigValidation:
    def test_valid_hours(self):
        config = SchedulingConfig(active_start_hour=9, active_end_hour=22)
        assert config.active_start_hour == 9

    def test_invalid_start_hour(self):
        with pytest.raises(ValidationError):
            SchedulingConfig(active_start_hour=25)

    def test_invalid_end_hour(self):
        with pytest.raises(ValidationError):
            SchedulingConfig(active_end_hour=-1)


class TestClassifierConfigValidation:
    def test_valid_threshold(self):
        config = ClassifierConfig(confidence_threshold=0.7)
        assert config.confidence_threshold == 0.7

    def test_invalid_threshold_high(self):
        with pytest.raises(ValidationError):
            ClassifierConfig(confidence_threshold=1.5)

    def test_invalid_threshold_low(self):
        with pytest.raises(ValidationError):
            ClassifierConfig(confidence_threshold=-0.1)
