"""Codex CLI-based doctor profile validator.

Calls `codex exec` with gpt-5.1-codex-mini to filter noise from
extracted profile_raw arrays and judge whether a page actually
contains real doctor credential information.
"""

import json
import subprocess
import tempfile
from pathlib import Path

from .log import log

# Codex CLI settings
CODEX_MODEL = "gpt-5.1-codex-mini"
CODEX_REASONING = "low"
CODEX_TIMEOUT = 60  # seconds

VALIDATE_PROMPT = """\
You are a Korean dermatology clinic data validator.
Read {input_path}.
For each doctor object, filter profile_raw to keep ONLY actual professional credentials:
- Education: 학력, 졸업, 석사, 박사, 대학, 수료
- Career: 경력, 원장, 근무, 전공의, 수련, 과장, 교수, 연구원
- Certifications: 학회, 정회원, 인증, 전문의, 자격, 수상

Remove ALL noise: generic service names (피부과 진료, 레이저 클리닉, 쁘띠클리닉 etc),
marketing text, navigation, footer, intro sentences, addresses, phone numbers,
hospital descriptions, treatment descriptions.

Write result as JSON to {output_path} in this exact format:
[{{"name":"...","valid_items":[...],"is_valid":true/false}}]

is_valid=true ONLY if 2+ meaningful credential items exist.
Output ONLY the JSON file, no other files or explanations.\
"""


def validate_doctors(doctors: list, place_id: str) -> tuple[list, bool]:
    """Validate extracted doctors via Codex CLI.

    Args:
        doctors: List of doctor dicts with profile_raw arrays.
        place_id: Hospital identifier for logging.

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

    # Skip validation if all profile_raw are empty
    if all(len(d["profile_raw"]) == 0 for d in input_data):
        return doctors, False

    try:
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".json", prefix="codex_in_", delete=False, dir="/tmp"
        ) as f_in:
            json.dump(input_data, f_in, ensure_ascii=False)
            input_path = f_in.name

        output_path = input_path.replace("codex_in_", "codex_out_")

        prompt = VALIDATE_PROMPT.format(input_path=input_path, output_path=output_path)

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
            return doctors, True  # On error, pass through

        # Read validation result
        out_path = Path(output_path)
        if not out_path.exists():
            log(f"[{place_id}] Codex output not found at {output_path}")
            return doctors, True

        with open(out_path, encoding="utf-8") as f:
            validated = json.load(f)

        # Build lookup by name
        valid_map = {}
        any_valid = False
        for v in validated:
            name = v.get("name", "")
            valid_map[name] = v
            if v.get("is_valid", False):
                any_valid = True

        # Apply validation results to original doctors
        filtered = []
        for doc in doctors:
            name = doc.get("name", "")
            v = valid_map.get(name)
            if v and v.get("is_valid", False):
                doc["profile_raw"] = v.get("valid_items", doc.get("profile_raw", []))
                filtered.append(doc)
            elif v and not v.get("is_valid", False):
                # Keep doctor but mark empty profile
                doc["profile_raw"] = v.get("valid_items", [])
                filtered.append(doc)

        valid_count = sum(1 for v in validated if v.get("is_valid", False))
        log(f"[{place_id}] Codex validated: {valid_count}/{len(doctors)} doctors have real credentials")

        # Cleanup temp files
        Path(input_path).unlink(missing_ok=True)
        out_path.unlink(missing_ok=True)

        # any_valid = True if we have doctors (Codex cleans profile, not reject page)
        return filtered, len(filtered) > 0

    except subprocess.TimeoutExpired:
        log(f"[{place_id}] Codex validator timeout ({CODEX_TIMEOUT}s)")
        return doctors, True  # Timeout = pass through
    except Exception as e:
        log(f"[{place_id}] Codex validator exception: {e}")
        return doctors, True  # On error, pass through
