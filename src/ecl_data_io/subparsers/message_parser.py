from dataclasses import dataclass
from itertools import takewhile
from typing import List

from ecl_data_io.errors import ParsingError

from .subparser import SubParser


@dataclass
class MessageRecord:
    message: str


class MessageSubParser(SubParser):
    @property
    def keyword(self):
        return "MESSAGE"

    def parse(self, super_parser, lines):
        try:
            yield MessageRecord(next(lines))
        except StopIteration as e:
            raise ParsingError("Reached end of file while parsing MESSAGE") from e
