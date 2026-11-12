from decimal import Decimal

import httpx

from plummet_core import repository as repo
from plummet_core.config import Settings
from plummet_core.db import init_db, make_engine, session_scope
from plummet_core.fetcher import Fetcher
from plummet_worker.round import run_round


def fake_fetcher(settings):
    page = '<meta property="product:price:amount" content="9.50">'
    transport = httpx.MockTransport(lambda request: httpx.Response(200, text=page))
    return Fetcher(settings, client=httpx.Client(transport=transport))


def test_run_round_saves_prices_and_the_round(tmp_path):
    engine = make_engine(f"sqlite:///{tmp_path / 'test.db'}")
    init_db(engine)
    settings = Settings(max_retries=0)
    with session_scope(engine) as session:
        repo.add_product(session, "https://shop.test/a", "shop.test", target_price=Decimal("10"))

    summary = run_round(engine, settings, fetcher=fake_fetcher(settings))

    assert len(summary.alerts) == 1
    with session_scope(engine) as session:
        product = repo.list_products(session)[0]
        runs = repo.recent_runs(session)
        assert product.last_price == Decimal("9.50")
        assert len(runs) == 1
        assert (runs[0].checked, runs[0].alerts, runs[0].errors) == (1, 1, 0)
