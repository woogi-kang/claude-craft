"""OCR parsing helpers for doctor extraction from image-based pages."""

import json
import os
import re
import subprocess

# Gemini model for OCR and AI navigation
GEMINI_MODEL = "gemini-3-flash-preview"

# Prompt template for Gemini OCR doctor extraction
OCR_PROMPT_TEMPLATE = (
    "Read the image file at {path}.\n\n"
    "This is a screenshot from a Korean dermatology/skin clinic website's "
    "doctor introduction page (의료진 소개).\n\n"
    "Extract ONLY doctor/physician information. Look for:\n"
    "- Names: 2-3 Korean characters (한글). Common surnames: "
    "김,이,박,최,정,강,조,윤,장,임,한,오,서,신,권,황,안,송,류,전,홍\n"
    "- Titles: 대표원장, 원장, 부원장, 전문의, 피부과전문의\n"
    "- Education: contains 대학교, 졸업, 수료, 석사, 박사, 의학전문대학원\n"
    "- Career (약력/경력/이력): contains 병원, 의원, 클리닉, 센터, 수련, "
    "전공의, 레지던트, 前, 전임, 근무, 과장, 진료, 외래, 파견, "
    "연구원, 펠로우, 교수, 조교수, 부교수, 강사\n"
    "- Credentials: contains 학회, 정회원, 전문의, 자격, 인증\n\n"
    "IMPORTANT: Look for sections labeled 약력, 경력, 이력, 프로필 - "
    "these contain career information.\n"
    "Lines starting with 前 or 전) mean 'former' and indicate career history.\n\n"
    "IGNORE: navigation menus, hospital name/address/phone, "
    "nurses (간호사), coordinators (코디네이터), consultants (상담사).\n\n"
    "Return ONLY a valid JSON array. No explanation, no markdown fences.\n"
    "Each item: {{\"name\":\"...\",\"role\":\"...\","
    "\"profile_raw\":[...all education, career, credentials lines merged...]}}\n"
    "If no doctors found, return: []"
)


def parse_ocr_json(text: str) -> list:
    """Parse JSON array from Gemini OCR output with robust fallback."""
    if not text or not text.strip():
        return []

    # Strategy 1: Extract from markdown code fences
    json_match = re.search(r"```(?:json)?\s*(\[[\s\S]*?\])\s*```", text)
    if json_match:
        try:
            return json.loads(json_match.group(1))
        except json.JSONDecodeError:
            pass

    # Strategy 2: Find shortest valid JSON array
    json_match = re.search(r"\[[\s\S]*?\]", text)
    if json_match:
        try:
            return json.loads(json_match.group(0))
        except json.JSONDecodeError:
            pass

    # Strategy 3: Find longest valid JSON array (greedy, then shrink)
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


def run_gemini_ocr(prompt: str, image_path: str) -> list:
    """Run Gemini CLI with image via --include-directories for vision mode."""
    image_dir = os.path.dirname(image_path)
    r = subprocess.run(
        ["gemini", "-m", GEMINI_MODEL, "-p", prompt,
         "-y", "--include-directories", image_dir],
        capture_output=True, text=True, timeout=90,
    )
    if r.returncode == 0:
        return parse_ocr_json(r.stdout)
    return []


def append_ocr_doctors(doctors_raw: list, seen_names: set, result_doctors: list) -> int:
    """Append unique OCR doctors to result list. Returns count added."""
    added = 0
    for doc in doctors_raw:
        name = doc.get("name", "")
        if name and len(name) >= 2 and name not in seen_names:
            seen_names.add(name)
            # Merge profile_raw from either unified or legacy format
            profile_raw = doc.get("profile_raw") or []
            if not profile_raw:
                edu = doc.get("education") or []
                career = doc.get("career") or []
                creds = doc.get("credentials") or []
                profile_raw = edu + career + creds
            result_doctors.append({
                "name": name, "name_english": "",
                "role": doc.get("role", "specialist"),
                "photo_url": "",
                "profile_raw": profile_raw,
                "page_text": "",
                "source_url": "",
                "screenshot_path": "",
                "branch": "", "branches": [],
                "extraction_source": "ocr", "ocr_source": True,
            })
            added += 1
    return added
