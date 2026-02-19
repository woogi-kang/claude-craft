"""System prompts for tweet classification and content generation.

All prompts are structured templates with placeholders that are filled
at runtime.  The classification prompt embeds domain knowledge from the
treatment knowledge base.
"""

from __future__ import annotations


CLASSIFICATION_SYSTEM_PROMPT = """\
You are a classification engine for the @ask.nandemo X account, a neutral \
data-driven resource about Korean dermatology clinics for Japanese users.

Your task: classify Japanese tweets about Korean beauty/dermatology clinics \
into one of three categories and assign a confidence score.

## Categories

1. **needs_help** -- The user is experiencing a problem, had a bad experience, \
or needs guidance. They would benefit from empathetic support and factual data.
   - Examples: treatment failure, upselling complaints, aftercare issues, \
language barrier problems, unexpected results.

2. **seeking_info** -- The user is actively looking for information, comparing \
options, planning a visit, or asking questions. They would benefit from \
data-driven answers.
   - Examples: clinic recommendations, price comparisons, treatment selection, \
first-time visit planning, before/after questions.

3. **irrelevant** -- The tweet does not represent a real person with genuine \
interest or need. Skip these.
   - Examples: clinic marketing accounts, bot-like posts, unrelated content, \
spam, stealth marketing from Korean accounts posing as Japanese users.

## Template Categories (for needs_help and seeking_info only)

Assign one template category based on the tweet content:
- A: Experience report (positive or negative)
- B: Question / concern about clinics or treatments
- C: Price sharing or comparison
- D: Trouble / failure / complaint
- E: Planning / preparation for a visit
- F: Clinic official account post
- G: Before/after progress report

## Classification Rules

1. If the account has a profile URL pointing to a clinic, classify as irrelevant.
2. If the bio contains clinic marketing keywords, classify as irrelevant.
3. If follower count > 10,000, classify as irrelevant (influencer/commercial).
4. If confidence < 0.7, force classification to irrelevant.
5. Tweets with genuine emotion (positive or negative) lean toward needs_help \
or seeking_info, never irrelevant.
6. Questions about prices, clinics, treatments lean toward seeking_info.
7. Complaints, failures, aftercare issues lean toward needs_help.

{domain_context}

## Output Format

Respond with ONLY a JSON object (no markdown, no explanation):
{{
  "classification": "needs_help" | "seeking_info" | "irrelevant",
  "confidence": 0.0 to 1.0,
  "rationale": "Brief explanation in English",
  "template_category": "A" | "B" | "C" | "D" | "E" | "F" | "G" | null
}}
"""


CLASSIFICATION_USER_PROMPT = """\
Classify this tweet:

Tweet content: {tweet_content}
Author username: @{author_username}
Author bio: {author_bio}
Author follower count: {follower_count}
Author following count: {following_count}
Tweet engagement: {likes} likes, {retweets} RTs, {replies} replies
"""


def build_classification_system_prompt(domain_context: str) -> str:
    """Build the full system prompt with domain context injected.

    Parameters
    ----------
    domain_context:
        Treatment terminology and concern mappings from the knowledge base.
    """
    return CLASSIFICATION_SYSTEM_PROMPT.format(domain_context=domain_context)


def build_classification_user_prompt(
    tweet_content: str,
    author_username: str,
    author_bio: str,
    follower_count: int,
    following_count: int,
    likes: int,
    retweets: int,
    replies: int,
) -> str:
    """Build the user prompt for classifying a single tweet."""
    return CLASSIFICATION_USER_PROMPT.format(
        tweet_content=tweet_content,
        author_username=author_username,
        author_bio=author_bio or "(no bio)",
        follower_count=follower_count,
        following_count=following_count,
        likes=likes,
        retweets=retweets,
        replies=replies,
    )
