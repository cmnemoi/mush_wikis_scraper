from bs4 import BeautifulSoup

from mushpedia_scraper.ports.page_reader import PageReader
from mushpedia_scraper.thread_pool_decorator import thread_pool


class ScrapeMushpedia:
    """Use case to scrape mushpedia.com."""

    def __init__(self, page_reader: PageReader) -> None:
        self.page_reader = page_reader

    @thread_pool
    def execute(self, mushpedia_links: list[str]) -> list[str]:
        """Execute the use case on the given Mushpedia links.

        Args:
            mushpedia_links (list[str]): A list of Mushpedia article links.

        Returns:
            list[str]: A list of scrapped Mushpedia articles in HTML format.
        """
        return mushpedia_links

    def _scrap_page(self, page_reader_link: str) -> str:
        page_reader = BeautifulSoup(self.page_reader.get(page_reader_link), "html.parser")
        return page_reader.prettify()
