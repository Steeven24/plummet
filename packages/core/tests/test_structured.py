import json
from decimal import Decimal

from bs4 import BeautifulSoup

from plummet_core.parsing.structured import from_json_ld


def soup(html):
    return BeautifulSoup(html, "html.parser")


def json_ld(data):
    return soup(f'<script type="application/ld+json">{json.dumps(data)}</script>')


def test_json_ld_product():
    page = json_ld(
        {
            "@type": "Product",
            "name": "Kindle Paperwhite",
            "offers": {"@type": "Offer", "price": "129.99", "priceCurrency": "USD"},
        }
    )

    product = from_json_ld(page)

    assert product.price == Decimal("129.99")
    assert product.name == "Kindle Paperwhite"
    assert product.currency == "USD"


def test_json_ld_inside_graph_with_offer_list():
    page = json_ld(
        {"@graph": [{"@type": "WebPage"}, {"@type": ["Product"], "offers": [{"price": 49}]}]}
    )

    assert from_json_ld(page).price == Decimal("49")


def test_json_ld_aggregate_offer_uses_low_price():
    page = json_ld({"@type": "Product", "offers": {"@type": "AggregateOffer", "lowPrice": "10.5"}})

    assert from_json_ld(page).price == Decimal("10.5")


def test_json_ld_ignores_broken_json_and_other_types():
    page = soup(
        '<script type="application/ld+json">{broken</script>'
        '<script type="application/ld+json">{"@type": "Organization"}</script>'
    )

    assert from_json_ld(page) is None
