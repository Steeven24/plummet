import httpx
import pytest

from plummet_core.config import Settings
from plummet_core.db import init_db, make_engine, session_scope
from plummet_core.fetcher import Fetcher


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


@pytest.fixture
def make_fetcher():
    """Build a fetcher that talks to a fake server instead of the internet.

    It returns the fetcher and the list of waits, so tests do not really sleep.
    """

    def build(handler, retries=3):
        settings = Settings(max_retries=retries)
        client = httpx.Client(transport=httpx.MockTransport(handler))
        waits = []
        return Fetcher(settings, client=client, sleep=waits.append), waits

    return build
