import pytest

from mush_wikis_scraper import FileSystemPageReader
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
