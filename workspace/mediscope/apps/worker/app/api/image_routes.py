"""API routes for image generation."""

import logging
import uuid

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import Response
from pydantic import BaseModel

from ..api.routes import verify_bearer
from ..services.image_generator import (
    ImageType,
    generate_image,
    list_templates,
    upload_image_to_storage,
)

logger = logging.getLogger("checkyourhospital.image")
router = APIRouter()


class GenerateImageRequest(BaseModel):
    image_type: ImageType
    procedure_name: str
    language: str = "ko"
    data: dict = {}
    width: int | None = None
    height: int | None = None
    upload: bool = False


class GenerateImageUrlResponse(BaseModel):
    url: str
    filename: str


@router.post("/content/image")
async def generate_image_endpoint(
    body: GenerateImageRequest,
    _token: str = Depends(verify_bearer),
):
    """Generate an image from a template.

    If upload=true, uploads to Supabase Storage and returns URL.
    Otherwise, returns PNG bytes directly.
    """
    try:
        png_bytes = await generate_image(
            image_type=body.image_type,
            procedure_name=body.procedure_name,
            data=body.data,
            language=body.language,
            width=body.width,
            height=body.height,
        )
    except Exception as e:
        logger.exception(f"Image generation failed: {e}")
        raise HTTPException(status_code=500, detail="Image generation failed")

    if body.upload:
        filename = f"{body.image_type.value}/{uuid.uuid4()}.png"
        try:
            url = upload_image_to_storage(filename, png_bytes)
        except RuntimeError:
            raise HTTPException(status_code=500, detail="Storage not configured")
        return GenerateImageUrlResponse(url=url, filename=filename)

    return Response(content=png_bytes, media_type="image/png")


@router.get("/content/image/templates")
async def get_image_templates(
    _token: str = Depends(verify_bearer),
):
    """Return available image template types."""
    return {"templates": list_templates()}
