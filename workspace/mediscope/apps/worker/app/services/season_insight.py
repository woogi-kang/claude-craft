"""Medical tourism season insight service.

Provides country-specific monthly demand data and marketing timing
recommendations based on the current date.
"""

from __future__ import annotations

from datetime import date

# 국가별 월별 의료관광 수요 (1-5, 5가 성수기)
# 한국관광공사 통계 + 업계 일반적 패턴 기반
SEASON_DATA: dict[str, dict] = {
    "jp": {
        "label": "일본",
        "flag": "🇯🇵",
        "monthly": {
            1: 2, 2: 2, 3: 4, 4: 5, 5: 3,
            6: 3, 7: 5, 8: 5, 9: 3, 10: 3, 11: 3, 12: 4,
        },
        "peak_reasons": {
            4: "벚꽃 시즌 + 골든위크(4/29~5/5)",
            7: "여름방학",
            8: "여름방학 + 오봉야스미",
            12: "연말 연휴",
        },
    },
    "cn": {
        "label": "중국",
        "flag": "🇨🇳",
        "monthly": {
            1: 5, 2: 5, 3: 2, 4: 3, 5: 4,
            6: 2, 7: 3, 8: 3, 9: 2, 10: 5, 11: 3, 12: 2,
        },
        "peak_reasons": {
            1: "춘절 연휴",
            2: "춘절 연휴",
            5: "노동절 연휴",
            10: "국경절 연휴(10/1~7)",
        },
    },
    "us": {
        "label": "미국",
        "flag": "🇺🇸",
        "monthly": {
            1: 2, 2: 2, 3: 3, 4: 3, 5: 3,
            6: 4, 7: 5, 8: 5, 9: 3, 10: 2, 11: 3, 12: 4,
        },
        "peak_reasons": {
            7: "여름 휴가",
            8: "여름 휴가",
            12: "크리스마스 + 연말 휴가",
        },
    },
    "th": {
        "label": "태국",
        "flag": "🇹🇭",
        "monthly": {
            1: 2, 2: 2, 3: 3, 4: 4, 5: 3,
            6: 2, 7: 3, 8: 3, 9: 2, 10: 3, 11: 3, 12: 3,
        },
        "peak_reasons": {
            4: "송크란(태국 새해, 4/13~15)",
        },
    },
    "vn": {
        "label": "베트남",
        "flag": "🇻🇳",
        "monthly": {
            1: 4, 2: 4, 3: 2, 4: 3, 5: 3,
            6: 3, 7: 4, 8: 4, 9: 3, 10: 2, 11: 2, 12: 3,
        },
        "peak_reasons": {
            1: "뗏(음력 설)",
            2: "뗏 연휴",
            7: "여름방학",
            8: "여름방학",
        },
    },
}

DEMAND_LEVELS: dict[int, str] = {
    1: "very_low",
    2: "low",
    3: "moderate",
    4: "high",
    5: "peak",
}

MONTH_NAMES = {
    1: "1월", 2: "2월", 3: "3월", 4: "4월", 5: "5월", 6: "6월",
    7: "7월", 8: "8월", 9: "9월", 10: "10월", 11: "11월", 12: "12월",
}

QUARTER_NAMES = {1: "Q1", 2: "Q2", 3: "Q3", 4: "Q4"}


def _demand_level(value: int) -> str:
    return DEMAND_LEVELS.get(value, "moderate")


def _months_until(current_month: int, target_month: int) -> int:
    if target_month > current_month:
        return target_month - current_month
    if target_month == current_month:
        return 0
    return 12 - current_month + target_month


def _days_approx(months: int, current_day: int, current_month_days: int = 30) -> int:
    if months == 0:
        return 0
    remaining_in_month = current_month_days - current_day
    return remaining_in_month + (months - 1) * 30


def get_season_insight(current_date: date | None = None) -> dict:
    """Generate medical tourism season insight based on the current date."""
    if current_date is None:
        current_date = date.today()

    month = current_date.month
    year = current_date.year

    # Build calendar for all countries
    calendar: dict[str, list[dict]] = {}
    for code, info in SEASON_DATA.items():
        monthly = []
        for m in range(1, 13):
            demand = info["monthly"][m]
            monthly.append({
                "month": m,
                "demand": demand,
                "level": _demand_level(demand),
            })
        calendar[code] = monthly

    # Current opportunities: countries with demand >= 4 this month
    current_opportunities = []
    for code, info in SEASON_DATA.items():
        demand = info["monthly"][month]
        if demand >= 4:
            reason = info["peak_reasons"].get(month, "")
            current_opportunities.append({
                "country": code,
                "label": info["label"],
                "flag": info["flag"],
                "demand": demand,
                "level": _demand_level(demand),
                "reason": reason,
            })
    current_opportunities.sort(key=lambda x: x["demand"], reverse=True)

    # Upcoming peaks: next 3 months, demand >= 4
    upcoming_peaks = []
    for offset in range(1, 4):
        target_month = (month - 1 + offset) % 12 + 1
        for code, info in SEASON_DATA.items():
            demand = info["monthly"][target_month]
            if demand >= 4:
                reason = info["peak_reasons"].get(target_month, "")
                days = _days_approx(offset, current_date.day)
                upcoming_peaks.append({
                    "country": code,
                    "label": info["label"],
                    "flag": info["flag"],
                    "month": target_month,
                    "month_name": MONTH_NAMES[target_month],
                    "demand": demand,
                    "level": _demand_level(demand),
                    "reason": reason,
                    "days_until": days,
                })
    upcoming_peaks.sort(key=lambda x: (x["days_until"], -x["demand"]))

    # Marketing actions
    marketing_actions = _build_marketing_actions(month, current_date.day, upcoming_peaks)

    # Quarterly forecast
    next_q_start = ((month - 1) // 3 + 1) * 3 + 1
    if next_q_start > 12:
        next_q_start = 1
        next_q_year = year + 1
    else:
        next_q_year = year
    next_q_num = (next_q_start - 1) // 3 + 1
    next_quarter_label = f"{QUARTER_NAMES[next_q_num]} {next_q_year}"

    # Find top market for next quarter
    best_market = ""
    best_demand = 0
    for code, info in SEASON_DATA.items():
        q_demand = sum(
            info["monthly"][(next_q_start - 1 + i) % 12 + 1] for i in range(3)
        )
        if q_demand > best_demand:
            best_demand = q_demand
            best_market = code

    best_label = SEASON_DATA[best_market]["label"] if best_market else ""
    expected = f"{best_label} 시장 성수기 진입" if best_market else ""

    return {
        "current_month": month,
        "current_month_name": MONTH_NAMES[month],
        "calendar": calendar,
        "current_opportunities": current_opportunities,
        "upcoming_peaks": upcoming_peaks,
        "marketing_actions": marketing_actions,
        "quarterly_forecast": {
            "next_quarter": next_quarter_label,
            "top_market": best_market,
            "expected_demand": expected,
        },
    }


def _build_marketing_actions(
    month: int, day: int, upcoming_peaks: list[dict]
) -> list[dict]:
    actions: list[dict] = []

    # Actions for upcoming peaks
    for peak in upcoming_peaks:
        days = peak["days_until"]
        country = peak["country"]
        label = SEASON_DATA[country]["label"]
        reason = peak["reason"]
        month_name = peak["month_name"]

        if days <= 30:
            priority = "high"
            if reason:
                msg = f"{month_name} {reason} 대비 {label} 프로모션 준비 (D-{days})"
            else:
                msg = f"{month_name} 성수기 대비 {label} 마케팅 강화 (D-{days})"
        elif days <= 60:
            priority = "medium"
            if reason:
                msg = f"{month_name} {reason} 대비 {label} 콘텐츠 강화"
            else:
                msg = f"{month_name} 수요 증가 대비 {label} 콘텐츠 준비"
        else:
            priority = "low"
            if reason:
                msg = f"{month_name} {reason} 대비 {label} 사전 기획"
            else:
                msg = f"{month_name} 수요 증가 대비 {label} 사전 기획"

        # Avoid duplicate messages for same country
        if not any(a["country"] == country and a["priority"] == priority for a in actions):
            actions.append({
                "priority": priority,
                "country": country,
                "message": msg,
            })

    # Sort: high > medium > low
    priority_order = {"high": 0, "medium": 1, "low": 2}
    actions.sort(key=lambda x: priority_order.get(x["priority"], 3))

    return actions
