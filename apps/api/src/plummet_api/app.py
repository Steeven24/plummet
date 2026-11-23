"""Build the FastAPI app."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import Engine

from plummet_api.routes import cron, dashboard, products
from plummet_core.config import Settings, get_settings
from plummet_core.db import init_db, make_engine


def create_app(engine: Engine | None = None, settings: Settings | None = None) -> FastAPI:
    """Create the app. Tests can give their own engine."""
    settings = settings or get_settings()
    if engine is None:
        engine = make_engine()
    init_db(engine)

    app = FastAPI(title="Plummet API", version="1.0.0")
    app.state.engine = engine
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    @app.get("/api/health", tags=["health"])
    def health() -> dict[str, str]:
        return {"status": "ok"}

    app.include_router(products.router)
    app.include_router(dashboard.router)
    app.include_router(cron.router)
    return app
