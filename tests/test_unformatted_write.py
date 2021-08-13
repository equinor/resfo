import io

import numpy as np
import pytest

import ecl_data_io._unformatted.write as ecl_unf_write


def test_write_array_header():
    buf = io.BytesIO()
    ecl_unf_write.write_array_header(buf, "KEYWORD1", b"INTE", 3)

    assert (
        buf.getvalue()
        == b"\x00\x00\x00\x10KEYWORD1\x00\x00\x00\x03INTE\x00\x00\x00\x10"
    )


def test_write_array_header_with_x231():
    buf = io.BytesIO()
    ecl_unf_write.write_array_header(buf, "KEYWORD1", b"INTE", 5000000000)

    marker = (16).to_bytes(4, byteorder="big", signed=True)
    assert buf.getvalue() == (
        marker
        + b"KEYWORD1"
        + (-2).to_bytes(4, byteorder="big", signed=True)
        + b"X231"
        + marker
        + marker
        + b"KEYWORD1"
        + (705032704).to_bytes(4, byteorder="big", signed=True)
        + b"INTE"
        + marker
    )


def test_write_array_header_short_keyword():
    buf = io.BytesIO()

    with pytest.raises(ValueError, match="must have length"):
        ecl_unf_write.write_array_header(buf, "KEY", b"INTE", 3)


def test_write_array_header_not_a_type():
    buf = io.BytesIO()

    with pytest.raises(ecl_unf_write.EclWriteError, match="a valid ecl type"):
        ecl_unf_write.write_array_header(buf, "KEYWORD1", b"NOTY", 3)


@pytest.mark.parametrize(
    "array, expected_array",
    [
        (np.array([1], dtype=np.int32), np.array([1], dtype=np.int32)),
        (np.array([1.0], dtype=np.float32), np.array([1.0], dtype=np.float32)),
        (np.array([1.0], dtype=np.float64), np.array([1.0], dtype=np.float64)),
        (np.array([True, False], dtype=np.bool_), np.array([1, 0], dtype=np.int32)),
        (np.array([10, 20], dtype=np.int8), np.array([10, 20], dtype=np.int32)),
        (np.array([1.0], dtype=np.float128), np.array([1.0], dtype=np.float64)),
    ],
)
def test_cast_array_to_ecl(array, expected_array):
    assert np.array_equal(ecl_unf_write.cast_array_to_ecl(array), expected_array)


def test_cast_array_to_ecl_bad_type():
    array = np.array([b"ABC"], dtype="|S")
    with pytest.raises(ValueError, match="Cannot cast"):
        ecl_unf_write.cast_array_to_ecl(array)


def test_write_np_array():
    buf = io.BytesIO()
    ecl_unf_write.write_np_array(
        buf, np.ones(shape=(1300,), dtype=np.dtype(np.int32).newbyteorder(">"))
    )

    assert buf.getvalue() == (
        (
            (4000).to_bytes(4, byteorder="big", signed=True)
            + b"\x00\x00\x00\x01" * 1000
            + (4000).to_bytes(4, byteorder="big", signed=True)
        )
        + (
            (1200).to_bytes(4, byteorder="big", signed=True)
            + b"\x00\x00\x00\x01" * 300
            + (1200).to_bytes(4, byteorder="big", signed=True)
        )
    )


def test_write_str_list_too_long():
    buf = io.BytesIO()
    str_list = ["a" * 200]

    with pytest.raises(ValueError, match="strings of length"):
        ecl_unf_write.write_str_list(buf, str_list, b"CHAR")


def test_write_str_list_non_ascii():
    buf = io.BytesIO()
    str_list = ["\u2167"]

    with pytest.raises(ValueError, match="non-ascii"):
        ecl_unf_write.write_str_list(buf, str_list, b"CHAR")


def test_write_str_list_char():
    buf = io.BytesIO()
    str_list = ["a" * 8, "b" * 4]

    ecl_unf_write.write_str_list(buf, str_list, b"CHAR")

    marker = (16).to_bytes(4, byteorder="big", signed=True)

    assert buf.getvalue() == marker + b"a" * 8 + b"b" * 4 + b" " * 4 + marker
