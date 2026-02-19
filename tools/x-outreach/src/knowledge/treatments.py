"""Treatment knowledge base loader.

Loads dermatology procedure data from the project's shared JSON dataset
and provides lookup by Japanese treatment name to Korean name, price
range, and description.
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path


@dataclass(frozen=True)
class TreatmentInfo:
    """Summarised treatment information for classification context."""

    procedure_id: int
    korean_name: str
    aliases: list[str] = field(default_factory=list)
    principle: str = ""
    average_price: str = ""
    downtime: str = ""
    duration: str = ""
    recommended_cycle: str = ""


# Japanese treatment name -> Korean procedure name mapping.
# This covers the most common terms seen in X posts.
JAPANESE_TO_KOREAN: dict[str, str] = {
    "ボトックス": "보톡스",
    "フィラー": "필러",
    "ヒアルロン酸": "히알루론산 필러",
    "ポテンツァ": "포텐자",
    "ピコレーザー": "피코레이저",
    "ピコトーニング": "피코토닝",
    "ダーマペン": "더마펜",
    "リジュラン": "리쥬란",
    "水光注射": "물광주사",
    "ハイフ": "하이푸(HIFU)",
    "シュリンク": "슈링크",
    "ウルセラ": "울쎄라",
    "レーザートーニング": "레이저토닝",
    "フラクショナルレーザー": "프락셔널 레이저",
    "シミ取り": "점/기미 제거",
    "肌管理": "피부관리",
    "エラボトックス": "사각턱 보톡스",
    "涙袋": "눈밑 필러",
    "唇フィラー": "입술 필러",
    "スキンボトックス": "스킨보톡스",
    "モピドス": "모피더스8",
    "モフィアス": "모피더스8",
    "オリジオ": "오리지오",
    "オンダリフト": "온다리프트",
    "糸リフト": "실리프팅",
    "脂肪溶解注射": "지방분해주사",
    "毛穴": "모공 관리",
    "ニキビ跡": "여드름 자국 치료",
    "美白": "미백 관리",
    "美肌": "피부 미인 관리",
}

# Concern -> recommended procedures mapping (for classification context)
CONCERN_TO_PROCEDURES: dict[str, list[str]] = {
    "シミ": ["ピコレーザー", "レーザートーニング", "ピコトーニング"],
    "毛穴": ["ポテンツァ", "ダーマペン", "フラクショナルレーザー"],
    "しわ": ["ボトックス", "ヒアルロン酸", "ハイフ"],
    "たるみ": ["ハイフ", "糸リフト", "ポテンツァ"],
    "ニキビ跡": ["ダーマペン", "フラクショナルレーザー", "ポテンツァ"],
    "美白": ["ピコトーニング", "水光注射", "レーザートーニング"],
    "保湿": ["水光注射", "リジュラン"],
    "エラ": ["エラボトックス"],
    "涙袋": ["ヒアルロン酸"],
    "唇": ["ヒアルロン酸"],
    "小顔": ["ボトックス", "ハイフ", "糸リフト"],
}


class TreatmentKnowledgeBase:
    """In-memory knowledge base for dermatology procedures.

    Call :meth:`load` once at startup; subsequent lookups are O(1).
    """

    def __init__(self) -> None:
        self._by_id: dict[int, TreatmentInfo] = {}
        self._by_name: dict[str, TreatmentInfo] = {}
        self._loaded: bool = False

    @property
    def is_loaded(self) -> bool:
        return self._loaded

    @property
    def count(self) -> int:
        return len(self._by_id)

    def load(self, json_path: str | Path | None = None) -> int:
        """Load procedures from the shared JSON dataset.

        Parameters
        ----------
        json_path:
            Path to ``dermatology_procedure_details_complete.json``.
            Defaults to the project-root data directory.

        Returns
        -------
        int
            Number of procedures loaded.
        """
        if json_path is None:
            # Resolve relative to claude-craft project root
            json_path = (
                Path(__file__).resolve().parent.parent.parent.parent.parent
                / "data"
                / "dermatology"
                / "dermatology_procedure_details_complete.json"
            )

        json_path = Path(json_path)
        if not json_path.exists():
            self._loaded = True
            return 0

        with open(json_path, encoding="utf-8") as f:
            data = json.load(f)

        details = data.get("details", [])
        for proc in details:
            info = TreatmentInfo(
                procedure_id=proc.get("procedure_id", 0),
                korean_name=proc.get("procedure_name", ""),
                aliases=proc.get("alias", []),
                principle=proc.get("principle", ""),
                average_price=proc.get("average_price", ""),
                downtime=proc.get("downtime", ""),
                duration=proc.get("duration", ""),
                recommended_cycle=proc.get("recommended_cycle", ""),
            )
            self._by_id[info.procedure_id] = info
            # Index by Korean name
            self._by_name[info.korean_name.lower()] = info
            # Index by each alias
            for alias in info.aliases:
                self._by_name[alias.lower()] = info

        self._loaded = True
        return len(details)

    def lookup_by_japanese(self, japanese_name: str) -> TreatmentInfo | None:
        """Look up a treatment by its Japanese name.

        Uses the ``JAPANESE_TO_KOREAN`` mapping to resolve to Korean,
        then searches the loaded dataset by Korean name or alias.
        """
        korean = JAPANESE_TO_KOREAN.get(japanese_name)
        if korean is None:
            return None
        return self._by_name.get(korean.lower())

    def lookup_by_name(self, name: str) -> TreatmentInfo | None:
        """Look up a treatment by Korean name or alias (case-insensitive)."""
        return self._by_name.get(name.lower())

    def get_procedures_for_concern(self, concern: str) -> list[str]:
        """Return Japanese procedure names recommended for a skin concern."""
        return CONCERN_TO_PROCEDURES.get(concern, [])

    def get_classification_context(self) -> str:
        """Build a compact summary string for use in classification prompts."""
        lines: list[str] = ["Treatment terminology (Japanese -> Korean):"]
        for jp, kr in sorted(JAPANESE_TO_KOREAN.items()):
            lines.append(f"  {jp} = {kr}")
        lines.append("")
        lines.append("Concern -> Procedures:")
        for concern, procs in sorted(CONCERN_TO_PROCEDURES.items()):
            lines.append(f"  {concern}: {', '.join(procs)}")
        return "\n".join(lines)
