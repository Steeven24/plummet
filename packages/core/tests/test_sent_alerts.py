from datetime import timedelta

from plummet_core import repository as repo
from plummet_core.models import SentAlert, utc_now


def test_save_and_read_alerts(session):
    product = repo.add_product(session, "https://shop.test/a", "shop.test")
    repo.save_alert(session, product, "price_drop", "Old", delivered=True)
    old = repo.save_alert(session, product, "price_drop", "Too old", delivered=True)
    old.created_at = utc_now() - timedelta(days=10)
    repo.save_alert(session, product, "below_target", "New", delivered=False, error="No bot")

    alerts = repo.recent_alerts(session, days=7)

    assert [a.text for a in alerts] == ["New", "Old"]
    assert alerts[0].error == "No bot"


def test_deleting_product_deletes_its_alerts(session):
    product = repo.add_product(session, "https://shop.test/a", "shop.test")
    repo.save_alert(session, product, "price_drop", "Hi", delivered=True)

    repo.delete_product(session, product.id)

    assert session.query(SentAlert).count() == 0
