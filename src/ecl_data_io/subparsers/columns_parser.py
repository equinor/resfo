from dataclasses import dataclass

from ecl_data_io.errors import ParsingError

from .subparser import SubParser


@dataclass
class ColumnsRecord:
    left: int
    right: int


class ColumnsSubParser(SubParser):
    @property
    def keyword(self):
        return "COLUMN"

    def parse(self, super_parser, lines):
        try:
            contents = []
            while True:
                for word in next(lines).split():
                    if word[0] == "/":
                        if len(contents != 2):
                            raise ParsingError("Expected 2 values in columns record")
                        left = int(contents[0])
                        right = int(contents[1])
                        super_parser.col_start = left
                        super_parser.col_end = right
                        yield ColumnsRecord(left, right)
                        return

        except StopIteration as e:
            raise ParsingError("Reached end of file while parsing COLUMNS") from e
