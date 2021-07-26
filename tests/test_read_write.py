import sys
from os.path import join

import hypothesis.strategies as st
import numpy as np
import pytest
from hypothesis import HealthCheck, given, settings
from hypothesis.extra.numpy import arrays
from numpy.testing import assert_allclose

from ecl_data_io import Format, read, write

formats = st.sampled_from(Format)
in_formats = st.one_of(formats, st.just(None))
keywords = st.text(
    min_size=8, max_size=8, alphabet=st.characters(min_codepoint=40, max_codepoint=126)
)

unicode_arrays = st.builds(np.array, st.lists(keywords))
str_arrays = st.builds(lambda arr: arr.astype("|S"), unicode_arrays)
int_arrays = arrays(dtype=np.int32, shape=(10,))
float_arrays = arrays(
    dtype=np.float64,
    elements=st.floats(width=64, min_value=-1e100, max_value=1e100),
    shape=(10,),
)

ecl_arrays = st.one_of(float_arrays, int_arrays, str_arrays, unicode_arrays)
ecl_datas = st.lists(st.tuples(keywords, ecl_arrays))


@pytest.fixture(params=["file", "path"])
def filelike(request, tmp_path, tmpdir):
    if request.param == "file":
        return join(tmpdir, "test.txt")
    if request.param == "path":
        return tmp_path / "testpath.txt"


def same_keyword(a, b):
    return a.strip() == b.strip()


@pytest.mark.skipif(
    sys.version_info < (3, 7), reason="Hypothesis requires python3.7 or higher"
)
@settings(suppress_health_check=[HealthCheck.function_scoped_fixture])
@given(file_format=formats, data=ecl_datas)
def test_read_write(filelike, file_format, data):
    write(filelike, data, fileformat=file_format)
    for (kw, arr), (okw, oarr) in zip(data, read(filelike)):
        assert same_keyword(kw, okw)
        if len(arr) == 0 and len(oarr) == 0:
            continue
        if isinstance(arr[0], bytes):
            arr = np.array([el.decode("ascii") for el in arr])
        if isinstance(oarr[0], bytes):
            oarr = np.array([el.decode("ascii") for el in oarr])

        if np.issubdtype(arr.dtype, np.inexact):
            assert_allclose(arr, oarr)
        else:
            assert np.array_equal(arr, oarr)
