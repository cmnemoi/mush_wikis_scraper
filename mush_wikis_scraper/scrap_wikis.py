import asyncio
from typing import Callable, Optional, TypedDict

import trafilatura
from bs4 import BeautifulSoup
from markdownify import MarkdownConverter  # type: ignore

from mush_wikis_scraper.page_reader import PageReader

ProgressCallback = Callable[[float | None], bool | None]
ScrapingResult = TypedDict("ScrapingResult", {"title": str, "link": str, "source": str, "content": str})


class ScrapWikis:
    def __init__(self, page_reader: PageReader, progress_callback: Optional[ProgressCallback] = None) -> None:
        """Scraper for eMushpedia, Aide aux Bolets and Mush Forums.

        Args:
            page_reader (PageReader): The page reader to use.
            progress_callback (Callable[[int], None], optional): A callback to call with the progress of the scrapping. Defaults to None.
            Adapters available are currently `FileSystemPageReader` and `HttpPageReader` from the `adapter` module.
        """
        self.page_reader = page_reader
        self.progress_callback = progress_callback

    async def execute(self, wiki_links: list[str], format: str = "html") -> list[ScrapingResult]:
        """Execute the use case on the given links.

        Args:
            wiki_links (list[str]): A list of wiki article links.
            format (str, optional): The format of the output. Defaults to "html".

        Returns:
            list[ScrapingResult]: A list of scrapped wiki articles with article title, link and content in selected format.
        """
        tasks = [self._scrap_page(link, format) for link in wiki_links]
        results = await asyncio.gather(*tasks)
        return list(results)

    async def _scrap_page(self, page_reader_link: str, format: str) -> ScrapingResult:
        page_parser = BeautifulSoup(await self.page_reader.get(page_reader_link), "html.parser")
        if self.progress_callback is not None:
            self.progress_callback(1)

        match format:
            case "html":
                content = page_parser.prettify().replace("\n", "")
            case "text":
                content = page_parser.get_text()
            case "markdown":
                content = MarkdownConverter().convert_soup(page_parser)
            case "trafilatura-markdown":
                content = trafilatura.extract(
                    page_parser.prettify(), include_formatting=True, output_format="markdown"
                )  # type: ignore
            case "trafilatura-html":
                content = trafilatura.extract(page_parser.prettify(), include_formatting=True, output_format="html")  # type: ignore
            case "trafilatura-text":
                content = trafilatura.extract(page_parser.prettify(), include_formatting=True, output_format="txt")  # type: ignore
            case _:
                raise ValueError(f"Unknown format: {format}")

        return {
            "title": self._get_title_from(page_reader_link, page_parser),
            "link": page_reader_link,
            "source": self._get_source_from_link(page_reader_link),
            "content": content,  # type: ignore
        }

    def _get_source_from_link(self, link: str) -> str:
        if "emushpedia" in link:
            return "eMushpedia"
        elif "archive_aide_aux_bolets" in link:
            return "Aide aux Bolets"
        elif "twinoid-archives.netlify.app" in link:
            return "Mush Forums"
        else:
            raise ValueError(f"Unknown source for link: {link}")  # pragma: no cover

    def _get_title_from(self, link: str, page_parser: BeautifulSoup) -> str:
        source = self._get_source_from_link(link)
        parts = link.split("/")

        if source == "eMushpedia":
            return parts[-1].replace("_", " ").capitalize()

        if source in ("Aide aux Bolets", "Mush Forums"):
            tag = page_parser.select_one("span.tid_title")
            if tag is None:
                raise ValueError(
                    f"No title found for Aide aux Bolets article or Mush Forums thread: {link}"
                )  # pragma: no cover

            return tag.text

        raise ValueError(f"Unknown source for link: {link}")  # pragma: no cover
