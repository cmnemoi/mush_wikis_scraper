from concurrent.futures import ThreadPoolExecutor, as_completed
from multiprocessing import cpu_count

from bs4 import BeautifulSoup

from mushpedia_scraper.ports.page_reader import PageReader


class ScrapeMushpedia:
    """Use case to scrape mushpedia.com."""

    def __init__(self, page_reader: PageReader) -> None:
        self.page_reader = page_reader

    def execute(self, mushpedia_links: list[str], workers: int = -1) -> list[str]:
        """Execute the use case on the given Mushpedia links.

        Args:
            mushpedia_links (list[str]): A list of Mushpedia article links.

        Returns:
            list[str]: A list of scrapped Mushpedia articles in HTML format.
        """
        results = []
        with ThreadPoolExecutor(max_workers=self._get_workers(workers)) as executor:
            # Submit all scraping tasks
            future_to_url = {executor.submit(self._scrap_page_reader, url): url for url in mushpedia_links}

            # Collect results as they complete
            for future in as_completed(future_to_url):
                try:
                    result = future.result()
                    results.append(result)
                except Exception as exc:
                    url = future_to_url[future]
                    print(f"Scraping generated an exception for {url}: {exc}")

        return results

    def _scrap_page_reader(self, page_reader_link: str) -> str:
        page_reader = BeautifulSoup(self.page_reader.get(page_reader_link), "html.parser")
        return page_reader.prettify()

    def _get_workers(self, workers: int) -> int:
        return cpu_count() if workers == -1 else min(workers, cpu_count())
