from io import BytesIO, StringIO

import pytest
from ecl_data_io import EclParsingError, EclWriteError, Format, read, write


def test_invalid_formatted_content():
    file_contents = StringIO("Not valid ecl content")
    with pytest.raises(EclParsingError, match='Expected "\'"'):
        read(file_contents)


def test_invalid_unformatted_content():
    file_contents = BytesIO(b"\x00" * 100)
    with pytest.raises(EclParsingError, match="Unexpected size of record"):
        read(file_contents)


@pytest.mark.parametrize(
    "buffer, format", [(BytesIO(), Format.UNFORMATTED), (StringIO(), Format.FORMATTED)]
)
def test_invalid_read_content(buffer, format):
    with pytest.raises(EclWriteError, match="Could not convert"):
        write(buffer, [("FILEHEAD", "a" * 100)], format)


def test_invalid_keyword():
    with pytest.raises(EclWriteError, match="keywords"):
        write(StringIO(), [("'", ["a" * 8])], Format.FORMATTED)
