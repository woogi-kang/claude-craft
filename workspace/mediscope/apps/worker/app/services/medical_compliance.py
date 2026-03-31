"""Medical advertising compliance checker for Korean and Japanese regulations."""

import re
from collections import defaultdict

from bs4 import BeautifulSoup

# Page type classification (reuse patterns from multilingual_analyzer)
_PROCEDURE_RE = re.compile(
    r"(시술|치료|수술|treatment|procedure|surgery|laser|filler|botox|리프팅|필러|보톡스|레이저)",
    re.I,
)
_REVIEW_RE = re.compile(
    r"(후기|review|before.?after|사례|testimonial|결과|체험)", re.I,
)

# === Korean Medical Act Article 56 ===

KR_EXAGGERATION = [
    re.compile(r"최고의?", re.I),
    re.compile(r"최상의?", re.I),
    re.compile(r"100\s*%", re.I),
    re.compile(r"보장", re.I),
    re.compile(r"완벽", re.I),
    re.compile(r"확실", re.I),
    re.compile(r"1등", re.I),
    re.compile(r"유일", re.I),
    re.compile(r"독보적", re.I),
    re.compile(r"업계\s*최초", re.I),
]

KR_COMPARISON = [
    re.compile(r"가장\s+\w+[한]", re.I),
    re.compile(r"제일\s+\w+[한]", re.I),
    re.compile(r"최초의", re.I),
]

KR_DISCOUNT = [
    re.compile(r"무료\s*(시술|상담|체험)", re.I),
    re.compile(r"[5-9]0%\s*할인", re.I),
    re.compile(r"파격\s*할인", re.I),
]

KR_PROHIBITED: dict[str, list[re.Pattern]] = {
    "exaggeration": KR_EXAGGERATION,
    "comparison": KR_COMPARISON,
    "discount": KR_DISCOUNT,
}

# Required disclosures on procedure pages
KR_REQUIRED_DISCLOSURES = [
    re.compile(r"부작용"),
    re.compile(r"합병증"),
    re.compile(r"주의사항"),
    re.compile(r"개인\s*차"),
    re.compile(r"결과.*다를\s*수"),
]

# === Japanese Medical Act ===

JP_TESTIMONIAL = [
    re.compile(r"体験談", re.I),
    re.compile(r"患者.*の声", re.I),
    re.compile(r"お客様の声", re.I),
]

JP_COMPARISON = [
    re.compile(r"日本一", re.I),
    re.compile(r"No\.\s*1", re.I),
    re.compile(r"ナンバーワン", re.I),
    re.compile(r"業界初", re.I),
]

JP_BEFORE_AFTER = [
    re.compile(r"ビフォー.*アフター", re.I),
    re.compile(r"before.*after", re.I),
    re.compile(r"施術前.*施術後", re.I),
]

# === Rule metadata ===

_RULE_META: dict[str, dict] = {
    "kr_exaggeration": {
        "law": "의료법 제56조 (과대광고 금지)",
        "description": "과장 표현 사용",
    },
    "kr_comparison": {
        "law": "의료법 제56조 (비교광고 금지)",
        "description": "근거 없는 비교 표현",
    },
    "kr_discount": {
        "law": "의료법 제27조의3 (경제적 이익 제공 금지)",
        "description": "과도한 할인/무료 광고",
    },
    "kr_no_side_effects": {
        "law": "의료법 시행령 제23조의2",
        "description": "시술 페이지에 부작용/주의사항 미고지",
    },
    "kr_before_after": {
        "law": "의료법 제56조제2항",
        "description": "Before/After 사진 규제",
    },
    "jp_testimonial": {
        "law": "医療法 (체험담 광고 규제)",
        "description": "환자 체험담을 광고로 사용",
    },
    "jp_comparison": {
        "law": "医療法 (비교 광고 금지)",
        "description": "비교 광고 표현",
    },
    "jp_before_after": {
        "law": "医療法 (술전술후 사진 규제)",
        "description": "Before/After 사진에 설명 부재",
    },
    "global_privacy": {
        "law": "GDPR / 개인정보보호법",
        "description": "개인정보 처리방침 다국어 미비",
    },
}

# Privacy-related keywords
_PRIVACY_KEYWORDS = [
    re.compile(r"개인정보", re.I),
    re.compile(r"privacy\s*policy", re.I),
    re.compile(r"プライバシー", re.I),
    re.compile(r"隐私", re.I),
    re.compile(r"個人情報", re.I),
]

# Language detection helpers
_HANGUL_RE = re.compile(r"[\uAC00-\uD7A3]")
_HIRAGANA_RE = re.compile(r"[\u3040-\u309F]")
_KATAKANA_RE = re.compile(r"[\u30A0-\u30FF]")


def _extract_text(html: str) -> str:
    """Extract visible text from HTML."""
    soup = BeautifulSoup(html, "html.parser")
    for tag in soup(["script", "style", "noscript"]):
        tag.decompose()
    return soup.get_text(separator=" ", strip=True)


def _is_procedure_page(url: str, html: str) -> bool:
    """Check if a page is a procedure/treatment page."""
    soup = BeautifulSoup(html, "html.parser")
    title = soup.title.string if soup.title else ""
    text_sample = _extract_text(html)[:500]
    return bool(
        _PROCEDURE_RE.search(url)
        or _PROCEDURE_RE.search(title or "")
        or _PROCEDURE_RE.search(text_sample)
    )


def _is_review_page(url: str, html: str) -> bool:
    """Check if a page is a review/testimonial page."""
    soup = BeautifulSoup(html, "html.parser")
    title = soup.title.string if soup.title else ""
    return bool(
        _REVIEW_RE.search(url)
        or _REVIEW_RE.search(title or "")
    )


def _detect_page_lang(html: str) -> str:
    """Detect primary language of a page (ko/ja/other)."""
    text = _extract_text(html)[:2000]
    hangul = len(_HANGUL_RE.findall(text))
    japanese = len(_HIRAGANA_RE.findall(text)) + len(_KATAKANA_RE.findall(text))
    if japanese > hangul and japanese > 10:
        return "ja"
    if hangul > 10:
        return "ko"
    return "other"


def _find_pattern_matches(
    text: str, patterns: list[re.Pattern], max_context: int = 30,
) -> list[str]:
    """Find pattern matches with surrounding context."""
    matches: list[str] = []
    for pattern in patterns:
        for m in pattern.finditer(text):
            start = max(0, m.start() - max_context)
            end = min(len(text), m.end() + max_context)
            context = text[start:end].strip()
            if context not in matches:
                matches.append(context)
    return matches


def _check_kr_violations(pages: list[dict]) -> tuple[list[dict], list[dict], list[dict]]:
    """Check Korean medical advertising violations."""
    violations: list[dict] = []
    warnings: list[dict] = []
    compliant: list[dict] = []

    procedure_pages_checked = 0
    procedure_pages_with_disclosure = 0

    for page in pages:
        url = page["url"]
        html = page["html"]
        text = _extract_text(html)
        lang = _detect_page_lang(html)

        # Only check Korean-language pages for KR rules
        if lang != "ko":
            continue

        # Check prohibited expressions
        for rule_key, patterns in KR_PROHIBITED.items():
            full_rule = f"kr_{rule_key}"
            meta = _RULE_META.get(full_rule, {})
            matches = _find_pattern_matches(text, patterns)
            for match_text in matches:
                severity = "high" if rule_key == "exaggeration" else "medium"
                violations.append({
                    "severity": severity,
                    "rule": full_rule,
                    "text": match_text,
                    "url": url,
                    "law": meta.get("law", ""),
                    "description": meta.get("description", ""),
                })

        # Check procedure pages for required disclosures
        if _is_procedure_page(url, html):
            procedure_pages_checked += 1
            has_disclosure = any(p.search(text) for p in KR_REQUIRED_DISCLOSURES)
            if has_disclosure:
                procedure_pages_with_disclosure += 1
                compliant.append({
                    "rule": "kr_side_effects_disclosed",
                    "url": url,
                    "message": "부작용/주의사항이 고지되어 있습니다",
                })
            else:
                meta = _RULE_META["kr_no_side_effects"]
                violations.append({
                    "severity": "high",
                    "rule": "kr_no_side_effects",
                    "text": "시술 페이지에 부작용/주의사항 설명 없음",
                    "url": url,
                    "law": meta["law"],
                    "description": meta["description"],
                })

        # Check Before/After pages
        if _is_review_page(url, html):
            ba_patterns = [re.compile(r"before.*after", re.I), re.compile(r"전후")]
            if any(p.search(text) for p in ba_patterns):
                consent_keywords = [re.compile(r"동의"), re.compile(r"consent", re.I)]
                has_consent = any(p.search(text) for p in consent_keywords)
                if not has_consent:
                    meta = _RULE_META["kr_before_after"]
                    warnings.append({
                        "severity": "medium",
                        "rule": "kr_before_after",
                        "text": "Before/After 사진에 동의 관련 고지가 확인되지 않음",
                        "url": url,
                        "law": meta["law"],
                        "description": meta["description"],
                    })

    # Summary compliant items
    if procedure_pages_checked > 0 and procedure_pages_with_disclosure == procedure_pages_checked:
        compliant.append({
            "rule": "kr_all_disclosures",
            "message": f"모든 시술 페이지({procedure_pages_checked}개)에 부작용/주의사항이 고지됨",
        })

    return violations, warnings, compliant


def _check_jp_violations(pages: list[dict]) -> tuple[list[dict], list[dict], list[dict]]:
    """Check Japanese medical advertising violations."""
    violations: list[dict] = []
    warnings: list[dict] = []
    compliant: list[dict] = []

    for page in pages:
        url = page["url"]
        html = page["html"]
        text = _extract_text(html)
        lang = _detect_page_lang(html)

        if lang != "ja":
            continue

        # Check testimonial usage
        matches = _find_pattern_matches(text, JP_TESTIMONIAL)
        for match_text in matches:
            meta = _RULE_META["jp_testimonial"]
            violations.append({
                "severity": "high",
                "rule": "jp_testimonial",
                "text": match_text,
                "url": url,
                "law": meta["law"],
                "description": meta["description"],
            })

        # Check comparison ads
        matches = _find_pattern_matches(text, JP_COMPARISON)
        for match_text in matches:
            meta = _RULE_META["jp_comparison"]
            warnings.append({
                "severity": "medium",
                "rule": "jp_comparison",
                "text": match_text,
                "url": url,
                "law": meta["law"],
                "description": meta["description"],
            })

        # Check Before/After without explanation
        if _is_procedure_page(url, html) or _is_review_page(url, html):
            ba_matches = _find_pattern_matches(text, JP_BEFORE_AFTER)
            if ba_matches:
                explanation_re = [
                    re.compile(r"治療内容", re.I),
                    re.compile(r"リスク", re.I),
                    re.compile(r"費用", re.I),
                    re.compile(r"期間", re.I),
                ]
                has_explanation = sum(1 for p in explanation_re if p.search(text)) >= 2
                if not has_explanation:
                    meta = _RULE_META["jp_before_after"]
                    warnings.append({
                        "severity": "medium",
                        "rule": "jp_before_after",
                        "text": "Before/After写真に治療内容・リスク・費用の説明なし",
                        "url": url,
                        "law": meta["law"],
                        "description": meta["description"],
                    })

    if not violations and not warnings:
        compliant.append({
            "rule": "jp_compliant",
            "message": "日本語ページで医療法違反は検出されませんでした",
        })

    return violations, warnings, compliant


def _check_global_compliance(pages: list[dict]) -> tuple[list[dict], list[dict], list[dict]]:
    """Check global compliance items."""
    violations: list[dict] = []
    warnings: list[dict] = []
    compliant: list[dict] = []

    # Check privacy policy presence in multiple languages
    privacy_langs: set[str] = set()
    for page in pages:
        text = _extract_text(page["html"])
        for kw in _PRIVACY_KEYWORDS:
            if kw.search(text):
                lang = _detect_page_lang(page["html"])
                privacy_langs.add(lang)
                break

    if not privacy_langs:
        meta = _RULE_META["global_privacy"]
        violations.append({
            "severity": "medium",
            "rule": "global_privacy",
            "text": "개인정보 처리방침을 찾을 수 없습니다",
            "url": pages[0]["url"] if pages else "",
            "law": meta["law"],
            "description": meta["description"],
        })
    elif len(privacy_langs) < 2:
        meta = _RULE_META["global_privacy"]
        warnings.append({
            "severity": "low",
            "rule": "global_privacy",
            "text": f"개인정보 처리방침이 {len(privacy_langs)}개 언어에서만 확인됨",
            "url": pages[0]["url"] if pages else "",
            "law": meta["law"],
            "description": meta["description"],
        })
    else:
        compliant.append({
            "rule": "global_privacy",
            "message": f"개인정보 처리방침이 {len(privacy_langs)}개 언어에서 확인됨",
        })

    return violations, warnings, compliant


def _calculate_score(
    violations: list[dict], warnings: list[dict], total_pages: int,
) -> int:
    """Calculate compliance score (0-100)."""
    score = 100

    for v in violations:
        if v.get("severity") == "high":
            score -= 10
        else:
            score -= 5

    for w in warnings:
        score -= 3

    return max(0, min(100, score))


def _generate_recommendations(
    violations: list[dict], warnings: list[dict],
) -> list[dict]:
    """Generate actionable recommendations from violations."""
    recs: list[dict] = []
    seen_rules: set[str] = set()

    for v in violations:
        rule = v.get("rule", "")
        if rule in seen_rules:
            continue
        seen_rules.add(rule)

        if rule == "kr_no_side_effects":
            recs.append({
                "priority": "high",
                "message": "시술 페이지에 부작용, 합병증, 주의사항을 반드시 기재하세요 (의료법 시행령)",
            })
        elif rule.startswith("kr_exaggeration"):
            recs.append({
                "priority": "high",
                "message": "'최고', '100%', '보장' 등 과장 표현을 제거하세요 (의료법 제56조)",
            })
        elif rule.startswith("kr_comparison"):
            recs.append({
                "priority": "medium",
                "message": "'가장', '제일', '최초' 등 비교 표현은 객관적 근거 없이 사용할 수 없습니다",
            })
        elif rule.startswith("kr_discount"):
            recs.append({
                "priority": "high",
                "message": "과도한 할인 광고(50% 이상)나 무료 시술 광고를 수정하세요",
            })
        elif rule == "jp_testimonial":
            recs.append({
                "priority": "high",
                "message": "일본어 페이지에서 환자 체험담(体験談)을 광고로 사용하지 마세요 (医療法)",
            })
        elif rule == "jp_comparison":
            recs.append({
                "priority": "medium",
                "message": "일본어 페이지에서 'No.1', '日本一' 등 비교 광고를 제거하세요",
            })
        elif rule == "global_privacy":
            recs.append({
                "priority": "medium",
                "message": "개인정보 처리방침을 다국어(한/영/일)로 제공하세요",
            })

    for w in warnings:
        rule = w.get("rule", "")
        if rule in seen_rules:
            continue
        seen_rules.add(rule)

        if rule == "kr_before_after":
            recs.append({
                "priority": "medium",
                "message": "Before/After 사진에 환자 동의 고지를 명시하세요",
            })
        elif rule == "jp_before_after":
            recs.append({
                "priority": "medium",
                "message": "일본어 Before/After에 치료내용, 리스크, 비용, 기간을 명시하세요",
            })

    return recs


def check_medical_compliance(pages: list[dict]) -> dict:
    """
    Check crawled pages for medical advertising regulation violations.

    Args:
        pages: List of dicts with keys: url, html

    Returns:
        Compliance analysis result with violations, warnings, scores by country.
    """
    if not pages:
        return {
            "overall_score": 0,
            "violations": [],
            "warnings": [],
            "compliant_items": [],
            "by_country": {
                "kr": {"score": 0, "violations": 0, "warnings": 0},
                "jp": {"score": 0, "violations": 0, "warnings": 0},
                "global": {"score": 0, "violations": 0, "warnings": 0},
            },
            "recommendations": [],
        }

    # Run checks by country
    kr_violations, kr_warnings, kr_compliant = _check_kr_violations(pages)
    jp_violations, jp_warnings, jp_compliant = _check_jp_violations(pages)
    gl_violations, gl_warnings, gl_compliant = _check_global_compliance(pages)

    all_violations = kr_violations + jp_violations + gl_violations
    all_warnings = kr_warnings + jp_warnings + gl_warnings
    all_compliant = kr_compliant + jp_compliant + gl_compliant

    # Country scores
    kr_score = _calculate_score(kr_violations, kr_warnings, len(pages))
    jp_score = _calculate_score(jp_violations, jp_warnings, len(pages))
    gl_score = _calculate_score(gl_violations, gl_warnings, len(pages))

    # Overall = weighted average (KR most important for Korean hospitals)
    if kr_violations or kr_warnings:
        overall_score = round(kr_score * 0.5 + jp_score * 0.3 + gl_score * 0.2)
    elif jp_violations or jp_warnings:
        overall_score = round(kr_score * 0.3 + jp_score * 0.5 + gl_score * 0.2)
    else:
        overall_score = round((kr_score + jp_score + gl_score) / 3)

    recommendations = _generate_recommendations(all_violations, all_warnings)

    return {
        "overall_score": overall_score,
        "violations": all_violations,
        "warnings": all_warnings,
        "compliant_items": all_compliant,
        "by_country": {
            "kr": {
                "score": kr_score,
                "violations": len(kr_violations),
                "warnings": len(kr_warnings),
            },
            "jp": {
                "score": jp_score,
                "violations": len(jp_violations),
                "warnings": len(jp_warnings),
            },
            "global": {
                "score": gl_score,
                "violations": len(gl_violations),
                "warnings": len(gl_warnings),
            },
        },
        "recommendations": recommendations,
    }
