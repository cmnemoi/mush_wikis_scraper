import pytest

from mushpedia_scraper.adapters.file_system_page_reader import FileSystemPageReader
from mushpedia_scraper.usecases.scrap_mushpedia import ScrapeMushpedia


@pytest.mark.parametrize(
    "page_data",
    [
        {
            "title": "Game Basics",
            "link": "tests/data/Game Basics",
            "expected_content": "There are two teams of players on the ship. Humans who are trying to save Humanity",
        },
        {
            "title": "Human Play",
            "link": "tests/data/Human Play",
            "expected_content": "Figure out what your character's role is and do it.",
        },
    ],
)
def test_run(page_data) -> None:
    # given I have page links
    page_links = [page_data["link"]]

    # when I run the scraper
    scraper = ScrapeMushpedia(FileSystemPageReader())
    pages = scraper.execute(page_links)

    # then I should get the pages content
    page = pages[0]
    assert list(page.keys()) == ["title", "link", "content"]
    assert page["title"] == page_data["title"]
    assert page["link"] == page_data["link"]
    assert page_data["expected_content"] in page["content"]


def test_remove_line_breaks() -> None:
    # given I have page links
    page_links = ["tests/data/Game Basics"]

    # when I run the scraper
    scraper = ScrapeMushpedia(FileSystemPageReader())
    pages = scraper.execute(page_links)

    # then I should get the pages content without line breaks
    assert pages[0]["content"].count("\n") == 0
