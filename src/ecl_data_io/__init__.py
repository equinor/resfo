import ecl_data_io.version

from .format import Format
from .read import lazy_read, read
from .write import write

__author__ = "Equinor"
__email__ = "fg_sib-scout@equinor.com"

__version__ = ecl_data_io.version.version

__all__ = ["read", "lazy_read", "write", "Format"]
