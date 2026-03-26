"""CheckYourHospital Worker — FastAPI crawling engine."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .api.batch_routes import router as batch_router
from .api.benchmark_routes import router as benchmark_router
from .api.routes import router
from .config import settings

app = FastAPI(
    title="CheckYourHospital Worker",
    version="0.1.0",
    docs_url="/docs" if settings.debug else None,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)

app.include_router(router, prefix="/worker")
app.include_router(batch_router, prefix="/worker")
app.include_router(benchmark_router, prefix="/worker")


@app.get("/")
async def root():
    return {"service": "checkyourhospital-worker", "version": "0.1.0"}
