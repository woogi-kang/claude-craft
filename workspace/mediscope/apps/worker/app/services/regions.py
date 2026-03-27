"""Medical tourism region mapping for Korean cities."""

MEDICAL_REGIONS: dict[str, set[str]] = {
    "강남/서초": {"강남구", "서초구"},
    "홍대/마포": {"마포구"},
    "명동/을지": {"중구"},
    "신촌/연남": {"서대문구"},
    "잠실/송파": {"송파구", "강동구"},
    "건대/성수": {"광진구", "성동구"},
    "압구정/청담": {"강남구"},  # 강남구 내 세분화는 dong으로
    "영등포/여의도": {"영등포구"},
    "부산 서면": {"부산진구", "연제구"},
    "부산 해운대": {"해운대구", "수영구"},
    "대구 수성": {"수성구"},
    "제주": {"제주시", "서귀포시"},
}


def get_region_name(sido: str, sggu: str) -> str:
    """sggu를 의료관광 권역명으로 변환."""
    for region_name, sggus in MEDICAL_REGIONS.items():
        if sggu in sggus:
            return region_name
    return f"{sido} {sggu}"  # 매핑 없으면 원래 시도+구군


def get_region_sggus(region_name: str) -> set[str]:
    """권역명에 해당하는 sggu 세트 반환."""
    return MEDICAL_REGIONS.get(region_name, set())
