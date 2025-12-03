FROM python:3.12

ENV PYTHONUNBUFFERED=1

WORKDIR /app/

# Install uv
COPY --from=ghcr.io/astral-sh/uv:0.5.11 /uv /uvx /bin/

# Place executables in the environment at the front of the path
ENV PATH="/app/.venv/bin:$PATH"

# Compile bytecode
ENV UV_COMPILE_BYTECODE=1

# uv Cache
ENV UV_LINK_MODE=copy

# Copy dependency files first for better caching
COPY ./pyproject.toml ./uv.lock ./README.md /app/

# Install dependencies
RUN uv sync --frozen --no-install-project

ENV PYTHONPATH=/app

# Copy application code
COPY ./app /app/app
COPY ./knowledge_base /app/knowledge_base

# Sync the project (installs the project itself)
RUN uv sync

CMD ["sh", "-c", "fastapi run --host 0.0.0.0 --port ${PORT:-8000} app/main.py"]