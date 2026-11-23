import json
from decimal import Decimal

from bs4 import BeautifulSoup

from plummet_core.parsing.structured import from_json_ld, from_meta_tags


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


def test_meta_tags():
    page = soup(
        '<meta property="product:price:amount" content="2549.00">'
        '<meta property="product:price:currency" content="MXN">'
    )

    product = from_meta_tags(page)

    assert product.price == Decimal("2549.00")
    assert product.currency == "MXN"


def test_microdata_content_attribute():
    page = soup('<span itemprop="price" content="19.99">$19.99</span>')

    assert from_meta_tags(page).price == Decimal("19.99")


def test_microdata_visible_text_with_thousands():
    page = soup('<span itemprop="price">2.549</span>')

    assert from_meta_tags(page).price == Decimal("2549")


def test_meta_tags_without_price():
    assert from_meta_tags(soup("<p>No price here</p>")) is None
