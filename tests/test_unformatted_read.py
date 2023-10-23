import io

import numpy as np
import pytest
import resfo._unformatted.read as uwrite


def test_unformatted_array_eof():
    buf = io.BytesIO(b"")
    arr = uwrite.UnformattedResArray(buf)
    assert arr.is_eof


@pytest.fixture
def simple_unformatted_buffer():
    return io.BytesIO(
        b"\x00\x00\x00\x10KEYWORD1\x00\x00\x00\x01INTE\x00\x00\x00\x10"
        b"\x00\x00\x00\x04\x00\x00\x00\x00\x00\x00\x00\x04"
    )


def test_unformatted_array_simple_read(simple_unformatted_buffer):
    arr = uwrite.UnformattedResArray(simple_unformatted_buffer)
    assert not arr.is_eof
    assert arr.read_keyword() == "KEYWORD1"
    assert arr.read_type() == b"INTE"
    assert arr.read_length() == 1
    assert np.array_equal(arr.read_array(), np.zeros(shape=(1,), dtype=">i4"))


def test_unformatted_array_simple_type_loads(simple_unformatted_buffer):
    arr = uwrite.UnformattedResArray(simple_unformatted_buffer)
    assert arr.read_type() == b"INTE"


def test_unformatted_array_simple_length_loads(simple_unformatted_buffer):
    arr = uwrite.UnformattedResArray(simple_unformatted_buffer)
    assert arr.read_length() == 1


def test_unformatted_array_big_read():
    buf = io.BytesIO(
        b"\x00\x00\x00\x10KEYWORD1"
        + (2300).to_bytes(4, byteorder="big")
        + b"INTE\x00\x00\x00\x10"
        + (
            (4000).to_bytes(4, byteorder="big")
            + b"\x00\x00\x00\x01" * 1000
            + (4000).to_bytes(4, byteorder="big")
        )
        * 2
        + (
            (4 * 300).to_bytes(4, byteorder="big")
            + b"\x00\x00\x00\x01" * 300
            + (4 * 300).to_bytes(4, byteorder="big")
        )
    )
    arr = uwrite.UnformattedResArray(buf)
    assert not arr.is_eof
    assert arr.read_keyword() == "KEYWORD1"
    assert arr.read_type() == b"INTE"
    assert arr.read_length() == 2300
    assert np.array_equal(arr.read_array(), np.ones(shape=(2300,), dtype=">i4"))


def test_unformatted_array_bad_record_marker():
    buf = io.BytesIO(
        b"\x00\x00\x00\x10KEYWORD1"
        + (2300).to_bytes(4, byteorder="big")
        + b"INTE\x00\x00\x00\x10"
        + b"\x00" * (4 * 2300 + 4 * 6)
    )
    arr = uwrite.UnformattedResArray(buf)
    with pytest.raises(uwrite.ResfoParsingError, match="size of record"):
        arr.read_array()


def test_unformatted_array_read_record_marker():
    buf = io.BytesIO(b"\x00\x00\x00\x00")
    arr = uwrite.UnformattedResArray(buf)

    arr._read_record_marker(0)
    assert not buf.read(1)
    buf.seek(0)

    with pytest.raises(uwrite.ResfoParsingError, match="size of record"):
        arr._read_record_marker(1)


def test_unformatted_array_bad_initial_marker():
    buf = io.BytesIO(b"\x00\x00\x00\x01KEYWORD1")
    arr = uwrite.UnformattedResArray(buf)

    with pytest.raises(uwrite.ResfoParsingError, match="size of record"):
        arr.read_keyword()


def test_unformatted_array_bad_middle_marker():
    buf = io.BytesIO(b"\x00\x00\x00\x10KEYWORD1\x00\x00\x00\x00INTE\x00\x00\x00\x01")
    arr = uwrite.UnformattedResArray(buf)

    with pytest.raises(uwrite.ResfoParsingError, match="size of record"):
        arr.read_keyword()


def test_unformatted_array_eof_during_keyword():
    buf = io.BytesIO(b"\x00\x00\x00\x10A")
    arr = uwrite.UnformattedResArray(buf)

    with pytest.raises(
        uwrite.ResfoParsingError, match="end-of-file while reading keyword"
    ):
        arr.read_keyword()


def test_unformatted_array_eof_during_length():
    buf = io.BytesIO(b"\x00\x00\x00\x10AKEYWORD\x00")
    arr = uwrite.UnformattedResArray(buf)

    with pytest.raises(
        uwrite.ResfoParsingError, match="end-of-file while reading length"
    ):
        arr.read_keyword()


def test_unformatted_array_eof_during_type():
    buf = io.BytesIO(b"\x00\x00\x00\x10AKEYWORD\x00\x00\x00\x00T")
    arr = uwrite.UnformattedResArray(buf)

    with pytest.raises(
        uwrite.ResfoParsingError, match="end-of-file while reading type"
    ):
        arr.read_keyword()


@pytest.mark.parametrize(
    "typestr, size, value, pyvalue",
    [
        (b"INTE", 4, b"\x00" * 4, 0),
        (b"REAL", 4, b"\x00" * 4, 0.0),
        (b"LOGI", 4, b"\x00" * 4, 0),
        (b"DOUB", 8, b"\x00" * 8, 0.0),
        (b"CHAR", 8, b"A8STRING", b"A8STRING"),
        (b"C011", 11, b"HELLO WORLD", b"HELLO WORLD"),
    ],
)
def test_unformatted_array_types(typestr, size, value, pyvalue):
    buf = io.BytesIO(
        b"\x00\x00\x00\x10AKEYWORD\x00\x00\x00\x01"
        + typestr
        + b"\x00\x00\x00\x10"
        + size.to_bytes(4, signed=True, byteorder="big")
        + value
        + size.to_bytes(4, signed=True, byteorder="big")
    )
    arr = uwrite.UnformattedResArray(buf)

    assert arr.read_keyword() == "AKEYWORD"
    assert np.array_equal(arr.read_array(), np.array([pyvalue]))


def test_unformatted_array_non_type():
    buf = io.BytesIO(b"\x00\x00\x00\x10AKEYWORD\x00\x00\x00\x01TYPE\x00\x00\x00\x10")
    arr = uwrite.UnformattedResArray(buf)

    with pytest.raises(uwrite.ResfoParsingError, match="Unexpected item type"):
        arr.read_keyword()


def test_unformatted_array_bad_end_marker():
    buf = io.BytesIO(b"\x00\x00\x00\x10AKEYWORD\x00\x00\x00\x01INTE\x00\x00\x10\x10")
    arr = uwrite.UnformattedResArray(buf)

    with pytest.raises(uwrite.ResfoParsingError, match="size of record"):
        arr.read_keyword()


def test_unformatted_array_zero_len():
    buf = io.BytesIO(b"\x00\x00\x00\x10AKEYWORD\x00\x00\x00\x00INTE\x00\x00\x00\x10")
    arr = uwrite.UnformattedResArray(buf)
    assert arr.read_keyword() == "AKEYWORD"
    assert len(arr.read_array()) == 0


def test_unformatted_simple_unformatted_parse():
    buf = io.BytesIO(
        (
            b"\x00\x00\x00\x10KEYWORD1\x00\x00\x00\x01INTE\x00\x00\x00\x10"
            b"\x00\x00\x00\x04\x00\x00\x00\x00\x00\x00\x00\x04"
        )
        * 10
    )
    for arr in uwrite.UnformattedResArray.parse(buf):
        assert not arr.is_eof
        assert arr.read_keyword() == "KEYWORD1"
        assert arr.read_type() == b"INTE"
        assert arr.read_length() == 1
        assert np.array_equal(arr.read_array(), np.zeros(shape=(1,), dtype=">i4"))

    buf.seek(0)

    assert len(list(uwrite.UnformattedResArray.parse(buf))) == 10


def test_unformatted_x231_parse():
    """
    This test simply tests the math of the X231 reading, but
    relies on the lazy evaluation to avoid having an array
    with 5,000,000,000 elements follow the two records
    defining the array.
    """
    buf = io.BytesIO(
        (
            (16).to_bytes(4, byteorder="big", signed=True)
            + b"KEYWORD1"
            + (-2).to_bytes(4, byteorder="big", signed=True)
            + b"X231"
            + (16).to_bytes(4, byteorder="big", signed=True)
            + (16).to_bytes(4, byteorder="big", signed=True)
            + b"KEYWORD1"
            + (705032704).to_bytes(4, byteorder="big", signed=True)
            + b"INTE"
            + (16).to_bytes(4, byteorder="big", signed=True)
        )
    )
    for arr in uwrite.UnformattedResArray.parse(buf):
        assert not arr.is_eof
        assert arr.read_keyword() == "KEYWORD1"
        assert arr.read_type() == b"INTE"
        assert arr.read_length() == 5000000000

    buf.seek(0)

    assert len(list(uwrite.UnformattedResArray.parse(buf))) == 1


def test_unformatted_x231_wrong_kw():
    buf = io.BytesIO(
        (
            (16).to_bytes(4, byteorder="big", signed=True)
            + b"KEYWORD1"
            + (-1).to_bytes(4, byteorder="big", signed=True)
            + b"X231"
            + (16).to_bytes(4, byteorder="big", signed=True)
            + (16).to_bytes(4, byteorder="big", signed=True)
            + b"KEYWORD2"
            + (1).to_bytes(4, byteorder="big", signed=True)
            + b"INTE"
            + (16).to_bytes(4, byteorder="big", signed=True)
        )
    )
    with pytest.raises(uwrite.ResfoParsingError, match="x231 type record"):
        list(uwrite.UnformattedResArray.parse(buf))


def test_unformatted_parse_mess():
    buf = io.BytesIO(
        (
            (16).to_bytes(4, byteorder="big", signed=True)
            + b"KEYWORD1"
            + (0).to_bytes(4, byteorder="big", signed=True)
            + b"MESS"
            + (16).to_bytes(4, byteorder="big", signed=True)
        )
    )

    for arr in uwrite.UnformattedResArray.parse(buf):
        assert not arr.is_eof
        assert arr.read_keyword() == "KEYWORD1"
        assert arr.read_type() == b"MESS"
        assert arr.read_length() == 0

    buf.seek(0)

    assert len(list(uwrite.UnformattedResArray.parse(buf))) == 1
