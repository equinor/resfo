from dataclasses import dataclass
from itertools import takewhile
from typing import List

from ecl_data_io.errors import ParsingError


@dataclass
class DoubleDataRecord:
    keyword: str
    data: List[List[str]]


class DoubleDataSubParser:
    def __init__(self, keyword):
        self.keyword = keyword

    def match(self, line):
        return line[0 : min(len(line), 8)].rstrip() == self.keyword

    def parse(self, super_parser, lines):
        try:
            contents = [[]]
            while True:
                for word in next(lines).split():
                    if word[0] == "/":
                        if contents[-1]:
                            contents.append([])
                        else:
                            yield DoubleDataRecord(self.keyword, contents)
                            return
                    contents[-1].append(word)

        except StopIteration as e:
            raise ParsingError(
                f"Reached end of file while parsing keyword {self.keyword}"
            ) from e
