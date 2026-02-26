from fastapi import FastAPI

from app.api.routes.analyze import router as analyze_router
from app.api.routes.ingest import router as ingest_router
from app.api.routes.stocks import router as stocks_router
from app.core.logging import setup_logging


def create_app() -> FastAPI:
    setup_logging()
    app = FastAPI(title="AI Equity Research Agent")

    @app.get("/ping", tags=["health"])
    async def ping() -> dict:
        """Lightweight health-check used by the frontend to wake the service."""
        return {"status": "ok"}

    app.include_router(ingest_router)
    app.include_router(analyze_router)
    app.include_router(stocks_router)
    return app


app = create_app()
