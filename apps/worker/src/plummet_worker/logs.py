"""Logging for the worker: to the console and to a file."""

import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path

LOG_FORMAT = "%(asctime)s  %(levelname)-5s  %(message)s"
DATE_FORMAT = "%Y-%m-%d %H:%M:%S"


def setup_logging(level: str = "INFO", log_file: Path | None = None) -> None:
    """Send logs to the console and, if given, to a file.

    The file is rotated at 1 MB and we keep 5 old files, so it does not
    fill the disk when cron runs for months.
    """
    formatter = logging.Formatter(LOG_FORMAT, DATE_FORMAT)
    handlers: list[logging.Handler] = [logging.StreamHandler()]

    if log_file is not None:
        log_file.parent.mkdir(parents=True, exist_ok=True)
        handlers.append(RotatingFileHandler(log_file, maxBytes=1_000_000, backupCount=5))

    root = logging.getLogger()
    root.setLevel(level.upper())
    for handler in root.handlers[:]:
        root.removeHandler(handler)
    for handler in handlers:
        handler.setFormatter(formatter)
        root.addHandler(handler)

    # httpx logs every request, which is too much for us.
    logging.getLogger("httpx").setLevel(logging.WARNING)
