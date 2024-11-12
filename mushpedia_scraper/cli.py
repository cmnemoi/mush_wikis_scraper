import typer

from mushpedia_scraper.adapters import HttpPageReader
from mushpedia_scraper.usecases.scrap_mushpedia import ScrapeMushpedia
from mushpedia_scraper.links import LINKS

cli = typer.Typer()


@cli.command()
def main(
    limit: int = typer.Option(None, help="Number of pages to scrap. Will scrap all pages if not set."),
    format: str = typer.Option("html", help="Format of the output. Can be `html`, `text` or `markdown`."),
) -> None:
    """Scrap http://mushpedia.com."""
    nb_pages_to_scrap = limit if limit else len(LINKS)

    scraper = ScrapeMushpedia(HttpPageReader())
    pages = scraper.execute(LINKS[:nb_pages_to_scrap], format=format)
    for page in pages:
        print(page)
