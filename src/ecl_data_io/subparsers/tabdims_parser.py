from dataclasses import dataclass
from typing import Optional

from ecl_data_io.errors import ParsingError
from ecl_data_io.subparsers.subparser import SubParser


@dataclass
class TabdimsRecord:
    ntsfun: int = 1
    ntpvt: int = 1
    nssfun: int = 50
    nppvt: int = 50
    ntfip: int = 1
    nrpvt: int = 20
    nrvpvt: int = 20
    ntendp: int = 1
    nmeosr: int = 1
    nmeoss: Optional[int] = None
    mxnflx: int = 10
    mxnthr: int = 10
    ntrocc: Optional[int] = None
    mxnpmr: int = 0
    ntabkt: int = 0
    ntalpha: Optional[int] = None
    naspka: int = 10
    maxrawg: int = 10
    maxraso: int = 10
    _not_used_: Optional[int] = None
    mcaspp: int = 5
    mraspp: int = 5
    mxratf: int = 5
    mxnkvt: int = 0
    _reserved_: int = 0

    @property
    def keyword(self):
        return "TABDIMS"


class TabdimsSubParser(SubParser):
    def __init__(self):
        self.last_record = TabdimsRecord()

    @property
    def keyword(self):
        return "TABDIMS"

    def parse(self, super_parser, lines):
        try:
            contents = []
            while True:
                for word in next(lines).split():
                    if word[0] == "/":
                        if len(contents) > 25:
                            raise ParsingError("Too many values in tabdim record")
                        yield TabdimsRecord([int(c) for c in contents])
                        return
                    contents.append(word)

        except StopIteration as e:
            raise ParsingError(
                f"Reached end of file while parsing keyword {self.keyword}"
            ) from e
