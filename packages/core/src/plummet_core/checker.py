"""Check the price of products: download, parse, save and find alerts."""

import logging
from dataclasses import dataclass
from decimal import Decimal

from sqlalchemy.orm import Session

from plummet_core import repository as repo
from plummet_core.alerts import Alert, detect_alert
from plummet_core.config import Settings, get_settings
from plummet_core.fetcher import Fetcher, FetchError
from plummet_core.models import Product
from plummet_core.money import to_cents
from plummet_core.parsing import ParseError, parse_product

logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class CheckResult:
    """What happened when we checked one product."""

    product_id: int
    price: Decimal | None = None
    alert: Alert | None = None
    error: str | None = None

    @property
    def ok(self) -> bool:
        return self.error is None


def check_product(
    session: Session,
    product: Product,
    fetcher: Fetcher,
    settings: Settings | None = None,
) -> CheckResult:
    """Check one product. Errors are saved on the product, they are not raised."""
    settings = settings or get_settings()
    try:
        page = fetcher.fetch(product.url)
        parsed = parse_product(page.html, product.url, product.price_selector)
    except (FetchError, ParseError) as error:
        logger.warning("%s · %s", product.store, error)
        repo.record_error(session, product, str(error))
        return CheckResult(product.id, error=str(error))

    old_cents = product.last_price_cents
    if product.name is None:
        product.name = parsed.name
    if parsed.currency:
        product.currency = parsed.currency
    repo.record_price(session, product, parsed.price)

    alert = detect_alert(
        old_cents, to_cents(parsed.price), product.target_cents, settings.min_drop_percent
    )
    if alert and not product.alerts_enabled:
        alert = None
    logger.info("%s → %s %s", product.store, parsed.price, product.currency)
    return CheckResult(product.id, price=parsed.price, alert=alert)
