import httpx
import pytest

from plummet_core.config import Settings
from plummet_core.fetcher import FetchError, build_headers


def test_returns_page(make_fetcher):
    fetcher, _ = make_fetcher(lambda request: httpx.Response(200, text="<h1>Hi</h1>"))

    page = fetcher.fetch("https://shop.test/a")

    assert page.status_code == 200
    assert page.html == "<h1>Hi</h1>"
    assert page.url == "https://shop.test/a"


def test_not_found_fails_without_retry(make_fetcher):
    calls = []

    def handler(request):
        calls.append(request)
        return httpx.Response(404)

    fetcher, _ = make_fetcher(handler)

    with pytest.raises(FetchError, match="404"):
        fetcher.fetch("https://shop.test/missing")
    assert len(calls) == 1


def test_headers_look_like_a_browser():
    headers = build_headers(Settings(user_agent="TestAgent/1.0"))

    assert headers["User-Agent"] == "TestAgent/1.0"
    assert "text/html" in headers["Accept"]


def test_closes_client_when_used_with_with(make_fetcher):
    fetcher, _ = make_fetcher(lambda request: httpx.Response(200))

    with fetcher:
        pass

    assert fetcher.client.is_closed
