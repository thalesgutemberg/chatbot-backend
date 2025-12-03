"""FastAPI application entry point."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.lifecycle import lifespan


def create_app() -> FastAPI:
    """Create and configure the FastAPI application."""
    app = FastAPI(
        title=settings.project_name,
        description="Agentic SaaS Backend API",
        version="0.1.0",
        openapi_url=f"{settings.api_v1_prefix}/openapi.json",
        docs_url="/docs",
        redoc_url="/redoc",
        lifespan=lifespan,
    )

    # Configure CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Include routers
    from app.api.v1.router import api_router

    app.include_router(api_router, prefix=settings.api_v1_prefix)

    @app.get("/health")
    async def health_check() -> dict[str, str]:
        """Health check endpoint."""
        return {"status": "healthy"}

    @app.get("/")
    async def root() -> dict[str, str]:
        """Root endpoint."""
        return {
            "message": f"Welcome to {settings.project_name}",
            "docs": "/docs",
        }

    return app


# Create application instance
app = create_app()
