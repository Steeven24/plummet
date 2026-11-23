"""Routes for the scheduled job card: how the cron rounds are doing."""

from datetime import timedelta
from typing import Annotated

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from plummet_api.deps import get_session
from plummet_api.logs import LogLine, read_log_tail
from plummet_api.schemas import CronStatus, RunOut
from plummet_core import repository as repo
from plummet_core.config import get_settings
from plummet_core.schedule import cron_expression

router = APIRouter(prefix="/api/cron", tags=["cron"])
SessionDep = Annotated[Session, Depends(get_session)]


@router.get("", response_model=CronStatus)
def cron_status(session: SessionDep):
    interval = get_settings().check_interval_minutes
    runs = repo.recent_runs(session, days=7)
    last = runs[0] if runs else None
    checked = sum(r.checked for r in runs)
    return CronStatus(
        schedule=cron_expression(interval),
        interval_minutes=interval,
        last_run=RunOut.model_validate(last) if last else None,
        next_run_at=last.started_at + timedelta(minutes=interval) if last else None,
        runs_week=len(runs),
        success_rate=round(sum(r.ok for r in runs) / checked * 100, 1) if checked else None,
        avg_seconds=round(sum(r.seconds for r in runs) / len(runs), 1) if runs else None,
    )


@router.get("/logs", response_model=list[LogLine])
def cron_logs(lines: int = Query(20, ge=1, le=200)):
    return read_log_tail(get_settings().worker_log_file, lines)
