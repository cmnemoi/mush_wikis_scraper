import asyncio
from abc import ABC, abstractmethod
from pathlib import Path

import httpx


class PageReader(ABC):
    @abstractmethod
    async def get(self, path: str) -> str:
        pass  # pragma: no cover


class HttpPageReader(PageReader):
    async def get(self, path: str) -> str:
        async with httpx.AsyncClient(timeout=60, follow_redirects=True) as client:
            response = await client.get(path)
            return response.text


class FileSystemPageReader(PageReader):
    async def get(self, path: str) -> str:
        return await asyncio.to_thread(self._read_file, path)

    def _read_file(self, path: str) -> str:
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
