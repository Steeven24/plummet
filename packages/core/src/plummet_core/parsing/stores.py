"""CSS selectors for stores that do not have good structured data."""

from urllib.parse import urlparse

from bs4 import BeautifulSoup

from plummet_core.parsing.price_text import detect_currency, parse_price_text
from plummet_core.parsing.result import ParsedProduct
from plummet_core.parsing.structured import element_value

# Key: a word in the store domain. Value: price selectors, best one first.
PRICE_SELECTORS: dict[str, list[str]] = {
    "amazon": [
        "#corePrice_feature_div .a-offscreen",
        "#corePriceDisplay_desktop_feature_div .a-offscreen",
        ".a-price .a-offscreen",
    ],
    "mercadolibre": [
        ".ui-pdp-price__second-line .andes-money-amount__fraction",
        ".andes-money-amount__fraction",
    ],
    "ebay": [".x-price-primary .ux-textspans", "#prcIsum"],
}

NAME_SELECTORS: dict[str, list[str]] = {
    "amazon": ["#productTitle"],
    "mercadolibre": ["h1.ui-pdp-title"],
    "ebay": [".x-item-title__mainTitle"],
}


def store_name(url: str) -> str:
    """Return the domain of the store without "www.", for example "amazon.com"."""
    host = urlparse(url).hostname or url
    return host.removeprefix("www.")


def store_key(url: str) -> str | None:
    """Return the key of a known store, or None if we do not know the store."""
    host = store_name(url)
    return next((key for key in PRICE_SELECTORS if key in host), None)


def from_selectors(soup: BeautifulSoup, selectors: list[str]) -> ParsedProduct | None:
    """Try each CSS selector and return the first price we can read."""
    for selector in selectors:
        text = element_value(soup.select_one(selector))
        if price := parse_price_text(text):
            return ParsedProduct(price=price, currency=detect_currency(text))
    return None


def find_name(soup: BeautifulSoup, url: str) -> str | None:
    """Find the product name with the store selectors, og:title or <h1>."""
    key = store_key(url)
    selectors = [*NAME_SELECTORS.get(key, []), 'meta[property="og:title"]', "h1", "title"]
    for selector in selectors:
        if name := element_value(soup.select_one(selector)):
            return name[:300]
    return None
