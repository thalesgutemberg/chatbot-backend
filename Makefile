.PHONY: help setup dev dev-local lint format clean logs

help:
	@echo "Available commands:"
	@echo ""
	@echo "Development:"
	@echo "  make setup     - Install dependencies with UV"
	@echo "  make dev       - Start with Docker"
	@echo "  make dev-local - Start locally (without Docker)"
	@echo ""
	@echo "Quality:"
	@echo "  make lint      - Run linting (ruff + mypy)"
	@echo "  make format    - Format code with ruff"
	@echo ""
	@echo "Utilities:"
	@echo "  make clean     - Clean up Docker containers and caches"
	@echo "  make logs      - View Docker logs"

setup:
	uv sync --all-extras

dev:
	docker compose up --build

dev-local:
	uv run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

lint:
	uv run ruff check app/
	uv run mypy app/

format:
	uv run ruff check app/ --fix
	uv run ruff format app/

clean:
	docker compose down -v
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete 2>/dev/null || true

logs:
	docker compose logs -f
