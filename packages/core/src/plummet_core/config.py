"""App settings loaded from environment variables or a .env file."""

from functools import lru_cache

from pydantic import Field, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """All settings use the PLUMMET_ prefix, for example PLUMMET_LOG_LEVEL."""

    model_config = SettingsConfigDict(
        env_prefix="PLUMMET_",
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    # Database
    database_url: str = "sqlite:///data/plummet.db"

    # Telegram
    telegram_bot_token: SecretStr | None = None
    telegram_chat_id: str | None = None

    # Scraping
    request_timeout: float = Field(default=15.0, gt=0)
    max_retries: int = Field(default=3, ge=0, le=10)
    user_agent: str = (
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/130.0 Safari/537.36"
    )

    # Scheduler
    check_interval_minutes: int = Field(default=30, ge=5)

    # Logging
    log_level: str = "INFO"

    @property
    def telegram_enabled(self) -> bool:
        """True when the bot has a token and a chat to send messages to."""
        return self.telegram_bot_token is not None and self.telegram_chat_id is not None


@lru_cache
def get_settings() -> Settings:
    """Return the settings. They are read only once and then reused."""
    return Settings()
