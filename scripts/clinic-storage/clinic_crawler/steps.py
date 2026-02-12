"""Step functions for the clinic crawl pipeline.

Each step operates on a CrawlContext dataclass that holds shared state.
Extracted from crawl_hospital() in crawl_single.py during Phase 3 refactoring.
"""

from __future__ import annotations

import json
import os
import re
import shutil
import subprocess
import time
from dataclasses import dataclass, field
from typing import Any
from urllib.parse import urljoin, urlparse

from clinic_crawler.constants import (
    DOCTOR_PRIMARY,
    DOCTOR_SECONDARY,
    DOCTOR_SUBMENU_PARENTS,
)
from clinic_crawler.js_snippets import (
    JS_CHECK_ENCODING,
    JS_CHECK_IMAGE_BASED,
    JS_DETECT_CMS,
    JS_DISMISS_POPUPS,
    JS_EXTRACT_DOCTORS,
    JS_FIND_DOCTOR_MENU,
    JS_FIND_DOCTOR_SUBLINKS,
    JS_FIND_DOCTOR_TABS,
    JS_FIND_INTRO_LINKS,
    JS_GET_PAGE_TEXT_LENGTH,
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
from clinic_crawler.url_utils import classify_url, normalize_url


@dataclass
class CrawlContext:
    """Shared state container for the crawl pipeline."""

    hospital_no: int
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
    log(f"#{ctx.hospital_no} Starting crawl: {ctx.url}")

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
                log(f"#{ctx.hospital_no} robots.txt blocks all paths")
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
    log(f"#{ctx.hospital_no} Navigating to {ctx.url}")
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
        log(f"#{ctx.hospital_no} Navigation failed: {err_msg[:100]}")
        return False

    # Redirect detection
    try:
        final_url = await ctx.page.evaluate("() => window.location.href")
        if final_url and final_url != ctx.url:
            ctx.result["final_url"] = final_url
            log(f"#{ctx.hospital_no} Redirected to {final_url}")
    except Exception:
        pass

    # CMS detection
    try:
        cms = await ctx.page.evaluate(JS_DETECT_CMS)
        if cms:
            ctx.result["cms_platform"] = cms
            log(f"#{ctx.hospital_no} CMS: {cms}")
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
            log(f"#{ctx.hospital_no} Encoding error detected")
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
                log(f"#{ctx.hospital_no} Error page detected")
    except Exception:
        pass

    # Anti-bot detection
    try:
        page_text = await ctx.page.evaluate(
            "() => (document.body?.innerText || '').substring(0, 1000)"
        )
        if "Checking your browser" in page_text or "CAPTCHA" in page_text:
            log(f"#{ctx.hospital_no} Anti-bot detected, waiting 15s")
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
            log(f"#{ctx.hospital_no} Splash page detected "
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
    log(f"#{ctx.hospital_no} Checking for popups")
    for attempt in range(3):
        try:
            dismissed = await ctx.page.evaluate(JS_DISMISS_POPUPS)
            if dismissed == 0:
                break
            log(f"#{ctx.hospital_no} Dismissed {dismissed} popup(s), "
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
            log(f"#{ctx.hospital_no} Minimal content ({text_len} chars), "
                f"waiting for SPA")
            spa_result = await ctx.page.evaluate(JS_SPA_WAIT)
            log(f"#{ctx.hospital_no} SPA wait result: {spa_result}")
    except Exception:
        pass


# ---------------------------------------------------------------------------
# Step 4: Extract Social Channels
# ---------------------------------------------------------------------------


async def step_extract_social(ctx: CrawlContext) -> None:
    """Extract social consultation channels via multi-pass strategy."""
    log(f"#{ctx.hospital_no} Extracting social channels")
    raw_channels = []

    # Pass 1 + 1.5 + 1.75 + 2 (static + iframe + structured + dynamic)
    try:
        channels = await ctx.page.evaluate(JS_SOCIAL_EXTRACT)
        raw_channels.extend(channels)
        log(f"#{ctx.hospital_no} Found {len(channels)} channels "
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
            log(f"#{ctx.hospital_no} Intercepted {len(intercepted)} "
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
                log(f"#{ctx.hospital_no} Resolved naver.me -> "
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
            log(f"#{ctx.hospital_no} Found {len(redirect_links)} "
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
                        log(f"#{ctx.hospital_no} Redirect resolved: "
                            f"{rl['text'][:20]} -> {platform}: "
                            f"{resolved_norm[:60]}")
            except Exception:
                try:
                    await redir_page.close()
                except Exception:
                    pass
    except Exception as e:
        log(f"#{ctx.hospital_no} Redirect scan error: "
            f"{str(e)[:100]}")

    log(f"#{ctx.hospital_no} Total social channels: "
        f"{len(ctx.result['social_channels'])}")


# ---------------------------------------------------------------------------
# Step 5: Collect Candidate URLs for Doctor Page
# ---------------------------------------------------------------------------


async def step_collect_candidates(ctx: CrawlContext) -> list:
    """Collect and deduplicate candidate URLs for doctor page discovery.

    Returns list of (url, source_label) tuples.
    """
    log(f"#{ctx.hospital_no} Looking for doctor page")
    candidate_urls = []

    # Reveal hidden submenus via hover
    try:
        await ctx.page.evaluate(JS_REVEAL_SUBMENUS)
        await ctx.page.wait_for_timeout(500)
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
            log(f"#{ctx.hospital_no} Found {len(doctor_links)} "
                f"doctor menu link(s)")
        else:
            log(f"#{ctx.hospital_no} No doctor menu found")
    except Exception as e:
        log(f"#{ctx.hospital_no} Doctor menu search error: "
            f"{str(e)[:100]}")

    # Step 5b-1: Navigate to intro/about pages, scan for doctor sub-links
    if True:
        try:
            intro_links = await ctx.page.evaluate(JS_FIND_INTRO_LINKS)
            for link in (intro_links or []):
                log(f"#{ctx.hospital_no} Scanning intro page: "
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
                                log(f"#{ctx.hospital_no} Sub-page found "
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
            log(f"#{ctx.hospital_no} Intro page scan error: "
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

    log(f"#{ctx.hospital_no} Collected {len(unique_candidates)} "
        f"candidate URLs:")
    for i, (c_url, source) in enumerate(unique_candidates):
        log(f"#{ctx.hospital_no}   [{i + 1}] {source} -> {c_url}")

    return unique_candidates


# ---------------------------------------------------------------------------
# Step 6: Extract Doctor Info (sub-function: AI navigation)
# ---------------------------------------------------------------------------


async def _try_ai_navigation(
    ctx: CrawlContext, ocr_state: OcrState, seen_candidate_urls: set,
) -> None:
    """Phase 2: AI-assisted navigation discovery using Gemini."""
    log(f"#{ctx.hospital_no} Phase 2: AI navigation discovery from main page")
    try:
        await ctx.page.goto(
            ctx.url, wait_until="domcontentloaded", timeout=15000,
        )
        await ctx.page.wait_for_timeout(2000)

        ts_nav = int(time.time())
        nav_path = f"/tmp/clinic_nav_{ctx.hospital_no}_{ts_nav}.jpg"
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
            ["gemini", "-p", nav_prompt,
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
                        ctx.result["doctors"].append({
                            "name": name, "name_english": "",
                            "role": doc.get("role", "specialist"),
                            "photo_url": "",
                            "education": doc.get("education", []),
                            "career": doc.get("career", []),
                            "credentials": doc.get("credentials", []),
                            "branch": "", "branches": [],
                            "extraction_source": "ai_nav",
                            "ocr_source": True,
                        })

                if ctx.result["doctors"]:
                    ctx.doctor_page_found = True
                    log(f"#{ctx.hospital_no} AI found "
                        f"{len(ctx.result['doctors'])} doctors on "
                        f"main page")

                if not ctx.result["doctors"]:
                    ai_paths = nav_data.get("suggested_paths", [])
                    log(f"#{ctx.hospital_no} AI suggested "
                        f"{len(ai_paths)} paths: {ai_paths}")

                    for ai_path in ai_paths[:3]:
                        try:
                            ai_url = urljoin(
                                ctx.base_url + "/", ai_path,
                            )
                            if ai_url.rstrip("/") in seen_candidate_urls:
                                continue

                            log(f"#{ctx.hospital_no} Trying AI "
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
                                        f"#{ctx.hospital_no} AI path "
                                        f"DOM: {len(valid_doctors)} "
                                        f"valid / {len(doctors)} total",
                                    )
                                    break

                            ts_ai = int(time.time())
                            ai_ss = (
                                f"/tmp/clinic_ai_"
                                f"{ctx.hospital_no}_{ts_ai}.jpg"
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
                                    f"#{ctx.hospital_no} AI path OCR: "
                                    f"{len(ctx.result['doctors'])} "
                                    f"doctors",
                                )
                                break
                        except Exception as e:
                            log(f"#{ctx.hospital_no} AI path error: "
                                f"{str(e)[:100]}")
                            continue

    except subprocess.TimeoutExpired:
        log(f"#{ctx.hospital_no} AI navigation timeout")
    except Exception as e:
        log(f"#{ctx.hospital_no} AI navigation error: {str(e)[:100]}")


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

    try:
        for cand_idx, (cand_url, cand_source) in enumerate(candidates):
            if ctx.result["doctors"]:
                break

            log(f"#{ctx.hospital_no} Trying candidate "
                f"{cand_idx + 1}/{len(candidates)}: {cand_source}")

            # Skip javascript: URLs (can't navigate to them)
            if cand_url.startswith("javascript:"):
                log(f"#{ctx.hospital_no} Skipping javascript: URL")
                continue

            # Navigate to candidate
            try:
                await ctx.page.goto(
                    cand_url, wait_until="domcontentloaded", timeout=15000,
                )
                await ctx.page.wait_for_timeout(1500)
            except Exception as e:
                log(f"#{ctx.hospital_no} Navigation failed for "
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
                        log(f"#{ctx.hospital_no} Clicked tab: {tab_text}")
                    except Exception:
                        pass
            except Exception:
                pass

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
                            ctx.result["doctors"] = valid_doctors
                            ctx.doctor_page_found = True
                            log(f"#{ctx.hospital_no} DOM: "
                                f"{len(valid_doctors)} valid / "
                                f"{len(doctors)} total from "
                                f"{cand_source}")
                            break
                        else:
                            log(f"#{ctx.hospital_no} DOM: "
                                f"{len(doctors)} entries but 0 valid "
                                f"names from {cand_source}, "
                                f"falling back to OCR")
                            need_ocr = True
                    else:
                        log(f"#{ctx.hospital_no} DOM: 0 doctors "
                            f"from {cand_source}")
                        need_ocr = True
                else:
                    log(f"#{ctx.hospital_no} Image-based page: "
                        f"{cand_source}")

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
                        f"{ctx.hospital_no}_{ts}.jpg"
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
                        log(f"#{ctx.hospital_no} OCR Tier B on "
                            f"{cand_source}")
                        prompt_b = OCR_PROMPT_TEMPLATE.replace(
                            "{path}", fullpage_path,
                        )
                        doctors_raw = run_gemini_ocr(
                            prompt_b, fullpage_path,
                        )
                        added = append_ocr_doctors(
                            doctors_raw, ocr_state.seen_names,
                            ctx.result["doctors"],
                        )
                        if ctx.result["doctors"]:
                            ctx.doctor_page_found = True
                            log(f"#{ctx.hospital_no} OCR: {added} "
                                f"doctors from {cand_source}")
                            break
                        else:
                            log(f"#{ctx.hospital_no} OCR: 0 doctors "
                                f"from {cand_source}")
                    except subprocess.TimeoutExpired:
                        log(f"#{ctx.hospital_no} OCR timeout on "
                            f"{cand_source}, trying next candidate")
                    except FileNotFoundError:
                        log(f"#{ctx.hospital_no} Gemini CLI "
                            f"not installed")
                        break

            except Exception as e:
                log(f"#{ctx.hospital_no} Extraction error on "
                    f"{cand_source}: {str(e)[:100]}")

        # After ALL candidates exhausted - final OCR fallback
        if not ctx.result["doctors"] and ocr_state.last_screenshot_path:
            log(f"#{ctx.hospital_no} All {len(candidates)} candidates "
                f"returned 0. Final OCR attempt.")

            # Tier B retry on last screenshot
            try:
                log(f"#{ctx.hospital_no} OCR Tier B retry on last page")
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
                            f"{ctx.hospital_no}"
                            f"_{int(time.time())}_{i}.jpg"
                        )
                        await ctx.page.screenshot(
                            path=chunk_path, full_page=False,
                            type="jpeg", quality=85,
                        )
                        chunk_paths.append(chunk_path)
                        if len(chunk_paths) >= 8:
                            break
                    log(f"#{ctx.hospital_no} OCR Tier C: "
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
                log(f"#{ctx.hospital_no} Final OCR: "
                    f"{len(ctx.result['doctors'])} doctors found")

        # Phase 2: AI-assisted navigation discovery
        if not ctx.result["doctors"]:
            seen_candidate_urls = {
                u.rstrip("/") for u, _ in candidates
            }
            await _try_ai_navigation(
                ctx, ocr_state, seen_candidate_urls,
            )

        # Save screenshot if all methods exhausted
        if not ctx.result["doctors"] and ocr_state.last_screenshot_path:
            save_dir = os.path.join(
                os.path.dirname(
                    os.path.dirname(
                        os.path.dirname(
                            os.path.dirname(os.path.abspath(__file__))
                        )
                    )
                ),
                "data", "clinic-results", "screenshots",
            )
            os.makedirs(save_dir, exist_ok=True)
            save_path = os.path.join(
                save_dir, f"{ctx.hospital_no}_doctors.jpg",
            )
            shutil.copy2(ocr_state.last_screenshot_path, save_path)
            log(f"#{ctx.hospital_no} All methods exhausted. "
                f"Screenshot saved: {save_path}")
            ctx.result["errors"].append({
                "type": "all_methods_exhausted",
                "message": (
                    f"Rule-based ({len(candidates)} candidates) + "
                    f"AI navigation all failed. "
                    f"Screenshot: {save_path}"
                ),
                "step": "doctor_extract", "retryable": True,
            })

        log(f"#{ctx.hospital_no} Doctor extraction complete: "
            f"{len(ctx.result['doctors'])} doctors")

    except Exception as e:
        ctx.result["errors"].append({
            "type": "extraction", "message": str(e)[:200],
            "step": "doctor_extract", "retryable": True,
        })
    finally:
        for sp in ocr_state.temp_screenshots:
            try:
                os.remove(sp)
            except OSError:
                pass


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

    hospital_no = result["hospital_no"]
    log(f"#{hospital_no} Saving results (status={result['status']}, "
        f"channels={len(result['social_channels'])}, "
        f"doctors={len(result['doctors'])})")
    try:
        save_result(db_path, result)
        log(f"#{hospital_no} Saved to {db_path}")
    except Exception as e:
        result["errors"].append({
            "type": "storage_error", "message": str(e)[:200],
            "step": "save", "retryable": True,
        })
        log(f"#{hospital_no} Storage error: {e}")
