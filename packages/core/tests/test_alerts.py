from decimal import Decimal

from plummet_core.alerts import Alert, AlertKind, detect_alert


def check(old, new, target=None, min_drop=5.0):
    return detect_alert(old, new, target, min_drop)


def test_crossing_the_target_sends_alert():
    alert = check(old=11000, new=9900, target=10000)

    assert alert.kind == AlertKind.BELOW_TARGET
    assert alert.new_price == Decimal("99.00")
    assert alert.target_price == Decimal("100.00")


def test_first_price_under_target_sends_alert():
    assert check(old=None, new=9000, target=10000).kind == AlertKind.BELOW_TARGET


def test_price_equal_to_target_sends_alert():
    assert check(old=10100, new=10000, target=10000).kind == AlertKind.BELOW_TARGET


def test_no_repeat_when_already_under_target():
    assert check(old=9500, new=9400, target=10000) is None


def test_big_drop_sends_alert_while_under_target():
    assert check(old=9500, new=8000, target=10000).kind == AlertKind.PRICE_DROP


def test_big_drop_without_target():
    alert = check(old=10000, new=9000)

    assert alert.kind == AlertKind.PRICE_DROP
    assert alert.drop_percent == 10.0


def test_small_drop_does_not_send_alert():
    assert check(old=10000, new=9600) is None


def test_price_going_up_does_not_send_alert():
    assert check(old=10000, new=12000, target=9000) is None


def test_first_price_without_target_does_not_send_alert():
    assert check(old=None, new=5000) is None


def test_drop_percent_is_none_without_drop():
    alert = Alert(AlertKind.BELOW_TARGET, new_price=Decimal("10"), old_price=None)

    assert alert.drop_percent is None
