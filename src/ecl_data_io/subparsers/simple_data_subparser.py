from dataclasses import dataclass
from itertools import takewhile
from typing import List

from ecl_data_io.errors import ParsingError

from .subparser import SubParser


@dataclass
class SimpleDataRecord:
    keyword: str
    data: List[str]


class SimpleDataSubParser(SubParser):
    def __init__(self, keyword):
        self._keyword = keyword

    @property
    def keyword(self):
        return self._keyword

    def parse(self, super_parser, lines):
        try:
            contents = []
            while True:
                for word in next(lines).split():
                    if word[0] == "/":
                        yield SimpleDataRecord(self.keyword, contents)
                        return
                    contents.append(word)

        except StopIteration as e:
            raise ParsingError(
                f"Reached end of file while parsing keyword {self.keyword}"
            ) from e
