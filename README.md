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
| `PLUMMET_MIN_DROP_PERCENT` | `5` | Price drop (%) that sends an alert |
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

## How pages are downloaded

The fetcher in `plummet_core.fetcher` downloads each store page with
browser-like headers. When a request fails for a temporary reason
(network error, `429` or `5xx`), it tries again and waits a bit longer
each time: 1s, 2s, 4s... If the store sends a `Retry-After` header, it
waits that time instead (max 30s). Errors like `404` fail at once.

Please be polite with stores: do not check the same product too often.

## How prices are found

`plummet_core.parsing.parse_product()` reads the page HTML and tries
these ways in order. It uses the first one that finds a price:

1. A CSS selector you give for the product (optional)
2. JSON-LD data (`schema.org/Product`), which many stores add for Google
3. Meta tags (`product:price:amount`) and microdata (`itemprop="price"`)
4. Built-in selectors for known stores: Amazon, Mercado Libre and eBay

It understands prices like `$1,299.99`, `1.299,99 €` or `$ 2.549`, and it
finds the currency when it is clear (`US$`, `R$`, `€`, `MXN`...).

## When you get an alert

`plummet_core.checker.check_all()` checks every product, saves the new
price and decides if it is good news. There are two kinds of alerts:

| Alert | When |
|---|---|
| `below_target` | The price goes to or under your target price |
| `price_drop` | The price goes down at least `PLUMMET_MIN_DROP_PERCENT` since the last check |

To avoid spam, `below_target` is sent only once, when the price crosses
the target. If the price stays under the target, you only get a new alert
when it drops a lot again. You can turn off alerts for each product.

If a product fails (page not found, no price...), the error is saved on
the product and the other products are still checked.
