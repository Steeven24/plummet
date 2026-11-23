from decimal import Decimal

import pytest
from bs4 import BeautifulSoup

from plummet_core.parsing.stores import find_name, from_selectors, store_key, store_name


@pytest.mark.parametrize(
    ("url", "name", "key"),
    [
        ("https://www.amazon.com/dp/B0", "amazon.com", "amazon"),
        ("https://www.mercadolibre.com.mx/p/MLM1", "mercadolibre.com.mx", "mercadolibre"),
        ("https://shop.test/item", "shop.test", None),
    ],
)
def test_store_name_and_key(url, name, key):
    assert store_name(url) == name
    assert store_key(url) == key


def test_from_selectors_uses_first_match():
    soup = BeautifulSoup('<b class="old">$20</b><b class="new">$15.50</b>', "html.parser")

    product = from_selectors(soup, [".missing", ".new", ".old"])

    assert product.price == Decimal("15.50")


def test_find_name_falls_back_to_h1():
    soup = BeautifulSoup("<h1>  Nice Shoes  </h1>", "html.parser")

    assert find_name(soup, "https://shop.test/a") == "Nice Shoes"
