"""Functions for reading page content from different sources."""

from typing import Callable

import httpx

PageReader = Callable[[str], str]


def read_from_filesystem(path: str) -> str:
    """Read page content from the filesystem.

    Args:
        path: Path to the file to read

    Returns:
        The content of the file
    """
    with open(path, "r") as file:
        return file.read()


def read_from_http(url: str) -> str:
    """Read page content from an HTTP URL.

    Args:
        url: URL to read from

    Returns:
        The content of the page
    """
    return httpx.get(url, timeout=60, follow_redirects=True).text
