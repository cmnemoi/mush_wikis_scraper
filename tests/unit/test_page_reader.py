import pytest
from httpx import ConnectError

from mush_wikis_scraper.page_reader import HttpPageReader


class FakeHttpxClient:
    """Fake httpx.AsyncClient for testing retry logic."""

    def __init__(self, failure_count: int = 0) -> None:
        self.failure_count = failure_count
        self.call_count = 0
        self.get_call_count = 0

    async def get(self, path: str) -> "FakeResponse":
        """Simulate HTTP GET request with configurable failures."""
        self.get_call_count += 1
        if self.get_call_count <= self.failure_count:
            raise ConnectError("Connection failed")
        return FakeResponse()

    async def __aenter__(self) -> "FakeHttpxClient":
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        pass


class FakeResponse:
    """Fake httpx.Response for testing."""

    def __init__(self) -> None:
        self.text = "<html><body>Test content</body></html>"


@pytest.mark.asyncio
async def test_http_page_reader_succeeds_on_first_attempt() -> None:
    """Test that HttpPageReader succeeds when no retries are needed."""
    # given an HttpPageReader and a working URL
    page_reader = HttpPageReader()
    fake_client = FakeHttpxClient(failure_count=0)

    # when I fetch the page
    content = await page_reader._get_with_client(fake_client, "https://example.com")

    # then I should get the content
    assert content == "<html><body>Test content</body></html>"
    # and it should only call get once
    assert fake_client.get_call_count == 1


@pytest.mark.asyncio
async def test_http_page_reader_retries_on_connect_error() -> None:
    """Test that HttpPageReader retries on ConnectError and succeeds."""
    # given an HttpPageReader and a URL that fails once before succeeding
    page_reader = HttpPageReader()
    fake_client = FakeHttpxClient(failure_count=1)

    # when I fetch the page
    content = await page_reader._get_with_client(fake_client, "https://example.com")

    # then I should eventually get the content
    assert content == "<html><body>Test content</body></html>"
    # and it should have retried once
    assert fake_client.get_call_count == 2


@pytest.mark.asyncio
async def test_http_page_reader_retries_multiple_times() -> None:
    """Test that HttpPageReader retries multiple times before succeeding."""
    # given an HttpPageReader and a URL that fails twice before succeeding
    page_reader = HttpPageReader()
    fake_client = FakeHttpxClient(failure_count=2)

    # when I fetch the page
    content = await page_reader._get_with_client(fake_client, "https://example.com")

    # then I should eventually get the content
    assert content == "<html><body>Test content</body></html>"
    # and it should have retried twice
    assert fake_client.get_call_count == 3


@pytest.mark.asyncio
async def test_http_page_reader_fails_after_max_retries() -> None:
    """Test that HttpPageReader fails after maximum retries exceeded."""
    # given an HttpPageReader and a URL that always fails
    page_reader = HttpPageReader()
    fake_client = FakeHttpxClient(failure_count=10)  # More than max retries

    # when I try to fetch the page
    # then it should raise a ConnectError after max retries
    with pytest.raises(ConnectError):
        await page_reader._get_with_client(fake_client, "https://example.com")

    # and it should have attempted max_retries + 1 times (initial + retries)
    assert fake_client.get_call_count == 4  # 1 initial + 3 retries
