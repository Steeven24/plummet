# One image for the API, the worker and the Telegram bot.
# Each service in docker-compose.yml runs a different command.
FROM python:3.12-slim

COPY --from=ghcr.io/astral-sh/uv:0.13.7 /uv /usr/local/bin/uv

ENV UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy \
    UV_PYTHON_DOWNLOADS=never \
    PATH="/app/.venv/bin:$PATH" \
    PLUMMET_DATABASE_URL=sqlite:////app/data/plummet.db \
    PLUMMET_WORKER_LOG_FILE=/app/logs/worker.log

WORKDIR /app

# Copy the project files first and the code later, so Docker can reuse the
# layer with the installed packages when only the code changes.
COPY pyproject.toml uv.lock .python-version README.md ./
COPY packages/core/pyproject.toml packages/core/
COPY apps/api/pyproject.toml apps/api/
COPY apps/bot/pyproject.toml apps/bot/
COPY apps/worker/pyproject.toml apps/worker/
RUN uv sync --frozen --all-packages --no-dev --no-install-workspace

COPY packages packages
COPY apps/api apps/api
COPY apps/bot apps/bot
COPY apps/worker apps/worker
RUN uv sync --frozen --all-packages --no-dev

# Do not run as root.
RUN useradd --create-home plummet && mkdir -p data logs && chown plummet data logs
USER plummet

CMD ["plummet-api"]
