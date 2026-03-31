"""Voice search optimization readiness analyzer."""

import re

from bs4 import BeautifulSoup

# ── Question patterns for heading detection ──────────────────────────────────

QUESTION_PATTERNS = [
    re.compile(r"\?$"),
    re.compile(
        r"^(what|how|why|when|where|who|which|can|do|does|is|are)\s", re.I
    ),
    re.compile(r"(은|는|이|가)\s*(무엇|뭐|어떤|어떻게|왜|언제|어디)"),
    re.compile(r"(とは|ですか|でしょうか)"),
    re.compile(r"(이란|란)\s*(무엇|뭐)"),
]

# ── Featured snippet: definition patterns ────────────────────────────────────

_DEFINITION_PATTERNS = [
    re.compile(r"(은|는|이|가)\s+.{5,}(이다|입니다|됩니다|합니다)"),
    re.compile(r"\bis\s+(?:a|an|the)\s+", re.I),
    re.compile(r"refers?\s+to\s+", re.I),
]

# ── Long-tail keyword: 5+ word question content ─────────────────────────────

_LONG_TAIL_RE = re.compile(
    r"(what|how|why|when|where|who|which|can|do|does|is|are)"
    r"(\s+\S+){4,}\?",
    re.I,
)
_LONG_TAIL_KO_RE = re.compile(
    r"(무엇|어떤|어떻게|왜|언제|어디).{15,}\?",
)


def _count_question_headings(soup: BeautifulSoup) -> list[str]:
    """Find H2/H3 headings that are question-form."""
    questions: list[str] = []
    for h in soup.find_all(["h2", "h3"]):
        text = h.get_text(strip=True)
        if not text:
            continue
        for pat in QUESTION_PATTERNS:
            if pat.search(text):
                questions.append(text)
                break
    return questions


def _check_featured_snippet_paragraphs(soup: BeautifulSoup) -> list[str]:
    """Find paragraphs under H2/H3 that are 40-60 words and definition-form."""
    snippets: list[str] = []
    for heading in soup.find_all(["h2", "h3"]):
        sibling = heading.find_next_sibling()
        if sibling and sibling.name == "p":
            text = sibling.get_text(strip=True)
            word_count = len(text.split())
            if 40 <= word_count <= 60:
                for pat in _DEFINITION_PATTERNS:
                    if pat.search(text):
                        snippets.append(text[:80] + "...")
                        break
    return snippets


def _has_howto_schema(json_ld_items: list[dict]) -> bool:
    """Check for HowTo schema in JSON-LD items."""
    for item in json_ld_items:
        t = item.get("@type", "")
        types = t if isinstance(t, list) else [t]
        if "HowTo" in types:
            return True
        if "@graph" in item and isinstance(item["@graph"], list):
            for node in item["@graph"]:
                nt = node.get("@type", "")
                ntypes = nt if isinstance(nt, list) else [nt]
                if "HowTo" in ntypes:
                    return True
    return False


def _count_long_tail_questions(soup: BeautifulSoup) -> int:
    """Count long-tail (5+ word) question-form content in text."""
    for tag in soup(["script", "style", "noscript"]):
        tag.decompose()
    text = soup.get_text(separator=" ", strip=True)
    en_matches = _LONG_TAIL_RE.findall(text)
    ko_matches = _LONG_TAIL_KO_RE.findall(text)
    return len(en_matches) + len(ko_matches)


def _extract_json_ld(html: str) -> list[dict]:
    """Extract JSON-LD structured data from HTML."""
    import json

    soup = BeautifulSoup(html, "html.parser")
    results = []
    for script in soup.find_all("script", type="application/ld+json"):
        try:
            data = json.loads(script.string or "")
            if isinstance(data, list):
                results.extend(data)
            else:
                results.append(data)
        except (json.JSONDecodeError, TypeError):
            continue
    return results


def _get_types(json_ld_items: list[dict]) -> set[str]:
    """Get all @type values from JSON-LD items."""
    types: set[str] = set()
    for item in json_ld_items:
        if "@type" in item:
            t = item["@type"]
            if isinstance(t, list):
                types.update(t)
            else:
                types.add(t)
        if "@graph" in item and isinstance(item["@graph"], list):
            for node in item["@graph"]:
                if "@type" in node:
                    t = node["@type"]
                    if isinstance(t, list):
                        types.update(t)
                    else:
                        types.add(t)
    return types


def analyze_voice_search_readiness(
    pages: list[dict], category_scores: dict
) -> dict:
    """Analyze voice search optimization readiness.

    Args:
        pages: Crawled page dicts with keys: url, html
        category_scores: Per-item score breakdown from scorer

    Returns:
        Voice search readiness analysis with 8 check items, score, recommendations.
    """
    if not pages:
        return {
            "overall_score": 0,
            "checks": {},
            "pass_count": 0,
            "total_checks": 8,
            "recommendations": [],
        }

    # Use main page for HTML analysis
    main_html = pages[0].get("html", "")
    soup = BeautifulSoup(main_html, "html.parser")
    json_ld = _extract_json_ld(main_html)
    schema_types = _get_types(json_ld)

    checks: dict[str, dict] = {}
    recommendations: list[dict] = []

    # 1. FAQ Schema (FAQPage)
    faq_score = category_scores.get("faq_content", {})
    has_faq_schema = faq_score.get("details", {}).get("has_faq_schema", False)
    if not has_faq_schema:
        has_faq_schema = "FAQPage" in schema_types
    if has_faq_schema:
        checks["faq_schema"] = {
            "status": "pass",
            "description": "FAQPage 구조화 데이터 존재",
        }
    else:
        checks["faq_schema"] = {
            "status": "fail",
            "description": "FAQ 구조화 데이터 없음",
        }
        recommendations.append({
            "priority": "high",
            "message": "FAQ 페이지 + FAQPage Schema 추가로 음성 검색 노출 강화",
        })

    # 2. Question-form headings
    question_headings = _count_question_headings(soup)
    # Also check sub-pages
    for page in pages[1:]:
        sub_soup = BeautifulSoup(page.get("html", ""), "html.parser")
        question_headings.extend(_count_question_headings(sub_soup))
    q_count = len(question_headings)
    if q_count >= 5:
        checks["question_headings"] = {
            "status": "pass",
            "count": q_count,
            "description": f"질문형 헤딩 {q_count}개 (충분)",
        }
    elif q_count >= 1:
        checks["question_headings"] = {
            "status": "warn",
            "count": q_count,
            "description": f"질문형 헤딩 {q_count}개 (권장: 5개+)",
        }
        recommendations.append({
            "priority": "medium",
            "message": f"질문형 헤딩을 {5 - q_count}개 이상 추가하세요 (예: '보톡스란 무엇인가요?')",
        })
    else:
        checks["question_headings"] = {
            "status": "fail",
            "count": 0,
            "description": "질문형 헤딩 없음",
        }
        recommendations.append({
            "priority": "high",
            "message": "H2/H3에 자연어 질문형 헤딩 추가 (예: '보톡스 시술 후 주의사항은?')",
        })

    # 3. Featured Snippet suitability
    snippets = _check_featured_snippet_paragraphs(soup)
    for page in pages[1:]:
        sub_soup = BeautifulSoup(page.get("html", ""), "html.parser")
        snippets.extend(_check_featured_snippet_paragraphs(sub_soup))
    if len(snippets) >= 2:
        checks["featured_snippet"] = {
            "status": "pass",
            "count": len(snippets),
            "description": f"Featured Snippet 적합 단락 {len(snippets)}개",
        }
    elif len(snippets) == 1:
        checks["featured_snippet"] = {
            "status": "warn",
            "count": 1,
            "description": "Featured Snippet 적합 단락 1개 (권장: 2개+)",
        }
        recommendations.append({
            "priority": "medium",
            "message": "각 시술 소개 하단에 40-60단어의 간결한 정의형 답변 단락 추가",
        })
    else:
        checks["featured_snippet"] = {
            "status": "fail",
            "count": 0,
            "description": "간결한 정의형 답변 단락 없음",
        }
        recommendations.append({
            "priority": "high",
            "message": "Featured Snippet 확보를 위해 각 주제 아래 40-60단어 정의형 답변 추가",
        })

    # 4. LocalBusiness Schema
    sd_score = category_scores.get("structured_data", {})
    sd_types = sd_score.get("details", {}).get("schema_types", [])
    local_types = {"LocalBusiness", "MedicalClinic", "Hospital", "Dentist"}
    has_local = bool(local_types & set(sd_types)) or bool(local_types & schema_types)
    if has_local:
        checks["local_business"] = {
            "status": "pass",
            "description": "LocalBusiness Schema 존재",
        }
    else:
        checks["local_business"] = {
            "status": "fail",
            "description": "LocalBusiness Schema 없음",
        }
        recommendations.append({
            "priority": "high",
            "message": "LocalBusiness 또는 MedicalClinic Schema 추가로 '근처 병원' 음성 검색 대응",
        })

    # 5. Page speed (LCP < 3s)
    lcp_score = category_scores.get("lcp", {})
    lcp_details = lcp_score.get("details", {})
    lcp_value = lcp_details.get("lcp_ms", lcp_details.get("lcp", None))
    if lcp_value is not None:
        lcp_sec = lcp_value / 1000 if lcp_value > 100 else lcp_value
        if lcp_sec < 3:
            checks["page_speed"] = {
                "status": "pass",
                "description": f"LCP {lcp_sec:.1f}초 (<3초)",
            }
        else:
            checks["page_speed"] = {
                "status": "fail",
                "description": f"LCP {lcp_sec:.1f}초 (3초 이상)",
            }
            recommendations.append({
                "priority": "high",
                "message": "페이지 로딩 속도 3초 이내로 개선 — 음성 검색 결과는 빠른 페이지 우선",
            })
    else:
        lcp_raw_score = lcp_score.get("score")
        if lcp_raw_score is not None and lcp_raw_score >= 60:
            checks["page_speed"] = {
                "status": "pass",
                "description": "페이지 속도 양호",
            }
        elif lcp_raw_score is not None:
            checks["page_speed"] = {
                "status": "fail",
                "description": "페이지 속도 느림",
            }
            recommendations.append({
                "priority": "high",
                "message": "페이지 로딩 속도 개선 필요 — 음성 검색은 빠른 페이지를 우선 노출",
            })
        else:
            checks["page_speed"] = {
                "status": "warn",
                "description": "페이지 속도 측정 불가",
            }

    # 6. Mobile optimization
    mobile_score = category_scores.get("mobile", {})
    mobile_raw = mobile_score.get("score")
    if mobile_raw is not None and mobile_raw >= 60:
        checks["mobile"] = {
            "status": "pass",
            "description": "모바일 최적화 완료",
        }
    elif mobile_raw is not None:
        checks["mobile"] = {
            "status": "fail",
            "description": "모바일 최적화 미흡",
        }
        recommendations.append({
            "priority": "high",
            "message": "모바일 최적화 필수 — 음성 검색의 대부분은 모바일 기기에서 발생",
        })
    else:
        checks["mobile"] = {
            "status": "warn",
            "description": "모바일 최적화 상태 확인 불가",
        }

    # 7. HowTo Schema
    has_howto = _has_howto_schema(json_ld)
    if not has_howto:
        for page in pages[1:]:
            page_ld = _extract_json_ld(page.get("html", ""))
            if _has_howto_schema(page_ld):
                has_howto = True
                break
    if has_howto:
        checks["howto_schema"] = {
            "status": "pass",
            "description": "HowTo Schema 존재",
        }
    else:
        checks["howto_schema"] = {
            "status": "fail",
            "description": "HowTo Schema 없음",
        }
        recommendations.append({
            "priority": "medium",
            "message": "시술 과정을 HowTo Schema로 구조화하여 음성 어시스턴트가 단계별 안내 가능하도록 설정",
        })

    # 8. Long-tail keyword content (5+ words)
    long_tail_count = _count_long_tail_questions(
        BeautifulSoup(main_html, "html.parser")
    )
    for page in pages[1:]:
        long_tail_count += _count_long_tail_questions(
            BeautifulSoup(page.get("html", ""), "html.parser")
        )
    if long_tail_count >= 3:
        checks["long_tail"] = {
            "status": "pass",
            "count": long_tail_count,
            "description": f"장문 키워드 콘텐츠 {long_tail_count}개",
        }
    elif long_tail_count >= 1:
        checks["long_tail"] = {
            "status": "warn",
            "count": long_tail_count,
            "description": f"장문 키워드 콘텐츠 {long_tail_count}개 (권장: 3개+)",
        }
        recommendations.append({
            "priority": "medium",
            "message": "5단어 이상 질문형 콘텐츠 추가 (예: 'How long does botox last?')",
        })
    else:
        checks["long_tail"] = {
            "status": "fail",
            "count": 0,
            "description": "장문 키워드 콘텐츠 없음",
        }
        recommendations.append({
            "priority": "medium",
            "message": "장문 키워드(5단어+) 질문형 콘텐츠 추가로 음성 검색 롱테일 쿼리 대응",
        })

    # Calculate overall score
    pass_count = sum(1 for c in checks.values() if c["status"] == "pass")
    warn_count = sum(1 for c in checks.values() if c["status"] == "warn")
    total_checks = len(checks)

    # Score: pass=100, warn=50, fail=0, averaged
    score_sum = pass_count * 100 + warn_count * 50
    overall_score = round(score_sum / total_checks) if total_checks > 0 else 0

    # Sort recommendations by priority
    priority_order = {"high": 0, "medium": 1, "low": 2}
    recommendations.sort(key=lambda r: priority_order.get(r["priority"], 9))

    return {
        "overall_score": overall_score,
        "checks": checks,
        "pass_count": pass_count,
        "total_checks": total_checks,
        "recommendations": recommendations,
    }
