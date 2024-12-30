from concurrent.futures import ThreadPoolExecutor
from multiprocessing import cpu_count
from typing import TypedDict

from bs4 import BeautifulSoup
from markdownify import MarkdownConverter  # type: ignore

from mush_wikis_scraper.ports.page_reader import PageReader

ScrapingResult = TypedDict("ScrapingResult", {"title": str, "link": str, "source": str, "content": str})


def scrap_wikis(
    page_reader: PageReader,
    page_links: list[str],
    format: str = "html",
    max_workers: int = -1,
) -> list[ScrapingResult]:
    """Scrape multiple pages in parallel and return their content.

    Args:
        page_reader: The page reader to use
        page_links: List of links to scrape
        format: Format to return the content in ("html", "text", or "markdown")
        max_workers: Maximum number of workers to use, -1 for auto

    Returns:
        List of dictionaries containing page title, link, source and content
    """
    nb_workers = _get_optimal_worker_count(max_workers, len(page_links))

    with ThreadPoolExecutor(max_workers=nb_workers) as executor:
        results = list(executor.map(lambda link: _scrap_single_page(page_reader, link, format), page_links))

    return [result for result in results]


def _get_optimal_worker_count(max_workers: int, links_count: int) -> int:
    """Get the optimal number of workers for parallel scraping.

    Args:
        max_workers: Maximum number of workers to use, -1 for auto
        links_count: Number of links to scrape

    Returns:
        The optimal number of workers to use
    """
    workers = max_workers if max_workers > 0 else 2 * cpu_count()
    return min(workers, links_count)


def _scrap_single_page(page_reader: PageReader, page_link: str, format: str) -> ScrapingResult:
    """Scrape a single page and return its content in the specified format.

    Args:
        page_reader: The page reader to use
        page_link: The link to the page to scrape
        format: The format to return the content in ("html", "text", or "markdown")

    Returns:
        A dictionary containing the page title, link, source and content
    """
    page_parser = BeautifulSoup(page_reader.get(page_link), "html.parser")

    return {
        "title": _get_title_from(page_link, page_parser),
        "link": page_link,
        "source": _get_source_from_link(page_link),
        "content": _format_content(page_parser, format),
    }


def _get_source_from_link(link: str) -> str:
    """Get the source wiki name from a link.

    Args:
        link: The link to get the source from

    Returns:
        The source wiki name

    Raises:
        ValueError: If the source cannot be determined from the link
    """
    if "mushpedia" in link:
        return "Mushpedia"
    elif "twin.tithom.fr" in link:
        return "Twinpedia"
    elif "archive_aide_aux_bolets" in link:
        return "Aide aux Bolets"
    elif "twinoid-archives.netlify.app" in link:
        return "Mush Forums"
    else:
        raise ValueError(f"Unknown source for link: {link}")


def _get_title_from(link: str, page_parser: BeautifulSoup) -> str:
    """Get the title from a link and page parser.

    Args:
        link: The link to get the title from
        page_parser: The BeautifulSoup parser for the page

    Returns:
        The page title

    Raises:
        ValueError: If the title cannot be determined
    """
    source = _get_source_from_link(link)
    parts = link.split("/")

    if source == "Mushpedia":
        return parts[-1]

    if source == "Twinpedia":
        match len(parts):
            case 5:
                return parts[-1].capitalize()
            case 6:
                return f"{parts[-2].capitalize()} - {parts[-1].capitalize()}"
            case 7:
                return f"{parts[-3].capitalize()} - {parts[-2].capitalize()} - {parts[-1].capitalize()}"
            case _:
                raise ValueError(f"Unknown source for link: {link}")

    if source == "Aide aux Bolets" or source == "Mush Forums":
        tag = page_parser.select_one("span.tid_title")
        if tag:
            return tag.text.strip()
        raise ValueError(f"Could not find title for link: {link}")

    raise ValueError(f"Unknown source for link: {link}")


def _format_content(page_parser: BeautifulSoup, format: str) -> str:
    """Format the page content according to the specified format.

    Args:
        page_parser: The BeautifulSoup parser for the page
        format: The format to return ("html", "text", or "markdown")

    Returns:
        The formatted content

    Raises:
        ValueError: If the format is not recognized
    """
    match format:
        case "html":
            return page_parser.prettify().replace("\n", "")
        case "text":
            return page_parser.get_text()
        case "markdown":
            return MarkdownConverter().convert_soup(page_parser)
        case _:
            raise ValueError(f"Unknown format: {format}")
