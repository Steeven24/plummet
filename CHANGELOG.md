# Changelog

## 1.0.0 – 2026-11-22

First full version.

### Added

- Monorepo with uv workspace: `packages/core` and the `api`, `bot`, `worker` and `web` apps
- Settings from environment variables or a `.env` file
- SQLite database with products, price history, sent alerts and check rounds
- Fetcher with browser-like headers, retries with backoff and `Retry-After` support
- Price parsers: JSON-LD, meta tags, microdata, store selectors and custom CSS selectors
- Alert rules: price under target (sent once) and big price drops
- Worker commands: `run`, `loop`, `add`, `cron`, `demo` and `test-telegram`
- Telegram alerts after each round, saved even when Telegram fails
- Private Telegram bot with `/add`, `/list`, `/target`, `/alerts` and `/remove`
- REST API with FastAPI for products, history, overview, alerts and cron status
- Web dashboard with summary cards, price chart, product table, alert feed and cron card
- Light and dark theme, phone layout
- Docker Compose to run everything with one command
- GitHub Actions for Python and web checks
