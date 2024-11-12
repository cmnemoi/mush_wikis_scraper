from concurrent.futures import ThreadPoolExecutor
from multiprocessing import cpu_count

from bs4 import BeautifulSoup
from html2text import HTML2Text

from mushpedia_scraper.ports.page_reader import PageReader

ScrapingResult = dict[str, str]


class ScrapeMushpedia:
    """Use case to scrape mushpedia.com."""

    def __init__(self, page_reader: PageReader) -> None:
        self.page_reader = page_reader

    def execute(self, mushpedia_links: list[str], max_workers: int = -1, format: str = "html") -> list[ScrapingResult]:
        """Execute the use case on the given Mushpedia links.

        Args:
            mushpedia_links (list[str]): A list of Mushpedia article links.
            max_workers (int, optional): The maximum number of workers to use. Defaults to -1, which will use 2 * number of CPUs cores available.
            format (str, optional): The format of the output. Defaults to "html".

        Returns:
            list[ScrapingResult]: A list of scrapped Mushpedia articles with article title, link and content in HTML format.
        """
        nb_workers = self._get_workers(max_workers, mushpedia_links)
        with ThreadPoolExecutor(max_workers=nb_workers) as executor:
            results = list(executor.map(self._scrap_page, mushpedia_links, [format] * len(mushpedia_links)))

        return [
            {"title": link.split("/")[-1], "link": link, "content": result}
            for link, result in zip(mushpedia_links, results)
        ]

    def _scrap_page(self, page_reader_link: str, format: str) -> str:
        page_reader = BeautifulSoup(self.page_reader.get(page_reader_link), "html.parser")
        match format:
            case "html":
                return page_reader.prettify().replace("\n", "")
            case "text":
                return page_reader.get_text().replace("\n", "")
            case "markdown":
                return HTML2Text().handle(page_reader.prettify())
            case _:
                raise ValueError(f"Unknown format: {format}")

    def _get_workers(self, max_workers: int, mushpedia_links: list[str]) -> int:
        workers = max_workers if max_workers > 0 else 2 * cpu_count()

        return min(workers, len(mushpedia_links))
