"""Base types for check modules."""

from dataclasses import dataclass, field
from enum import Enum


class Grade(str, Enum):
    PASS = "pass"
    WARN = "warn"
    FAIL = "fail"


@dataclass
class CheckResult:
    name: str
    score: float  # 0.0 - 1.0
    grade: Grade
    details: dict = field(default_factory=dict)
    issues: list[str] = field(default_factory=list)
