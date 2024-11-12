from abc import ABC, abstractmethod


class PageReader(ABC):
    @abstractmethod
    def get(self, path: str) -> str:
        pass
