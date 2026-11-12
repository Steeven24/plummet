"""Command line for the worker. Cron runs `plummet-worker run`."""

import argparse
import logging
from collections.abc import Sequence
from pathlib import Path

from plummet_core.config import get_settings
from plummet_core.db import init_db, make_engine
from plummet_worker.lock import AlreadyRunning, RunLock
from plummet_worker.logs import setup_logging
from plummet_worker.round import run_round

logger = logging.getLogger("plummet.worker")


def cmd_run(args: argparse.Namespace) -> int:
    settings = get_settings()
    setup_logging(settings.log_level, args.log_file)
    try:
        with RunLock(args.lock_file):
            engine = make_engine()
            init_db(engine)
            summary = run_round(engine, settings)
    except AlreadyRunning as error:
        logger.info("%s. Skipping this round.", error)
        return 0
    all_failed = bool(summary.results) and len(summary.errors) == len(summary.results)
    return 1 if all_failed else 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="plummet-worker", description="Check product prices.")
    commands = parser.add_subparsers(dest="command", required=True)

    run = commands.add_parser("run", help="check all products once")
    run.add_argument("--log-file", type=Path, default=Path("logs/worker.log"))
    run.add_argument("--lock-file", type=Path, default=Path("data/worker.lock"))
    run.set_defaults(func=cmd_run)

    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
