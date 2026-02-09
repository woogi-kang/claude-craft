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

### Credentials
- `.doctor-career`, `.doctor-history`
- `.career-list`, `.credentials`
- `.doctor-card ul`

## Extraction Flow

1. Scan navigation menu for primary labels
2. If not found, check secondary labels
3. If found inside submenu parent, expand parent first then click
4. After navigation, wait for page load (check for doctor-related content)
5. Extract using content selectors
6. If selectors fail (image-based page), trigger Gemini OCR workflow

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
