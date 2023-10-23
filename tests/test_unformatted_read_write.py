import io

import numpy as np
import pytest

from resfo._unformatted.read import UnformattedResArray
from resfo._unformatted.write import unformatted_write


@pytest.mark.filterwarnings("ignore:casting")
@pytest.mark.filterwarnings("ignore:downcasting")
@pytest.mark.parametrize("container", [dict, lambda x: x])
@pytest.mark.parametrize(
    "data",
    [
        [("KEYWORD1", [1, 2, 3])],
        [("KEYWORD1", [""])],
        [
            ("KEYWORD1", [1, 2, 3]),
            ("22222222", np.array([1.1, 2.1, 3.1])),
        ],
        [
            ("KEYWORD1", np.array([1, 2, 3])),
            ("KEYWORD2", [1.0, 2.0, 3.0]),
        ],
        [
            ("KEYWORS1", np.array(["HELLO WORLD"], dtype="|S")),
            ("KEYWORS2", np.array(["HELLO WORLD"], dtype="|S11")),
            ("KEYWORU1", np.array(["HELLO WORLD"], dtype="|U")),
            ("KEYWORU2", np.array(["HELLO WORLD"], dtype="|U11")),
        ],
    ],
)
def test_unformatted_write(container, data):
    buf = io.BytesIO()
    unformatted_write(buf, container(data))
    buf.seek(0)
    out_records = list(UnformattedResArray.parse(buf))
    out_keywords = [r.read_keyword() for r in out_records]
    out_arrays = [r.read_array() for r in out_records]
    out_lengths = [r.read_length() for r in out_records]

    assert out_lengths == [len(arr) for arr in out_arrays]

    for (kw, arr), okw, oarr in zip(data, out_keywords, out_arrays):
        assert kw == okw
        if isinstance(arr[0], str):
            for el, elo in zip(arr, oarr):
                elo = elo.decode("ascii")
                assert elo.startswith(el)
                assert all(c.isspace() for c in elo[len(el) :])
        else:
            assert np.array_equal(arr, oarr)
