from decimal import Decimal

import pytest

from plummet_bot.commands import CommandError, add_command, list_command, parse_price
from plummet_core import repository as repo

URL = "https://www.shop.test/mouse"


def test_add_product_with_target(session):
    text = add_command(session, [URL, "1,299.99"])

    product = repo.get_product_by_url(session, URL)
    assert product.target_price == Decimal("1299.99")
    assert product.store == "shop.test"
    assert "Tracking product <b>1</b>" in text


@pytest.mark.parametrize(
    ("args", "error"),
    [([], "Usage"), (["shop.test/a"], "full link"), ([URL, "cheap"], "not a valid price")],
)
def test_add_with_bad_input(session, args, error):
    with pytest.raises(CommandError, match=error):
        add_command(session, args)


def test_add_same_url_twice(session):
    add_command(session, [URL])

    with pytest.raises(CommandError, match="already track"):
        add_command(session, [URL])


@pytest.mark.parametrize(("text", "price"), [("99.90", "99.90"), ("1.299,99", "1299.99")])
def test_parse_price(text, price):
    assert parse_price(text) == Decimal(price)


def test_list_without_products(session):
    assert "do not track any product" in list_command(session)


def test_list_shows_products(session):
    add_command(session, [URL, "50"])
    product = repo.get_product_by_url(session, URL)
    repo.record_price(session, product, Decimal("55"))
    product.name = "Mouse <Pro>"
    product.last_error = "timeout"

    text = list_command(session)

    assert "Your products (1)" in text
    assert "Mouse &lt;Pro&gt;" in text
    assert "55.00 USD · target 50.00 · 🔔" in text
    assert "Last check failed: timeout" in text
