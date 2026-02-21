from fastapi import FastAPI

from app.api.routes.analyze import router as analyze_router
from app.api.routes.ingest import router as ingest_router
from app.core.logging import setup_logging


def create_app() -> FastAPI:
    setup_logging()
    app = FastAPI(title="AI Equity Research Agent")
    app.include_router(ingest_router)
    app.include_router(analyze_router)
    return app


app = create_app()
