import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.pool import StaticPool

from plummet_api.app import create_app
from plummet_core.config import Settings


@pytest.fixture
def engine():
    """One database in memory, shared by the threads of the test client."""
    engine = create_engine(
        "sqlite://", connect_args={"check_same_thread": False}, poolclass=StaticPool
    )
    yield engine
    engine.dispose()


@pytest.fixture
def client(engine):
    with TestClient(create_app(engine, Settings())) as client:
        yield client
