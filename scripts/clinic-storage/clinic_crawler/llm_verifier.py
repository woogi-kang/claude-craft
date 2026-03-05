"""LLM-based doctor verification using Gemini Flash.

After DOM extraction generates candidate doctors, this module sends the
candidate list + page screenshot to Gemini for visual verification.
The LLM sees the actual page and confirms which names are real doctors
vs. noise (navigation text, marketing copy, credential fragments).

This replaces blocklist-based filtering as the primary defense against
false positives, while blocklists remain as a fast pre-filter.
"""

import json
import os
import re
import subprocess
import tempfile

from .log import log

GEMINI_MODEL = os.environ.get("CLINIC_GEMINI_MODEL", "gemini-3-flash-preview")
GEMINI_TIMEOUT = int(os.environ.get("CLINIC_GEMINI_VERIFY_TIMEOUT", "60"))

VERIFY_PROMPT = """\
You are a Korean dermatology clinic data validator.

I extracted these doctor candidates from a clinic website page.
The screenshot of that page is included as {screenshot_path}.

Candidates:
{candidates_json}

For each candidate, determine if it is a REAL doctor on this page:

REAL doctor criteria (is_valid=true):
- The name appears on the page as a doctor/physician name
- The name is 2-4 Korean characters with a valid Korean surname
- The name is associated with a medical title (원장, 대표원장, 부원장, 전문의, 의사)

FALSE POSITIVE criteria (is_valid=false):
- Navigation menu text, UI labels (전체, 더보기, 이전, 다음)
- Common Korean words (한국, 이력, 방문, 전국, 공동, 안심, etc.)
- Credential fragments (한민국 from 대한민국, 원부 from 부원장, etc.)
- Brand names, clinic names, marketing text
- Location names (강남, 서초, 홍대, etc.)
- Customer-facing text (고객님, 상담, 예약, etc.)

Return ONLY a valid JSON array. No explanation, no markdown fences.
Each item: {{"name":"...","is_valid":true/false,"reason":"brief reason"}}
If unsure, set is_valid=false.
"""


def verify_doctors_with_llm(
    candidates: list,
    screenshot_path: str,
    place_id: str,
) -> list:
    """Verify DOM-extracted doctor candidates using Gemini Flash + screenshot.

    Args:
        candidates: List of doctor dicts from DOM extraction.
        screenshot_path: Path to the page screenshot for visual context.
        place_id: Hospital identifier for logging.

    Returns:
        Filtered list of verified doctors.
    """
    if not candidates:
        return candidates

    if not screenshot_path or not os.path.exists(screenshot_path):
        log(f"[{place_id}] LLM verify: no screenshot, skipping")
        return candidates

    # Prepare candidate summary for the prompt
    cand_summary = [
        {"name": d.get("name", ""), "role": d.get("role", "")}
        for d in candidates
    ]

    prompt = VERIFY_PROMPT.format(
        screenshot_path=os.path.basename(screenshot_path),
        candidates_json=json.dumps(cand_summary, ensure_ascii=False, indent=2),
    )

    try:
        image_dir = os.path.dirname(screenshot_path)
        result = subprocess.run(
            ["gemini", "-m", GEMINI_MODEL, "-p", prompt,
             "-y", "--include-directories", image_dir],
            capture_output=True, text=True, timeout=GEMINI_TIMEOUT,
        )

        if result.returncode != 0:
            log(f"[{place_id}] LLM verify: Gemini error, keeping all candidates")
            return candidates

        verified = _parse_verification(result.stdout)
        if not verified:
            log(f"[{place_id}] LLM verify: parse failed, keeping all candidates. "
                f"Raw output length={len(result.stdout)}")
            return candidates

        # Build explicit rejection map (only reject names the LLM
        # explicitly marked is_valid=false; keep unmentioned names)
        explicitly_invalid = {}
        explicitly_valid = set()
        for v in verified:
            name = v.get("name", "")
            if v.get("is_valid", False):
                explicitly_valid.add(name)
            else:
                explicitly_invalid[name] = v.get("reason", "unknown")

        # Filter: remove only explicitly rejected names
        filtered = [
            d for d in candidates
            if d.get("name", "") not in explicitly_invalid
        ]

        rejected_count = len(candidates) - len(filtered)
        unmentioned = [
            d.get("name", "") for d in candidates
            if d.get("name", "") not in explicitly_valid
            and d.get("name", "") not in explicitly_invalid
        ]

        if rejected_count > 0:
            rejected_names = [
                d.get("name", "") for d in candidates
                if d.get("name", "") in explicitly_invalid
            ]
            log(f"[{place_id}] LLM verify: rejected {rejected_count} "
                f"candidates: {rejected_names}")
            for name in rejected_names:
                log(f"[{place_id}]   {name}: {explicitly_invalid[name]}")

        if unmentioned:
            log(f"[{place_id}] LLM verify: {len(unmentioned)} candidates "
                f"not in LLM output (kept): {unmentioned}")

        log(f"[{place_id}] LLM verify: {len(filtered)}/{len(candidates)} "
            f"candidates kept ({rejected_count} rejected, "
            f"{len(unmentioned)} unmentioned)")
        return filtered

    except subprocess.TimeoutExpired:
        log(f"[{place_id}] LLM verify: timeout ({GEMINI_TIMEOUT}s), "
            f"keeping all candidates")
        return candidates
    except Exception as e:
        log(f"[{place_id}] LLM verify: error {e}, keeping all candidates")
        return candidates


def _parse_verification(text: str) -> list:
    """Parse JSON array from Gemini verification output."""
    if not text or not text.strip():
        return []

    # Strategy 1: markdown fences
    m = re.search(r"```(?:json)?\s*(\[[\s\S]*?\])\s*```", text)
    if m:
        try:
            return json.loads(m.group(1))
        except json.JSONDecodeError:
            pass

    # Strategy 2: shortest JSON array
    m = re.search(r"\[[\s\S]*?\]", text)
    if m:
        try:
            return json.loads(m.group(0))
        except json.JSONDecodeError:
            pass

    # Strategy 3: longest JSON array
    m = re.search(r"\[[\s\S]*\]", text)
    if m:
        raw = m.group(0)
        for i in range(len(raw) - 1, 0, -1):
            if raw[i] == ']':
                try:
                    return json.loads(raw[:i + 1])
                except json.JSONDecodeError:
                    continue

    # Strategy 4: collect individual JSON objects line-by-line
    objects = []
    for obj_match in re.finditer(r'\{[^{}]*\}', text):
        try:
            obj = json.loads(obj_match.group(0))
            if "name" in obj and "is_valid" in obj:
                objects.append(obj)
        except json.JSONDecodeError:
            continue
    if objects:
        return objects

    return []
