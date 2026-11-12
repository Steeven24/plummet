#!/usr/bin/env bash
# Run one round of price checks. Cron calls this script.
#
# Cron starts with almost no environment, so we go to the project
# folder (to read .env and use data/ and logs/) and find uv ourselves.
set -euo pipefail

cd "$(dirname "$0")/.."

export PATH="$HOME/.local/bin:$HOME/.cargo/bin:$PATH"

exec uv run --frozen plummet-worker run "$@"
