import httpx
import pytest

from plummet_core.fetcher import FetchError, parse_retry_after


def fails_then_works(*statuses):
    """A fake server that answers with these statuses first, and then 200."""
    answers = list(statuses)

    def handler(request):
        return httpx.Response(answers.pop(0) if answers else 200, text="ok")

    return handler


def test_retries_server_errors_and_waits_more_each_time(make_fetcher):
    fetcher, waits = make_fetcher(fails_then_works(503, 500, 502))

    page = fetcher.fetch("https://shop.test/a")

    assert page.html == "ok"
    assert waits == [1.0, 2.0, 4.0]


def test_gives_up_after_max_retries(make_fetcher):
    fetcher, waits = make_fetcher(fails_then_works(503, 503, 503), retries=2)

    with pytest.raises(FetchError, match="after 3 tries"):
        fetcher.fetch("https://shop.test/a")
    assert len(waits) == 2


def test_retries_network_errors(make_fetcher):
    calls = []

    def handler(request):
        calls.append(request)
        if len(calls) == 1:
            raise httpx.ConnectTimeout("too slow")
        return httpx.Response(200, text="ok")

    fetcher, _ = make_fetcher(handler)

    assert fetcher.fetch("https://shop.test/a").html == "ok"


def test_uses_retry_after_header(make_fetcher):
    answers = [httpx.Response(429, headers={"Retry-After": "7"}), httpx.Response(200)]
    fetcher, waits = make_fetcher(lambda request: answers.pop(0))

    fetcher.fetch("https://shop.test/a")

    assert waits == [7.0]


@pytest.mark.parametrize(
    ("value", "wait"),
    [("5", 5.0), ("120", 30.0), (None, None), ("soon", None), ("-3", None), ("0", None)],
)
def test_parse_retry_after(value, wait):
    assert parse_retry_after(value) == wait
