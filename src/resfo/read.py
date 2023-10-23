from typing import TYPE_CHECKING, Iterator, List, Optional, Tuple

from resfo._formatted.read import FormattedArray
from resfo._unformatted.read import UnformattedResArray
from resfo.array_entry import ResArray
from resfo.format import Format, check_correct_mode, get_stream, guess_format

if TYPE_CHECKING:
    from .types import ReadArrayValue


def read(*args, **kwargs) -> List[Tuple[str, "ReadArrayValue"]]:
    """
    Read the contents of a res file and return a list of
    tuples (keyword, array). Takes the same parameters as
    lazy_read, but differs in return type
    """
    return [
        (arr.read_keyword(), arr.read_array()) for arr in lazy_read(*args, **kwargs)
    ]


def lazy_read(filelike, fileformat: Optional[Format] = None) -> Iterator[ResArray]:
    """
    Reads the contents of an res file and generates the entries
    of that file. Each entry has a entry.read_keyword() and
    entry.read_array() method which will return the corresponding
    data, but only upon request. This requires the user to
    pay attention to when values are read as it should happen
    before the file is closed.

    When lazy_read is given a path or filename, the file will be closed once
    the generator has ran out of elements.

    For greater control, one can pass an opened file so that close
    can be called at the correct time.

    :param filelike: Either filename, pathlib.Path or stream
        to write file to. For fileformat=Format.UNFORMATTED the
        stream must be in binary mode and for fileformat=Format.FORMATTED
        in text mode.
    :param fileformat: Either resfo.Format.FORMATTED for ascii
        format, resfo.Format.UNFORMATTED for binary formatted files
        or None for guess.

    :raises resfo.ResfoParsingError: If the file is not a valid
        res file.

    .. note::
        If given a file to be open (as opposed to a stream), the errors
        (various `IOError` s) associated with the default behavior of the
        built-in `open()` function may be raised.

        When given a stream, the exceptions associated with the stream will
        pass through.
    """
    if fileformat is None:
        fileformat = guess_format(filelike)
    stream, didopen = get_stream(filelike, fileformat)

    check_correct_mode(stream, fileformat)

    try:
        if fileformat == Format.FORMATTED:
            yield from FormattedArray.parse(stream)
        else:
            yield from UnformattedResArray.parse(stream)
    finally:
        if didopen:
            stream.close()
