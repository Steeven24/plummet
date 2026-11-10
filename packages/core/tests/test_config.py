import pytest
from pydantic import ValidationError

from plummet_core.config import Settings


@pytest.fixture(autouse=True)
def clean_env(monkeypatch, tmp_path):
    """Run each test in an empty folder, so a real .env file is not used."""
    monkeypatch.chdir(tmp_path)
    for key in ("PLUMMET_TELEGRAM_BOT_TOKEN", "PLUMMET_TELEGRAM_CHAT_ID"):
        monkeypatch.delenv(key, raising=False)


def test_default_values():
    settings = Settings()

    assert settings.database_url == "sqlite:///data/plummet.db"
    assert settings.max_retries == 3
    assert settings.check_interval_minutes == 30
    assert settings.telegram_enabled is False


def test_reads_env_vars(monkeypatch):
    monkeypatch.setenv("PLUMMET_MAX_RETRIES", "5")
    monkeypatch.setenv("PLUMMET_LOG_LEVEL", "DEBUG")

    settings = Settings()

    assert settings.max_retries == 5
    assert settings.log_level == "DEBUG"


def test_reads_env_file(tmp_path):
    (tmp_path / ".env").write_text("PLUMMET_CHECK_INTERVAL_MINUTES=60\n")

    assert Settings().check_interval_minutes == 60


def test_telegram_enabled_with_token_and_chat(monkeypatch):
    monkeypatch.setenv("PLUMMET_TELEGRAM_BOT_TOKEN", "123:abc")
    monkeypatch.setenv("PLUMMET_TELEGRAM_CHAT_ID", "42")

    settings = Settings()

    assert settings.telegram_enabled is True
    assert "123:abc" not in repr(settings)


def test_rejects_interval_too_short(monkeypatch):
    monkeypatch.setenv("PLUMMET_CHECK_INTERVAL_MINUTES", "1")

    with pytest.raises(ValidationError):
        Settings()
