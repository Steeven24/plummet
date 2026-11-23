from datetime import timedelta

from plummet_core import repository as repo
from plummet_core.models import utc_now


def test_record_run(session):
    run = repo.record_run(
        session, started_at=utc_now(), seconds=14.2, checked=6, alerts=2, errors=1
    )

    assert run.id is not None
    assert run.ok == 5


def test_recent_runs_newest_first(session):
    now = utc_now()
    for days_ago in (10, 3, 1):
        repo.record_run(
            session,
            started_at=now - timedelta(days=days_ago),
            seconds=1,
            checked=1,
            alerts=0,
            errors=0,
        )

    runs = repo.recent_runs(session, days=7)

    assert [(now - r.started_at).days for r in runs] == [1, 3]
