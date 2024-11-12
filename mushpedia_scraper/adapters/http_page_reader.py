import httpx

from mushpedia_scraper.ports.page_reader import PageReader


class HttpPageReader(PageReader):
    def get(self, page_link: str) -> str:
        return httpx.get(page_link, timeout=10).text
