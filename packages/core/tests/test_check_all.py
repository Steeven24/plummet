from decimal import Decimal

import httpx

from plummet_core import repository as repo
from plummet_core.checker import check_all

PAGES = {
    "https://shop.test/cheap": '<meta property="product:price:amount" content="8">',
    "https://shop.test/normal": '<meta property="product:price:amount" content="20">',
    "https://shop.test/no-price": "<h1>Sold out</h1>",
}


def handler(request):
    url = str(request.url)
    if url == "https://shop.test/crash":
        raise ValueError("something strange")
    return httpx.Response(200, text=PAGES[url])


def test_check_all_returns_summary(session, make_fetcher):
    repo.add_product(session, "https://shop.test/cheap", "shop.test", target_price=Decimal("10"))
    repo.add_product(session, "https://shop.test/normal", "shop.test")
    repo.add_product(session, "https://shop.test/no-price", "shop.test")
    fetcher, _ = make_fetcher(handler, retries=0)

    summary = check_all(session, fetcher)

    assert len(summary.results) == 3
    assert len(summary.alerts) == 1
    assert len(summary.errors) == 1
    assert summary.seconds >= 0


def test_unexpected_error_does_not_stop_the_round(session, make_fetcher):
    crash = repo.add_product(session, "https://shop.test/crash", "shop.test")
    repo.add_product(session, "https://shop.test/normal", "shop.test")
    fetcher, _ = make_fetcher(handler, retries=0)

    summary = check_all(session, fetcher)

    assert [r.ok for r in summary.results] == [False, True]
    assert "Unexpected error" in crash.last_error


def test_check_all_without_products(session, make_fetcher):
    fetcher, _ = make_fetcher(handler)

    summary = check_all(session, fetcher)

    assert summary.results == []
