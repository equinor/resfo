from dataclasses import dataclass

from ecl_data_io.errors import ParsingError

from .record import Record
from .split_line import split_line
from .subparser import SubParser


class ColumnsSubParser(SubParser):
    @property
    def keyword(self):
        return "COLUMN"

    def parse(self, super_parser, lines):
        try:
            contents = []
            while True:
                for word in split_line(next(lines)):
                    if word[0] == "/":
                        if len(contents != 2):
                            raise ParsingError("Expected 2 values in columns record")
                        left = int(contents[0])
                        right = int(contents[1])
                        super_parser.col_start = left
                        super_parser.col_end = right
                        yield Record("COLUMN", [left, right])
                        return

        except StopIteration as e:
            raise ParsingError("Reached end of file while parsing COLUMNS") from e
