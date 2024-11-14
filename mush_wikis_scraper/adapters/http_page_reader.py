import httpx

from mush_wikis_scraper.ports.page_reader import PageReader


class HttpPageReader(PageReader):
    def get(self, page_link: str) -> str:
        return httpx.get(page_link, timeout=60, follow_redirects=True).text
