from abc import ABC, abstractmethod
from pathlib import Path

import httpx


class PageReader(ABC):
    @abstractmethod
    def get(self, path: str) -> str:
        pass  # pragma: no cover


class HttpPageReader(PageReader):
    def get(self, path: str) -> str:
        return httpx.get(path, timeout=60, follow_redirects=True).text


class FileSystemPageReader(PageReader):
    def get(self, path: str) -> str:
        file_path = Path(path)
        target_path = file_path if file_path.is_file() else None

        if target_path is None:
            alternative_path = file_path.with_name(file_path.name.replace("-", "_"))
            if alternative_path.is_file():
                target_path = alternative_path
            else:
                raise FileNotFoundError(path)

        with open(target_path, "r") as file:
            return file.read()
