from io import BytesIO, StringIO

import pytest
from resfo import Format, ResfoParsingError, ResfoWriteError, read, write


def test_invalid_formatted_content():
    file_contents = StringIO("Not valid res content")
    with pytest.raises(ResfoParsingError, match='Expected "\'"'):
        read(file_contents)


def test_invalid_unformatted_content():
    file_contents = BytesIO(b"\x00" * 100)
    with pytest.raises(ResfoParsingError, match="Unexpected size of record"):
        read(file_contents)


@pytest.mark.parametrize(
    "buffer, format", [(BytesIO(), Format.UNFORMATTED), (StringIO(), Format.FORMATTED)]
)
def test_invalid_read_content(buffer, format):
    with pytest.raises(ResfoWriteError, match="Could not convert"):
        write(buffer, [("FILEHEAD", "a" * 100)], format)


def test_invalid_keyword():
    with pytest.raises(ResfoWriteError, match="keywords"):
        write(StringIO(), [("'", ["a" * 8])], Format.FORMATTED)
