#!/usr/bin/env python3
"""Standalone single-hospital crawler with its own isolated browser.

Each invocation launches a headless Chromium browser, performs the full crawl
workflow, saves results to SQLite, and exits. Safe for parallel execution.

Dependencies: playwright (pip install playwright && python -m playwright install chromium)

Usage:
    python3 crawl_single.py --no 123 --name "고은미인의원" --url "https://example.com"
    python3 crawl_single.py --no 123 --name "병원" --url "https://..." --db hospitals.db --timeout 60
"""

import argparse
import asyncio
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import time
from pathlib import Path
from typing import Optional
from urllib.parse import urlparse, urljoin, parse_qs, urlencode, urlunparse

# Add parent dir to path for storage_manager import
sys.path.insert(0, str(Path(__file__).parent))
from storage_manager import save_result, export_unified_csv, DB_DEFAULT

CSV_SOURCE = "data/clinic-results/skin_clinics.csv"
CSV_UNIFIED_OUTPUT = "data/clinic-results/exports/clinic_results.csv"

# ---------------------------------------------------------------------------
# Platform URL patterns for social channel detection
# ---------------------------------------------------------------------------
PLATFORM_PATTERNS = {
    "KakaoTalk": [
        r"pf\.kakao\.com/", r"open\.kakao\.com/o/",
        r"talk\.kakao\.com/", r"kakao\.com/channel/",
    ],
    "NaverTalk": [r"talk\.naver\.com/"],
    "NaverShortlink": [r"naver\.me/"],
    "Line": [r"line\.me/", r"lin\.ee/"],
    "WeChat": [r"u\.wechat\.com/", r"weixin\.qq\.com/"],
    "WhatsApp": [r"wa\.me/", r"api\.whatsapp\.com/"],
    "Telegram": [r"t\.me/[^/]+$"],
    "FacebookMessenger": [r"m\.me/"],
    "NaverBooking": [r"booking\.naver\.com/"],
    "NaverMap": [r"map\.naver\.com/", r"m\.place\.naver\.com/"],
    "Instagram": [r"instagram\.com/"],
    "YouTube": [r"youtube\.com/", r"youtu\.be/"],
    "NaverBlog": [r"blog\.naver\.com/"],
    "NaverCafe": [r"cafe\.naver\.com/"],
    "Facebook": [r"facebook\.com/(?!.*messenger)"],
}

PHONE_RE = re.compile(
    r"(?:0\d{1,2})[-.\s]?\d{3,4}[-.\s]?\d{4}|\+82[-.\s]?\d{1,2}[-.\s]?\d{3,4}[-.\s]?\d{4}"
)

TRACKING_PARAMS = {"utm_source", "utm_medium", "utm_campaign", "utm_term",
                   "utm_content", "ref", "fbclid", "gclid", "igshid"}

# Doctor menu labels
DOCTOR_PRIMARY = [
    "의료진", "의료진 소개", "의료진소개", "원장 소개", "원장소개",
    "전문의 소개", "전문의소개", "DOCTOR", "Doctor", "Our Doctors", "Medical Staff",
]
DOCTOR_SECONDARY = [
    "원장님", "대표원장", "의료팀", "진료진", "진료 안내",
    "클리닉 소개", "Staff", "Team", "About Us",
    "병원소개", "병원 소개", "About Umi", "About TheHill",
]
DOCTOR_SUBMENU_PARENTS = [
    "병원 소개", "병원소개", "클리닉 소개", "소개", "병원 안내", "클리닉 안내",
    "About", "About Us", "병원소개/위치",
]
# Regex pattern: "{hospital_name_fragment} 소개" as submenu parent (e.g. "시아 소개")
_SUBMENU_PARENT_INTRO_RE = re.compile(r".{1,10}\s*소개$")

DOCTOR_ROLES_KEEP = {"원장", "대표원장", "부원장", "전문의", "의사", "레지던트", "인턴"}
DOCTOR_ROLES_EXCLUDE = {"간호사", "간호조무사", "피부관리사", "상담사", "코디네이터", "스텝", "직원"}

# Korean name validation - top ~60 surnames covering 99%+ of population
KOREAN_SURNAMES = set("김이박최정강조윤장임한오서신권황안송류전홍고문양손배백허유남노하곡성차주우방공민변탁도진지엄채원천구현은봉추위석선설마길연")
# Common verb/adjective endings that get misidentified as given names
_NON_NAME_SUFFIXES = {
    "싶은", "있는", "없는", "않는", "되는", "하는", "같은", "때문", "부터",
    "에서", "으로", "까지", "에게", "한다", "된다", "니다", "입니", "세요",
    "해서", "해야", "라고", "아서", "어서", "이라", "라는", "하고", "지만",
}
_NON_NAME_WORDS = {"대표원", "원대표", "부대표", "병원장"}
# Title/role suffixes that are NOT given names (e.g. 정대표 = 정 + 대표)
_NON_NAME_GIVEN = {"대표", "원장", "부장", "과장", "실장", "팀장", "소개", "안내"}


def _is_plausible_korean_name(name: str) -> bool:
    """Check if a string is plausibly a Korean person's name."""
    if not name or len(name) < 2 or len(name) > 4:
        return False
    # All characters should be Korean syllables (가-힣)
    if not all('\uac00' <= c <= '\ud7a3' for c in name):
        return False
    # First character should be a known surname
    if name[0] not in KOREAN_SURNAMES:
        return False
    # Exclude common non-name patterns
    if name in _NON_NAME_WORDS:
        return False
    if name[1:] in _NON_NAME_SUFFIXES:
        return False
    if name[1:] in _NON_NAME_GIVEN:
        return False
    return True

ROLE_RE = re.compile(r"^(.+?)\s+(원장|대표원장|부원장|전문의|의사|레지던트|인턴)$")

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def classify_url(url: str) -> Optional[str]:
    """Classify a URL into a social platform name."""
    if not url:
        return None
    # Exclude YouTube individual video URLs (not channel-level social links)
    if re.search(r"youtube\.com/(embed|watch|shorts)[\?/]", url, re.IGNORECASE):
        return None
    if re.search(r"youtu\.be/", url, re.IGNORECASE):
        return None
    for platform, patterns in PLATFORM_PATTERNS.items():
        for pat in patterns:
            if re.search(pat, url, re.IGNORECASE):
                return platform
    if url.startswith("tel:"):
        return "Phone"
    if url.startswith("sms:"):
        return "SMS"
    return None


def strip_tracking(url: str) -> str:
    """Remove tracking parameters from URL."""
    try:
        parsed = urlparse(url)
        params = parse_qs(parsed.query)
        clean = {k: v for k, v in params.items() if k not in TRACKING_PARAMS}
        return urlunparse(parsed._replace(query=urlencode(clean, doseq=True)))
    except Exception:
        return url


def normalize_url(url: str) -> str:
    """Normalize URL for dedup: strip tracking, lowercase host, strip trailing slash, normalize phone."""
    if url.startswith("tel:") or url.startswith("sms:"):
        prefix = url[:4]
        return prefix + re.sub(r"[-.\s()+]", "", url[4:])
    url = strip_tracking(url)
    try:
        parsed = urlparse(url)
        host = parsed.netloc.lower()
        path = parsed.path.rstrip("/") or "/"
        # Strip YouTube channel suffixes for dedup (/videos, /featured, /about)
        if "youtube.com" in host:
            path = re.sub(r"/(videos|featured|about|playlists|community|channels)$", "", path)
        return urlunparse(parsed._replace(netloc=host, path=path))
    except Exception:
        return url


def log(msg: str) -> None:
    """Log to stderr (stdout reserved for JSON output)."""
    print(f"[crawl] {msg}", file=sys.stderr, flush=True)


# ---------------------------------------------------------------------------
# JavaScript snippets for page.evaluate()
# ---------------------------------------------------------------------------

JS_SOCIAL_EXTRACT = """
() => {
    const results = [];
    const seen = new Set();

    function normalizeUrl(u) {
        if (u.startsWith('tel:') || u.startsWith('sms:')) {
            return u.substring(0, 4) + u.substring(4).replace(/[-.\s()+]/g, '');
        }
        try {
            const obj = new URL(u);
            obj.hostname = obj.hostname.toLowerCase();
            if (obj.pathname.length > 1 && obj.pathname.endsWith('/'))
                obj.pathname = obj.pathname.slice(0, -1);
            return obj.toString();
        } catch { return u; }
    }

    function addResult(platform, url, method) {
        if (!url) return;
        const norm = normalizeUrl(url);
        if (seen.has(norm)) return;
        seen.add(norm);
        results.push({platform, url: norm, method});
    }

    // Platform detection regex map
    const platformPatterns = {
        KakaoTalk: /pf\\.kakao\\.com|open\\.kakao\\.com\\/o|talk\\.kakao\\.com|kakao\\.com\\/channel/i,
        NaverTalk: /talk\\.naver\\.com\\//i,
        NaverShortlink: /naver\\.me\\//i,
        Line: /line\\.me\\/|lin\\.ee\\//i,
        WeChat: /u\\.wechat\\.com|weixin\\.qq\\.com/i,
        WhatsApp: /wa\\.me\\/|api\\.whatsapp\\.com/i,
        Telegram: /t\\.me\\/[^/]+$/i,
        FacebookMessenger: /m\\.me\\//i,
        NaverBooking: /booking\\.naver\\.com/i,
        Instagram: /instagram\\.com\\//i,
        YouTube: /youtube\\.com\\/|youtu\\.be\\//i,
        NaverBlog: /blog\\.naver\\.com\\//i,
        NaverCafe: /cafe\\.naver\\.com\\//i,
        Facebook: /facebook\\.com\\//i,
    };

    function classifyUrl(url) {
        if (!url) return null;
        if (url.startsWith('tel:')) return 'Phone';
        if (url.startsWith('sms:')) return 'SMS';
        // Exclude YouTube individual video URLs (not channel-level links)
        if (/youtube\\.com\\/(embed|watch|shorts)[\\/\\?]/i.test(url)) return null;
        if (/youtu\\.be\\//i.test(url)) return null;
        for (const [platform, re] of Object.entries(platformPatterns)) {
            if (re.test(url)) return platform;
        }
        return null;
    }

    // Pass 1: Static DOM - scan all <a href>
    document.querySelectorAll('a[href]').forEach(a => {
        const href = a.href || a.getAttribute('href') || '';
        const platform = classifyUrl(href);
        if (platform) {
            // Honeypot filter
            const style = getComputedStyle(a);
            if (style.display === 'none' || style.visibility === 'hidden' ||
                style.opacity === '0' || a.offsetHeight === 0) return;
            addResult(platform, href, 'dom_static');
        }
    });

    // Pass 1: tel: and sms: links
    document.querySelectorAll('a[href^="tel:"], a[href^="sms:"]').forEach(a => {
        const href = a.getAttribute('href');
        const platform = href.startsWith('tel:') ? 'Phone' : 'SMS';
        addResult(platform, href, 'phone_text');
    });

    // Pass 1.5: iframe detection
    document.querySelectorAll('iframe').forEach(f => {
        const src = f.src || f.getAttribute('src') || '';
        const platform = classifyUrl(src);
        if (platform) addResult(platform, src, 'iframe');
    });

    // Pass 1.5: Google Maps iframe - phone from surrounding context
    document.querySelectorAll('iframe[src*="google.com/maps"], iframe[src*="maps.google"]').forEach(f => {
        const parent = f.closest('section, div, article') || f.parentElement;
        const text = parent?.innerText || '';
        const phones = text.match(/(?:0\\d{1,2})[-.\s]?\\d{3,4}[-.\s]?\\d{4}/g);
        if (phones) phones.forEach(p => addResult('Phone', 'tel:' + p.replace(/[-.\s]/g,''), 'maps_embed'));
    });

    // Pass 1.75: Structured data (JSON-LD)
    document.querySelectorAll('script[type="application/ld+json"]').forEach(s => {
        try {
            const data = JSON.parse(s.textContent);
            const items = Array.isArray(data) ? data : [data];
            items.forEach(item => {
                if (item.sameAs) {
                    const links = Array.isArray(item.sameAs) ? item.sameAs : [item.sameAs];
                    links.forEach(url => {
                        const p = classifyUrl(url);
                        if (p) addResult(p, url, 'structured_data');
                    });
                }
                if (item.contactPoint?.telephone) {
                    addResult('Phone', 'tel:' + item.contactPoint.telephone.replace(/[-.\s]/g,''), 'structured_data');
                }
            });
        } catch(e) {}
    });

    // Pass 2: onclick handlers with window.open
    document.querySelectorAll('[onclick]').forEach(el => {
        const onclick = el.getAttribute('onclick') || '';
        const match = onclick.match(/window\\.open\\(['"]([^'"]+)['"]/);
        if (match) {
            const p = classifyUrl(match[1]);
            if (p) addResult(p, match[1], 'dom_dynamic');
        }
    });

    // Pass 2: Widget SDK detection
    const sdks = [];
    if (window.Kakao?.Channel) sdks.push({name: 'KakaoTalk', detected: true});
    if (window.ChannelIO) sdks.push({name: 'ChannelIO', detected: true});
    if (window.tawk_chat) sdks.push({name: 'TawkTo', detected: true});
    if (window.Crisp?.chat) sdks.push({name: 'Crisp', detected: true});
    if (window.zE) sdks.push({name: 'Zendesk', detected: true});
    if (window.Intercom) sdks.push({name: 'Intercom', detected: true});
    if (window.drift) sdks.push({name: 'Drift', detected: true});
    if (window.HubSpotConversations) sdks.push({name: 'HubSpot', detected: true});
    if (window.fcWidget) sdks.push({name: 'Freshchat', detected: true});

    sdks.forEach(sdk => {
        addResult(sdk.name, 'widget:' + sdk.name, 'widget_sdk');
    });

    // Pass 2: Shadow DOM traversal
    document.querySelectorAll('*').forEach(el => {
        if (el.shadowRoot) {
            el.shadowRoot.querySelectorAll('a[href]').forEach(a => {
                const p = classifyUrl(a.href);
                if (p) addResult(p, a.href, 'shadow_dom');
            });
        }
    });

    // Pass 3: WeChat QR image detection
    document.querySelectorAll('img').forEach(img => {
        const src = img.src || img.getAttribute('data-src') || '';
        if (!src) return;
        const alt = (img.alt || '').toLowerCase();
        const cls = (img.className || '').toLowerCase();
        const parentText = (img.parentElement?.textContent || '').toLowerCase();
        if (/wechat|weixin|微信|위챗/.test(alt + ' ' + cls + ' ' + parentText)) {
            addResult('WeChat', src, 'qr_image');
        }
    });

    // Korean phone numbers in page text (Pass 4)
    const bodyText = document.body.innerText || '';
    const phoneMatches = bodyText.match(/(?:0\\d{1,2})[-.\s]?\\d{3,4}[-.\s]?\\d{4}/g);
    if (phoneMatches) {
        // Only add first 3 unique phones (avoid noise)
        const phoneSet = new Set();
        phoneMatches.forEach(p => {
            const normalized = p.replace(/[-.\s]/g, '');
            if (!phoneSet.has(normalized) && phoneSet.size < 3) {
                phoneSet.add(normalized);
                addResult('Phone', 'tel:' + normalized, 'phone_text');
            }
        });
    }

    return results;
}
"""

JS_WINDOW_OPEN_INTERCEPT = """
() => {
    const captured = [];
    const orig = window.open;
    window.open = function(url) { if (url) captured.push(String(url)); return null; };

    // Intercept link navigation to prevent page leaving
    const handler = (e) => { e.preventDefault(); e.stopPropagation(); };
    document.addEventListener('click', handler, true);

    document.querySelectorAll('button, [role="button"]').forEach(el => {
        const text = el.textContent || '';
        if (/상담|문의|채팅|톡|consultation|chat/i.test(text)) {
            try { el.click(); } catch(e) {}
        }
    });

    document.removeEventListener('click', handler, true);
    window.open = orig;
    return captured;
}
"""

JS_DISMISS_POPUPS = """
() => {
    let dismissed = 0;
    const popupSelectors = [
        '.popup', '.modal', '.layer-popup', '.pop-layer',
        '[class*="popup"]', '[class*="modal"]', '[role="dialog"]'
    ];
    const closeSelectors = [
        'button.close', '.popup-close', '.modal-close', '.btn-close',
        '[aria-label="닫기"]', '[aria-label="Close"]',
        '.popup .close', '.modal .close',
        '.layer-close', '.pop-close', '.closeBtn', '.close-btn'
    ];
    const closeTexts = ['닫기', '확인', '창닫기', '팝업닫기', 'CLOSE', 'Close', 'OK'];

    // Check for visible popups
    for (const sel of popupSelectors) {
        document.querySelectorAll(sel).forEach(popup => {
            const style = getComputedStyle(popup);
            if (style.display === 'none' || style.visibility === 'hidden' || style.opacity === '0') return;

            // Strategy 1: X button
            for (const closeSel of closeSelectors) {
                const btn = popup.querySelector(closeSel);
                if (btn) { btn.click(); dismissed++; return; }
            }

            // Strategy 2: Text button
            popup.querySelectorAll('button, a, span').forEach(el => {
                if (closeTexts.includes(el.textContent.trim())) {
                    el.click(); dismissed++;
                }
            });
        });
    }

    // Strategy 3: Checkbox then close
    document.querySelectorAll('input[type="checkbox"]').forEach(cb => {
        const label = cb.parentElement?.textContent || '';
        if (/오늘.*열지|오늘.*보지|다시.*보지|하루동안|Don't show/i.test(label)) {
            cb.checked = true;
            cb.dispatchEvent(new Event('change', {bubbles: true}));
        }
    });

    // Strategy 4: Overlay click
    ['.modal-backdrop', '.popup-overlay', '.popup-bg', '.dim', '.dimmed', '.overlay'].forEach(sel => {
        document.querySelectorAll(sel).forEach(el => {
            const style = getComputedStyle(el);
            if (style.display !== 'none') { el.click(); dismissed++; }
        });
    });

    // Cookie suppression
    document.cookie = "popup_close=done; path=/; max-age=86400";
    document.cookie = "todayClose=Y; path=/; max-age=86400";
    document.cookie = "popup_today=done; path=/; max-age=86400";

    return dismissed;
}
"""

JS_SPA_WAIT = """
() => new Promise((resolve) => {
    let timer;
    const observer = new MutationObserver(() => {
        clearTimeout(timer);
        timer = setTimeout(() => { observer.disconnect(); resolve('stable'); }, 2000);
    });
    observer.observe(document.body, { childList: true, subtree: true });
    setTimeout(() => { observer.disconnect(); resolve('timeout'); }, 10000);
    timer = setTimeout(() => { observer.disconnect(); resolve('idle'); }, 2000);
})
"""

JS_DETECT_CMS = """
() => {
    if (document.querySelector('meta[name="generator"][content*="modoo"]') || document.querySelector('script[src*="modoo"]')) return 'modoo';
    if (document.querySelector('meta[name="generator"][content*="imweb"]') || document.querySelector('script[src*="imweb"]')) return 'imweb';
    if (document.querySelector('meta[name="generator"][content*="cafe24"]') || document.querySelector('script[src*="cafe24"]')) return 'cafe24';
    if (document.querySelector('meta[name="generator"][content*="WordPress"]')) return 'wordpress';
    if (document.querySelector('meta[name="generator"][content*="Wix"]')) return 'wix';
    if (document.querySelector('script[src*="gnuboard"]') || document.querySelector('meta[name="generator"][content*="gnu"]')) return 'gnuboard';
    return '';
}
"""

JS_CHECK_ENCODING = """
() => {
    const text = document.body.innerText || '';
    const garbledCount = (text.match(/[\\ufffd]/g) || []).length;
    const ratio = garbledCount / Math.max(text.length, 1);
    return { charset: document.characterSet, garbledRatio: ratio, textLength: text.length };
}
"""

JS_FIND_DOCTOR_MENU = """
([primaryLabels, secondaryLabels, submenuParents]) => {
    const allLinks = Array.from(document.querySelectorAll('nav a, header a, .menu a, .gnb a, .lnb a, [class*="nav"] a, [class*="menu"] a, a'));
    const results = [];
    const doctorUrlRe = /\\/doctor|\\/staff|\\/team|\\/의료진|\\/원장|\\/전문의|about.*(?:doctor|team|staff)/i;
    const genericUrlRe = /^\\/(?:about|introduce|clinic|소개|병원)(?:[#?/]|$)/i;

    for (const a of allLinks) {
        const text = (a.textContent || '').trim();
        const href = a.href || a.getAttribute('href') || '';
        if (!text || text.length > 30) continue;

        const visible = a.offsetParent !== null && a.offsetWidth > 0;
        let matched = false;

        // Check primary labels
        for (const label of primaryLabels) {
            if (text === label || text.includes(label)) {
                results.push({text, href, priority: 1, visible, element: a.outerHTML.substring(0, 200)});
                matched = true; break;
            }
        }
        if (matched) continue;
        // Check secondary labels
        for (const label of secondaryLabels) {
            if (text === label || text.includes(label)) {
                results.push({text, href, priority: 2, visible, element: a.outerHTML.substring(0, 200)});
                matched = true; break;
            }
        }
        if (matched) continue;
        // Check URL patterns
        if (doctorUrlRe.test(href)) {
            results.push({text, href, priority: 1, visible, element: a.outerHTML.substring(0, 200)});
        }
    }

    // Submenu child scanning: find doctor links inside dropdown parents
    const menuParentSels = ['nav > ul > li', '.gnb > li', '.menu > li', '[class*="nav"] > ul > li', 'header li'];
    for (const sel of menuParentSels) {
        document.querySelectorAll(sel).forEach(parent => {
            const parentLink = parent.querySelector(':scope > a');
            const parentText = (parentLink?.textContent || '').trim();
            const isIntroParent = /.\s*소개$/.test(parentText);
            if (!isIntroParent && !submenuParents.some(label => parentText.includes(label))) return;
            parent.querySelectorAll('ul a, .sub a, .submenu a, .depth2 a, .snb a, a').forEach(child => {
                const childText = (child.textContent || '').trim();
                const childHref = child.href || child.getAttribute('href') || '';
                for (const label of primaryLabels) {
                    if (childText === label || childText.includes(label)) {
                        results.push({
                            text: childText, href: childHref, priority: 0,
                            visible: child.offsetParent !== null,
                            element: child.outerHTML.substring(0, 200),
                            parentMenu: parentText,
                        });
                        return;
                    }
                }
                // Also check secondary labels under parent menus
                for (const label of secondaryLabels) {
                    if (childText === label || childText.includes(label)) {
                        results.push({
                            text: childText, href: childHref, priority: 1,
                            visible: child.offsetParent !== null,
                            element: child.outerHTML.substring(0, 200),
                            parentMenu: parentText,
                        });
                        return;
                    }
                }
                // Check if child URL matches doctor patterns
                if (doctorUrlRe.test(childHref)) {
                    results.push({
                        text: childText, href: childHref, priority: 1,
                        visible: child.offsetParent !== null,
                        element: child.outerHTML.substring(0, 200),
                        parentMenu: parentText,
                    });
                }
            });
        });
    }

    // Boost specific doctor URLs, demote generic parent URLs
    for (const r of results) {
        try {
            const path = new URL(r.href).pathname;
            if (doctorUrlRe.test(path)) r.priority = Math.min(r.priority, 0);
            else if (genericUrlRe.test(path) && r.priority > 0) r.priority = 3;
        } catch {}
    }

    // Sort: priority first, then visible links
    const unique = [];
    const seenHrefs = new Set();
    results.sort((a, b) => {
        if (a.priority !== b.priority) return a.priority - b.priority;
        if (a.visible !== b.visible) return a.visible ? -1 : 1;
        return 0;
    });
    for (const r of results) {
        if (!seenHrefs.has(r.href)) {
            seenHrefs.add(r.href);
            unique.push(r);
        }
    }
    return unique.slice(0, 5);
}
"""

JS_EXTRACT_DOCTORS = """
() => {
    const rolePattern = /원장|대표원장|부원장|전문의|의사|레지던트|인턴/;
    const excludeRoles = ['간호사', '간호조무사', '피부관리사', '상담사', '코디네이터', '스텝', '직원'];

    // ─── Shared name-validation filters ───
    const nonNameWords = [
        '병원', '의원', '클리닉', '외과', '내과', '의과', '센터',
        '학회', '학교', '대학', '약국', '닥터', '학과', '피부',
        '점', '위원', '회원', '전문가', '구매', '상식', '활동',
        '협력', '총괄', '증서', '인후과', '의료', '연구',
        '서울', '인터', '채용', '공지', '조회', '철산',
        '미용', '홍보', '오늘', '강사', '소개', '마사',
    ];
    const surnames = new Set(
        '김이박최정강조윤장임한오서신권황안송류전홍유고문양손배백허남심노하곽성차주우구민진지엄채원천방공현함변추도소석선설마길연위표명기반왕금옥육인맹제모탁국여어은편빈예봉경태피감복'.split('')
    );
    const nonNameExact = new Set([
        '대표', '멤버', '보유', '대한', '의학', '교육', '운영', '학력',
        '소개', '경력', '인사', '선생', '안내', '예약', '진료',
        '진단', '보험', '도입', '경험', '인증', '소속',
        // Common non-name words that pass surname check
        '원장', '전담', '기기', '최신', '어떤', '최애', '주요',
        '안과', '여의사', '주름', '노하우', '원소개', '이퓨어',
        '우아성', '박훤함', '마인피', '하나이',
        // Location names (chain hospital branches)
        '강남', '천호', '하남', '구리', '강서', '송파', '구로',
        '연신내', '왕십리',
    ]);

    function isPlausibleName(name) {
        if (!name || name.length < 2 || name.length > 3) return false;
        if (excludeRoles.some(r => name.includes(r))) return false;
        if (nonNameWords.some(s => name.includes(s))) return false;
        if (nonNameExact.has(name)) return false;
        if (!surnames.has(name[0])) return false;
        // Reject truncated words (e.g. "경희의" from "경희의료원", "연세대" from "연세대학교")
        if (name.length === 3 && /[의과에적대는여]$/.test(name)) return false;
        // Reject garbled role prefix (e.g. "원장유" from "원장 유동...")
        if (name.startsWith('원장') || name.startsWith('전문')) return false;
        return true;
    }

    // ─── Card extraction helper ───
    function extractFromCard(card, source, seen) {
        const nameEl = card.querySelector('.doctor-name, .staff-name, h3, h4, h2, .name, strong, b');
        let name = nameEl?.textContent?.trim() || '';
        if (!name || name.length < 2 || name.length > 20) return null;

        let role = 'specialist';
        // Forward: name + role (e.g. "김상우 대표원장")
        const fwd = name.match(/^(.+?)\\s*(원장|대표원장|부원장|전문의|의사|레지던트|인턴)$/);
        if (fwd) { name = fwd[1].trim(); role = fwd[2]; }
        // Reverse: role + name (e.g. "대표원장 김상우")
        if (role === 'specialist') {
            const rev = name.match(/^(대표원장|부원장|원장|전문의|의사)\\s+(.+)$/);
            if (rev) { role = rev[1]; name = rev[2].trim(); }
        }

        // Validate: must contain Korean chars; short Korean names must pass isPlausibleName
        const hasKorean = /[가-힣]/.test(name);
        if (!hasKorean) return null;
        if (name.length <= 3 && !isPlausibleName(name)) return null;

        const cardText = card.textContent || '';
        if (excludeRoles.some(r => cardText.includes(r) && !cardText.includes('원장') && !cardText.includes('전문의'))) return null;

        if (seen.has(name)) return null;
        seen.add(name);

        let photo = '';
        const img = card.querySelector('img');
        if (img) photo = img.src || img.getAttribute('data-src') || '';
        if (!photo) {
            const photoEl = card.querySelector('[class*="photo"], [class*="image"], [class*="avatar"], [class*="img"]');
            if (photoEl) {
                const bg = getComputedStyle(photoEl).backgroundImage;
                const bgMatch = bg?.match(/url\\(['"]?([^'"\\)]+)['"]?\\)/);
                if (bgMatch) photo = bgMatch[1];
            }
        }

        const lists = card.querySelectorAll('ul, ol, .career, .credentials, .history, [class*="career"], [class*="credential"]');
        const credentials = [], education = [], career = [];
        lists.forEach(list => {
            const items = list.querySelectorAll('li, p, span, dd');
            items.forEach(item => {
                const text = item.textContent.trim();
                if (!text || text.length > 100) return;
                if (/대학|학위|졸업|수료|학사|석사|박사|의학전문대/.test(text)) education.push(text);
                else if (/병원|클리닉|근무|전공의|수련|센터/.test(text)) career.push(text);
                else if (/정회원|학회|자격|인증|협회|전문의/.test(text)) credentials.push(text);
                else career.push(text);
            });
        });

        return { name, name_english: '', role, photo_url: photo, education, career, credentials, branch: '', branches: [], extraction_source: source, ocr_source: false };
    }

    // ─── Text context extraction helper ───
    function extractContext(name, allText) {
        const idx = allText.indexOf(name);
        const ctx = allText.substring(Math.max(0, idx - 100), Math.min(allText.length, idx + 800));
        const lines = ctx.split(/\\n/).map(l => l.trim()).filter(l => l.length > 3 && l.length < 100);
        const education = [], career = [], credentials = [];
        for (const line of lines) {
            if (/대학|학위|졸업|수료|학사|석사|박사|의학전문대/.test(line)) education.push(line.replace(/^[ㆍ·•\\-\\s]+/, ''));
            else if (/병원|클리닉|근무|전공의|수련|센터/.test(line)) career.push(line.replace(/^[ㆍ·•\\-\\s]+/, ''));
            else if (/정회원|학회|자격|인증|협회|전문의/.test(line)) credentials.push(line.replace(/^[ㆍ·•\\-\\s]+/, ''));
        }
        return { education, career, credentials };
    }

    // ═════════════════════════════════════════════════════
    //  Run ALL strategies independently, then merge
    // ═════════════════════════════════════════════════════

    // ── Strategy 1: Doctor-specific card selectors ──
    const s1 = [];
    {
        const seen1 = new Set();
        const cardSelectors = [
            '.doctor-card', '.doctor-item', '.staff-item', '.team-member',
            '.doctor-info', '.doctor-list > li', '.staff-list > li',
            '[class*="doctor"]', '[class*="staff"]',
        ];
        // Also try finding containers that HAVE a .doctor-name child
        if (document.querySelector('.doctor-name')) {
            const nameEls = document.querySelectorAll('.doctor-name');
            for (const el of nameEls) {
                const card = el.closest('div, section, article, li, td, tr') || el.parentElement;
                if (card) {
                    const doc = extractFromCard(card, 'dom', seen1);
                    if (doc) s1.push(doc);
                }
            }
        }
        for (const sel of cardSelectors) {
            const found = document.querySelectorAll(sel);
            if (found.length > 0 && found.length < 50) {
                for (const card of found) {
                    const doc = extractFromCard(card, 'dom', seen1);
                    if (doc) s1.push(doc);
                }
                break;
            }
        }
    }

    // ── Strategy 2: Generic containers with doctor-role filter ──
    const s2 = [];
    {
        const seen2 = new Set();
        const items = document.body.querySelectorAll(
            'li, article, section, .item, .card, .member, [class*="team"], [class*="profile"], [class*="intro"], div[class*="doctor"], div[class*="staff"]'
        );
        for (const card of items) {
            const text = card.textContent || '';
            if (text.length > 5000 || text.length < 4) continue;
            if (!rolePattern.test(text)) continue;
            const doc = extractFromCard(card, 'dom', seen2);
            if (doc && isPlausibleName(doc.name)) s2.push(doc);
        }
    }

    // ── Strategy 3: Text-based scan (forward + reverse patterns) ──
    const s3 = [];
    {
        const allText = document.body.innerText || '';
        const seen3 = new Set();
        const MAX = 20;

        // Pattern A: name + role (e.g. "김상우 대표원장")
        const nameRoleRe = /([가-힣]{2,3})\\s*(대표원장|부원장|원장|전문의|의사)/g;
        let m;
        while ((m = nameRoleRe.exec(allText)) !== null && s3.length < MAX) {
            const name = m[1].trim();
            const role = m[2];
            if (seen3.has(name) || !isPlausibleName(name)) continue;
            seen3.add(name);
            const ctx = extractContext(name, allText);
            s3.push({ name, name_english: '', role, photo_url: '', ...ctx, branch: '', branches: [], extraction_source: 'dom_text', ocr_source: false });
        }

        // Pattern B: role + name (e.g. "대표원장 김상우")
        const roleNameRe = /(대표원장|부원장|원장|전문의|의사)\\s+([가-힣]{2,3})/g;
        while ((m = roleNameRe.exec(allText)) !== null && s3.length < MAX) {
            const role = m[1];
            const name = m[2].trim();
            if (seen3.has(name) || !isPlausibleName(name)) continue;
            seen3.add(name);
            const ctx = extractContext(name, allText);
            s3.push({ name, name_english: '', role, photo_url: '', ...ctx, branch: '', branches: [], extraction_source: 'dom_text', ocr_source: false });
        }

        // Pattern C: spaced Korean name + role (e.g. "서 인 예 대표원장")
        const spacedNameRoleRe = /([가-힣])\\s([가-힣])\\s?([가-힣])?\\s*(대표원장|부원장|원장|전문의|의사)/g;
        while ((m = spacedNameRoleRe.exec(allText)) !== null && s3.length < MAX) {
            const name = (m[1] + m[2] + (m[3] || '')).trim();
            const role = m[4];
            if (seen3.has(name) || !isPlausibleName(name)) continue;
            seen3.add(name);
            const ctx = extractContext(m[0], allText);
            s3.push({ name, name_english: '', role, photo_url: '', ...ctx, branch: '', branches: [], extraction_source: 'dom_text', ocr_source: false });
        }
    }

    // ── Strategy 4: Heading-based scan (h1-h5, strong, b) ──
    const s4 = [];
    {
        const seen4 = new Set();
        const headings = document.querySelectorAll('h1, h2, h3, h4, h5, strong, b, .title, [class*="name"]');
        for (const el of headings) {
            const text = (el.textContent || '').trim();
            if (text.length < 2 || text.length > 4) continue;
            if (!isPlausibleName(text)) continue;
            const parent = el.closest('div, section, article, li, td') || el.parentElement;
            const context = (parent?.textContent || '').substring(0, 500);
            if (!rolePattern.test(context)) continue;
            if (seen4.has(text)) continue;
            seen4.add(text);
            let role = 'specialist';
            const roleMatch = context.match(/(대표원장|부원장|원장|전문의|의사)/);
            if (roleMatch) role = roleMatch[1];
            let photo = '';
            const img = parent?.querySelector('img');
            if (img) photo = img.src || img.getAttribute('data-src') || '';
            const allText4 = document.body.innerText || '';
            const ctx = extractContext(text, allText4);
            s4.push({ name: text, name_english: '', role, photo_url: photo, ...ctx, branch: '', branches: [], extraction_source: 'dom_heading', ocr_source: false });
        }
    }

    // ── Merge: deduplicate by name, combine best info ──
    const merged = new Map();
    function mergeDoc(doc) {
        if (merged.has(doc.name)) {
            const ex = merged.get(doc.name);
            if (!ex.photo_url && doc.photo_url) ex.photo_url = doc.photo_url;
            for (const e of (doc.education || [])) { if (!ex.education.includes(e)) ex.education.push(e); }
            for (const c of (doc.career || [])) { if (!ex.career.includes(c)) ex.career.push(c); }
            for (const c of (doc.credentials || [])) { if (!ex.credentials.includes(c)) ex.credentials.push(c); }
            if (ex.extraction_source === 'dom_text' && doc.extraction_source === 'dom') ex.extraction_source = 'dom';
        } else {
            merged.set(doc.name, { ...doc, education: [...(doc.education||[])], career: [...(doc.career||[])], credentials: [...(doc.credentials||[])] });
        }
    }

    // Priority order: S1 (best selectors) → S2 (generic) → S3 (text) → S4 (headings)
    for (const d of s1) mergeDoc(d);
    for (const d of s2) mergeDoc(d);
    for (const d of s3) mergeDoc(d);
    for (const d of s4) mergeDoc(d);

    return Array.from(merged.values());
}
"""

JS_CHECK_IMAGE_BASED = """
() => {
    // Count text nodes with doctor-related content
    // Use document.body to avoid querySelector picking wrong container
    // (e.g. first empty <article> when doctor info is in a later <article>)
    const walker = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT, null, false);
    const textNodes = [];
    while (walker.nextNode()) {
        const text = walker.currentNode.textContent.trim();
        if (text.length >= 2 && /원장|대표원장|부원장|전문의|의사|학력|경력|약력|자격|졸업|수료|대학원|대학교|정회원|학회|인턴|레지던트|수련|피부과/.test(text)) {
            textNodes.push(text);
        }
    }
    return textNodes.length < 2;
}
"""

JS_SCROLL_TRIGGER = """
async () => {
    window.scrollTo(0, document.body.scrollHeight / 2);
    window.dispatchEvent(new Event('scroll'));
    await new Promise(r => setTimeout(r, 2000));

    // Re-scan for position:fixed elements
    const fixed = [];
    document.querySelectorAll('*').forEach(el => {
        const style = getComputedStyle(el);
        if (style.position === 'fixed' || style.position === 'sticky') {
            el.querySelectorAll('a[href]').forEach(a => {
                fixed.push({href: a.href, text: a.textContent?.trim()});
            });
        }
    });
    return fixed;
}
"""

JS_GET_PAGE_TEXT_LENGTH = """
() => (document.body?.innerText || '').length
"""


# ---------------------------------------------------------------------------
# Main crawl function
# ---------------------------------------------------------------------------

async def crawl_hospital(hospital_no: int, name: str, url: str, db_path: str,
                         timeout: int = 45, headless: bool = True) -> dict:
    """Crawl a single hospital website with an isolated browser instance."""
    from playwright.async_api import async_playwright

    result = {
        "hospital_no": hospital_no,
        "name": name,
        "url": url,
        "final_url": "",
        "status": "success",
        "cms_platform": "",
        "schema_version": "2.0.0",
        "social_channels": [],
        "doctors": [],
        "errors": [],
        "doctor_page_exists": None,
    }

    async with async_playwright() as pw:
        browser = await pw.chromium.launch(headless=headless)
        context = await browser.new_context(
            viewport={"width": 1280, "height": 800},
            locale="ko-KR",
            user_agent=(
                "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/120.0.0.0 Safari/537.36"
            ),
            ignore_https_errors=True,
        )
        page = await context.new_page()
        page.set_default_timeout(timeout * 1000)
        page.set_default_navigation_timeout(timeout * 1000)

        try:
            # ---------------------------------------------------------------
            # Step 0: Pre-flight
            # ---------------------------------------------------------------
            parsed = urlparse(url)
            if parsed.scheme not in ("http", "https"):
                result["status"] = "failed"
                result["errors"].append({
                    "type": "invalid_url", "message": f"Invalid scheme: {parsed.scheme}",
                    "step": "preflight", "retryable": False,
                })
                await browser.close()
                return result

            base_url = f"{parsed.scheme}://{parsed.netloc}"
            log(f"#{hospital_no} Starting crawl: {url}")

            # robots.txt check - only block if User-agent: * disallows /
            try:
                robots_resp = await page.goto(f"{base_url}/robots.txt", wait_until="domcontentloaded", timeout=8000)
                if robots_resp and robots_resp.ok:
                    robots_text = await page.evaluate("() => document.body?.innerText || ''")
                    # Parse User-agent sections properly
                    current_agent = None
                    wildcard_disallowed = []
                    for line in robots_text.split("\n"):
                        line = line.strip()
                        if line.lower().startswith("user-agent:"):
                            current_agent = line.split(":", 1)[1].strip()
                        elif line.lower().startswith("disallow:") and current_agent == "*":
                            path = line.split(":", 1)[1].strip()
                            if path:
                                wildcard_disallowed.append(path)
                    if any(d == "/" for d in wildcard_disallowed) and not any(line.strip().lower().startswith("allow:") and line.split(":", 1)[1].strip() == "/" for line in robots_text.split("\n")):
                        result["status"] = "robots_blocked"
                        result["errors"].append({
                            "type": "robots_blocked", "message": "robots.txt disallows all paths",
                            "step": "preflight", "retryable": False,
                        })
                        log(f"#{hospital_no} robots.txt blocks all paths")
                        await browser.close()
                        return result
            except Exception:
                pass  # robots.txt failure is not blocking

            # ---------------------------------------------------------------
            # Step 1: Navigate and Resolve
            # ---------------------------------------------------------------
            log(f"#{hospital_no} Navigating to {url}")
            try:
                response = await page.goto(url, wait_until="domcontentloaded", timeout=timeout * 1000)
            except Exception as e:
                err_msg = str(e)
                result["status"] = "failed"
                if "timeout" in err_msg.lower():
                    result["errors"].append({"type": "timeout", "message": err_msg[:200], "step": "navigate", "retryable": True})
                elif "net::" in err_msg.lower():
                    result["errors"].append({"type": "network", "message": err_msg[:200], "step": "navigate", "retryable": True})
                else:
                    result["errors"].append({"type": "navigation", "message": err_msg[:200], "step": "navigate", "retryable": True})
                log(f"#{hospital_no} Navigation failed: {err_msg[:100]}")
                await browser.close()
                return result

            # Redirect detection
            try:
                final_url = await page.evaluate("() => window.location.href")
                if final_url and final_url != url:
                    result["final_url"] = final_url
                    log(f"#{hospital_no} Redirected to {final_url}")
            except Exception:
                pass

            # CMS detection
            try:
                cms = await page.evaluate(JS_DETECT_CMS)
                if cms:
                    result["cms_platform"] = cms
                    log(f"#{hospital_no} CMS: {cms}")
            except Exception:
                pass

            # Encoding check
            try:
                enc_info = await page.evaluate(JS_CHECK_ENCODING)
                if enc_info.get("garbledRatio", 0) > 0.1:
                    result["status"] = "encoding_error"
                    result["errors"].append({
                        "type": "encoding", "message": f"Garbled text ratio: {enc_info['garbledRatio']:.2%}",
                        "step": "navigate", "retryable": False,
                    })
                    log(f"#{hospital_no} Encoding error detected")
                    await browser.close()
                    return result
            except Exception:
                pass

            # Error page detection
            try:
                page_text = await page.evaluate("() => (document.body?.innerText || '').substring(0, 500)")
                if any(kw in page_text for kw in ["점검", "불가", "오류", "유지보수"]):
                    text_len = await page.evaluate(JS_GET_PAGE_TEXT_LENGTH)
                    if text_len < 500:  # Short error page
                        result["status"] = "partial"
                        result["errors"].append({
                            "type": "error_page", "message": "Maintenance/error page detected",
                            "step": "navigate", "retryable": True,
                        })
                        log(f"#{hospital_no} Error page detected")
            except Exception:
                pass

            # Anti-bot detection
            try:
                page_text = await page.evaluate("() => (document.body?.innerText || '').substring(0, 1000)")
                if "Checking your browser" in page_text or "CAPTCHA" in page_text:
                    log(f"#{hospital_no} Anti-bot detected, waiting 15s")
                    await page.wait_for_timeout(15000)
                    page_text = await page.evaluate("() => (document.body?.innerText || '').substring(0, 1000)")
                    if "Checking your browser" in page_text or "CAPTCHA" in page_text:
                        result["status"] = "requires_manual"
                        result["errors"].append({
                            "type": "antibot", "message": "CloudFlare/CAPTCHA not auto-resolved",
                            "step": "navigate", "retryable": False,
                        })
                        await browser.close()
                        return result
            except Exception:
                pass

            # Step 1b: Split-entry / splash page bypass
            # Chain clinics may show a branch selector with few links and minimal text
            try:
                splash_info = await page.evaluate("""
                () => {
                    const text = (document.body?.innerText || '').trim();
                    const links = Array.from(document.querySelectorAll('a[href]'));
                    const host = location.hostname.replace(/^www\\./, '');
                    const internal = links.filter(a => {
                        try {
                            const h = new URL(a.href).hostname.replace(/^www\\./, '');
                            return h === host || h.endsWith('.' + host);
                        } catch { return false; }
                    });
                    const internalHrefs = internal.map(a => ({
                        href: a.href,
                        text: (a.textContent || '').trim().toLowerCase(),
                    }));
                    return {
                        textLen: text.length,
                        totalLinks: links.length,
                        internalLinks: internalHrefs,
                        firstHref: internal[0]?.href || null,
                    };
                }
                """)
                if (splash_info.get("totalLinks", 99) <= 10
                        and splash_info.get("textLen", 9999) < 500
                        and splash_info.get("firstHref")):
                    # Pick best link from splash page (prefer skin/face/clinic keywords)
                    internal_links = splash_info.get("internalLinks", [])
                    best_link = splash_info["firstHref"]
                    if len(internal_links) > 1:
                        skin_kw = re.compile(r"face|skin|피부|clinic|derma", re.IGNORECASE)
                        for link in internal_links:
                            if skin_kw.search(link.get("href", "")) or skin_kw.search(link.get("text", "")):
                                best_link = link["href"]
                                break
                    first_link = best_link
                    log(f"#{hospital_no} Splash page detected "
                        f"({splash_info['totalLinks']} links, {splash_info['textLen']} chars), "
                        f"navigating to {first_link}")
                    await page.goto(first_link, wait_until="domcontentloaded", timeout=15000)
                    try:
                        final_url = await page.evaluate("() => window.location.href")
                        result["final_url"] = final_url
                    except Exception:
                        pass
            except Exception:
                pass

            # ---------------------------------------------------------------
            # Step 2: Dismiss Popups
            # ---------------------------------------------------------------
            log(f"#{hospital_no} Checking for popups")
            for attempt in range(3):
                try:
                    dismissed = await page.evaluate(JS_DISMISS_POPUPS)
                    if dismissed == 0:
                        break
                    log(f"#{hospital_no} Dismissed {dismissed} popup(s), attempt {attempt + 1}")
                    await page.wait_for_timeout(500)
                except Exception:
                    break

            # ---------------------------------------------------------------
            # Step 3: SPA Content Wait
            # ---------------------------------------------------------------
            try:
                text_len = await page.evaluate(JS_GET_PAGE_TEXT_LENGTH)
                if text_len < 200:
                    log(f"#{hospital_no} Minimal content ({text_len} chars), waiting for SPA")
                    spa_result = await page.evaluate(JS_SPA_WAIT)
                    log(f"#{hospital_no} SPA wait result: {spa_result}")
            except Exception:
                pass

            # ---------------------------------------------------------------
            # Step 4: Extract Social Channels
            # ---------------------------------------------------------------
            log(f"#{hospital_no} Extracting social channels")
            raw_channels = []

            # Pass 1 + 1.5 + 1.75 + 2 (static + iframe + structured + dynamic)
            try:
                channels = await page.evaluate(JS_SOCIAL_EXTRACT)
                raw_channels.extend(channels)
                log(f"#{hospital_no} Found {len(channels)} channels from main extraction")
            except Exception as e:
                result["errors"].append({"type": "extraction", "message": str(e)[:200], "step": "social", "retryable": False})

            # Pass 2: window.open intercept
            try:
                intercepted = await page.evaluate(JS_WINDOW_OPEN_INTERCEPT)
                for u in intercepted:
                    platform = classify_url(u)
                    if platform:
                        raw_channels.append({"platform": platform, "url": u, "method": "window_open_intercept"})
                if intercepted:
                    log(f"#{hospital_no} Intercepted {len(intercepted)} window.open calls")
            except Exception:
                pass

            # Pass 2.5: Scroll-triggered elements
            try:
                scroll_results = await page.evaluate(JS_SCROLL_TRIGGER)
                for item in scroll_results:
                    platform = classify_url(item.get("href", ""))
                    if platform:
                        raw_channels.append({"platform": platform, "url": item["href"], "method": "scroll_triggered"})
            except Exception:
                pass

            # Pass 4: URL Validation + de-duplication
            seen_urls = set()
            for ch in raw_channels:
                url_val = normalize_url(ch.get("url", ""))
                if not url_val or url_val in seen_urls:
                    continue
                # Skip widget: pseudo-URLs for now (just note them in errors)
                if url_val.startswith("widget:"):
                    result["errors"].append({"type": "info", "message": f"Widget detected: {url_val}", "step": "social", "retryable": False})
                    continue
                seen_urls.add(url_val)
                platform = ch.get("platform") or classify_url(url_val)
                if platform:
                    result["social_channels"].append({
                        "platform": platform,
                        "url": url_val,
                        "extraction_method": ch.get("method", "unknown"),
                        "confidence": 1.0,
                        "status": "active",
                    })

            # Pass 5: Resolve NaverShortlink (naver.me) URLs via redirect
            for ch in result["social_channels"]:
                if ch["platform"] != "NaverShortlink":
                    continue
                try:
                    new_page = await context.new_page()
                    resp = await new_page.goto(ch["url"], wait_until="commit", timeout=5000)
                    resolved = new_page.url
                    await new_page.close()
                    new_platform = classify_url(resolved)
                    if new_platform and new_platform != "NaverShortlink":
                        ch["platform"] = new_platform
                        ch["url"] = normalize_url(resolved)
                        log(f"#{hospital_no} Resolved naver.me -> {new_platform}: {resolved[:80]}")
                except Exception:
                    try:
                        await new_page.close()
                    except Exception:
                        pass

            # Pass 6: Follow internal redirect links (page.asp?m=kakao, link.php?go=, etc.)
            # When 0 social channels found, scan page for internal links whose
            # text/alt contains social keywords and resolve them via navigation.
            if not result["social_channels"]:
                try:
                    redirect_links = await page.evaluate("""
                    () => {
                        const keywords = /kakao|카카오|naver|네이버|blog|블로그|instagram|인스타|youtube|유튜브|facebook|페이스북|line|라인|talk|톡/i;
                        const links = [];
                        document.querySelectorAll('a[href], area[href]').forEach(el => {
                            const href = el.href || el.getAttribute('href') || '';
                            const text = (el.textContent || '').trim();
                            const alt = el.querySelector('img')?.alt || '';
                            const title = el.getAttribute('title') || '';
                            const combined = text + ' ' + alt + ' ' + title;
                            // Must be internal link (same domain or relative) with social keyword
                            if (!href) return;
                            const isInternal = href.startsWith('/') || href.includes(location.hostname) ||
                                /\.(asp|php|jsp|do|html?)\?/.test(href);
                            const hasSocialKeyword = keywords.test(combined) || keywords.test(href);
                            // Skip already-social URLs (pf.kakao.com, instagram.com, etc.)
                            const alreadySocial = /kakao\.com|instagram\.com|youtube\.com|naver\.com|facebook\.com|line\.me/.test(href);
                            if (isInternal && hasSocialKeyword && !alreadySocial && href.length < 300) {
                                links.push({href: href, text: combined.substring(0, 50)});
                            }
                        });
                        // Also check iframes for redirect links
                        document.querySelectorAll('iframe').forEach(iframe => {
                            try {
                                const iDoc = iframe.contentDocument;
                                if (!iDoc) return;
                                iDoc.querySelectorAll('a[href]').forEach(el => {
                                    const href = el.href || el.getAttribute('href') || '';
                                    const text = (el.textContent || '').trim();
                                    const alt = el.querySelector('img')?.alt || '';
                                    const combined = text + ' ' + alt;
                                    const isInternal = href.startsWith('/') || href.includes(location.hostname) ||
                                        /\.(asp|php|jsp|do|html?)\?/.test(href);
                                    const hasSocialKeyword = keywords.test(combined) || keywords.test(href);
                                    const alreadySocial = /kakao\.com|instagram\.com|youtube\.com|naver\.com|facebook\.com|line\.me/.test(href);
                                    if (isInternal && hasSocialKeyword && !alreadySocial && href.length < 300) {
                                        links.push({href: href, text: combined.substring(0, 50)});
                                    }
                                });
                            } catch(e) {}
                        });
                        // Deduplicate
                        const seen = new Set();
                        return links.filter(l => { if (seen.has(l.href)) return false; seen.add(l.href); return true; });
                    }
                    """)
                    if redirect_links:
                        log(f"#{hospital_no} Found {len(redirect_links)} internal redirect candidates")
                    for rl in redirect_links[:10]:  # max 10 to avoid abuse
                        try:
                            redir_page = await context.new_page()
                            await redir_page.goto(rl["href"], wait_until="commit", timeout=8000)
                            resolved_url = redir_page.url
                            await redir_page.close()
                            resolved_norm = normalize_url(resolved_url)
                            if resolved_norm and resolved_norm not in seen_urls:
                                platform = classify_url(resolved_norm)
                                if platform:
                                    seen_urls.add(resolved_norm)
                                    result["social_channels"].append({
                                        "platform": platform,
                                        "url": resolved_norm,
                                        "extraction_method": "redirect_follow",
                                        "confidence": 0.9,
                                        "status": "active",
                                    })
                                    log(f"#{hospital_no} Redirect resolved: {rl['text'][:20]} -> {platform}: {resolved_norm[:60]}")
                        except Exception:
                            try:
                                await redir_page.close()
                            except Exception:
                                pass
                except Exception as e:
                    log(f"#{hospital_no} Redirect scan error: {str(e)[:100]}")

            log(f"#{hospital_no} Total social channels: {len(result['social_channels'])}")

            # ---------------------------------------------------------------
            # Step 5: Collect ALL Candidate URLs for Doctor Page
            # ---------------------------------------------------------------
            log(f"#{hospital_no} Looking for doctor page")
            doctor_page_found = False
            candidate_urls = []  # list of (url, source_label)

            # Step 5a: Reveal hidden submenus via hover before searching
            try:
                await page.evaluate("""
                () => {
                    const parents = document.querySelectorAll(
                        'nav > ul > li, .gnb > li, .menu > li, [class*="nav"] > ul > li, header li'
                    );
                    parents.forEach(li => {
                        li.dispatchEvent(new MouseEvent('mouseenter', {bubbles: true}));
                        li.dispatchEvent(new MouseEvent('mouseover', {bubbles: true}));
                    });
                }
                """)
                await page.wait_for_timeout(500)
            except Exception:
                pass

            # Step 5a: Collect doctor menu links
            try:
                doctor_links = await page.evaluate(
                    JS_FIND_DOCTOR_MENU,
                    [DOCTOR_PRIMARY, DOCTOR_SECONDARY, DOCTOR_SUBMENU_PARENTS],
                )
                for link in (doctor_links or []):
                    href = link.get("href", "")
                    if href and href.startswith("http"):
                        candidate_urls.append((href, f"menu:{link['text']}"))
                if doctor_links:
                    log(f"#{hospital_no} Found {len(doctor_links)} doctor menu link(s)")
                else:
                    log(f"#{hospital_no} No doctor menu found")
            except Exception as e:
                log(f"#{hospital_no} Doctor menu search error: {str(e)[:100]}")

            # Step 5b-1: Navigate to intro/about pages, scan for doctor sub-links
            # Also add the intro/about pages themselves as candidates
            # Always run regardless of 5a results (menu links may be wrong pages)
            if True:
                try:
                    intro_links = await page.evaluate("""() => {
                        const kw = ['소개', 'about', 'intro'];
                        return Array.from(document.querySelectorAll('a[href]'))
                            .filter(a => {
                                const text = (a.textContent || '').trim().toLowerCase();
                                const href = (a.href || '').toLowerCase();
                                return text.length < 20 && kw.some(k => text.includes(k) || href.includes(k));
                            })
                            .map(a => ({text: a.textContent.trim(), href: a.href}))
                            .filter(l => l.href && !l.href.includes('#'))
                            .slice(0, 5);
                    }""")
                    for link in (intro_links or []):
                        log(f"#{hospital_no} Scanning intro page: {link['text']} -> {link['href']}")
                        try:
                            await page.goto(link["href"], wait_until="domcontentloaded", timeout=15000)
                            await page.wait_for_timeout(1500)
                            # Re-scan for doctor links on this page
                            doctor_links_2nd = await page.evaluate("""() => {
                                const docKw = ['의료진', '원장', '전문의', 'doctor', 'staff', 'team'];
                                return Array.from(document.querySelectorAll('a[href]'))
                                    .filter(a => {
                                        const text = (a.textContent || '').trim().toLowerCase();
                                        const href = (a.href || '').toLowerCase();
                                        return docKw.some(k => text.includes(k) || href.includes('/doctor') || href.includes('/staff') || href.includes('/team'));
                                    })
                                    .map(a => ({text: a.textContent.trim(), href: a.href}))
                                    .slice(0, 3);
                            }""")
                            for dl in (doctor_links_2nd or []):
                                if dl['href'] and dl['href'].startswith("http"):
                                    candidate_urls.append((dl['href'], f"intro_sub:{dl['text']}"))
                        except Exception:
                            pass
                        # Add the intro/about page itself as a candidate (may contain doctor info directly)
                        candidate_urls.append((link['href'], f"intro_page:{link['text']}"))
                except Exception as e:
                    log(f"#{hospital_no} Intro page scan error: {str(e)[:100]}")

            # Step 5b-2: Sitemap - collect ALL matching URLs
            try:
                sitemap_url = f"{base_url}/sitemap.xml"
                await page.goto(sitemap_url, wait_until="domcontentloaded", timeout=10000)
                sitemap_text = await page.evaluate("() => document.body?.innerText || ''")
                doc_patterns = ["/doctor", "/staff", "/team", "/about", "/introduce",
                               "/intro", "/의료진", "/원장", "/전문의"]
                for pattern in doc_patterns:
                    matches = re.findall(rf"(https?://[^\s<]+{re.escape(pattern)}[^\s<]*)", sitemap_text)
                    for doc_url in matches:
                        candidate_urls.append((doc_url, f"sitemap:{pattern}"))
            except Exception:
                pass

            # Step 5c: Main page as last resort (always included)
            candidate_urls.append((url, "main_page"))

            # Deduplicate preserving priority order
            seen_urls = set()
            unique_candidates = []
            for c_url, source in candidate_urls:
                normalized = c_url.rstrip('/')
                if normalized not in seen_urls:
                    seen_urls.add(normalized)
                    unique_candidates.append((c_url, source))

            log(f"#{hospital_no} Collected {len(unique_candidates)} candidate URLs:")
            for i, (c_url, source) in enumerate(unique_candidates):
                log(f"#{hospital_no}   [{i+1}] {source} -> {c_url}")

            # ---------------------------------------------------------------
            # Step 6: Extract Doctor Info - iterate through ALL candidates
            # ---------------------------------------------------------------
            # Define OCR helpers before the candidate loop
            ocr_prompt_tpl = (
                "Read the image file at {path}.\n\n"
                "This is a screenshot from a Korean dermatology/skin clinic website's "
                "doctor introduction page (의료진 소개).\n\n"
                "Extract ONLY doctor/physician information. Look for:\n"
                "- Names: 2-3 Korean characters (한글). Common surnames: "
                "김,이,박,최,정,강,조,윤,장,임,한,오,서,신,권,황,안,송,류,전,홍\n"
                "- Titles: 대표원장, 원장, 부원장, 전문의, 피부과전문의\n"
                "- Education: contains 대학교, 졸업, 수료, 석사, 박사, 의학전문대학원\n"
                "- Career: contains 병원, 클리닉, 센터, 수련, 전공의, 레지던트\n"
                "- Credentials: contains 학회, 정회원, 전문의, 자격, 인증\n\n"
                "IGNORE: navigation menus, hospital name/address/phone, "
                "nurses (간호사), coordinators (코디네이터), consultants (상담사).\n\n"
                "Return ONLY a valid JSON array. No explanation, no markdown fences.\n"
                "Each item: {{\"name\":\"...\",\"role\":\"...\","
                "\"education\":[...],\"career\":[...],\"credentials\":[...]}}\n"
                "If no doctors found, return: []"
            )

            def _parse_ocr_json(text):
                """Parse JSON array from Gemini OCR output with robust fallback."""
                json_match = re.search(r"```(?:json)?\s*(\[[\s\S]*?\])\s*```", text)
                if json_match:
                    try:
                        return json.loads(json_match.group(1))
                    except json.JSONDecodeError:
                        pass
                json_match = re.search(r"\[[\s\S]*?\]", text)
                if json_match:
                    try:
                        return json.loads(json_match.group(0))
                    except json.JSONDecodeError:
                        pass
                json_match = re.search(r"\[[\s\S]*\]", text)
                if json_match:
                    raw = json_match.group(0)
                    for i in range(len(raw) - 1, 0, -1):
                        if raw[i] == ']':
                            try:
                                return json.loads(raw[:i+1])
                            except json.JSONDecodeError:
                                continue
                return []

            def _run_gemini_ocr(prompt, image_path):
                """Run Gemini CLI with image via --include-directories for vision mode."""
                image_dir = os.path.dirname(image_path)
                r = subprocess.run(
                    ["gemini", "-p", prompt,
                     "-y", "--include-directories", image_dir],
                    capture_output=True, text=True, timeout=90,
                )
                if r.returncode == 0:
                    return _parse_ocr_json(r.stdout)
                return []

            def _append_ocr_doctors(doctors_raw, seen_names, result_doctors):
                """Append unique OCR doctors to result list. Returns count added."""
                added = 0
                for doc in doctors_raw:
                    name = doc.get("name", "")
                    if name and len(name) >= 2 and name not in seen_names:
                        seen_names.add(name)
                        result_doctors.append({
                            "name": name, "name_english": "",
                            "role": doc.get("role", "specialist"),
                            "photo_url": "",
                            "education": doc.get("education", []),
                            "career": doc.get("career", []),
                            "credentials": doc.get("credentials", []),
                            "branch": "", "branches": [],
                            "extraction_source": "ocr", "ocr_source": True,
                        })
                        added += 1
                return added

            ocr_seen_names = set()
            last_screenshot_path = None
            temp_screenshots = []

            try:
                for cand_idx, (cand_url, cand_source) in enumerate(unique_candidates):
                    if result["doctors"]:
                        break  # Already found doctors

                    log(f"#{hospital_no} Trying candidate {cand_idx+1}/{len(unique_candidates)}: {cand_source}")

                    # Navigate to candidate
                    try:
                        await page.goto(cand_url, wait_until="domcontentloaded", timeout=15000)
                        await page.wait_for_timeout(1500)
                    except Exception as e:
                        log(f"#{hospital_no} Navigation failed for {cand_url}: {str(e)[:100]}")
                        continue

                    # Scroll for lazy loading
                    try:
                        for _ in range(10):
                            await page.evaluate("window.scrollBy(0, 600)")
                            await page.wait_for_timeout(500)
                        await page.wait_for_timeout(1000)
                    except Exception:
                        pass

                    # Click tabs with doctor keywords
                    try:
                        tab_texts = await page.evaluate("""
                        () => {
                            const tabEls = document.querySelectorAll(
                                '[role="tab"], .tab-link, .tabs > *, .tab-item, [class*="tab"] a, [class*="tab"] button'
                            );
                            const kw = ['의료진', '원장', '전문의', '대표', 'doctor', 'staff', '소개'];
                            return Array.from(tabEls)
                                .filter(t => {
                                    const txt = (t.textContent || '').trim().toLowerCase();
                                    return txt.length < 20 && kw.some(k => txt.includes(k));
                                })
                                .map(t => (t.textContent || '').trim())
                                .slice(0, 5);
                        }
                        """)
                        for tab_text in (tab_texts or []):
                            try:
                                await page.get_by_text(tab_text, exact=True).first.click(timeout=3000)
                                await page.wait_for_timeout(1000)
                                log(f"#{hospital_no} Clicked tab: {tab_text}")
                            except Exception:
                                pass
                    except Exception:
                        pass

                    # DOM extraction
                    try:
                        is_image_based = await page.evaluate(JS_CHECK_IMAGE_BASED)

                        need_ocr = is_image_based
                        if not is_image_based:
                            doctors = await page.evaluate(JS_EXTRACT_DOCTORS)
                            if doctors:
                                # Validate names - filter to plausible Korean names only
                                valid_doctors = [d for d in doctors if _is_plausible_korean_name(d.get("name", ""))]
                                if valid_doctors:
                                    result["doctors"] = valid_doctors
                                    doctor_page_found = True
                                    log(f"#{hospital_no} DOM: {len(valid_doctors)} valid / {len(doctors)} total from {cand_source}")
                                    break
                                else:
                                    log(f"#{hospital_no} DOM: {len(doctors)} entries but 0 valid names from {cand_source}, falling back to OCR")
                                    need_ocr = True
                            else:
                                log(f"#{hospital_no} DOM: 0 doctors from {cand_source}")
                                need_ocr = True
                        else:
                            log(f"#{hospital_no} Image-based page: {cand_source}")

                        if need_ocr:
                            # Scroll to load lazy images
                            try:
                                scroll_h = await page.evaluate("() => document.body.scrollHeight")
                                for pos in range(0, scroll_h, 600):
                                    await page.evaluate(f"window.scrollTo(0, {pos})")
                                    await page.wait_for_timeout(300)
                            except Exception:
                                pass

                            ts = int(time.time())
                            fullpage_path = f"/tmp/clinic_crawl_{hospital_no}_{ts}.jpg"
                            await page.evaluate("window.scrollTo(0, 0)")
                            await page.wait_for_timeout(300)
                            await page.screenshot(path=fullpage_path, full_page=True, type="jpeg", quality=85)
                            last_screenshot_path = fullpage_path
                            temp_screenshots.append(fullpage_path)

                            # Tier B: one OCR attempt per candidate
                            try:
                                log(f"#{hospital_no} OCR Tier B on {cand_source}")
                                prompt_b = ocr_prompt_tpl.replace("{path}", fullpage_path)
                                doctors_raw = _run_gemini_ocr(prompt_b, fullpage_path)
                                added = _append_ocr_doctors(doctors_raw, ocr_seen_names, result["doctors"])
                                if result["doctors"]:
                                    doctor_page_found = True
                                    log(f"#{hospital_no} OCR: {added} doctors from {cand_source}")
                                    break
                                else:
                                    log(f"#{hospital_no} OCR: 0 doctors from {cand_source}")
                            except subprocess.TimeoutExpired:
                                log(f"#{hospital_no} OCR timeout on {cand_source}, trying next candidate")
                            except FileNotFoundError:
                                log(f"#{hospital_no} Gemini CLI not installed")
                                break

                    except Exception as e:
                        log(f"#{hospital_no} Extraction error on {cand_source}: {str(e)[:100]}")

                # After ALL candidates exhausted - final OCR fallback (Tier B retry + Tier C)
                if not result["doctors"] and last_screenshot_path:
                    log(f"#{hospital_no} All {len(unique_candidates)} candidates returned 0. Final OCR attempt.")

                    # Tier B retry on last screenshot
                    try:
                        log(f"#{hospital_no} OCR Tier B retry on last page")
                        prompt_retry = ocr_prompt_tpl.replace("{path}", last_screenshot_path)
                        retry_docs = _run_gemini_ocr(prompt_retry, last_screenshot_path)
                        _append_ocr_doctors(retry_docs, ocr_seen_names, result["doctors"])
                    except Exception:
                        pass

                    if not result["doctors"]:
                        # Tier C: viewport chunks on last page
                        chunk_paths = []
                        try:
                            vp_height = 900
                            scroll_h = await page.evaluate("() => document.body.scrollHeight")
                            for i, pos in enumerate(range(0, scroll_h, vp_height)):
                                await page.evaluate(f"window.scrollTo(0, {pos})")
                                await page.wait_for_timeout(300)
                                chunk_path = f"/tmp/clinic_crawl_{hospital_no}_{int(time.time())}_{i}.jpg"
                                await page.screenshot(path=chunk_path, full_page=False, type="jpeg", quality=85)
                                chunk_paths.append(chunk_path)
                                if len(chunk_paths) >= 8:
                                    break
                            log(f"#{hospital_no} OCR Tier C: {len(chunk_paths)} viewport chunks")
                        except Exception:
                            pass

                        for cp in chunk_paths:
                            try:
                                prompt_c = ocr_prompt_tpl.replace("{path}", cp)
                                chunk_docs = _run_gemini_ocr(prompt_c, cp)
                                _append_ocr_doctors(chunk_docs, ocr_seen_names, result["doctors"])
                            except Exception:
                                pass

                        temp_screenshots.extend(chunk_paths)

                    if result["doctors"]:
                        doctor_page_found = True
                        log(f"#{hospital_no} Final OCR: {len(result['doctors'])} doctors found")

                # ── Phase 2: AI-assisted navigation discovery ──
                # When all rule-based candidates failed, let Gemini analyze the
                # main page and suggest where the doctor page might be.
                if not result["doctors"]:
                    log(f"#{hospital_no} Phase 2: AI navigation discovery from main page")
                    try:
                        await page.goto(url, wait_until="domcontentloaded", timeout=15000)
                        await page.wait_for_timeout(2000)

                        ts_nav = int(time.time())
                        nav_path = f"/tmp/clinic_nav_{hospital_no}_{ts_nav}.jpg"
                        await page.screenshot(path=nav_path, full_page=False, type="jpeg", quality=85)
                        temp_screenshots.append(nav_path)

                        nav_prompt = (
                            f"Read the image file at {nav_path}.\n\n"
                            "This is a Korean skin/dermatology clinic website homepage.\n\n"
                            "TASK 1: Are doctor names, photos, or medical credentials "
                            "visible on THIS page? If yes, extract them.\n\n"
                            "TASK 2: Look at the navigation menu (top bar, sidebar, footer). "
                            "Which menu or link most likely leads to a doctor/medical staff page?\n"
                            "Common labels: 의료진, 원장, 전문의, 병원소개, About, Staff, Team\n\n"
                            "Return ONLY JSON (no markdown fences):\n"
                            "{\"doctors\": [{\"name\": \"...\", \"role\": \"...\"}], "
                            "\"suggested_paths\": [\"/path1\", \"/path2\"]}\n"
                            "doctors: any doctors visible on THIS page ([] if none)\n"
                            "suggested_paths: relative URL paths likely containing doctor info"
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

                                # Check doctors found on main page
                                for doc in nav_data.get("doctors", []):
                                    name = doc.get("name", "")
                                    if name and _is_plausible_korean_name(name) and name not in ocr_seen_names:
                                        ocr_seen_names.add(name)
                                        result["doctors"].append({
                                            "name": name, "name_english": "",
                                            "role": doc.get("role", "specialist"),
                                            "photo_url": "",
                                            "education": doc.get("education", []),
                                            "career": doc.get("career", []),
                                            "credentials": doc.get("credentials", []),
                                            "branch": "", "branches": [],
                                            "extraction_source": "ai_nav", "ocr_source": True,
                                        })

                                if result["doctors"]:
                                    doctor_page_found = True
                                    log(f"#{hospital_no} AI found {len(result['doctors'])} doctors on main page")

                                # Try AI-suggested paths
                                if not result["doctors"]:
                                    ai_paths = nav_data.get("suggested_paths", [])
                                    log(f"#{hospital_no} AI suggested {len(ai_paths)} paths: {ai_paths}")

                                    for ai_path in ai_paths[:3]:
                                        try:
                                            ai_url = urljoin(base_url + "/", ai_path)
                                            if ai_url.rstrip('/') in seen_urls:
                                                continue

                                            log(f"#{hospital_no} Trying AI suggestion: {ai_path} -> {ai_url}")
                                            await page.goto(ai_url, wait_until="domcontentloaded", timeout=15000)
                                            await page.wait_for_timeout(2000)

                                            # Scroll
                                            for _ in range(8):
                                                await page.evaluate("window.scrollBy(0, 600)")
                                                await page.wait_for_timeout(400)

                                            # DOM extraction + validation
                                            doctors = await page.evaluate(JS_EXTRACT_DOCTORS)
                                            if doctors:
                                                valid_doctors = [d for d in doctors if _is_plausible_korean_name(d.get("name", ""))]
                                                if valid_doctors:
                                                    result["doctors"] = valid_doctors
                                                    doctor_page_found = True
                                                    log(f"#{hospital_no} AI path DOM: {len(valid_doctors)} valid / {len(doctors)} total")
                                                    break

                                            # OCR on AI-suggested page
                                            ts_ai = int(time.time())
                                            ai_ss = f"/tmp/clinic_ai_{hospital_no}_{ts_ai}.jpg"
                                            await page.evaluate("window.scrollTo(0, 0)")
                                            await page.wait_for_timeout(300)
                                            await page.screenshot(path=ai_ss, full_page=True, type="jpeg", quality=85)
                                            temp_screenshots.append(ai_ss)

                                            prompt_ai = ocr_prompt_tpl.replace("{path}", ai_ss)
                                            ai_docs = _run_gemini_ocr(prompt_ai, ai_ss)
                                            _append_ocr_doctors(ai_docs, ocr_seen_names, result["doctors"])

                                            if result["doctors"]:
                                                doctor_page_found = True
                                                log(f"#{hospital_no} AI path OCR: {len(result['doctors'])} doctors")
                                                break
                                        except Exception as e:
                                            log(f"#{hospital_no} AI path error: {str(e)[:100]}")
                                            continue

                    except subprocess.TimeoutExpired:
                        log(f"#{hospital_no} AI navigation timeout")
                    except Exception as e:
                        log(f"#{hospital_no} AI navigation error: {str(e)[:100]}")

                # Final: save screenshot if still no doctors
                if not result["doctors"] and last_screenshot_path:
                    save_dir = os.path.join(
                        os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),
                        "data", "clinic-results", "screenshots",
                    )
                    os.makedirs(save_dir, exist_ok=True)
                    save_path = os.path.join(save_dir, f"{hospital_no}_doctors.jpg")
                    shutil.copy2(last_screenshot_path, save_path)
                    log(f"#{hospital_no} All methods exhausted. Screenshot saved: {save_path}")
                    result["errors"].append({
                        "type": "all_methods_exhausted",
                        "message": f"Rule-based ({len(unique_candidates)} candidates) + AI navigation all failed. Screenshot: {save_path}",
                        "step": "doctor_extract", "retryable": True,
                    })

                log(f"#{hospital_no} Doctor extraction complete: {len(result['doctors'])} doctors")

            except Exception as e:
                result["errors"].append({"type": "extraction", "message": str(e)[:200], "step": "doctor_extract", "retryable": True})
            finally:
                # Cleanup all temp screenshots
                for sp in temp_screenshots:
                    try:
                        os.remove(sp)
                    except OSError:
                        pass

            # Determine final status
            has_social = len(result["social_channels"]) > 0
            has_doctors = len(result["doctors"]) > 0

            # Track whether a doctor page exists on this site
            result["doctor_page_exists"] = 1 if (doctor_page_found or has_doctors) else 0

            if result["status"] == "success":
                if has_social and has_doctors:
                    pass  # success: both categories have data
                elif has_social or has_doctors:
                    result["status"] = "partial"
                    missing = "doctors" if not has_doctors else "social_channels"
                    result["errors"].append({
                        "type": "partial_data",
                        "message": f"Missing {missing}: social={len(result['social_channels'])}, doctors={len(result['doctors'])}",
                        "step": "final_status", "retryable": True,
                    })
                else:
                    result["status"] = "empty"  # crawl completed but no data

        except Exception as e:
            result["status"] = "failed"
            result["errors"].append({
                "type": "unexpected", "message": str(e)[:300],
                "step": "unknown", "retryable": True,
            })
            log(f"#{hospital_no} Unexpected error: {e}")

        finally:
            await browser.close()

    # ---------------------------------------------------------------
    # Step 7: Save Results
    # ---------------------------------------------------------------
    log(f"#{hospital_no} Saving results (status={result['status']}, "
        f"channels={len(result['social_channels'])}, doctors={len(result['doctors'])})")
    try:
        save_result(db_path, result)
        log(f"#{hospital_no} Saved to {db_path}")
    except Exception as e:
        result["errors"].append({
            "type": "storage_error", "message": str(e)[:200],
            "step": "save", "retryable": True,
        })
        log(f"#{hospital_no} Storage error: {e}")

    return result


# ---------------------------------------------------------------------------
# CLI entry point
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(description="Crawl a single hospital with isolated browser")
    parser.add_argument("--no", type=int, required=True, help="Hospital number")
    parser.add_argument("--name", required=True, help="Hospital name")
    parser.add_argument("--url", required=True, help="Hospital website URL")
    parser.add_argument("--db", default=DB_DEFAULT, help=f"SQLite DB path (default: {DB_DEFAULT})")
    parser.add_argument("--timeout", type=int, default=45, help="Page timeout in seconds (default: 45)")
    parser.add_argument("--headed", action="store_true", help="Run with visible browser (for debugging)")
    args = parser.parse_args()

    result = asyncio.run(
        crawl_hospital(
            hospital_no=args.no,
            name=args.name,
            url=args.url,
            db_path=args.db,
            timeout=args.timeout,
            headless=not args.headed,
        )
    )

    # Output JSON to stdout
    print(json.dumps(result, ensure_ascii=False, indent=2))

    # Auto-export unified CSV after crawl completion
    if result["status"] in ("success", "partial"):
        try:
            export_unified_csv(args.db, CSV_SOURCE, CSV_UNIFIED_OUTPUT)
        except Exception as e:
            print(f"[crawl] CSV export failed: {e}", file=sys.stderr, flush=True)

    sys.exit(0 if result["status"] in ("success", "partial") else 1)


if __name__ == "__main__":
    main()
