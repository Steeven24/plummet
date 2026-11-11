"""Download store pages over HTTP."""

from dataclasses import dataclass

import httpx

from plummet_core.config import Settings, get_settings


class FetchError(Exception):
    """The page could not be downloaded."""


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

    def __init__(self, settings: Settings | None = None, client: httpx.Client | None = None):
        self.settings = settings or get_settings()
        self.client = client or httpx.Client(
            headers=build_headers(self.settings),
            timeout=self.settings.request_timeout,
            follow_redirects=True,
        )

    def fetch(self, url: str) -> Page:
        try:
            response = self.client.get(url)
        except httpx.HTTPError as error:
            raise FetchError(f"Could not open {url}: {error}") from error
        if response.status_code >= 400:
            raise FetchError(f"{url} answered with status {response.status_code}")
        return Page(url=str(response.url), status_code=response.status_code, html=response.text)

    def close(self) -> None:
        self.client.close()

    def __enter__(self) -> "Fetcher":
        return self

    def __exit__(self, *args: object) -> None:
        self.close()
