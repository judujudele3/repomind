"""RepoMind FastAPI application entrypoint."""
import structlog
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config.logging import setup_logging
from app.config.settings import get_settings

settings = get_settings()
setup_logging(settings.log_level)
logger = structlog.get_logger(__name__)


def create_app() -> FastAPI:
    """Create and configure the FastAPI application."""
    app = FastAPI(
        title="RepoMind",
        description="Agentic codebase understanding system",
        version="1.0.0",
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_methods=["*"],
        allow_headers=["*"],
    )

    @app.get("/health")
    async def health() -> dict:
        return {"status": "ok", "version": "1.0.0"}

    logger.info("RepoMind API initialized", env=settings.app_env)
    return app


app = create_app()
