import typer

from mushpedia_scraper.adapters import HttpPageReader
from mushpedia_scraper.usecases.scrap_mushpedia import ScrapeMushpedia
from mushpedia_scraper.links import LINKS

cli = typer.Typer()


@cli.command()
def main() -> None:
    """Scrap http://mushpedia.com."""
    scraper = ScrapeMushpedia(HttpPageReader())
    pages = scraper.execute(LINKS)
    for page in pages:
        print(page)


if __name__ == "__main__":
    cli()
