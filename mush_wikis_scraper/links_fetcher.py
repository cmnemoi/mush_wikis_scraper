"""Links fetcher for eMushpedia wiki articles."""

from typing import Any, Protocol

EMUSHPEDIA_HOSTS = ("fr.emushpedia.com", "en.emushpedia.com", "es.emushpedia.com")


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


class EmushpediaApiFetcher:
    """Fetcher that retrieves eMushpedia links from MediaWiki API."""

    def __init__(self, http_client: HttpClient) -> None:
        """Initialize the eMushpedia API fetcher.

        Args:
            http_client (HttpClient): HTTP client implementing the HttpClient protocol.
        """
        self.http_client = http_client

    async def get_links(self) -> list[str]:
        """Fetch localized eMushpedia links from their APIs.

        Returns:
            list[str]: List of French, English, and Spanish article URLs.
        """
        links: list[str] = []  # @spec supported-wiki::supports-localized-emushpedia
        for host in EMUSHPEDIA_HOSTS:
            links.extend(await self._fetch_emushpedia_links(host))
        return links

    async def _fetch_emushpedia_links(self, host: str) -> list[str]:
        all_pages: list[dict[str, Any]] = []
        continue_token: str | None = None

        while True:
            response_data = await self._fetch_api_page(host, continue_token)

            # Add pages from current response
            if "query" in response_data and "allpages" in response_data["query"]:
                all_pages.extend(response_data["query"]["allpages"])

            # Check if there are more pages to fetch
            if "continue" not in response_data:
                break

            continue_token = response_data["continue"].get("apcontinue")

        # Convert page titles to URLs
        return [self._build_url(host, page["title"]) for page in all_pages]

    async def _fetch_api_page(self, host: str, continue_token: str | None = None) -> dict[str, Any]:
        params = {"action": "query", "list": "allpages", "aplimit": "max", "format": "json"}

        if continue_token:
            params["apcontinue"] = continue_token

        # Build URL with query parameters
        url = f"https://{host}/api.php?{'&'.join(f'{key}={value}' for key, value in params.items())}"

        response = await self.http_client.get(url)
        return response.json()

    def _build_url(self, host: str, title: str) -> str:
        # Replace spaces with underscores (MediaWiki style), keep Unicode raw
        return f"https://{host}/wiki/{title.replace(' ', '_')}"
