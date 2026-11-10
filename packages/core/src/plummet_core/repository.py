"""Functions to read and save data. Apps use these instead of writing queries."""

from datetime import datetime, timedelta
from decimal import Decimal

from sqlalchemy import select
from sqlalchemy.orm import Session

from plummet_core.models import PriceRecord, Product, utc_now
from plummet_core.money import to_cents


def add_product(
    session: Session,
    url: str,
    store: str,
    target_price: Decimal | None = None,
    name: str | None = None,
    currency: str = "USD",
) -> Product:
    product = Product(
        url=url,
        store=store,
        name=name,
        currency=currency,
        target_cents=None if target_price is None else to_cents(target_price),
    )
    session.add(product)
    session.flush()
    return product


def get_product(session: Session, product_id: int) -> Product | None:
    return session.get(Product, product_id)


def get_product_by_url(session: Session, url: str) -> Product | None:
    return session.scalar(select(Product).where(Product.url == url))


def list_products(session: Session) -> list[Product]:
    return list(session.scalars(select(Product).order_by(Product.created_at)))


def set_target_price(session: Session, product: Product, target_price: Decimal | None) -> None:
    product.target_cents = None if target_price is None else to_cents(target_price)
    session.flush()


def delete_product(session: Session, product_id: int) -> bool:
    """Delete a product and its price history. Return False if it does not exist."""
    product = get_product(session, product_id)
    if product is None:
        return False
    session.delete(product)
    session.flush()
    return True


def record_price(
    session: Session,
    product: Product,
    price: Decimal,
    checked_at: datetime | None = None,
) -> PriceRecord:
    """Save a new price and update the last price of the product."""
    checked_at = checked_at or utc_now()
    record = PriceRecord(product=product, price_cents=to_cents(price), checked_at=checked_at)
    product.last_price_cents = record.price_cents
    product.last_checked_at = checked_at
    product.last_error = None
    session.add(record)
    session.flush()
    return record


def record_error(session: Session, product: Product, message: str) -> None:
    """Save why the last check failed, so we can show it in the dashboard."""
    product.last_error = message[:500]
    product.last_checked_at = utc_now()
    session.flush()


def price_history(session: Session, product_id: int, days: int = 30) -> list[PriceRecord]:
    """Return the prices of the last days, oldest first."""
    since = utc_now() - timedelta(days=days)
    query = (
        select(PriceRecord)
        .where(PriceRecord.product_id == product_id, PriceRecord.checked_at >= since)
        .order_by(PriceRecord.checked_at)
    )
    return list(session.scalars(query))
