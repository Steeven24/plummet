from datetime import timedelta
from decimal import Decimal

from plummet_core import repository as repo
from plummet_core.db import session_scope
from plummet_core.models import utc_now


def seed(engine):
    """Two products: one under its target, and one with an alert."""
    now = utc_now()
    with session_scope(engine) as session:
        mouse = repo.add_product(session, "https://a.test/mouse", "a.test", Decimal("50"))
        repo.record_price(session, mouse, Decimal("60"), checked_at=now - timedelta(days=3))
        repo.record_price(session, mouse, Decimal("45"), checked_at=now)
        kindle = repo.add_product(session, "https://b.test/kindle", "b.test", name="Kindle")
        repo.record_price(session, kindle, Decimal("100"), checked_at=now)
        repo.save_alert(session, kindle, "price_drop", "<b>Drop</b>", delivered=True)
        return mouse.id


def test_products_have_trend_and_change(client, engine):
    seed(engine)

    mouse = client.get("/api/products").json()[0]

    assert mouse["trend"] == [60.0, 45.0]
    assert mouse["change_7d"] == -25.0


def test_price_history(client, engine):
    mouse_id = seed(engine)

    points = client.get(f"/api/products/{mouse_id}/history?days=7").json()

    assert [p["price"] for p in points] == [60.0, 45.0]
    assert client.get("/api/products/999/history").status_code == 404


def test_overview(client, engine):
    seed(engine)

    data = client.get("/api/overview").json()
    data.pop("telegram_enabled")

    assert data == {
        "products": 2,
        "stores": 2,
        "below_target": 1,
        "alerts_week": 1,
        "alerts_today": 1,
        "savings": 15.0,
        "currency": "USD",
    }


def test_alerts(client, engine):
    seed(engine)

    alerts = client.get("/api/alerts").json()

    assert [(a["product_name"], a["kind"], a["delivered"]) for a in alerts] == [
        ("Kindle", "price_drop", True)
    ]
