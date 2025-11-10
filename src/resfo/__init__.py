from .errors import ResfoParsingError, ResfoWriteError
from .format import Format
from .read import lazy_read, read
from .types import MESS, ArrayValue, MessType
from .version import __version__
from .write import write

__author__ = "Equinor"
__email__ = "fg_sib-scout@equinor.com"

__all__ = [
    "read",
    "lazy_read",
    "write",
    "Format",
    "MESS",
    "MessType",
    "ResfoParsingError",
    "ResfoWriteError",
    "ArrayValue",
    "__version__",
]
