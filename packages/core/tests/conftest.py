import pytest

from plummet_core.db import init_db, make_engine, session_scope


@pytest.fixture
def engine():
    """A new empty database in memory for each test."""
    engine = make_engine("sqlite://")
    init_db(engine)
    yield engine
    engine.dispose()


@pytest.fixture
def session(engine):
    with session_scope(engine) as session:
        yield session
