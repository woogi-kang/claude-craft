"""Step functions for the clinic crawl pipeline.

Each step operates on a CrawlContext dataclass that holds shared state.
Extracted from crawl_hospital() in crawl_single.py during Phase 3 refactoring.
"""

from __future__ import annotations

import asyncio
import json
import os
import re
import shutil
import subprocess
import tempfile
import time
from dataclasses import dataclass, field
from typing import Any
from urllib.parse import urljoin, urlparse

from clinic_crawler.constants import (
    DETAIL_MORE_LABELS,
    DOCTOR_PRIMARY,
    DOCTOR_SECONDARY,
    DOCTOR_SUBMENU_PARENTS,
    SCREENSHOT_DIR,
)
from clinic_crawler.js_snippets import (
    JS_CHECK_ENCODING,
    JS_CHECK_IMAGE_BASED,
    JS_CLICK_BRANCH_AND_GET_DOCTOR,
    JS_DETECT_CMS,
    JS_DETECT_FRAMES,
    JS_DISMISS_POPUPS,
    JS_EXTRACT_DOCTORS,
    JS_EXTRACT_PAGE_TEXT,
    JS_FIND_DOCTOR_DETAIL_LINKS,
    JS_FIND_DOCTOR_MENU,
    JS_FIND_DOCTOR_SUBLINKS,
    JS_FIND_DOCTOR_TABS,
    JS_FIND_INTRO_LINKS,
    JS_GET_PAGE_TEXT_LENGTH,
    JS_OPEN_MOBILE_MENUS,
    JS_REDIRECT_SCAN,
    JS_REVEAL_SUBMENUS,
    JS_SCROLL_TRIGGER,
    JS_SOCIAL_EXTRACT,
    JS_SPA_WAIT,
    JS_SPLASH_DETECT,
    JS_WINDOW_OPEN_INTERCEPT,
)
from clinic_crawler.korean_name import is_plausible_korean_name
from clinic_crawler.log import log
from clinic_crawler.ocr import (
    OCR_PROMPT_TEMPLATE,
    append_ocr_doctors,
    run_gemini_ocr,
)
from clinic_crawler.codex_validator import validate_doctors
from clinic_crawler.llm_verifier import verify_doctors_with_llm
from clinic_crawler.google_drive import (
    is_drive_enabled,
    keep_local_copy_after_upload,
    upload_screenshot,
)
from clinic_crawler.url_utils import classify_url, normalize_url


_MAX_CREDENTIALS = 25  # A single doctor rarely has >25 real credentials
_CHAIN_CAP = 20        # Max doctors per clinic; above this = cross-branch contamination


def _dedup_cross_contaminated(doctors: list, place_id: str) -> list:
    """Remove cross-contaminated profile_raw where multiple doctors share >50% items.

    Uses symmetric overlap: checks against the smaller of the two profiles.
    Order-dependent: earlier doctors in the list keep their profiles.
    Also caps per-doctor credential count to detect contamination.
    Mutates doctor dicts in-place.
    """
    if len(doctors) < 2:
        return doctors
    _THRESHOLD = 0.5
    for i, d in enumerate(doctors):
        raw_i = set(d.get("profile_raw") or [])
        if len(raw_i) < 3:
            continue
        for j in range(i + 1, len(doctors)):
            d2 = doctors[j]
            raw_j = set(d2.get("profile_raw") or [])
            if len(raw_j) < 3:
                continue
            overlap = raw_i & raw_j
            min_size = min(len(raw_i), len(raw_j))
            if len(overlap) > min_size * _THRESHOLD:
                d2["profile_raw"] = [x for x in (d2.get("profile_raw") or []) if x not in overlap]
                log(f"[{place_id}] Dedup: removed {len(overlap)} shared items from {d2.get('name', '?')}")

    # Cap: truncate abnormally long credential lists (cross-contamination residue)
    for d in doctors:
        raw = d.get("profile_raw") or []
        if len(raw) > _MAX_CREDENTIALS:
            log(f"[{place_id}] Cap: {d.get('name', '?')} had {len(raw)} items, "
                f"truncated to {_MAX_CREDENTIALS}")
            d["profile_raw"] = raw[:_MAX_CREDENTIALS]

    return doctors


def _filter_by_branch(doctors: list, hospital_name: str, place_id: str) -> list:
    """Filter doctors by branch for chain hospitals.

    Only applies when doctors have explicit branch labels (populated by JS
    extraction's branch detection). If no branch labels exist, returns all
    doctors unchanged.
    """
    if not doctors:
        return doctors

    # Check if any doctor has branch labels
    has_branches = any(d.get("branches") for d in doctors)
    if not has_branches:
        return doctors

    # Extract branch keyword from hospital name (e.g. "밴스의원 구로" → "구로")
    import re
    branch_match = re.search(r"([가-힣0-9]+?)(?:점|역)?$", hospital_name.strip())
    if not branch_match:
        return doctors
    branch_keyword = branch_match.group(1)

    # If majority of doctors have branch labels, unlabeled ones are likely
    # company-wide staff, not branch-specific — exclude them.
    labeled_count = sum(1 for d in doctors if d.get("branches"))
    label_ratio = labeled_count / len(doctors) if doctors else 0
    keep_unlabeled = label_ratio < 0.5  # keep only when less than half are labeled

    # Filter: keep doctors whose branches contain the keyword
    filtered = []
    for d in doctors:
        branches = d.get("branches") or []
        if not branches:
            if keep_unlabeled:
                filtered.append(d)
            continue
        if any(branch_keyword in b for b in branches):
            filtered.append(d)

    if filtered and len(filtered) < len(doctors):
        log(f"[{place_id}] Branch filter: kept {len(filtered)}/{len(doctors)} "
            f"doctors for branch '{branch_keyword}'")

    return filtered if filtered else doctors


def _extract_branch_name(hospital_name: str) -> str | None:
    """Extract branch indicator from hospital name.

    Examples:
        '바로그의원 강남' -> '강남'
        '콜나움의원 강남' -> '강남'
        '뷰티라운지의원 강남점' -> '강남'
    """
    m = re.search(
        r"(?:의원|병원|클리닉|센터)\s+(.{1,6}?)(?:점|본점)?$",
        hospital_name,
    )
    if m:
        return m.group(1)
    return None


@dataclass
class CrawlContext:
    """Shared state container for the crawl pipeline."""

    place_id: str
    name: str
    url: str
    base_url: str
    result: dict
    page: Any
    context: Any
    browser: Any
    timeout: int
    doctor_page_found: bool = False


@dataclass
class OcrState:
    """Mutable state shared across doctor extraction sub-functions."""

    seen_names: set = field(default_factory=set)
    last_screenshot_path: str | None = None
    temp_screenshots: list = field(default_factory=list)


# ---------------------------------------------------------------------------
# Step 0: Pre-flight
# ---------------------------------------------------------------------------


async def step_preflight(ctx: CrawlContext) -> bool:
    """Validate URL and check robots.txt. Returns False if crawl should abort."""
    parsed = urlparse(ctx.url)
    if parsed.scheme not in ("http", "https"):
        ctx.result["status"] = "failed"
        ctx.result["errors"].append({
            "type": "invalid_url",
            "message": f"Invalid scheme: {parsed.scheme}",
            "step": "preflight", "retryable": False,
        })
        return False

    ctx.base_url = f"{parsed.scheme}://{parsed.netloc}"
    log(f"[{ctx.place_id}] Starting crawl: {ctx.url}")

    try:
        robots_resp = await ctx.page.goto(
            f"{ctx.base_url}/robots.txt",
            wait_until="domcontentloaded", timeout=8000,
        )
        if robots_resp and robots_resp.ok:
            robots_text = await ctx.page.evaluate(
                "() => document.body?.innerText || ''"
            )
            current_agent = None
            wildcard_disallowed = []
            for line in robots_text.split("\n"):
                line = line.strip()
                if line.lower().startswith("user-agent:"):
                    current_agent = line.split(":", 1)[1].strip()
                elif (line.lower().startswith("disallow:")
                      and current_agent == "*"):
                    path = line.split(":", 1)[1].strip()
                    if path:
                        wildcard_disallowed.append(path)
            if (any(d == "/" for d in wildcard_disallowed)
                    and not any(
                        line.strip().lower().startswith("allow:")
                        and line.split(":", 1)[1].strip() == "/"
                        for line in robots_text.split("\n")
                    )):
                ctx.result["status"] = "robots_blocked"
                ctx.result["errors"].append({
                    "type": "robots_blocked",
                    "message": "robots.txt disallows all paths",
                    "step": "preflight", "retryable": False,
                })
                log(f"[{ctx.place_id}] robots.txt blocks all paths")
                return False
    except Exception:
        pass

    return True


# ---------------------------------------------------------------------------
# Step 1: Navigate and Resolve
# ---------------------------------------------------------------------------


async def step_navigate(ctx: CrawlContext) -> bool:
    """Navigate to URL, detect CMS/encoding/errors/anti-bot/splash.

    Returns False if crawl should abort.
    """
    log(f"[{ctx.place_id}] Navigating to {ctx.url}")
    try:
        await ctx.page.goto(
            ctx.url, wait_until="domcontentloaded",
            timeout=ctx.timeout * 1000,
        )
    except Exception as e:
        err_msg = str(e)
        ctx.result["status"] = "failed"
        if "timeout" in err_msg.lower():
            ctx.result["errors"].append({
                "type": "timeout", "message": err_msg[:200],
                "step": "navigate", "retryable": True,
            })
        elif "net::" in err_msg.lower():
            ctx.result["errors"].append({
                "type": "network", "message": err_msg[:200],
                "step": "navigate", "retryable": True,
            })
        else:
            ctx.result["errors"].append({
                "type": "navigation", "message": err_msg[:200],
                "step": "navigate", "retryable": True,
            })
        log(f"[{ctx.place_id}] Navigation failed: {err_msg[:100]}")
        return False

    # Redirect detection
    try:
        final_url = await ctx.page.evaluate("() => window.location.href")
        if final_url and final_url != ctx.url:
            ctx.result["final_url"] = final_url
            log(f"[{ctx.place_id}] Redirected to {final_url}")
    except Exception:
        pass

    # CMS detection
    try:
        cms = await ctx.page.evaluate(JS_DETECT_CMS)
        if cms:
            ctx.result["cms_platform"] = cms
            log(f"[{ctx.place_id}] CMS: {cms}")
    except Exception:
        pass

    # Encoding check
    try:
        enc_info = await ctx.page.evaluate(JS_CHECK_ENCODING)
        if enc_info.get("garbledRatio", 0) > 0.1:
            ctx.result["status"] = "encoding_error"
            ctx.result["errors"].append({
                "type": "encoding",
                "message": f"Garbled text ratio: {enc_info['garbledRatio']:.2%}",
                "step": "navigate", "retryable": False,
            })
            log(f"[{ctx.place_id}] Encoding error detected")
            return False
    except Exception:
        pass

    # Error page detection
    try:
        page_text = await ctx.page.evaluate(
            "() => (document.body?.innerText || '').substring(0, 500)"
        )
        if any(kw in page_text for kw in ["\uC810\uAC80", "\uBD88\uAC00", "\uC624\uB958", "\uC720\uC9C0\uBCF4\uC218"]):
            text_len = await ctx.page.evaluate(JS_GET_PAGE_TEXT_LENGTH)
            if text_len < 500:
                ctx.result["status"] = "partial"
                ctx.result["errors"].append({
                    "type": "error_page",
                    "message": "Maintenance/error page detected",
                    "step": "navigate", "retryable": True,
                })
                log(f"[{ctx.place_id}] Error page detected")
    except Exception:
        pass

    # Anti-bot detection
    try:
        page_text = await ctx.page.evaluate(
            "() => (document.body?.innerText || '').substring(0, 1000)"
        )
        if "Checking your browser" in page_text or "CAPTCHA" in page_text:
            log(f"[{ctx.place_id}] Anti-bot detected, waiting 15s")
            await ctx.page.wait_for_timeout(15000)
            page_text = await ctx.page.evaluate(
                "() => (document.body?.innerText || '').substring(0, 1000)"
            )
            if "Checking your browser" in page_text or "CAPTCHA" in page_text:
                ctx.result["status"] = "requires_manual"
                ctx.result["errors"].append({
                    "type": "antibot",
                    "message": "CloudFlare/CAPTCHA not auto-resolved",
                    "step": "navigate", "retryable": False,
                })
                return False
    except Exception:
        pass

    # Splash page bypass
    try:
        splash_info = await ctx.page.evaluate(JS_SPLASH_DETECT)
        if (splash_info.get("totalLinks", 99) <= 10
                and splash_info.get("textLen", 9999) < 500
                and splash_info.get("firstHref")):
            internal_links = splash_info.get("internalLinks", [])
            best_link = splash_info["firstHref"]
            if len(internal_links) > 1:
                skin_kw = re.compile(
                    r"face|skin|\uD53C\uBD80|clinic|derma", re.IGNORECASE,
                )
                for link in internal_links:
                    if (skin_kw.search(link.get("href", ""))
                            or skin_kw.search(link.get("text", ""))):
                        best_link = link["href"]
                        break
            first_link = best_link
            log(f"[{ctx.place_id}] Splash page detected "
                f"({splash_info['totalLinks']} links, "
                f"{splash_info['textLen']} chars), "
                f"navigating to {first_link}")
            await ctx.page.goto(
                first_link, wait_until="domcontentloaded", timeout=15000,
            )
            try:
                final_url = await ctx.page.evaluate(
                    "() => window.location.href"
                )
                ctx.result["final_url"] = final_url
            except Exception:
                pass
    except Exception:
        pass

    return True


# ---------------------------------------------------------------------------
# Step 2: Dismiss Popups
# ---------------------------------------------------------------------------


async def step_dismiss_popups(ctx: CrawlContext) -> None:
    """Dismiss overlay popups (up to 3 attempts)."""
    log(f"[{ctx.place_id}] Checking for popups")
    for attempt in range(3):
        try:
            dismissed = await ctx.page.evaluate(JS_DISMISS_POPUPS)
            if dismissed == 0:
                break
            log(f"[{ctx.place_id}] Dismissed {dismissed} popup(s), "
                f"attempt {attempt + 1}")
            await ctx.page.wait_for_timeout(500)
        except Exception:
            break


# ---------------------------------------------------------------------------
# Step 3: SPA Content Wait
# ---------------------------------------------------------------------------


async def step_spa_wait(ctx: CrawlContext) -> None:
    """Wait for SPA content if page has minimal text."""
    try:
        text_len = await ctx.page.evaluate(JS_GET_PAGE_TEXT_LENGTH)
        if text_len < 200:
            log(f"[{ctx.place_id}] Minimal content ({text_len} chars), "
                f"waiting for SPA")
            spa_result = await ctx.page.evaluate(JS_SPA_WAIT)
            log(f"[{ctx.place_id}] SPA wait result: {spa_result}")
    except Exception:
        pass


# ---------------------------------------------------------------------------
# Step 4: Extract Social Channels
# ---------------------------------------------------------------------------


async def step_extract_social(ctx: CrawlContext) -> None:
    """Extract social consultation channels via multi-pass strategy."""
    log(f"[{ctx.place_id}] Extracting social channels")
    raw_channels = []

    # Pass 1 + 1.5 + 1.75 + 2 (static + iframe + structured + dynamic)
    try:
        channels = await ctx.page.evaluate(JS_SOCIAL_EXTRACT)
        raw_channels.extend(channels)
        log(f"[{ctx.place_id}] Found {len(channels)} channels "
            f"from main extraction")
    except Exception as e:
        ctx.result["errors"].append({
            "type": "extraction", "message": str(e)[:200],
            "step": "social", "retryable": False,
        })

    # Pass 2: window.open intercept
    try:
        intercepted = await ctx.page.evaluate(JS_WINDOW_OPEN_INTERCEPT)
        for u in intercepted:
            platform = classify_url(u)
            if platform:
                raw_channels.append({
                    "platform": platform, "url": u,
                    "method": "window_open_intercept",
                })
        if intercepted:
            log(f"[{ctx.place_id}] Intercepted {len(intercepted)} "
                f"window.open calls")
    except Exception:
        pass

    # Pass 2.5: Scroll-triggered elements
    try:
        scroll_results = await ctx.page.evaluate(JS_SCROLL_TRIGGER)
        for item in scroll_results:
            platform = classify_url(item.get("href", ""))
            if platform:
                raw_channels.append({
                    "platform": platform, "url": item["href"],
                    "method": "scroll_triggered",
                })
    except Exception:
        pass

    # Pass 4: URL Validation + de-duplication
    seen_urls = set()
    for ch in raw_channels:
        url_val = normalize_url(ch.get("url", ""))
        if not url_val or url_val in seen_urls:
            continue
        if url_val.startswith("widget:"):
            ctx.result["errors"].append({
                "type": "info",
                "message": f"Widget detected: {url_val}",
                "step": "social", "retryable": False,
            })
            continue
        seen_urls.add(url_val)
        platform = ch.get("platform") or classify_url(url_val)
        if platform:
            ctx.result["social_channels"].append({
                "platform": platform,
                "url": url_val,
                "extraction_method": ch.get("method", "unknown"),
                "confidence": 1.0,
                "status": "active",
            })

    # Pass 5: Resolve NaverShortlink (naver.me) URLs via redirect
    for ch in ctx.result["social_channels"]:
        if ch["platform"] != "NaverShortlink":
            continue
        try:
            new_page = await ctx.context.new_page()
            await new_page.goto(
                ch["url"], wait_until="commit", timeout=5000,
            )
            resolved = new_page.url
            await new_page.close()
            new_platform = classify_url(resolved)
            if new_platform and new_platform != "NaverShortlink":
                ch["platform"] = new_platform
                ch["url"] = normalize_url(resolved)
                log(f"[{ctx.place_id}] Resolved naver.me -> "
                    f"{new_platform}: {resolved[:80]}")
        except Exception:
            try:
                await new_page.close()
            except Exception:
                pass

    # Pass 6: Follow internal redirect links (always run to catch hidden social links)
    try:
        redirect_links = await ctx.page.evaluate(JS_REDIRECT_SCAN)
        if redirect_links:
            log(f"[{ctx.place_id}] Found {len(redirect_links)} "
                f"internal redirect candidates")
        for rl in redirect_links[:10]:
            try:
                redir_page = await ctx.context.new_page()
                await redir_page.goto(
                    rl["href"], wait_until="commit", timeout=8000,
                )
                resolved_url = redir_page.url
                await redir_page.close()
                resolved_norm = normalize_url(resolved_url)
                if resolved_norm and resolved_norm not in seen_urls:
                    platform = classify_url(resolved_norm)
                    if platform:
                        seen_urls.add(resolved_norm)
                        ctx.result["social_channels"].append({
                            "platform": platform,
                            "url": resolved_norm,
                            "extraction_method": "redirect_follow",
                            "confidence": 0.9,
                            "status": "active",
                        })
                        log(f"[{ctx.place_id}] Redirect resolved: "
                            f"{rl['text'][:20]} -> {platform}: "
                            f"{resolved_norm[:60]}")
            except Exception:
                try:
                    await redir_page.close()
                except Exception:
                    pass
    except Exception as e:
        log(f"[{ctx.place_id}] Redirect scan error: "
            f"{str(e)[:100]}")

    log(f"[{ctx.place_id}] Total social channels: "
        f"{len(ctx.result['social_channels'])}")


# ---------------------------------------------------------------------------
# Step 5: Collect Candidate URLs for Doctor Page
# ---------------------------------------------------------------------------


async def step_collect_candidates(ctx: CrawlContext) -> list:
    """Collect and deduplicate candidate URLs for doctor page discovery.

    Returns list of (url, source_label) tuples.
    """
    log(f"[{ctx.place_id}] Looking for doctor page")
    candidate_urls = []

    # Reveal hidden submenus via hover
    try:
        await ctx.page.evaluate(JS_REVEAL_SUBMENUS)
        await ctx.page.wait_for_timeout(500)
    except Exception:
        pass

    # Open mobile menu drawers (hamburger, bottom nav "메뉴", etc.)
    try:
        opened = await ctx.page.evaluate(JS_OPEN_MOBILE_MENUS)
        if opened:
            await ctx.page.wait_for_timeout(1000)
            log(f"[{ctx.place_id}] Opened {opened} mobile menu toggle(s)")
    except Exception:
        pass

    # Step 5a: Collect doctor menu links
    try:
        doctor_links = await ctx.page.evaluate(
            JS_FIND_DOCTOR_MENU,
            [DOCTOR_PRIMARY, DOCTOR_SECONDARY, DOCTOR_SUBMENU_PARENTS],
        )
        for link in (doctor_links or []):
            href = link.get("href", "")
            if href and href.startswith("http"):
                candidate_urls.append((href, f"menu:{link['text']}"))
        if doctor_links:
            log(f"[{ctx.place_id}] Found {len(doctor_links)} "
                f"doctor menu link(s)")
        else:
            log(f"[{ctx.place_id}] No doctor menu found")
    except Exception as e:
        log(f"[{ctx.place_id}] Doctor menu search error: "
            f"{str(e)[:100]}")

    # Step 5b-1: Navigate to intro/about pages, scan for doctor sub-links
    if True:
        try:
            intro_links = await ctx.page.evaluate(JS_FIND_INTRO_LINKS)
            for link in (intro_links or []):
                log(f"[{ctx.place_id}] Scanning intro page: "
                    f"{link['text']} -> {link['href']}")
                try:
                    if link["href"].startswith("javascript:"):
                        continue
                    await ctx.page.goto(
                        link["href"],
                        wait_until="domcontentloaded", timeout=15000,
                    )
                    await ctx.page.wait_for_timeout(1500)

                    # Opportunistic social extraction from sub-pages
                    if not ctx.result["social_channels"]:
                        try:
                            sub_channels = await ctx.page.evaluate(
                                JS_SOCIAL_EXTRACT,
                            )
                            for ch in (sub_channels or []):
                                url_val = normalize_url(ch.get("url", ""))
                                platform = classify_url(url_val)
                                if platform and url_val:
                                    ctx.result["social_channels"].append({
                                        "platform": platform,
                                        "url": url_val,
                                        "extraction_method": "subpage_scan",
                                        "confidence": 0.9,
                                        "status": "active",
                                    })
                            if ctx.result["social_channels"]:
                                log(f"[{ctx.place_id}] Sub-page found "
                                    f"{len(ctx.result['social_channels'])} "
                                    f"social channels")
                        except Exception:
                            pass

                    doctor_links_2nd = await ctx.page.evaluate(
                        JS_FIND_DOCTOR_SUBLINKS,
                    )
                    for dl in (doctor_links_2nd or []):
                        if dl["href"] and dl["href"].startswith("http"):
                            candidate_urls.append(
                                (dl["href"], f"intro_sub:{dl['text']}"),
                            )
                except Exception:
                    pass
                candidate_urls.append(
                    (link["href"], f"intro_page:{link['text']}"),
                )
        except Exception as e:
            log(f"[{ctx.place_id}] Intro page scan error: "
                f"{str(e)[:100]}")

    # Step 5b-2: Sitemap
    try:
        sitemap_url = f"{ctx.base_url}/sitemap.xml"
        await ctx.page.goto(
            sitemap_url, wait_until="domcontentloaded", timeout=10000,
        )
        sitemap_text = await ctx.page.evaluate(
            "() => document.body?.innerText || ''",
        )
        doc_patterns = [
            "/doctor", "/staff", "/team", "/about", "/introduce",
            "/intro", "/\uC758\uB8CC\uC9C4", "/\uC6D0\uC7A5", "/\uC804\uBB38\uC758",
        ]
        for pattern in doc_patterns:
            matches = re.findall(
                rf"(https?://[^\s<]+{re.escape(pattern)}[^\s<]*)",
                sitemap_text,
            )
            for doc_url in matches:
                candidate_urls.append((doc_url, f"sitemap:{pattern}"))
    except Exception:
        pass

    # Step 5-iframe: Handle frame-based sites (e.g. 뉴케이의원)
    # When the main page has very little text and uses frames/iframes,
    # navigate into the frame content and re-scan for doctor menu links.
    if not candidate_urls:
        try:
            await ctx.page.goto(
                ctx.url, wait_until="domcontentloaded", timeout=15000,
            )
            frame_info = await ctx.page.evaluate(JS_DETECT_FRAMES)
            if (frame_info["bodyTextLength"] < 200
                    and frame_info["frameCount"] > 0):
                log(f"[{ctx.place_id}] Frame-based site detected "
                    f"({frame_info['frameCount']} frames, "
                    f"{frame_info['bodyTextLength']} chars)")
                for frame_src in frame_info["frameSrcs"][:3]:
                    abs_url = urljoin(ctx.url, frame_src)
                    try:
                        await ctx.page.goto(
                            abs_url, wait_until="domcontentloaded",
                            timeout=15000,
                        )
                        await ctx.page.wait_for_timeout(2000)

                        # Check for nested frames (up to 1 level deep)
                        inner = await ctx.page.evaluate(JS_DETECT_FRAMES)
                        if (inner["bodyTextLength"] < 200
                                and inner["frameCount"] > 0):
                            for inner_src in inner["frameSrcs"][:3]:
                                inner_abs = urljoin(abs_url, inner_src)
                                try:
                                    await ctx.page.goto(
                                        inner_abs,
                                        wait_until="domcontentloaded",
                                        timeout=10000,
                                    )
                                    await ctx.page.wait_for_timeout(1500)
                                    txt_len = await ctx.page.evaluate(
                                        JS_GET_PAGE_TEXT_LENGTH,
                                    )
                                    if txt_len > 200:
                                        abs_url = inner_abs
                                        break
                                except Exception:
                                    pass

                        # Re-run menu detection from frame content
                        doctor_links = await ctx.page.evaluate(
                            JS_FIND_DOCTOR_MENU,
                            [DOCTOR_PRIMARY, DOCTOR_SECONDARY,
                             DOCTOR_SUBMENU_PARENTS],
                        )
                        for link in (doctor_links or []):
                            href = link.get("href", "")
                            if href and href.startswith("http"):
                                candidate_urls.append(
                                    (href, f"frame_menu:{link['text']}"),
                                )
                            elif href:
                                resolved = urljoin(abs_url, href)
                                candidate_urls.append(
                                    (resolved, f"frame_menu:{link['text']}"),
                                )
                        if doctor_links:
                            log(f"[{ctx.place_id}] Found "
                                f"{len(doctor_links)} doctor link(s) "
                                f"in frame")

                        # Add frame content page itself as candidate
                        current = await ctx.page.evaluate(
                            "() => window.location.href",
                        )
                        candidate_urls.append(
                            (current, "frame_content"),
                        )
                        if doctor_links:
                            break
                    except Exception:
                        pass
        except Exception:
            pass

    # Step 5c: Main page as last resort
    candidate_urls.append((ctx.url, "main_page"))

    # Deduplicate preserving priority order
    seen_urls = set()
    unique_candidates = []
    for c_url, source in candidate_urls:
        normalized = c_url.rstrip("/")
        if normalized not in seen_urls:
            seen_urls.add(normalized)
            unique_candidates.append((c_url, source))

    log(f"[{ctx.place_id}] Collected {len(unique_candidates)} "
        f"candidate URLs:")
    for i, (c_url, source) in enumerate(unique_candidates):
        log(f"[{ctx.place_id}]   [{i + 1}] {source} -> {c_url}")

    return unique_candidates


# ---------------------------------------------------------------------------
# Step 6: Extract Doctor Info (sub-function: AI navigation)
# ---------------------------------------------------------------------------


async def _try_ai_navigation(
    ctx: CrawlContext, ocr_state: OcrState, seen_candidate_urls: set,
) -> None:
    """Phase 2: AI-assisted navigation discovery using Gemini."""
    log(f"[{ctx.place_id}] Phase 2: AI navigation discovery from main page")
    try:
        await ctx.page.goto(
            ctx.url, wait_until="domcontentloaded", timeout=15000,
        )
        await ctx.page.wait_for_timeout(2000)

        ts_nav = int(time.time())
        nav_path = f"/tmp/clinic_nav_{ctx.place_id}_{ts_nav}.jpg"
        await ctx.page.screenshot(
            path=nav_path, full_page=False, type="jpeg", quality=85,
        )
        ocr_state.temp_screenshots.append(nav_path)

        nav_prompt = (
            f"Read the image file at {nav_path}.\n\n"
            "This is a Korean skin/dermatology clinic website homepage.\n\n"
            "TASK 1: Are doctor names, photos, or medical credentials "
            "visible on THIS page? If yes, extract them.\n\n"
            "TASK 2: Look at the navigation menu (top bar, sidebar, "
            "footer). Which menu or link most likely leads to a "
            "doctor/medical staff page?\n"
            "Common labels: \uC758\uB8CC\uC9C4, \uC6D0\uC7A5, \uC804\uBB38\uC758, \uBCD1\uC6D0\uC18C\uAC1C, "
            "About, Staff, Team\n\n"
            "Return ONLY JSON (no markdown fences):\n"
            '{"doctors": [{"name": "...", "role": "..."}], '
            '"suggested_paths": ["/path1", "/path2"]}\n'
            "doctors: any doctors visible on THIS page ([] if none)\n"
            "suggested_paths: relative URL paths likely containing "
            "doctor info"
        )

        r_nav = subprocess.run(
            ["gemini", "-m", "gemini-3-flash-preview", "-p", nav_prompt,
             "-y", "--include-directories", os.path.dirname(nav_path)],
            capture_output=True, text=True, timeout=90,
        )

        if r_nav.returncode == 0:
            nav_json = re.search(r'\{[\s\S]*\}', r_nav.stdout)
            if nav_json:
                nav_data = json.loads(nav_json.group(0))

                for doc in nav_data.get("doctors", []):
                    name = doc.get("name", "")
                    if (name
                            and is_plausible_korean_name(name)
                            and name not in ocr_state.seen_names):
                        ocr_state.seen_names.add(name)
                        profile_raw = (
                            doc.get("profile_raw")
                            or (doc.get("education", [])
                                + doc.get("career", [])
                                + doc.get("credentials", []))
                        )
                        ctx.result["doctors"].append({
                            "name": name, "name_english": "",
                            "role": doc.get("role", "specialist"),
                            "photo_url": "",
                            "profile_raw": profile_raw,
                            "page_text": "", "source_url": "",
                            "screenshot_path": "",
                            "branch": "", "branches": [],
                            "extraction_source": "ai_nav",
                            "ocr_source": True,
                        })

                if ctx.result["doctors"]:
                    ctx.doctor_page_found = True
                    log(f"[{ctx.place_id}] AI found "
                        f"{len(ctx.result['doctors'])} doctors on "
                        f"main page")

                if not ctx.result["doctors"]:
                    ai_paths = nav_data.get("suggested_paths", [])
                    log(f"[{ctx.place_id}] AI suggested "
                        f"{len(ai_paths)} paths: {ai_paths}")

                    for ai_path in ai_paths[:3]:
                        try:
                            ai_url = urljoin(
                                ctx.base_url + "/", ai_path,
                            )
                            if ai_url.rstrip("/") in seen_candidate_urls:
                                continue

                            log(f"[{ctx.place_id}] Trying AI "
                                f"suggestion: {ai_path} -> {ai_url}")
                            await ctx.page.goto(
                                ai_url,
                                wait_until="domcontentloaded",
                                timeout=15000,
                            )
                            await ctx.page.wait_for_timeout(2000)

                            for _ in range(8):
                                await ctx.page.evaluate(
                                    "window.scrollBy(0, 600)",
                                )
                                await ctx.page.wait_for_timeout(400)

                            doctors = await ctx.page.evaluate(
                                JS_EXTRACT_DOCTORS,
                            )
                            if doctors:
                                valid_doctors = [
                                    d for d in doctors
                                    if is_plausible_korean_name(
                                        d.get("name", ""),
                                    )
                                ]
                                if valid_doctors:
                                    ctx.result["doctors"] = valid_doctors
                                    ctx.doctor_page_found = True
                                    log(
                                        f"[{ctx.place_id}] AI path "
                                        f"DOM: {len(valid_doctors)} "
                                        f"valid / {len(doctors)} total",
                                    )
                                    break

                            ts_ai = int(time.time())
                            ai_ss = (
                                f"/tmp/clinic_ai_"
                                f"{ctx.place_id}_{ts_ai}.jpg"
                            )
                            await ctx.page.evaluate(
                                "window.scrollTo(0, 0)",
                            )
                            await ctx.page.wait_for_timeout(300)
                            await ctx.page.screenshot(
                                path=ai_ss, full_page=True,
                                type="jpeg", quality=85,
                            )
                            ocr_state.temp_screenshots.append(ai_ss)

                            prompt_ai = OCR_PROMPT_TEMPLATE.replace(
                                "{path}", ai_ss,
                            )
                            ai_docs = run_gemini_ocr(prompt_ai, ai_ss)
                            append_ocr_doctors(
                                ai_docs, ocr_state.seen_names,
                                ctx.result["doctors"],
                            )

                            if ctx.result["doctors"]:
                                ctx.doctor_page_found = True
                                log(
                                    f"[{ctx.place_id}] AI path OCR: "
                                    f"{len(ctx.result['doctors'])} "
                                    f"doctors",
                                )
                                break
                        except Exception as e:
                            log(f"[{ctx.place_id}] AI path error: "
                                f"{str(e)[:100]}")
                            continue

    except subprocess.TimeoutExpired:
        log(f"[{ctx.place_id}] AI navigation timeout")
    except Exception as e:
        log(f"[{ctx.place_id}] AI navigation error: {str(e)[:100]}")


# ---------------------------------------------------------------------------
# Step 6: Extract Doctor Info (main)
# ---------------------------------------------------------------------------


async def step_extract_doctors(
    ctx: CrawlContext, candidates: list,
) -> None:
    """Extract doctor info by iterating through candidate URLs.

    Uses DOM extraction, OCR fallback, and AI navigation discovery.
    """
    ocr_state = OcrState()

    # Track best result across ALL candidates (don't stop at first match)
    best_doctors = []       # doctors list from best candidate so far
    best_valid_count = 0    # number of doctors with real credentials
    best_source = ""        # source label of best candidate
    branch_attempted = False  # prevent infinite branch-click loops

    try:
        for cand_idx, (cand_url, cand_source) in enumerate(candidates):
            log(f"[{ctx.place_id}] Trying candidate "
                f"{cand_idx + 1}/{len(candidates)}: {cand_source}")

            # Skip javascript: URLs (can't navigate to them)
            if cand_url.startswith("javascript:"):
                log(f"[{ctx.place_id}] Skipping javascript: URL")
                continue

            # Navigate to candidate
            try:
                await ctx.page.goto(
                    cand_url, wait_until="domcontentloaded", timeout=15000,
                )
                await ctx.page.wait_for_timeout(1500)
            except Exception as e:
                log(f"[{ctx.place_id}] Navigation failed for "
                    f"{cand_url}: {str(e)[:100]}")
                continue

            # Scroll for lazy loading
            try:
                for _ in range(10):
                    await ctx.page.evaluate("window.scrollBy(0, 600)")
                    await ctx.page.wait_for_timeout(500)
                await ctx.page.wait_for_timeout(1000)
            except Exception:
                pass

            # Click tabs with doctor keywords
            try:
                tab_texts = await ctx.page.evaluate(JS_FIND_DOCTOR_TABS)
                for tab_text in (tab_texts or []):
                    try:
                        await ctx.page.get_by_text(
                            tab_text, exact=True,
                        ).first.click(timeout=3000)
                        await ctx.page.wait_for_timeout(1000)
                        log(f"[{ctx.place_id}] Clicked tab: {tab_text}")
                    except Exception:
                        pass
            except Exception:
                pass

            # Capture page text and source URL for this candidate
            try:
                cand_page_text = await ctx.page.evaluate(JS_EXTRACT_PAGE_TEXT)
                cand_source_url = await ctx.page.evaluate("() => window.location.href")
            except Exception:
                cand_page_text = ""
                cand_source_url = cand_url

            # DOM extraction
            try:
                is_image_based = await ctx.page.evaluate(
                    JS_CHECK_IMAGE_BASED,
                )

                need_ocr = is_image_based
                if not is_image_based:
                    doctors = await ctx.page.evaluate(JS_EXTRACT_DOCTORS)
                    if doctors:
                        valid_doctors = [
                            d for d in doctors
                            if is_plausible_korean_name(d.get("name", ""))
                        ]
                        if valid_doctors:
                            # LLM verification: screenshot + candidates → Gemini
                            verify_ss = tempfile.mktemp(
                                suffix=".jpg", prefix="verify_",
                            )
                            try:
                                await ctx.page.screenshot(
                                    path=verify_ss, full_page=True,
                                    type="jpeg", quality=60,
                                )
                                valid_doctors = verify_doctors_with_llm(
                                    valid_doctors, verify_ss, ctx.place_id,
                                )
                                ocr_state.temp_screenshots.append(verify_ss)
                            except Exception as e:
                                log(f"[{ctx.place_id}] LLM verify screenshot "
                                    f"error: {e}")
                        if valid_doctors:
                            # Codex CLI validation: filter noise, check real credentials
                            validated, any_valid = validate_doctors(
                                valid_doctors, ctx.place_id, ctx.name,
                            )
                            # Use Codex-validated list if available,
                            # otherwise fall back to raw DOM doctors
                            dom_result = validated if validated else valid_doctors
                            dom_result = _dedup_cross_contaminated(dom_result, ctx.place_id)
                            dom_result = _filter_by_branch(dom_result, ctx.name, ctx.place_id)
                            if dom_result:
                                for d in dom_result:
                                    d["page_text"] = cand_page_text
                                    d["source_url"] = cand_source_url
                                # Count doctors with actual credentials
                                cred_count = sum(
                                    1 for d in dom_result
                                    if d.get("profile_raw")
                                )
                                log(f"[{ctx.place_id}] DOM: "
                                    f"{len(dom_result)} doctors, "
                                    f"{cred_count} with credentials "
                                    f"from {cand_source}")
                                # Track best result across all candidates
                                # Skip results exceeding chain cap (cross-branch)
                                if len(dom_result) > _CHAIN_CAP:
                                    log(f"[{ctx.place_id}] Skipping "
                                        f"{cand_source}: {len(dom_result)} "
                                        f"doctors exceeds chain cap "
                                        f"{_CHAIN_CAP}")
                                elif cred_count > best_valid_count:
                                    best_doctors = dom_result
                                    best_valid_count = cred_count
                                    best_source = f"dom:{cand_source}"
                                elif (cred_count == best_valid_count
                                      and len(dom_result) > len(best_doctors)):
                                    best_doctors = dom_result
                                    best_source = f"dom:{cand_source}"
                                # If ALL doctors have credentials, no need to search more
                                if cred_count == len(dom_result) and cred_count > 0:
                                    log(f"[{ctx.place_id}] All {cred_count} "
                                        f"doctors have credentials, "
                                        f"accepting from {cand_source}")
                                    break
                                # Otherwise keep searching (OCR may find credentials)
                                need_ocr = True
                                continue
                            else:
                                need_ocr = True
                        else:
                            log(f"[{ctx.place_id}] DOM: "
                                f"{len(doctors)} entries but 0 valid "
                                f"names from {cand_source}, "
                                f"falling back to OCR")
                            need_ocr = True
                    else:
                        log(f"[{ctx.place_id}] DOM: 0 doctors "
                            f"from {cand_source}")
                        need_ocr = True
                else:
                    log(f"[{ctx.place_id}] Image-based page: "
                        f"{cand_source}")

                # Branch selector: for chain hospitals, click matching
                # branch and follow doctor sub-link (e.g. 바로그의원)
                if need_ocr and not best_doctors and not branch_attempted:
                    branch_name = _extract_branch_name(ctx.name)
                    if branch_name:
                        try:
                            result = await ctx.page.evaluate(
                                JS_CLICK_BRANCH_AND_GET_DOCTOR,
                                branch_name,
                            )
                            if result and result.get("href"):
                                branch_attempted = True
                                branch_url = result["href"]
                                log(f"[{ctx.place_id}] Clicked branch "
                                    f"selector: {result['clicked']}")
                                log(f"[{ctx.place_id}] Found branch "
                                    f"doctor page: {branch_url}")
                                candidates.append(
                                    (branch_url,
                                     f"branch:{cand_source}"),
                                )
                                continue  # skip OCR, process branch URL next
                        except Exception:
                            pass

                if need_ocr:
                    # Scroll to load lazy images
                    try:
                        scroll_h = await ctx.page.evaluate(
                            "() => document.body.scrollHeight",
                        )
                        for pos in range(0, scroll_h, 600):
                            await ctx.page.evaluate(
                                f"window.scrollTo(0, {pos})",
                            )
                            await ctx.page.wait_for_timeout(300)
                    except Exception:
                        pass

                    ts = int(time.time())
                    fullpage_path = (
                        f"/tmp/clinic_crawl_"
                        f"{ctx.place_id}_{ts}.jpg"
                    )
                    await ctx.page.evaluate("window.scrollTo(0, 0)")
                    await ctx.page.wait_for_timeout(300)
                    await ctx.page.screenshot(
                        path=fullpage_path, full_page=True,
                        type="jpeg", quality=85,
                    )
                    ocr_state.last_screenshot_path = fullpage_path
                    ocr_state.temp_screenshots.append(fullpage_path)

                    # Tier B: one OCR attempt per candidate
                    try:
                        log(f"[{ctx.place_id}] OCR Tier B on "
                            f"{cand_source}")
                        prompt_b = OCR_PROMPT_TEMPLATE.replace(
                            "{path}", fullpage_path,
                        )
                        doctors_raw = run_gemini_ocr(
                            prompt_b, fullpage_path,
                        )
                        ocr_doctors_tmp = []
                        ocr_seen_tmp = set(ocr_state.seen_names)
                        added = append_ocr_doctors(
                            doctors_raw, ocr_seen_tmp,
                            ocr_doctors_tmp,
                        )
                        if ocr_doctors_tmp:
                            cred_count = sum(
                                1 for d in ocr_doctors_tmp
                                if d.get("profile_raw")
                            )
                            log(f"[{ctx.place_id}] OCR: {added} "
                                f"doctors, {cred_count} with "
                                f"credentials from {cand_source}")
                            if len(ocr_doctors_tmp) > _CHAIN_CAP:
                                log(f"[{ctx.place_id}] Skipping "
                                    f"OCR {cand_source}: "
                                    f"{len(ocr_doctors_tmp)} doctors "
                                    f"exceeds chain cap {_CHAIN_CAP}")
                            elif cred_count > best_valid_count:
                                best_doctors = ocr_doctors_tmp
                                best_valid_count = cred_count
                                best_source = f"ocr:{cand_source}"
                                ocr_state.seen_names = ocr_seen_tmp
                        else:
                            log(f"[{ctx.place_id}] OCR: 0 doctors "
                                f"from {cand_source}")
                    except subprocess.TimeoutExpired:
                        log(f"[{ctx.place_id}] OCR timeout on "
                            f"{cand_source}, trying next candidate")
                    except FileNotFoundError:
                        log(f"[{ctx.place_id}] Gemini CLI "
                            f"not installed")
                        break

            except Exception as e:
                log(f"[{ctx.place_id}] Extraction error on "
                    f"{cand_source}: {str(e)[:100]}")

        # Accept best result found across all candidates
        if best_doctors:
            ctx.result["doctors"] = best_doctors
            ctx.doctor_page_found = True
            log(f"[{ctx.place_id}] Best result: {len(best_doctors)} "
                f"doctors ({best_valid_count} with credentials) "
                f"from {best_source}")

        # After ALL candidates exhausted - final OCR fallback
        if not ctx.result["doctors"] and ocr_state.last_screenshot_path:
            log(f"[{ctx.place_id}] All {len(candidates)} candidates "
                f"returned 0. Final OCR attempt.")

            # Tier B retry on last screenshot
            try:
                log(f"[{ctx.place_id}] OCR Tier B retry on last page")
                prompt_retry = OCR_PROMPT_TEMPLATE.replace(
                    "{path}", ocr_state.last_screenshot_path,
                )
                retry_docs = run_gemini_ocr(
                    prompt_retry, ocr_state.last_screenshot_path,
                )
                append_ocr_doctors(
                    retry_docs, ocr_state.seen_names,
                    ctx.result["doctors"],
                )
            except Exception:
                pass

            if not ctx.result["doctors"]:
                # Tier C: viewport chunks on last page
                chunk_paths = []
                try:
                    vp_height = 900
                    scroll_h = await ctx.page.evaluate(
                        "() => document.body.scrollHeight",
                    )
                    for i, pos in enumerate(
                        range(0, scroll_h, vp_height),
                    ):
                        await ctx.page.evaluate(
                            f"window.scrollTo(0, {pos})",
                        )
                        await ctx.page.wait_for_timeout(300)
                        chunk_path = (
                            f"/tmp/clinic_crawl_"
                            f"{ctx.place_id}"
                            f"_{int(time.time())}_{i}.jpg"
                        )
                        await ctx.page.screenshot(
                            path=chunk_path, full_page=False,
                            type="jpeg", quality=85,
                        )
                        chunk_paths.append(chunk_path)
                        if len(chunk_paths) >= 8:
                            break
                    log(f"[{ctx.place_id}] OCR Tier C: "
                        f"{len(chunk_paths)} viewport chunks")
                except Exception:
                    pass

                for cp in chunk_paths:
                    try:
                        prompt_c = OCR_PROMPT_TEMPLATE.replace(
                            "{path}", cp,
                        )
                        chunk_docs = run_gemini_ocr(prompt_c, cp)
                        append_ocr_doctors(
                            chunk_docs, ocr_state.seen_names,
                            ctx.result["doctors"],
                        )
                    except Exception:
                        pass

                ocr_state.temp_screenshots.extend(chunk_paths)

            if ctx.result["doctors"]:
                ctx.doctor_page_found = True
                log(f"[{ctx.place_id}] Final OCR: "
                    f"{len(ctx.result['doctors'])} doctors found")

        # Phase 2: AI-assisted navigation discovery
        if not ctx.result["doctors"]:
            seen_candidate_urls = {
                u.rstrip("/") for u, _ in candidates
            }
            await _try_ai_navigation(
                ctx, ocr_state, seen_candidate_urls,
            )

        # Persist screenshots to permanent storage
        await _persist_screenshots(ctx, ocr_state)

        # Save screenshot if all methods exhausted
        if not ctx.result["doctors"] and ocr_state.last_screenshot_path:
            log(f"[{ctx.place_id}] All methods exhausted. "
                f"Screenshot saved for review.")
            ctx.result["errors"].append({
                "type": "all_methods_exhausted",
                "message": (
                    f"Rule-based ({len(candidates)} candidates) + "
                    f"AI navigation all failed."
                ),
                "step": "doctor_extract", "retryable": True,
            })

        # Codex validation on final doctors (covers all paths: DOM, OCR, AI)
        # DOM path already validates inside the candidate loop, but OCR
        # fallback paths (Tier B retry, Tier C, AI navigation) skip it.
        # Running once here ensures uniform quality regardless of source.
        if ctx.result["doctors"]:
            has_ocr = any(
                d.get("ocr_source") for d in ctx.result["doctors"]
            )
            if has_ocr:
                validated_final, any_valid = validate_doctors(
                    ctx.result["doctors"], ctx.place_id, ctx.name,
                )
                if validated_final:
                    validated_final = _dedup_cross_contaminated(
                        validated_final, ctx.place_id,
                    )
                    ctx.result["doctors"] = validated_final

        # Deduplicate doctors by name within same hospital
        if ctx.result["doctors"]:
            seen_dedup = set()
            unique_docs = []
            for doc in ctx.result["doctors"]:
                dname = doc.get("name", "")
                if dname and dname not in seen_dedup:
                    seen_dedup.add(dname)
                    unique_docs.append(doc)
            if len(unique_docs) < len(ctx.result["doctors"]):
                log(f"[{ctx.place_id}] Deduplicated: "
                    f"{len(ctx.result['doctors'])} -> {len(unique_docs)}")
            ctx.result["doctors"] = unique_docs

        # Chain hospital cap: if >_CHAIN_CAP doctors after all filtering,
        # likely cross-branch contamination — flag and truncate
        if len(ctx.result["doctors"]) > _CHAIN_CAP:
            log(f"[{ctx.place_id}] Chain cap: {len(ctx.result['doctors'])} "
                f"doctors exceeds {_CHAIN_CAP}, likely cross-branch "
                f"contamination. Clearing doctor list.")
            ctx.result["errors"].append({
                "type": "chain_contamination",
                "message": (
                    f"Extracted {len(ctx.result['doctors'])} doctors, "
                    f"exceeds chain cap {_CHAIN_CAP}. "
                    f"Likely cross-branch data."
                ),
                "step": "doctor_extract", "retryable": False,
            })
            ctx.result["doctors"] = []

        log(f"[{ctx.place_id}] Doctor extraction complete: "
            f"{len(ctx.result['doctors'])} doctors")

    except Exception as e:
        ctx.result["errors"].append({
            "type": "extraction", "message": str(e)[:200],
            "step": "doctor_extract", "retryable": True,
        })
    finally:
        # Clean up temp screenshots that were NOT persisted
        for sp in ocr_state.temp_screenshots:
            if not sp.startswith("/tmp/"):
                continue
            try:
                os.remove(sp)
            except OSError:
                pass


# ---------------------------------------------------------------------------
# Step 7: Determine Final Status
# ---------------------------------------------------------------------------


async def _persist_screenshots(ctx: CrawlContext, ocr_state: OcrState) -> None:
    """Copy screenshots and upload to Drive without blocking the event loop."""
    # steps.py is at scripts/clinic-storage/clinic_crawler/steps.py
    # Need 4 levels up to reach project root (claude-craft/)
    project_root = os.path.dirname(
        os.path.dirname(
            os.path.dirname(
                os.path.dirname(os.path.abspath(__file__))
            )
        )
    )
    save_dir = os.path.join(project_root, SCREENSHOT_DIR)
    os.makedirs(save_dir, exist_ok=True)

    # Persist the last screenshot (main doctor page)
    if ocr_state.last_screenshot_path and os.path.exists(ocr_state.last_screenshot_path):
        save_path = os.path.join(
            save_dir, f"{ctx.place_id}_doctors.jpg",
        )
        await asyncio.to_thread(shutil.copy2, ocr_state.last_screenshot_path, save_path)
        stored_ref = save_path
        upload_succeeded = False

        if is_drive_enabled():
            try:
                uploaded = await asyncio.to_thread(
                    upload_screenshot, save_path, ctx.place_id
                )
                stored_ref = uploaded.url
                upload_succeeded = True
                log(f"[{ctx.place_id}] Uploaded screenshot to Google Drive: {uploaded.file_id}")
            except Exception as e:
                log(f"[{ctx.place_id}] Drive upload failed, fallback to local path: {str(e)[:120]}")
                ctx.result["errors"].append({
                    "type": "screenshot_upload",
                    "message": str(e)[:200],
                    "step": "doctor_extract", "retryable": True,
                })

        if upload_succeeded and is_drive_enabled() and not keep_local_copy_after_upload():
            try:
                await asyncio.to_thread(os.remove, save_path)
                log(f"[{ctx.place_id}] Removed local screenshot after Drive upload")
            except OSError as e:
                log(f"[{ctx.place_id}] Local screenshot cleanup failed: {str(e)[:120]}")

        # Attach screenshot_path to all doctors that don't have one
        for doc in ctx.result["doctors"]:
            if not doc.get("screenshot_path"):
                doc["screenshot_path"] = stored_ref


# ---------------------------------------------------------------------------
# Step 7: Determine Final Status
# ---------------------------------------------------------------------------


def step_determine_status(ctx: CrawlContext) -> None:
    """Set final crawl status based on extracted data."""
    has_social = len(ctx.result["social_channels"]) > 0
    has_doctors = len(ctx.result["doctors"]) > 0

    ctx.result["doctor_page_exists"] = (
        1 if (ctx.doctor_page_found or has_doctors) else 0
    )

    if ctx.result["status"] == "success":
        if has_social and has_doctors:
            pass
        elif has_social or has_doctors:
            ctx.result["status"] = "partial"
            missing = "doctors" if not has_doctors else "social_channels"
            ctx.result["errors"].append({
                "type": "partial_data",
                "message": (
                    f"Missing {missing}: "
                    f"social={len(ctx.result['social_channels'])}, "
                    f"doctors={len(ctx.result['doctors'])}"
                ),
                "step": "final_status", "retryable": True,
            })
        else:
            ctx.result["status"] = "empty"


# ---------------------------------------------------------------------------
# Step 8: Save Results
# ---------------------------------------------------------------------------


def step_save_results(result: dict, db_path: str) -> None:
    """Save crawl results to SQLite database."""
    from storage_manager import save_result

    place_id = result["place_id"]
    log(f"[{place_id}] Saving results (status={result['status']}, "
        f"channels={len(result['social_channels'])}, "
        f"doctors={len(result['doctors'])})")
    try:
        save_result(db_path, result)
        log(f"[{place_id}] Saved to {db_path}")
    except Exception as e:
        result["errors"].append({
            "type": "storage_error", "message": str(e)[:200],
            "step": "save", "retryable": True,
        })
        log(f"[{place_id}] Storage error: {e}")
