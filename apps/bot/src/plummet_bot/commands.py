"""What each bot command does.

These functions do not know about Telegram. They get the command words and
return the answer text, so they are easy to test.
"""

from decimal import Decimal
from html import escape
from urllib.parse import urlparse

from sqlalchemy.orm import Session

from plummet_core import repository as repo
from plummet_core.parsing import store_name
from plummet_core.parsing.price_text import parse_price_text

HELP_TEXT = """<b>Plummet</b> tracks prices and tells you when they go down.

/add <i>url</i> [<i>target</i>] – track a product
/list – see your products
/target <i>id</i> <i>price</i> – change the target price
/alerts <i>id</i> on|off – turn alerts on or off
/remove <i>id</i> – stop tracking a product
/help – show this message"""


class CommandError(Exception):
    """The user wrote the command in a wrong way. The text is shown to them."""


def parse_price(text: str) -> Decimal:
    """Read prices like 99.90, 1,299.99 or 1.299,99."""
    price = parse_price_text(text)
    if price is None:
        raise CommandError(f"“{escape(text)}” is not a valid price. Example: 99.90")
    return price


def parse_url(text: str) -> str:
    parsed = urlparse(text)
    if parsed.scheme not in ("http", "https") or not parsed.netloc:
        raise CommandError("Please send a full link that starts with https://")
    return text


def add_command(session: Session, args: list[str]) -> str:
    if not args:
        raise CommandError("Usage: /add <i>url</i> [<i>target price</i>]")
    url = parse_url(args[0])
    target = parse_price(args[1]) if len(args) > 1 else None
    if existing := repo.get_product_by_url(session, url):
        raise CommandError(f"You already track this product (id {existing.id}).")

    product = repo.add_product(session, url, store_name(url), target_price=target)
    text = f"✅ Tracking product <b>{product.id}</b> from {escape(product.store)}."
    if target is not None:
        text += f"\nI will tell you when it costs {target:,.2f} or less."
    return text + "\nThe first check runs in the next round."
