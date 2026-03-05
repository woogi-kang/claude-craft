# Clinic Crawler Edge Cases

Known limitations and difficult sites for future improvement.

## Category: No Doctor Profile Page

Sites where no doctor credentials (education/career/certifications) exist anywhere on the site.
The doctor's name may be found, but no profile page or credential information is available.

### hana-skin.com (김동준피부과, place_id: 12048920)

- **URL**: http://www.hana-skin.com/
- **Status**: success (name found, credentials missing)
- **Issue**: Site has only a greeting from 김동준 원장 + treatment images. No 의료진 소개 menu. No credentials in any text or image.
- **Pages checked**:
  - `/#1` (병원소개): Doctor photo + greeting text only
  - `/hayannara-skingroup/`: Group intro image, no individual credentials
- **OCR viable**: No. Images contain no credential information.
- **Resolution**: Accept as partial — name extractable, credentials unavailable on site.

## Category: Hidden Submenu (CSS Dropdown Not Detected)

Sites where doctor profile page exists but is hidden behind CSS hover dropdown
that the crawler's `JS_REVEAL_SUBMENUS` fails to trigger.

### reachmi.co.kr (리치미의원, place_id: 12929433)

- **URL**: http://reachmi.co.kr/
- **Status**: success (name found, credentials are news articles not real credentials)
- **Issue**: Doctor profile page exists at `/?mir_code=1148` (의료진소개) with full credentials as image. But the link is hidden in CSS dropdown under "리치미클리닉 소개" parent menu. `JS_REVEAL_SUBMENUS` mouseenter/mouseover does not trigger the "오토메디" CMS dropdown, so the crawler never discovers `mir_code=1148`.
- **Doctor profile page**: `/?mir_code=1148` — full image-based profile with:
  - 대표약력: 서울대학교 의대 졸업, 서울대학교 병원 전문의
  - 학회/인증: KCS 정회원, IMCAS, 스컬트라 MASTERS TOP 10, ELLANSE Key Doctor
  - 학회 정회원: 대한미용피부외과학회, 한국타운성형학회(KCCS)
- **OCR viable**: Yes. Full credentials visible in page image.
- **Root cause**: `JS_REVEAL_SUBMENUS` dispatches mouseenter/mouseover on `nav > ul > li` etc., but this CMS uses a different menu activation pattern. The submenu `의료진소개` link is not in initial DOM or not matched by current selectors.
- **Fix needed**: Improve submenu discovery — try clicking parent menu items, or scan for sequential `mir_code` URLs (1147 -> 1148), or use Gemini AI navigation to find hidden submenus.
