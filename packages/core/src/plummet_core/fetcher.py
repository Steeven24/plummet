"""Download store pages over HTTP."""

import time
from collections.abc import Callable
from dataclasses import dataclass

import httpx

from plummet_core.config import Settings, get_settings

# Status codes that can work if we try again later.
RETRY_STATUS = {429, 500, 502, 503, 504}
BACKOFF_SECONDS = 1.0
MAX_WAIT_SECONDS = 30.0


class FetchError(Exception):
    """The page could not be downloaded."""


class _TemporaryError(Exception):
    """An error that can be fixed by trying again."""

    def __init__(self, message: str, wait: float | None = None):
        super().__init__(message)
        self.wait = wait


def parse_retry_after(value: str | None) -> float | None:
    """Read the Retry-After header. We only support the number of seconds.

    Return None when the value is missing or not useful, so the normal wait is used.
    """
    try:
        seconds = float(value) if value else 0.0
    except ValueError:
        return None
    return min(seconds, MAX_WAIT_SECONDS) if seconds > 0 else None


@dataclass(frozen=True)
class Page:
    """A downloaded page."""

    url: str
    status_code: int
    html: str


def build_headers(settings: Settings) -> dict[str, str]:
    """Headers that look like a normal browser, so stores do not block us so fast."""
    return {
        "User-Agent": settings.user_agent,
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.9,es;q=0.8",
    }


class Fetcher:
    """Download pages with one shared HTTP client.

    Use it with `with Fetcher() as fetcher:` so the client is closed at the end.
    """

    def __init__(
        self,
        settings: Settings | None = None,
        client: httpx.Client | None = None,
        sleep: Callable[[float], None] = time.sleep,
    ):
        self.settings = settings or get_settings()
        self.sleep = sleep
        self.client = client or httpx.Client(
            headers=build_headers(self.settings),
            timeout=self.settings.request_timeout,
            follow_redirects=True,
        )

    def fetch(self, url: str) -> Page:
        """Download a page. Try again with a longer wait each time if it fails."""
        attempts = self.settings.max_retries + 1
        for attempt in range(attempts):
            try:
                return self._fetch_once(url)
            except _TemporaryError as error:
                if attempt == attempts - 1:
                    raise FetchError(f"{error} (after {attempts} tries)") from error
                self.sleep(error.wait or BACKOFF_SECONDS * 2**attempt)
        raise AssertionError("unreachable")

    def _fetch_once(self, url: str) -> Page:
        try:
            response = self.client.get(url)
        except httpx.HTTPError as error:
            raise _TemporaryError(f"Could not open {url}: {error}") from error
        if response.status_code in RETRY_STATUS:
            raise _TemporaryError(
                f"{url} answered with status {response.status_code}",
                wait=parse_retry_after(response.headers.get("Retry-After")),
            )
        if response.status_code >= 400:
            raise FetchError(f"{url} answered with status {response.status_code}")
        return Page(url=str(response.url), status_code=response.status_code, html=response.text)

    def close(self) -> None:
        self.client.close()

    def __enter__(self) -> "Fetcher":
        return self

    def __exit__(self, *args: object) -> None:
        self.close()
