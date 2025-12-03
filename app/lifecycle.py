"""Application lifecycle management."""

from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

import structlog
from fastapi import FastAPI

from app.config import settings
from app.logging import setup_logging

logger = structlog.get_logger()


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    """Manage application lifecycle events."""
    setup_logging()
    logger.info(
        "Application starting",
        environment=settings.environment,
        debug=settings.debug,
    )

    yield

    logger.info("Application shutting down")
