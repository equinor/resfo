import numpy as np

import ecl_data_io.types as ecl_io_types


def test_ecl_to_np_type():
    assert ecl_io_types.to_np_type(b"C032") == np.dtype("|S32")
    assert ecl_io_types.to_np_type(b"CHAR") == np.dtype("|S8")
    assert ecl_io_types.to_np_type(b"INTE") == np.dtype(">i4")
    assert ecl_io_types.to_np_type(b"REAL") == np.dtype(">f4")
    assert ecl_io_types.to_np_type(b"LOGI") == np.dtype(">i4")
    assert ecl_io_types.to_np_type(b"DOUB") == np.dtype(">f8")
    assert ecl_io_types.to_np_type(b"MESS") is None
    assert ecl_io_types.to_np_type(b"x321") is None


def test_from_np_dtype():
    assert ecl_io_types.from_np_dtype(np.array([], dtype=np.dtype("|S32"))) == b"C032"
    assert ecl_io_types.from_np_dtype(np.array([], dtype=np.dtype("|S8"))) == b"CHAR"
    assert ecl_io_types.from_np_dtype(np.array([], dtype=np.dtype(">i4"))) == b"INTE"
    assert ecl_io_types.from_np_dtype(np.array([], dtype=np.dtype(">f4"))) == b"REAL"
    assert ecl_io_types.from_np_dtype(np.array([], dtype=np.dtype(np.bool_))) == b"LOGI"
    assert ecl_io_types.from_np_dtype(np.array([], dtype=np.dtype(">f8"))) == b"DOUB"
    assert (
        ecl_io_types.from_np_dtype(np.array(["HELLO WORLD"], dtype=np.dtype("|S")))
        == b"C011"
    )
