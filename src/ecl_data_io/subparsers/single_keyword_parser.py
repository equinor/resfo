from dataclasses import dataclass
from itertools import takewhile
from typing import List

from ecl_data_io.errors import ParsingError

from .subparser import SubParser


@dataclass
class SingleKeywordRecord:
    keyword: str


class SingleKeywordSubParser(SubParser):
    def __init__(self, keyword):
        self._keyword = keyword

    @property
    def keyword(self):
        return self._keyword

    def parse(self, super_parser, lines):
        return iter([])
