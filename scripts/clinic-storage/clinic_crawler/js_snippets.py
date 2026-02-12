"""JavaScript snippets injected via page.evaluate() during browser crawling.

Each constant is a string containing a JavaScript function body.
These are used by both MCP mode (Mode 1) and Python Playwright mode (Mode 2).
"""

JS_SOCIAL_EXTRACT = """
() => {
    const results = [];
    const seen = new Set();

    function normalizeUrl(u) {
        if (u.startsWith('tel:') || u.startsWith('sms:')) {
            return u.substring(0, 4) + u.substring(4).replace(/[-.\\s()+]/g, '');
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
        const phones = text.match(/(?:0\\d{1,2})[-.\\s]?\\d{3,4}[-.\\s]?\\d{4}/g);
        if (phones) phones.forEach(p => addResult('Phone', 'tel:' + p.replace(/[-.\\s]/g,''), 'maps_embed'));
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
                    addResult('Phone', 'tel:' + item.contactPoint.telephone.replace(/[-.\\s]/g,''), 'structured_data');
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
    const phoneMatches = bodyText.match(/(?:0\\d{1,2})[-.\\s]?\\d{3,4}[-.\\s]?\\d{4}/g);
    if (phoneMatches) {
        // Only add first 3 unique phones (avoid noise)
        const phoneSet = new Set();
        phoneMatches.forEach(p => {
            const normalized = p.replace(/[-.\\s]/g, '');
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
            const isIntroParent = /.\\s*소개$/.test(parentText);
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
# Inline JS extracted from crawl_single.py (Phase 3)
# ---------------------------------------------------------------------------

JS_SPLASH_DETECT = """
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
"""

JS_REDIRECT_SCAN = """
() => {
    const keywords = /kakao|\uCE74\uCE74\uC624|naver|\uB124\uC774\uBC84|blog|\uBE14\uB85C\uADF8|instagram|\uC778\uC2A4\uD0C0|youtube|\uC720\uD29C\uBE0C|facebook|\uD398\uC774\uC2A4\uBD81|line|\uB77C\uC778|talk|\uD1A1/i;
    const links = [];
    document.querySelectorAll('a[href], area[href]').forEach(el => {
        const href = el.href || el.getAttribute('href') || '';
        const text = (el.textContent || '').trim();
        const alt = el.querySelector('img')?.alt || '';
        const title = el.getAttribute('title') || '';
        const combined = text + ' ' + alt + ' ' + title;
        if (!href) return;
        const isInternal = href.startsWith('/') || href.includes(location.hostname) ||
            /\\.(asp|php|jsp|do|html?)\\?/.test(href);
        const hasSocialKeyword = keywords.test(combined) || keywords.test(href);
        const alreadySocial = /kakao\\.com|instagram\\.com|youtube\\.com|naver\\.com|facebook\\.com|line\\.me/.test(href);
        if (isInternal && hasSocialKeyword && !alreadySocial && href.length < 300) {
            links.push({href: href, text: combined.substring(0, 50)});
        }
    });
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
                    /\\.(asp|php|jsp|do|html?)\\?/.test(href);
                const hasSocialKeyword = keywords.test(combined) || keywords.test(href);
                const alreadySocial = /kakao\\.com|instagram\\.com|youtube\\.com|naver\\.com|facebook\\.com|line\\.me/.test(href);
                if (isInternal && hasSocialKeyword && !alreadySocial && href.length < 300) {
                    links.push({href: href, text: combined.substring(0, 50)});
                }
            });
        } catch(e) {}
    });
    const seen = new Set();
    return links.filter(l => { if (seen.has(l.href)) return false; seen.add(l.href); return true; });
}
"""

JS_REVEAL_SUBMENUS = """
() => {
    const parents = document.querySelectorAll(
        'nav > ul > li, .gnb > li, .menu > li, [class*="nav"] > ul > li, header li'
    );
    parents.forEach(li => {
        li.dispatchEvent(new MouseEvent('mouseenter', {bubbles: true}));
        li.dispatchEvent(new MouseEvent('mouseover', {bubbles: true}));
    });
}
"""

JS_FIND_INTRO_LINKS = """
() => {
    const kw = ['\uC18C\uAC1C', 'about', 'intro'];
    return Array.from(document.querySelectorAll('a[href]'))
        .filter(a => {
            const text = (a.textContent || '').trim().toLowerCase();
            const href = (a.href || '').toLowerCase();
            return text.length < 20 && kw.some(k => text.includes(k) || href.includes(k));
        })
        .map(a => ({text: a.textContent.trim(), href: a.href}))
        .filter(l => l.href && !l.href.includes('#'))
        .slice(0, 5);
}
"""

JS_FIND_DOCTOR_SUBLINKS = """
() => {
    const docKw = ['\uC758\uB8CC\uC9C4', '\uC6D0\uC7A5', '\uC804\uBB38\uC758', 'doctor', 'staff', 'team'];
    return Array.from(document.querySelectorAll('a[href]'))
        .filter(a => {
            const text = (a.textContent || '').trim().toLowerCase();
            const href = (a.href || '').toLowerCase();
            return docKw.some(k => text.includes(k) || href.includes('/doctor') || href.includes('/staff') || href.includes('/team'));
        })
        .map(a => ({text: a.textContent.trim(), href: a.href}))
        .slice(0, 3);
}
"""

JS_FIND_DOCTOR_TABS = """
() => {
    const tabEls = document.querySelectorAll(
        '[role="tab"], .tab-link, .tabs > *, .tab-item, [class*="tab"] a, [class*="tab"] button'
    );
    const kw = ['\uC758\uB8CC\uC9C4', '\uC6D0\uC7A5', '\uC804\uBB38\uC758', '\uB300\uD45C', 'doctor', 'staff', '\uC18C\uAC1C'];
    return Array.from(tabEls)
        .filter(t => {
            const txt = (t.textContent || '').trim().toLowerCase();
            return txt.length < 20 && kw.some(k => txt.includes(k));
        })
        .map(t => (t.textContent || '').trim())
        .slice(0, 5);
}
"""
