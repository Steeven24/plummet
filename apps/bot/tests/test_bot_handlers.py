import asyncio
from types import SimpleNamespace

from telegram.ext import Application, CommandHandler

from plummet_bot.commands import CommandError
from plummet_bot.handlers import COMMANDS, make_handler, register_handlers


class FakeMessage:
    def __init__(self):
        self.replies = []

    async def reply_html(self, text, **kwargs):
        self.replies.append(text)


def run(engine, command, args=()):
    """Call a handler like Telegram does and return the answer."""
    message = FakeMessage()
    update = SimpleNamespace(effective_message=message)
    context = SimpleNamespace(args=list(args))
    asyncio.run(make_handler(engine, command)(update, context))
    return message.replies[0]


def test_handler_sends_command_answer(engine):
    assert run(engine, lambda session, args: f"Hi {args[0]}", ["Ana"]) == "Hi Ana"


def test_handler_shows_command_errors(engine):
    def command(session, args):
        raise CommandError("Usage: /add url")

    assert run(engine, command) == "⚠️ Usage: /add url"


def test_handler_hides_unexpected_errors(engine):
    def command(session, args):
        raise RuntimeError("database is broken")

    answer = run(engine, command)

    assert "Something went wrong" in answer
    assert "database" not in answer


def test_register_handlers_only_for_owner(engine):
    app = Application.builder().token("123:abc").build()

    register_handlers(app, engine, chat_id=42)

    command_handlers = [h for h in app.handlers[0] if isinstance(h, CommandHandler)]
    assert len(command_handlers) == len(COMMANDS)
    assert all(42 in h.filters.chat_ids for h in command_handlers)
