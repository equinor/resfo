import numpy as np
import pytest
import resfo


@pytest.mark.parametrize(
    "contents, expected_type",
    [
        ("'SPECGRID' 1 'INTE' 1 ", np.dtype(np.int32).newbyteorder(">")),
        ("'SPECGRID' 1 'REAL' 1.0 ", np.dtype(np.float32).newbyteorder(">")),
        ("'SPECGRID' 1 'DOUB' 1.0 ", np.dtype(np.float64).newbyteorder(">")),
        ("'SPECGRID' 1 'CHAR' 'SPECGRID' ", np.dtype("<U8")),
        ("'SPECGRID' 1 'C010' 'SPECGRID99' ", np.dtype("<U10")),
        ("'SPECGRID' 1 'LOGI' T ", bool),
    ],
)
def test_formatted_read_type_resolution(tmp_path, contents, expected_type):
    with (tmp_path / "test.txt").open("w") as f:
        f.write(contents)

    with (tmp_path / "test.txt").open("r") as f:
        ((specgrid, arr),) = resfo.read(f)

    assert arr.dtype == expected_type


@pytest.mark.parametrize(
    "data, expected_type",
    [
        (["KEYWORD1"], "'CHAR'"),
        (["KEYWORD10"], "'C009'"),
        ([1], "'INTE'"),
        ([1.0], "'DOUB'"),
        (np.array([1.0], dtype=np.float32), "'REAL'"),
        ([True], "'LOGI'"),
    ],
)
def test_formatted_write_type_resolution(tmp_path, data, expected_type):
    file = tmp_path / "test.txt"

    with file.open("w") as f:
        resfo.write(f, {"SPECGRID": data}, resfo.Format.FORMATTED)

    assert expected_type in file.read_text()


def keyword_start(res_type):
    return b"\x00\x00\x00\x10SPECGRID\x00\x00\x00\x01" + res_type + b"\x00\x00\x00\x10"


@pytest.mark.parametrize(
    "contents, expected_type",
    [
        (
            keyword_start(b"INTE")
            + b"\x00\x00\x00\x04\x00\x00\x00\x00\x00\x00\x00\x04",
            np.dtype(np.int32).newbyteorder(">"),
        ),
        (
            keyword_start(b"REAL")
            + b"\x00\x00\x00\x04\x00\x00\x00\x00\x00\x00\x00\x04",
            np.dtype(np.float32).newbyteorder(">"),
        ),
        (
            keyword_start(b"DOUB")
            + b"\x00\x00\x00\x08"
            + b"\x00" * 8
            + b"\x00\x00\x00\x08",
            np.dtype(np.float64).newbyteorder(">"),
        ),
        (
            keyword_start(b"CHAR")
            + b"\x00\x00\x00\x08"
            + b"SPECGRID"
            + b"\x00\x00\x00\x08",
            np.dtype("|S8"),
        ),
        (
            keyword_start(b"C010")
            + b"\x00\x00\x00\x0A"
            + b"SPECGRID10"
            + b"\x00\x00\x00\x0A",
            np.dtype("|S10"),
        ),
        (
            keyword_start(b"LOGI")
            + b"\x00\x00\x00\x04\x00\x00\x00\x00\x00\x00\x00\x04",
            bool,
        ),
    ],
)
def test_unformatted_read_type_resolution(tmp_path, contents, expected_type):
    with (tmp_path / "test.txt").open("wb") as f:
        f.write(contents)

    with (tmp_path / "test.txt").open("rb") as f:
        ((specgrid, arr),) = resfo.read(f)

    assert arr.dtype == expected_type


@pytest.mark.parametrize(
    "data, expected_type",
    [
        (["KEYWORD1"], b"CHAR"),
        (["KEYWORD10"], b"C009"),
        ([1], b"INTE"),
        ([1.0], b"DOUB"),
        (np.array([1.0], dtype=np.float32), b"REAL"),
        ([True], b"LOGI"),
    ],
)
def test_unformatted_write_type_resolution(tmp_path, data, expected_type):
    file = tmp_path / "test.txt"

    with file.open("wb") as f:
        resfo.write(f, {"SPECGRID": data}, resfo.Format.UNFORMATTED)

    assert expected_type in file.read_bytes()
