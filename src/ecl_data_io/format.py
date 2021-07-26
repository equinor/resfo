import io
from enum import Enum, auto, unique
from pathlib import Path


@unique
class Format(Enum):
    """
    The format of an ecl file, either FORMATTED for ascii
    or UNFORMATTED for binary.
    """

    FORMATTED = auto()
    UNFORMATTED = auto()


def guess_format(filelike):
    """
    Guess the format of a given filelike.

    If given a filename or pathlib.Path the guess is based on
    seeing if the first 4 bytes are a fortran marker. If given
    a stream, assumes byte stream means Format.FORMATTED and
    text stream means Format.UNFORMATTED.

    :param filelike: Either a filename, pathlib.Path or opened stream.
    :returns: Either Format.FORMATTED or Format.UNFORMATTED.
    """
    if isinstance(filelike, (Path, str)):
        with open(filelike, "rb") as file_handle:
            if int.from_bytes(file_handle.read(4), byteorder="big", signed=True) == 16:
                return Format.UNFORMATTED
            else:
                return Format.FORMATTED
    goback = filelike.tell()
    bytes_or_str = filelike.read(1)
    filelike.seek(goback)
    if isinstance(bytes_or_str, bytes):
        return Format.UNFORMATTED
    else:
        return Format.FORMATTED


def get_stream(filepath, fileformat, mode="r"):
    """
    Openes the given file with the correct mode (text or binary)
    based on fileformat.
    :param filepath: Either a filename or pathlib.Path
    :param fileformat: A ecl_data_io.Format.
    :returns: The opened file.
    """
    if isinstance(filepath, (str, Path)):
        if fileformat == Format.FORMATTED:
            return open(filepath, mode + "t"), True
        else:
            return open(filepath, mode + "b"), True
    else:
        return filepath, False


def check_correct_mode(stream, fileformat):
    """
    Checks that the stream is the correct mode (text or binary) for the given
    fileformat.
    """
    if isinstance(stream, io.TextIOBase) and fileformat == Format.UNFORMATTED:
        raise ValueError(
            "Formatted file was opened in byte reading mode, should be text mode"
        )
