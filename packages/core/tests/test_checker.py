from decimal import Decimal

import httpx

from plummet_core import repository as repo
from plummet_core.alerts import AlertKind
from plummet_core.checker import check_product


def price_page(price):
    return f'<h1>Nice Mouse</h1><meta property="product:price:amount" content="{price}">'


def fetcher_for(make_fetcher, html, status=200):
    fetcher, _ = make_fetcher(lambda request: httpx.Response(status, text=html), retries=0)
    return fetcher


def add(session, target=None):
    return repo.add_product(session, "https://shop.test/mouse", "shop.test", target_price=target)


def test_saves_price_and_name(session, make_fetcher):
    product = add(session)

    result = check_product(session, product, fetcher_for(make_fetcher, price_page("49.90")))

    assert result.ok
    assert result.price == Decimal("49.90")
    assert product.last_price == Decimal("49.90")
    assert product.name == "Nice Mouse"
    assert len(product.prices) == 1


def test_alert_when_price_goes_under_target(session, make_fetcher):
    product = add(session, target=Decimal("45"))
    repo.record_price(session, product, Decimal("50"))

    result = check_product(session, product, fetcher_for(make_fetcher, price_page("44.00")))

    assert result.alert.kind == AlertKind.BELOW_TARGET
    assert result.alert.old_price == Decimal("50.00")


def test_no_alert_when_alerts_are_off(session, make_fetcher):
    product = add(session, target=Decimal("45"))
    product.alerts_enabled = False

    result = check_product(session, product, fetcher_for(make_fetcher, price_page("40")))

    assert result.alert is None


def test_fetch_error_is_saved(session, make_fetcher):
    product = add(session)

    result = check_product(session, product, fetcher_for(make_fetcher, "", status=404))

    assert not result.ok
    assert "404" in product.last_error
    assert product.prices == []


def test_parse_error_is_saved(session, make_fetcher):
    product = add(session)

    result = check_product(session, product, fetcher_for(make_fetcher, "<h1>No price</h1>"))

    assert "No price found" in result.error
    assert product.last_error == result.error
