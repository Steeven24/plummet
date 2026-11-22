from decimal import Decimal

import pytest

from plummet_bot.commands import CommandError, alerts_command, remove_command, target_command
from plummet_core import repository as repo


@pytest.fixture
def product(session):
    return repo.add_product(session, "https://shop.test/a", "shop.test", name="Nice Mouse")


def test_remove(session, product):
    text = remove_command(session, [str(product.id)])

    assert "Stopped tracking Nice Mouse" in text
    assert repo.list_products(session) == []


@pytest.mark.parametrize(("arg", "error"), [("abc", "not a product id"), ("99", "no product")])
def test_remove_bad_id(session, product, arg, error):
    with pytest.raises(CommandError, match=error):
        remove_command(session, [arg])


def test_change_target(session, product):
    text = target_command(session, [str(product.id), "45.5"])

    assert product.target_price == Decimal("45.50")
    assert "45.50 USD" in text


def test_remove_target(session, product):
    target_command(session, [str(product.id), "45"])

    target_command(session, [str(product.id), "none"])

    assert product.target_price is None


def test_turn_alerts_off_and_on(session, product):
    assert "off" in alerts_command(session, [str(product.id), "off"])
    assert product.alerts_enabled is False

    alerts_command(session, [str(product.id), "ON"])
    assert product.alerts_enabled is True


@pytest.mark.parametrize("args", [[], ["1"], ["1", "maybe"]])
def test_alerts_bad_usage(session, product, args):
    with pytest.raises(CommandError, match="Usage"):
        alerts_command(session, args)
