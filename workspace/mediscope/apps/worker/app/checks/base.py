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
    fail_type: str = "site_issue"  # site_issue | system_limit | api_error | not_applicable
    display_name: str = ""  # 고객 친화적 이름 (빈 값이면 name 사용)
    description: str = ""  # 왜 중요한지 한 줄 설명
    recommendation: str = ""  # 개선 방법
    issues: list[str] = field(default_factory=list)
    details: dict = field(default_factory=dict)
