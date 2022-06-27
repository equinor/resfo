import hypothesis.strategies as st
import numpy as np
from hypothesis.extra.numpy import arrays

from ecl_data_io import Format

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
