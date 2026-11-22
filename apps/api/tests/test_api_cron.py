from datetime import timedelta

import pytest

from plummet_api.logs import read_log_tail
from plummet_core import repository as repo
from plummet_core.config import get_settings
from plummet_core.db import session_scope
from plummet_core.models import utc_now

LOG = """2026-11-12 09:30:02  INFO   Starting round · 6 products
Traceback (most recent call last):
2026-11-12 09:30:13  WARNING  liverpool · retry 1/3
2026-11-12 09:30:16  INFO   Round done in 14s · 1 alerts · 0 errors
"""


@pytest.fixture
def log_file(tmp_path, monkeypatch):
    path = tmp_path / "worker.log"
    path.write_text(LOG)
    monkeypatch.setenv("PLUMMET_WORKER_LOG_FILE", str(path))
    get_settings.cache_clear()
    yield path
    get_settings.cache_clear()


def test_read_log_tail_skips_other_lines(log_file):
    lines = read_log_tail(log_file, lines=2)

    assert [(line.level, line.message) for line in lines] == [
        ("WARNING", "liverpool · retry 1/3"),
        ("INFO", "Round done in 14s · 1 alerts · 0 errors"),
    ]


def test_read_log_tail_without_file(tmp_path):
    assert read_log_tail(tmp_path / "missing.log") == []


def test_cron_logs_route(client, log_file):
    lines = client.get("/api/cron/logs?lines=10").json()

    assert len(lines) == 3
    assert lines[0]["time"] == "09:30:02"


def test_cron_status(client, engine):
    now = utc_now()
    with session_scope(engine) as session:
        repo.record_run(session, now - timedelta(hours=1), 10, checked=4, alerts=0, errors=0)
        repo.record_run(session, now, 20, checked=4, alerts=1, errors=2)

    data = client.get("/api/cron").json()

    assert data["schedule"] == "*/30 * * * *"
    assert data["runs_week"] == 2
    assert data["success_rate"] == 75.0
    assert data["avg_seconds"] == 15.0
    assert data["last_run"]["errors"] == 2
    assert data["next_run_at"].endswith("Z")
