"""Fill an empty database with example data, to try the dashboard."""

import random
from datetime import timedelta
from decimal import Decimal

from sqlalchemy.orm import Session

from plummet_core import repository as repo
from plummet_core.alerts import Alert, AlertKind
from plummet_core.messages import alert_message
from plummet_core.models import utc_now

# name, store, currency, price today, target, alerts on
PRODUCTS = [
    ("Sony WH-1000XM5 Headphones", "amazon.com", "USD", "329.99", "299", True),
    ("Kindle Paperwhite 16 GB", "mercadolibre.com.mx", "MXN", "2549", "2600", True),
    ("Logitech MX Master 3S Mouse", "amazon.com", "USD", "89.99", "79", True),
    ('LG 27" 4K UHD Monitor', "bestbuy.com", "USD", "296.99", "280", True),
    ("Ninja Air Fryer 5.5 L", "target.com", "USD", "119.00", "99", False),
]


def make_history(today: Decimal, days: int, rng: random.Random) -> list[Decimal]:
    """Prices of the last days (oldest first) that end at today's price."""
    prices = [today]
    for _ in range(days - 1):
        step = Decimal(str(rng.uniform(-0.018, 0.02))) * prices[0]
        prices.insert(0, (prices[0] - step).quantize(Decimal("0.01")))
    return prices


def fill_demo_data(session: Session, days: int = 90, seed: int = 7) -> int:
    """Add example products, prices, alerts and rounds. Return the product count."""
    rng = random.Random(seed)
    now = utc_now()
    for index, (name, store, currency, price, target, alerts_on) in enumerate(PRODUCTS):
        url = f"https://www.{store}/demo-{index + 1}"
        product = repo.add_product(session, url, store, Decimal(target), name, currency)
        product.alerts_enabled = alerts_on
        history = make_history(Decimal(price), days, rng)
        for day, value in enumerate(history):
            repo.record_price(session, product, value, now - timedelta(days=days - 1 - day))
        alert = Alert(AlertKind.PRICE_DROP, history[-1], history[-2] * Decimal("1.07"))
        if history[-1] <= Decimal(target):
            alert = Alert(AlertKind.BELOW_TARGET, history[-1], history[-2], Decimal(target))
        if alerts_on and index < 3:
            repo.save_alert(session, product, alert.kind, alert_message(product, alert), True)
    for step in range(48):
        started = now - timedelta(minutes=30 * step + 8)
        errors = 1 if step % 9 == 4 else 0
        repo.record_run(session, started, round(rng.uniform(9, 18), 1), len(PRODUCTS), 0, errors)
    return len(PRODUCTS)
