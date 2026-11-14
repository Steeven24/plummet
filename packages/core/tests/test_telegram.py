import json

import httpx
import pytest

from plummet_core.config import Settings
from plummet_core.telegram import TelegramClient, TelegramError

TOKEN = "123:secret-token"


def make_client(handler):
    return TelegramClient(TOKEN, "42", client=httpx.Client(transport=httpx.MockTransport(handler)))


def test_send_message():
    sent = []

    def handler(request):
        sent.append(request)
        return httpx.Response(200, json={"ok": True})

    make_client(handler).send_message("<b>Hi</b>")

    assert sent[0].url.path == f"/bot{TOKEN}/sendMessage"
    body = json.loads(sent[0].content)
    assert body == {"chat_id": "42", "text": "<b>Hi</b>", "parse_mode": "HTML"}


def test_api_error_shows_description():
    def handler(request):
        return httpx.Response(400, json={"ok": False, "description": "Bad Request: chat not found"})

    with pytest.raises(TelegramError, match="chat not found"):
        make_client(handler).send_message("Hi")


def test_network_error_does_not_show_token():
    def handler(request):
        raise httpx.ConnectError(f"failed for {request.url}")

    with pytest.raises(TelegramError) as error:
        make_client(handler).send_message("Hi")

    assert TOKEN not in str(error.value)
    assert error.value.__cause__ is None


def test_from_settings():
    assert TelegramClient.from_settings(Settings(telegram_bot_token=None)) is None

    client = TelegramClient.from_settings(Settings(telegram_bot_token=TOKEN, telegram_chat_id="42"))

    assert client.chat_id == "42"
