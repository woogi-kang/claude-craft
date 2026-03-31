"""AI content generation engine for dermatology procedure marketing."""

from __future__ import annotations

import json
import re
from datetime import datetime, timezone
from enum import Enum

import httpx

from ..config import settings
from .medical_compliance import KR_COMPARISON, KR_DISCOUNT, KR_EXAGGERATION, KR_REQUIRED_DISCLOSURES
from .procedure_data import ProcedureData, get_procedure_data


class ContentType(str, Enum):
    BLOG_POST = "blog_post"
    FAQ = "faq"
    PROCEDURE_PAGE = "procedure_page"
    SNS_SET = "sns_set"
    MEDICAL_GUIDE = "medical_guide"


class ContentLanguage(str, Enum):
    KO = "ko"
    EN = "en"
    JA = "ja"
    ZH = "zh"


# ---------------------------------------------------------------------------
# Prompt templates
# ---------------------------------------------------------------------------

CONTENT_TEMPLATES: dict[ContentType, dict[str, str]] = {
    ContentType.BLOG_POST: {
        "system": (
            "당신은 피부과 전문 의료 콘텐츠 작성자입니다. "
            "SEO에 최적화된 블로그 포스트를 작성합니다."
        ),
        "user": """
{hospital_name}의 {procedure_name} 시술에 대한 SEO 최적화 블로그 포스트를 작성하세요.

## 시술 데이터
- 원리: {principle}
- 방법: {method}
- 소요시간: {duration}
- 부작용: {side_effects}
- 다운타임: {downtime}
- 사후관리: {post_care}
- 가격: {average_price}

## 작성 규칙
1. 2000자 이상 작성
2. H2/H3 태그로 구조화
3. 타겟 키워드 '{keywords}' 자연스럽게 포함
4. 부작용과 주의사항 반드시 포함 (의료법 준수)
5. "개인에 따라 결과가 다를 수 있습니다" 문구 포함
6. FAQ 섹션 3~5개 포함
""",
    },
    ContentType.FAQ: {
        "system": (
            "의료 FAQ 전문 작성자입니다. "
            "Schema.org FAQPage 마크업에 적합한 Q&A를 작성합니다."
        ),
        "user": """
{procedure_name} 시술에 대한 FAQ 15~20개를 작성하세요.

## 시술 데이터
{procedure_data_text}

## 규칙
- 환자가 실제로 묻는 질문 형태
- 답변은 2-4문장, 구체적
- Schema.org FAQPage JSON-LD 마크업 포함
- 음성 검색 최적화 (자연어 질문)
""",
    },
    ContentType.PROCEDURE_PAGE: {
        "system": "의료 웹사이트 콘텐츠 전문가입니다.",
        "user": """
{procedure_name} 시술 소개 페이지를 {language}로 작성하세요.

{procedure_data_text}

## 페이지 구조
1. 시술 소개 (원리)
2. 시술 과정 (단계별)
3. 소요시간/다운타임
4. 부작용/주의사항
5. 사후관리
6. 가격 안내 (한국 vs 해외 비교: {price_comparison})
7. FAQ 5개

{language_specific_instructions}
""",
    },
    ContentType.SNS_SET: {
        "system": "소셜 미디어 콘텐츠 전문가입니다.",
        "user": """
{procedure_name} 시술에 대한 SNS 콘텐츠 세트를 작성하세요.

## 플랫폼별 요구사항
1. 인스타그램 슬라이드 (5장): 각 슬라이드 텍스트 + 해시태그 20개
2. 네이버 블로그: SEO 최적화 포스트 (1500자)
3. 小红书: 중국어 체험형 콘텐츠 (500자)

## 시술 데이터
{procedure_data_text}
""",
    },
    ContentType.MEDICAL_GUIDE: {
        "system": "의료관광 가이드 전문 작성자입니다.",
        "user": """
{target_country} 환자를 위한 한국 {procedure_name} 시술 가이드를 {language}로 작성하세요.

## 포함 내용
1. 한국에서 {procedure_name} 받기 장점
2. 비용 비교 ({target_country} vs 한국): {price_comparison}
3. 시술 과정 상세
4. 한국 방문 타임라인 (입국 → 상담 → 시술 → 회복 → 귀국)
5. 사후 관리 (귀국 후)
6. 기본 한국어 회화 (병원 방문용)

{procedure_data_text}
""",
    },
}

LANGUAGE_INSTRUCTIONS: dict[str, str] = {
    "ko": "한국어로 작성하세요. 존댓말을 사용하고 의료 전문 용어와 일반어를 적절히 혼합하세요.",
    "en": (
        "Write in English. Use professional medical terminology "
        "with patient-friendly explanations."
    ),
    "ja": "日本語で作成してください。丁寧語を使い、医療専門用語と一般用語を適切に混ぜてください。",
    "zh": "请用中文撰写。使用专业医疗术语，同时确保患者能理解。",
}

COUNTRY_NAMES: dict[str, dict[str, str]] = {
    "en": {"ko": "South Korea", "us": "United States", "jp": "Japan", "cn": "China"},
    "ko": {"ko": "한국", "us": "미국", "jp": "일본", "cn": "중국"},
    "ja": {"ko": "韓国", "us": "アメリカ", "jp": "日本", "cn": "中国"},
    "zh": {"ko": "韩国", "us": "美国", "jp": "日本", "cn": "中国"},
}


# ---------------------------------------------------------------------------
# SEO scoring
# ---------------------------------------------------------------------------

def calculate_seo_score(
    content: str,
    title: str,
    meta_description: str,
    target_keywords: list[str] | None = None,
) -> int:
    """Calculate SEO score (0-100) for generated content."""
    score = 0
    total_weight = 0

    # Title length (30-60 chars) — weight 15
    total_weight += 15
    title_len = len(title)
    if 30 <= title_len <= 60:
        score += 15
    elif 20 <= title_len <= 70:
        score += 10
    elif title_len > 0:
        score += 5

    # Meta description length (120-160 chars) — weight 10
    total_weight += 10
    meta_len = len(meta_description)
    if 120 <= meta_len <= 160:
        score += 10
    elif 80 <= meta_len <= 200:
        score += 7
    elif meta_len > 0:
        score += 3

    # H2/H3 structure — weight 15
    total_weight += 15
    h2_count = len(re.findall(r"<h2|## ", content))
    h3_count = len(re.findall(r"<h3|### ", content))
    if h2_count >= 3 and h3_count >= 2:
        score += 15
    elif h2_count >= 2:
        score += 10
    elif h2_count >= 1:
        score += 5

    # Keyword density (1-3%) — weight 15
    total_weight += 15
    if target_keywords:
        content_lower = content.lower()
        total_words = len(content_lower.split())
        if total_words > 0:
            keyword_count = sum(
                content_lower.count(kw.lower()) for kw in target_keywords
            )
            density = (keyword_count / total_words) * 100
            if 1.0 <= density <= 3.0:
                score += 15
            elif 0.5 <= density <= 5.0:
                score += 10
            elif keyword_count > 0:
                score += 5
    else:
        score += 10  # No keywords specified — partial credit

    # Word count (2000+ chars) — weight 20
    total_weight += 20
    char_count = len(content)
    if char_count >= 2000:
        score += 20
    elif char_count >= 1500:
        score += 15
    elif char_count >= 1000:
        score += 10
    elif char_count >= 500:
        score += 5

    # Image alt text — weight 10
    total_weight += 10
    img_tags = re.findall(r"<img[^>]*>", content)
    if not img_tags:
        score += 10  # No images needed
    else:
        imgs_with_alt = len(re.findall(r'<img[^>]+alt="[^"]+', content))
        if imgs_with_alt == len(img_tags):
            score += 10
        elif imgs_with_alt > 0:
            score += 5

    # Internal links — weight 5
    total_weight += 5
    link_count = len(re.findall(r"<a\s|]\(", content))
    if link_count >= 3:
        score += 5
    elif link_count >= 1:
        score += 3

    # FAQ section — weight 10
    total_weight += 10
    has_faq = bool(re.search(r"FAQ|자주\s*묻는\s*질문|よくある質問|常见问题", content, re.I))
    if has_faq:
        score += 10

    return round((score / total_weight) * 100) if total_weight > 0 else 0


# ---------------------------------------------------------------------------
# Compliance filtering
# ---------------------------------------------------------------------------

_KR_PROHIBITED_PATTERNS = KR_EXAGGERATION + KR_COMPARISON + KR_DISCOUNT

_KR_REQUIRED_DISCLAIMER = "개인에 따라 결과가 다를 수 있습니다"


def filter_compliance(content: str, language: str) -> tuple[str, list[str]]:
    """Filter prohibited expressions and insert required disclaimers.

    Returns (filtered_content, warnings).
    """
    warnings: list[str] = []
    filtered = content

    if language == "ko":
        for pattern in _KR_PROHIBITED_PATTERNS:
            matches = pattern.findall(filtered)
            for m in matches:
                warnings.append(f"금지 표현 제거됨: '{m}'")
                filtered = pattern.sub("", filtered)

        # Ensure required disclaimer
        has_disclaimer = any(p.search(filtered) for p in KR_REQUIRED_DISCLOSURES)
        if not has_disclaimer:
            filtered += f"\n\n※ {_KR_REQUIRED_DISCLAIMER}"
            warnings.append("필수 고지문 자동 삽입됨")

    return filtered.strip(), warnings


# ---------------------------------------------------------------------------
# Schema.org markup generation
# ---------------------------------------------------------------------------

def _generate_schema_markup(
    content_type: ContentType,
    title: str,
    description: str,
    procedure_name: str,
    hospital_name: str | None = None,
    faq_pairs: list[dict] | None = None,
) -> str:
    """Generate JSON-LD schema markup for the content."""
    schemas: list[dict] = []

    if content_type == ContentType.FAQ and faq_pairs:
        faq_schema = {
            "@context": "https://schema.org",
            "@type": "FAQPage",
            "mainEntity": [
                {
                    "@type": "Question",
                    "name": pair["question"],
                    "acceptedAnswer": {
                        "@type": "Answer",
                        "text": pair["answer"],
                    },
                }
                for pair in faq_pairs
            ],
        }
        schemas.append(faq_schema)

    article_schema: dict = {
        "@context": "https://schema.org",
        "@type": "MedicalWebPage" if content_type != ContentType.SNS_SET else "Article",
        "name": title,
        "description": description,
        "about": {
            "@type": "MedicalProcedure",
            "name": procedure_name,
        },
    }
    if hospital_name:
        article_schema["publisher"] = {
            "@type": "MedicalClinic",
            "name": hospital_name,
        }
    schemas.append(article_schema)

    return json.dumps(schemas, ensure_ascii=False, indent=2)


# ---------------------------------------------------------------------------
# LLM integration
# ---------------------------------------------------------------------------

async def _call_llm(system_prompt: str, user_prompt: str) -> str | None:
    """Call configured LLM API. Returns None if no API key configured."""
    api_key = settings.content_llm_api_key
    if not api_key:
        return None

    provider = settings.content_llm_provider
    model = settings.content_llm_model

    async with httpx.AsyncClient(timeout=60.0) as client:
        if provider == "claude":
            resp = await client.post(
                "https://api.anthropic.com/v1/messages",
                headers={
                    "x-api-key": api_key,
                    "anthropic-version": "2023-06-01",
                    "content-type": "application/json",
                },
                json={
                    "model": model,
                    "max_tokens": 4096,
                    "system": system_prompt,
                    "messages": [{"role": "user", "content": user_prompt}],
                },
            )
            resp.raise_for_status()
            data = resp.json()
            return data["content"][0]["text"]

        elif provider == "openai":
            resp = await client.post(
                "https://api.openai.com/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {api_key}",
                    "Content-Type": "application/json",
                },
                json={
                    "model": model,
                    "messages": [
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_prompt},
                    ],
                    "max_tokens": 4096,
                },
            )
            resp.raise_for_status()
            data = resp.json()
            return data["choices"][0]["message"]["content"]

    return None


# ---------------------------------------------------------------------------
# Template-based fallback (no LLM required)
# ---------------------------------------------------------------------------

def _format_procedure_text(data: ProcedureData) -> str:
    """Format procedure data as readable text block."""
    lines = [
        f"시술명: {data.name}",
        f"카테고리: {data.category}" if data.category else "",
        f"원리: {data.principle}" if data.principle else "",
        f"시술 방법: {data.method}" if data.method else "",
        f"소요시간: {data.duration}" if data.duration else "",
        f"부작용: {data.side_effects}" if data.side_effects else "",
        f"통증: {data.pain_description}" if data.pain_description else "",
        f"다운타임: {data.downtime}" if data.downtime else "",
        f"사후관리: {data.post_care}" if data.post_care else "",
        f"평균가격: {data.average_price}" if data.average_price else "",
    ]
    return "\n".join(line for line in lines if line)


def _format_price_comparison(data: ProcedureData, language: str = "ko") -> str:
    """Format price comparison text."""
    if not data.price_by_country:
        return "가격 비교 정보 없음"
    lines = []
    for country, info in data.price_by_country.items():
        name = COUNTRY_NAMES.get(language, COUNTRY_NAMES["ko"]).get(
            country.lower(), country
        )
        price = info.get("price", 0)
        currency = info.get("currency", "")
        unit = info.get("price_unit", "")
        lines.append(f"- {name}: {currency} {price:,} {unit}".strip())
    return "\n".join(lines) if lines else "가격 비교 정보 없음"


def _fallback_blog_post(
    data: ProcedureData,
    hospital_name: str,
    hospital_region: str,
    keywords: list[str],
    language: str,
) -> str:
    """Generate blog post content without LLM."""
    loc = f" ({hospital_region})" if hospital_region else ""
    hospital = hospital_name or "전문 피부과"
    kw_text = ", ".join(keywords) if keywords else data.name

    return f"""<h2>{data.name} 시술 완벽 가이드 - {hospital}{loc}</h2>

<p>{hospital}에서 제공하는 {data.name} 시술을 알아보겠습니다. \
{kw_text} 관심 분들을 위한 종합 가이드입니다.</p>

<h2>{data.name} 시술이란?</h2>
<p>{data.principle or '피부과에서 시행하는 전문 시술입니다.'}</p>
{f'<p>{data.mechanism_detail}</p>' if data.mechanism_detail else ''}

<h3>시술 대상</h3>
<p>{data.target or '피부 고민이 있는 분들에게 추천됩니다.'}</p>

<h3>기대 효과</h3>
<p>{data.effect or '전문의 상담을 통해 기대 효과를 확인하세요.'}</p>

<h2>시술 과정</h2>
<p>{data.method or '전문의가 개인 피부 상태에 맞춰 시술을 진행합니다.'}</p>
<ul>
<li>소요시간: {data.duration or '전문의 상담 시 안내'}</li>
<li>통증: {data.pain_description or '개인차가 있습니다'}</li>
<li>다운타임: {data.downtime or '시술에 따라 다릅니다'}</li>
</ul>

<h2>부작용 및 주의사항</h2>
<p>{data.side_effects or '모든 시술에는 부작용이 있을 수 있습니다. 전문의와 상담하세요.'}</p>
{f'<p>비추천 대상: {data.not_recommended}</p>' if data.not_recommended else ''}

<h2>사후관리</h2>
<p>{data.post_care or '시술 후 전문의의 안내에 따라 관리해 주세요.'}</p>

<h2>비용 안내</h2>
<p>평균 가격: {data.average_price or '전문의 상담 시 안내'}</p>
{_format_price_comparison(data, language)}

<h2>자주 묻는 질문 (FAQ)</h2>

<h3>Q. {data.name} 시술은 아프나요?</h3>
<p>A. {data.pain_description or '통증은 개인차가 있으며, 마취 크림으로 최소화합니다.'}</p>

<h3>Q. 다운타임은 얼마나 되나요?</h3>
<p>A. {data.downtime or '시술 종류와 개인 상태에 따라 다릅니다. 전문의와 상담하세요.'}</p>

<h3>Q. 몇 회 시술이 필요한가요?</h3>
<p>A. 개인의 피부 상태에 따라 다릅니다. 전문의 상담을 통해 적절한 시술 횟수를 결정합니다.</p>

<p><em>※ 개인에 따라 결과가 다를 수 있습니다. 반드시 전문의와 상담 후 시술을 결정하세요.</em></p>
"""


def _fallback_faq(data: ProcedureData) -> str:
    """Generate FAQ content without LLM."""
    name = data.name
    faqs = [
        (
            f"{name} 시술이란 무엇인가요?",
            data.principle or "피부과에서 시행하는 전문 시술입니다.",
        ),
        (
            f"{name} 시술 과정은 어떻게 되나요?",
            data.method or "전문의가 개인 상태에 맞춰 진행합니다.",
        ),
        ("시술 시간은 얼마나 걸리나요?", data.duration or "시술 종류에 따라 다릅니다."),
        ("통증이 심한가요?", data.pain_description or "개인차가 있으며, 마취로 최소화합니다."),
        ("다운타임이 있나요?", data.downtime or "시술에 따라 다릅니다."),
        ("부작용은 무엇인가요?", data.side_effects or "전문의와 상담하세요."),
        ("사후관리는 어떻게 하나요?", data.post_care or "전문의 안내에 따라 관리합니다."),
        (
            "비용은 얼마인가요?",
            f"평균 {data.average_price}" if data.average_price else "전문의 상담 시 안내됩니다.",
        ),
        ("누구에게 추천하나요?", data.target or "피부 고민이 있는 분께 추천합니다."),
        ("효과는 어떤가요?", data.effect or "전문의 상담을 통해 확인하세요."),
    ]

    faq_html = ""
    for q, a in faqs:
        faq_html += f"<h3>Q. {q}</h3>\n<p>A. {a}</p>\n\n"

    schema = {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [
            {
                "@type": "Question",
                "name": q,
                "acceptedAnswer": {"@type": "Answer", "text": a},
            }
            for q, a in faqs
        ],
    }

    schema_json = json.dumps(schema, ensure_ascii=False, indent=2)
    return (
        faq_html
        + '\n<script type="application/ld+json">\n'
        + schema_json
        + "\n</script>"
    )


def _fallback_procedure_page(
    data: ProcedureData, language: str, hospital_name: str
) -> str:
    """Generate procedure page without LLM."""
    lang_label = {"ko": "한국어", "en": "English", "ja": "日本語", "zh": "中文"}.get(
        language, language
    )

    # Use translation if available
    tr = data.translations.get(language, {})
    name = tr.get("translated_name") or data.name
    principle = tr.get("principle") or data.principle
    method = tr.get("method") or data.method
    downtime = tr.get("downtime") or data.downtime
    post_care = tr.get("post_care") or data.post_care

    return f"""<h1>{name}</h1>
<p>Language: {lang_label}</p>

<h2>시술 소개</h2>
<p>{principle or '전문 피부과 시술입니다.'}</p>

<h2>시술 과정</h2>
<p>{method or '전문의가 진행합니다.'}</p>

<h2>소요시간 / 다운타임</h2>
<p>소요시간: {data.duration or '상담 시 안내'}</p>
<p>다운타임: {downtime or '시술에 따라 다릅니다'}</p>

<h2>부작용 및 주의사항</h2>
<p>{data.side_effects or '전문의와 상담하세요.'}</p>

<h2>사후관리</h2>
<p>{post_care or '전문의 안내를 따르세요.'}</p>

<h2>가격 안내</h2>
<p>{data.average_price or '상담 시 안내'}</p>
{_format_price_comparison(data, language)}

<p><em>※ 개인에 따라 결과가 다를 수 있습니다.</em></p>
"""


def _fallback_sns_set(data: ProcedureData) -> str:
    """Generate SNS content set without LLM."""
    return f"""## 인스타그램 슬라이드 (5장)

**슬라이드 1:** {data.name} 시술, 알고 계셨나요?
**슬라이드 2:** 시술 원리 — {(data.principle or '전문 피부과 시술')[:80]}
**슬라이드 3:** 시술 과정 — {(data.method or '전문의가 진행')[:80]}
**슬라이드 4:** 다운타임: {data.downtime or '상이'} / 통증: {data.pain_description or '개인차'}
**슬라이드 5:** 지금 상담 예약하세요!

해시태그: #{data.name} #피부과 #피부관리 #피부시술 #뷰티 #스킨케어 #강남피부과 #피부고민 #시술후기

---

## 네이버 블로그

{data.name} 시술 후기 — 원리부터 가격까지 총정리

{data.name}은(는) {data.principle or '피부과에서 시행하는 전문 시술입니다.'}
시술 방법: {data.method or '전문의가 개인 상태에 맞춰 진행합니다.'}
소요시간: {data.duration or '시술에 따라 다름'}
다운타임: {data.downtime or '시술에 따라 다름'}
가격: {data.average_price or '상담 시 안내'}

※ 개인에 따라 결과가 다를 수 있습니다.

---

## 小红书

{data.name}韩国皮肤科体验分享 🇰🇷

来韩国体验了{data.name}！效果真的很棒～
价格：{data.average_price or '咨询时告知'}
过程：{(data.method or '专业医生操作')[:50]}
恢复期：{data.downtime or '因人而异'}

※ 个人效果可能不同，请咨询专业医生。
"""


def _fallback_medical_guide(
    data: ProcedureData, language: str, hospital_name: str
) -> str:
    """Generate medical tourism guide without LLM."""
    return f"""<h1>{data.name} — Medical Tourism Guide</h1>

<h2>Why Get {data.name} in Korea?</h2>
<p>Korea is a global leader in dermatology and aesthetics. \
Advanced technology, experienced specialists, and competitive pricing make it ideal.</p>

<h2>Cost Comparison</h2>
{_format_price_comparison(data, language)}

<h2>Procedure Details</h2>
<p>{data.principle or 'Professional dermatological procedure.'}</p>
<p>Method: {data.method or 'Performed by certified specialists.'}</p>
<p>Duration: {data.duration or 'Varies by treatment'}</p>
<p>Downtime: {data.downtime or 'Varies by individual'}</p>

<h2>Visit Timeline</h2>
<ol>
<li>Day 1: Arrival in Korea, hotel check-in</li>
<li>Day 2: Clinic consultation and skin assessment</li>
<li>Day 3: {data.name} procedure</li>
<li>Day 4-5: Recovery and follow-up check</li>
<li>Day 6-7: Sightseeing and departure</li>
</ol>

<h2>Post-Treatment Care</h2>
<p>{data.post_care or 'Follow your doctor instructions after returning home.'}</p>

<h2>Useful Korean Phrases</h2>
<ul>
<li>안녕하세요 (Annyeonghaseyo) — Hello</li>
<li>예약했습니다 (Yeyak haesseumnida) — I have a reservation</li>
<li>아파요 (Apayo) — It hurts</li>
<li>감사합니다 (Gamsahamnida) — Thank you</li>
</ul>

<p><em>※ Results may vary by individual. Please consult with a specialist.</em></p>
"""


# ---------------------------------------------------------------------------
# Main entry point
# ---------------------------------------------------------------------------

async def generate_content(
    content_type: ContentType,
    procedure_name: str,
    hospital_name: str | None = None,
    hospital_region: str | None = None,
    target_language: ContentLanguage = ContentLanguage.KO,
    target_keywords: list[str] | None = None,
    custom_context: str | None = None,
) -> dict:
    """Generate content for a dermatology procedure.

    Uses LLM if API key is configured, otherwise falls back to template-based generation.
    """
    # Fetch procedure data from DB
    proc_data = await get_procedure_data(procedure_name)
    if proc_data is None:
        # Create minimal stub for generation
        proc_data = ProcedureData(name=procedure_name)

    hospital = hospital_name or ""
    region = hospital_region or ""
    lang = target_language.value
    keywords = target_keywords or [procedure_name]

    # Try LLM generation first
    content = await _try_llm_generation(
        content_type, proc_data, hospital, region, lang, keywords, custom_context
    )

    # Fallback to template-based
    if content is None:
        content = _generate_fallback(
            content_type, proc_data, hospital, region, lang, keywords
        )

    # Apply compliance filtering
    filtered_content, compliance_warnings = filter_compliance(content, lang)

    # Generate metadata
    title = _extract_title(filtered_content, proc_data.name, hospital)
    meta_description = _generate_meta_description(proc_data, hospital, lang)
    seo_score = calculate_seo_score(
        filtered_content, title, meta_description, keywords
    )

    schema_markup = _generate_schema_markup(
        content_type, title, meta_description, proc_data.name, hospital
    )

    return {
        "content_type": content_type.value,
        "title": title,
        "content": filtered_content,
        "meta_title": title[:60] if len(title) > 60 else title,
        "meta_description": meta_description,
        "seo_score": seo_score,
        "word_count": len(filtered_content),
        "language": lang,
        "schema_markup": schema_markup,
        "compliance_warnings": compliance_warnings,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "source_data": {
            "procedure": proc_data.name,
            "hospital": hospital or None,
            "region": region or None,
        },
    }


async def _try_llm_generation(
    content_type: ContentType,
    data: ProcedureData,
    hospital: str,
    region: str,
    language: str,
    keywords: list[str],
    custom_context: str | None,
) -> str | None:
    """Try to generate content via LLM API."""
    template = CONTENT_TEMPLATES.get(content_type)
    if template is None:
        return None

    proc_text = _format_procedure_text(data)
    price_comp = _format_price_comparison(data, language)
    lang_instructions = LANGUAGE_INSTRUCTIONS.get(language, "")
    country_names = COUNTRY_NAMES.get(language, COUNTRY_NAMES["ko"])

    user_prompt = template["user"].format(
        procedure_name=data.name,
        hospital_name=hospital or "전문 피부과",
        principle=data.principle,
        method=data.method,
        duration=data.duration,
        side_effects=data.side_effects,
        downtime=data.downtime,
        post_care=data.post_care,
        average_price=data.average_price,
        keywords=", ".join(keywords),
        procedure_data_text=proc_text,
        price_comparison=price_comp,
        language=language,
        language_specific_instructions=lang_instructions,
        target_country=country_names.get("us", ""),
    )

    if custom_context:
        user_prompt += f"\n\n## 추가 컨텍스트\n{custom_context}"

    system_prompt = template["system"]
    return await _call_llm(system_prompt, user_prompt)


def _generate_fallback(
    content_type: ContentType,
    data: ProcedureData,
    hospital: str,
    region: str,
    language: str,
    keywords: list[str],
) -> str:
    """Generate content using templates (no LLM)."""
    if content_type == ContentType.BLOG_POST:
        return _fallback_blog_post(data, hospital, region, keywords, language)
    elif content_type == ContentType.FAQ:
        return _fallback_faq(data)
    elif content_type == ContentType.PROCEDURE_PAGE:
        return _fallback_procedure_page(data, language, hospital)
    elif content_type == ContentType.SNS_SET:
        return _fallback_sns_set(data)
    elif content_type == ContentType.MEDICAL_GUIDE:
        return _fallback_medical_guide(data, language, hospital)
    return f"<p>{data.name} 시술 정보</p>"


def _extract_title(content: str, procedure_name: str, hospital: str) -> str:
    """Extract or generate title from content."""
    # Try to find H1 or H2
    m = re.search(r"<h[12][^>]*>(.+?)</h[12]>", content)
    if m:
        return re.sub(r"<[^>]+>", "", m.group(1)).strip()

    # Try markdown heading
    m = re.search(r"^#{1,2}\s+(.+)$", content, re.MULTILINE)
    if m:
        return m.group(1).strip()

    # Fallback
    hosp = f" - {hospital}" if hospital else ""
    return f"{procedure_name} 시술 가이드{hosp}"


def _generate_meta_description(
    data: ProcedureData, hospital: str, language: str
) -> str:
    """Generate SEO meta description (120-160 chars)."""
    hosp = f"{hospital}의 " if hospital else ""
    base = f"{hosp}{data.name} 시술 안내. "

    parts = []
    if data.principle:
        parts.append(data.principle[:50])
    if data.duration:
        parts.append(f"소요시간 {data.duration}")
    if data.downtime:
        parts.append(f"다운타임 {data.downtime}")
    if data.average_price:
        parts.append(f"가격 {data.average_price}")

    desc = base + " ".join(parts)

    # Trim to 160 chars
    if len(desc) > 160:
        desc = desc[:157] + "..."
    return desc


def get_supported_content_types() -> list[dict]:
    """Return list of available content types with descriptions."""
    return [
        {
            "type": ContentType.BLOG_POST.value,
            "name": "SEO 블로그 포스트",
            "description": "2000자 이상의 SEO 최적화 블로그 포스트",
        },
        {
            "type": ContentType.FAQ.value,
            "name": "FAQ + Schema.org",
            "description": "Schema.org FAQPage 마크업 포함 FAQ 15~20개",
        },
        {
            "type": ContentType.PROCEDURE_PAGE.value,
            "name": "시술 소개 페이지",
            "description": "다국어 시술 소개 페이지",
        },
        {
            "type": ContentType.SNS_SET.value,
            "name": "SNS 콘텐츠 세트",
            "description": "인스타그램 + 네이버 블로그 + 小红书 콘텐츠",
        },
        {
            "type": ContentType.MEDICAL_GUIDE.value,
            "name": "의료관광 가이드",
            "description": "외국인 환자 대상 시술 + 관광 가이드",
        },
    ]


def get_supported_languages() -> list[dict]:
    """Return list of supported languages."""
    return [
        {"code": "ko", "name": "한국어"},
        {"code": "en", "name": "English"},
        {"code": "ja", "name": "日本語"},
        {"code": "zh", "name": "中文"},
    ]
