from typing import Any

import pytest

from mush_wikis_scraper.links import LINKS
from mush_wikis_scraper.links_fetcher import EmushpediaApiFetcher, StaticLinksFetcher


@pytest.mark.asyncio
async def test_static_links_fetcher() -> None:
    # given I have a static links fetcher
    fetcher = StaticLinksFetcher()

    # when I fetch links
    links = await fetcher.get_links()

    # then I should get all links from the LINKS constant
    assert links == LINKS


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

    # then I should get eMushpedia URLs plus non-eMushpedia links (properly encoded)
    assert "https://emushpedia.miraheze.org/wiki/Abn%C3%A9gation" in links
    assert "https://emushpedia.miraheze.org/wiki/Accueil%2Ffr" in links
    assert "https://emushpedia.miraheze.org/wiki/Actions" in links
    # Should also include non-eMushpedia links
    assert any("archive_aide_aux_bolets" in link for link in links)
    # Should call API only once (no pagination needed)
    assert http_client.call_count == 1


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
    http_client = FakeHttpClient([first_response, second_response])

    # when I fetch links from the API
    fetcher = EmushpediaApiFetcher(http_client)
    links = await fetcher.get_links()

    # then I should get pages from both API calls
    assert "https://emushpedia.miraheze.org/wiki/Page_A" in links
    assert "https://emushpedia.miraheze.org/wiki/Page_B" in links
    # Should call API twice (pagination)
    assert http_client.call_count == 2
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

    # then URLs should be properly encoded
    assert "https://emushpedia.miraheze.org/wiki/Title%20with%20spaces" in links
    assert "https://emushpedia.miraheze.org/wiki/%C3%89t%C3%A9" in links
    assert "https://emushpedia.miraheze.org/wiki/L%27apostrophe" in links


@pytest.mark.asyncio
async def test_emushpedia_api_fetcher_combines_with_non_emushpedia() -> None:
    # given I have an API response
    api_response = {
        "batchcomplete": "",
        "query": {"allpages": [{"pageid": 1, "ns": 0, "title": "Test"}]},
    }
    http_client = FakeHttpClient([api_response])

    # when I fetch links from the API
    fetcher = EmushpediaApiFetcher(http_client)
    links = await fetcher.get_links()

    # then I should get both eMushpedia and non-eMushpedia links
    emushpedia_links = [link for link in links if "emushpedia" in link]
    aide_aux_bolets_links = [link for link in links if "archive_aide_aux_bolets" in link]
    forum_links = [link for link in links if "twinoid-archives.netlify.app" in link]

    assert len(emushpedia_links) > 0
    assert len(aide_aux_bolets_links) > 0
    assert len(forum_links) > 0
    # Should have eMushpedia link from API
    assert "https://emushpedia.miraheze.org/wiki/Test" in links
