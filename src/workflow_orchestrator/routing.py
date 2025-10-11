from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware

from .api.main import app as api_app
from .observability import router as obs_router
from .logging import setup_logging


def create_app() -> FastAPI:
    """Create and configure the FastAPI application instance."""

    # 1) Logging setup
    try:
        setup_logging("INFO")
    except Exception:
        # Logging should never block app creation
        pass

    # 2) Root FastAPI app
    app = FastAPI(title="Workflow Orchestrator")

    # 3) Global middleware
    app.add_middleware(GZipMiddleware, minimum_size=1024)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # Adjust for production (e.g. ["https://your.domain"])
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # 4) Routers and sub-apps
    # Mount the primary API (from api/main.py)
    app.mount("/", api_app)

    # Observability endpoints (e.g. /observability/health)
    app.include_router(obs_router, prefix="/observability")

    # 5) Lifecycle hooks
    @app.on_event("startup")
    async def _startup() -> None:
        """Called once on application startup.
        Use for initializing DB connections, caches, etc.
        Example: await mongo_repo.create_indexes()
        """
        pass

    @app.on_event("shutdown")
    async def _shutdown() -> None:
        """Called on graceful shutdown.
        Use for cleanup, closing connections, or flushing metrics.
        """
        pass

    return app