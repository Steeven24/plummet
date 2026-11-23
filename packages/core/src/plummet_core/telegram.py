"""Send messages with the Telegram Bot API.

We only need `sendMessage`, so we call the API with httpx and do not need
a big Telegram library here.
"""

import httpx

from plummet_core.config import Settings

API_URL = "https://api.telegram.org"


class TelegramError(Exception):
    """Telegram did not accept the message. The text never has the bot token."""


class TelegramClient:
    def __init__(self, token: str, chat_id: str, client: httpx.Client | None = None):
        self._token = token
        self.chat_id = chat_id
        self.client = client or httpx.Client(timeout=10)

    @classmethod
    def from_settings(cls, settings: Settings) -> "TelegramClient | None":
        """Return a client, or None if the token or chat ID are missing."""
        if not settings.telegram_enabled:
            return None
        token = settings.telegram_bot_token.get_secret_value()  # type: ignore[union-attr]
        return cls(token, str(settings.telegram_chat_id))

    def send_message(self, text: str) -> None:
        payload = {"chat_id": self.chat_id, "text": text, "parse_mode": "HTML"}
        try:
            response = self.client.post(f"{API_URL}/bot{self._token}/sendMessage", json=payload)
        except httpx.HTTPError as error:
            # The error text can include the URL, and the URL has the token.
            raise TelegramError(f"Could not reach Telegram ({type(error).__name__})") from None
        if response.status_code != 200:
            raise TelegramError(f"Telegram error {response.status_code}: {_description(response)}")

    def close(self) -> None:
        self.client.close()


def _description(response: httpx.Response) -> str:
    """Telegram explains the error in the "description" field."""
    try:
        return str(response.json().get("description", "unknown error"))
    except ValueError:
        return "unknown error"
