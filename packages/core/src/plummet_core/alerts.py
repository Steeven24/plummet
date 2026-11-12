"""Rules that decide when a price change should send an alert."""

from dataclasses import dataclass
from decimal import Decimal
from enum import StrEnum

from plummet_core.money import from_cents


class AlertKind(StrEnum):
    BELOW_TARGET = "below_target"  # The price is now at or under the target
    PRICE_DROP = "price_drop"  # The price went down a lot since the last check


@dataclass(frozen=True)
class Alert:
    kind: AlertKind
    new_price: Decimal
    old_price: Decimal | None = None
    target_price: Decimal | None = None

    @property
    def drop_percent(self) -> float | None:
        """How much the price went down, for example 12.5 (%)."""
        if not self.old_price or self.new_price >= self.old_price:
            return None
        return round(float((self.old_price - self.new_price) / self.old_price * 100), 1)


def detect_alert(
    old_cents: int | None,
    new_cents: int,
    target_cents: int | None,
    min_drop_percent: float,
) -> Alert | None:
    """Return an alert if the new price is good news, or None.

    - BELOW_TARGET only when the price crosses the target. If it was already
      under the target, we do not send the same alert again on every check.
    - PRICE_DROP when the price goes down at least `min_drop_percent`.
    """
    old = None if old_cents is None else from_cents(old_cents)
    new = from_cents(new_cents)
    target = None if target_cents is None else from_cents(target_cents)

    crossed_target = (
        target_cents is not None
        and new_cents <= target_cents
        and (old_cents is None or old_cents > target_cents)
    )
    if crossed_target:
        return Alert(AlertKind.BELOW_TARGET, new, old, target)

    if old_cents and new_cents < old_cents:
        drop = (old_cents - new_cents) / old_cents * 100
        if drop >= min_drop_percent:
            return Alert(AlertKind.PRICE_DROP, new, old, target)
    return None
