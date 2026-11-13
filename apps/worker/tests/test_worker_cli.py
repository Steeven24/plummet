import pytest

from plummet_core.config import get_settings
from plummet_worker.lock import RunLock
from plummet_worker.main import main


@pytest.fixture(autouse=True)
def temp_project(tmp_path, monkeypatch):
    """Run each command in an empty folder with its own database."""
    monkeypatch.chdir(tmp_path)
    monkeypatch.setenv("PLUMMET_DATABASE_URL", f"sqlite:///{tmp_path / 'test.db'}")
    get_settings.cache_clear()
    yield tmp_path
    get_settings.cache_clear()


def test_add_product(capsys):
    assert main(["add", "https://www.shop.test/a", "--target", "19.99"]) == 0
    assert "Tracking product 1 from shop.test" in capsys.readouterr().out


def test_add_same_product_twice(capsys):
    main(["add", "https://shop.test/a"])

    assert main(["add", "https://shop.test/a"]) == 1
    assert "Already tracking" in capsys.readouterr().out


def test_run_without_products_works(temp_project):
    assert main(["run"]) == 0
    assert (temp_project / "logs" / "worker.log").exists()


def test_run_is_skipped_when_another_round_is_running(temp_project, caplog):
    with RunLock(temp_project / "data" / "worker.lock"):
        assert main(["run"]) == 0
    assert "Skipping this round" in caplog.text


def test_cron_prints_line(capsys, monkeypatch):
    monkeypatch.setenv("PLUMMET_CHECK_INTERVAL_MINUTES", "15")

    main(["cron"])

    assert capsys.readouterr().out.startswith("*/15 * * * * ")
