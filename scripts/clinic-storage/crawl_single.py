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
    "NaverTalk": [r"talk\.naver\.com/", r"naver\.me/"],
    "Line": [r"line\.me/", r"lin\.ee/"],
    "WeChat": [r"u\.wechat\.com/", r"weixin\.qq\.com/"],
    "WhatsApp": [r"wa\.me/", r"api\.whatsapp\.com/"],
    "Telegram": [r"t\.me/[^/]+$"],
    "FacebookMessenger": [r"m\.me/"],
    "NaverBooking": [r"booking\.naver\.com/"],
    "Instagram": [r"instagram\.com/"],
    "YouTube": [r"youtube\.com/", r"youtu\.be/"],
    "NaverBlog": [r"blog\.naver\.com/"],
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
]
DOCTOR_SUBMENU_PARENTS = [
    "병원 소개", "클리닉 소개", "소개", "병원 안내", "클리닉 안내", "About",
]

DOCTOR_ROLES_KEEP = {"원장", "대표원장", "부원장", "전문의", "의사", "레지던트", "인턴"}
DOCTOR_ROLES_EXCLUDE = {"간호사", "간호조무사", "피부관리사", "상담사", "코디네이터", "스텝", "직원"}

ROLE_RE = re.compile(r"^(.+?)\s+(원장|대표원장|부원장|전문의|의사|레지던트|인턴)$")

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def classify_url(url: str) -> Optional[str]:
    """Classify a URL into a social platform name."""
    if not url:
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

    function addResult(platform, url, method) {
        if (!url || seen.has(url)) return;
        seen.add(url);
        results.push({platform, url, method});
    }

    // Platform detection regex map
    const platformPatterns = {
        KakaoTalk: /pf\\.kakao\\.com|open\\.kakao\\.com\\/o|talk\\.kakao\\.com|kakao\\.com\\/channel/i,
        NaverTalk: /talk\\.naver\\.com|naver\\.me\\//i,
        Line: /line\\.me\\/|lin\\.ee\\//i,
        WeChat: /u\\.wechat\\.com|weixin\\.qq\\.com/i,
        WhatsApp: /wa\\.me\\/|api\\.whatsapp\\.com/i,
        Telegram: /t\\.me\\/[^/]+$/i,
        FacebookMessenger: /m\\.me\\//i,
        NaverBooking: /booking\\.naver\\.com/i,
        Instagram: /instagram\\.com\\//i,
        YouTube: /youtube\\.com\\/|youtu\\.be\\//i,
        NaverBlog: /blog\\.naver\\.com\\//i,
        Facebook: /facebook\\.com\\//i,
    };

    function classifyUrl(url) {
        if (!url) return null;
        if (url.startsWith('tel:')) return 'Phone';
        if (url.startsWith('sms:')) return 'SMS';
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

    for (const a of allLinks) {
        const text = (a.textContent || '').trim();
        const href = a.href || a.getAttribute('href') || '';
        if (!text || text.length > 30) continue;

        const visible = a.offsetParent !== null && a.offsetWidth > 0;

        // Check primary labels
        for (const label of primaryLabels) {
            if (text === label || text.includes(label)) {
                results.push({text, href, priority: 1, visible, element: a.outerHTML.substring(0, 200)});
            }
        }
        // Check secondary labels
        for (const label of secondaryLabels) {
            if (text === label || text.includes(label)) {
                results.push({text, href, priority: 2, visible, element: a.outerHTML.substring(0, 200)});
            }
        }
        // Check URL patterns
        if (/\\/doctor|\\/staff|\\/team|\\/about|\\/introduce|\\/의료진|\\/원장|\\/전문의|\\/소개/.test(href)) {
            results.push({text, href, priority: 1, visible, element: a.outerHTML.substring(0, 200)});
        }
    }

    // De-duplicate: prefer visible links, then sort by priority
    const unique = [];
    const seenHrefs = new Set();
    results.sort((a, b) => {
        if (a.visible !== b.visible) return a.visible ? -1 : 1;
        return a.priority - b.priority;
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
        '서울', '인터', '채용', '공지', '조회',
        '미용', '홍보', '오늘', '강사', '소개', '마사',
    ];
    const surnames = new Set(
        '김이박최정강조윤장임한오서신권황안송류전홍유고문양손배백허남심노하곽성차주우구민진지엄채원천방공현함변추도소석선설마길연위표명기반왕금옥육인맹제모탁국여어은편빈예봉경태피감복'.split('')
    );
    const nonNameExact = new Set([
        '대표', '멤버', '보유', '대한', '의학', '교육', '운영',
        '소개', '경력', '인사', '선생', '안내', '예약', '진료',
        '진단', '보험', '도입', '경험', '인증', '소속',
        // Common non-name words that pass surname check
        '원장', '전담', '기기', '최신', '어떤', '최애', '주요',
        '안과', '여의사', '주름', '노하우', '원소개', '이퓨어',
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
        if (name.length === 3 && /[의과에적대는]$/.test(name)) return false;
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
            'li, article, section, .item, .card, .member, [class*="team"], [class*="profile"], [class*="intro"]'
        );
        for (const card of items) {
            const text = card.textContent || '';
            if (text.length > 2000 || text.length < 4) continue;
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

    // Priority order: S1 (best selectors) → S2 (generic) → S3 (text)
    for (const d of s1) mergeDoc(d);
    for (const d of s2) mergeDoc(d);
    for (const d of s3) mergeDoc(d);

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
        if (text.length > 2 && /원장|대표원장|부원장|전문의|의사|학력|경력|약력|자격|졸업|수료|대학원|대학교|정회원|학회|인턴|레지던트|수련|피부과/.test(text)) {
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
                url_val = strip_tracking(ch.get("url", ""))
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

            log(f"#{hospital_no} Total social channels: {len(result['social_channels'])}")

            # ---------------------------------------------------------------
            # Step 5: Find and Navigate to Doctor Page
            # ---------------------------------------------------------------
            log(f"#{hospital_no} Looking for doctor page")
            doctor_page_found = False

            # Step 5a: Menu-based navigation
            try:
                doctor_links = await page.evaluate(
                    JS_FIND_DOCTOR_MENU,
                    [DOCTOR_PRIMARY, DOCTOR_SECONDARY, DOCTOR_SUBMENU_PARENTS],
                )
                if doctor_links:
                    best = doctor_links[0]
                    is_hidden = not best.get("visible", True)
                    log(f"#{hospital_no} Found doctor menu: {best['text']} -> {best['href']}"
                        f"{' (hidden submenu)' if is_hidden else ''}")
                    href = best.get("href", "")
                    if is_hidden and href and href.startswith("http"):
                        # Hidden link (dropdown submenu) - navigate directly
                        try:
                            await page.goto(href, wait_until="domcontentloaded", timeout=15000)
                            doctor_page_found = True
                        except Exception:
                            pass
                    else:
                        # Visible link - try click first, fallback to goto
                        try:
                            link_text = best["text"]
                            link = page.get_by_text(link_text, exact=True).first
                            await link.click(timeout=10000)
                            await page.wait_for_timeout(2000)
                            doctor_page_found = True
                        except Exception:
                            if href and href.startswith("http"):
                                try:
                                    await page.goto(href, wait_until="domcontentloaded", timeout=15000)
                                    doctor_page_found = True
                                except Exception:
                                    pass
                else:
                    log(f"#{hospital_no} No doctor menu found")
            except Exception as e:
                log(f"#{hospital_no} Doctor menu search error: {str(e)[:100]}")

            # Step 5b: Sitemap fallback (independent try block)
            if not doctor_page_found:
                try:
                    sitemap_url = f"{base_url}/sitemap.xml"
                    await page.goto(sitemap_url, wait_until="domcontentloaded", timeout=10000)
                    sitemap_text = await page.evaluate("() => document.body?.innerText || ''")
                    doc_patterns = ["/doctor", "/staff", "/team", "/about", "/introduce",
                                   "/의료진", "/원장", "/전문의"]
                    for pattern in doc_patterns:
                        match = re.search(rf"(https?://[^\s<]+{re.escape(pattern)}[^\s<]*)", sitemap_text)
                        if match:
                            doc_url = match.group(1)
                            log(f"#{hospital_no} Sitemap fallback: {doc_url}")
                            await page.goto(doc_url, wait_until="domcontentloaded", timeout=15000)
                            doctor_page_found = True
                            break
                except Exception:
                    pass

            # Step 5c: Main page fallback (independent try block)
            if not doctor_page_found:
                try:
                    await page.goto(url, wait_until="domcontentloaded", timeout=15000)
                    log(f"#{hospital_no} Main page fallback for doctor extraction")
                except Exception:
                    pass

            # ---------------------------------------------------------------
            # Step 6: Extract Doctor Information
            # ---------------------------------------------------------------
            # Scroll page to trigger lazy loading (imweb CMS etc.)
            # Use page-level waits between scrolls so the browser actually
            # fires IntersectionObserver / scroll events that load content.
            # IMPORTANT: Do NOT scroll back to top — imweb unloads content
            # when sections leave the viewport (bidirectional lazy loading).
            try:
                for _ in range(10):
                    await page.evaluate("window.scrollBy(0, 600)")
                    await page.wait_for_timeout(500)
                await page.wait_for_timeout(1000)
            except Exception:
                pass

            log(f"#{hospital_no} Extracting doctor info")
            try:
                # Check if page is image-based
                is_image_based = await page.evaluate(JS_CHECK_IMAGE_BASED)

                if not is_image_based:
                    # DOM extraction
                    doctors = await page.evaluate(JS_EXTRACT_DOCTORS)
                    result["doctors"] = doctors
                    log(f"#{hospital_no} Extracted {len(doctors)} doctors from DOM")
                else:
                    log(f"#{hospital_no} Image-based page detected, attempting OCR")
                    # Take screenshot for OCR
                    screenshot_path = f"/tmp/clinic_crawl_{hospital_no}_{int(time.time())}.jpg"
                    await page.screenshot(path=screenshot_path, full_page=False, type="jpeg", quality=85)

                    # Try Gemini CLI OCR
                    try:
                        ocr_result = subprocess.run(
                            ["gemini", "-p",
                             f"Read the image file at {screenshot_path}. "
                             "Extract doctor/medical staff information in JSON format. "
                             "Return a JSON array where each item has: name, role, credentials (array), "
                             "education (array), career (array). Only return the JSON, nothing else.",
                             "-y"],
                            capture_output=True, text=True, timeout=60,
                        )
                        if ocr_result.returncode == 0:
                            ocr_text = ocr_result.stdout
                            # Multi-strategy JSON parse
                            json_match = re.search(r"```(?:json)?\s*(\[[\s\S]*?\])\s*```", ocr_text)
                            if json_match:
                                doctors_raw = json.loads(json_match.group(1))
                            else:
                                json_match = re.search(r"\[[\s\S]*\]", ocr_text)
                                if json_match:
                                    doctors_raw = json.loads(json_match.group(0))
                                else:
                                    doctors_raw = []

                            for doc in doctors_raw:
                                if not doc.get("name") or len(doc["name"]) < 2:
                                    continue
                                result["doctors"].append({
                                    "name": doc.get("name", ""),
                                    "name_english": "",
                                    "role": doc.get("role", "specialist"),
                                    "photo_url": "",
                                    "education": doc.get("education", []),
                                    "career": doc.get("career", []),
                                    "credentials": doc.get("credentials", []),
                                    "branch": "",
                                    "branches": [],
                                    "extraction_source": "ocr",
                                    "ocr_source": True,
                                })
                            log(f"#{hospital_no} OCR extracted {len(result['doctors'])} doctors")
                        else:
                            log(f"#{hospital_no} Gemini CLI error: {ocr_result.stderr[:200]}")
                            result["errors"].append({
                                "type": "ocr_error", "message": ocr_result.stderr[:200],
                                "step": "doctor_ocr", "retryable": True,
                            })
                    except FileNotFoundError:
                        log(f"#{hospital_no} Gemini CLI not installed, skipping OCR")
                        result["errors"].append({
                            "type": "ocr_unavailable", "message": "Gemini CLI not installed",
                            "step": "doctor_ocr", "retryable": False,
                        })
                    except subprocess.TimeoutExpired:
                        log(f"#{hospital_no} Gemini CLI timeout")
                        result["errors"].append({
                            "type": "ocr_timeout", "message": "Gemini CLI timed out",
                            "step": "doctor_ocr", "retryable": True,
                        })
                    finally:
                        # Cleanup screenshot
                        try:
                            os.remove(screenshot_path)
                        except OSError:
                            pass

            except Exception as e:
                result["errors"].append({"type": "extraction", "message": str(e)[:200], "step": "doctor_extract", "retryable": True})

            # Determine final status
            has_social = len(result["social_channels"]) > 0
            has_doctors = len(result["doctors"]) > 0

            # Track whether a doctor page exists on this site
            result["doctor_page_exists"] = 1 if (doctor_page_found or has_doctors) else 0

            if result["status"] == "success":
                if has_social and has_doctors:
                    pass  # success: both categories have data
                elif has_social or has_doctors:
                    result["status"] = "partial"  # only one category
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
