import io

import numpy as np
import resfo._formatted.read as fread


def test_drop_while_space():
    buf = io.StringIO("  a  ")
    fread.drop_while_space(buf)
    assert buf.read(1) == "a"
    fread.drop_while_space(buf)
    assert not buf.read(1)


def test_formatted_array_eof():
    buf = io.StringIO("")
    arr = fread.FormattedArray(buf)
    assert arr.is_eof


def test_simple_array_read(tmp_path):
    contents = "'SPECGRID' 4 'INTE' 40 64 14 1 "

    with (tmp_path / "test.txt").open("w") as f:
        f.write(contents)

    with (tmp_path / "test.txt").open("r") as f:
        arr = fread.FormattedArray(f)

        assert arr.read_type() == b"INTE"
        assert arr.read_length() == 4
        assert arr.read_keyword() == "SPECGRID"
        assert np.array_equal(arr.read_array(), [40, 64, 14, 1])


def test_simple_char_array_read(tmp_path):
    contents = "'CHARARR1' 2 'CHAR' 'HELLO   ' 'WORLD   ' "

    with (tmp_path / "test.txt").open("w") as f:
        f.write(contents)

    with (tmp_path / "test.txt").open("r") as f:
        arr = fread.FormattedArray(f)

        assert arr.read_type() == b"CHAR"
        assert arr.read_length() == 2
        assert arr.read_keyword() == "CHARARR1"
        assert np.array_equal(arr.read_array(), ["HELLO   ", "WORLD   "])


def test_simple_logi_array_read(tmp_path):
    contents = "'KEYWORD1' 2 'LOGI' T F "

    with (tmp_path / "test.txt").open("w") as f:
        f.write(contents)

    with (tmp_path / "test.txt").open("r") as f:
        arr = fread.FormattedArray(f)

        assert arr.read_type() == b"LOGI"
        assert arr.read_length() == 2
        assert arr.read_keyword() == "KEYWORD1"
        assert np.array_equal(arr.read_array(), [True, False])
