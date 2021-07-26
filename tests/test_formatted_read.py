import io

import numpy as np

import ecl_data_io._formatted.read as ecl_read


def test_drop_while_space():
    buf = io.StringIO("  a  ")
    ecl_read.drop_while_space(buf)
    assert buf.read(1) == "a"
    ecl_read.drop_while_space(buf)
    assert not buf.read(1)


def test_formatted_ecl_array_eof():
    buf = io.StringIO("")
    ecl_arr = ecl_read.FormattedEclArray(buf)
    assert ecl_arr.is_eof


def test_simple_ecl_array_read(tmp_path):
    contents = "'SPECGRID' 4 'INTE' 40 64 14 1 "

    with (tmp_path / "test.txt").open("w") as f:
        f.write(contents)

    with (tmp_path / "test.txt").open("r") as f:
        ecl_arr = ecl_read.FormattedEclArray(f)

        assert ecl_arr.type == b"INTE"
        assert ecl_arr.length == 4
        assert ecl_arr.read_keyword() == "SPECGRID"
        assert np.array_equal(ecl_arr.read_array(), [40, 64, 14, 1])


def test_simple_ecl_char_array_read(tmp_path):
    contents = "'CHARARR1' 2 'CHAR' 'HELLO   ' 'WORLD   ' "

    with (tmp_path / "test.txt").open("w") as f:
        f.write(contents)

    with (tmp_path / "test.txt").open("r") as f:
        ecl_arr = ecl_read.FormattedEclArray(f)

        assert ecl_arr.type == b"CHAR"
        assert ecl_arr.length == 2
        assert ecl_arr.read_keyword() == "CHARARR1"
        assert np.array_equal(ecl_arr.read_array(), ["HELLO   ", "WORLD   "])


def test_simple_ecl_logi_array_read(tmp_path):
    contents = "'KEYWORD1' 2 'LOGI' T F "

    with (tmp_path / "test.txt").open("w") as f:
        f.write(contents)

    with (tmp_path / "test.txt").open("r") as f:
        ecl_arr = ecl_read.FormattedEclArray(f)

        assert ecl_arr.type == b"LOGI"
        assert ecl_arr.length == 2
        assert ecl_arr.read_keyword() == "KEYWORD1"
        assert np.array_equal(ecl_arr.read_array(), [True, False])
