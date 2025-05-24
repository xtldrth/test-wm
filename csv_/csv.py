from collections.abc import Generator
from io import TextIOWrapper


class CSV:
    def __init__(self, *files_paths: str):
        self.files: list[TextIOWrapper] | None = None
        self.files_paths = files_paths

    def open(self):
        if self.files is None:
            self.files = []
        for path in self.files_paths:
            self.files.append(open(path, encoding="UTF-8"))

    def close(self):
        for file in self.files:
            if file.closed:
                continue
            file.close()

    def __enter__(self, *args) -> "CSV":
        self.open()
        return self

    def __exit__(self, *args):
        self.close()

    def get_rows(self) -> Generator[dict[str, str], None, None]:
        for file in self.files:
            header_fields = file.readline().split(",")
            while row := file.readline():
                yield {
                    field.strip(): value.strip()
                    for field, value in zip(header_fields, row.split(","))
                }
