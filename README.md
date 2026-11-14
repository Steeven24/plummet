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
├── deploy/        # Cron script and examples
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
| `check_runs` | Each round of checks: time, seconds, alerts and errors |
| `sent_alerts` | Every alert message and if Telegram got it |

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

## Set up Telegram alerts

1. Open Telegram, talk to [@BotFather](https://t.me/BotFather) and send `/newbot`.
   It gives you a token like `123456:ABC-DEF...`.
2. Send any message to your new bot.
3. Open `https://api.telegram.org/bot<TOKEN>/getUpdates` in your browser and
   copy the number in `"chat":{"id": ...}`. This is your chat ID.
4. Add both values to your `.env` file:

   ```bash
   PLUMMET_TELEGRAM_BOT_TOKEN=123456:ABC-DEF...
   PLUMMET_TELEGRAM_CHAT_ID=987654321
   ```

5. Check that it works:

   ```bash
   uv run plummet-worker test-telegram
   ```

After each round, the worker sends one message per alert. Every alert is
also saved in the `sent_alerts` table, even when Telegram fails, so you
can see it later in the dashboard. Keep your token secret: Plummet never
writes it in the logs.

## Run the checks with cron

The worker app checks all products once and stops. Cron runs it again
and again.

```bash
# Add a product (the Telegram bot will do this later)
uv run plummet-worker add "https://www.amazon.com/dp/B0..." --target 79.99

# Check all prices once
make check-prices

# Print the line for your crontab, with your paths and interval
uv run plummet-worker cron
```

Then run `crontab -e` and paste the line. It looks like this:

```
*/30 * * * * /path/to/plummet/deploy/run-worker.sh >> /path/to/plummet/logs/cron.log 2>&1
```

- Logs are saved in `logs/worker.log` (max 1 MB, 5 old files are kept).
- If a round is still running when cron starts the next one, the new one
  is skipped. A lock file in `data/worker.lock` controls this.
- Each round is saved in the `check_runs` table: time, seconds, products
  checked, alerts and errors. The dashboard will use it.
