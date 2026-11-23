.PHONY: install test lint format check-prices bot api web web-test

install: ## Install all Python and web packages
	uv sync --all-packages
	cd apps/web && npm install

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

bot: ## Start the Telegram bot
	uv run plummet-bot

api: ## Start the API for the web dashboard
	uv run plummet-api

web: ## Start the web dashboard (needs `make api` in another terminal)
	cd apps/web && npm run dev

web-test: ## Check types and run the web tests
	cd apps/web && npm run typecheck && npm test
