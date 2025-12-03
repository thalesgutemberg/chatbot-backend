FROM python:3.12

ENV PYTHONUNBUFFERED=1

WORKDIR /app/

# Install uv
COPY --from=ghcr.io/astral-sh/uv:0.5.11 /uv /uvx /bin/

# PATH + uv configs
ENV PATH="/app/.venv/bin:$PATH"
ENV UV_COMPILE_BYTECODE=1
ENV UV_LINK_MODE=copy

# Install dependencies
RUN --mount=type=cache,id=4998b6c7-c7ae-4c71-9931-74f7364363a2,target=/root/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv sync --frozen --no-install-project

ENV PYTHONPATH=/app

COPY ./pyproject.toml ./uv.lock ./README.md /app/
COPY ./app /app/app

# Sync project deps
RUN --mount=type=cache,id=4998b6c7-c7ae-4c71-9931-74f7364363a2,target=/root/.cache/uv \
    uv sync

CMD ["sh", "-c", "fastapi run --host 0.0.0.0 --port ${PORT:-8000} app/main.py"]
