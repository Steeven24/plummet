"""Turn price text like "$1,299.99" or "1.299,99 €" into a Decimal."""

import re
from decimal import Decimal, InvalidOperation

_NUMBER = re.compile(r"\d[\d.,\s ]*")
_SPACES = re.compile(r"[\s ]")


def parse_price_text(text: str | None) -> Decimal | None:
    """Return the first price found in the text, or None."""
    match = _NUMBER.search(text or "")
    if not match:
        return None
    raw = _SPACES.sub("", match.group()).rstrip(".,")
    try:
        value = Decimal(_normalize(raw))
    except InvalidOperation:
        return None
    return value if value > 0 else None


def _normalize(raw: str) -> str:
    """Change the number to the "1299.99" format that Decimal understands."""
    last_dot, last_comma = raw.rfind("."), raw.rfind(",")

    if last_dot != -1 and last_comma != -1:
        # Both are used: the last one is the decimal mark ("1,299.99" or "1.299,99").
        decimal_mark = "." if last_dot > last_comma else ","
        thousands = "," if decimal_mark == "." else "."
        return raw.replace(thousands, "").replace(decimal_mark, ".")

    if last_dot == -1 and last_comma == -1:
        return raw

    mark = "." if last_dot != -1 else ","
    parts = raw.split(mark)
    # Groups of 3 digits mean thousands ("2.549" or "1,299,000").
    if len(parts) > 2 or len(parts[-1]) == 3:
        return raw.replace(mark, "")
    return raw.replace(mark, ".")


# The order matters: "US$" and "R$" must be checked before "$".
_CURRENCY_SYMBOLS = [
    ("US$", "USD"),
    ("R$", "BRL"),
    ("S/", "PEN"),
    ("€", "EUR"),
    ("£", "GBP"),
]
_CURRENCY_CODE = re.compile(r"\b(USD|EUR|GBP|MXN|BRL|ARS|COP|CLP|PEN)\b")


def detect_currency(text: str | None) -> str | None:
    """Return the ISO code of the currency in the text, if it is clear.

    A single "$" is used by many countries, so we return None for it.
    """
    text = text or ""
    if match := _CURRENCY_CODE.search(text.upper()):
        return match.group(1)
    for symbol, code in _CURRENCY_SYMBOLS:
        if symbol in text:
            return code
    return None
