import pytest

from mush_wikis_scraper.page_readers import read_from_filesystem
from mush_wikis_scraper.scrap_wikis import scrap_wikis


@pytest.mark.parametrize(
    "page_data",
    [
        {
            "title": "Game Basics",
            "link": "tests/data/mushpedia.com/Game Basics",
            "source": "Mushpedia",
            "content": "There are two teams of players on the ship. Humans who are trying to save Humanity",
        },
        {
            "title": "Human Play",
            "link": "tests/data/mushpedia.com/Human Play",
            "source": "Mushpedia",
            "content": "Figure out what your character's role is and do it.",
        },
        {
            "title": "Personnages - Pnj",
            "link": "tests/data/twin.tithom.fr/mush/personnages/pnj",
            "source": "Twinpedia",
            "content": "NERON est l'intelligence artifcielle de bord, sa puissance de calcul est indispensable à l'opération du PILGRED.",
        },
        {
            "title": "Pilgred",
            "link": "tests/data/twin.tithom.fr/mush/pilgred",
            "source": "Twinpedia",
            "content": "Si la réparation du PILGRED est complétée avant la décryogénisation de tous, il est possible de rentrer sur Sol. Aucun point de triomphe n'est perdu pour le retour sur Sol avant la désignation des Mush, puisqu'il n'y a techniquement aucun membre Mush à bord du Daedalus, à ce moment.",
        },
        {
            "title": "Exploration - Sections - Rencontres",
            "link": "tests/data/twin.tithom.fr/mush/exploration/sections/rencontres",
            "source": "Twinpedia",
            "content": "Truc enorme qui bouffe les joueurs un par un",
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
def test_execute(page_data) -> None:
    # given I have page links
    page_links = [page_data["link"]]

    # when I run the scraper
    pages = scrap_wikis(read_from_filesystem, page_links)

    # then I should get the pages content
    page = pages[0]
    assert list(page.keys()) == ["title", "link", "source", "content"]
    assert page["title"] == page_data["title"]
    assert page["link"] == page_data["link"]
    assert page["source"] == page_data["source"]
    assert page_data["content"] in page["content"]


@pytest.mark.parametrize(
    "format",
    ["html"],
)
def test_remove_line_breaks(format: str) -> None:
    # given I have page links
    page_links = ["tests/data/mushpedia.com/Game Basics"]

    # when I run the scraper
    pages = scrap_wikis(read_from_filesystem, page_links, format=format)

    # then I should get the pages content without line breaks
    assert pages[0]["content"].count("\n") == 0


def test_execute_with_html_format() -> None:
    # given I have page links
    page_links = ["tests/data/mushpedia.com/Game Basics"]

    # when I run the scraper
    pages = scrap_wikis(read_from_filesystem, page_links, format="html")

    # then I should get the pages content in HTML format
    assert pages[0]["content"].startswith("<!DOCTYPE html>")


def test_execute_with_text_format() -> None:
    # given I have page links
    page_links = ["tests/data/mushpedia.com/Game Basics"]

    # when I run the scraper
    pages = scrap_wikis(read_from_filesystem, page_links, format="text")

    # then I should get the pages content without HTML tags
    assert "<!DOCTYPE html>" not in pages[0]["content"]


def test_execute_with_markdown_format() -> None:
    # given I have page links
    page_links = ["tests/data/mushpedia.com/Game Basics"]

    # when I run the scraper
    pages = scrap_wikis(read_from_filesystem, page_links, format="markdown")

    # then I should get the pages content in Markdown format
    assert "Game Basics\n===========" in pages[0]["content"]


def test_execute_with_unknown_format() -> None:
    # given I have page links
    page_links = ["tests/data/mushpedia.com/Game Basics"]

    # when I run the scraper
    with pytest.raises(ValueError):
        scrap_wikis(read_from_filesystem, page_links, format="unknown")
