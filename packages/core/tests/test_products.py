from decimal import Decimal

from plummet_core import repository as repo


def test_add_product(session):
    product = repo.add_product(
        session, "https://shop.test/kindle", "shop.test", target_price=Decimal("99.90")
    )

    assert product.id is not None
    assert product.target_price == Decimal("99.90")
    assert product.alerts_enabled is True
    assert product.last_price is None


def test_add_product_with_selector(session):
    product = repo.add_product(session, "https://shop.test/a", "shop.test", price_selector=".price")

    assert product.price_selector == ".price"


def test_get_product_by_url(session):
    repo.add_product(session, "https://shop.test/a", "shop.test")

    assert repo.get_product_by_url(session, "https://shop.test/a") is not None
    assert repo.get_product_by_url(session, "https://shop.test/b") is None


def test_list_products_in_order(session):
    repo.add_product(session, "https://shop.test/a", "shop.test")
    repo.add_product(session, "https://shop.test/b", "shop.test")

    urls = [p.url for p in repo.list_products(session)]

    assert urls == ["https://shop.test/a", "https://shop.test/b"]


def test_set_target_price(session):
    product = repo.add_product(session, "https://shop.test/a", "shop.test")

    repo.set_target_price(session, product, Decimal("10"))

    assert product.target_cents == 1000


def test_delete_product_with_history(session):
    product = repo.add_product(session, "https://shop.test/a", "shop.test")
    repo.record_price(session, product, Decimal("5"))

    assert repo.delete_product(session, product.id) is True
    assert repo.get_product(session, product.id) is None
    assert repo.delete_product(session, product.id) is False
