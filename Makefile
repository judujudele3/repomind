.PHONY: install run run-ollama stop test lint format typecheck clean logs shell help

# =============================================================================
# RepoMind — Makefile
# =============================================================================

help: ## Show this help message
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | \
		awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

# -----------------------------------------------------------------------------
# Setup & run
# -----------------------------------------------------------------------------

install: ## Build Docker images
	docker compose build

run: ## Start the full stack (app + ChromaDB)
	cp -n .env.example .env 2>/dev/null || true
	docker compose up --build

run-ollama: ## Start the full stack including Ollama (local LLM)
	cp -n .env.example .env 2>/dev/null || true
	docker compose --profile ollama up --build

stop: ## Stop all services
	docker compose down

restart: ## Restart all services
	docker compose down && docker compose up --build

# -----------------------------------------------------------------------------
# Development
# -----------------------------------------------------------------------------

test: ## Run the test suite
	docker compose run --rm app pytest

test-cov: ## Run tests with HTML coverage report
	docker compose run --rm app pytest --cov-report=html

lint: ## Lint the codebase with ruff
	docker compose run --rm app ruff check app/ tests/

format: ## Format code with black + isort
	docker compose run --rm app black app/ tests/
	docker compose run --rm app isort app/ tests/

typecheck: ## Run mypy type checking
	docker compose run --rm app mypy app/

check: lint typecheck ## Run lint + typecheck together

# -----------------------------------------------------------------------------
# Utilities
# -----------------------------------------------------------------------------

logs: ## Tail logs from all services
	docker compose logs -f

shell: ## Open a shell in the app container
	docker compose run --rm app bash

clean: ## Remove containers, volumes, and cache
	docker compose down -v
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".mypy_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".ruff_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name "htmlcov" -exec rm -rf {} + 2>/dev/null || true
