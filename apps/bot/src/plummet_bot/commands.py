"""What each bot command does.

These functions do not know about Telegram. They get the command words and
return the answer text, so they are easy to test.
"""

from decimal import Decimal
from html import escape
from urllib.parse import urlparse

from sqlalchemy.orm import Session

from plummet_core import repository as repo
from plummet_core.messages import format_price
from plummet_core.models import Product
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


def product_line(product: Product) -> str:
    """Show one product in two or three short lines."""
    name = escape(product.name or product.store)
    bell = "🔔" if product.alerts_enabled else "🔕"
    price = format_price(product.last_price, product.currency)
    if product.last_price is None:
        price = "waiting for first check"
    lines = [f'<b>{product.id}.</b> <a href="{escape(product.url, quote=True)}">{name}</a>']
    details = f"   {price} · target {format_price(product.target_price)} · {bell}"
    lines.append(details)
    if product.last_error:
        lines.append(f"   ⚠️ Last check failed: {escape(product.last_error[:80])}")
    return "\n".join(lines)


def list_command(session: Session) -> str:
    products = repo.list_products(session)
    if not products:
        return "You do not track any product yet.\nSend /add <i>url</i> to start."
    lines = [f"📦 <b>Your products ({len(products)})</b>", ""]
    lines += [product_line(p) for p in products]
    return "\n".join(lines)
