import resfo.version

from .errors import ResfoParsingError, ResfoWriteError
from .format import Format
from .read import lazy_read, read
from .types import MESS
from .write import write

__author__ = "Equinor"
__email__ = "fg_sib-scout@equinor.com"

__version__ = resfo.version.version

__all__ = [
    "read",
    "lazy_read",
    "write",
    "Format",
    "MESS",
    "ResfoParsingError",
    "ResfoWriteError",
]
