"""Send the alerts found in a round and save them."""

import logging

from sqlalchemy.orm import Session

from plummet_core import repository as repo
from plummet_core.checker import CheckSummary
from plummet_core.messages import alert_message
from plummet_core.telegram import TelegramClient, TelegramError

logger = logging.getLogger(__name__)

NOT_SET_UP = "Telegram is not set up"


def send_alerts(
    session: Session,
    summary: CheckSummary,
    telegram: TelegramClient | None,
) -> int:
    """Send one message per alert. Return how many were delivered.

    Every alert is saved, also the ones that fail, so the dashboard can show
    them. A failed message does not stop the others.
    """
    if summary.alerts and telegram is None:
        logger.warning("%s, so %d alerts were not sent", NOT_SET_UP, len(summary.alerts))

    delivered = 0
    for result in summary.alerts:
        product = repo.get_product(session, result.product_id)
        if product is None or result.alert is None:
            continue
        text = alert_message(product, result.alert)
        error = NOT_SET_UP if telegram is None else _send(telegram, text)
        repo.save_alert(
            session, product, result.alert.kind, text, delivered=error is None, error=error
        )
        if error is None:
            delivered += 1
            logger.info("telegram · alert sent for %s", product.store)
    return delivered


def _send(telegram: TelegramClient, text: str) -> str | None:
    """Send the message and return the error text, or None if it worked."""
    try:
        telegram.send_message(text)
    except TelegramError as error:
        logger.warning("telegram · %s", error)
        return str(error)
    return None
