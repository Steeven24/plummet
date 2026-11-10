"""Functions to read and save data. Apps use these instead of writing queries."""

from decimal import Decimal

from sqlalchemy import select
from sqlalchemy.orm import Session

from plummet_core.models import Product
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
