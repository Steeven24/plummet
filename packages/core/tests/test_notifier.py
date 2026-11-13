from decimal import Decimal

from plummet_core import repository as repo
from plummet_core.alerts import Alert, AlertKind
from plummet_core.checker import CheckResult, CheckSummary
from plummet_core.notifier import NOT_SET_UP, send_alerts
from plummet_core.telegram import TelegramError


class FakeTelegram:
    def __init__(self, fail_on=()):
        self.sent = []
        self.fail_on = fail_on

    def send_message(self, text):
        if any(word in text for word in self.fail_on):
            raise TelegramError("Telegram error 400: chat not found")
        self.sent.append(text)


def make_summary(session, *names):
    results = []
    for name in names:
        product = repo.add_product(session, f"https://shop.test/{name}", "shop.test", name=name)
        alert = Alert(AlertKind.PRICE_DROP, Decimal("8"), Decimal("10"))
        results.append(CheckResult(product.id, price=Decimal("8"), alert=alert))
    results.append(CheckResult(999, error="404"))
    return CheckSummary(results=results)


def test_sends_and_saves_every_alert(session):
    telegram = FakeTelegram()

    delivered = send_alerts(session, make_summary(session, "mouse", "kindle"), telegram)

    assert delivered == 2
    assert len(telegram.sent) == 2
    assert all(a.delivered for a in repo.recent_alerts(session))


def test_failed_message_does_not_stop_others(session):
    telegram = FakeTelegram(fail_on=["mouse"])

    delivered = send_alerts(session, make_summary(session, "mouse", "kindle"), telegram)

    assert delivered == 1
    failed = [a for a in repo.recent_alerts(session) if not a.delivered]
    assert failed[0].error == "Telegram error 400: chat not found"


def test_without_telegram_alerts_are_saved_as_not_sent(session):
    delivered = send_alerts(session, make_summary(session, "mouse"), telegram=None)

    alerts = repo.recent_alerts(session)
    assert delivered == 0
    assert (alerts[0].delivered, alerts[0].error) == (False, NOT_SET_UP)
