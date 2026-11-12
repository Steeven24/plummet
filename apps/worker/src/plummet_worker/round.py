"""One round of price checks."""

from sqlalchemy import Engine

from plummet_core import repository as repo
from plummet_core.checker import CheckSummary, check_all
from plummet_core.config import Settings
from plummet_core.db import session_scope
from plummet_core.fetcher import Fetcher
from plummet_core.models import utc_now


def run_round(engine: Engine, settings: Settings, fetcher: Fetcher | None = None) -> CheckSummary:
    """Check all products and save the round, so the dashboard can show it."""
    started_at = utc_now()
    own_fetcher = fetcher is None
    fetcher = fetcher or Fetcher(settings)
    try:
        with session_scope(engine) as session:
            summary = check_all(session, fetcher, settings)
            repo.record_run(
                session,
                started_at=started_at,
                seconds=summary.seconds,
                checked=len(summary.results),
                alerts=len(summary.alerts),
                errors=len(summary.errors),
            )
    finally:
        if own_fetcher:
            fetcher.close()
    return summary
