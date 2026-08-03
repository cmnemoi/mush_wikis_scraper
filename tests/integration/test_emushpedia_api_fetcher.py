from urllib.parse import urlsplit

import httpx
import pytest

from mush_wikis_scraper.links_fetcher import EmushpediaApiFetcher

SUPPORTED_HOSTS = {"fr.emushpedia.com", "en.emushpedia.com", "es.emushpedia.com"}


@pytest.mark.asyncio
async def test_should_fetch_pages_from_every_supported_emushpedia_api() -> None:
    # Given a real HTTP client
    async with httpx.AsyncClient(timeout=30, follow_redirects=True) as http_client:
        # When links are fetched from eMushpedia
        links = await EmushpediaApiFetcher(http_client).get_links()

    # Then every supported API returns pages and no other host is included
    assert {urlsplit(link).hostname for link in links} == SUPPORTED_HOSTS
