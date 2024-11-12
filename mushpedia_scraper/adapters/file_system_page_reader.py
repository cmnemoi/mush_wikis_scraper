from ..ports.page_reader import PageReader


class FileSystemPageReader(PageReader):
    def get(self, path: str) -> str:
        with open(path, "r") as file:
            return file.read()
