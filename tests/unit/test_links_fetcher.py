from typing import Any

import pytest

from mush_wikis_scraper.links_fetcher import EmushpediaApiFetcher


class FakeHttpResponse:
    """Fake HTTP response implementing HttpResponse protocol."""

    def __init__(self, json_data: dict[str, Any]) -> None:
        """Initialize fake response with JSON data.

        Args:
            json_data (dict[str, Any]): The JSON data to return.
        """
        self._json_data = json_data

    def json(self) -> dict[str, Any]:
        """Return the JSON data.

        Returns:
            dict[str, Any]: The JSON data.
        """
        return self._json_data


class FakeHttpClient:
    """Fake HTTP client implementing HttpClient protocol."""

    def __init__(self, responses: list[dict[str, Any]]) -> None:
        """Initialize fake HTTP client with predefined responses.

        Args:
            responses (list[dict[str, Any]]): List of JSON responses to return sequentially.
        """
        self.responses = responses
        self.call_count = 0
        self.urls_called: list[str] = []

    async def get(self, url: str) -> FakeHttpResponse:
        """Return fake response for the given URL.

        Args:
            url (str): The URL being requested.

        Returns:
            FakeHttpResponse: A fake response object with json() method.
        """
        self.urls_called.append(url)
        response_data = self.responses[self.call_count] if self.call_count < len(self.responses) else {}
        self.call_count += 1
        return FakeHttpResponse(response_data)


@pytest.mark.asyncio
async def test_emushpedia_api_fetcher_single_page() -> None:
    # given I have an API response with less than 500 pages
    api_response = {
        "batchcomplete": "",
        "query": {
            "allpages": [
                {"pageid": 669, "ns": 0, "title": "Abnégation"},
                {"pageid": 125, "ns": 0, "title": "Accueil/fr"},
                {"pageid": 784, "ns": 0, "title": "Actions"},
            ]
        },
    }
    http_client = FakeHttpClient([api_response])

    # when I fetch links from the API
    fetcher = EmushpediaApiFetcher(http_client)
    links = await fetcher.get_links()

    # then I should get French eMushpedia URLs (with raw Unicode)
    assert "https://fr.emushpedia.com/wiki/Abnégation" in links
    assert "https://fr.emushpedia.com/wiki/Accueil/fr" in links
    assert "https://fr.emushpedia.com/wiki/Actions" in links
    assert all(link.startswith("https://fr.emushpedia.com/wiki/") for link in links)
    # Should call each localized API once (no pagination needed)
    assert http_client.call_count == 3


@pytest.mark.asyncio
async def test_emushpedia_api_fetcher_pagination() -> None:
    # given I have an API with pagination (2 pages)
    first_response = {
        "continue": {"apcontinue": "Page_B", "continue": "-||"},
        "query": {"allpages": [{"pageid": 1, "ns": 0, "title": "Page_A"}]},
    }
    second_response = {
        "batchcomplete": "",
        "query": {"allpages": [{"pageid": 2, "ns": 0, "title": "Page_B"}]},
    }
    http_client = FakeHttpClient([first_response, second_response, {}, {}])

    # when I fetch links from the API
    fetcher = EmushpediaApiFetcher(http_client)
    links = await fetcher.get_links()

    # then I should get pages from both API calls
    assert "https://fr.emushpedia.com/wiki/Page_A" in links
    assert "https://fr.emushpedia.com/wiki/Page_B" in links
    # Should paginate the French API and call the other localized APIs once
    assert http_client.call_count == 4
    # Second call should include the continuation parameter
    assert "apcontinue=Page_B" in http_client.urls_called[1]


@pytest.mark.asyncio
async def test_emushpedia_api_fetcher_url_encoding() -> None:
    # given I have an API response with special characters in titles
    api_response = {
        "batchcomplete": "",
        "query": {
            "allpages": [
                {"pageid": 1, "ns": 0, "title": "Title with spaces"},
                {"pageid": 2, "ns": 0, "title": "Été"},
                {"pageid": 3, "ns": 0, "title": "L'apostrophe"},
            ]
        },
    }
    http_client = FakeHttpClient([api_response])

    # when I fetch links from the API
    fetcher = EmushpediaApiFetcher(http_client)
    links = await fetcher.get_links()

    # then URLs should keep raw Unicode, spaces as underscores
    assert "https://fr.emushpedia.com/wiki/Title_with_spaces" in links
    assert "https://fr.emushpedia.com/wiki/Été" in links
    assert "https://fr.emushpedia.com/wiki/L'apostrophe" in links


@pytest.mark.asyncio
async def test_emushpedia_api_fetcher_only_calls_supported_wikis() -> None:
    # given I have an API response
    api_response = {
        "batchcomplete": "",
        "query": {"allpages": [{"pageid": 1, "ns": 0, "title": "Test"}]},
    }
    http_client = FakeHttpClient([api_response])

    # when I fetch links from the API
    fetcher = EmushpediaApiFetcher(http_client)
    links = await fetcher.get_links()

    # then only supported eMushpedia APIs should be called
    assert links == ["https://fr.emushpedia.com/wiki/Test"]
    assert [url.split("/")[2] for url in http_client.urls_called] == [
        "fr.emushpedia.com",
        "en.emushpedia.com",
        "es.emushpedia.com",
    ]  # @spec supported-wiki::supports-localized-emushpedia


@pytest.mark.asyncio
async def test_emushpedia_api_fetcher_returns_all_supported_languages() -> None:
    # Given one page from each localized eMushpedia API
    responses = [{"query": {"allpages": [{"title": title}]}} for title in ("Accueil", "Home", "Inicio")]
    http_client = FakeHttpClient(responses)

    # When links are fetched
    links = await EmushpediaApiFetcher(http_client).get_links()

    # Then all supported localized wikis are returned
    assert links == [
        "https://fr.emushpedia.com/wiki/Accueil",
        "https://en.emushpedia.com/wiki/Home",
        "https://es.emushpedia.com/wiki/Inicio",
    ]  # @spec supported-wiki::supports-localized-emushpedia
