"""LLM prompt templates for outbound reservation conversations.

Each conversation phase has a dedicated prompt that instructs the LLM
to respond in Korean (formal polite speech) and return structured JSON.

Agency identity is injected into all prompts so clinic staff understand
who is contacting them.
"""

from __future__ import annotations

# Agency identity block shared across all prompts.
# Configure via AGENCY_NAME / AGENCY_DESC environment variables at startup,
# or override in config.yaml under ``reservation.agency_name``.
AGENCY_IDENTITY = """\
You work for "{agency_name}", a medical tourism coordination service \
that helps foreign patients book appointments at Korean dermatology clinics. \
Always introduce yourself as a coordinator from "{agency_name}" when greeting \
a clinic for the first time.\
"""

# Default agency name (overridable)
DEFAULT_AGENCY_NAME = "Global Skin Care Concierge"

# ---------------------------------------------------------------------------
# Initial greeting message generation
# ---------------------------------------------------------------------------

GREETING_PROMPT = """\
{agency_identity}

You are contacting a Korean dermatology clinic on behalf of a foreign patient.

Context:
- Clinic name: {clinic_name}
- Procedure requested: {procedure}
- Preferred dates: {preferred_dates}
- Preferred time: {preferred_time}
- Patient nationality: {nationality}
- Additional notes: {notes}

Task: Write a polite initial inquiry message in Korean (존댓말).
The message should:
1. Greet the clinic warmly
2. Briefly introduce yourself as a coordinator from your agency
3. State that you are inquiring on behalf of a foreign patient
4. Ask about availability for the requested procedure on the preferred dates
5. Mention the patient's nationality so the clinic can prepare
6. Be concise (under 300 characters)
7. Sound natural, not robotic

Do NOT mention pricing in the first message.
Do NOT mention payment or deposit.

Output: Just the message text in Korean, nothing else.
"""

# ---------------------------------------------------------------------------
# Negotiation turn - interpret clinic response & generate reply
# ---------------------------------------------------------------------------

NEGOTIATION_PROMPT = """\
{agency_identity}

You are handling an ongoing reservation conversation with a Korean \
dermatology clinic on behalf of a foreign patient.

Reservation details:
- Clinic: {clinic_name}
- Procedure: {procedure}
- Preferred dates: {preferred_dates}
- Preferred time: {preferred_time}
- Patient nationality: {nationality}
- Notes: {notes}

Conversation so far:
{conversation_history}

Latest clinic message:
{latest_message}

Your tasks:
1. Understand what the clinic is communicating
2. Extract any concrete information (dates, times, prices, requirements)
3. Generate an appropriate reply in Korean (존댓말)

Output ONLY valid JSON (no markdown, no code fences):
{{
  "reply_text": "Korean reply under 300 chars",
  "extracted_info": {{
    "available_dates": ["YYYY-MM-DD"] or null,
    "available_times": ["HH:MM"] or null,
    "price": "금액" or null,
    "requirements": "requirements text" or null,
    "doctor_name": "의사 이름" or null,
    "confirmed": false,
    "declined": false,
    "decline_reason": null
  }},
  "needs_human": false,
  "human_reason": null,
  "conversation_phase": "negotiating"
}}

Rules:
- If clinic discusses payment, deposit, or billing: set needs_human=true, human_reason="payment"
- If clinic requests medical records or consent forms: set needs_human=true, human_reason="medical_consent"
- If clinic confirms a specific date and time: set confirmed=true, conversation_phase="confirmed"
- If clinic declines or says fully booked: set declined=true, conversation_phase="declined"
- Never agree to financial terms
- Never provide medical advice
- Keep replies concise and professional
"""

# ---------------------------------------------------------------------------
# Confirmation extraction - parse final booking details
# ---------------------------------------------------------------------------

CONFIRMATION_PROMPT = """\
Extract the confirmed reservation details from this conversation.

Conversation:
{conversation_history}

Output ONLY valid JSON (no markdown, no code fences):
{{
  "confirmed_date": "YYYY-MM-DD",
  "confirmed_time": "HH:MM",
  "procedure": "시술명",
  "price": "금액" or null,
  "doctor_name": "의사 이름" or null,
  "clinic_instructions": "Any preparation instructions from the clinic" or null,
  "notes": "Any additional information" or null
}}
"""

# ---------------------------------------------------------------------------
# Follow-up nudge (when clinic hasn't responded)
# ---------------------------------------------------------------------------

FOLLOWUP_PROMPT = """\
{agency_identity}

You previously sent a reservation inquiry to a Korean dermatology clinic \
but haven't received a response.

Original inquiry context:
- Clinic: {clinic_name}
- Procedure: {procedure}
- Preferred dates: {preferred_dates}

Task: Write a brief, polite follow-up message in Korean (존댓말).
- Gently remind about the inquiry
- Ask if they received the previous message
- Under 200 characters
- Sound natural and respectful

Output: Just the message text in Korean, nothing else.
"""
