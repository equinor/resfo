import sys

import numpy as np
import pytest
from hypothesis import HealthCheck, given, settings
from numpy.testing import assert_allclose

from ecl_data_io import read, write

from .generators import ecl_datas, formats


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
