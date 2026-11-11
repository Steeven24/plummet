"""Find the price and name of a product on a store page."""

from dataclasses import replace

from bs4 import BeautifulSoup

from plummet_core.parsing.result import ParsedProduct, ParseError
from plummet_core.parsing.stores import PRICE_SELECTORS, find_name, from_selectors, store_key
from plummet_core.parsing.structured import from_json_ld, from_meta_tags


def parse_product(html: str, url: str, selector: str | None = None) -> ParsedProduct:
    """Read the product from the page HTML.

    We try these ways in order and use the first one that finds a price:
    1. The CSS selector given by the user, if there is one
    2. JSON-LD structured data
    3. Meta tags and microdata
    4. The CSS selectors we know for this store
    """
    soup = BeautifulSoup(html, "html.parser")
    product = _find_price(soup, url, selector)
    if product is None:
        raise ParseError(f"No price found on {url}")
    if product.name is None:
        product = replace(product, name=find_name(soup, url))
    return product


def _find_price(soup: BeautifulSoup, url: str, selector: str | None) -> ParsedProduct | None:
    if selector and (product := from_selectors(soup, [selector])):
        return product
    if product := from_json_ld(soup) or from_meta_tags(soup):
        return product
    key = store_key(url)
    return from_selectors(soup, PRICE_SELECTORS[key]) if key else None
