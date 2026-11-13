.PHONY: install test lint format check-prices

install: ## Install all Python packages
	uv sync --all-packages

test: ## Run all tests
	uv run pytest

lint: ## Check code style
	uv run ruff check .
	uv run ruff format --check .

format: ## Fix code style
	uv run ruff check --fix .
	uv run ruff format .

check-prices: ## Check all product prices once
	uv run plummet-worker run
