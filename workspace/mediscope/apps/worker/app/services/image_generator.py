"""Image generator: Jinja2 HTML templates → Playwright screenshot → PNG bytes."""

import logging
from enum import Enum
from pathlib import Path

from jinja2 import Environment, FileSystemLoader
from playwright.async_api import async_playwright

from ..config import settings
from ..db.supabase import get_supabase_client

logger = logging.getLogger("mediscope.image")

TEMPLATES_DIR = Path(__file__).resolve().parent.parent / "templates" / "images"

_jinja_env = Environment(
    loader=FileSystemLoader(str(TEMPLATES_DIR)),
    autoescape=True,
)


class ImageType(str, Enum):
    INFOGRAPHIC = "infographic"
    SNS_CARD = "sns_card"
    COMPARISON_CHART = "comparison"
    BANNER = "banner"
    PROCEDURE_SUMMARY = "summary"


IMAGE_TYPE_DEFAULTS: dict[ImageType, tuple[int, int]] = {
    ImageType.INFOGRAPHIC: (1080, 1350),
    ImageType.SNS_CARD: (1080, 1080),
    ImageType.COMPARISON_CHART: (1080, 1080),
    ImageType.BANNER: (1200, 630),
    ImageType.PROCEDURE_SUMMARY: (1080, 1080),
}

TEMPLATE_FILES: dict[ImageType, str] = {
    ImageType.INFOGRAPHIC: "infographic.html",
    ImageType.SNS_CARD: "sns_card.html",
    ImageType.COMPARISON_CHART: "comparison_chart.html",
    ImageType.BANNER: "banner.html",
    ImageType.PROCEDURE_SUMMARY: "procedure_summary.html",
}


def render_image_html(
    image_type: ImageType,
    procedure_name: str,
    data: dict,
    language: str = "ko",
) -> str:
    """Render an image template with Jinja2."""
    template = _jinja_env.get_template(TEMPLATE_FILES[image_type])
    return template.render(
        procedure_name=procedure_name,
        data=data,
        language=language,
    )


async def html_to_screenshot(
    html: str,
    width: int = 1080,
    height: int = 1080,
) -> bytes:
    """Convert HTML string to PNG screenshot bytes using Playwright."""
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page(viewport={"width": width, "height": height})
        await page.set_content(html, wait_until="networkidle")
        png_bytes = await page.screenshot(type="png", full_page=False)
        await browser.close()
    return png_bytes


async def generate_image(
    image_type: ImageType,
    procedure_name: str,
    data: dict,
    language: str = "ko",
    width: int | None = None,
    height: int | None = None,
) -> bytes:
    """HTML template → Playwright rendering → PNG bytes.

    1. Render HTML template with Jinja2 (data injection)
    2. Open page with Playwright Chromium
    3. Capture screenshot at specified size
    4. Return PNG bytes
    """
    default_w, default_h = IMAGE_TYPE_DEFAULTS[image_type]
    w = width or default_w
    h = height or default_h

    html = render_image_html(image_type, procedure_name, data, language)
    png_bytes = await html_to_screenshot(html, w, h)
    logger.info(f"Image generated: type={image_type.value} size={len(png_bytes)} bytes")
    return png_bytes


def upload_image_to_storage(filename: str, png_bytes: bytes) -> str:
    """Upload PNG to Supabase Storage and return public URL."""
    client = get_supabase_client()
    if client is None:
        raise RuntimeError("Supabase client not configured")

    bucket = settings.supabase_image_bucket
    client.storage.from_(bucket).upload(
        filename,
        png_bytes,
        file_options={"content-type": "image/png", "upsert": "true"},
    )
    return client.storage.from_(bucket).get_public_url(filename)


def list_templates() -> list[dict]:
    """Return available image types with their default sizes."""
    return [
        {
            "type": img_type.value,
            "name": img_type.name.replace("_", " ").title(),
            "default_width": w,
            "default_height": h,
        }
        for img_type, (w, h) in IMAGE_TYPE_DEFAULTS.items()
    ]
