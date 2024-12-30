"""Scraper for http://mushpedia.com/, http://twin.tithom.fr/mush/, https://cmnemoi.github.io/archive_aide_aux_bolets/ and QA Mush forum threads."""

from .page_reader import FileSystemPageReader, HttpPageReader
from .scrap_wikis import ScrapWikis

__all__ = [
    "FileSystemPageReader",
    "HttpPageReader",
    "ScrapWikis",
]
