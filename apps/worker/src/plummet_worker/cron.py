"""Build the crontab line from the check interval in the settings."""


def cron_expression(minutes: int) -> str:
    """Turn an interval in minutes into a cron schedule.

    - Less than 60 minutes: "*/30 * * * *" (every 30 minutes)
    - Whole hours: "0 */2 * * *" (every 2 hours)
    - One day: "0 0 * * *" (every day at midnight)

    Note: cron starts again at minute 0 each hour, so values that do not
    divide 60 (like 45) are not perfectly even.
    """
    if minutes < 1:
        raise ValueError("The interval must be at least 1 minute")
    if minutes < 60:
        return f"*/{minutes} * * * *"
    if minutes == 1440:
        return "0 0 * * *"
    if minutes % 60 == 0 and minutes < 1440:
        return f"0 */{minutes // 60} * * *"
    raise ValueError(
        f"Cron cannot run every {minutes} minutes. "
        "Use less than 60, a whole number of hours, or 1440 (one day)."
    )


def crontab_line(minutes: int, script: str, log_file: str) -> str:
    """The full line to paste in `crontab -e`."""
    return f"{cron_expression(minutes)} {script} >> {log_file} 2>&1"
