import asyncio
from abc import ABC, abstractmethod
from pathlib import Path

import httpx


class PageReader(ABC):
    @abstractmethod
    async def get(self, path: str) -> str:
        pass  # pragma: no cover


class HttpPageReader(PageReader):
    def __init__(self, max_retries: int = 3, initial_delay: float = 1.0) -> None:
        """Initialize HttpPageReader with retry configuration.

        Args:
            max_retries (int): Maximum number of retry attempts. Defaults to 3.
            initial_delay (float): Initial delay in seconds between retries. Defaults to 1.0.
        """
        self.max_retries = max_retries
        self.initial_delay = initial_delay

    async def get(self, path: str) -> str:
        """Fetch page content from URL with retry logic.

        Args:
            path (str): URL to fetch

        Returns:
            str: Page content

        Raises:
            httpx.ConnectError: If connection fails after all retries
        """
        async with httpx.AsyncClient(timeout=60, follow_redirects=True) as client:
            return await self._get_with_client(client, path)

    async def _get_with_client(self, client: httpx.AsyncClient, path: str) -> str:
        """Fetch page content with exponential backoff retry logic.

        Args:
            client (httpx.AsyncClient): HTTP client to use
            path (str): URL to fetch

        Returns:
            str: Page content

        Raises:
            httpx.ConnectError: If connection fails after all retries
        """
        last_exception = None
        delay = self.initial_delay

        for attempt in range(self.max_retries + 1):
            try:
                response = await client.get(path)
                return response.text
            except httpx.ConnectError as e:
                last_exception = e
                if attempt < self.max_retries:
                    await asyncio.sleep(delay)
                    delay *= 2  # Exponential backoff

        raise last_exception  # type: ignore


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
