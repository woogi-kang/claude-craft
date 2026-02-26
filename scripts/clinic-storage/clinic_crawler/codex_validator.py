"""Codex CLI-based doctor profile validator.

Calls `codex exec` with gpt-5.3-codex to filter noise from
extracted profile_raw arrays, judge whether a page actually
contains real doctor credential information, and filter doctors
by branch for chain hospitals.
"""

import json
import os
import subprocess
import tempfile
from collections import defaultdict
from pathlib import Path

from .constants import DOCTOR_ROLES_KEEP
from .korean_name import is_plausible_korean_name
from .log import log

# Codex CLI settings (configurable via env vars)
CODEX_MODEL = os.environ.get("CLINIC_CODEX_MODEL", "gpt-5.3-codex-spark")
CODEX_REASONING = os.environ.get("CLINIC_CODEX_REASONING", "xhigh")
CODEX_TIMEOUT = int(os.environ.get("CLINIC_CODEX_TIMEOUT", "120"))

VALIDATE_PROMPT = """\
You are a Korean dermatology clinic data validator.
Read {input_path}.

Hospital name: {hospital_name}

Each doctor object has: "name", "role" (medical title), and "profile_raw" (credential list).

For each doctor object, filter profile_raw to keep ONLY actual professional credentials:
- Education: 학력, 졸업, 석사, 박사, 대학, 수료
- Career: 경력, 원장, 근무, 전공의, 수련, 과장, 교수, 연구원
- Certifications: 학회, 정회원, 인증, 전문의, 자격, 수상

Remove ALL noise: generic service names (피부과 진료, 레이저 클리닉, 쁘띠클리닉 etc),
marketing text, navigation, footer, intro sentences, addresses, phone numbers,
hospital descriptions, treatment descriptions.

NAME VALIDATION:
Check if each "name" is a real Korean person name (2-4 Korean syllables, surname + given name).
Set is_valid=false for names that are:
- Brand names (e.g. 차앤유, 유튜브)
- Common words (e.g. 고객, 안녕하)
- Sentence fragments or truncated words
- Duplicate/truncated versions of another doctor's name (e.g. 김석 when 김석준 exists)

CREDENTIAL DEDUP:
If multiple doctors share the EXACT SAME credential list, only the first is likely real.
Mark duplicates as is_valid=false.

CROSS-CONTAMINATION DETECTION:
If a single doctor has credentials from MULTIPLE different people (different universities,
different hospital careers that cannot belong to one person), the profile_raw is contaminated.
Signs of cross-contamination:
- Multiple different university graduations (e.g. 한양대 졸업 AND 서울대 졸업 AND 고려대 졸업)
- Multiple "전문의 수료" from different hospitals
- Credential count exceeding 20 items for a single doctor
When detected, keep ONLY the credentials that logically belong to ONE person (the first
coherent group), and discard the rest.

BRANCH FILTERING (chain hospitals):
This rule applies ONLY when the input data contains an EXPLICIT "branches" array
with branch location labels (e.g. ["구로점", "강남점"]) on individual doctors.
Do NOT infer branch information from credentials, career history, or hospital names.
For example, "(전) 블리비의원 강남역점 원장" is a CAREER ITEM, not a branch tag.
If no doctor in the input has a non-empty "branches" array, treat this as a
single-location clinic and keep ALL doctors — do not filter by branch.
If explicit branch tags exist, extract the branch name from the hospital name
and keep only doctors whose "branches" array contains a matching branch.

Write result as JSON to {output_path} in this exact format:
[{{"name":"...","valid_items":[...],"is_valid":true/false,"branch":"..."}}]

is_valid RULES (check the "role" field in the input):
- true if the name is a real Korean person name AND the "role" field contains
  a medical title (원장, 대표원장, 부원장, 전문의, 의사, specialist)
- true if the name is valid AND 2+ meaningful credential items exist
- false if the name is not a real Korean person name (brand, word fragment, etc.)
- false if no medical role in "role" field AND fewer than 2 credentials

IMPORTANT: In Korean clinics, it is NORMAL for non-lead doctors to have only
name + role without detailed credentials. Only the head doctor (대표원장)
typically lists full education/career history. A doctor with name="정진이"
and role="원장" but empty profile_raw is VALID — do NOT reject them.

"branch" is optional — include only if a branch tag was detected.
Output ONLY the JSON file, no other files or explanations.\
"""


def validate_doctors(doctors: list, place_id: str, hospital_name: str = "") -> tuple[list, bool]:
    """Validate extracted doctors via Codex CLI.

    Args:
        doctors: List of doctor dicts with profile_raw arrays.
        place_id: Hospital identifier for logging.
        hospital_name: Hospital name for chain branch filtering.

    Returns:
        (filtered_doctors, any_valid): Doctors with cleaned profile_raw,
        and whether any doctor had valid credentials.
    """
    if not doctors:
        return doctors, False

    # Prepare input: only send name + profile_raw to minimize tokens
    input_data = [
        {"name": d.get("name", ""), "role": d.get("role", ""), "profile_raw": d.get("profile_raw", [])}
        for d in doctors
    ]

    # If all profile_raw are empty, skip Codex but keep doctors with valid
    # name+role as "no_credentials" — OCR fallback will be attempted too,
    # and the best result (more credentials) wins in step_extract_doctors.
    if all(len(d["profile_raw"]) == 0 for d in input_data):
        return doctors, False

    input_path = None
    output_path = None
    try:
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".json", prefix="codex_in_", delete=False, dir="/tmp"
        ) as f_in:
            json.dump(input_data, f_in, ensure_ascii=False)
            input_path = f_in.name

        output_path = input_path.replace("codex_in_", "codex_out_", 1)

        safe_name = (hospital_name or "Unknown").replace("{", "").replace("}", "")
        prompt = VALIDATE_PROMPT.format(
            input_path=input_path,
            output_path=output_path,
            hospital_name=safe_name,
        )

        result = subprocess.run(
            [
                "codex", "exec",
                "-m", CODEX_MODEL,
                "-c", f'model_reasoning_effort="{CODEX_REASONING}"',
                "--full-auto",
                "--skip-git-repo-check",
                "--ephemeral",
                prompt,
            ],
            capture_output=True,
            text=True,
            timeout=CODEX_TIMEOUT,
            cwd="/tmp",
        )

        if result.returncode != 0:
            log(f"[{place_id}] Codex validator error: {result.stderr[:200]}")
            return [], False

        # Read validation result
        out_path = Path(output_path)
        if not out_path.exists():
            log(f"[{place_id}] Codex output not found at {output_path}")
            return [], False

        with open(out_path, encoding="utf-8") as f:
            validated = json.load(f)

        # Validate output structure
        if not isinstance(validated, list):
            log(f"[{place_id}] Codex returned non-list JSON, skipping")
            return [], False

        # Merge by index when lengths match (safer than name-based lookup)
        if len(validated) == len(doctors):
            filtered = []
            for doc, v in zip(doctors, validated):
                if v.get("is_valid", False):
                    doc["profile_raw"] = v.get("valid_items", doc.get("profile_raw", []))
                    if v.get("branch"):
                        doc["branch"] = v["branch"]
                    filtered.append(doc)
        else:
            # Fallback: name-based lookup with collision handling
            valid_map = defaultdict(list)
            for v in validated:
                valid_map[v.get("name", "")].append(v)

            filtered = []
            for doc in doctors:
                name = doc.get("name", "")
                entries = valid_map.get(name, [])
                v = entries.pop(0) if entries else None
                if v and v.get("is_valid", False):
                    doc["profile_raw"] = v.get("valid_items", doc.get("profile_raw", []))
                    if v.get("branch"):
                        doc["branch"] = v["branch"]
                    filtered.append(doc)

        # Recover doctors with valid Korean name + medical role that Codex
        # wrongly rejected (LLM inconsistency — same input pattern gets
        # different is_valid results across doctors).
        filtered_keys = {(d.get("name", ""), d.get("role", "")) for d in filtered}
        recovered = 0
        for doc in doctors:
            name = doc.get("name", "")
            role = doc.get("role", "")
            if (name, role) in filtered_keys:
                continue
            if is_plausible_korean_name(name) and role in DOCTOR_ROLES_KEEP:
                doc["profile_raw"] = []
                filtered.append(doc)
                recovered += 1

        valid_count = sum(1 for v in validated if v.get("is_valid", False))
        log(f"[{place_id}] Codex validated: {valid_count}/{len(doctors)} doctors have real credentials")
        if recovered:
            log(f"[{place_id}] Recovered {recovered} doctors with valid name+role rejected by Codex")

        return filtered, len(filtered) > 0

    except subprocess.TimeoutExpired:
        log(f"[{place_id}] Codex validator timeout ({CODEX_TIMEOUT}s) — falling back to OCR")
        return [], False
    except Exception as e:
        log(f"[{place_id}] Codex validator exception: {e}")
        return [], False
    finally:
        # Keep temp files for debugging (last run only)
        for old in Path("/tmp").glob("codex_debug_*.json"):
            old.unlink(missing_ok=True)
        if input_path and Path(input_path).exists():
            Path(input_path).rename(f"/tmp/codex_debug_in_{place_id}.json")
        if output_path and Path(output_path).exists():
            Path(output_path).rename(f"/tmp/codex_debug_out_{place_id}.json")
