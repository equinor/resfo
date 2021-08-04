import hypothesis.strategies as st
import pytest
from ecl_data_io._unformatted.common import bytes_in_array, group_len, item_size
from hypothesis import given


def test_group_len():
    assert group_len(b"C032") == 105
    assert group_len(b"CHAR") == 105
    assert group_len(b"INTE") == 1000
    assert group_len(b"REAL") == 1000
    assert group_len(b"LOGI") == 1000
    assert group_len(b"DOUB") == 1000
    assert group_len(b"MESS") == 1000
    assert group_len(b"x321") == 1000


def test_item_size():
    assert item_size(b"C032") == 32
    assert item_size(b"CHAR") == 8
    assert item_size(b"INTE") == 4
    assert item_size(b"REAL") == 4
    assert item_size(b"LOGI") == 4
    assert item_size(b"DOUB") == 8
    assert item_size(b"MESS") == 0
    assert item_size(b"x231") is None


def test_bytes_in_array():
    assert bytes_in_array(1000, b"DOUB") == 8008
    assert bytes_in_array(1000, b"REAL") == 4008
    assert bytes_in_array(900, b"REAL") == 900 * 4 + 8
    assert bytes_in_array(1100, b"REAL") == 1000 * 4 + 8 + 100 * 4 + 8
    assert bytes_in_array(0, b"REAL") == 0


@pytest.mark.parametrize(
    "item_type",
    [
        b"C032",
        b"CHAR",
        b"INTE",
        b"REAL",
        b"LOGI",
        b"DOUB",
    ],
)
@given(length=st.integers(min_value=1, max_value=104))
def test_bytes_in_array_one_group(item_type, length):
    assert bytes_in_array(length, item_type) == 8 + length * item_size(item_type)
