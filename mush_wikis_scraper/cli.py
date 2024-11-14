import json

import typer

from mush_wikis_scraper.adapters import HttpPageReader
from mush_wikis_scraper.usecases.scrap_wikis import ScrapWikis
from mush_wikis_scraper.links import LINKS

cli = typer.Typer()


@cli.command()
def main(
    limit: int = typer.Option(None, help="Number of pages to scrap. Will scrap all pages if not set."),
    format: str = typer.Option("html", help="Format of the output. Can be `html`, `text` or `markdown`."),
) -> None:
    """Scrap http://mushpedia.com."""
    nb_pages_to_scrap = limit if limit else len(LINKS)

    scraper = ScrapWikis(HttpPageReader())
    pages = scraper.execute(LINKS[:nb_pages_to_scrap], format=format)
    print(json.dumps(pages, indent=4))
