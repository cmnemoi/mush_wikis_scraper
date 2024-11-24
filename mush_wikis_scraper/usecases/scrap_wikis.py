from concurrent.futures import ThreadPoolExecutor
from multiprocessing import cpu_count
from typing import Callable, Optional, TypedDict

from bs4 import BeautifulSoup
from markdownify import MarkdownConverter  # type: ignore

from mush_wikis_scraper.ports.page_reader import PageReader

ProgressCallback = Callable[[float | None], bool | None]
ScrapingResult = TypedDict("ScrapingResult", {"title": str, "link": str, "source": str, "content": str})


class ScrapWikis:
    def __init__(self, page_reader: PageReader, progress_callback: Optional[ProgressCallback] = None) -> None:
        """Scraper for Mushpedia and Twinpedia.

        Args:
            page_reader (PageReader): The page reader to use.
            progress_callback (Callable[[int], None], optional): A callback to call with the progress of the scrapping. Defaults to None.
            Adapters available are currently `FileSystemPageReader` and `HttpPageReader` from the `adapter` module.
        """
        self.page_reader = page_reader
        self.progress_callback = progress_callback

    def execute(self, wiki_links: list[str], max_workers: int = -1, format: str = "html") -> list[ScrapingResult]:
        """Execute the use case on the given links.

        Args:
            wiki_links (list[str]): A list of wiki article links.
            max_workers (int, optional): The maximum number of workers to use. Defaults to -1, which will use 2 * number of CPUs cores available.
            format (str, optional): The format of the output. Defaults to "html".

        Returns:
            list[ScrapingResult]: A list of scrapped wiki articles with article title, link and content in selected format.
        """
        nb_workers = self._get_workers(max_workers, wiki_links)
        with ThreadPoolExecutor(max_workers=nb_workers) as executor:
            results = list(executor.map(self._scrap_page, wiki_links, [format] * len(wiki_links)))

        return [result for result in results]

    def _scrap_page(self, page_reader_link: str, format: str) -> ScrapingResult:
        page_parser = BeautifulSoup(self.page_reader.get(page_reader_link), "html.parser")
        if self.progress_callback is not None:
            self.progress_callback(1)

        match format:
            case "html":
                content = page_parser.prettify().replace("\n", "")
            case "text":
                content = page_parser.get_text()
            case "markdown":
                content = MarkdownConverter().convert_soup(page_parser)
            case _:
                raise ValueError(f"Unknown format: {format}")

        return {
            "title": self._get_title_from(page_reader_link, page_parser),
            "link": page_reader_link,
            "source": self._get_source_from_link(page_reader_link),
            "content": content,
        }

    def _get_workers(self, max_workers: int, wiki_links: list[str]) -> int:
        workers = max_workers if max_workers > 0 else 2 * cpu_count()

        return min(workers, len(wiki_links))

    def _get_source_from_link(self, link: str) -> str:
        if "mushpedia" in link:
            return "Mushpedia"
        elif "twin.tithom.fr" in link:
            return "Twinpedia"
        elif "archive_aide_aux_bolets" in link:
            return "Aide aux Bolets"
        elif "twinoid-archives.netlify.app" in link:
            return "Mush Forums"
        else:
            raise ValueError(f"Unknown source for link: {link}")  # pragma: no cover

    def _get_title_from(self, link: str, page_parser: BeautifulSoup) -> str:
        source = self._get_source_from_link(link)
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
                    raise ValueError(f"Unknown source for link: {link}")  # pragma: no cover

        if source == "Aide aux Bolets" or source == "Mush Forums":
            tag = page_parser.select_one("span.tid_title")
            if tag is None:
                raise ValueError(
                    f"No title found for Aide aux Bolets article or Mush Forums thread: {link}"
                )  # pragma: no cover

            return tag.text

        raise ValueError(f"Unknown source for link: {link}")  # pragma: no cover
