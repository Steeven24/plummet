"""Database engine and sessions."""

from collections.abc import Iterator
from contextlib import contextmanager
from pathlib import Path

from sqlalchemy import Engine, create_engine
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker

from plummet_core.config import get_settings


class Base(DeclarativeBase):
    """Base class for all database models."""


def _make_sqlite_folder(url: str) -> None:
    """SQLite cannot create the folder of the file, so we create it first."""
    prefix = "sqlite:///"
    if url.startswith(prefix) and url != "sqlite:///:memory:":
        Path(url.removeprefix(prefix)).parent.mkdir(parents=True, exist_ok=True)


def make_engine(url: str | None = None) -> Engine:
    """Create an engine. Without a URL it uses the one from the settings."""
    url = url or get_settings().database_url
    _make_sqlite_folder(url)
    return create_engine(url)


def init_db(engine: Engine) -> None:
    """Create all tables that do not exist yet."""
    from plummet_core import models  # noqa: F401  (load the models so the tables are known)

    Base.metadata.create_all(engine)


@contextmanager
def session_scope(engine: Engine) -> Iterator[Session]:
    """Open a session, save the changes at the end, or undo them on error."""
    session = sessionmaker(bind=engine, expire_on_commit=False)()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()
