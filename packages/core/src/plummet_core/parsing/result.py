"""What a parser returns."""

from dataclasses import dataclass
from decimal import Decimal


class ParseError(Exception):
    """We could not find a price on the page."""


@dataclass(frozen=True)
class ParsedProduct:
    """Data we found on a product page."""

    price: Decimal
    name: str | None = None
    currency: str | None = None
