from dataclasses import dataclass
from itertools import takewhile
from typing import List

from ecl_data_io.errors import ParsingError

from .record import Record
from .split_line import split_line


class FixedRecordSubParser:
    def __init__(self, keyword, num_getter):
        self.keyword = keyword

    def match(self, line):
        return line[0 : min(len(line), 8)].rstrip() == self.keyword

    def parse(self, super_parser, lines):
        num = self.num_getter(super_parser)
        try:
            contents = [[]]
            while True:
                for word in split_line(next(lines)):
                    if word[0] == "/":
                        if len(contents) == num:
                            yield Record(self.keyword, contents)
                            return
                        contents.append([])
                    contents[-1].append(word)

        except StopIteration as e:
            raise ParsingError(
                f"Reached end of file while parsing keyword {self.keyword}"
            ) from e


FIXED_RECORD_KEYWORDS = [
    ("IMPFILE", lambda x: 2),
    ("TUNING", lambda x: 3),
    ("TUNINGL", lambda x: 3),
    ("PRORDER", lambda x: 2),
]
