"""Routes with the numbers and alerts for the dashboard."""

from typing import Annotated

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from plummet_api.deps import get_session
from plummet_api.schemas import AlertOut, Overview
from plummet_core import repository as repo
from plummet_core.config import get_settings
from plummet_core.models import Product, utc_now
from plummet_core.stats import savings

router = APIRouter(prefix="/api", tags=["dashboard"])
SessionDep = Annotated[Session, Depends(get_session)]


def is_below_target(product: Product) -> bool:
    if product.last_price is None or product.target_price is None:
        return False
    return product.last_price <= product.target_price


@router.get("/overview", response_model=Overview)
def overview(session: SessionDep):
    products = repo.list_products(session)
    alerts = repo.recent_alerts(session, days=7)
    today = utc_now().date()
    total_savings = sum(
        (savings(repo.price_history(session, p.id, days=30), p.last_price) for p in products),
        start=0,
    )
    currencies = {p.currency for p in products if p.last_price is not None}
    return Overview(
        products=len(products),
        stores=len({p.store for p in products}),
        below_target=sum(is_below_target(p) for p in products),
        alerts_week=len(alerts),
        alerts_today=sum(a.created_at.date() == today for a in alerts),
        savings=float(total_savings),
        currency=currencies.pop() if len(currencies) == 1 else None,
        telegram_enabled=get_settings().telegram_enabled,
    )


@router.get("/alerts", response_model=list[AlertOut])
def alerts(
    session: SessionDep,
    days: int = Query(7, ge=1, le=90),
    limit: int = Query(20, ge=1, le=200),
):
    names = {p.id: p.name or p.store for p in repo.list_products(session)}
    return [
        AlertOut(
            id=a.id,
            product_id=a.product_id,
            product_name=names.get(a.product_id, "Deleted product"),
            kind=a.kind,
            text=a.text,
            delivered=a.delivered,
            error=a.error,
            created_at=a.created_at,
        )
        for a in repo.recent_alerts(session, days=days)[:limit]
    ]
