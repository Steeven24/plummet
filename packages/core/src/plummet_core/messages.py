"""Text of the Telegram messages. They use Telegram HTML format."""

from decimal import Decimal
from html import escape

from plummet_core.alerts import Alert, AlertKind
from plummet_core.models import Product


def format_price(price: Decimal | None, currency: str | None = None) -> str:
    """Show a price like "1,299.99 USD"."""
    if price is None:
        return "—"
    text = f"{price:,.2f}"
    return f"{text} {currency}" if currency else text


def alert_title(alert: Alert) -> str:
    if alert.kind == AlertKind.BELOW_TARGET:
        return "🎯 Price under your target!"
    return f"📉 Price drop: -{alert.drop_percent}%"


def alert_message(product: Product, alert: Alert) -> str:
    """Build the alert message for one product."""
    name = escape(product.name or product.url)
    currency = product.currency
    lines = [
        f"<b>{alert_title(alert)}</b>",
        f'<a href="{escape(product.url, quote=True)}">{name}</a>',
        "",
        f"Now: <b>{format_price(alert.new_price, currency)}</b>",
    ]
    if alert.old_price is not None:
        lines.append(f"Before: {format_price(alert.old_price, currency)}")
    if alert.target_price is not None:
        lines.append(f"Your target: {format_price(alert.target_price, currency)}")
    lines.append(f"Store: {escape(product.store)}")
    return "\n".join(lines)
