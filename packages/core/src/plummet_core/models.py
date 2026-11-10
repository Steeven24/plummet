"""Database tables: tracked products and their price history."""

from datetime import UTC, datetime
from decimal import Decimal

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from plummet_core.db import Base
from plummet_core.money import from_cents


def utc_now() -> datetime:
    """Current time in UTC. We save it without timezone because SQLite drops it."""
    return datetime.now(UTC).replace(tzinfo=None)


class Product(Base):
    __tablename__ = "products"

    id: Mapped[int] = mapped_column(primary_key=True)
    url: Mapped[str] = mapped_column(String(2048), unique=True)
    store: Mapped[str] = mapped_column(String(100))
    name: Mapped[str | None] = mapped_column(String(300))
    currency: Mapped[str] = mapped_column(String(3), default="USD")
    target_cents: Mapped[int | None]
    last_price_cents: Mapped[int | None]
    alerts_enabled: Mapped[bool] = mapped_column(default=True)
    last_checked_at: Mapped[datetime | None]
    last_error: Mapped[str | None] = mapped_column(String(500))
    created_at: Mapped[datetime] = mapped_column(default=utc_now)

    prices: Mapped[list["PriceRecord"]] = relationship(
        back_populates="product",
        cascade="all, delete-orphan",
        order_by="PriceRecord.checked_at",
    )

    @property
    def target_price(self) -> Decimal | None:
        return None if self.target_cents is None else from_cents(self.target_cents)

    @property
    def last_price(self) -> Decimal | None:
        return None if self.last_price_cents is None else from_cents(self.last_price_cents)


class PriceRecord(Base):
    """One price we found for a product at a given time."""

    __tablename__ = "price_records"

    id: Mapped[int] = mapped_column(primary_key=True)
    product_id: Mapped[int] = mapped_column(
        ForeignKey("products.id", ondelete="CASCADE"), index=True
    )
    price_cents: Mapped[int]
    checked_at: Mapped[datetime] = mapped_column(default=utc_now, index=True)

    product: Mapped[Product] = relationship(back_populates="prices")

    @property
    def price(self) -> Decimal:
        return from_cents(self.price_cents)
