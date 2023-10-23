import io

import hypothesis.strategies as st
import numpy as np
import pytest
from hypothesis import HealthCheck, given, settings

from resfo import MESS, lazy_read, read, write

from .generators import resfo_datas, float_arrays, keywords


@settings(suppress_health_check=[HealthCheck.function_scoped_fixture])
@given(data=st.lists(st.tuples(keywords, float_arrays)))
def test_update(filelike, data):
    data_zeros = [(kw, np.zeros(array.shape, dtype=array.dtype)) for kw, array in data]

    write(filelike, data_zeros)
    with open(filelike, "br+") as stream:
        for entry, (kw, arr) in zip(lazy_read(stream), data):
            assert kw == entry.read_keyword()
            entry.update(keyword="NEW_NAME")
            assert entry.read_array().tolist() == [0] * arr.size
            assert entry.read_keyword() == "NEW_NAME"
            entry.update(array=arr)
            assert entry.read_array().tolist() == pytest.approx(arr.tolist())


def test_update_mismatching_array_raises(filelike):
    write(filelike, [("KEYWORD1", [True, False])])

    with open(filelike, "br+") as stream:
        reader = lazy_read(stream)
        entry = next(reader)

        with pytest.raises(ValueError, match="different size"):
            entry.update(array=[True])

        with pytest.raises(ValueError, match="different type"):
            entry.update(array=["a", "b"])


def test_update_incorrect_mode_raises(filelike):
    write(filelike, [("KEYWORD1", [True, False])])

    with open(filelike, "br") as stream:
        entry = next(lazy_read(stream))
        with pytest.raises(io.UnsupportedOperation):
            entry.update(array=[False, False])


@settings(suppress_health_check=[HealthCheck.function_scoped_fixture])
@given(data=resfo_datas)
def test_update_preserves_type(filelike, data):
    write(filelike, data)
    with open(filelike, "br+") as stream:
        for (kw, arr), entry in zip(data, lazy_read(stream)):
            entry.update(keyword=kw, array=arr)

    for (kw, arr), (okw, oarr) in zip(data, read(filelike)):
        assert kw == okw
        if arr is MESS:
            continue
        if arr.dtype.type == np.str_:
            # Allow reading to result in bytestring instead of string
            assert oarr.dtype.type in [np.dtype("S8").type, np.dtype("<U8").type]
        else:
            assert arr.dtype.type == oarr.dtype.type
