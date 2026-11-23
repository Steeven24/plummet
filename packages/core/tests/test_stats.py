from datetime import timedelta
from decimal import Decimal

from plummet_core.models import PriceRecord, utc_now
from plummet_core.money import to_cents
from plummet_core.stats import change_in_days, daily_prices, percent_change, savings


def record(price, days_ago=0, hours_ago=0):
    when = utc_now() - timedelta(days=days_ago, hours=hours_ago)
    return PriceRecord(price_cents=to_cents(price), checked_at=when)


def test_daily_prices_keeps_last_price_of_each_day():
    now = utc_now().replace(hour=12)
    records = [
        PriceRecord(price_cents=1000, checked_at=now - timedelta(days=1)),
        PriceRecord(price_cents=900, checked_at=now - timedelta(hours=2)),
        PriceRecord(price_cents=950, checked_at=now),
    ]

    prices = [price for _, price in daily_prices(records)]

    assert prices == [Decimal("10.00"), Decimal("9.50")]


def test_percent_change():
    assert percent_change(Decimal("100"), Decimal("90")) == -10.0
    assert percent_change(None, Decimal("90")) is None
    assert percent_change(Decimal("0"), Decimal("90")) is None


def test_change_in_days_ignores_old_records():
    records = [record("50", days_ago=20), record("100", days_ago=6), record("110")]

    assert change_in_days(records, days=7) == 10.0
    assert change_in_days([record("110")], days=7) is None


def test_savings():
    records = [record("120", days_ago=3), record("100")]

    assert savings(records, Decimal("100")) == Decimal("20.00")
    assert savings(records, None) == Decimal("0")
    assert savings([], Decimal("5")) == Decimal("0")
