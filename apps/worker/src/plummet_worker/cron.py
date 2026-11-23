"""Build the crontab line from the check interval in the settings."""

from plummet_core.schedule import cron_expression

__all__ = ["cron_expression", "crontab_line"]


def crontab_line(minutes: int, script: str, log_file: str) -> str:
    """The full line to paste in `crontab -e`."""
    return f"{cron_expression(minutes)} {script} >> {log_file} 2>&1"
