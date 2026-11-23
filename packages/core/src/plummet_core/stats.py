"""Numbers for the dashboard, made from the price history."""

from collections.abc import Sequence
from datetime import date, timedelta
from decimal import Decimal

from plummet_core.models import PriceRecord, utc_now


def daily_prices(records: Sequence[PriceRecord]) -> list[tuple[date, Decimal]]:
    """Keep only the last price of each day, oldest day first."""
    by_day: dict[date, Decimal] = {}
    for record in sorted(records, key=lambda r: r.checked_at):
        by_day[record.checked_at.date()] = record.price
    return list(by_day.items())


def percent_change(old: Decimal | None, new: Decimal | None) -> float | None:
    """For example 100 → 90 is -10.0 (%)."""
    if not old or new is None:
        return None
    return round(float((new - old) / old * 100), 1)


def change_in_days(records: Sequence[PriceRecord], days: int) -> float | None:
    """Percent change from the first price of the last days to the newest price."""
    since = utc_now() - timedelta(days=days)
    recent = sorted((r for r in records if r.checked_at >= since), key=lambda r: r.checked_at)
    if len(recent) < 2:
        return None
    return percent_change(recent[0].price, recent[-1].price)


def savings(records: Sequence[PriceRecord], last_price: Decimal | None) -> Decimal:
    """How much cheaper the product is now than its highest price in the records."""
    if last_price is None or not records:
        return Decimal("0")
    highest = max(r.price for r in records)
    return max(Decimal("0"), highest - last_price)
