"""Content generation stub for Milestone 2.

Will use Claude to generate personalised reply and DM content
based on classification results and templates.
"""

from __future__ import annotations


class ContentGenerator:
    """Generate personalised outreach content (M2 implementation)."""

    async def generate_reply(self, tweet_content: str, template_category: str) -> str:
        """Generate a reply. Not yet implemented."""
        raise NotImplementedError("ContentGenerator is planned for Milestone 2")

    async def generate_dm(self, tweet_content: str, template_category: str) -> str:
        """Generate a DM. Not yet implemented."""
        raise NotImplementedError("ContentGenerator is planned for Milestone 2")
