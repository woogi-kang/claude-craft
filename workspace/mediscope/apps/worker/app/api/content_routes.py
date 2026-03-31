"""API routes for AI content generation engine."""

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel

from ..api.routes import verify_bearer
from ..services.content_engine import (
    ContentLanguage,
    ContentType,
    generate_content,
    get_supported_content_types,
    get_supported_languages,
)
from ..services.procedure_data import list_procedures

router = APIRouter()


# --- Request / Response models ---

class ContentGenerateRequest(BaseModel):
    content_type: ContentType
    procedure_name: str
    hospital_name: str | None = None
    hospital_region: str | None = None
    target_language: ContentLanguage = ContentLanguage.KO
    target_keywords: list[str] | None = None
    custom_context: str | None = None


class ContentGenerateResponse(BaseModel):
    content_type: str
    title: str
    content: str
    meta_title: str
    meta_description: str
    seo_score: int
    word_count: int
    language: str
    schema_markup: str
    compliance_warnings: list[str]
    generated_at: str
    source_data: dict


# --- Endpoints ---

@router.post("/content/generate", response_model=ContentGenerateResponse)
async def generate_content_endpoint(
    body: ContentGenerateRequest,
    _token: str = Depends(verify_bearer),
):
    """Generate AI-powered content for a dermatology procedure."""
    try:
        result = await generate_content(
            content_type=body.content_type,
            procedure_name=body.procedure_name,
            hospital_name=body.hospital_name,
            hospital_region=body.hospital_region,
            target_language=body.target_language,
            target_keywords=body.target_keywords,
            custom_context=body.custom_context,
        )
        return ContentGenerateResponse(**result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Content generation failed: {e}")


@router.get("/content/templates")
async def list_content_templates():
    """List available content types and supported languages."""
    return {
        "content_types": get_supported_content_types(),
        "languages": get_supported_languages(),
    }


@router.get("/content/procedures")
async def list_content_procedures(
    _token: str = Depends(verify_bearer),
):
    """List available procedures from DB (grouped by category)."""
    procedures = await list_procedures()
    return {"categories": procedures}
