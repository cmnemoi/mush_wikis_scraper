from concurrent.futures import ThreadPoolExecutor
from multiprocessing import cpu_count

from bs4 import BeautifulSoup

from mushpedia_scraper.ports.page_reader import PageReader

ScrapingResult = dict[str, str]


class ScrapeMushpedia:
    """Use case to scrape mushpedia.com."""

    def __init__(self, page_reader: PageReader) -> None:
        self.page_reader = page_reader

    def execute(self, mushpedia_links: list[str], max_workers: int = -1) -> list[ScrapingResult]:
        """Execute the use case on the given Mushpedia links.

        Args:
            mushpedia_links (list[str]): A list of Mushpedia article links.
            max_workers (int, optional): The maximum number of workers to use. Defaults to -1, which will use 2 * number of CPUs cores available as the maximum number of workers.

        Returns:
            list[ScrapingResult]: A list of scrapped Mushpedia articles with article title, link and content in HTML format.
        """
        nb_workers = self._get_workers(max_workers, mushpedia_links)
        with ThreadPoolExecutor(max_workers=nb_workers) as executor:
            results = list(executor.map(self._scrap_page, mushpedia_links))

        return [
            {"title": link.split("/")[-1], "link": link, "content": result}
            for link, result in zip(mushpedia_links, results)
        ]

    def _scrap_page(self, page_reader_link: str) -> str:
        page_reader = BeautifulSoup(self.page_reader.get(page_reader_link), "html.parser")
        return page_reader.prettify()

    def _get_workers(self, max_workers: int, mushpedia_links: list[str]) -> int:
        workers = max_workers if max_workers > 0 else 2 * cpu_count()

        return min(workers, len(mushpedia_links))
