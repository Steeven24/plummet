"""Start the Telegram bot: `plummet-bot`."""

import logging

from telegram import BotCommand
from telegram.ext import Application

from plummet_bot.handlers import register_handlers
from plummet_core.config import get_settings
from plummet_core.db import init_db, make_engine

logger = logging.getLogger("plummet.bot")

MENU = [
    BotCommand("list", "See your products"),
    BotCommand("add", "Track a product: /add url [target]"),
    BotCommand("target", "Change a target: /target id price"),
    BotCommand("alerts", "Turn alerts on or off: /alerts id on|off"),
    BotCommand("remove", "Stop tracking: /remove id"),
    BotCommand("help", "Show all commands"),
]


async def set_menu(app: Application) -> None:
    """Show the commands in the Telegram menu."""
    await app.bot.set_my_commands(MENU)


def main() -> int:
    settings = get_settings()
    logging.basicConfig(
        level=settings.log_level.upper(),
        format="%(asctime)s  %(levelname)-5s  %(message)s",
    )
    # httpx writes every request URL in the logs, and the URL has the bot token.
    logging.getLogger("httpx").setLevel(logging.WARNING)

    if not settings.telegram_enabled:
        print("Set PLUMMET_TELEGRAM_BOT_TOKEN and PLUMMET_TELEGRAM_CHAT_ID first.")
        return 1

    engine = make_engine()
    init_db(engine)
    token = settings.telegram_bot_token.get_secret_value()  # type: ignore[union-attr]
    app = Application.builder().token(token).post_init(set_menu).build()
    register_handlers(app, engine, int(str(settings.telegram_chat_id)))

    logger.info("Bot started. Press Ctrl+C to stop.")
    app.run_polling()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
