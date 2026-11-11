from decimal import Decimal

import pytest

from plummet_core.parsing.price_text import detect_currency, parse_price_text


@pytest.mark.parametrize(
    ("text", "price"),
    [
        ("$1,299.99", "1299.99"),
        ("1.299,99 €", "1299.99"),
        ("US$ 49.90", "49.90"),
        ("R$ 2.549,00", "2549.00"),
        ("$ 2.549", "2549"),
        ("1,299,000", "1299000"),
        ("19,99 €", "19.99"),
        ("£7.5", "7.5"),
        ("1 299,99 €", "1299.99"),
        ("Now only 35 USD!", "35"),
        ("$19.99 $25.00", "19.99"),
        ("1299.", "1299"),
    ],
)
def test_parse_price_text(text, price):
    assert parse_price_text(text) == Decimal(price)


@pytest.mark.parametrize("text", ["", None, "Out of stock", "$0.00", "Free"])
def test_returns_none_when_there_is_no_price(text):
    assert parse_price_text(text) is None


@pytest.mark.parametrize(
    ("text", "currency"),
    [
        ("US$ 49.90", "USD"),
        ("R$ 2.549,00", "BRL"),
        ("S/ 120.00", "PEN"),
        ("19,99 €", "EUR"),
        ("£7.50", "GBP"),
        ("1299 mxn", "MXN"),
        ("$ 2.549", None),
        ("", None),
    ],
)
def test_detect_currency(text, currency):
    assert detect_currency(text) == currency
