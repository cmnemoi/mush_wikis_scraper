import asyncio
import json
import logging

import httpx
import typer
from tqdm import tqdm

from mush_wikis_scraper import HttpPageReader, ScrapWikis
from mush_wikis_scraper.links_fetcher import EmushpediaApiFetcher

cli = typer.Typer()

# Configure logging
logging.basicConfig(level=logging.WARNING, format="%(levelname)s: %(message)s")


@cli.command()
def main(
    limit: int = typer.Option(None, help="Number of pages to scrap. Will scrap all pages if not set."),
    format: str = typer.Option(
        "trafilatura-markdown",
        help="Format of the output. Can be `html`, `text`, `markdown`, `trafilatura-markdown`, `trafilatura-html` or `trafilatura-text`.",
    ),
    url: list[str] = typer.Option(None, help="List of specific URLs to scrap. Must be URLs from the predefined list."),
) -> None:
    """Scrap the French, English, and Spanish eMushpedia wikis."""
    asyncio.run(_scrap(limit, format, url))


async def _scrap(limit: int | None, format: str, url: list[str] | None) -> None:
    """Async implementation of the main CLI function."""
    async with httpx.AsyncClient(timeout=60, follow_redirects=True) as http_client:
        links_to_scrap = await _get_links_to_scrap(http_client, url)
        nb_pages_to_scrap = limit if limit else len(links_to_scrap)
        links_to_scrap = links_to_scrap[:nb_pages_to_scrap]

        with tqdm(total=len(links_to_scrap), desc="Scraping pages") as progress_bar:
            scraper = ScrapWikis(HttpPageReader(), progress_callback=progress_bar.update)
            pages = await scraper.execute(links_to_scrap, format=format)
        print(json.dumps(pages, indent=4, ensure_ascii=False))


async def _get_links_to_scrap(http_client: httpx.AsyncClient, url: list[str] | None = None) -> list[str]:
    all_links = await EmushpediaApiFetcher(http_client).get_links()  # @spec supported-wiki::api-only-discovery

    # If specific URLs are provided, validate and filter them
    if url is None:
        return all_links

    # Validate that all provided URLs exist in available links
    invalid_urls = [u for u in url if u not in all_links]
    if invalid_urls:
        typer.echo(f"Error: The following URLs are not in the available links: {invalid_urls}", err=True)
        raise typer.Exit(code=1)

    return url
