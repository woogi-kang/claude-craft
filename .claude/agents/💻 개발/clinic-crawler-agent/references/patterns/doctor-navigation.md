# Doctor Page Navigation Patterns

Reference data for finding and extracting doctor/medical staff information from Korean clinic websites.

## Menu Labels

### Primary (exact match preferred)
- Korean: `의료진`, `의료진 소개`, `의료진소개`, `원장 소개`, `원장소개`, `전문의 소개`, `전문의소개`
- English: `DOCTOR`, `Doctor`, `Our Doctors`, `Medical Staff`

### Secondary (fallback)
- Korean: `원장님`, `대표원장`, `의료팀`, `진료진`, `진료 안내`, `클리닉 소개`
- English: `Staff`, `Team`, `About Us`

### Submenu Parents (expand first, then look for doctor items)
- Korean: `병원 소개`, `클리닉 소개`, `소개`, `병원 안내`, `클리닉 안내`
- English: `About`

## URL Patterns

Common doctor page URL segments:
- `/doctor`, `/doctors`, `/staff`, `/team`
- `/about`, `/introduce`
- `/sub/doctor`, `/page/doctor`, `/contents/doctor`

## Content Selectors

### Doctor Card Containers
- `.doctor-card`, `.doctor-item`, `.staff-item`
- `.team-member`, `.doctor-info`
- `.doctor-list > li`, `.staff-list > li`

### Doctor Name
- `.doctor-name`, `.staff-name`
- `.doctor-card h3`, `.doctor-card h4`
- `.name`

### Doctor Photo
- `.doctor-photo img`, `.doctor-img img`
- `.staff-photo img`, `.doctor-card img`
- `.team-member img`
- **CSS background-image fallback**:
  ```javascript
  document.querySelectorAll('[class*="photo"], [class*="image"], [class*="avatar"]').forEach(el => {
    const bg = getComputedStyle(el).backgroundImage;
    if (bg && bg !== 'none') { /* extract url() */ }
  });
  ```

### Credentials
- `.doctor-career`, `.doctor-history`
- `.career-list`, `.credentials`
- `.doctor-card ul`

## Extraction Flow

1. Scan navigation menu for primary labels
2. If not found, check secondary labels
3. If found inside submenu parent, expand parent first then click
4. After navigation, wait for page load (check for doctor-related content)
5. **AJAX detection**: If URL unchanged but DOM changed, doctor page loaded via AJAX
6. **Login wall check**: If `[type="password"]` or "회원"/"로그인" text detected, skip extraction
7. Extract using content selectors
8. If selectors fail (image-based page), trigger Gemini OCR workflow

### No Doctor Menu Fallback
If no menu label matches after all primary/secondary/submenu checks:

1. **Sitemap check** (try first):
   - Navigate to `{base_url}/sitemap.xml`
   - Parse for URLs matching: `/doctor`, `/staff`, `/team`, `/about`, `/introduce`, `/의료진`, `/원장`
   - Navigate to first matching URL, attempt extraction
   - Record `extraction_source: "sitemap"`

2. **Main page scan** (if sitemap fails):
   - Return to homepage
   - Scan for doctor content on main page (hero, about, team sections)
   - Check URL for doctor-like segments (`/about`, `/introduce`)
   - If single-doctor clinic, extract from main page with `extraction_source: "main_page"`

## UI Pattern Detection (Pre-Extraction)

Before extracting doctor data, detect and handle these UI patterns:

### Tabs / Accordion
- Detect: `[role="tab"]`, `[role="tabpanel"]`, `.accordion-item`, `.tab-pane`
- For each collapsed tab/section:
  1. Check `aria-selected="false"` or `display: none`
  2. `browser_click` on tab header
  3. Wait for content reveal (1000ms)
  4. Extract doctor info from expanded section

### Slider / Carousel
- Detect: `[class*="swiper"]`, `[class*="carousel"]`, `[class*="slider"]`
- For each slide:
  1. Extract visible doctors
  2. Click next arrow/dot
  3. Wait for slide transition (2000ms)
  4. Extract newly visible doctors
  5. Stop when returning to first slide or no new doctors

### Separate Profile Pages (One Page Per Doctor)
- Detect: Doctor list page shows names as clickable links (few text items, many `<a>` elements)
- For each doctor link:
  1. Record link URL
  2. `browser_click` to navigate to profile page
  3. Extract full doctor info from dedicated page
  4. Navigate back to list page
  5. Repeat for remaining links

### Expandable Content ("더보기" / "Read More")
- Detect: Buttons/links with text "더보기", "read more", "expand", "show more"
- For each expandable section:
  1. Check adjacent hidden element (`display: none`, `max-height: 0`)
  2. `browser_click` on expand button
  3. Wait for content reveal (1000ms)
  4. Re-extract credentials/career from expanded content

## Name Parsing and Staff Filtering

### Korean Honorific Separation
Raw text like "박미래 원장" should be split:
```
Pattern: (name) (honorific/role)
Regex: ^(.+?)\s+(원장|대표원장|부원장|전문의|의사|레지던트|인턴)$
Result: name = "박미래", role = "원장"
```

### Staff Role Filtering
**Keep** (doctor roles):
- 원장, 대표원장, 부원장, 전문의, 의사, 레지던트, 인턴

**Exclude** (non-doctor roles):
- 간호사, 간호조무사, 피부관리사, 상담사, 코디네이터, 스텝, 직원

If role field is empty, parse name/title text for keywords to classify.

### Credential Splitting
When credentials are on a single line with mixed separators:
1. Detect primary separator (most frequent: `/` vs `,` vs `•`)
2. Split by detected separator
3. Classify each item:
   - **Education**: contains 대학, 학위, 졸업, 수료
   - **Career**: contains 병원, 클리닉, 근무, 전공의
   - **Credentials**: contains 정회원, 학회, 자격, 인증, 협회

## Multi-Branch Site Handling

For chain hospitals with multiple branches on one site:

### Detection
- Site shows branch selector, tabs, or dropdown
- Multiple addresses/phone numbers visible
- URL contains branch identifier (e.g., `/hanam/`, `?branch=gangnam`)

### Branch Matching Strategy
1. Extract target hospital address city/district (e.g., "하남" from "경기도 하남시...")
2. Look for branch navigation elements:
   - Tabs: `browser_evaluate` -> `document.querySelectorAll('[role="tab"], .branch-tab, .location-tab')`
   - Dropdown: `select` elements with branch names
   - Links: navigation items with city/district names
3. Click matching branch tab/link
4. Wait for content update
5. Extract doctor info for the selected branch only
6. Record `branch` field in doctor result

### Fallback
- If no branch selector found, extract all doctors and note `branch: "unknown"`
- Include hospital address in result for manual matching

## Pagination Handling

After extracting doctors from the current page:

### Detection
Look for pagination elements:
- Numbered pages: `.pagination a`, `.paging a`, `[class*="page"] a`
- Next button: text containing `다음`, `next`, `>`
- Load more: text containing `더보기`, `more`, `load more`
- Infinite scroll: `browser_evaluate` -> check `document.body.scrollHeight > window.innerHeight`

### Extraction Loop
1. Extract doctors from current page
2. Check for next page / load more button
3. If found:
   - Click next page or load more
   - `browser_wait_for` content change (new doctor cards appearing)
   - Extract additional doctors
4. Repeat until:
   - No more pagination elements
   - Same content detected (no new doctors)
   - Max 5 pages reached
5. Merge all extracted doctors (de-duplicate by name)
