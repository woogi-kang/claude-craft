#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_CATALOG = ROOT / "references" / "font-catalog.json"

PROFILE_TAGS = {
    "product": {"ai", "b2b", "clean", "dashboard", "data", "developer", "docs", "modern", "product", "saas", "startup", "tech", "ui"},
    "editorial": {"art", "brand", "calm", "culture", "editorial", "essay", "formal", "institution", "literary", "premium", "serif", "story", "warm"},
    "playful": {"casual", "cheerful", "community", "cozy", "cute", "education", "family", "friendly", "lifestyle", "playful", "soft", "wellness", "youth"},
    "impact": {"bold", "campaign", "commerce", "condensed", "display", "ecommerce", "event", "gaming", "hero", "impact", "poster", "promo", "street"},
}

KEYWORDS = {
    "ai": ["ai", "인공지능", "llm", "agent", "에이전트"],
    "b2b": ["b2b", "기업", "엔터프라이즈", "업무툴"],
    "brand": ["brand", "브랜드", "브랜딩", "스토리"],
    "campaign": ["campaign", "캠페인", "이벤트", "프로모션", "런칭"],
    "clean": ["clean", "깔끔", "정갈", "단정", "미니멀", "심플"],
    "code": ["code", "코드", "개발", "개발자", "terminal", "터미널", "cli"],
    "community": ["community", "커뮤니티", "소셜"],
    "cozy": ["cozy", "포근", "따뜻", "아늑", "감성"],
    "dashboard": ["dashboard", "대시보드", "admin", "관리자", "운영툴"],
    "data": ["data", "데이터", "분석", "지표", "메트릭"],
    "docs": ["docs", "문서", "가이드", "헬프", "고객센터"],
    "editorial": ["editorial", "에디토리얼", "매거진", "저널", "긴 글"],
    "ecommerce": ["commerce", "이커머스", "쇼핑", "세일", "상품"],
    "formal": ["formal", "공식", "기관", "정책", "법률", "신뢰"],
    "friendly": ["friendly", "친근", "부드", "말랑"],
    "impact": ["impact", "강렬", "강한", "임팩트", "묵직"],
    "landing": ["landing", "랜딩", "마이크로사이트"],
    "literary": ["literary", "문학", "시적인", "에세이", "서정"],
    "modern": ["modern", "모던", "현대", "세련"],
    "playful": ["playful", "귀여", "발랄", "유쾌", "키즈"],
    "portfolio": ["portfolio", "포트폴리오"],
    "premium": ["premium", "프리미엄", "고급", "럭셔리"],
    "product": ["product", "프로덕트", "서비스", "앱", "웹앱", "ui"],
    "saas": ["saas", "스타트업"],
    "tech": ["tech", "테크", "기술", "엔지니어"],
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Recommend a compact Korean webfont role system.")
    parser.add_argument("--theme", required=True, help="Korean or English theme, product type, or mood.")
    parser.add_argument("--catalog", default=str(DEFAULT_CATALOG), help="Path to font-catalog.json.")
    parser.add_argument("--json", action="store_true", help="Emit structured JSON.")
    parser.add_argument("--limit", type=int, default=2, help="Number of alternatives per role.")
    parser.add_argument("--code", action="store_true", help="Force a code font recommendation.")
    return parser.parse_args()


def load_catalog(path: str) -> dict[str, Any]:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def infer_tags(theme: str) -> set[str]:
    normalized = theme.lower()
    tags: set[str] = set()
    for tag, words in KEYWORDS.items():
        if tag in normalized:
            tags.add(tag)
            continue
        if any(word.lower() in normalized for word in words):
            tags.add(tag)
    if re.search(r"\b(ai|saas|b2b|dashboard|admin|dev|developer|cli)\b", normalized):
        tags.update({"product", "tech"})
    return tags or {"product", "modern", "clean"}


def infer_profile(tags: set[str]) -> str:
    scores = {
        name: len(tags & profile_tags)
        for name, profile_tags in PROFILE_TAGS.items()
    }
    return max(scores, key=lambda name: (scores[name], name == "product"))


def role_candidates(fonts: list[dict[str, Any]], role: str) -> list[dict[str, Any]]:
    return [font for font in fonts if role in font.get("roles", [])]


def score_font(font: dict[str, Any], tags: set[str], profile: str, role: str) -> int:
    font_tags = set(font.get("tags", []))
    score = int(font.get("priority", 0))
    score += 5 * len(font_tags & tags)
    score += 2 * len(font_tags & PROFILE_TAGS[profile])
    if role == "body" and font["id"] in {"pretendard-variable", "spoqa-han-sans-neo", "ibm-plex-sans-kr", "noto-sans-kr"}:
        score += 8
    if role == "heading" and profile == "impact" and font["id"] in {"black-han-sans", "do-hyeon", "gmarket-sans"}:
        score += 12
    if role == "heading" and profile == "playful" and font["id"] in {"jua", "nanum-square-round", "single-day"}:
        score += 10
    if role == "heading" and profile == "editorial" and font["id"] in {"hahmlet", "maruburi", "noto-serif-kr"}:
        score += 10
    if role == "heading" and profile == "product":
        product_heading_bonus = {
            "nanum-square-neo": 14,
            "goorm-sans": 8,
            "pretendard-variable": 6,
        }
        score += product_heading_bonus.get(font["id"], 0)
    if role == "heading" and "landing" in tags and font["id"] in {"nanum-square-neo", "gmarket-sans"}:
        score += 8
    return score


def pick(fonts: list[dict[str, Any]], tags: set[str], profile: str, role: str, exclude: set[str] | None = None) -> dict[str, Any]:
    exclude = exclude or set()
    candidates = [font for font in role_candidates(fonts, role) if font["id"] not in exclude]
    return sorted(candidates, key=lambda font: score_font(font, tags, profile, role), reverse=True)[0]


def family_for(font: dict[str, Any], role: str) -> str:
    if role == "heading":
        return font.get("family_heading") or font["family_body"]
    return font["family_body"]


def stylesheet_for(font: dict[str, Any]) -> str:
    if font.get("stylesheet_url"):
        return f'@import url("{font["stylesheet_url"]}");'
    return font.get("style_css", "")


def should_include_code(tags: set[str], forced: bool) -> bool:
    code_tags = {"ai", "b2b", "code", "dashboard", "data", "developer", "docs", "tech"}
    return forced or bool(tags & code_tags)


def build_recommendation(catalog: dict[str, Any], theme: str, force_code: bool, limit: int) -> dict[str, Any]:
    fonts = catalog["fonts"]
    tags = infer_tags(theme)
    profile = infer_profile(tags)
    body = pick(fonts, tags, profile, "body")
    heading = pick(fonts, tags, profile, "heading", exclude={body["id"]})
    code = pick(fonts, tags, profile, "code") if should_include_code(tags, force_code) else None
    accent = pick(fonts, tags, profile, "accent", exclude={heading["id"]}) if profile in {"playful", "impact"} else None

    selected = [body, heading] + ([code] if code else []) + ([accent] if accent else [])
    deduped = []
    seen = set()
    for font in selected:
        if font and font["id"] not in seen:
            deduped.append(font)
            seen.add(font["id"])

    alternatives = {
        role: [
            {"id": font["id"], "name": font["name"], "fit": font["fit"]}
            for font in sorted(role_candidates(fonts, role), key=lambda font: score_font(font, tags, profile, role), reverse=True)
            if font["id"] not in {body["id"], heading["id"], code["id"] if code else "", accent["id"] if accent else ""}
        ][:limit]
        for role in ["body", "heading"]
    }

    return {
        "theme": theme,
        "tags": sorted(tags),
        "profile": profile,
        "roles": {
            "body": body,
            "heading": heading,
            "code": code,
            "accent": accent,
        },
        "stylesheets": [stylesheet_for(font) for font in deduped if stylesheet_for(font)],
        "families": {
            "body": family_for(body, "body"),
            "heading": family_for(heading, "heading"),
            "code": family_for(code, "body") if code else "\"SFMono-Regular\", Consolas, monospace",
            "accent": family_for(accent, "heading") if accent else None,
        },
        "alternatives": alternatives,
        "license_note": catalog["license_note"],
    }


def css_variables(rec: dict[str, Any]) -> str:
    families = rec["families"]
    lines = [
        ":root {",
        f"  --font-body: {families['body']};",
        f"  --font-heading: {families['heading']};",
        f"  --font-code: {families['code']};",
    ]
    if families.get("accent"):
        lines.append(f"  --font-accent: {families['accent']};")
    lines.extend([
        "}",
        "",
        "body { font-family: var(--font-body); }",
        "h1, h2, h3, .display, .headline { font-family: var(--font-heading); }",
        "code, pre, kbd, samp { font-family: var(--font-code); }",
        "table, .metric { font-variant-numeric: tabular-nums; }",
    ])
    return "\n".join(lines)


def emit_markdown(rec: dict[str, Any]) -> str:
    roles = rec["roles"]
    code_name = roles["code"]["name"] if roles["code"] else "none"
    accent_name = roles["accent"]["name"] if roles["accent"] else "none"
    imports = "\n".join(rec["stylesheets"])
    alt_body = ", ".join(item["name"] for item in rec["alternatives"]["body"]) or "none"
    alt_heading = ", ".join(item["name"] for item in rec["alternatives"]["heading"]) or "none"

    return f"""# Korean Typography Recommendation

Mood read: `{rec['theme']}` maps to `{rec['profile']}` with tags `{', '.join(rec['tags'])}`.

Recommended roles:
- Body: {roles['body']['name']} - {roles['body']['fit']}
- Heading: {roles['heading']['name']} - {roles['heading']['fit']}
- Code: {code_name}
- Accent: {accent_name}

Stylesheet imports:
```css
{imports}
```

CSS variables:
```css
{css_variables(rec)}
```

Alternatives:
- Body: {alt_body}
- Heading: {alt_heading}

License note: {rec['license_note']}
"""


def main() -> None:
    args = parse_args()
    catalog = load_catalog(args.catalog)
    rec = build_recommendation(catalog, args.theme, args.code, args.limit)
    if args.json:
        print(json.dumps(rec, ensure_ascii=False, indent=2))
    else:
        print(emit_markdown(rec))


if __name__ == "__main__":
    main()
