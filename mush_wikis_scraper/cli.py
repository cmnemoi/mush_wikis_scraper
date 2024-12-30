import json

import typer
from tqdm import tqdm

from mush_wikis_scraper.links import LINKS
from mush_wikis_scraper.page_readers import read_from_http
from mush_wikis_scraper.scrap_wikis import scrap_wikis

cli = typer.Typer()


@cli.command()
def main(
    limit: int = typer.Option(None, help="Number of pages to scrap. Will scrap all pages if not set."),
    format: str = typer.Option("html", help="Format of the output. Can be `html`, `text` or `markdown`."),
    url: list[str] = typer.Option(None, help="List of specific URLs to scrap. Must be URLs from the predefined list."),
) -> None:
    """Scrap http://mushpedia.com/ and http://twin.tithom.fr/mush/."""
    links_to_scrap = _validate_urls(url)
    nb_pages_to_scrap = limit if limit else len(links_to_scrap)
    links_to_scrap = links_to_scrap[:nb_pages_to_scrap]

    with tqdm(total=len(links_to_scrap), desc="Scraping pages") as progress_bar:
        pages = scrap_wikis(
            read_from_http,
            links_to_scrap,
            format=format,
        )
        progress_bar.update(len(links_to_scrap))

    print(json.dumps(pages, indent=4, ensure_ascii=False))


def _validate_urls(urls: list[str] | None = None) -> list[str]:
    if urls is None:
        return LINKS

    invalid_urls = [url for url in urls if url not in LINKS]
    if invalid_urls:
        typer.echo(f"Error: The following URLs are not in the predefined list: {invalid_urls}", err=True)
        raise typer.Exit(code=1)

    return urls
