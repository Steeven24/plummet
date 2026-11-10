"""Helpers for money values.

Prices are saved in the database as whole cents (int) to avoid
rounding problems with float numbers.
"""

from decimal import ROUND_HALF_UP, Decimal

CENT = Decimal("0.01")


def to_cents(amount: Decimal | int | float | str) -> int:
    """Turn an amount like Decimal("19.99") into cents (1999)."""
    value = Decimal(str(amount))
    return int((value * 100).quantize(Decimal("1"), rounding=ROUND_HALF_UP))


def from_cents(cents: int) -> Decimal:
    """Turn cents (1999) back into an amount (Decimal("19.99"))."""
    return (Decimal(cents) / 100).quantize(CENT)
