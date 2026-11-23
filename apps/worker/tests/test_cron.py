import pytest

from plummet_worker.cron import cron_expression, crontab_line


@pytest.mark.parametrize(
    ("minutes", "expression"),
    [
        (5, "*/5 * * * *"),
        (30, "*/30 * * * *"),
        (60, "0 */1 * * *"),
        (180, "0 */3 * * *"),
        (1440, "0 0 * * *"),
    ],
)
def test_cron_expression(minutes, expression):
    assert cron_expression(minutes) == expression


@pytest.mark.parametrize("minutes", [0, 90, 2000])
def test_cron_expression_rejects_bad_intervals(minutes):
    with pytest.raises(ValueError):
        cron_expression(minutes)


def test_crontab_line():
    line = crontab_line(30, "/app/deploy/run-worker.sh", "/app/logs/cron.log")

    assert line == "*/30 * * * * /app/deploy/run-worker.sh >> /app/logs/cron.log 2>&1"
