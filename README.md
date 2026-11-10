# Plummet 🔻

Plummet is a self-hosted price tracker. It checks online stores on a schedule
and sends you a Telegram message when a price drops below your target.

> 🚧 Work in progress. More details soon.

## Planned features

- Track products from any online store with a URL
- Save the price history of each product
- Get Telegram alerts when the price goes down
- Run checks automatically with cron
- See everything in a simple web dashboard

## Project structure

This is a monorepo. Each app lives in its own folder and they all share
the code in `packages/core`.

```
plummet/
├── apps/
│   ├── api/       # REST API for the web dashboard
│   ├── bot/       # Telegram bot that sends alerts
│   └── worker/    # Runs the price checks with cron
├── packages/
│   └── core/      # Shared code: database, scrapers, price logic
└── Makefile       # Common commands
```

## Getting started

You need Python 3.12 and [uv](https://docs.astral.sh/uv/).

```bash
make install   # install all packages
make test      # run the tests
make lint      # check the code style
```

## Configuration

Plummet reads its settings from environment variables or from a `.env` file.
All variables start with `PLUMMET_`.

```bash
cp .env.example .env
```

| Variable | Default | What it does |
|---|---|---|
| `PLUMMET_DATABASE_URL` | `sqlite:///data/plummet.db` | Where the data is saved |
| `PLUMMET_TELEGRAM_BOT_TOKEN` | — | Token from @BotFather |
| `PLUMMET_TELEGRAM_CHAT_ID` | — | Chat that gets the alerts |
| `PLUMMET_REQUEST_TIMEOUT` | `15` | Seconds to wait for a store page |
| `PLUMMET_MAX_RETRIES` | `3` | Tries before a check fails |
| `PLUMMET_CHECK_INTERVAL_MINUTES` | `30` | Time between checks (min. 5) |
| `PLUMMET_LOG_LEVEL` | `INFO` | How much detail the logs show |

Telegram alerts only work when both the token and the chat ID are set.

## Data

Plummet uses SQLite by default, so you do not need a database server.
The file is created at `data/plummet.db` the first time the app runs.

| Table | What it saves |
|---|---|
| `products` | The URL, store, target price and last price of each product |
| `price_records` | Every price found for a product, with the date |

Prices are saved as whole cents (for example `1999` for `19.99`)
to avoid rounding problems. All dates are in UTC.
