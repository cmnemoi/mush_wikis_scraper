"""Links fetcher for eMushpedia wiki articles."""

from abc import ABC, abstractmethod
from typing import Any, Protocol
from urllib.parse import quote

from mush_wikis_scraper.links import LINKS, NON_EMUSHPEDIA_LINKS

EMUSHPEDIA_API_URL = "https://emushpedia.miraheze.org/w/api.php"
EMUSHPEDIA_BASE_URL = "https://emushpedia.miraheze.org/wiki"


class HttpResponse(Protocol):
    """Protocol for HTTP response objects."""

    def json(self) -> dict[str, Any]:
        """Parse response body as JSON.

        Returns:
            dict[str, Any]: Parsed JSON response.
        """
        ...  # pragma: no cover


class HttpClient(Protocol):
    """Protocol for HTTP client objects."""

    async def get(self, url: str) -> HttpResponse:
        """Send GET request to the specified URL.

        Args:
            url (str): The URL to request.

        Returns:
            HttpResponse: The HTTP response.
        """
        ...  # pragma: no cover


class LinksFetcher(ABC):
    """Abstract base class for fetching wiki links."""

    @abstractmethod
    async def get_links(self) -> list[str]:
        """Fetch all wiki links.

        Returns:
            list[str]: List of wiki article URLs.
        """
        pass  # pragma: no cover


class StaticLinksFetcher(LinksFetcher):
    """Fetcher that returns hardcoded links from links.py file."""

    async def get_links(self) -> list[str]:
        """Return hardcoded links from LINKS constant.

        Returns:
            list[str]: List of hardcoded wiki article URLs.
        """
        return LINKS


class EmushpediaApiFetcher(LinksFetcher):
    """Fetcher that retrieves eMushpedia links from MediaWiki API."""

    def __init__(self, http_client: HttpClient) -> None:
        """Initialize the eMushpedia API fetcher.

        Args:
            http_client (HttpClient): HTTP client implementing the HttpClient protocol.
        """
        self.http_client = http_client

    async def get_links(self) -> list[str]:
        """Fetch eMushpedia links from API and combine with non-eMushpedia links.

        Returns:
            list[str]: List of all wiki article URLs (eMushpedia from API + others from file).
        """
        emushpedia_links = await self._fetch_emushpedia_links()
        return emushpedia_links + NON_EMUSHPEDIA_LINKS

    async def _fetch_emushpedia_links(self) -> list[str]:
        all_pages: list[dict[str, Any]] = []
        continue_token: str | None = None

        while True:
            response_data = await self._fetch_api_page(continue_token)

            # Add pages from current response
            if "query" in response_data and "allpages" in response_data["query"]:
                all_pages.extend(response_data["query"]["allpages"])

            # Check if there are more pages to fetch
            if "continue" not in response_data:
                break

            continue_token = response_data["continue"].get("apcontinue")

        # Convert page titles to URLs
        return [self._build_url(page["title"]) for page in all_pages]

    async def _fetch_api_page(self, continue_token: str | None = None) -> dict[str, Any]:
        params = {"action": "query", "list": "allpages", "aplimit": "max", "format": "json"}

        if continue_token:
            params["apcontinue"] = continue_token

        # Build URL with query parameters
        url = f"{EMUSHPEDIA_API_URL}?{'&'.join(f'{key}={value}' for key, value in params.items())}"

        response = await self.http_client.get(url)
        return response.json()

    def _build_url(self, title: str) -> str:
        # Encode special characters (spaces, accents, etc.)
        encoded_title = quote(title, safe="")
        return f"{EMUSHPEDIA_BASE_URL}/{encoded_title}"
