from mushpedia_scraper.adapters.file_system_page_reader import FileSystemPageReader
from mushpedia_scraper.usecases.scrap_mushpedia import ScrapeMushpedia


def test_run() -> None:
    # given I have page links
    page_links = [
        "tests/data/Game Basics - Mushpedia.html",
        "tests/data/Human Play - Mushpedia.html",
    ]

    # when I run the scraper
    scraper = ScrapeMushpedia(FileSystemPageReader())
    pages = scraper.execute(page_links)

    # then I should get the pages content

    pages_to_string = "\n".join(pages)

    assert "There are two teams of players on the ship. Humans who are trying to save Humanity" in pages_to_string
    assert "Figure out what your character's role is and do it." in pages_to_string
