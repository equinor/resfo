from dataclasses import dataclass
from typing import Optional

from ecl_data_io.errors import ParsingError
from ecl_data_io.subparsers.subparser import SubParser

from .fixed_record_parser import FixedRecordSubParser
from .split_line import split_line


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
    def values(self):
        return list(self)

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
                for word in split_line(next(lines)):
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


def get_nmeosr(super_parser):
    return super_parser.subparsers["TABDIMS"].last_record.nmeosr


def get_nmeoss(super_parser):
    return super_parser.subparsers["TABDIMS"].last_record.nmeoss


def get_nppvt(super_parser):
    return super_parser.subparsers["TABDIMS"].last_record.nppvt


def get_ntalpha(super_parser):
    return super_parser.subparsers["TABDIMS"].last_record.ntalpha


def get_ntcreg(super_parser):
    return super_parser.subparsers["TABDIMS"].last_record.ntcreg


def get_ntpvt(super_parser):
    return super_parser.subparsers["TABDIMS"].last_record.ntpvt


def get_ntsfun(super_parser):
    return super_parser.subparsers["TABDIMS"].last_record.ntsfun


tabdims_keywords = [
    ("ACF", get_nmeosr),
    ("ACFDET", get_nmeosr),
    ("ACFS", get_nmeoss),
    ("ADSALNOD", get_ntsfun),
    ("ADSORP", lambda x: get_ntsfun(x) + 1),
    ("ALKADS", get_ntsfun),
    ("ALKROCK", get_ntsfun),
    ("ALPHA", get_ntalpha),
    ("ALPHAD", get_ntalpha),
    ("ALPHAI", get_ntalpha),
    ("ALPOLADS", get_ntsfun),
    ("ALSURFAD", get_ntsfun),
    ("ALSURFST", get_nppvt),
    ("ASPKROW", get_ntsfun),
    ("BDENSITY", get_ntpvt),
    ("BIC", get_nmeosr),
    ("CTYPE", get_nmeosr),
    ("CTYPES", get_nmeosr),
    ("CGDTYPE", get_nmeosr),
    ("CGVTYPE", get_nmeosr),
    ("COALADS", get_ntcreg),
    ("CODTYPE", get_nmeosr),
    ("COVTYPE", get_nmeosr),
    ("CREF", get_nmeosr),
    ("CREFW", get_nmeosr),
    ("CREFWS", get_nmeoss),
    ("CVTYPE", get_nmeosr),
    ("CVTYPES", get_nmeoss),
    ("DENAQA", get_nmeosr),
    ("DIFFC", get_ntpvt),
    ("DPKRMOD", get_ntsfun),
    ("DREF", get_nmeosr),
    ("DREFS", get_nmeoss),
    ("DREFW", get_nmeosr),
    ("DREFWS", get_nmeoss),
    ("DRSDTR", get_ntpvt),
    ("EHYSTRR", get_ntsfun),
    ("ENKRVC", get_ntsfun),
    ("ENKRVT", get_ntsfun),
    ("ENPCVC", get_ntsfun),
    ("ENPTVC", get_ntsfun),
    ("ENPCVT", get_ntsfun),
    ("ENPTVT", get_ntsfun),
    ("EOS", get_nmeosr),
    ("EOSS", get_nmeoss),
    ("EPSODD3P", get_ntsfun),
    ("ESPNODE", get_ntpvt),
    ("ESSNODE", get_ntpvt),
    ("FOAMADS", get_ntsfun),
    ("FOAMDCYO", get_ntsfun),
    ("FOAMFRM", get_ntsfun),
    ("FOAMFSC", get_ntsfun),
    ("FOAMFST", get_ntsfun),
    ("FOAMFSW", get_ntsfun),
    ("FOAMMOB", get_ntpvt),
    ("FOAMMOBP", get_ntpvt),
    ("FOAMMOBS", get_ntpvt),
    ("FOAMROCK", get_ntsfun),
    ("GINODE", get_ntpvt),
    ("GRAVITY", get_ntpvt),
    ("GREF", get_nmeosr),
    ("GREFS", get_nmeoss),
    ("HEATVAP", get_nmeosr),
    ("HEATVAPE", get_nmeosr),
    ("HEATVAPS", get_nmeosr),
    ("HYDRO", get_nmeosr),
    ("IONXROCK", get_ntsfun),
    ("IONXSURF", get_ntsfun),
    ("JFUNCR", get_ntsfun),
    ("KRGDI", get_ntsfun),
    ("KRGDM", get_ntsfun),
    ("KRODI", get_ntsfun),
    ("KRODM", get_ntsfun),
    ("KRWDI", get_ntsfun),
    ("KRWDM", get_ntsfun),
    ("KVAN", get_nmeosr),
    ("KVCR", get_nmeosr),
    ("KVCRS", get_nmeoss),
    ("KVCRWAT", get_nmeoss),
    ("LANGMUIR", get_ntcreg),
    ("LANGSOLV", get_ntcreg),
    ("LBCCOEFR", get_nmeosr),
    ("LSALTFNC", get_ntsfun),
    ("MSFN", get_ntsfun),
    ("MW", get_nmeosr),
    ("MWDETAIL", get_nmeosr),
    ("MWS", get_nmeoss),
    ("MWW", get_nmeosr),
    ("MWWS", get_nmeoss),
    ("OILVINDX", get_ntpvt),
    ("OILVISCF", get_nmeosr),
    ("OILVISCT", get_ntpvt),
    ("OMEGAA", get_nmeosr),
    ("OMEGAADE", get_nmeosr),
    ("OMEGAAS", get_nmeoss),
    ("OMEGAASD", get_nmeoss),
    ("OMEGAB", get_nmeosr),
    ("OMEGABS", get_nmeoss),
    ("OMEGABSD", get_nmeoss),
    ("PCODD3P", get_ntsfun),
    ("PCODD3PG", get_ntsfun),
    ("PCODD3PW", get_ntsfun),
    ("PCRIT", get_nmeosr),
    ("PCRITDET", get_nmeosr),
    ("PCRITS", get_nmeoss),
    ("PCRITSDE", get_nmeoss),
    ("PEDTUNER", get_nmeosr),
    ("PLYADS", get_ntsfun),
    ("PLYDHFLF", get_ntpvt),
    ("PLYESAL", get_ntsfun),
    ("PLYROCK", get_ntsfun),
    ("PLYROCKM", get_ntsfun),
    ("PLYSHEAR", get_ntpvt),
    ("PLYSHLOG", lambda x: 2 * get_ntpvt(x)),
    ("PLYTRRF", get_ntsfun),
    ("PLYVISC", get_ntpvt),
    ("PPCWMAX", get_ntsfun),
    ("PREF", get_nmeosr),
    ("PREFS", get_nmeoss),
    ("PREFT", get_nmeosr),
    ("PREFTS", get_nmeoss),
    ("PREFWS", get_nmeoss),
    ("PVCDO", get_ntpvt),
    ("PVCO", get_ntpvt),
    ("PVDG", get_ntpvt),
    ("PVDS", get_ntpvt),
    ("PVTW", get_ntpvt),
    ("PVTWSALT", lambda x: 2 * get_ntpvt(x)),
    ("PVZG", lambda x: 2 * get_ntpvt(x)),
    ("ROCK", get_ntpvt),
    ("RSCONSTT", get_ntpvt),
]
