"""Scraper for the French, English, and Spanish eMushpedia wikis."""

from .links_fetcher import EmushpediaApiFetcher, HttpClient, HttpResponse
from .page_reader import FileSystemPageReader, HttpPageReader
from .scrap_wikis import ScrapWikis

__all__ = [
    "EmushpediaApiFetcher",
    "FileSystemPageReader",
    "HttpClient",
    "HttpPageReader",
    "HttpResponse",
    "ScrapWikis",
]
