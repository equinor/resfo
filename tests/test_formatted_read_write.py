import io

import numpy as np
import pytest

from ecl_data_io._formatted.read import FormattedEclArray
from ecl_data_io._formatted.write import formatted_write


@pytest.mark.parametrize("container", [dict, lambda x: x])
@pytest.mark.parametrize(
    "data",
    [
        [("KEYWORD1", [1, 2, 3])],
        [("KEYWORD1", [1, 2, 3]), ("22222222", np.array([1.1, 2.1, 3.1]))],
        [
            ("KEYWORD1", np.array([1, 2, 3])),
            ("KEYWORD2", [1.0, 2.0, 3.0]),
        ],
        [
            ("KEYWORDS", np.array(["HELLO WORLD"], dtype="|S")),
            ("KEYWORDU", np.array(["HELLO WORLD"], dtype="|U")),
            ("KEYWORDU", np.array(["HELLO WORLD"], dtype="|U11")),
        ],
    ],
)
def test_formatted_write(container, data, tmp_path):

    with (tmp_path / "test.data").open("wt") as fh:
        formatted_write(fh, container(data))

    with (tmp_path / "test.data").open("rt") as fh:
        out_records = list(FormattedEclArray.parse(fh))
        out_keywords = [r.read_keyword() for r in out_records]
        out_arrays = [r.read_array() for r in out_records]

    for (kw, arr), okw, oarr in zip(data, out_keywords, out_arrays):
        assert kw == okw
        if isinstance(arr[0], bytes):
            assert np.array_equal([el.decode("ascii") for el in arr], oarr)
        else:
            assert np.array_equal(arr, oarr)
