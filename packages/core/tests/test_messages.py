from decimal import Decimal

from plummet_core.alerts import Alert, AlertKind
from plummet_core.messages import alert_message, format_price
from plummet_core.models import Product


def make_product(name="Kindle <16 GB>"):
    return Product(url="https://shop.test/k?a=1&b=2", store="shop.test", name=name, currency="USD")


def test_format_price():
    assert format_price(Decimal("1299.9"), "USD") == "1,299.90 USD"
    assert format_price(Decimal("5")) == "5.00"
    assert format_price(None) == "—"


def test_below_target_message():
    alert = Alert(AlertKind.BELOW_TARGET, Decimal("89"), Decimal("99"), Decimal("90"))

    text = alert_message(make_product(), alert)

    assert "Price under your target" in text
    assert "Now: <b>89.00 USD</b>" in text
    assert "Before: 99.00 USD" in text
    assert "Your target: 90.00 USD" in text


def test_price_drop_message_shows_percent():
    alert = Alert(AlertKind.PRICE_DROP, Decimal("80"), Decimal("100"))

    text = alert_message(make_product(), alert)

    assert "Price drop: -20.0%" in text
    assert "Your target" not in text


def test_message_escapes_html():
    alert = Alert(AlertKind.PRICE_DROP, Decimal("80"), Decimal("100"))

    text = alert_message(make_product(), alert)

    assert "Kindle &lt;16 GB&gt;" in text
    assert 'href="https://shop.test/k?a=1&amp;b=2"' in text


def test_message_uses_url_when_there_is_no_name():
    alert = Alert(AlertKind.PRICE_DROP, Decimal("80"), Decimal("100"))

    assert "https://shop.test/k" in alert_message(make_product(name=None), alert)
