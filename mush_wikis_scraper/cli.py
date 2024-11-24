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
) -> None:
    """Scrap http://mushpedia.com/ and http://twin.tithom.fr/mush/."""
    nb_pages_to_scrap = limit if limit else len(LINKS)

    with tqdm(total=nb_pages_to_scrap, desc="Scraping pages") as progress_bar:
        scraper = ScrapWikis(HttpPageReader(), progress_callback=progress_bar.update)
        pages = scraper.execute(LINKS[:nb_pages_to_scrap], format=format)
    print(json.dumps(pages, indent=4, ensure_ascii=False))
