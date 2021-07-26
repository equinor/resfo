from ecl_data_io._unformatted.common import group_len, item_size


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
