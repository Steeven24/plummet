from decimal import Decimal

import pytest

from plummet_core.money import from_cents, to_cents


@pytest.mark.parametrize(
    ("amount", "cents"),
    [(Decimal("19.99"), 1999), ("5", 500), (0.1, 10), (Decimal("2.005"), 201), (0, 0)],
)
def test_to_cents(amount, cents):
    assert to_cents(amount) == cents


def test_from_cents():
    assert from_cents(1999) == Decimal("19.99")
    assert from_cents(500) == Decimal("5.00")


def test_round_trip():
    assert from_cents(to_cents("1234.56")) == Decimal("1234.56")
