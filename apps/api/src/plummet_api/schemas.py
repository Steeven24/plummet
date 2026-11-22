"""The JSON shapes the API receives and returns."""

from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field, HttpUrl


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
    last_checked_at: datetime | None
    last_error: str | None
    created_at: datetime


class ProductCreate(BaseModel):
    url: HttpUrl
    target_price: Decimal | None = Field(default=None, gt=0)
    price_selector: str | None = Field(default=None, max_length=300)


class ProductUpdate(BaseModel):
    """Only the fields that are sent are changed."""

    target_price: Decimal | None = Field(default=None, gt=0)
    alerts_enabled: bool | None = None
    price_selector: str | None = Field(default=None, max_length=300)
