"""MediScope Worker — FastAPI application."""

from fastapi import FastAPI

from .api.routes import router
from .config import settings

app = FastAPI(
    title=settings.app_name,
    version="0.1.0",
    docs_url="/docs" if settings.debug else None,
)

app.include_router(router, prefix="/worker")


@app.get("/")
async def root():
    return {"service": "mediscope-worker", "version": "0.1.0"}
