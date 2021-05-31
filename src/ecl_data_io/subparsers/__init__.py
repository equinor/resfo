from .columns_parser import ColumnsSubParser
from .one_line_parser import OneLineSubParser
from .simple_data_subparser import SimpleDataSubParser
from .single_keyword_parser import SingleKeywordSubParser
from .skip_parser import SkipSubParser

DEFAULT_SUBPARSERS = [
    OneLineSubParser("MESSAGE"),
    ColumnsSubParser(),
    SkipSubParser("SKIP"),
    SkipSubParser("SKIP100"),
    SingleKeywordSubParser("ENDSKIP"),
    SingleKeywordSubParser("SKIP300"),
]
COMMON_SUBPARSERS = [
    SimpleDataSubParser("GDORIENT"),
    SimpleDataSubParser("SPECGRID"),
    SimpleDataSubParser("COORD"),
    SimpleDataSubParser("ZCORN"),
    SimpleDataSubParser("ACTNUM"),
    SimpleDataSubParser("DIMENS"),
    SimpleDataSubParser("GRIDOPTS"),
    SingleKeywordSubParser("OIL"),
    SingleKeywordSubParser("WATER"),
    SingleKeywordSubParser("GAS"),
    SingleKeywordSubParser("DISGAS"),
    SingleKeywordSubParser("VAPOIL"),
    SingleKeywordSubParser("NOECHO"),
    SingleKeywordSubParser("ECHO"),
    SingleKeywordSubParser("RUNSPEC"),
    SingleKeywordSubParser("GRID"),
    SingleKeywordSubParser("EDIT"),
    SingleKeywordSubParser("PROPS"),
    SingleKeywordSubParser("REGIONS"),
    SingleKeywordSubParser("SOLUTION"),
    SingleKeywordSubParser("SUMMARY"),
    SingleKeywordSubParser("SCHEDULE"),
    SingleKeywordSubParser("END"),
]
