"""Routes to list, add, change and delete products."""

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from plummet_api.deps import get_session
from plummet_api.schemas import ProductCreate, ProductOut, ProductUpdate
from plummet_core import repository as repo
from plummet_core.models import Product
from plummet_core.parsing import store_name

router = APIRouter(prefix="/api/products", tags=["products"])
SessionDep = Annotated[Session, Depends(get_session)]


def get_or_404(session: Session, product_id: int) -> Product:
    product = repo.get_product(session, product_id)
    if product is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Product not found")
    return product


@router.get("", response_model=list[ProductOut])
def list_products(session: SessionDep):
    return repo.list_products(session)


@router.post("", response_model=ProductOut, status_code=status.HTTP_201_CREATED)
def add_product(data: ProductCreate, session: SessionDep):
    url = str(data.url)
    if repo.get_product_by_url(session, url):
        raise HTTPException(status.HTTP_409_CONFLICT, "This product is already tracked")
    return repo.add_product(
        session, url, store_name(url), data.target_price, price_selector=data.price_selector
    )


@router.get("/{product_id}", response_model=ProductOut)
def get_product(product_id: int, session: SessionDep):
    return get_or_404(session, product_id)


@router.patch("/{product_id}", response_model=ProductOut)
def update_product(product_id: int, data: ProductUpdate, session: SessionDep):
    product = get_or_404(session, product_id)
    sent = data.model_fields_set
    if "target_price" in sent:
        repo.set_target_price(session, product, data.target_price)
    if "alerts_enabled" in sent and data.alerts_enabled is not None:
        product.alerts_enabled = data.alerts_enabled
    if "price_selector" in sent:
        product.price_selector = data.price_selector or None
    session.flush()
    return product


@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_product(product_id: int, session: SessionDep) -> None:
    get_or_404(session, product_id)
    repo.delete_product(session, product_id)
