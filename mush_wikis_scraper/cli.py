import json

from tqdm import tqdm
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
    """Scrap http://mushpedia.com/ and http://twin.tithom.fr/mush/."""
    nb_pages_to_scrap = limit if limit else len(LINKS)

    with tqdm(total=nb_pages_to_scrap, desc="Scraping pages") as pbar:
        scraper = ScrapWikis(HttpPageReader(), progress_callback=pbar.update)
        pages = scraper.execute(LINKS[:nb_pages_to_scrap], format=format)
    print(json.dumps(pages, indent=4))
