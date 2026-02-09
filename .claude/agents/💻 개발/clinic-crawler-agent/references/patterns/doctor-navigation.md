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
