"""Shared things the routes need, like the database session."""

from collections.abc import Iterator

from fastapi import Request
from sqlalchemy.orm import Session

from plummet_core.db import session_scope


def get_session(request: Request) -> Iterator[Session]:
    """Give each request its own session. Changes are saved at the end."""
    with session_scope(request.app.state.engine) as session:
        yield session
