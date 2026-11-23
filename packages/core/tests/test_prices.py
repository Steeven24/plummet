from datetime import timedelta
from decimal import Decimal

from plummet_core import repository as repo
from plummet_core.models import PriceRecord, utc_now


def make_product(session):
    return repo.add_product(session, "https://shop.test/a", "shop.test")


def test_record_price_updates_product(session):
    product = make_product(session)
    product.last_error = "timeout"

    record = repo.record_price(session, product, Decimal("19.99"))

    assert record.price == Decimal("19.99")
    assert product.last_price == Decimal("19.99")
    assert product.last_checked_at == record.checked_at
    assert product.last_error is None


def test_record_error(session):
    product = make_product(session)

    repo.record_error(session, product, "x" * 600)

    assert len(product.last_error) == 500
    assert product.last_checked_at is not None


def test_price_history_only_recent_days(session):
    product = make_product(session)
    now = utc_now()
    repo.record_price(session, product, Decimal("30"), checked_at=now - timedelta(days=40))
    repo.record_price(session, product, Decimal("20"), checked_at=now - timedelta(days=2))
    repo.record_price(session, product, Decimal("10"), checked_at=now)

    prices = [r.price for r in repo.price_history(session, product.id, days=30)]

    assert prices == [Decimal("20.00"), Decimal("10.00")]


def test_delete_product_removes_prices(session):
    product = make_product(session)
    repo.record_price(session, product, Decimal("5"))

    repo.delete_product(session, product.id)

    assert session.query(PriceRecord).count() == 0
