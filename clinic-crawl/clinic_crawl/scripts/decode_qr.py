"""QR code image decoding for extracting social links (WeChat, KakaoTalk)."""

from __future__ import annotations

import io
import logging

import httpx
from PIL import Image

from clinic_crawl.models.enums import ExtractionMethod, SocialPlatform
from clinic_crawl.models.social import SocialLink
from clinic_crawl.net import MAX_IMAGE_SIZE, safe_get, validate_url
from clinic_crawl.patterns import identify_platform

logger = logging.getLogger(__name__)


def decode_qr_from_bytes(image_bytes: bytes) -> list[str]:
    """Decode QR codes from image bytes.

    Returns list of decoded text strings.
    """
    try:
        from pyzbar import pyzbar
    except ImportError:
        logger.warning("pyzbar not installed. QR decoding unavailable.")
        return []

    try:
        image = Image.open(io.BytesIO(image_bytes))
        # Reject abnormally large images (decompression bomb protection)
        max_dim = 4096
        if image.width > max_dim or image.height > max_dim:
            logger.warning("Image too large (%dx%d), skipping QR decode", image.width, image.height)
            return []
        # Convert to grayscale for better detection
        image = image.convert("L")
        decoded = pyzbar.decode(image)
        return [d.data.decode("utf-8", errors="replace") for d in decoded]
    except Exception as e:
        logger.debug("QR decode failed: %s", e)
        return []


async def download_and_decode_qr(
    url: str,
    client: httpx.AsyncClient | None = None,
) -> list[str]:
    """Download an image URL and try to decode QR codes."""
    url_error = await validate_url(url)
    if url_error:
        logger.debug("QR image URL blocked: %s (%s)", url, url_error)
        return []

    should_close = False
    if client is None:
        client = httpx.AsyncClient()
        should_close = True

    try:
        response = await safe_get(
            client,
            url,
            timeout=10.0,
            max_size=MAX_IMAGE_SIZE,
        )
        if response.status_code != 200:
            return []

        content_type = response.headers.get("content-type", "")
        if "image" not in content_type and not url.lower().endswith(
            (".png", ".jpg", ".jpeg", ".gif", ".webp")
        ):
            return []

        return decode_qr_from_bytes(response.content)
    except (httpx.HTTPError, ValueError) as e:
        logger.debug("Failed to download QR image %s: %s", url, e)
        return []
    finally:
        if should_close:
            await client.aclose()


def qr_text_to_social_link(text: str) -> SocialLink | None:
    """Convert decoded QR text to a SocialLink if it's a social URL."""
    text = text.strip()
    if not text.startswith("http"):
        return None

    platform = identify_platform(text)
    if platform is None:
        # WeChat QR codes sometimes contain weixin:// URLs
        if "weixin" in text.lower() or "wechat" in text.lower():
            platform = SocialPlatform.WECHAT
        else:
            return None

    return SocialLink(
        platform=platform,
        url=text,
        extraction_method=ExtractionMethod.QR_DECODE,
        confidence=0.95,
    )
