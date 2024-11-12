from bs4 import BeautifulSoup

from mushpedia_scraper.ports.page_reader import PageReader

ScrapingResult = dict[str, str]


class ScrapeMushpedia:
    """Use case to scrape mushpedia.com."""

    def __init__(self, page_reader: PageReader) -> None:
        self.page_reader = page_reader

    def execute(self, mushpedia_links: list[str]) -> list[ScrapingResult]:
        """Execute the use case on the given Mushpedia links.

        Args:
            mushpedia_links (list[str]): A list of Mushpedia article links.

        Returns:
            list[ScrapingResult]: A list of scrapped Mushpedia articles with article title, link and content in HTML format.
        """
        return [
            {"title": link.split("/")[-1], "link": link, "content": self._scrap_page(link)} for link in mushpedia_links
        ]

    def _scrap_page(self, page_reader_link: str) -> str:
        page_reader = BeautifulSoup(self.page_reader.get(page_reader_link), "html.parser")
        return page_reader.prettify()
