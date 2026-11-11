"""Read prices from structured data that many stores add for Google."""

import json
from collections.abc import Iterator
from decimal import Decimal, InvalidOperation
from typing import Any

from bs4 import BeautifulSoup

from plummet_core.parsing.price_text import parse_price_text
from plummet_core.parsing.result import ParsedProduct


def from_json_ld(soup: BeautifulSoup) -> ParsedProduct | None:
    """Find a schema.org Product inside <script type="application/ld+json">."""
    for script in soup.find_all("script", type="application/ld+json"):
        try:
            data = json.loads(script.string or "")
        except json.JSONDecodeError:
            continue
        for item in _walk(data):
            if _is_product(item) and (product := _product_from(item)):
                return product
    return None


def _walk(data: Any) -> Iterator[dict]:
    """Go through all objects, also the ones inside lists and "@graph"."""
    if isinstance(data, list):
        for value in data:
            yield from _walk(value)
    elif isinstance(data, dict):
        yield data
        yield from _walk(data.get("@graph", []))


def _is_product(item: dict) -> bool:
    kind = item.get("@type")
    return kind == "Product" or (isinstance(kind, list) and "Product" in kind)


def _product_from(item: dict) -> ParsedProduct | None:
    offers = item.get("offers")
    offer = offers[0] if isinstance(offers, list) and offers else offers
    if not isinstance(offer, dict):
        return None
    price = _to_decimal(offer.get("price") or offer.get("lowPrice"))
    if price is None:
        return None
    return ParsedProduct(price=price, name=item.get("name"), currency=offer.get("priceCurrency"))


def _to_decimal(value: Any) -> Decimal | None:
    """schema.org uses "1299.99", but some stores send "1.299,99", so we try both."""
    if value is None:
        return None
    try:
        price = Decimal(str(value))
    except InvalidOperation:
        return parse_price_text(str(value))
    return price if price > 0 else None
