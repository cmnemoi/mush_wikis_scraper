import asyncio
import logging
from typing import Callable, Optional, TypedDict, cast

import trafilatura
from bs4 import BeautifulSoup
from markdownify import MarkdownConverter  # type: ignore

from mush_wikis_scraper.page_reader import PageReader

logger = logging.getLogger(__name__)

ProgressCallback = Callable[[float | None], bool | None]
ScrapingResult = TypedDict("ScrapingResult", {"title": str, "link": str, "source": str, "content": str})


class ScrapWikis:
    def __init__(
        self, page_reader: PageReader, progress_callback: Optional[ProgressCallback] = None, max_concurrent: int = 10
    ) -> None:
        """Scraper for eMushpedia, Aide aux Bolets and Mush Forums.

        Args:
            page_reader (PageReader): The page reader to use.
            progress_callback (Callable[[int], None], optional): A callback to call with the progress of the scrapping. Defaults to None.
            max_concurrent (int, optional): Maximum number of concurrent requests. Defaults to 10.
            Adapters available are currently `FileSystemPageReader` and `HttpPageReader` from the `adapter` module.
        """
        self.page_reader = page_reader
        self.progress_callback = progress_callback
        self.max_concurrent = max_concurrent
        self._semaphore: asyncio.Semaphore | None = None

    async def execute(self, wiki_links: list[str], format: str = "html") -> list[ScrapingResult]:
        """Execute the use case on the given links.

        Args:
            wiki_links (list[str]): A list of wiki article links.
            format (str, optional): The format of the output. Defaults to "html".

        Returns:
            list[ScrapingResult]: A list of scrapped wiki articles with article title, link and content in selected format.
                Failed pages are logged as warnings and excluded from results.

        Raises:
            ValueError: If the format is not supported.
        """
        # Validate format upfront before executing
        valid_formats = {"html", "text", "markdown", "trafilatura-markdown", "trafilatura-html", "trafilatura-text"}
        if format not in valid_formats:
            raise ValueError(f"Unknown format: {format}")

        self._semaphore = asyncio.Semaphore(self.max_concurrent)
        tasks = [self._scrap_page(link, format) for link in wiki_links]
        results = await asyncio.gather(*tasks, return_exceptions=True)

        # Filter out exceptions and log them
        processed_results: list[ScrapingResult] = []
        for i, result in enumerate(results):
            if isinstance(result, Exception):
                logger.warning(f"Failed to scrape page {wiki_links[i]}: {str(result)}")
            else:
                # Type narrowing: we know result is ScrapingResult here
                processed_results.append(cast(ScrapingResult, result))

        return processed_results

    async def _scrap_page(self, page_reader_link: str, format: str) -> ScrapingResult:
        async with self._semaphore:  # type: ignore
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
                    content = trafilatura.extract(
                        page_parser.prettify(), include_formatting=True, output_format="html"
                    )  # type: ignore
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
