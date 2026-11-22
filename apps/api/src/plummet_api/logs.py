"""Read the last lines of the worker log for the dashboard."""

import re
from collections import deque
from pathlib import Path

from pydantic import BaseModel

# Same format as the worker: "2026-11-12 16:52:52  INFO   Starting round"
LINE = re.compile(r"^(\d{4}-\d{2}-\d{2}) (\d{2}:\d{2}:\d{2})\s+([A-Z]+)\s+(.*)$")


class LogLine(BaseModel):
    date: str
    time: str
    level: str
    message: str


def read_log_tail(path: Path, lines: int = 20) -> list[LogLine]:
    """Return the newest log lines, oldest first. Lines in other formats are skipped."""
    if not path.is_file():
        return []
    with path.open(encoding="utf-8", errors="replace") as file:
        last = deque(file, maxlen=lines * 3)
    parsed = [LINE.match(line.rstrip("\n")) for line in last]
    found = [LogLine(date=m[1], time=m[2], level=m[3], message=m[4]) for m in parsed if m]
    return found[-lines:]
