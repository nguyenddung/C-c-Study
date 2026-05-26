"""
CócStudy FastAPI Application
=============================
Entry point: registers middleware, static files, API routers,
startup/shutdown lifecycle events, and the health-check endpoint.
"""

from contextlib import asynccontextmanager
from pathlib import Path

import structlog
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.api.v1 import auth, groups, matching, messages, notifications, profiles, uploads, users
from app.core.config import settings
from app.database.session import engine
from app.database.base import Base
from app.middleware.rate_limiter import RateLimitMiddleware

logger = structlog.get_logger(__name__)


# ── Lifespan (startup + shutdown) ─────────────────────────────────────────

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Run startup tasks (create tables if absent) and teardown on shutdown."""
    logger.info("CócStudy API starting", env=settings.APP_ENV)

    # Ensure upload directories exist
    Path(settings.UPLOAD_DIR).mkdir(parents=True, exist_ok=True)
    Path(settings.UPLOAD_DIR + "/avatars").mkdir(exist_ok=True)
    Path(settings.UPLOAD_DIR + "/documents").mkdir(exist_ok=True)

    # In development, auto-create tables (production uses Alembic migrations)
    if settings.APP_ENV == "development":
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        logger.info("Database tables checked/created")

    yield

    logger.info("CócStudy API shutting down")
    await engine.dispose()


# ── App factory ────────────────────────────────────────────────────────────

def create_app() -> FastAPI:
    app = FastAPI(
        title="CócStudy API",
        description="AI-powered study partner matching for Vietnamese university students",
        version="1.0.0",
        docs_url="/docs",
        redoc_url="/redoc",
        lifespan=lifespan,
    )

    # ── CORS ───────────────────────────────────────────────────────────────
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.allowed_origins_list,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # ── Rate limiting ──────────────────────────────────────────────────────
    app.add_middleware(
        RateLimitMiddleware,
        requests_per_minute=settings.RATE_LIMIT_PER_MINUTE,
    )

    # ── Static file serving (avatars, uploaded docs) ───────────────────────
    upload_path = Path(settings.UPLOAD_DIR)
    upload_path.mkdir(parents=True, exist_ok=True)
    app.mount("/static", StaticFiles(directory=str(upload_path)), name="static")

    # ── API routers ────────────────────────────────────────────────────────
    prefix = "/api/v1"
    app.include_router(auth.router,          prefix=prefix)
    app.include_router(users.router,         prefix=prefix)
    app.include_router(profiles.router,      prefix=prefix)
    app.include_router(matching.router,      prefix=prefix)
    app.include_router(groups.router,        prefix=prefix)
    app.include_router(messages.router,      prefix=prefix)
    app.include_router(notifications.router, prefix=prefix)
    app.include_router(uploads.router,       prefix=prefix)

    # ── Health check ───────────────────────────────────────────────────────
    @app.get("/health", tags=["system"])
    async def health():
        return {"status": "ok", "app": settings.APP_NAME, "env": settings.APP_ENV}

    return app


app = create_app()