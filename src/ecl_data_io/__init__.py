import ecl_data_io.version

from .errors import EclParsingError, EclWriteError
from .format import Format
from .read import lazy_read, read
from .types import MESS
from .write import write

__author__ = "Equinor"
__email__ = "fg_sib-scout@equinor.com"

__version__ = ecl_data_io.version.version

__all__ = [
    "read",
    "lazy_read",
    "write",
    "Format",
    "MESS",
    "EclParsingError",
    "EclWriteError",
]
