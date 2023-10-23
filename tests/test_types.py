import numpy as np
import resfo.types


def test_resfo_to_np_type():
    assert resfo.types.to_np_type(b"C032") == np.dtype("|S32")
    assert resfo.types.to_np_type(b"CHAR") == np.dtype("|S8")
    assert resfo.types.to_np_type(b"INTE") == np.dtype(">i4")
    assert resfo.types.to_np_type(b"REAL") == np.dtype(">f4")
    assert resfo.types.to_np_type(b"LOGI") == np.dtype(">i4")
    assert resfo.types.to_np_type(b"DOUB") == np.dtype(">f8")
    assert resfo.types.to_np_type(b"MESS") is None
    assert resfo.types.to_np_type(b"x321") is None


def test_from_np_dtype():
    assert resfo.types.from_np_dtype(np.array([], dtype=np.dtype("|S32"))) == b"C032"
    assert resfo.types.from_np_dtype(np.array([], dtype=np.dtype("|S8"))) == b"CHAR"
    assert resfo.types.from_np_dtype(np.array([], dtype=np.dtype(">i4"))) == b"INTE"
    assert resfo.types.from_np_dtype(np.array([], dtype=np.dtype(">f4"))) == b"REAL"
    assert resfo.types.from_np_dtype(np.array([], dtype=np.dtype(np.bool_))) == b"LOGI"
    assert resfo.types.from_np_dtype(np.array([], dtype=np.dtype(">f8"))) == b"DOUB"
    assert resfo.types.from_np_dtype(resfo.types.MESS) == b"MESS"
    assert (
        resfo.types.from_np_dtype(np.array(["HELLO WORLD"], dtype=np.dtype("|S")))
        == b"C011"
    )
