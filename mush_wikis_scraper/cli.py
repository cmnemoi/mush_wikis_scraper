import json

import typer
from tqdm import tqdm

from mush_wikis_scraper.adapters import HttpPageReader
from mush_wikis_scraper.links import LINKS
from mush_wikis_scraper.usecases.scrap_wikis import ScrapWikis

cli = typer.Typer()


@cli.command()
def main(
    limit: int = typer.Option(None, help="Number of pages to scrap. Will scrap all pages if not set."),
    format: str = typer.Option("html", help="Format of the output. Can be `html`, `text` or `markdown`."),
    url: list[str] = typer.Option(None, help="List of specific URLs to scrap. Must be URLs from the predefined list."),
) -> None:
    """Scrap http://mushpedia.com/ and http://twin.tithom.fr/mush/."""
    links_to_scrap = _get_links_to_scrap(url)
    nb_pages_to_scrap = limit if limit else len(links_to_scrap)
    links_to_scrap = links_to_scrap[:nb_pages_to_scrap]

    with tqdm(total=len(links_to_scrap), desc="Scraping pages") as progress_bar:
        scraper = ScrapWikis(HttpPageReader(), progress_callback=progress_bar.update)
        pages = scraper.execute(links_to_scrap, format=format)
    print(json.dumps(pages, indent=4, ensure_ascii=False))


def _get_links_to_scrap(url: list[str] | None = None) -> list[str]:
    """Get the list of URLs to scrape based on user input.

    Args:
        url: Optional list of URLs to scrape. If not provided, all URLs from LINKS will be used.

    Returns:
        List of validated URLs to scrape.

    Raises:
        typer.Exit: If any provided URL is not in the predefined list.
    """
    if url is None:
        return LINKS

    # Validate that all provided URLs exist in LINKS
    invalid_urls = [u for u in url if u not in LINKS]
    if invalid_urls:
        typer.echo(f"Error: The following URLs are not in the predefined list: {invalid_urls}", err=True)
        raise typer.Exit(code=1)

    return url
