from typing import Dict, Sequence, Tuple, Union

from resfo._formatted.write import formatted_write
from resfo._unformatted.write import unformatted_write
from resfo.format import Format, check_correct_mode, get_stream

from .types import WriteArrayValue


def write(
    filelike,
    contents: Union[Sequence[Tuple[str, WriteArrayValue]], Dict[str, WriteArrayValue]],
    fileformat: Format = Format.UNFORMATTED,
):
    """
    Write the given contents to the given file in res format.

    :param filelike: Either filename, pathlib.Path or stream
        to write file to. For fileformat=Format.UNFORMATTED the
        stream must be in binary mode and for fileformat=Format.FORMATTED
        in text mode.
    :param contents: list or iterable of tuples (kw, arr) where keyword
        is the keyword, and arr is a numpy arraylike of values. The
        keyword must have exactly 8 characters and the type of the array
        will be converted according to resfo.types.to_np_type
    :param fileformat: Either resfo.Format.FORMATTED for ascii
        format or resfo.Format.UNFORMATTED for binary format.

    :raises resfo.ResfoWriteError: If the given contents cannot be
        written to an res file.

    .. note::
        If given a file to be open (as opposed to a stream), the errors
        (various `IOError` s) associated with the default behavior of the
        built-in `open()` function may be raised.

        When given a stream, the exceptions associated with the stream will
        pass through.
    """
    stream, didopen = get_stream(filelike, fileformat, mode="w")

    check_correct_mode(stream, fileformat)

    if fileformat == Format.FORMATTED:
        formatted_write(stream, contents)
    else:
        unformatted_write(stream, contents)

    if didopen:
        stream.close()
