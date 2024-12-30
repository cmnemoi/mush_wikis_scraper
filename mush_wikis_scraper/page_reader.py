from abc import ABC, abstractmethod

import httpx


class PageReader(ABC):
    @abstractmethod
    def get(self, path: str) -> str:
        pass  # pragma: no cover


class HttpPageReader(PageReader):
    def get(self, page_link: str) -> str:
        return httpx.get(page_link, timeout=60, follow_redirects=True).text


class FileSystemPageReader(PageReader):
    def get(self, path: str) -> str:
        with open(path, "r") as file:
            return file.read()
