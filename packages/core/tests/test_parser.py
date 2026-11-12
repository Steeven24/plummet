from decimal import Decimal
from pathlib import Path

import pytest

from plummet_core.parsing import ParseError, parse_product

PAGES = Path(__file__).parent / "pages"


def page(name):
    return (PAGES / name).read_text()


def test_amazon_page():
    product = parse_product(page("amazon.html"), "https://www.amazon.com/dp/B0")

    assert product.price == Decimal("89.99")
    assert product.name == "Logitech MX Master 3S Wireless Mouse"


def test_mercadolibre_page():
    product = parse_product(page("mercadolibre.html"), "https://www.mercadolibre.com.mx/p/1")

    assert product.price == Decimal("2549")
    assert product.name == "Kindle Paperwhite 16 GB"


def test_json_ld_wins_over_visible_text():
    product = parse_product(page("json_ld.html"), "https://shop.test/fryer")

    assert product.price == Decimal("119.00")
    assert product.name == "Ninja Air Fryer"
    assert product.currency == "USD"


def test_custom_selector_comes_first():
    product = parse_product(page("json_ld.html"), "https://shop.test/fryer", selector=".price")

    assert product.price == Decimal("149.00")
    assert product.name == "Ninja Air Fryer 5.5 L"


def test_unknown_page_without_price():
    with pytest.raises(ParseError, match="No price found"):
        parse_product("<h1>Hello</h1>", "https://shop.test/a")
