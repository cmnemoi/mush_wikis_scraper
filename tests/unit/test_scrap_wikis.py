import logging

import pytest

from mush_wikis_scraper import FileSystemPageReader
from mush_wikis_scraper.page_reader import PageReader
from mush_wikis_scraper.scrap_wikis import ScrapWikis


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "page_data",
    [
        {
            "title": "Introduction au jeu",
            "link": "tests/data/emushpedia.miraheze.org/introduction_au_jeu",
            "source": "eMushpedia",
            "content": "eMush est un jeu via navigateur issu de Mush, initialement développé par Motion Twin, puis repris par la communauté pour continuer à le faire vivre malgré la fermeture définitive de Flash Player.",
        },
        {
            "title": "[A lire] Je débute - Partie 1",
            "link": "tests/data/cmnemoi.github.io/archive_aide_aux_bolets/a-lire-je-debute-partie-1",
            "source": "Aide aux Bolets",
            "content": "Cette première partie sera consacrée aux commandes du jeu et à ses mécanismes.",
        },
        {
            "title": "Q&A #16 (Read the first post!)",
            "link": "tests/data/twinoid-archives.netlify.app/en/mush/mush%20advice/57952519/1.html",
            "source": "Mush Forums",
            "content": "Welcome to the 16th iteration of this thread! Ask your simpler game questions here, and see them answered (usually!)",
        },
    ],
)
async def test_execute(page_data) -> None:
    # given I have page links
    page_links = [page_data["link"]]

    # when I run the scraper
    scraper = ScrapWikis(FileSystemPageReader())
    pages = await scraper.execute(page_links)

    # then I should get the pages content
    page = pages[0]
    assert list(page.keys()) == ["title", "link", "source", "content"]
    assert page["title"] == page_data["title"]
    assert page["link"] == page_data["link"]
    assert page["source"] == page_data["source"]
    assert page_data["content"] in page["content"]


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "format",
    ["html"],
)
async def test_remove_line_breaks(format: str) -> None:
    # given I have page links
    page_links = ["tests/data/emushpedia.miraheze.org/introduction-au-jeu"]

    # when I run the scraper
    scraper = ScrapWikis(FileSystemPageReader())
    pages = await scraper.execute(page_links, format=format)

    # then I should get the pages content without line breaks
    assert pages[0]["content"].count("\n") == 0


@pytest.mark.asyncio
async def test_execute_with_html_format() -> None:
    # given I have page links
    page_links = ["tests/data/emushpedia.miraheze.org/introduction-au-jeu"]

    # when I run the scraper
    scraper = ScrapWikis(FileSystemPageReader())
    pages = await scraper.execute(page_links, format="html")

    # then I should get the pages content in HTML format
    assert pages[0]["content"].startswith("<!DOCTYPE html>")


@pytest.mark.asyncio
async def test_execute_with_text_format() -> None:
    # given I have page links
    page_links = ["tests/data/emushpedia.miraheze.org/introduction-au-jeu"]

    # when I run the scraper
    scraper = ScrapWikis(FileSystemPageReader())
    pages = await scraper.execute(page_links, format="text")

    # then I should get the pages content without HTML tags
    assert "<!DOCTYPE html>" not in pages[0]["content"]


@pytest.mark.asyncio
async def test_execute_with_markdown_format() -> None:
    # given I have page links
    page_links = ["tests/data/emushpedia.miraheze.org/introduction-au-jeu"]

    # when I run the scraper
    scraper = ScrapWikis(FileSystemPageReader())
    pages = await scraper.execute(page_links, format="markdown")

    # then I should get the pages content in Markdown format
    assert "Introduction au jeu\n===================" in pages[0]["content"]


@pytest.mark.asyncio
async def test_execute_with_trafilatura_markdown_format() -> None:
    # given I have page links
    page_links = ["tests/data/emushpedia.miraheze.org/introduction-au-jeu"]

    # when I run the scraper
    scraper = ScrapWikis(FileSystemPageReader())
    pages = await scraper.execute(page_links, format="trafilatura-markdown")

    # then I should get the pages content in Markdown trafilatura format
    assert "# Introduction au jeu" in pages[0]["content"]


@pytest.mark.asyncio
async def test_execute_with_trafilatura_html_format() -> None:
    # given I have page links
    page_links = ["tests/data/emushpedia.miraheze.org/introduction-au-jeu"]

    # when I run the scraper
    scraper = ScrapWikis(FileSystemPageReader())
    pages = await scraper.execute(page_links, format="trafilatura-html")

    # then I should get the pages content in HTML trafilatura format
    assert "<h1>Introduction au jeu</h1>" in pages[0]["content"]


@pytest.mark.asyncio
async def test_execute_with_trafilatura_text_format() -> None:
    # given I have page links
    page_links = ["tests/data/emushpedia.miraheze.org/introduction-au-jeu"]

    # when I run the scraper
    scraper = ScrapWikis(FileSystemPageReader())
    pages = await scraper.execute(page_links, format="trafilatura-text")

    # then I should get the pages content in text trafilatura format
    assert "# Introduction au jeu\n\n###\nQu'est-ce que\n*\neMush\n" in pages[0]["content"]


@pytest.mark.asyncio
async def test_execute_with_unknown_format() -> None:
    # given I have page links
    page_links = ["tests/data/emushpedia.miraheze.org/introduction-au-jeu"]

    # when I run the scraper
    scraper = ScrapWikis(FileSystemPageReader())
    with pytest.raises(ValueError):
        await scraper.execute(page_links, format="unknown")


class FakeFailingPageReader:
    """Fake PageReader that always fails."""

    async def get(self, path: str) -> str:
        """Always raise an exception."""
        raise RuntimeError(f"Failed to fetch: {path}")


@pytest.mark.asyncio
async def test_execute_handles_individual_page_failures() -> None:
    """Test that ScrapWikis continues scraping even when some pages fail."""
    # given I have a mix of working and failing page links
    page_links = [
        "tests/data/emushpedia.miraheze.org/introduction-au-jeu",
        "https://failing-page.com/page1",
        "tests/data/cmnemoi.github.io/archive_aide_aux_bolets/a-lire-je-debute-partie-1",
    ]

    # and a page reader that fails for some pages
    class SelectiveFailingPageReader(PageReader):
        async def get(self, path: str) -> str:
            if "failing-page" in path:
                raise RuntimeError(f"Failed to fetch: {path}")
            return await FileSystemPageReader().get(path)

    scraper = ScrapWikis(SelectiveFailingPageReader())

    # when I run the scraper
    pages = await scraper.execute(page_links)

    # then I should get results only for successful pages
    assert len(pages) == 2
    # and successful pages should have content
    assert pages[0]["title"] == "Introduction-au-jeu"
    assert pages[1]["title"] == "[A lire] Je débute - Partie 1"
    # and failed pages are logged but not in results


@pytest.mark.asyncio
async def test_execute_continues_after_page_failure() -> None:
    """Test that ScrapWikis continues scraping after encountering a failure."""
    # given I have multiple page links where the first one fails
    page_links = [
        "https://failing-page.com/page1",
        "tests/data/emushpedia.miraheze.org/introduction-au-jeu",
    ]

    # and a page reader that fails for the first page
    class SelectiveFailingPageReader(PageReader):
        async def get(self, path: str) -> str:
            if "failing-page" in path:
                raise RuntimeError(f"Failed to fetch: {path}")
            return await FileSystemPageReader().get(path)

    scraper = ScrapWikis(SelectiveFailingPageReader())

    # when I run the scraper
    pages = await scraper.execute(page_links)

    # then I should get results only for successful pages
    assert len(pages) == 1
    # and the second page should be successfully scraped
    assert pages[0]["title"] == "Introduction-au-jeu"
    assert "eMush est un jeu" in pages[0]["content"]


@pytest.mark.asyncio
async def test_execute_logs_failed_pages(caplog: pytest.LogCaptureFixture) -> None:
    """Test that ScrapWikis logs failed pages as warnings."""
    # given I have a page that will fail
    page_links = ["https://failing-page.com/page1"]

    # and a page reader that fails
    class FailingPageReader(PageReader):
        async def get(self, path: str) -> str:
            raise RuntimeError("Connection failed")

    scraper = ScrapWikis(FailingPageReader())

    # when I run the scraper with logging enabled
    with caplog.at_level(logging.WARNING):
        pages = await scraper.execute(page_links)

    # then the error should be logged as a warning
    assert len(caplog.records) == 1
    assert caplog.records[0].levelname == "WARNING"
    assert "Failed to scrape page https://failing-page.com/page1" in caplog.records[0].message
    assert "Connection failed" in caplog.records[0].message
    # and no results should be returned
    assert len(pages) == 0
