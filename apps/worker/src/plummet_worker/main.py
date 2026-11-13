"""Command line for the worker. Cron runs `plummet-worker run`."""

import argparse
import logging
from collections.abc import Sequence
from decimal import Decimal
from pathlib import Path

from plummet_core import repository as repo
from plummet_core.config import get_settings
from plummet_core.db import init_db, make_engine, session_scope
from plummet_core.parsing import store_name
from plummet_core.telegram import TelegramClient
from plummet_worker.cron import crontab_line
from plummet_worker.lock import AlreadyRunning, RunLock
from plummet_worker.logs import setup_logging
from plummet_worker.round import run_round

logger = logging.getLogger("plummet.worker")


def cmd_run(args: argparse.Namespace) -> int:
    settings = get_settings()
    setup_logging(settings.log_level, args.log_file)
    telegram = TelegramClient.from_settings(settings)
    try:
        with RunLock(args.lock_file):
            engine = make_engine()
            init_db(engine)
            summary = run_round(engine, settings, telegram=telegram)
    except AlreadyRunning as error:
        logger.info("%s. Skipping this round.", error)
        return 0
    finally:
        if telegram is not None:
            telegram.close()
    all_failed = bool(summary.results) and len(summary.errors) == len(summary.results)
    return 1 if all_failed else 0


def cmd_add(args: argparse.Namespace) -> int:
    engine = make_engine()
    init_db(engine)
    with session_scope(engine) as session:
        if repo.get_product_by_url(session, args.url):
            print(f"Already tracking {args.url}")
            return 1
        product = repo.add_product(
            session, args.url, store_name(args.url), args.target, price_selector=args.selector
        )
        print(f"Tracking product {product.id} from {product.store}")
    return 0


def cmd_cron(args: argparse.Namespace) -> int:
    root = Path(__file__).resolve().parents[4]  # the monorepo folder
    script, log_file = root / "deploy" / "run-worker.sh", root / "logs" / "cron.log"
    print(crontab_line(get_settings().check_interval_minutes, str(script), str(log_file)))
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="plummet-worker", description="Check product prices.")
    commands = parser.add_subparsers(dest="command", required=True)

    run = commands.add_parser("run", help="check all products once")
    run.add_argument("--log-file", type=Path, default=Path("logs/worker.log"))
    run.add_argument("--lock-file", type=Path, default=Path("data/worker.lock"))
    run.set_defaults(func=cmd_run)

    add = commands.add_parser("add", help="start tracking a product")
    add.add_argument("url")
    add.add_argument("--target", type=Decimal, help="alert when the price is this or less")
    add.add_argument("--selector", help="CSS selector of the price, if needed")
    add.set_defaults(func=cmd_add)

    cron = commands.add_parser("cron", help="print the line to add with `crontab -e`")
    cron.set_defaults(func=cmd_cron)

    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
