"""Connect the commands to Telegram."""

import logging
from collections.abc import Callable

from sqlalchemy import Engine
from sqlalchemy.orm import Session
from telegram import LinkPreviewOptions, Update
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters

from plummet_bot import commands
from plummet_core.db import session_scope

logger = logging.getLogger("plummet.bot")

Command = Callable[[Session, list[str]], str]
NO_PREVIEW = LinkPreviewOptions(is_disabled=True)

COMMANDS: dict[str, Command] = {
    "start": lambda session, args: commands.HELP_TEXT,
    "help": lambda session, args: commands.HELP_TEXT,
    "add": commands.add_command,
    "list": lambda session, args: commands.list_command(session),
    "target": commands.target_command,
    "alerts": commands.alerts_command,
    "remove": commands.remove_command,
}


def make_handler(engine: Engine, command: Command):
    """Run a command in its own database session and send the answer."""

    async def handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        if update.effective_message is None:
            return
        try:
            with session_scope(engine) as session:
                text = command(session, list(context.args or []))
        except commands.CommandError as error:
            text = f"⚠️ {error}"
        except Exception:
            logger.exception("A command failed")
            text = "😕 Something went wrong. Please try again."
        await update.effective_message.reply_html(text, link_preview_options=NO_PREVIEW)

    return handler


async def ignore_stranger(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """The bot is private. We do not answer other people."""
    chat = update.effective_chat
    logger.warning("Message from unknown chat %s was ignored", chat.id if chat else "?")


def register_handlers(app: Application, engine: Engine, chat_id: int) -> None:
    only_owner = filters.Chat(chat_id=chat_id)
    for name, command in COMMANDS.items():
        app.add_handler(CommandHandler(name, make_handler(engine, command), filters=only_owner))
    app.add_handler(MessageHandler(~only_owner, ignore_stranger))
