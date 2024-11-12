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
def test_execute(page_data) -> None:
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


@pytest.mark.parametrize(
    "format",
    [
        "html",
        "text",
    ],
)
def test_remove_line_breaks(format: str) -> None:
    # given I have page links
    page_links = ["tests/data/Game Basics"]

    # when I run the scraper
    scraper = ScrapeMushpedia(FileSystemPageReader())
    pages = scraper.execute(page_links, format=format)

    # then I should get the pages content without line breaks
    assert pages[0]["content"].count("\n") == 0


def test_execute_with_html_format() -> None:
    # given I have page links
    page_links = ["tests/data/Game Basics"]

    # when I run the scraper
    scraper = ScrapeMushpedia(FileSystemPageReader())
    pages = scraper.execute(page_links, format="html")

    # then I should get the pages content in HTML format
    assert pages[0]["content"].startswith("<!DOCTYPE html>")


def test_execute_with_text_format() -> None:
    # given I have page links
    page_links = ["tests/data/Game Basics"]

    # when I run the scraper
    scraper = ScrapeMushpedia(FileSystemPageReader())
    pages = scraper.execute(page_links, format="text")

    # then I should get the pages content without HTML tags
    assert "<!DOCTYPE html>" not in pages[0]["content"]


def test_execute_with_markdown_format() -> None:
    # given I have page links
    page_links = ["tests/data/Game Basics"]

    # when I run the scraper
    scraper = ScrapeMushpedia(FileSystemPageReader())
    pages = scraper.execute(page_links, format="markdown")

    # then I should get the pages content in Markdown format
    assert "#  Game Basics" in pages[0]["content"]


def test_execute_with_unknown_format() -> None:
    # given I have page links
    page_links = ["tests/data/Game Basics"]

    # when I run the scraper
    scraper = ScrapeMushpedia(FileSystemPageReader())
    with pytest.raises(ValueError):
        scraper.execute(page_links, format="unknown")
