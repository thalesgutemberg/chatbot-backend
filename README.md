# Agentic SaaS Backend

FastAPI backend with 5-layer architecture, event-driven patterns, and LangGraph AI agents.

## Quick Start

```bash
# With Docker
docker compose up -d

# Development
uv sync
uv run uvicorn app.main:app --reload
```

## Architecture

- Layer 1: Models (SQLAlchemy ORM)
- Layer 2: Schemas (Pydantic DTOs)
- Layer 3: Repositories (Data access)
- Layer 4: Services (Business logic)
- Layer 5: API (FastAPI endpoints)

## Testing

```bash
uv run pytest
```
