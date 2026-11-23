"""The JSON shapes the API receives and returns."""

from datetime import UTC, datetime
from decimal import Decimal
from typing import Annotated

from pydantic import BaseModel, ConfigDict, Field, HttpUrl, PlainSerializer


def _as_utc(value: datetime) -> str:
    """The database saves UTC without timezone. Add it, so browsers read it right."""
    return value.replace(tzinfo=UTC).isoformat().replace("+00:00", "Z")


UtcDatetime = Annotated[datetime, PlainSerializer(_as_utc, return_type=str)]


class ProductOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    url: str
    store: str
    name: str | None
    currency: str
    target_price: float | None
    last_price: float | None
    alerts_enabled: bool
    price_selector: str | None
    last_checked_at: UtcDatetime | None
    last_error: str | None
    created_at: UtcDatetime


class ProductCreate(BaseModel):
    url: HttpUrl
    target_price: Decimal | None = Field(default=None, gt=0)
    price_selector: str | None = Field(default=None, max_length=300)


class ProductUpdate(BaseModel):
    """Only the fields that are sent are changed."""

    target_price: Decimal | None = Field(default=None, gt=0)
    alerts_enabled: bool | None = None
    price_selector: str | None = Field(default=None, max_length=300)
