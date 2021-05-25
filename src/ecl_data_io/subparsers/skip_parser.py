from dataclasses import dataclass
from itertools import takewhile

from ecl_data_io.errors import ParsingError

from .subparser import SubParser


@dataclass
class SkipRecord:
    keyword: str
    skipped_section: str


class SkipSubParser:
    def __init__(self, keyword="SKIP"):
        self._keyword = keyword

    @property
    def keyword(self):
        return self._keyword

    def parse(self, super_parser, lines):
        contents = ""
        try:
            while True:
                line = next(lines)
                if line.startswith("ENDSKIP"):
                    yield SkipRecord(self.keyword, contents)
                    return
                contents += line + "\n"
        except StopIteration as e:
            raise ParsingError(
                f"Reached end of file while parsing {self.keyword} keyword"
            ) from e
